#!/usr/bin/env python3
"""Prepare ONLY public portfolio snapshots for manual GitHub Pages publishing.
Never connects to GitHub, publishes, changes the Desk DB or includes owner files.
PDF duplicates and private content books are intentionally excluded.
"""
from pathlib import Path
from bs4 import BeautifulSoup
from zipfile import ZipFile,ZipInfo,ZIP_DEFLATED
from hashlib import sha256
import html,json,shutil
ROOT=Path(__file__).resolve().parent
DEST=ROOT.parent/'public_portfolio_hosting';SITE=DEST/'website';DOWNLOAD=ROOT.parent/'downloads/Public_Portfolios_GitHub_Pages_Kit.zip'
BRANDS=[('avananusha','Avananusha','01','Lifestyle & product storytelling','Skin care · Hair care · Baby products · Educational toys · Lifestyle · Creator highlights','20 existing work samples'),('avanpakasastram','Avanpakasastram','02','Cooking, culture & a little creativity','Recipe storytelling · Food demonstrations · Creator-reported cooking achievements','1 existing work sample'),('avanadvaitham','Avanadvaitham','03','Devotional stories with intention','Devotional storytelling · Collaboration scope · Proposed rates','Sample videos to be added'),('myratechies','MyraTechies','04','Technology, explained through real use','Tech UGC · Demonstrations · Collaboration scope','Sample videos to be added')]

