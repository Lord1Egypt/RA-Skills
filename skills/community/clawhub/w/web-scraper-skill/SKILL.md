---
name: web-scraper-skill
description: >
  Use this skill to scrape, crawl, or extract data from websites using Apify or Firecrawl APIs.
  Trigger whenever the user wants to: scrape a URL, crawl a website, extract structured data from web pages,
  run an Apify Actor, batch scrape multiple URLs, search and scrape the web, map a site's URLs,
  collect product/price/review data, or build any web data pipeline. If the user says things like
  "scrape this site", "get data from this URL", "crawl this website", "run an Apify actor", "use Firecrawl",
  "extract content from a page", "pull data from the web", or mentions any web data extraction task —
  always use this skill. Also use it when the user wants to choose between Apify and Firecrawl.
---

# Web Scraper Skill (Apify + Firecrawl)

This skill helps Openclaw scrape and extract data from websites using two powerful APIs:
- **Firecrawl** — best for scraping individual pages, crawling entire sites, and getting LLM-ready content (markdown)
- **Apify** — best for specialized scrapers (social media, Google Maps, e-commerce, etc.) via pre-built Actors

---

## Quick Decision Guide: Apify vs Firecrawl

| Use Case | Recommended Tool |
|---|---|
| Scrape a single page into markdown/JSON | **Firecrawl** `/scrape` |
| Crawl an entire website (follow links) | **Firecrawl** `/crawl` |
| Map all URLs on a site | **Firecrawl** `/map` |
| Search web + scrape results | **Firecrawl** `/search` |
| Scrape Instagram / TikTok / Twitter | **Apify** (social actors) |
| Scrape Google Maps / reviews | **Apify** (compass/crawler-google-places) |
| Scrape Amazon products | **Apify** (apify/amazon-scraper) |
| Scrape Google Search results | **Apify** (apify/google-search-scraper) |
| Custom actor / any Apify Store actor | **Apify** |

---

## Authentication

Both APIs require API keys passed via headers. Always ask the user for their key if not provided.

**Firecrawl:** `Authorization: Bearer fc-YOUR_API_KEY`
**Apify:** `Authorization: Bearer YOUR_APIFY_TOKEN` (or `?token=YOUR_TOKEN` in URL)

---

## Firecrawl API Reference

**Base URL:** `https://api.firecrawl.dev/v2`

### 1. Scrape a Single Page
```http
POST /v2/scrape
Authorization: Bearer fc-YOUR_API_KEY
Content-Type: application/json

{
  "url": "https://example.com",
  "formats": ["markdown"],          // Options: markdown, html, rawHtml, links, screenshot, json
  "onlyMainContent": true,          // Strips nav/footer/ads
  "waitFor": 0,                     // ms to wait before scraping (for JS-heavy pages)
  "timeout": 30000,                 // ms
  "blockAds": true,
  "proxy": "auto"                   // "auto", "basic", or "stealth"
}
```
**Response:** `{ "success": true, "data": { "markdown": "...", "metadata": {...} } }`

### 2. Crawl an Entire Website
Crawling is async — starts a job, then poll for results.

```http
POST /v2/crawl
{
  "url": "https://docs.example.com",
  "limit": 50,                      // Max pages
  "maxDepth": 3,
  "allowExternalLinks": false,
  "scrapeOptions": {
    "formats": ["markdown"],
    "onlyMainContent": true
  }
}
```
**Response:** `{ "success": true, "id": "crawl-job-id" }`

**Poll status:**
```http
GET /v2/crawl/{crawl-job-id}
```
**Response:** `{ "status": "completed", "total": 50, "data": [...] }`

### 3. Map a Website's URLs
```http
POST /v2/map
{ "url": "https://example.com" }
```
**Response:** `{ "success": true, "links": [{ "url": "...", "title": "..." }] }`

### 4. Search + Scrape in One Call
```http
POST /v2/search
{
  "query": "best web scraping tools 2025",
  "limit": 5,
  "scrapeOptions": { "formats": ["markdown"] }
}
```
**Response:** `{ "data": [{ "url": "...", "title": "...", "markdown": "..." }] }`

