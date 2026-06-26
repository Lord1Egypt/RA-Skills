---
name: sitemap_content_scraper
description: Discover website sitemaps from robots.txt and common sitemap locations, choose the right sitemap or content family such as docs, blog, help center, academy, or changelog, and scrape selected public pages into a local folder as Markdown plus a manifest.
metadata: {"openclaw":{"requires":{"bins":["python3"]}}}
---

# Sitemap Content Scraper

Use this skill to turn a public website into a sitemap-driven scraping job. Prefer the existing sitemap structure over ad hoc crawling so the scrape stays bounded, explainable, and easy for the user to steer.

## Workflow

1. Ask for the website or URL scope if it is not already provided.
2. Run `python3 {baseDir}/scripts/discover_sitemaps.py <site-or-url>`.
3. Summarize the discovered sitemap inventory in plain language.
4. If user gave a scoped URL (for example `https://example.com/docs`), use `scope_hint_substring` from discovery output as default filter guidance.
5. Ask which content family the user wants, such as documentation, knowledge base, blog, academy, changelog, or another category.
6. Map the user request to the most relevant sitemap by name and sample URL patterns.
7. If multiple sitemaps still match, ask the user to choose one or give a tighter scope.
8. Ask for the destination folder if it is missing.
9. Run `python3 {baseDir}/scripts/scrape_sitemap.py --sitemap-url <chosen-sitemap> --output-dir <destination>`, and when a scoped URL was provided add `--include-substring <scope_hint_substring>` unless the user overrides scope.
10. Report what was scraped, where it was saved, and any skipped or failed pages.

## Quick Commands

Discover sitemap inventory:

```bash
python3 {baseDir}/scripts/discover_sitemaps.py https://example.com
```

Discover and preserve scope hint from a direct URL prompt:

```bash
python3 {baseDir}/scripts/discover_sitemaps.py https://example.com/docs
```

Scrape one sitemap into a chosen folder:

```bash
python3 {baseDir}/scripts/scrape_sitemap.py \
  --sitemap-url https://example.com/docs-sitemap.xml \
  --output-dir /tmp/example-docs
```

Filter to a subset of URLs when the sitemap mixes sections:

```bash
python3 {baseDir}/scripts/scrape_sitemap.py \
  --sitemap-url https://example.com/sitemap.xml \
  --output-dir /tmp/example-docs \
  --include-substring /docs/ \
  --exclude-substring /tag/
```

## Selection Rules

- Prefer sitemaps explicitly named for the requested content family, such as `docs-sitemap.xml`, `post-sitemap.xml`, `kb-sitemap.xml`, or `academy-sitemap.xml`.
- Use the sample URLs returned by `discover_sitemaps.py` to explain why a sitemap looks like docs, blog, help center, or another category.
- If the request is broad, offer the discovered choices instead of scraping everything by default.
- If no sitemap exists, stop and ask whether the user wants a bounded crawl workflow instead. Do not silently switch strategies.

## Output Contract

- Save one Markdown file per scraped page.
- Save `manifest.json` at the output root with success and failure details.
- Keep source URLs in the Markdown header so the corpus remains traceable.
- Preserve a stable folder structure derived from the source URL path.

Read `{baseDir}/references/sitemap-selection.md` when mapping user intent to sitemap candidates, handling ambiguous sitemap names, or explaining the output layout.

## Trigger Examples

- "Scrape `example.com/docs` content into `./out/docs`."
- "Pull the help center pages from `https://example.com/help`."
- "Find blog sitemaps for `example.com` and scrape only posts."

## Guardrails

- Scrape only public content.
- Accept only `http` and `https` targets.
- Reject `localhost`, private IP ranges, and internal-only hostnames.
- Enforce public-only targets using both hostname resolution checks and redirect-target checks at request time.
- Respect the chosen sitemap scope instead of broad site crawling.
- Avoid login flows, private dashboards, carts, checkout paths, or user-specific pages.
- Do not use authentication headers, cookies, or tokens.
- Ask before writing outside the intended working area.
- Tell the user when extraction quality looks weak on JavaScript-heavy pages. The bundled scraper is HTML-first and may miss client-rendered content.
