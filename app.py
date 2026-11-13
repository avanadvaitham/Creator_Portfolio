#!/usr/bin/env python3
"""Four independent portfolio roots, one private SQLite-backed editor.

Public pages never require login. Editing requires Basic auth and CSRF. No
Instagram publishing, account login, paid hosting, analytics or email sending.
"""
from __future__ import annotations
from contextlib import contextmanager
from copy import deepcopy
from datetime import datetime, timezone
from functools import wraps
from hashlib import sha256
from io import BytesIO
import argparse
import base64
import hmac
import json
import math
import os
from pathlib import Path
import re
import secrets
import sqlite3
from urllib.parse import urlsplit, quote, urlencode, parse_qs
from zipfile import ZipFile, ZIP_DEFLATED
from flask import Flask, Response, abort, jsonify, render_template, request, send_file, send_from_directory
from PIL import Image, ImageOps, UnidentifiedImageError
from waitress import serve
from werkzeug.middleware.proxy_fix import ProxyFix
from werkzeug.security import generate_password_hash, check_password_hash
from seed_content import BRANDS, BRAND_ORDER, TAGS, initial_videos

ROOT=Path(__file__).resolve().parent
MAX_VIDEOS=500
MAIN_MEDIA=ROOT/'static'/'media'


def timestamp():
    return datetime.now(timezone.utc).isoformat(timespec='seconds')


def text(value, label, limit=300, required=False):
    if not isinstance(value,str):
        raise ValueError(label+' must be text.')
    value=value.strip()
    if required and not value:raise ValueError('Add '+label.lower()+'.')
    if len(value)>limit:raise ValueError(label+' is too long.')
    if re.search(r'[\x00-\x08\x0b\x0c\x0e-\x1f\ud800-\udfff]',value):raise ValueError(label+' contains an unsupported character.')
    return value


def media_path(value):
    value=text(value or '', 'Image path', 200)
    if value and (not re.fullmatch(r'[A-Za-z0-9_/-]+\.(?:webp|jpg|jpeg|png)',value) or '..' in value):
        raise ValueError('Choose a valid uploaded image.')
    return value


def canonical_video_url(value):
    value=text(value,'Video URL',2000,True)
    u=urlsplit(value)
    if u.scheme!='https' or not u.hostname or u.username or u.password or u.port not in (None,443):
        raise ValueError('Use a public HTTPS Instagram, YouTube or direct MP4/WebM link.')
    host=u.hostname.lower()
    if host in {'instagram.com','www.instagram.com'}:
        match=re.fullmatch(r'/(reel|p)/([A-Za-z0-9_-]{5,40})/?',u.path)
        if not match:raise ValueError('Use a specific Instagram reel or post link, not a profile.')
        kind='post' if match[1]=='p' else 'reel'
        return f'https://www.instagram.com/{match[1]}/{match[2]}/',kind,match[2]
    if host in {'www.youtube.com','youtube.com','m.youtube.com','youtu.be'}:
        code=''
        if host=='youtu.be':
            match=re.fullmatch(r'/([A-Za-z0-9_-]{11})/?',u.path)
            if match:code=match[1]
        elif u.path=='/watch':
            values=parse_qs(u.query).get('v',[])
            if len(values)==1:code=values[0]
        else:
            match=re.fullmatch(r'/shorts/([A-Za-z0-9_-]{11})/?',u.path)
            if match:code=match[1]
        if not re.fullmatch(r'[A-Za-z0-9_-]{11}',code):raise ValueError('Use one YouTube watch, Shorts or youtu.be video link, not a playlist/channel.')
        return 'https://www.youtube.com/watch?v='+code,'youtube',code
    if u.path.lower().endswith(('.mp4','.webm')):
        return value,'video',None
    raise ValueError('Use an Instagram post/reel, YouTube watch/Shorts, or direct HTTPS MP4/WebM link.')


def video_key(url):
    canonical,kind,code=canonical_video_url(url)
    return ('youtube',code) if kind=='youtube' else ('instagram',code) if kind in {'reel','post'} else ('video',canonical)


