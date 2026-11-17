# Search engines and speed (before and after going live)

Ported from 6x7-app-factory's `checklists/seo.md` and `checklists/performance.md` (lessons from the 6x7 launches), minus what Shipyard's template and `verify.mjs` already do (robots, sitemap, llms.txt, icons, per-page canonical, `poweredByHeader: false`, security headers). Tick each with the student; fix in a pull request.

## Make a public app searchable (checklist)

1. **One canonical site URL, lowercase**, with `https://` and no trailing slash (`NEXT_PUBLIC_SITE_URL=https://<your-domain>`). Use it for `metadataBase`, canonicals, the sitemap and robots. Mixed case or `www`/non-`www` both live means duplicate pages: redirect one to the other.
2. **Sitemap of real public pages only**: home, about, pricing, help, blog posts, privacy, terms. Never sign-in-only pages, `/api`, `/admin`, `/settings`, previews, or pages that redirect or 404. Every URL absolute, on the canonical host.
3. **robots** allows public pages, disallows `/api/`, `/admin`, `/settings`, app-only routes and private areas, and points to `Sitemap: https://<your-domain>/sitemap.xml`. Never `Disallow: /` on a public app.
4. **Metadata**: `metadataBase`, unique title and description per page, `alternates.canonical` per page, Open Graph and Twitter card with an OG image (1200x630).
5. **JSON-LD** in the layout or home page: `WebSite` (name, url), `Organization` (name, url, logo), and `SoftwareApplication` for an app (name, applicationCategory, operatingSystem `Web`, offers with price `0` if free).
6. **A short indexable landing page** at `/` (or `/about`) that signed-out visitors and crawlers can read: one H1 saying what the app does, a few sentences, a sign-up button. An app whose home page is only a sign-in form ranks for nothing.
7. **Private apps and betas: `noindex`** on every page (`robots: { index: false }` / the private marker) and an empty sitemap. Write down that it must be removed at launch; a forgotten `noindex` is the most common reason a launched app never shows up in Google. `verify` warns while it is on.

## Search engines (public apps)

- Unique `<title>` and description per page, one H1 per page, alt text on every image.
- `metadataBase` set from the site address so share images get full URLs; an Open Graph image and Twitter card on the home page.
- JSON-LD `WebSite` and `Organization` in the layout (`Article` on blog posts, breadcrumbs on nested pages).
- `robots` never says `Disallow: /` for the whole site; private routes (`/api/`, `/settings`, `/admin`) are disallowed.
- No duplicate addresses for the same page in the sitemap.
- Google Search Console: follow `search-console.md` (Domain property verified by a DNS TXT record, covers every subdomain; then submit each sitemap and request indexing). The proxy must not redirect sitemaps or verification files to sign-in; age gates and sign-in walls must let the home page be read.
- Private apps: `noindex` everywhere and an empty sitemap instead.

## Speed

- `next/image` for photos, lazy loading below the fold, subset fonts (`subsets: ["latin"]`).
- Fetch in parallel; no query per list row; select only the columns a page shows.
- Skeletons or `loading.tsx` on slow routes (not on pages that can answer 404).
- The proxy does not hit the database on every request (cache the check in a cookie).
- Service worker: never cache sign-in routes; bump the cache version on every deploy; serve `/sw.js` with `no-cache`.

## Lighthouse (manual before launch, optional in CI)

Lighthouse is Google's free page scorer. Budgets for public pages: performance 90 on phone, accessibility 95, best practices 95, SEO 90 (private apps: SEO is expected to fail, ignore it).

- **Before launch (always):** `node "${CLAUDE_PLUGIN_ROOT}/scripts/verify.mjs" <appDir> --only lighthouse` scores `/`, `/about` and `/sign-in` on phone and desktop against the live address and names the failing audits. Or, in the app, `npm run lighthouse -- https://<address>` (Lighthouse CI with `lighthouserc.json`). Fix what it names, redeploy, re-run.
- **In CI (optional, ask the student):** the template ships `.github/workflows/lighthouse.yml`. It runs after each Vercel deploy and by hand; set the repo variable `SITE_URL` to the live address, and `LIGHTHOUSE_SKIP_SEO=true` for a private app. It reports; it does not block merges. If the student does not want it, delete the file; never leave a job that is red on main.
- Common failures seen on the 6x7 apps: unlabeled logo or icon links (link-name), noindex left on from scaffolding (is-crawlable), low colour contrast in a theme, tap targets under 48px, animating non-composited properties (animate transform and opacity only), no Content-Security-Policy (csp-xss), too much JavaScript on the home page (total-byte-weight, unused-javascript).
- Signed-in pages are not covered by the CI job. To score them, run Lighthouse in a signed-in browser (Chrome DevTools > Lighthouse) with the student present.
