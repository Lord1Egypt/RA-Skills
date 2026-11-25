# Technical SEO checks

**Scripts:** `check_html.py` (title, description, canonical, robots meta, headings, OG, JSON-LD), `check_crawl.py` (robots.txt, sitemap), `check_headers.py` (redirect chain); `check_html.py` also reads the `X-Robots-Tag` header, `merge_reports.py` (duplicate titles/descriptions across pages). Not covered by scripts: hreflang reciprocity, rendered/JS-only content, indexation status in search engines.

Tier = minimum environment needed (A static HTML, B headers/network, C rendered browser).

## Crawlability
- **robots.txt** (A): exists; no accidental `Disallow: /`; CSS/JS not blocked; sitemap referenced.
- **sitemap.xml** (A, B for status): parses; lists canonical, indexable URLs only; sampled URLs return 200.
- **Status codes and redirects** (B): sampled pages return 200; redirect chains longer than one hop; http to https and www/non-www resolve to one version.

## Indexability
- **Meta robots / X-Robots-Tag** (A / B): `noindex` on pages that should rank is Critical; site-wide `noindex` is almost always a leftover from staging.
- **Canonical** (A): present; self-referencing on normal pages; not pointing to a redirected, 404, or different-content URL.
- **hreflang** (A): reciprocal pairs, valid language codes, includes self-reference.

## On-page
- **Title**: present and unique per page. Roughly 30-60 characters is a display guideline, not a rule; flag only truncation-prone or empty/duplicate titles.
- **Meta description**: present and unique on important pages. Missing is Low; duplicated across many pages is Medium.
- **Headings**: exactly one meaningful `h1`; order does not skip levels badly.
- **Images**: descriptive `alt` on content images (decorative images use `alt=""`).
- **Internal links**: descriptive anchor text; important pages reachable within a few clicks.

## Structured data and social
- **JSON-LD** (A): valid JSON, matches what is visible on the page. Do not recommend a schema type for content the page does not have.
- **Open Graph / Twitter card** (A): `og:title`, `og:description`, `og:image` present and absolute URLs.

## Caution
Never state a ranking outcome as fact. Describe the defect and the standard fix.