class Store:
    def __init__(self, directory):
        self.directory=Path(directory);self.directory.mkdir(parents=True,exist_ok=True)
        self.path=self.directory/'portfolio.sqlite3'
        self.uploads=self.directory/'uploads';self.uploads.mkdir(exist_ok=True)
        with self.connection() as c:
            c.execute('PRAGMA journal_mode=WAL')
            c.execute('CREATE TABLE IF NOT EXISTS settings (slug TEXT PRIMARY KEY, payload TEXT NOT NULL)')
            c.execute('CREATE TABLE IF NOT EXISTS videos (id TEXT PRIMARY KEY, payload TEXT NOT NULL)')
            c.execute('CREATE TABLE IF NOT EXISTS meta (key TEXT PRIMARY KEY, value TEXT NOT NULL)')
            c.execute('BEGIN IMMEDIATE')
            if not c.execute("SELECT value FROM meta WHERE key='initialised'").fetchone():
                for slug,b in BRANDS.items():c.execute('INSERT OR IGNORE INTO settings VALUES (?,?)',(slug,json.dumps(b,ensure_ascii=False)))
                for v in initial_videos():
                    v['rights_confirmed']=False;v['updated_at']=timestamp()
                    c.execute('INSERT OR IGNORE INTO videos VALUES (?,?)',(v['id'],json.dumps(v,ensure_ascii=False)))
                c.execute("INSERT INTO meta VALUES ('initialised',?)",(timestamp(),))
    @contextmanager
    def connection(self):
        c=sqlite3.connect(self.path,timeout=15)
        try:
            yield c;c.commit()
        except Exception:
            c.rollback();raise
        finally:c.close()
    def settings(self,slug):
        with self.connection() as c:r=c.execute('SELECT payload FROM settings WHERE slug=?',(slug,)).fetchone()
        if not r:raise ValueError('Portfolio not found.')
        return json.loads(r[0])
    def videos(self):
        with self.connection() as c:rows=c.execute('SELECT payload FROM videos').fetchall()
        return sorted([json.loads(r[0]) for r in rows],key=lambda v:(v.get('sort_order',999),v['id']))
    def public(self,slug):
        return self.settings(slug),[v for v in self.videos() if slug in v['brands'] and v['status']=='published']
    def save_settings(self,slug,payload):
        with self.connection() as c:c.execute('UPDATE settings SET payload=? WHERE slug=?',(json.dumps(payload,ensure_ascii=False),slug))
    def save_video(self,payload):
        with self.connection() as c:
            c.execute('BEGIN IMMEDIATE')
            rows=c.execute('SELECT id,payload FROM videos').fetchall()
            if any(row[0]!=payload['id'] and video_key(json.loads(row[1])['url'])==video_key(payload['url']) for row in rows):raise ValueError('This post is already saved; edit its assignments instead.')
            c.execute('INSERT INTO videos VALUES (?,?) ON CONFLICT(id) DO UPDATE SET payload=excluded.payload',(payload['id'],json.dumps(payload,ensure_ascii=False)))
    def remove(self,vid):
        with self.connection() as c:c.execute('DELETE FROM videos WHERE id=?',(vid,))
    def export(self):
        return {'schema_version':2,'exported_at':timestamp(),'brands':{s:self.settings(s) for s in BRAND_ORDER},'videos':self.videos()}


