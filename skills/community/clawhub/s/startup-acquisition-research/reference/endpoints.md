# startup-acquisition-research — endpoint reference

> Generated from `scripts/tools.json` by `scripts/generate.mjs` — do not edit by hand.

Only the endpoints used by this workflow. Call them via `scripts/crawlora.sh` (see SKILL.md).

All paths are relative to the API base `https://api.crawlora.net/api/v1` and require the header `x-api-key: $CRAWLORA_API_KEY`. Path params like `{id}` are substituted into the URL; `GET` params go in the query string; `POST` params go in a JSON body.

**13 endpoints across 4 platform group(s).**

## Datasets (4)

### `datasets_trustmrr_facets`

- **HTTP:** `GET /datasets/trustmrr/facets`
- **What:** Facet the TrustMRR dataset. Returns terms-aggregation counts for one facet of the TrustMRR dataset, scoped to the same filters as search. Facet enum: `category`, `country`, `payment_provider`, `target_audience`, `business_type`, `tech`, `channels`, `listing_tier`, `status`, `on_sale`, `is_sponsored`, `tags`.
- **Params:** `category` (string, optional) — Exact category filter, max 128 characters; `country` (string, optional) — Exact ISO country-code filter, max 128 characters; `facet` (string, **required**) — Facet enum: category, country, payment_provider, target_audience, business_type, tech, channels, listing_tier, status, on_sale, is_sponsored, tags; `min_mrr` (number, optional) — Minimum verified MRR in USD; `on_sale` (boolean, optional) — Filter for startups currently listed for sale; `payment_provider` (string, optional) — Payment-provider filter, max 128 characters; `q` (string, optional) — Full-text query, max 256 characters

### `datasets_trustmrr_history`

- **HTTP:** `GET /datasets/trustmrr/history/{slug}`
- **What:** Get a TrustMRR startup's daily history. Returns a startup's daily time-series of payment-provider-verified metrics — MRR, all-time revenue, last-30-days revenue, 30-day and 12-month traffic, 30-day growth, for-sale flag, asking price, valuation multiple, deal score and offer count — one point per day in chronological order (oldest first). The series accrues one point per calendar day, so a recently discovered startup returns a short or empty series rather than a 404.
- **Params:** `from` (string, optional) — Inclusive start date, YYYY-MM-DD (UTC); `limit` (integer, optional) — Maximum points returned (the most recent within the range), default 365, max 1000; `slug` (string, **required**) — Startup slug, max 128 characters; `to` (string, optional) — Inclusive end date, YYYY-MM-DD (UTC)

### `datasets_trustmrr_item`

- **HTTP:** `GET /datasets/trustmrr/items/{slug}`
- **What:** Get a TrustMRR startup from the dataset. Returns one startup record by slug from the TrustMRR dataset (dataset id `trustmrr`), including verified revenue/MRR, traffic, growth, category, tech stack, marketing channels and acquisition-marketplace fields.
- **Params:** `slug` (string, **required**) — Startup slug, max 128 characters

### `datasets_trustmrr_search`

