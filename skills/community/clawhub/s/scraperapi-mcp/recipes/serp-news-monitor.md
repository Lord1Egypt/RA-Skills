# SERP & News Monitoring — Detailed Guide

A workflow for monitoring Google Search (SERP) and Google News using the `scrape` MCP tool. Useful for SEO monitoring, media tracking, competitive intelligence, and trend analysis.

## Overview

This workflow enables:

- Fetching Google Search results (organic + Top Stories)
- Fetching Google News headlines
- Normalizing and canonicalizing URLs
- Deduplicating results
- Producing structured JSON output
- Generating change reports (new / removed / rank shifts)

All web fetching is performed via the **ScraperAPI MCP tool (`scrape`)**.

## Inputs to Ask For (only if missing)

- **Query** (required)
- **Mode**: `serp` or `news` (default: `serp`)
- **Locale**: `hl` (default: `en`), `gl` (default: `GB`)
- **Result count** for SERP (default: 10)
- **Recency filter**: none | last day | last week | last month

## URLs to Build

### SERP

```
https://www.google.com/search?q=<QUERY>&num=<N>&hl=<HL>&gl=<GL>&pws=0
```

Recency filters (append to URL):
- Last day → `&tbs=qdr:d`
- Last week → `&tbs=qdr:w`
- Last month → `&tbs=qdr:m`

### Google News

```
https://news.google.com/search?q=<QUERY>&hl=<HL>&gl=<GL>&ceid=<GL>:<HL>
```

## Fetch Strategy (must follow)

1. Call `scrape` with just the URL first (cheapest).
2. If the page is incomplete or shows a consent/interstitial:
   - Retry with `deviceType: "desktop"`
   - Then try `deviceType: "mobile"` if needed
3. If geo issues / repeated errors: retry with `countryCode` matching the market (e.g., `gb`, `us`).
4. If blocking persists: set `premium: true`. If still failing, use `ultraPremium: true`.
   - **NEVER** combine `premium` and `ultraPremium`.

## Extraction Requirements

### SERP JSON

Extract and return:
- `query`, `fetched_at`, `locale {hl, gl}`, `num`
- `organic_results`: array of
  - `rank` (1..N)
  - `title`
  - `link` (canonicalized; remove Google redirect wrappers)
  - `displayed_link` (if visible)
  - `snippet` (if visible)
- `top_stories` (optional): array of
  - `title`
  - `source` (if visible)
  - `time` (if visible)
  - `link` (canonicalized)

### News JSON

Extract and return:
- `query`, `fetched_at`, `locale {hl, gl}`
- `headlines`: array of
  - `title`
  - `source` (publisher)
  - `time` (relative time if present)
  - `link` (canonicalized)
  - `snippet` (if visible)

## Normalization Rules

- If a result link is a Google redirect (e.g., `/url?q=<real_url>`), extract and use the real URL.
- Canonicalize URLs by stripping common tracking params (`utm_*`).
- Dedupe by canonical URL; if missing/unstable, fallback to hash(title + source).

## Output Format (always)

Return a single JSON object:

```json
{
  "mode": "serp | news",
  "query": "...",
  "locale": { "hl": "...", "gl": "..." },
  "fetched_at": "...ISO timestamp...",
  "results": { "..." },
  "notes": [ "..." ]
}
```

If the user asks for insights, add a short prose summary after the JSON.

## Optional: Change Report

If the user provides a previous snapshot JSON, compute:

- `new_items` — results present now but not in the previous snapshot
- `removed_items` — results in the previous snapshot but not now
- `moved_items` (SERP only) — results whose rank changed

Then summarize the changes.

## Best Practices

- **Always use `scrape`** (not `google_search` or `google_news`) for this workflow — scraping Google directly gives full page context including Top Stories, People Also Ask, etc.
- **Set `outputFormat: "markdown"`** for easier parsing of the HTML structure.
- **Use recency filters** to keep results fresh for monitoring use cases.
- **Store snapshots** as JSON to enable change detection across runs.
- **Dedupe before comparing** — URL canonicalization prevents false positives in change reports.