def validate_brand(raw,current):
    if not isinstance(raw,dict):raise ValueError('Send portfolio settings.')
    out=deepcopy(current)
    for k,lim in {'name':80,'wordmark':80,'eyebrow':100,'headline':160,'accent_line':100,'intro':650,'about_title':150,'about':1600,'hero_alt':200,'hero_caption':250,'gallery_note':500,'empty_note':500,'usage_note':1200,'booking_note':1200,'rate_note':1200,'achievements_note':650,'samples_status':250}.items():
        if k in raw:out[k]=text(raw[k],k.replace('_',' ').title(),lim,k in {'name','headline','intro'})
    for k in ['pillars','service_angles','languages']:
        if k in raw:
            values=raw[k]
            if not isinstance(values,list) or not 1<=len(values)<=8:raise ValueError('Add 1–8 '+k.replace('_',' ')+'.')
            out[k]=[text(v,k,90,True) for v in values]
    if 'email' in raw:
        value=text(raw['email'],'Business email',200)
        if value and not re.fullmatch(r'[^\s@<>]+@[^\s@<>]+\.[^\s@<>]+',value):raise ValueError('Use a valid public business email.')
        out['email']=value
    if 'whatsapp' in raw:
        value=text(raw['whatsapp'],'WhatsApp number',30)
        if value:
            value=re.sub(r'[\s()+-]','',value)
            if not re.fullmatch(r'\d{8,15}',value):raise ValueError('Use the WhatsApp number with country code, digits only.')
        out['whatsapp']=value
    if 'instagram' in raw:
        value=text(raw['instagram'],'Instagram profile',250)
        if value:
            u=urlsplit(value)
            if u.scheme!='https' or u.hostname not in {'www.instagram.com','instagram.com'} or not re.fullmatch(r'/[A-Za-z0-9_.]+/?',u.path):raise ValueError('Use the exact Instagram profile URL, or leave it blank.')
            value='https://www.instagram.com/'+u.path.strip('/')+'/'
        out['instagram']=value
    for k in ['hero_image']:
        if k in raw:out[k]=media_path(raw[k])
    for k in ['hero_illustrative','preview_mode','niche_rates_published']:
        if k in raw:
            if not isinstance(raw[k],bool):raise ValueError(k+' must be true or false.')
            out[k]=raw[k]
    if 'rate_status' in raw:
        if raw['rate_status'] not in {'quote','proposed','approved'}:raise ValueError('Choose quote, proposed or approved pricing status.')
        out['rate_status']=raw['rate_status']
    if 'gallery_filters' in raw:
        if not isinstance(raw['gallery_filters'],list) or len(raw['gallery_filters'])>12 or any(t not in TAGS for t in raw['gallery_filters']):raise ValueError('Choose valid gallery categories.')
        out['gallery_filters']=list(dict.fromkeys(raw['gallery_filters']))
    if 'achievements' in raw:
        if not isinstance(raw['achievements'],list) or len(raw['achievements'])>12:raise ValueError('Use at most 12 achievement records.')
        entries=[]
        for item in raw['achievements']:
            if not isinstance(item,dict):raise ValueError('Invalid achievement record.')
            a={k:text(item.get(k,''),k,lim,k in {'result','event'}) for k,lim in [('year',40),('result',160),('event',240),('detail',650),('evidence_url',2000)]}
            if a['evidence_url']:
                u=urlsplit(a['evidence_url'])
                if u.scheme!='https' or not u.hostname or u.username or u.password:raise ValueError('Achievement evidence needs a normal HTTPS URL, or leave it blank.')
            entries.append(a)
        out['achievements']=entries
    if 'niche_rates' in raw:
        if not isinstance(raw['niche_rates'],list) or len(raw['niche_rates'])>12:raise ValueError('Use at most 12 niche rates.')
        entries=[]
        for item in raw['niche_rates']:
            if not isinstance(item,dict):raise ValueError('Invalid niche rate.')
            entry={k:text(item.get(k,''),k,lim,True) for k,lim in [('niche',120),('scope',500)]}
            for key in ['amount','bundle_amount']:
                amount=item.get(key)
                if amount in ('',None):amount=None
                else:
                    if isinstance(amount,bool):raise ValueError('Use numeric niche rates.')
                    try:amount=float(amount)
                    except (TypeError,ValueError):raise ValueError('Use numeric niche rates.')
                    if not math.isfinite(amount) or not 0<=amount<=10000000:raise ValueError('Niche amount is outside the allowed range.')
                entry[key]=amount
            entries.append(entry)
        out['niche_rates']=entries
    if 'rate_addons' in raw:
        if not isinstance(raw['rate_addons'],list) or len(raw['rate_addons'])>12:raise ValueError('Use at most 12 add-ons.')
        entries=[]
        for item in raw['rate_addons']:
            if not isinstance(item,dict):raise ValueError('Invalid add-on.')
            entries.append({k:text(item.get(k,''),k,lim,True) for k,lim in [('name',120),('price',160),('scope',600)]})
        out['rate_addons']=entries
    if 'currency' in raw:
        if raw['currency'] not in {'INR','USD','GBP','EUR'}:raise ValueError('Choose a listed currency.')
        out['currency']=raw['currency']
    if 'packages' in raw:
        if not isinstance(raw['packages'],list) or len(raw['packages'])!=3:raise ValueError('Use three rate-card packages.')
        packages=[]
        for item in raw['packages']:
            if not isinstance(item,dict):raise ValueError('Invalid package.')
            p={k:text(item.get(k,''),k,500,k in {'name','description'}) for k in ['name','label','description']}
            items=item.get('items',[])
            if not isinstance(items,list) or not 1<=len(items)<=6:raise ValueError('Add 1–6 package deliverables.')
            p['items']=[text(v,'Deliverable',200,True) for v in items]
            amount=item.get('amount')
            if amount in ('',None):amount=None
            else:
                if isinstance(amount,bool):raise ValueError('Use a valid rate amount.')
                try:amount=float(amount)
                except (ValueError,TypeError):raise ValueError('Use a numeric rate amount.')
                if not math.isfinite(amount) or not 0<=amount<=10000000:raise ValueError('Rate amount is outside the allowed range.')
            p.update(amount=amount,from_price=bool(item.get('from_price',True)),approved=bool(item.get('approved',False)))
            if p['approved'] and amount is None:raise ValueError('Add an amount before approving its display, or leave Request a quote.')
            packages.append(p)
        out['packages']=packages
    return out


