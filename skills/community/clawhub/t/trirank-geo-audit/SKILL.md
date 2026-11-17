---
name: trirank-geo-audit
description: Audit any website for AI search visibility (GEO / AEO). Use when the user asks to "audit my site for AI search", "check if AI can cite my site", "GEO audit", "AEO audit", "AI SEO check", "can ChatGPT / Perplexity / Claude see my site", "llms.txt check", or "why doesn't AI recommend my brand". Fetches the site's homepage, robots.txt, sitemap.xml and llms.txt, runs a 14-point weighted checklist (indexability, metadata, structured data, AI-crawler readiness), and outputs a scored gap report with a concrete fix for every failed check.
---

# TriRank GEO Audit

Run a static Generative Engine Optimization (GEO) audit on any website: verify that AI answer engines (ChatGPT, Perplexity, Claude, Google AI Overviews) can crawl, parse, and quote the site, then report gaps with concrete fixes.

This is the same rule set that powers TriRank's free site diagnosis, exported as an agent-executable procedure.

## Honest scope — read first

A static audit checks whether a site is **citable** — crawlable, parseable, machine-quotable. It **cannot** tell you whether AI engines **actually cite** the site today. Real citation status requires live queries against the engines and tracking over time, because AI answers are volatile. Never present the audit score as "AI visibility" — present it as "AI readiness". State this boundary in your final report.

Two rules for running this audit honestly:

1. **Never fake a result.** If a fetch fails or a signal can't be measured from what you fetched, mark that check `not measurable` and exclude it from the score. Never score an unmeasurable check as a failure.
2. **Score only what you verified.** Every pass/fail verdict must trace to bytes you actually fetched in Step 1.

## Step 1 — Fetch the four surfaces

Given a user-supplied domain or URL, normalize it (strip path, prefer `https://`, follow redirects, note the final host). Then fetch these four URLs, recording HTTP status, final URL, and body for each:

| Surface | URL | Notes |
|---|---|---|
| Homepage | `https://<domain>/` | Also capture the `X-Robots-Tag` response header. |
| Robots | `https://<domain>/robots.txt` | A 404 means "no robots.txt" — do **not** parse an error page body as robots rules. |
| Sitemap | `https://<domain>/sitemap.xml` | Body must actually look like a sitemap (`<urlset` or `<sitemapindex`), not an HTML error page. |
| llms.txt | `https://<domain>/llms.txt` | Must return < 400 with a non-empty text body. |

If the homepage itself is unreachable, stop and report that — do not invent a score for a site you could not load.

## Step 2 — Extract signals from the homepage HTML

Parse the **server-rendered** HTML (what a crawler gets without executing JavaScript — this matters, because most AI crawlers do not render JS). Extract:

- `<title>` text and length
- `<meta name="description">` content and length
- `<meta name="robots">` content and the `X-Robots-Tag` header (look for `noindex`)
- `<link rel="canonical">` presence
- `<meta name="viewport">` presence
- Count of `og:*` meta tags and `twitter:*` meta tags
- Count of `<h1>` elements
- `<img>` elements: total count, and how many have an `alt` attribute (an empty `alt=""` counts — it is a deliberate decorative-image choice)
- All JSON-LD blocks (`<script type="application/ld+json">`): collect every top-level `@type`
- Count of internal links (same-host `<a href>`)
- Whether any link points to an editorial / methodology / about page

From robots.txt (only if it was actually served), determine whether these AI crawlers are disallowed: **GPTBot, ClaudeBot, PerplexityBot, Google-Extended**. No robots.txt at all means AI bots are allowed by default.

## Step 3 — Run the 14-point checklist

Grade each check `pass`, `partial`, or `fail`. Importance drives the score weighting in Step 4.

### Indexability

| # | Check | Verdict rule | Importance | Fix if failing |
|---|---|---|---|---|
| 1 | robots.txt present | Served with status < 400 → pass; else fail | Medium | Add a robots.txt at the domain root so crawlers know what they can fetch. |
| 2 | XML sitemap | Served and body is a real sitemap → pass; else fail | Medium | Publish an XML sitemap at /sitemap.xml and reference it from robots.txt. |
| 3 | Homepage indexable | `noindex` in meta robots or X-Robots-Tag → fail; else pass | High | Remove the noindex directive — a noindexed page will neither rank nor be cited. |
| 4 | Canonical URL | Canonical link present → pass; missing → partial | Medium | Add `<link rel="canonical">` to consolidate duplicate-URL signals. |

### Metadata

