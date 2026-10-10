# State Line Gym — complete website source

## Preview immediately
Requires Python 3 to serve the included website. Rebuilding requires Python 3.12 or newer. No Node.js or build step is needed to preview the included HTML.

```sh
cd state-line-gym
python -m http.server 8000 --directory dist
```

Open http://localhost:8000 in your browser. Do not open the HTML with file://, because links and assets use root-relative paths.

## Files
- `dist/`: nine content pages, CSS, JavaScript, local font, logo, optimized photographs, robots, a 404 page and public contact configuration. A sitemap is generated when a public domain is configured.
- `build.py`: reusable page templates and static HTML generator.
- `config.json`: business details, pricing, checkout URLs, contact endpoint and site origin.
- `assets.json`: photo paths and descriptions.
- `prepare-assets.py`: optional photo optimization script.
- `original-assets/`: original uploaded photos ZIP, logo and design mockup.
- `brief.txt`: original project requirements and verbatim waiver.
- `validate.py`: source validation checks.
- `OWNER-NOTES.md`: outstanding business details and migration guidance.
- `vercel.json`: static deployment settings; serves the committed `dist/` directory without an install or build step.

## Push to GitHub
Create an empty GitHub repository without an initial README, license or gitignore. From this project folder, initialize and commit if it is not already a Git repository:

```sh
git init -b main
git add .
git commit -m "Prepare State Line Gym for Vercel"
```

Connect your repository and push (replace `YOUR-USERNAME` and the repository name):

```sh
git remote add origin https://github.com/YOUR-USERNAME/state-line-gym.git
git push -u origin main
```

The optimized assets and generated pages in `dist/` must be committed. The original `photos.zip` archive and design mockup are kept locally and excluded by `.gitignore`. Keep a separate backup of these originals. To regenerate photos from a fresh clone, restore `original-assets/photos.zip` first.

## Deploy with Vercel
Import the GitHub repository as a new Vercel project. Keep the Root Directory at the repository root so Vercel reads `vercel.json`. The settings are:

- Framework Preset: **Other**
- Build Command: **empty / skipped**
- Install Command: **empty / skipped**
- Output Directory: **dist**

Then select Deploy. No Python runtime, environment variables or package installation are needed for this static deployment. The configuration follows [Vercel's static deployment settings](https://vercel.com/docs/builds/configure-a-build).

Vercel serves the committed HTML rather than running `build.py`. After changing templates, business details or styles/scripts, run `python build.py` and `python validate.py`, then commit and push the updated source and `dist/` files together. If only changing CSS or JavaScript, rebuilding also updates their cache version URLs.

Once you choose your permanent domain (or Vercel production URL), set `origin` in `config.json`, rebuild and push to enable the canonical URLs, social image URLs and sitemap.

## Edit and rebuild
Edit `config.json` for business data and destinations. Edit `build.py` for page content/layout, `dist/styles.css` for styling and `dist/app.js` for interactions.

```sh
python build.py
python validate.py
```

The included local font is reused without requiring system fonts. To regenerate image variants from originals (optional):

```sh
python -m pip install -r requirements.txt
python prepare-assets.py
python build.py
```

## Deploy elsewhere
Upload the contents of `dist/` to a static web host. Configure directory index pages and the custom `404.html` error page. `origin` in `config.json` is intentionally empty until the public domain is confirmed. Set it to your full origin (for example, `https://your-domain.com`) and rebuild to generate canonical URLs, the sitemap, social image URLs and breadcrumb metadata. Local preview emits page titles, descriptions, sharing text and business schema without inventing a domain.

Privacy and Terms pages and links have been removed. The original waiver remains. The build removes stale output for those two routes, so rebuilding will not bring them back.

Enable Brotli or gzip and sensible static asset caching through your production host. CSS and JavaScript URLs include a content version so edits can refresh cached files. Hosting configuration and real-world connection speeds determine final transfer times.

## Image and loading improvements
The 33 real gym photographs have three WebP variants. The manifest records actual encoded widths, and image `sizes` match the page layouts. The home hero is preloaded and gets high fetch priority; other photos load lazily. The original logo artwork is served as a small lossless WebP, with a separate favicon. Google Maps only loads after the visitor selects the map button; directions remain available as a normal link. The final call-to-action uses a CSS gradient instead of fetching an additional background photo.

## Integrations still needed
Membership checkout URLs, the day-pass checkout URL and direct form endpoint are configurable but not connected. Until supplied, plan buttons open a contact inquiry, the day-pass CTA starts a phone call, and the contact form prepares an email. See OWNER-NOTES.md for business details and migration guidance.

## Verification
Source checks cover links, metadata, image dimensions, schema, removed routes and the exact waiver. Browser checks covered all nine pages at widths of 320, 390, 768 and 1440 pixels, plus mobile navigation, gallery controls, inquiry prefill and loading the map on demand. Production Core Web Vitals and real-device performance have not been measured. Third-party map rendering was not verified.
