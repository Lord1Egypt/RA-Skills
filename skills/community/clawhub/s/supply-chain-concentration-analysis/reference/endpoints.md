# supply-chain-concentration-analysis — endpoint reference

> Generated from `scripts/tools.json` by `scripts/generate.mjs` — do not edit by hand.

Only the endpoints used by this workflow. Call them via `scripts/crawlora.sh` (see SKILL.md).

All paths are relative to the API base `https://api.crawlora.net/api/v1` and require the header `x-api-key: $CRAWLORA_API_KEY`. Path params like `{id}` are substituted into the URL; `GET` params go in the query string; `POST` params go in a JSON body.

**5 endpoints across 4 platform group(s).**

## ImportYeti (2)

### `importyeti_company`

- **HTTP:** `GET /importyeti/company`
- **What:** Get an ImportYeti company report. Returns an ImportYeti company report: identity, headline US customs shipment-volume metrics (total shipments, average TEU, last shipment date, estimated shipping spend), its supplier list, and recent bill-of-lading shipment activity.
- **Params:** `slug` (string, **required**) — ImportYeti company slug, the last path segment of a /company/{slug} URL

### `importyeti_search`

- **HTTP:** `GET /importyeti/search`
- **What:** Search ImportYeti companies and suppliers by name. Searches ImportYeti for companies and suppliers matching a name, returning each match's kind (company or supplier), slug, country, address, and headline shipment stats. A "company" result's slug chains into GET /importyeti/company.
- **Params:** `page` (integer, optional) — 1-indexed result page, defaults to 1; `q` (string, **required**) — Company or supplier name to search for

## Bing (1)

### `bing_search`

- **HTTP:** `GET /bing/search`
- **What:** Search Bing web results. Returns Bing web search results for a query string, including organic results, optional context panel data, related queries, people-also-ask questions, news modules, video modules, and page-based pagination. Empty optional blocks are omitted from the JSON response. Locale defaults to country=us and lang=en-us. Returns 503 on a genuine transport failure or challenge page. Bing occasionally serves a well-formed page whose results share no significant term with the query; when every attempt hits this, the response is still returned as 200 with data.low_confidence set to true (and the X-Low-Confidence header) instead of being withheld, so callers get Bing's real answer plus an honest signal to double-check it rather than nothing. Queries that use the site: operator (for example site:gov.hu) are not supported: Bing serves a bot-verification challenge for them, so they are rejected with 400 before any request is made. Use the DuckDuckGo (/api/v1/duckduckgo/search), Brave (/api/v1/brave/search), or Yahoo (/api/v1/yahoo-search/search) search endpoints for domain-restricted searches instead.
- **Params:** `count` (integer, optional) — Results per page; defaults to 10, clamped to 1..50; `country` (string, optional) — Two-letter country code; defaults to us; `lang` (string, optional) — Bing UI language; defaults to en-us; `page` (integer, optional) — 1-based page number; defaults to 1; `q` (string, **required**) — Search query

## Web (1)

### `web_scrape`

- **HTTP:** `POST /web/scrape`
- **What:** Scrape a URL into markdown, HTML, links or metadata. Fetches a single public URL and returns clean content in the requested formats (markdown, html, raw_html, links, metadata). The request body IS the ScrapeOption object itself — e.g. {"url": "https://example.com"} — do not wrap it in an extra key. With render=auto the request starts as a fast HTTP fetch and escalates to a real browser when the page is blocked or rendered with JavaScript. only_main_content (default true) strips navigation, headers, footers and other boilerplate before conversion. Only public pages are supported; respect each site's terms of use and robots directives. A handful of popular sites (Amazon, Reddit, Yelp, LinkedIn, and others) already have a dedicated, more reliable endpoint elsewhere in this API — a failed scrape against one of them names it. A Reddit URL that maps onto a dedicated Reddit endpoint (listings, search, comment threads, user and domain pages) is answered by that endpoint instead, and its response is returned as-is in data with an X-Routed-To header; send dedicated=false to always get the scraped page.
- **Params:** `scrapeOption` (object, **required**) — Scrape options
- **REST body:** Send the value of the MCP argument `scrapeOption` directly as the JSON body; do not wrap it in a `scrapeOption` property.

## Brand (1)

### `brand_retrieve`

- **HTTP:** `GET /brand/retrieve`
- **What:** Retrieve brand data by domain. Returns a brand profile for a domain (title, description, brand colors as hex, logos and icons ranked best-first, backdrops, socials, links, and any schema.org organization data). Enrichment-only fields that are not present in the page markup are returned as null.
- **Params:** `domain` (string, **required**) — Domain to retrieve brand data for, e.g. context.dev; `force_language` (string, optional) — Accepted for compatibility; not applied in HTML-only mode; `maxAgeMs` (integer, optional) — Cache freshness window in milliseconds, clamps to 1 day..1 year; `maxSpeed` (boolean, optional) — Optimize for speed by skipping schema.org and footer-link extraction; `timeoutMS` (integer, optional) — Upstream fetch timeout in milliseconds, clamps to 1000..300000