def validate_video(raw,existing=None):
    if not isinstance(raw,dict):raise ValueError('Send a portfolio entry.')
    out=deepcopy(existing or {})
    out['title']=text(raw.get('title',''),'Video title',180,True)
    out['url'],out['kind'],code=canonical_video_url(raw.get('url',''))
    out['id']=out.get('id') or ('yt_'+code if out['kind']=='youtube' else code) or secrets.token_hex(8)
    out['youtube_id']=code if out['kind']=='youtube' else ''
    original_path=urlsplit(raw.get('url','')).path
    if 'is_short' in raw and not isinstance(raw['is_short'],bool):raise ValueError('Shorts format must be true or false.')
    out['is_short']=raw.get('is_short',out.get('is_short',False)) if out['kind']=='youtube' else False
    if out['kind']=='youtube' and original_path.startswith('/shorts/'):out['is_short']=True
    out['client']=text(raw.get('client',''),'Brand / client',100)
    out['disclosure']=text(raw.get('disclosure',''),'Disclosure note',200)
    out['notes_private']=text(raw.get('notes_private',''),'Private review note',2000)
    out['thumbnail']=media_path(raw.get('thumbnail',''))
    brands=raw.get('brands',[]);tags=raw.get('tags',[])
    if not isinstance(brands,list) or not brands or any(s not in BRAND_ORDER for s in brands):raise ValueError('Choose at least one portfolio.')
    if not isinstance(tags,list) or not tags or any(t not in TAGS for t in tags):raise ValueError('Choose at least one collection.')
    out['brands']=list(dict.fromkeys(brands));out['tags']=list(dict.fromkeys(tags))
    if raw.get('status') not in {'draft','published'}:raise ValueError('Choose draft or visible in preview.')
    out['status']=raw['status'];out['rights_confirmed']=bool(raw.get('rights_confirmed',False))
    try:out['sort_order']=int(raw.get('sort_order',99))
    except (ValueError,TypeError):raise ValueError('Sort order must be a number.')
    if not 0<=out['sort_order']<=9999:raise ValueError('Sort order must be 0–9999.')
    out['updated_at']=timestamp()
    return out


def price_label(package,brand):
    if not package.get('approved') or package.get('amount') is None:return 'Request a quote'
    symbol={'INR':'₹','USD':'$','GBP':'£','EUR':'€'}[brand['currency']]
    amount=package['amount'];amount=f'{amount:,.0f}' if amount==int(amount) else f'{amount:,.2f}'
    return ('From ' if package.get('from_price') else '')+symbol+amount