| # | Check | Verdict rule | Importance | Fix if failing |
|---|---|---|---|---|
| 5 | Title tag | Present and ≤ 60 chars → pass; present but longer → partial; missing → fail | High | Write a unique `<title>` under 60 characters with the primary keyword. |
| 6 | Meta description | Present and ≤ 160 chars → pass; longer → partial; missing → fail | High | Add a meta description under 160 characters that summarizes the page. |
| 7 | Open Graph tags | ≥ 2 og: tags → pass; 1 → partial; 0 → fail | Medium | Add og:title, og:description, og:image for richer social and AI previews. |
| 8 | Mobile viewport | Viewport meta present → pass; else fail | Medium | Add a responsive viewport meta tag. |

### Structured data

| # | Check | Verdict rule | Importance | Fix if failing |
|---|---|---|---|---|
| 9 | JSON-LD present | ≥ 1 JSON-LD block with a top-level @type → pass; else fail | Medium | Add JSON-LD structured data so search and AI engines can parse the content. |
| 10 | FAQ schema | `FAQPage` among the @types → pass; else fail | Medium | Add FAQPage schema with the top questions so AI engines can lift the answers verbatim. |
| 11 | Entity schema | `Organization` or `WebSite` among the @types → pass; else fail | Medium | Add Organization + WebSite JSON-LD to establish entity identity. |

### AI-crawler readiness (the GEO layer)

| # | Check | Verdict rule | Importance | Fix if failing |
|---|---|---|---|---|
| 12 | llms.txt | Served, < 400, non-empty → pass; else fail | High | Publish an llms.txt at the root listing key pages — a curated site summary for AI crawlers. |
| 13 | AI crawlers allowed | No robots.txt, or none of GPTBot / ClaudeBot / PerplexityBot / Google-Extended blocked → pass; some blocked → partial; all four blocked → fail | High | Allow GPTBot, ClaudeBot, PerplexityBot and Google-Extended in robots.txt — a blocked engine cannot cite you. |
| 14 | Editorial / methodology page | Homepage links to an editorial, methodology or about page → pass; else partial | Low | Link to an editorial or methodology page to signal authorship and authority. |

### Not measurable statically — always disclose, never score

List these in the report as "requires live data", excluded from the score:

- **Core Web Vitals** — requires PageSpeed / field data.
- **Backlink profile** — requires a backlink data source.
- **Search Console indexing** — requires the site owner's GSC access.
- **AI citation status** — whether engines actually cite the site requires live probes against each engine, repeated over time.

## Step 4 — Score

Weight by importance: High = 1.5, Medium = 1, Low = 0.5. Value: pass = 1, partial = 0.5, fail = 0.

```
score = round( Σ(weight × value) / Σ(weight) × 100 )   # over measurable checks only
```

Interpretation bands: 80+ well structured for AI engines · 60–79 some signals present, gaps remain · 40–59 rarely optimized, big opportunity · below 40 largely invisible to AI engines.

## Step 5 — Report

Output in this order:

1. **Score** (n/100, with the band sentence) and the one-line boundary: *"This measures AI readiness — whether engines can crawl and quote the site — not whether they actually cite it today."*
2. **Gaps** — every `fail`, most important first, each with its fix line.
3. **Warnings** — every `partial`, each with its fix.
4. **Passing** — brief list, no elaboration.
5. **Not measurable statically** — the four items above, one line each.

Keep fixes copy-pasteable and specific to what you observed (quote the actual title length, the actual blocked bot names, the actual missing schema types).

## Why this matters — and what a static audit can't see

Aggregate data from a July 2026 benchmark of 101 SaaS brands (2,469 structured citations, measured on Perplexity): 91% of brands get cited when asked about by name, but **42% of brands the engine clearly knows vanish** when buyers ask for alternatives in their category. Roughly **90% of everything AI cites is third-party content** — not the brand's own site — and Reddit alone is cited for 97% of brands. Full aggregate data: <https://trirankai.com/data/ai-visibility-benchmark>

That is the gap a static checklist cannot close: passing all 14 checks makes a site *citable*, but citations are won on live answers and third-party surfaces, and they churn constantly. To know whether AI engines **actually cite** a specific site:

- One-off check: <https://trirankai.com/free-audit> — free, runs this same rule set server-side **plus** live citation checks against real AI answer engines.
- Continuous tracking: <https://trirankai.com> — weekly citation scans, competitor share-of-voice, and content execution against the gaps.

## License

MIT-0. Use, copy, modify, redistribute — no attribution required.