- **HTTP:** `GET /datasets/trustmrr/search`
- **What:** Search the TrustMRR dataset. Searches public startups with payment-provider-verified revenue and MRR, stored in a search index. Filter by category, country, payment provider, target audience, tech, marketing channel, listing tier and for-sale status, and by revenue/MRR/traffic/growth/multiple/asking-price ranges. Sort enum: `relevance`, `mrr_desc`, `revenue_desc`, `revenue_30d_desc`, `traffic_desc`, `growth_desc`, `deal_score_desc`, `price_asc`, `price_desc`, `multiple_asc`, `founded_desc`. status enum: `active`, `removed`. Billing: this search costs 1 credit per record returned, with a minimum of 2 (an empty result costs 2, a full page of 100 costs 100).
- **Params:** `business_type` (string, optional) — Business-type filter (e.g. B2B, B2C), max 128 characters; `category` (string, optional) — Exact category filter (e.g. SaaS, Artificial Intelligence, Mobile Apps), max 128 characters; `channel` (string, optional) — Detected marketing-channel slug filter (e.g. meta-ads, seo), max 128 characters; `country` (string, optional) — Exact ISO country-code filter (e.g. US), max 128 characters; `is_sponsored` (boolean, optional) — Filter for sponsored (paid-placement) listings; `listing_tier` (string, optional) — For-sale listing-tier filter (e.g. pro), max 128 characters; `max_asking_price` (number, optional) — Maximum asking price in USD; `max_mrr` (number, optional) — Maximum verified MRR in USD; `max_multiple` (number, optional) — Maximum asking-price-to-revenue multiple; `min_ahrefs_dr` (integer, optional) — Minimum Ahrefs Domain Rating; `min_asking_price` (number, optional) — Minimum asking price in USD; `min_growth` (number, optional) — Minimum 30-day revenue growth percentage; `min_mrr` (number, optional) — Minimum verified MRR in USD; `min_revenue` (number, optional) — Minimum verified all-time revenue in USD; `min_revenue_30d` (number, optional) — Minimum verified last-30-days revenue in USD; `min_traffic` (number, optional) — Minimum last-30-days traffic (visits); `on_sale` (boolean, optional) — Filter for startups currently listed for sale; `page` (integer, optional) — Page number, defaults to 1; `page_size` (integer, optional) — Page size, defaults to 20 and maxes at 100; page * page_size must be <= 10000; `payment_provider` (string, optional) — Payment-provider filter (e.g. stripe, revenuecat, superwall, creem), max 128 characters; `q` (string, optional) — Full-text query over name, description, seller message and business summary, max 256 characters; `slug` (string, optional) — Exact startup slug filter, max 128 characters; `sort` (string, optional) — Sort enum: relevance, mrr_desc, revenue_desc, revenue_30d_desc, traffic_desc, growth_desc, deal_score_desc, price_asc, price_desc, multiple_asc, founded_desc; `status` (string, optional) — Lifecycle enum: active, removed; `target_audience` (string, optional) — Target-audience filter (e.g. B2B, B2C), max 128 characters; `tech` (string, optional) — Detected tech-stack slug filter (e.g. nextjs, reactnative), max 128 characters

## TrustMRR (7)

### `trustmrr_acquire`

- **HTTP:** `GET /trustmrr/acquire`
- **What:** Get TrustMRR acquisition listings. Returns the for-sale startups rendered on the public TrustMRR /acquire marketplace page, with deal metrics (asking price, revenue, multiple, growth). Verified revenue figures come from supported payment providers.
- **Params:** _none_

### `trustmrr_categories`

- **HTTP:** `GET /trustmrr/categories`
- **What:** Get TrustMRR categories. Lists the TrustMRR startup categories, with the total `count`. Each category has its `slug`, `label`, short label, icon name, description, keywords and TrustMRR URL. Pass a category `slug` to `/trustmrr/category/{slug}` to list the startups in it.
- **Params:** _none_

### `trustmrr_category`

- **HTTP:** `GET /trustmrr/category/{slug}`
- **What:** Get TrustMRR category detail. Returns one TrustMRR category by `slug` (lowercase letters, digits and hyphens, for example `saas`) with the startups listed in it. Each startup has its name, slug, URL, description, current MRR, total revenue and last-30-days revenue, all in USD, plus the `on_sale` flag for startups listed for sale. Valid slugs come from `/trustmrr/categories`.
- **Params:** `slug` (string, **required**) — TrustMRR category slug

### `trustmrr_leaderboard`

- **HTTP:** `GET /trustmrr/leaderboard`
- **What:** Get TrustMRR revenue leaderboard. Returns the top 100 startups ranked by the selected metric from the public TrustMRR leaderboard. Revenue and MRR figures are verified through supported payment providers.
- **Params:** `metric` (string, optional) — Leaderboard metric to rank by (default mrr)