def make_app(slug='avananusha',data_dir=None,password=None,secret=None,studio=True):
    if slug not in BRAND_ORDER:raise ValueError('Unknown portfolio.')
    app=Flask(__name__,static_folder=str(ROOT/'static'),template_folder=str(ROOT/'templates'))
    app.wsgi_app=ProxyFix(app.wsgi_app,x_proto=1,x_host=1)
    app.config.update(MAX_CONTENT_LENGTH=10*1024*1024,JSON_AS_ASCII=False)
    store=Store(data_dir or ROOT/'data');app.extensions['store']=store
    password=password or os.environ.get('STUDIO_PASSWORD','')
    if studio and len(password)<16:raise ValueError('Set a studio password of at least 16 characters.')
    password_hash=generate_password_hash(password) if password else ''
    secret=secret or os.environ.get('STUDIO_SECRET') or secrets.token_hex(32)
    csrf=hmac.new(secret.encode(),b'creator-portfolio-studio-v1','sha256').hexdigest()
    def auth_required(fn):
        @wraps(fn)
        def wrapped(*args,**kwargs):
            if not studio:abort(404)
            auth=request.authorization
            if not auth or not hmac.compare_digest(auth.username or '', 'creator') or not check_password_hash(password_hash,auth.password or ''):
                return Response('Creator Desk sign-in required.',401,{'WWW-Authenticate':'Basic realm="Creator Desk", charset="UTF-8"','Cache-Control':'no-store'})
            if request.method not in {'GET','HEAD','OPTIONS'}:
                if not hmac.compare_digest(request.headers.get('X-Studio-CSRF',''),csrf):return jsonify(error='Refresh Studio and try again. CSRF check failed.'),403
                origin=request.headers.get('Origin')
                if origin and origin.rstrip('/')!=request.host_url.rstrip('/'):return jsonify(error='Use Studio from this site origin.'),403
            return fn(*args,**kwargs)
        return wrapped
    def readiness(b,vs):
        missing=[]
        if not b.get('email') and not b.get('whatsapp'):missing.append('Add a public business email or WhatsApp number.')
        visible=[v for v in vs if b['slug'] in v['brands'] and v['status']=='published']
        if not visible:missing.append('Add at least one real portfolio entry for this identity.')
        if any(not v.get('rights_confirmed') for v in visible):missing.append('Confirm portfolio-reuse rights for the visible entries, including child/privacy permission where relevant.')
        return missing
    def public_videos(vs):
        keys=['id','title','client','url','kind','brands','tags','thumbnail','sort_order','disclosure','posted_date','youtube_id','is_short']
        return [{k:v.get(k,'') for k in keys} for v in vs]
    def resolve_media(name):
        return store.directory/name if name.startswith('uploads/') else MAIN_MEDIA/name
    def view_data(target_slug=None):
        brand,videos=store.public(target_slug or slug)
        brand=deepcopy(brand)
        for package in brand['packages']:
            if not package.get('approved') or brand.get('rate_status')=='quote':package['amount']=None
        if not brand.get('niche_rates_published',False) or brand.get('rate_status')=='quote':
            for rate in brand.get('niche_rates',[]):rate['amount']=None;rate['bundle_amount']=None
        hero_video=next((v['id'] for v in videos if v.get('thumbnail')==brand.get('hero_image')),None)
        return dict(brand=brand,videos=public_videos(videos),tags=TAGS,price_label=price_label,rate_label=lambda amount:price_label({'approved':True,'amount':amount,'from_price':True},brand),year=2026,hero_video=hero_video)
    app.extensions['creator_auth']=auth_required
    app.extensions['creator_csrf']=csrf
    app.extensions['portfolio_view_data']=view_data
    @app.after_request
    def headers(response):
        response.headers['X-Content-Type-Options']='nosniff'
        response.headers['Referrer-Policy']='strict-origin-when-cross-origin'
        if request.path.startswith(('/studio','/api/studio')):
            response.headers['Cache-Control']='no-store';response.headers['X-Robots-Tag']='noindex, nofollow'
        return response
    @app.errorhandler(ValueError)
    def invalid(error):return jsonify(error=str(error)),400
    @app.errorhandler(413)
    def too_large(error):return jsonify(error='Use an image smaller than 8 MB.'),413
    @app.get('/static/media/uploads/<path:filename>')
    def uploaded_image(filename):
        if not re.fullmatch(r'[a-f0-9]{24}\.webp',filename):abort(404)
        return send_from_directory(store.uploads,filename)
    @app.get('/favicon.ico')
    def favicon():
        return Response('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="17" fill="#b85869"/><text x="32" y="46" text-anchor="middle" fill="white" font-size="45">✳</text></svg>',mimetype='image/svg+xml')
    @app.get('/health')
    def health():return jsonify(ok=True,portfolio=slug)
    @app.get('/')
    def index():return render_template('site.html',**view_data())
    @app.get('/api/portfolio')
    def portfolio():
        data=view_data();return jsonify(brand=data['brand'],videos=data['videos'],tags=TAGS)
    @app.get('/media-kit')
    def media_kit():
        data=view_data();image=resolve_media(data['brand']['hero_image'])
        data['hero_data']=''
        if image.is_file():data['hero_data']='data:image/webp;base64,'+base64.b64encode(image.read_bytes()).decode()
        html=render_template('media_kit.html',**data)
        response=Response(html,content_type='text/html; charset=utf-8')
        if request.args.get('download')=='1':response.headers['Content-Disposition']=f'attachment; filename="{data["brand"]["name"]}_Media_Kit.html"'
        return response
    @app.get('/rate-card')
    def rate_card():
        data=view_data()
        html=render_template('rate_card.html',**data)
        response=Response(html,content_type='text/html; charset=utf-8')
        if request.args.get('download')=='1':response.headers['Content-Disposition']=f'attachment; filename="{data["brand"]["name"]}_Rate_Card.html"'
        return response
    @app.get('/studio')
    @auth_required
    def editor():return render_template('studio.html',csrf=csrf,tags=TAGS,brand_order=BRAND_ORDER)
    @app.get('/api/studio/state')
    @auth_required
    def state():
        data=store.export();data.update(csrf=csrf,tags=TAGS,readiness={s:readiness(data['brands'][s],data['videos']) for s in BRAND_ORDER})
        return jsonify(data)
    @app.put('/api/studio/brands/<target>')
    @auth_required
    def update_brand(target):
        if target not in BRAND_ORDER:abort(404)
        b=validate_brand(request.get_json(silent=True),store.settings(target))
        if not b['preview_mode']:
            missing=readiness(b,store.videos())
            if missing:return jsonify(error='Before removing the preview label: '+' '.join(missing)),400
        store.save_settings(target,b);return jsonify(ok=True)
    @app.post('/api/studio/videos')
    @auth_required
    def add_video():
        current=store.videos()
        if len(current)>=MAX_VIDEOS:return jsonify(error='Export a backup before adding more than 500 entries.'),409
        video=validate_video(request.get_json(silent=True))
        if any(video_key(v['url'])==video_key(video['url']) for v in current):return jsonify(error='This post is already saved. Edit its collections or portfolio assignment instead.'),409
        if any(v['id']==video['id'] for v in current):video['id']=secrets.token_hex(8)
        store.save_video(video);return jsonify(ok=True,id=video['id']),201
    @app.put('/api/studio/videos/<vid>')
    @auth_required
    def edit_video(vid):
        existing=next((v for v in store.videos() if v['id']==vid),None)
        if not existing:abort(404)
        video=validate_video(request.get_json(silent=True),existing)
        if existing.get('desk_piece_id'):
            if video_key(video['url'])!=video_key(existing['url']):return jsonify(error='Keep the actual Creator Desk publication URL unchanged; use draft status to hide a withdrawn work. Record corrections in its private notes.'),409
            if video['status']=='published' and not video.get('rights_confirmed'):return jsonify(error='Confirm portfolio-reuse permission before showing a new Creator Desk work.'),400
        if any(v['id']!=vid and video_key(v['url'])==video_key(video['url']) for v in store.videos()):return jsonify(error='This URL belongs to another saved entry.'),409
        store.save_video(video);return jsonify(ok=True,id=vid)
    @app.delete('/api/studio/videos/<vid>')
    @auth_required
    def delete_video(vid):
        existing=next((v for v in store.videos() if v['id']==vid),None)
        if not existing:abort(404)
        if existing.get('desk_piece_id'):return jsonify(error='This work is linked to a Creator Desk publication. Set it to draft or change portfolio assignments instead of erasing the production record.'),409
        store.remove(vid);return jsonify(ok=True)
    @app.post('/api/studio/upload')
    @auth_required
    def upload():
        f=request.files.get('image')
        if not f:raise ValueError('Choose an image.')
        raw=f.read(8*1024*1024+1)
        if len(raw)>8*1024*1024:raise ValueError('Use an image smaller than 8 MB.')
        try:
            image=Image.open(BytesIO(raw))
            if image.width*image.height>20000000:raise ValueError('Use an image smaller than 20 megapixels.')
            if image.format not in {'JPEG','PNG','WEBP'}:raise ValueError('Choose a JPG, PNG or WebP image.')
            image=ImageOps.exif_transpose(image).convert('RGB');image.thumbnail((1600,1600))
        except (UnidentifiedImageError,OSError,Image.DecompressionBombError):raise ValueError('Could not read that image.')
        name='uploads/'+sha256(raw).hexdigest()[:24]+'.webp';path=store.directory/name;path.parent.mkdir(parents=True,exist_ok=True)
        image.save(path,'WEBP',quality=87);return jsonify(path=name,url='/static/media/'+name)
    @app.get('/api/studio/backup')
    @auth_required
    def backup():
        stream=BytesIO()
        with ZipFile(stream,'w',ZIP_DEFLATED) as z:
            z.writestr('content.json',json.dumps(store.export(),ensure_ascii=False,indent=2))
            z.writestr('README.txt','Private content and media backup. Contains portfolio settings and uploaded images. Does not include passwords. Keep private. Restore content only after validating it; do not replace your only copy without a backup.')
            for f in MAIN_MEDIA.rglob('*'):
                if f.is_file() and f.suffix.lower() in {'.webp','.jpg','.png','.jpeg'}:z.write(f,'media/'+str(f.relative_to(MAIN_MEDIA)))
            for f in store.uploads.glob('*.webp'):z.write(f,'media/uploads/'+f.name)
        stream.seek(0);return send_file(stream,mimetype='application/zip',as_attachment=True,download_name='Creator_Portfolios_Content_Backup.zip')
    return app