GUIDE='''# Put your public portfolios online — GitHub Pages

## What this kit does

This is **public-only static hosting**, not the working Creator Desk. The four portfolio pages, public media kits and proposed rate cards can be opened on other laptops/phones after publishing. Your laptop can be off. There is no Desk login, database, 470-draft content book, private upload, AI key or backend in the upload folder. The private Desk stays on your laptop.

GitHub Pages is available with GitHub Free for **public repositories**. Everyone can read/download the repository files and their history. This kit is for your portfolio showcase, not a paid SaaS or payment-processing site. Official documentation: [1](https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages).

**Nothing has been uploaded or made live by preparing this ZIP.** GitHub publishing is not supported by the tools in this chat, so the owner must perform the following account steps. Never send passwords, tokens, recovery codes or card details in chat.

## Before you publish

- Review the existing videos, images, child/family privacy, brand/music and portfolio-reuse permissions. Source visibility is not reuse permission.
- Verify the proposed rates, five creator-reported cooking achievements and public wording. Kerala Tourism's unspecified year stays unspecified.
- **No public business email/WhatsApp is configured in the current snapshots.** If you want enquiries, supply a business contact explicitly for publication, add it in your private Portfolio Studio and regenerate the public exports. Never copy an account email into public files without that choice.
- Preview banners and `noindex, nofollow` are intentionally retained from the existing portfolio settings. The links can still be opened publicly; `noindex` is NOT a password or privacy protection. Review/approve details before removing preview labels or enabling indexing.
- Tech/devotional sample galleries remain empty rather than fabricated. The original 20 unique works are preserved; Kidzola appears in both requested portfolios.

## Step 1 — Create a new PUBLIC repository

1. Sign in to https://github.com using your own account.
2. Click **+ → New repository**.
3. Suggested repository name: **creator-portfolios**. If that name already exists, choose a fresh name; do not overwrite an existing project.
4. Choose **Public**. The free Pages route requires this; do not put private app material in it.
5. You can enable **Add a README** to create the main branch. Click **Create repository**.

No Render account, paid backend or purchased domain is needed for this static stage. Check GitHub's applicable plan/usage limits; this does not include hosting the private Flask app.

## Step 2 — Upload ONLY the website folder's CONTENTS

1. Extract **Public_Portfolios_GitHub_Pages_Kit.zip** on a laptop.
2. Open its **website** folder.
3. In the new repository, select **Add file → Upload files**. For an empty repository, use the **uploading an existing file** link.
4. Drag **the contents inside website** into the upload area: `index.html`, the four portfolio folders and `.nojekyll` if shown. Keep folders intact.
5. Commit directly to **main** using **Commit changes**.

**Correct repository layout:**

```
index.html
.nojekyll
avananusha/index.html
avananusha/media-kit.html
avananusha/rate-card.html
avanpakasastram/index.html
avanpakasastram/media-kit.html
avanpakasastram/rate-card.html
avanadvaitham/index.html
avanadvaitham/media-kit.html
avanadvaitham/rate-card.html
myratechies/index.html
myratechies/media-kit.html
myratechies/rate-card.html
```

**Wrong:** uploading the ZIP itself, putting everything under an extra `website/` folder in the repository, or uploading `Creator_Desk_Final_Kit.zip`, database, private scripts, backups or credentials. The root `index.html` must be visible directly in the repository. `.nojekyll` is a harmless empty marker; no custom workflow is required for this plain HTML kit.

## Step 3 — Enable Pages

1. Open the repository's **Settings** tab.
2. In the sidebar select **Pages**.
3. Under **Build and deployment → Source**, choose **Deploy from a branch**.
4. Select **main** and **/(root)**, then **Save**.
5. Wait for deployment to finish; check **Actions** if a build is still pending or fails.
6. Return to **Settings → Pages**. Open the actual published URL GitHub shows. Use **Enforce HTTPS** if that option is available and not already enforced.

GitHub documents selecting a branch/root folder as a Pages publishing source here: [1](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site).

## Your link structure

The following are **TEMPLATES, NOT LIVE LINKS**. Replace YOUR-USERNAME with your real GitHub username, and creator-portfolios with the exact repository name you chose. Use the actual URL shown by Pages if you already use a custom domain.

```
Home:
https://YOUR-USERNAME.github.io/creator-portfolios/

Avananusha:
https://YOUR-USERNAME.github.io/creator-portfolios/avananusha/

Avanpakasastram:
https://YOUR-USERNAME.github.io/creator-portfolios/avanpakasastram/

Avanadvaitham:
https://YOUR-USERNAME.github.io/creator-portfolios/avanadvaitham/

MyraTechies:
https://YOUR-USERNAME.github.io/creator-portfolios/myratechies/
```

Each portfolio also has `media-kit.html` and `rate-card.html` in its own folder. These public HTML documents can be printed to PDF from a browser. Existing portfolio buttons retain their portable HTML download behavior.

## Step 4 — Check on laptop and mobile

- Open all four links and the home page, then use the All portfolios link to return.
- Check Avananusha's six collections, the one distinct Johnson baby-oil source, the toy sources and shared Kidzola.
- Check all five supplied cooking achievements; no Kerala Tourism year is invented.
- Tech/devotional pages must not contain fabricated videos.
- Read the proposed rate cards and media-kit links.
- Video players contact a third-party platform only after visitor consent. Actual playback may require platform login or depend on region/browser; original source links remain available.
- The enquiry form only prepares text in the browser. It is not a hosted inbox or automatic email service. No business email/WhatsApp is configured yet.
- A mobile browser does not need your laptop to remain on once GitHub Pages publishes the static files.

## Later updates

These are **snapshots, not live sync**. Editing Creator Desk, Excel, Google Sheets or an old downloaded HTML file does not update the published repository.

After changing public details in the working Desk, run these in the activated laptop environment:

```
python export_public.py
python prepare_public_hosting.py
```

If the earlier owner ZIP does not contain the second script, use the included helper from this kit: put `prepare_public_hosting.py` beside `creator_desk.py` first. Upload the regenerated website contents to the same repository/branch and commit. Never upload private owner files. Public Git history can retain old content after deletion; remove private information before the first upload.

This process makes only your portfolios live. The working Desk, private video review and optional AI still require a separate secured backend deployment later. No paid hosting or external publishing was performed while preparing this kit.
'''


