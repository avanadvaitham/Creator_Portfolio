"""Creator-requested portfolio curation and assistant-proposed introductory rates.

Request date: 12 November 2026. No audience statistics, event certificates,
current product claims or booking contacts are inferred from these settings.
"""
from copy import deepcopy

REQUEST_DATE='2026-11-12'
PUBLIC_FILTERS={
    'avananusha':['skin-care','hair-care','baby-products','educational-toys','lifestyle','highlights'],
    'avanpakasastram':['cooking'],
    'avanadvaitham':['devotional'],
    'myratechies':['tech'],
}
ADDITIONAL_TAGS={'baby-products':'Baby products','educational-toys':'Kids educational toys'}
ACHIEVEMENTS=[
    {'year':'2021','result':'First prize','event':'Online National Cooking Competition · Season 2','detail':'Conducted by Febina.','evidence_url':''},
    {'year':'Mar 2021','result':'First prize','event':'International online cooking competition · ShreshtasFoods','detail':'Conducted on the eve of Women’s Day.','evidence_url':''},
    {'year':'Year not specified','result':'Top 150','event':'International online cooking competition · Kerala Tourism','detail':'Selected in the top 150.','evidence_url':''},
    {'year':'2026','result':'Participant','event':'National cooking competition · “Kahi ghum na ho gaya”','detail':'Participated in the national cooking competition.','evidence_url':''},
    {'year':'2026','result':'Selected among the top 5 to perform','event':'Green Gourmet cooking competition · Ektava festival','detail':'Participated in Ektava festival; selected among the top five to perform.','evidence_url':''},
]
RATE_NOTE='Proposed introductory rates in INR, prepared at the creator’s request. These are starting prices for new content, not fees to reuse archived posts or prices derived from verified audience metrics. Final scope, suitability, rights and fees are confirmed in writing.'
USAGE_NOTE='Base UGC includes 90-day non-exclusive organic use on one brand’s owned social channels and website. Creator posting is included only where named. Paid ads/partnership ads, raw clips, exclusivity, extended licensing, extra languages and reshoots are separate. No AI training, voice cloning, perpetual rights or sublicensing is included.'
BOOKING_NOTE='One agreed concept, edited 9:16 1080p delivery, captions and one consolidated minor revision round. 50% to book; balance before unwatermarked delivery. Product, shipping, special ingredients, travel and applicable taxes are extra. Typical target: 5–7 business days after product receipt and brief approval; recipe/technical scopes may need 7–10. No guaranteed views or sales. Child appearances are not included by default.'
ADDONS=[
    {'name':'Additional opening hook','price':'₹750 each','scope':'A new scripted opening using the same approved shoot and edit.'},
    {'name':'Extra minor revision round','price':'₹750 per round','scope':'Consolidated changes; a new concept, script or reshoot is quoted separately.'},
    {'name':'Additional language adaptation','price':'From ₹1,500 / language / video','scope':'Voiceover/subtitles on the same approved edit; no new shoot included.'},
    {'name':'Paid-ad licence','price':'+50% of creation fee / 30 days','scope':'Proposed India-targeted use on one platform. Partnership-ad permissions and eligibility are agreed separately.'},
    {'name':'Selected usable raw clips','price':'+50% of creation fee','scope':'Only agreed, cleared clips; not a blanket transfer of every recording or family footage.'},
    {'name':'Rush delivery','price':'+25%, subject to capacity','scope':'Only after confirming product availability, brief and a feasible deadline.'},
    {'name':'Exclusivity / extended rights','price':'Custom quote','scope':'Category, competitors, territory, platform and duration must be specified.'},
]


def package(name,label,description,amount,items):
    # Legacy "approved" controls permission to DISPLAY an amount. It does not
    # mean the proposed fee is a signed quote or that a brand booked the work.
    return {'name':name,'label':label,'description':description,'amount':amount,'items':items,'approved':True,'from_price':True}


