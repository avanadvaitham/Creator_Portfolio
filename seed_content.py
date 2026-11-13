"""Creator-supplied work, editable copy and explicitly proposed rates. No invented metrics."""
from copy import deepcopy
from portfolio_updates import ADDITIONAL_TAGS, patch_brand, patch_existing_video, new_videos

BRAND_ORDER = ['avananusha', 'avanpakasastram', 'avanadvaitham', 'myratechies']
CHECKED_DATE = '2026-11-12'
LANGUAGES = ['Telugu', 'Hindi', 'English', 'Hinglish']
TAGS = {'highlights': 'Creator highlights', 'collaborations': 'Brand collaborations', 'hair-care': 'Hair care', 'kids-collabs': 'Kids & family features', 'parenting-baby': 'Parenting & baby care', 'skin-care': 'Skin care', 'lifestyle': 'Lifestyle', 'cooking': 'Cooking', 'devotional': 'Devotional', 'tech': 'Tech UGC'}

TAGS.update(ADDITIONAL_TAGS)

def packages():
    return [
        {'name': 'UGC creation', 'label': 'CONTENT FOR YOUR CHANNELS', 'description': 'Product-led vertical content created for your brand. Posting to the creator account is a separate scope.', 'items': ['Concept and agreed script direction', 'Edited vertical video with captions', 'A clear, brief-specific call to action'], 'amount': None, 'from_price': True, 'approved': False},
        {'name': 'Influencer partnership', 'label': 'CONTENT + CREATOR POSTING', 'description': 'A creator-led integration for a relevant audience, with platform, deliverables and reporting agreed in the brief.', 'items': ['Reel or post integration as agreed', 'Clear commercial disclosure', 'Reporting scope confirmed before booking'], 'amount': None, 'from_price': True, 'approved': False},
        {'name': 'Content bundle', 'label': 'MULTIPLE STORIES, ONE BRIEF', 'description': 'A coordinated collection of videos or variations for a launch, product range or campaign.', 'items': ['Custom deliverable and hook mix', 'Consistent visual direction', 'Usage and revision scope in writing'], 'amount': None, 'from_price': True, 'approved': False},
    ]

COMMON = {'email': '', 'whatsapp': '', 'instagram': '', 'currency': 'INR', 'languages': LANGUAGES, 'packages': packages(), 'preview_mode': True,
          'usage_note': 'Paid-ad usage, partnership ads, raw footage, exclusivity, additional revisions and reshoots are quoted separately. No perpetual or unrestricted rights are included by default.',
          'booking_note': 'Final deliverables, revision rounds, delivery dates, product logistics, payment schedule and applicable taxes are confirmed in a written proposal before booking.'}

