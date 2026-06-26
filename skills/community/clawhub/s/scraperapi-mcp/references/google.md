# Google Search Tools — Detailed Guide

Five MCP tools for structured Google data extraction. All return JSON.

## Contents
- [Common Parameters](#common-parameters-shared-by-all-google-tools)
- [google_search](#tool-google_search) — web search with organic results, knowledge graph
- [google_news](#tool-google_news) — news articles with dates and sources
- [google_jobs](#tool-google_jobs) — job listings from Google Jobs
- [google_shopping](#tool-google_shopping) — product results with pricing
- [google_maps_search](#tool-google_maps_search) — local business results
- [Pagination](#pagination)
- [Time Filtering](#time-filtering)
- [Localization](#localization)

## Common Parameters (shared by all Google tools)

| Parameter | Type | Description |
|-----------|------|-------------|
| `query` | string | **Required.** Search query |
| `tld` | string | Google TLD: `"com"`, `"co.uk"`, `"de"`, `"fr"`, etc. |
| `countryCode` | string | Two-letter country code for geo-specific results |
| `num` | number | Number of results to return |
| `hl` | string | Interface language code (`"en"`, `"fr"`, `"de"`) |
| `gl` | string | Geolocation country for results (`"us"`, `"uk"`) |
| `start` | number | Result offset for pagination (not a page number) |
| `uule` | string | Google encoded location hint |

## Tool: `google_search`

Web search results with organic results, knowledge graph, and related questions.

### Additional Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `dateRangeStart` | string | Start date filter (MM/DD/YYYY) |
| `dateRangeEnd` | string | End date filter (MM/DD/YYYY) |
| `timePeriod` | enum | `"1H"`, `"1D"`, `"1W"`, `"1M"`, `"1Y"` |
| `tbs` | string | Custom time/date filter (advanced, overrides timePeriod) |
| `includeHtml` | boolean | Include raw HTML in response |

### Response Structure

```json
{
  "organic_results": [
    { "title": "...", "link": "...", "snippet": "...", "position": 1 }
  ],
  "knowledge_graph": { "title": "...", "description": "...", "..." },
  "related_questions": [
    { "question": "...", "answer": "...", "source": "..." }
  ],
  "videos": [
    { "title": "...", "link": "...", "duration": "..." }
  ],
  "pagination": { "next": "...", "other_pages": {} }
}
```

### Best Practices
- Extract URLs from `organic_results[].link` to scrape full content.
- Use `timePeriod: "1D"` or `"1W"` for current events and recent information.
- Use `dateRangeStart`/`dateRangeEnd` (MM/DD/YYYY) for specific date ranges.
- Craft specific queries — `"python asyncio tutorial site:docs.python.org"` beats `"python async"`.

---

## Tool: `google_news`

News articles with publication dates and sources.

### Additional Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `dateRangeStart` | string | Start date filter (MM/DD/YYYY) |
| `dateRangeEnd` | string | End date filter (MM/DD/YYYY) |
| `timePeriod` | enum | `"1H"`, `"1D"`, `"1W"`, `"1M"`, `"1Y"` |

### Best Practices
- Always set `timePeriod` for news — stale news is rarely useful.
- `"1H"` for breaking/developing stories, `"1D"` for today's news, `"1W"` for recent coverage.
- Combine with `scrape` to read full articles from the returned links.

---

## Tool: `google_jobs`

Job listings from Google Jobs aggregator.

### Parameters
Only common parameters (no date/time filtering — listings are inherently current).

### Best Practices
- Include location in the query: `"software engineer San Francisco"`.
- Use `countryCode` for country-specific job boards.

---

## Tool: `google_shopping`

Product results with pricing and ratings.

### Additional Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `includeHtml` | boolean | Include raw HTML in response |

### Best Practices
- Include brand/model for specific products: `"iPhone 15 Pro Max 256GB"`.
- Use `countryCode` for region-specific pricing and availability.
- Good for price comparison tasks.

---

## Tool: `google_maps_search`

Local business results with reviews, ratings, and contact info.

### Additional Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `latitude` | string | Map center latitude (e.g., `"40.7128"`) |
| `longitude` | string | Map center longitude (e.g., `"-74.0060"`) |
| `zoom` | string | Zoom level (e.g., `"12"`) |
| `includeHtml` | boolean | Include raw HTML in response |

Note: Maps does **not** have `num`, `start`, `hl`, `gl`, or `uule` — only `tld` and `countryCode` from common params.

### Best Practices
- **Always provide `latitude`/`longitude`** for location-relevant queries — without them, results may not be local.
- Include the location in the query as well: `"coffee shops downtown Austin"`.
- `zoom` controls search radius — lower values = wider area.

---

## Pagination

All Google tools (except Maps) support pagination via `num` + `start`:

- `num`: results per page (e.g., 10)
- `start`: offset (e.g., 0 for page 1, 10 for page 2, 20 for page 3)

Example: To get page 3 with 10 results per page → `num: 10, start: 20`.

## Time Filtering

`timePeriod` values (search and news only):
- `"1H"` — past hour (breaking news)
- `"1D"` — past 24 hours
- `"1W"` — past week
- `"1M"` — past month
- `"1Y"` — past year

For custom date ranges, use `dateRangeStart` and `dateRangeEnd` in MM/DD/YYYY format.

The `tbs` parameter is an advanced alternative that accepts raw Google time filter strings (e.g., `"qdr:h"`, `"qdr:d"`). Prefer `timePeriod` for simplicity.

## Localization

Combine these for precise localization:
- `countryCode` — proxy location (affects what Google shows for that region)
- `tld` — Google domain (`"co.uk"` for google.co.uk)
- `hl` — interface language
- `gl` — geographic boost for results