### 5. Batch Scrape Multiple URLs
```http
POST /v2/batch/scrape
{
  "urls": ["https://a.com", "https://b.com"],
  "formats": ["markdown"]
}
```
Returns a job ID; poll with `GET /v2/batch/scrape/{id}`

---

## Apify API Reference

**Base URL:** `https://api.apify.com/v2`
**Auth:** Pass token as query param `?token=YOUR_TOKEN` or in Authorization header.

### Core Workflow
Apify runs "Actors" (pre-built scrapers). The flow is:
1. **Start a run** → get a `runId` and `defaultDatasetId`
2. **Poll status** until `SUCCEEDED`
3. **Fetch results** from the dataset

### 1. Run an Actor (Async)
```http
POST /v2/acts/{actorId}/runs?token=YOUR_TOKEN
Content-Type: application/json

{ ...actor-specific input... }
```
**Response:**
```json
{
  "data": {
    "id": "RUN_ID",
    "status": "RUNNING",
    "defaultDatasetId": "DATASET_ID"
  }
}
```

Common Actor IDs:
- `apify/web-scraper` — generic JS scraper
- `apify/google-search-scraper` — Google SERPs
- `compass/crawler-google-places` — Google Maps
- `apify/instagram-scraper` — Instagram
- `clockworks/free-tiktok-scraper` — TikTok
- `apify/amazon-scraper` — Amazon products

### 2. Poll Run Status
```http
GET /v2/acts/{actorId}/runs/{runId}?token=YOUR_TOKEN
```
Poll until `status` is `SUCCEEDED` or `FAILED`. Recommended interval: 5 seconds.

### 3. Fetch Results
```http
GET /v2/datasets/{datasetId}/items?token=YOUR_TOKEN&format=json
```
Optional params: `format` (json/csv/xlsx/xml), `limit`, `offset`

### 4. Run Synchronously (≤5 minutes)
For short runs, use the sync endpoint — it waits and returns dataset items directly:
```http
POST /v2/acts/{actorId}/run-sync-get-dataset-items?token=YOUR_TOKEN
Content-Type: application/json

{ ...actor input... }
```

### Common Actor Inputs

**Google Search Scraper:**
```json
{ "queries": "web scraping tools", "maxPagesPerQuery": 1, "resultsPerPage": 10 }
```

**Google Maps Scraper:**
```json
{ "searchStringsArray": ["restaurants in Mumbai"], "maxCrawledPlaces": 20 }
```

**Web Scraper (generic):**
```json
{
  "startUrls": [{ "url": "https://example.com" }],
  "pageFunction": "async function pageFunction(context) { const $ = context.jQuery; return { title: $('title').text() }; }",
  "maxPagesPerCrawl": 10
}
```

---

## Output Handling

- **Firecrawl** returns data directly in the response (or via polling for crawl/batch).
- **Apify** stores results in a dataset; retrieve with `GET /v2/datasets/{id}/items`.
- Both support JSON output. Firecrawl also provides clean markdown ideal for LLMs.
- Apify also supports CSV, XLSX, XML output formats.

---

## Code Templates

See `references/code-templates.md` for ready-to-run Python and JavaScript code for both APIs.

---

## Error Handling

- **Firecrawl 402** → out of credits; user needs to upgrade plan
- **Firecrawl 429** → rate limited; add delays between requests
- **Apify FAILED run** → check run logs via `GET /v2/acts/{id}/runs/{runId}/log`
- Always wrap API calls in try/catch and check `success: false` in Firecrawl responses
- Firecrawl crawls respect `robots.txt` by default
- For JS-heavy pages, increase `waitFor` (Firecrawl) or use Playwright/Puppeteer actors (Apify)

---

## Best Practices

1. **Start small** — test with 1 URL or a small `limit` before scaling
2. **Use `onlyMainContent: true`** in Firecrawl to remove nav/footer noise
3. **Choose async for large jobs** — don't use sync endpoints for crawls with 50+ pages
4. **Store API keys securely** — never hardcode them; use environment variables
5. **Check rate limits** — Firecrawl: varies by plan; Apify: 250k requests/min global
6. **Prefer Firecrawl for LLM pipelines** — markdown output is clean and ready for RAG/AI
7. **Prefer Apify for social/structured data** — specialized actors handle anti-bot better
