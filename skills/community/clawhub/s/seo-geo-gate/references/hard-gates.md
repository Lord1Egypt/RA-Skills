# Hard gates — exact thresholds + why + how to fix

Each gate below is enforced as a **build-fail** in the source project (the reference site). Format: the rule → why it matters → general fix → the Astro+Cloudflare reference implementation. `audit-seo.mjs` checks gates 1–11; gate 12 needs your routing config.

---

## 1. Exactly one `<h1>`
**Rule:** every page has `<h1>` count === 1.
**Why:** the H1 is the page's primary topic signal; zero = no topic, multiple = diluted/ambiguous topic for both classic crawlers and LLMs extracting page meaning.
**Fix:** one H1 per page (the page title/hero). Demote extra H1s to H2/H3. Section headings are H2+.
**Reference:** one `<h1>` in the page hero; `audit-h1.mjs` fails build otherwise.

## 2. Viewport meta
**Rule:** `<meta name="viewport">` exists and content contains both `width=device-width` and `initial-scale=1`.
**Why:** mobile-first indexing — without it Google renders at desktop width and mobile usability tanks.
**Fix:** `<meta name="viewport" content="width=device-width, initial-scale=1.0">` in `<head>`.
**Reference:** emitted once in `BaseLayout.astro`; `audit-viewport.mjs`.

## 3. Semantic landmarks
**Rule:** each page contains `<main>` **and** `<nav>` **and** `<footer>`.
**Why:** landmark structure aids accessibility (screen readers) and gives crawlers/LLMs a content vs chrome map. Accessibility and SEO overlap heavily.
**Fix:** wrap primary content in `<main>`, nav in `<nav>`, footer in `<footer>`. Use `<article>`/`<aside>` where semantically right.
**Reference:** shared `Nav.astro` / `Footer.astro` + `<main>` in layout; `audit-semantic.mjs`.

## 4. Title + meta description
**Rule:** `<title>` present (warn outside ~10–60 chars); `<meta name="description">` present (warn outside ~50–160 chars). **Length is a soft warn, not an error** — the reference site deliberately runs longer, keyword/entity-rich titles for AI extraction. Missing entirely = error.
**Why:** title is the #1 on-page ranking factor and the SERP/AI headline; description drives CTR and is often the snippet LLMs quote.
**Fix:** unique, descriptive title + description per page. Front-load the primary entity. Don't keyword-stuff.
**Reference:** per-route `title`/`description` fields in `routes.ts`; build asserts description length 20–240; `<meta keywords>` intentionally omitted (ignored/abused signal).

## 5. Canonical — build-time, absolute, host-matched
**Rule:** `<link rel="canonical">` with an absolute `https://…` URL whose host === the deploy origin.
**Why:** prevents duplicate-content dilution across www/apex, trailing-slash, query-param variants. Wrong-host canonical (e.g. staging URL shipped to prod) is catastrophic — it tells Google your prod pages are duplicates of a noindex domain.
**Fix:** generate canonical at **build time** from a `PUBLIC_SITE_ORIGIN` env var baked into the HTML — never a runtime value. One built artifact = one origin; never deploy the same build to two domains.
**Reference:** `buildCanonical(origin, path)` (rejects trailing-slash origin / non-`/` path); `BaseLayout` reads `import.meta.env.PUBLIC_SITE_ORIGIN`; `build:dev` vs `build:prod` inject different origins; `audit-routes.mjs` asserts `dist` canonical host === `PUBLIC_SITE_ORIGIN`. **Pitfall:** the Cloudflare Worker runtime `BASE_URL` var does NOT enter the static build — don't use it for canonical.

## 6. Open Graph
**Rule:** `og:title` + `og:image` present (warn if missing).
**Why:** controls how links render when shared (social, chat, AI surfaces). Missing OG = ugly/empty unfurls = lower CTR.
**Fix:** `og:title`, `og:description`, `og:image` (absolute URL, ~1200×630), `og:type`, plus `twitter:card=summary_large_image`.

## 7. Images
**Rule (per `<img>`):** has `width` + `height` + `alt`; non-hero images `loading="lazy"`; hero/LCP image `loading="eager"` + `fetchpriority="high"`. **Rule (per file):** ≤ **500 KB** (`.webp/.avif/.jpg/.jpeg/.png/.gif/.svg`).
**Why:** `width`/`height` reserve space → no CLS (a Core Web Vital). `alt` = accessibility + image SEO. `lazy` on below-fold cuts initial bytes; `fetchpriority="high"` on the LCP image cuts LCP. Oversized images are the #1 LCP killer.
**Fix:** use a build-time image pipeline (Astro `<Image>`, `next/image`, etc.) that emits dimensions + modern formats. Recompress anything >500 KB to WebP/AVIF. Lazy-load everything except the one hero image.
**Reference:** `astro:assets` auto WebP/AVIF + dimensions; `audit-images.mjs` (500 KB on the *built* artifact, not source).