def rate(niche,scope,amount,bundle_amount):
    return {'niche':niche,'scope':scope,'amount':amount,'bundle_amount':bundle_amount}

RATES={
 'avananusha':{
  'packages':[
   package('Single UGC video','BRAND-CHANNEL CONTENT','One product-led vertical video; the exact niche rate below determines the final starting fee.',3500,['30–60 seconds · 1 concept · 9:16 1080p','Script direction, edit, captions and 1 minor revision','90-day organic brand usage; no creator posting']),
   package('Three-video UGC bundle','A CONSISTENT CONTENT SET','Three agreed videos in one batched shoot, for one product/category. More involved niches are priced below.',9000,['3 edited videos · one approved brief and shoot plan','One consolidated minor revision per video','90-day organic brand usage; paid ads excluded']),
   package('Creator-posted reel','CREATION + AVANANUSHA POSTING','One newly created reel plus an agreed post on Avananusha’s Instagram. No audience or performance guarantee.',6500,['One 30–60 second reel with disclosure where required','Posting and retention period confirmed before booking','Reporting scope agreed; paid/partnership ads excluded']),
  ],
  'niche_rates':[
   rate('Skin care','30–60 sec product texture/routine/demo; substantiated claims only.',4000,10500),
   rate('Hair care','30–60 sec routine/product demo; no unverified regrowth or repair promises.',4000,10500),
   rate('Baby products','30–60 sec adult-led packaging/product demo; no child appearance included.',4500,12000),
   rate('Kids educational toys','30–60 sec adult-led feature/use demo; no developmental-outcome promise.',4500,12000),
   rate('Lifestyle','30–60 sec everyday-use product story.',3500,9000),
   rate('Creator-led storytelling / highlights','30–60 sec newly commissioned personal-brand or highlight-style story.',5000,13500),
  ],
 },
 'avanpakasastram':{
  'packages':[
   package('Recipe-led UGC video','FROM INGREDIENT TO FINAL PLATE','One product-integrated recipe video, up to 60–90 seconds; special ingredients/logistics are separate.',6000,['One recipe, approved concept and cooking shoot','Edited vertical video, captions and 1 minor revision','90-day organic brand usage; no creator posting']),
   package('Three-recipe bundle','A BATCH OF FOOD STORIES','Three recipe-led videos for one agreed campaign, using a batched production plan.',16000,['3 recipe videos, each up to 60–90 seconds','One consolidated minor revision per video','Special ingredients, travel and paid ads excluded']),
   package('Creator-posted recipe reel','CREATION + COOKING-ACCOUNT POSTING','One new recipe-led reel plus an agreed creator post. Exact account/platform and reporting are confirmed in writing.',8500,['One recipe-led reel and required disclosure','Account, posting and retention period confirmed','No follower, reach, order or sales guarantee']),
  ],
  'niche_rates':[
   rate('Recipe-led cooking','Up to 60–90 sec · one recipe and approved product integration.',6000,16000),
   rate('Food & ingredient feature','30–60 sec product-use/ingredient feature; simple preparation.',4500,12000),
   rate('Cookware / kitchen appliance demo','30–60 sec real-use demo; more involved tests quoted separately.',5500,15000),
   rate('Kitchen essentials','30–60 sec practical kitchen product story.',4500,12000),
  ],
 },
 'avanadvaitham':{
  'packages':[
   package('Devotional UGC video','RESPECTFUL BRAND CONTENT','One culturally considered product/setup story; no spiritual-outcome guarantees.',3500,['30–60 seconds · 1 concept · captions','One consolidated minor revision','90-day organic brand usage; no creator posting']),
   package('Three-video ritual series','ONE CONSISTENT VISUAL DIRECTION','Three agreed devotional/ritual product stories for one campaign.',9000,['3 edited vertical videos','Cultural-fit and disclosure review','Paid ads, exclusivity and extra locations excluded']),
   package('Creator-posted devotional reel','CREATION + AGREED CREATOR POST','One new reel and agreed devotional-account posting; exact profile/platform and rights confirmed before booking.',5500,['One 30–60 second reel with appropriate disclosure','Posting and retention period confirmed','No guaranteed spiritual, audience or sales outcomes']),
  ],
  'niche_rates':[
   rate('Puja / ritual essentials','30–60 sec respectful product/setup demo.',3500,9000),
   rate('Devotional visual storytelling','30–60 sec culturally appropriate visual story.',3500,9000),
   rate('Festival / cultural storytelling','30–60 sec single-location seasonal concept; logistics separate.',4000,10500),
  ],
 },
 'myratechies':{
  'packages':[
   package('Single tech UGC video','GADGET / ACCESSORY CONTENT','One genuine use-case demonstration. Introductory offering; tech portfolio samples are in production.',5000,['30–60 sec · actual product access required','Edited 9:16 video, captions and 1 minor revision','90-day organic brand usage; no creator posting']),
   package('Three-video tech bundle','THREE USE CASES, ONE DIRECTION','Three approved demo/use-case videos for one product or campaign.',13500,['3 edited vertical videos in a batched shoot','Observed features only; no invented benchmarks','Paid ads, raw clips and extra devices excluded']),
   package('Demo + two extra hooks','ONE CORE EDIT, THREE OPENINGS','One 30–60 second core demo with two extra opening variations, not three separate concepts.',7000,['1 core video + 2 alternate openings','Captions and one consolidated minor revision','Organic brand usage; creator posting excluded']),
  ],
  'niche_rates':[
   rate('Gadgets & accessories','30–60 sec one-device real-use demo.',5000,13500),
   rate('Apps & software walkthroughs','45–90 sec planned screen demonstration; test access required.',6000,16000),
   rate('Unboxing / setup / first-use','30–60 sec factual product/setup story.',5000,13500),
  ],
 },
}