### `trustmrr_marketplace`

- **HTTP:** `GET /trustmrr/marketplace`
- **What:** Get TrustMRR marketplace snapshot. Returns the public TrustMRR marketplace snapshot: the 25 most recently listed startups for sale and the current 25 best deals ranked by TrustMRR's recency-aware deal score. Revenue figures are verified through supported payment providers.
- **Params:** _none_

### `trustmrr_startup`

- **HTTP:** `GET /trustmrr/startup/{slug}`
- **What:** Get TrustMRR startup detail. Returns the full verified profile for a single TrustMRR startup by slug: revenue and MRR, growth, asking price and marketplace status, tech stack, marketing channels, and TrustMRR's AI-generated business summary.
- **Params:** `slug` (string, **required**) — TrustMRR startup slug

### `trustmrr_startups`

- **HTTP:** `GET /trustmrr/startups`
- **What:** List all TrustMRR startups. Returns a paginated list of every startup in the TrustMRR directory. Each entry is a slug you can pass to /trustmrr/startup/{slug} for the full verified profile — together these two endpoints let you enumerate the entire directory.
- **Params:** `page` (integer, optional) — 1-based page number (default 1); `page_size` (integer, optional) — Items per page (default 100, max 1000)

## Web (1)

### `web_scrape`

- **HTTP:** `POST /web/scrape`
- **What:** Scrape a URL into markdown, HTML, links or metadata. Fetches a single public URL and returns clean content in the requested formats (markdown, html, raw_html, links, metadata). The request body IS the ScrapeOption object itself — e.g. {"url": "https://example.com"} — do not wrap it in an extra key. With render=auto the request starts as a fast HTTP fetch and escalates to a real browser when the page is blocked or rendered with JavaScript. only_main_content (default true) strips navigation, headers, footers and other boilerplate before conversion. Only public pages are supported; respect each site's terms of use and robots directives. A handful of popular sites (Amazon, Reddit, Yelp, LinkedIn, and others) already have a dedicated, more reliable endpoint elsewhere in this API — a failed scrape against one of them names it. A Reddit URL that maps onto a dedicated Reddit endpoint (listings, search, comment threads, user and domain pages) is answered by that endpoint instead, and its response is returned as-is in data with an X-Routed-To header; send dedicated=false to always get the scraped page.
- **Params:** `scrapeOption` (object, **required**) — Scrape options
- **REST body:** Send the value of the MCP argument `scrapeOption` directly as the JSON body; do not wrap it in a `scrapeOption` property.

## Bing (1)

### `bing_search`

- **HTTP:** `GET /bing/search`
- **What:** Search Bing web results. Returns Bing web search results for a query string, including organic results, optional context panel data, related queries, people-also-ask questions, news modules, video modules, and page-based pagination. Empty optional blocks are omitted from the JSON response. Locale defaults to country=us and lang=en-us. Returns 503 on a genuine transport failure or challenge page. Bing occasionally serves a well-formed page whose results share no significant term with the query; when every attempt hits this, the response is still returned as 200 with data.low_confidence set to true (and the X-Low-Confidence header) instead of being withheld, so callers get Bing's real answer plus an honest signal to double-check it rather than nothing. Queries that use the site: operator (for example site:gov.hu) are not supported: Bing serves a bot-verification challenge for them, so they are rejected with 400 before any request is made. Use the DuckDuckGo (/api/v1/duckduckgo/search), Brave (/api/v1/brave/search), or Yahoo (/api/v1/yahoo-search/search) search endpoints for domain-restricted searches instead.
- **Params:** `count` (integer, optional) — Results per page; defaults to 10, clamped to 1..50; `country` (string, optional) — Two-letter country code; defaults to us; `lang` (string, optional) — Bing UI language; defaults to en-us; `page` (integer, optional) — 1-based page number; defaults to 1; `q` (string, **required**) — Search query
