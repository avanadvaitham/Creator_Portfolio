# Put your public portfolios online — GitHub Pages

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