BRAND_PATCHES={
 'avananusha':{
  'pillars':['Skin care','Hair care','Baby products','Kids educational toys','Lifestyle','Creator highlights'],
  'intro':'Skin care, hair care, baby products, kids educational toys and everyday lifestyle—brought together by a Telugu-first creator and mom’s point of view.',
  'about':'Avananusha brings skin-care, hair-care, baby-product, kids educational-toy and lifestyle stories into one creator-led space. Creator highlights add the personal voice behind the product work. Explore original Instagram and YouTube selections, then build a brief around a real use case and a relevant audience.',
  'service_angles':['Skin-care & hair-care UGC','Baby products & educational-toy demos','Lifestyle stories & creator-led integrations'],
  'gallery_note':'Six focused collections, with original Instagram and YouTube links. Historical toy reviews are selected from the playlist already supplied by the creator.',
 },
 'avanpakasastram':{
  'about':'Avanpakasastram is Anusha’s dedicated space for recipe-led storytelling, food features, cookware and kitchen products. Her creator-supplied competition record includes first-prize wins in 2021 and selected cooking performances in 2026. Each integration should show the real role of a product in the cooking process.',
  'gallery_note':'A separate cooking portfolio, including the Kidzola oil family-cooking feature explicitly shared with Avananusha. Chef milestones appear below.',
  'achievements':ACHIEVEMENTS,
  'achievements_note':'Competition details are provided by the creator. Event names are retained as supplied; certificates and official result links have not been attached.',
 },
 'myratechies':{
  'empty_note':'New tech UGC samples are in production. The creator plans to share links in about a week. No samples, benchmarks or brand collaborations are claimed before those links are supplied.',
  'samples_status':'Tech UGC samples in production · new work coming soon',
 },
}

CURATION_ORDER=['DLp77UPSAeZ','DcVwhedSJ18','yt_qtpSqo5HAuA','yt_h81C6CiKS1o','DcAxeEMyw_I','DdEiKGGvEnS','DUnCvZkgFzX','yt_kp9NEugH3Dg','DOxsMIvALd8','DcQR0NKSgFp','C_zmo0uSe1k','yt__PeFe-we8bI','DVJRkJkEgpm','DJ6ZYr7y-n_','Daau5WPS3YK','DNz-NjdQIbx','DJULjLtSaF-','DLp8PnXSXOP','DfAIQ75xmFr','DdmAfXBPnBe']

