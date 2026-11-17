---
name: scraping-google-search-results
description: >
  Scrapes Google search results for any query using apidojo's Google Search scraper on Apify.
  Triggers when the user asks to: get Google search results for a keyword, scrape SERP data
  for a query, export Google results to a dataset, fetch URLs and snippets from Google for
  a search term, get all results from a Google search, or collect Google SERP data for
  multiple keywords. Returns URL, title, snippet, position, and SERP feature type per result.
  Ideal for SEO analysts, researchers, journalists, and competitive intelligence teams.
license: Apache-2.0
metadata:
  author: apidojo
  version: "1.0"
  apify-actor: apidojo/google-search-scraper
---

# Scraping Google Search Results

Raw SERP dataset for any search query. Returns organic results, featured snippets, People Also Ask boxes, and other SERP features.

## Prerequisites

- `APIFY_TOKEN` environment variable set
- Optional: Apify MCP server installed

## Inputs

| Parameter | Type | Required | Default | Notes |
|-----------|------|----------|---------|-------|
| `startUrls` | array | Optional | `[]` | Google search URLs |
| `searchTerms` | array | Optional | `[]` | Keywords to search on Google |
| `countryCode` | string | Optional | `US` | Country for Google search (e.g. `US`, `GB`, `TR`) |
| `languageCode` | string | Optional | — | Language for results (e.g. `en`) |
| `maxItems` | number | Optional | Unlimited | Maximum results to return across all queries |
| `maxPagesPerQuery` | integer | Optional | `1` | Maximum result pages per query |
| `mobileResults` | boolean | Optional | `false` | Fetch mobile SERP layout |
| `customMapFunction` | string | Optional | — | JavaScript function to transform each output object |

## Workflow

```
Progress:
- [ ] Step 1: Normalize query list
- [ ] Step 2: Run google-search-scraper
- [ ] Step 3: Poll for SUCCEEDED
- [ ] Step 4: Deliver SERP dataset
```

### Step 2: Run the Actor


**Recommended — run_actor.js (handles waiting, output, and file saving automatically):**
```bash
# Quick answer (prints table to chat)
node scripts/run_actor.js \
  --actor "apidojo~google-search-scraper" \
  --input '{"param": "value"}'

# Save as CSV
node scripts/run_actor.js \
  --actor "apidojo~google-search-scraper" \
  --input '{"param": "value"}' \
  --output YYYY-MM-DD_results.csv --format csv

# Save as JSON
node scripts/run_actor.js \
  --actor "apidojo~google-search-scraper" \
  --input '{"param": "value"}' \
  --output YYYY-MM-DD_results.json --format json
```
> `APIFY_TOKEN` must be set in environment or `.env` file.

**If Apify MCP is available:**
```
Tool: apify:run-actor
Actor: "apidojo~google-search-scraper"
Input:
{
  "queries": ["query1", "query2"],
  "maxPagesPerQuery": 1,
  "countryCode": "us",
  "languageCode": "en"
}
```

**REST API fallback:**
```bash
curl -X POST \
  "https://api.apify.com/v2/acts/apidojo~google-search-scraper/runs?token=$APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"queries": ["query1", "query2"], "maxPagesPerQuery": 1}'
```

Save `id` as `RUN_ID`. Poll until `status = SUCCEEDED`:
```bash
curl "https://api.apify.com/v2/actor-runs/$RUN_ID?token=$APIFY_TOKEN" | grep '"status"'
```

Fetch results:
```bash
curl "https://api.apify.com/v2/actor-runs/$RUN_ID/dataset/items?token=$APIFY_TOKEN&format=json"
```

### Step 3: Handle Edge Cases

- **0 organic results**: Query may trigger only ads or knowledge panels — note to user.
- **SERP features present (PAA, snippets)**: These are returned as separate result types — include them in output with `type` field.
- **Different results per country**: Specify `countryCode` explicitly when geo-specific results are needed.

## Output Format

```
# Google SERP Dataset: "<query>"
Query: <query> | Country: <cc> | Pages: N | Results: N

| Position | URL | Title | Snippet (truncated) | Type |
|----------|-----|-------|---------------------|------|
| 1        | ... | ...   | ...                 | organic |
| —        | ... | ...   | ...                 | featured_snippet |
| —        | ... | ...   | ...                 | paa |

Available fields: query, position, url, title, description, type (organic/
featured_snippet/paa/local_pack/image/video), sitelinks, rating, reviewsCount
```

## Troubleshooting

**Google CAPTCHA / blocks:** Actor handles this automatically; if persistent, reduce query batch size.
**Inconsistent positions:** SERP positions vary by location and personalization — use `countryCode` for consistency.