def main():
 SITE.mkdir(parents=True,exist_ok=True)
 cards=[]
 for slug,name,number,title,scope,status in BRANDS:
  directory=SITE/slug;directory.mkdir(exist_ok=True)
  source=ROOT/'exports/public'/(name+'_Portfolio.html')
  if not source.is_file():raise SystemExit('Run python export_public.py first.')
  soup=BeautifulSoup(source.read_text(encoding='utf-8'),'html.parser')
  # Relative link works under any GitHub project prefix and ordinary static host.
  nav=soup.new_tag('div');nav['style']='padding:9px 20px;border-bottom:1px solid #dce3d5;background:#f4f5ef;text-align:center;font:11px/1.8 Arial,sans-serif'
  a=soup.new_tag('a',href='../index.html');a['style']='color:#315f4c;text-decoration:none';a.string='← All portfolios';nav.append(a);soup.body.insert(0,nav)
  (directory/'index.html').write_text(str(soup),encoding='utf-8')
  for suffix,dest in [('Media_Kit','media-kit.html'),('Rate_Card','rate-card.html')]:shutil.copyfile(ROOT/'exports/public'/(name+'_'+suffix+'.html'),directory/dest)
  cards.append(f'<a class="card" href="{slug}/index.html"><div class="top"><span>{number} / PORTFOLIO</span><span aria-hidden="true">↗</span></div><h2>{html.escape(name)}</h2><h3>{html.escape(title)}</h3><p>{html.escape(scope)}</p><div class="status">{html.escape(status)}</div></a>')
 css='''*{box-sizing:border-box}body{margin:0;background:#f4f5ef;color:#233d35;font:15px/1.85 Arial,sans-serif}main{max-width:1120px;margin:auto;padding:34px 30px 50px}header{display:flex;justify-content:space-between;align-items:center;border-bottom:1px solid #d8e1d0;padding-bottom:22px;gap:16px}.wordmark{font:25px/1.2 Georgia,serif;letter-spacing:-.6px}.wordmark span{color:#668058}header small{font-size:9px;letter-spacing:1.5px;color:#74846d}.hero{padding:64px 0 45px;max-width:850px}.eyebrow{font-size:9px;letter-spacing:2px;color:#718765;font-weight:bold}h1{font:68px/1.1 Georgia,serif;letter-spacing:-2px;margin:20px 0 26px}h1 em{color:#315f4c;font-weight:normal}.lead{font-size:15px;color:#74816c;max-width:680px}.cards{display:grid;grid-template-columns:1fr 1fr;gap:20px}.card{display:flex;flex-direction:column;color:inherit;text-decoration:none;background:#fffefa;padding:30px;border:1px solid #dce3d5;border-radius:13px;transition:border-color .2s,transform .2s;min-width:0}.card:hover{border-color:#a4bb91;transform:translateY(-3px)}.card:focus-visible{outline:3px solid #9eb58a;outline-offset:4px}.top{display:flex;justify-content:space-between;color:#718765;font-size:9px;letter-spacing:1.2px}h2{font:35px/1.2 Georgia,serif;letter-spacing:-.9px;margin:24px 0 16px;overflow-wrap:anywhere}h3{font-size:13px;font-weight:500;color:#315f4c;margin:0 0 12px}.card p{font-size:12px;color:#7b877b;margin:0 0 26px}.status{font-size:10px;color:#718765;border-top:1px solid #e3e9dd;padding-top:16px;margin-top:auto}.note{margin-top:28px;padding:18px 22px;background:#edf2e5;border:1px solid #dce3d5;border-radius:9px;color:#6d7e64;font-size:11px}footer{margin-top:40px;border-top:1px solid #dce3d5;padding-top:22px;display:flex;justify-content:space-between;gap:20px;font-size:9px;color:#7b877b}@media(max-width:600px){main{padding:25px 20px 35px}header{flex-wrap:wrap}.hero{padding:42px 0 27px}h1{font-size:47px;letter-spacing:-1.4px}.lead{font-size:13px}.cards{grid-template-columns:1fr;gap:15px}.card{padding:27px}h2{font-size:33px}.note{font-size:10px}footer{flex-direction:column;gap:9px}}@media(prefers-reduced-motion:reduce){.card{transition:none}}'''
 page='<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,nofollow"><meta name="description" content="Explore Avananusha, Avanpakasastram, Avanadvaitham and MyraTechies creator portfolios, original work and proposed collaboration rates."><title>Creator portfolios · Four worlds, one point of view</title><style>'+css+'</style></head><body><main><header><div class="wordmark">creator <span>portfolios.</span></div><small>PRODUCTS · FOOD · DEVOTIONAL · TECH</small></header><section class="hero"><p class="eyebrow">FOUR WORLDS. ONE POINT OF VIEW.</p><h1>Stories with a little<br><em>more intention.</em></h1><p class="lead">Explore product storytelling, cooking, devotional content and tech UGC. Choose a portfolio to see the available work, collaboration scope and proposed starting rates.</p></section><nav class="cards" aria-label="Choose a creator portfolio">'+''.join(cards)+'</nav><p class="note">Portfolio preview · Proposed rates and relevant rights checks remain subject to creator confirmation. Existing work stays separate from planned content; tech and devotional samples will appear only when actual videos are supplied.</p><footer><span>Avananusha · Avanpakasastram · Avanadvaitham · MyraTechies</span><span>Original source links · Visitor-controlled video previews</span></footer></main></body></html>'
 (SITE/'index.html').write_text(page,encoding='utf-8');(SITE/'.nojekyll').write_text('')
 DEST.mkdir(exist_ok=True);(DEST/'README_UPLOAD.md').write_text(GUIDE,encoding='utf-8')
 # Portable instructions outside the upload folder, with no package dependency.
 try:
  import markdown
  guide_html=markdown.markdown(GUIDE,extensions=['fenced_code'])
 except ImportError:guide_html='<pre>'+html.escape(GUIDE)+'</pre>'
 doc='<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Start here · Publish public portfolios with GitHub Pages</title><style>body{margin:0;background:#f4f5ef;color:#233d35;font:14px/1.85 Arial,sans-serif}main{max-width:940px;margin:auto;padding:40px 24px;overflow-wrap:anywhere}h1,h2{font-family:Georgia,serif;line-height:1.25}h1{font-size:38px}h2{font-size:26px;margin-top:32px}a{color:#315f4c}pre{white-space:pre-wrap;background:#fffefa;border:1px solid #dce3d5;border-radius:8px;padding:18px;font-size:12px}code{overflow-wrap:anywhere}li{margin:7px 0}strong{color:#315f4c}@media(max-width:500px){h1{font-size:30px}main{padding:28px 19px}}@media print{body{background:white}main{padding:0}h2{break-after:avoid}}</style></head><body><main><p><a href="website/index.html">Open the local public-portfolio preview →</a></p>'+guide_html+'</main></body></html>'
 (DEST/'START_HERE.html').write_text(doc,encoding='utf-8')
 # Developer helper goes outside website; NEVER upload it to the public repo.
 helper=Path(__file__).read_bytes()
 actual_secrets=[]
 for f in (ROOT/'private').glob('*login.json'):
  data=json.loads(f.read_text());actual_secrets.extend(data[k].encode() for k in ['password','secret'] if data.get(k))
 ai=ROOT/'data/private/ai_settings.json'
 if ai.exists() and (key:=json.loads(ai.read_text()).get('api_key')):actual_secrets.append(key.encode())
 entries={}
 for f in SITE.rglob('*'):
  if not f.is_file():continue
  rel=str(f.relative_to(SITE));data=f.read_bytes();assert f.suffix in {'.html',''} and not any(x in rel.lower() for x in ['private','sqlite','login','backup','content_book'])
  for forbidden in [b'notes_private',b'boot-data',b'X-Studio-CSRF',b'/api/desk',b'desk_pieces',b'facts_confirmed']+actual_secrets:assert forbidden not in data,(rel,'Private payload found')
  entries['website/'+rel]=data
 for name in ['START_HERE.html','README_UPLOAD.md']:entries[name]=(DEST/name).read_bytes()
 entries['prepare_public_hosting.py']=helper
 DOWNLOAD.parent.mkdir(exist_ok=True)
 with ZipFile(DOWNLOAD,'w',ZIP_DEFLATED,compresslevel=9) as z:
  for name,data in sorted(entries.items()):
   info=ZipInfo('Public_Portfolios_GitHub_Pages/'+name);info.create_system=3;info.external_attr=0o100644<<16;z.writestr(info,data,compress_type=ZIP_DEFLATED,compresslevel=9)
 with ZipFile(DOWNLOAD) as z:assert z.testzip() is None
 print(json.dumps({'folder':str(SITE),'upload_files':len(list(SITE.rglob('*.html')))+1,'zip':str(DOWNLOAD),'zip_bytes':DOWNLOAD.stat().st_size,'zip_sha256':sha256(DOWNLOAD.read_bytes()).hexdigest(),'external_upload_performed':False,'working_desk_included':False,'business_contact_configured':False,'preview_and_noindex_retained':True},indent=2))
if __name__=='__main__':main()