BRANDS = {
    'avananusha': {**deepcopy(COMMON), 'slug': 'avananusha', 'name': 'Avananusha', 'wordmark': 'avan anusha', 'monogram': 'aa', 'theme': 'rose', 'eyebrow': 'UGC CREATOR · MOM INFLUENCER', 'headline': 'Everyday stories.\nReal connection.', 'accent_line': 'Real connection.', 'intro': 'Parenting, beauty and life in between. Relatable, product-led content with a Telugu-first voice—and a clear place for your brand.', 'about_title': 'A little life.\nA lot of storytelling.', 'about': 'Avananusha brings motherhood, parenting, baby-care, skin-care, hair-care and lifestyle stories into one creator-led space. Explore original posts and selected product collaborations, then build a brief around the audience and outcome that matter to your brand.', 'pillars': ['Parenting & baby care', 'Skin care', 'Hair care', 'Lifestyle'], 'service_angles': ['Relatable mom & parenting stories', 'Beauty and personal-care demos', 'Product integrations & UGC'], 'hero_image': 'reels/DUnCvZkgFzX.webp', 'hero_alt': 'Avananusha in a frame from her submitted skincare collaboration', 'hero_caption': 'A frame from Avananusha’s submitted portfolio work.', 'hero_illustrative': False, 'instagram': 'https://www.instagram.com/avananusha/', 'gallery_note': 'A creator-curated selection of existing Instagram work. Open any card to see the original post.', 'empty_note': ''},
    'avanpakasastram': {**deepcopy(COMMON), 'slug': 'avanpakasastram', 'name': 'Avanpakasastram', 'wordmark': 'avan pakasastram', 'monogram': 'ap', 'theme': 'spice', 'eyebrow': 'COOKING · FOOD · KITCHEN UGC', 'headline': 'Good food.\nBetter stories.', 'accent_line': 'Better stories.', 'intro': 'From the first ingredient to the final plate. A dedicated space for cooking stories, food features and useful kitchen demonstrations.', 'about_title': 'Made for the kitchen.\nTold with flavour.', 'about': 'Avanpakasastram is the dedicated cooking portfolio for recipe-led storytelling, food features, cookware and kitchen products. Each collaboration should show the real role of a product in the cooking process—not a forced product placement.', 'pillars': ['Recipe storytelling', 'Food & ingredients', 'Cookware', 'Kitchen essentials'], 'service_angles': ['Recipe-led product integrations', 'Cookware & kitchen demonstrations', 'Food and ingredient features'], 'hero_image': 'cooking-editorial.webp', 'hero_alt': 'Illustrative South Indian meal on a warmly lit table', 'hero_caption': 'Illustrative preview artwork—not a creator portfolio sample.', 'hero_illustrative': True, 'gallery_note': 'This cooking gallery is kept separate from Avananusha’s parenting and beauty work.', 'empty_note': 'Cooking selections are being curated. No sample videos or brand collaborations have been invented.'},
    'avanadvaitham': {**deepcopy(COMMON), 'slug': 'avanadvaitham', 'name': 'Avanadvaitham', 'wordmark': 'avan advaitham', 'monogram': 'ad', 'theme': 'ritual', 'eyebrow': 'DEVOTIONAL · RITUALS · THOUGHTFUL UGC', 'headline': 'Meaningful rituals.\nThoughtful stories.', 'accent_line': 'Thoughtful stories.', 'intro': 'A respectful space for devotional storytelling, mindful rituals and relevant products—created with cultural care.', 'about_title': 'Rooted in meaning.\nCreated with care.', 'about': 'Avanadvaitham is a dedicated portfolio for devotional content and relevant puja or ritual essentials. Collaboration ideas are considered for cultural fit and presented respectfully, without promises of miracles or guaranteed spiritual outcomes.', 'pillars': ['Devotional stories', 'Puja essentials', 'Ritual setups', 'Cultural storytelling'], 'service_angles': ['Respectful product integrations', 'Ritual and setup storytelling', 'Devotional visual content'], 'hero_image': 'devotional-editorial.webp', 'hero_alt': 'Illustrative unlit brass diya with flowers and an ivory cloth', 'hero_caption': 'Illustrative preview artwork—not a creator portfolio sample.', 'hero_illustrative': True, 'gallery_note': 'Devotional work has its own curation and brand-fit review, separate from the other portfolios.', 'empty_note': 'Devotional selections are being curated. No sample videos or brand collaborations have been invented.'},
    'myratechies': {**deepcopy(COMMON), 'slug': 'myratechies', 'name': 'MyraTechies', 'wordmark': 'myra techies', 'monogram': 'mt', 'theme': 'tech', 'eyebrow': 'TECH UGC · GADGETS · DIGITAL PRODUCTS', 'headline': 'Less jargon.\nMore real-world tech.', 'accent_line': 'More real-world tech.', 'intro': 'Product-first stories that put gadgets, accessories and apps into everyday context. Clear demos. Useful details. Human explanations.', 'about_title': 'Technology,\nwith a human point of view.', 'about': 'MyraTechies is the dedicated home for tech UGC: gadgets, accessories, software and apps. Briefs focus on a genuine use case, a clear demonstration and observations supported by the product—not untested specifications or invented performance results.', 'pillars': ['Gadgets', 'Accessories', 'Apps & software', 'Product demos'], 'service_angles': ['Real-use product demonstrations', 'App & software walkthroughs', 'Tech launch content & UGC'], 'hero_image': 'tech-editorial.webp', 'hero_alt': 'Illustrative unbranded technology products on a dark studio desk', 'hero_caption': 'Illustrative preview artwork—not a creator portfolio sample.', 'hero_illustrative': True, 'gallery_note': 'Tech work lives here, independently of the parenting, cooking and devotional portfolios.', 'empty_note': 'Tech selections are being curated. No sample videos, test results or brand collaborations have been invented.'},
}