NEW_VIDEO_SOURCES=[
 {'id':'yt_qtpSqo5HAuA','youtube_id':'qtpSqo5HAuA','title':'Johnson’s baby oil · product review','client':'Johnson’s Baby','tags':['baby-products'],'posted_date':'2024-05-06','is_short':True,'sort_order':16,'thumbnail':'youtube/qtpSqo5HAuA.webp'},
 {'id':'yt__PeFe-we8bI','youtube_id':'_PeFe-we8bI','title':'Talking flash cards · educational device review','client':'Product review','tags':['educational-toys'],'posted_date':'2023-02-10','is_short':False,'sort_order':17,'thumbnail':'youtube/_PeFe-we8bI.webp'},
 {'id':'yt_h81C6CiKS1o','youtube_id':'h81C6CiKS1o','title':'Storio spelling game · product review','client':'Storio','tags':['educational-toys'],'posted_date':'2023-07-07','is_short':False,'sort_order':18,'thumbnail':'youtube/h81C6CiKS1o.webp'},
 {'id':'yt_kp9NEugH3Dg','youtube_id':'kp9NEugH3Dg','title':'ClassMonitor activity kit · product review','client':'ClassMonitor','tags':['educational-toys'],'posted_date':'2024-01-12','is_short':False,'sort_order':19,'thumbnail':'youtube/kp9NEugH3Dg.webp'},
]


def patch_brand(slug,current):
    out=deepcopy(current)
    out.update(deepcopy(BRAND_PATCHES.get(slug,{})))
    out.update(deepcopy(RATES[slug]))
    out.update(currency='INR',niche_rates_published=True,rate_status='proposed',rate_note=RATE_NOTE,usage_note=USAGE_NOTE,booking_note=BOOKING_NOTE,rate_addons=deepcopy(ADDONS),gallery_filters=PUBLIC_FILTERS[slug],rate_date=REQUEST_DATE)
    out.setdefault('achievements',[]);out.setdefault('achievements_note','');out.setdefault('samples_status','')
    return out


def patch_existing_video(video):
    out=deepcopy(video)
    if out['id'] in CURATION_ORDER:out['sort_order']=CURATION_ORDER.index(out['id'])
    if out['id'] in {'DdEiKGGvEnS','DVJRkJkEgpm','DfAIQ75xmFr','DdmAfXBPnBe'}:
        out['tags']=list(dict.fromkeys(out['tags']+['lifestyle']))
    if out['id']=='C_zmo0uSe1k':
        out['tags']=list(dict.fromkeys(out['tags']+['baby-products']))
    if out['id']=='DNz-NjdQIbx':
        out['tags']=list(dict.fromkeys(out['tags']+['lifestyle']))
    if out['id']=='DcAxeEMyw_I':
        out['title']='Kidzola oil · family-cooking feature'
        out['brands']=list(dict.fromkeys(out['brands']+['avananusha','avanpakasastram']))
        out['tags']=list(dict.fromkeys(out['tags']+['lifestyle','cooking']))
    return out


def new_videos():
    out=[]
    for item in NEW_VIDEO_SOURCES:
        v=deepcopy(item)
        v.update(url='https://www.youtube.com/watch?v='+v['youtube_id'],kind='youtube',brands=['avananusha'],status='published',rights_confirmed=False,disclosure='',notes_private='Historical creator work selected from supplied YouTube sources. Payment, current formula/model/availability, claim substantiation and raw-reuse/music rights are not inferred. No health, safety or developmental promises are copied.',source_checked=REQUEST_DATE,source_profile='AvanAnusha on YouTube',metrics_approved=False)
        v['sort_order']=CURATION_ORDER.index(v['id'])
        out.append(v)
    return out