## 8. No inline executable script / no inline handlers
**Rule:** no `<script>` with executable body unless `type` ∈ {`application/ld+json`, `application/json`, `importmap`}; no `on*=` attributes (`onclick`, `onload`, …).
**Why:** enables a strict CSP `script-src 'self'` (no `'unsafe-inline'`) — a security + trust signal — and forces JS into cacheable, deferred external modules (faster than parser-blocking inline). JSON-LD is a non-executable data block, so it's allowed.
**Fix:** move inline `<script>` to external `.js`/ES modules; rewrite `onclick=` to `addEventListener`. In Astro, set `vite: { build: { assetsInlineLimit: 0 } }` so it never auto-inlines small scripts, and avoid `is:inline`.
**Reference:** `audit-inline.mjs`; CSP `script-src 'self'`.

## 9. No external resource references
**Rule:** no `http(s)://` URLs on `<link rel=stylesheet/preload/prefetch>`, `<script src>`, `<img src>`, `<source>`, `srcset`, CSS `url()` / `@import`. (Cross-host `<a>` links are fine — and should get `rel="nofollow noopener"`.)
**Why:** self-hosting fonts/CSS/JS/images removes third-party DNS+TLS round-trips (speed), satisfies a strict CSP, and removes privacy/availability dependencies. Google Fonts via `<link>` is a classic offender.
**Fix:** download fonts to `/fonts/` with self-hosted `@font-face` (preload key weights); pull remote images into the repo and run them through the image pipeline; self-host any CDN script.
**Reference:** `audit-external.mjs` (empty whitelist); `inventory-remote-assets.mjs` to find offenders; `codemod-nofollow.mjs` post-build adds `rel="nofollow noopener"` to cross-host `<a>`.

## 10. Page weight budget
**Rule:** HTML bytes + same-page referenced **local** CSS + same-page **local** JS ≤ **500 KB** (images counted separately under gate 7).
**Why:** transfer size drives load time → LCP/INP and crawl efficiency. A 500 KB text budget keeps pages fast and forces discipline on framework bloat.
**Fix:** code-split, drop unused CSS/JS, inline only critical CSS, defer the rest. If over budget, the page is doing too much.
**Reference:** `audit-size.mjs`. (the reference site also inlines all stylesheets into HTML to kill render-blocking CSS round-trips — a deliberate trade of cache-reuse for first-paint speed.)

## 11. Structured data (JSON-LD)
**Rule:** JSON-LD present on content pages; site-wide **Organization** + **WebSite**; page-appropriate Article/Product/FAQPage/Breadcrumb.
**Why:** structured data is how machines (Google rich results AND LLMs) reliably extract entities, relationships, and facts. It's the single biggest GEO lever after being crawlable. See `structured-data.md`.
**Fix:** emit a nested `@graph` with Organization+WebSite globally, plus the right type per page. Validate at validator.schema.org / Google Rich Results Test.
**Reference:** `seo.ts` builders + `JsonLd.astro`; breadcrumb auto-emits `BreadcrumbList`.

## 12. URL hygiene (needs your routing config — not in audit-seo.mjs)
**Rule:** every path is lowercase, has a trailing slash, ≤3 segments deep, ≤256 bytes, and maps 1:1 to a page from a single route source of truth. Externally, mixed-case / missing-slash variants 301 to the canonical form.
**Why:** consistent URLs prevent duplicate-content splits and keep crawl budget focused. A single route table prevents canonical/sitemap/redirect drift.
**Fix:** one `routes.ts`-style table; enforce trailing slash (`trailingSlash: 'always'`); 301 non-canonical forms at the edge — **but skip `/api/*`, asset paths, and `*.ext`** so you don't 301-redirect away POST bodies or assets.
**Reference:** `routes.ts` (single source) → `routes.generated.json` (codegen) feeds sitemap + redirects; `audit-routes.mjs`.

---

## Baseline (accessibility ↔ SEO overlap)
- **Font-size floor:** no `font-size < 10px` anywhere (`audit-baseline.mjs`); body ~14–16px recommended. `audit-seo.mjs` flags this in standalone CSS.
- **Tap targets:** interactive elements ≥ 40×40px (inline links pad via line-height/padding).
- **HTTPS + HSTS + TLS 1.2+**, **Gzip/Brotli** — table stakes; `audit-live.mjs` checks HSTS.