BRANDS={slug:patch_brand(slug,brand) for slug,brand in BRANDS.items()}

# Collection membership is the creator’s supplied grouping. Cross-portfolio
# assignments are not inferred from a product category.
ROWS = [
    ('DdEiKGGvEnS','Gentle-parenting conversations','', ['highlights','parenting-baby'],'reel','2026-09-09','',254807),
    ('DVJRkJkEgpm','Pregnancy & motherhood stories','', ['highlights','parenting-baby'],'reel','2026-02-24','',152947),
    ('DLp77UPSAeZ','BAKE · sunscreen product feature','BAKE', ['highlights','collaborations','skin-care'],'reel','2025-07-03','Paid collaboration disclosed',None),
    ('DfAIQ75xmFr','Pregnancy series · October','', ['highlights','parenting-baby'],'reel','2026-10-27','',2176),
    ('DdmAfXBPnBe','Pregnancy series · September','', ['highlights','parenting-baby'],'reel','2026-09-22','',9646),
    ('DUnCvZkgFzX','Glow & Lovely · skincare feature','Glow & Lovely', ['collaborations','skin-care'],'reel','2026-02-11','Ad disclosed',273),
    ('DOxsMIvALd8','Garnier · cleanser feature','Garnier', ['collaborations','skin-care'],'reel','2025-09-19','Ad disclosed',None),
    ('DJ6ZYr7y-n_','WOW Skin Science · facewash feature','WOW Skin Science', ['collaborations','skin-care'],'reel','2025-05-21','Ad / collaboration disclosed',None),
    ('DJULjLtSaF-','Diyaa Pure · white-turmeric feature','Diyaa Pure', ['collaborations','skin-care'],'reel','2025-05-06','',None),
    ('DcVwhedSJ18','Redken · hair-serum feature','Redken', ['hair-care'],'reel','2026-08-22','PR disclosed; payment not established',151),
    ('DcQR0NKSgFp','L’Oréal Professionnel · hair-mask feature','L’Oréal Professionnel', ['hair-care'],'reel','2026-08-20','Ad disclosed',217),
    ('Daau5WPS3YK','Matrix · shampoo & conditioner','Matrix', ['hair-care'],'reel','2026-07-05','Ad disclosed',191),
    ('DLp8PnXSXOP','BAKE · hair-care product feature','BAKE', ['hair-care'],'reel','2025-07-03','Paid collaboration disclosed',None),
    ('DcAxeEMyw_I','Kidzola · family-cooking feature','Kidzola', ['parenting-baby','kids-collabs'],'reel','2026-08-14','',236),
    ('C_zmo0uSe1k','Parachute Advansed Baby · product post','Parachute Advansed Baby', ['parenting-baby','kids-collabs'],'post','2024-09-12','Home Tester Club opportunity mentioned',None),
    ('DNz-NjdQIbx','Nory · pregnancy-kit feature','Nory', ['parenting-baby','kids-collabs'],'reel','2025-08-26','',None),
]


def initial_videos():
    out=[]
    for order,(code,title,client,tags,kind,posted,disclosure,plays) in enumerate(ROWS):
        risk = ''
        if code in {'C_zmo0uSe1k','DcAxeEMyw_I','DNz-NjdQIbx','DJULjLtSaF-','DLp8PnXSXOP','DLp77UPSAeZ'}:
            risk = 'Review legacy caption claims before repurposing. Do not repeat medical, developmental, diagnostic, regrowth, universal-safety or product-performance claims without appropriate evidence. Public portfolio summaries are neutral.'
        out.append({'id':code,'title':title,'client':client,'url':f'https://www.instagram.com/{"p" if kind=="post" else "reel"}/{code}/','kind':kind,'brands':['avananusha'],'tags':tags,'status':'published','thumbnail':f'reels/{code}.webp','sort_order':order,'disclosure':disclosure,'notes_private':risk,'posted_date':posted,'source_checked':CHECKED_DATE,'source_profile':'avananusha','public_plays_snapshot':plays,'metrics_approved':False})
    return [patch_existing_video(v) for v in out]+new_videos()