def preview_credentials():
    private=ROOT/'private';private.mkdir(exist_ok=True)
    path=private/'studio_credentials.json'
    if path.exists():data=json.loads(path.read_text())
    else:
        data={'username':'creator','password':secrets.token_urlsafe(18),'secret':secrets.token_hex(32)}
        path.write_text(json.dumps(data,indent=2));path.chmod(0o600)
        (private/'Studio_Login.txt').write_text('PRIVATE — CREATOR STUDIO PREVIEW LOGIN\n\nUsername: creator\nPassword: '+data['password']+'\n\nOpen /studio on any of the four live preview links. This is not a public page. Change credentials before permanent deployment. Never upload this private folder to a public repository.\n')
        (private/'Studio_Login.txt').chmod(0o600)
    return data


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--brand',choices=BRAND_ORDER,default=os.getenv('PORTFOLIO_BRAND','avananusha'));parser.add_argument('--port',type=int,default=int(os.getenv('PORT','3101')));parser.add_argument('--data-dir',default=os.getenv('DATA_DIR',str(ROOT/'data')));args=parser.parse_args()
    password=os.getenv('STUDIO_PASSWORD');secret=os.getenv('STUDIO_SECRET')
    if not password:
        credentials=preview_credentials();password=credentials['password'];secret=credentials['secret']
        print('Preview-only credentials are in brand_portfolios/private/Studio_Login.txt. Not served publicly.',flush=True)
    app=make_app(args.brand,args.data_dir,password,secret)
    print(f'{BRANDS[args.brand]["name"]}: listening on 0.0.0.0:{args.port}; permanent hosting has not been provisioned.',flush=True)
    serve(app,host='0.0.0.0',port=args.port,threads=4)
