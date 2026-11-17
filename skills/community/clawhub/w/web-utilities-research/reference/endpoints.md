# web-utilities-research — endpoint reference

> Generated from `scripts/tools.json` by `scripts/generate.mjs` — do not edit by hand.

Endpoints this skill uses, grouped by platform. Call them via `scripts/crawlora.sh` (see SKILL.md).

All paths are relative to the API base `https://api.crawlora.net/api/v1` and require the header `x-api-key: $CRAWLORA_API_KEY`. Path params like `{id}` are substituted into the URL; `GET` params go in the query string; `POST` params go in a JSON body.

**19 endpoints across 6 platform group(s).**

## Numbeo (8)

### `numbeo_cost_of_living_city`

- **HTTP:** `GET /numbeo/cost-of-living/city/{slug}`
- **What:** Get a Numbeo city's cost-of-living prices. Returns itemized cost-of-living prices for one city (restaurants, markets, transportation, utilities, rent, and more), grouped by category.
- **Params:** `slug` (string, **required**) — Numbeo city slug

### `numbeo_cost_of_living_country`

- **HTTP:** `GET /numbeo/cost-of-living/country`
- **What:** Get a Numbeo country's cost-of-living prices. Returns aggregate itemized cost-of-living prices for a country, plus the headline cost-of-living indices for every city Numbeo tracks there.
- **Params:** `country` (string, **required**) — Country name as Numbeo spells it

### `numbeo_cost_of_living_rankings`

- **HTTP:** `GET /numbeo/cost-of-living/rankings`
- **What:** Get the global Numbeo cost-of-living city ranking. Returns the global cost-of-living city ranking (Cost of Living, Rent, Cost of Living Plus Rent, Groceries, Restaurant Price, and Local Purchasing Power indices), either the continuously-updated current index or a historical periodic snapshot.
- **Params:** `period` (string, optional) — Required when scope=historical, e.g. 2026-mid or 2025; `scope` (string, optional) — current (default) or historical

### `numbeo_cost_of_living_rankings_by_country`

- **HTTP:** `GET /numbeo/cost-of-living/rankings-by-country`
- **What:** Get the global Numbeo cost-of-living country ranking. Returns the global country-level cost-of-living ranking (Cost of Living, Rent, Cost of Living Plus Rent, Groceries, Restaurant Price, and Local Purchasing Power indices).
- **Params:** _none_

### `numbeo_indices_city`

- **HTTP:** `GET /numbeo/indices/city/{slug}`
- **What:** Get a Numbeo city's data for an index family. Returns one city's data for a Numbeo index family (quality of life, crime, health care, pollution, traffic, or property investment): headline indices, and (depending on the family) titled sub-index sections and/or itemized prices.
- **Params:** `index` (string, **required**) — Index family; `slug` (string, **required**) — Numbeo city slug

### `numbeo_indices_country`

- **HTTP:** `GET /numbeo/indices/country`
- **What:** Get a Numbeo country's data for an index family. Returns one country's aggregate data for a Numbeo index family, plus every city Numbeo tracks there with its index breakdown.
- **Params:** `country` (string, **required**) — Country name as Numbeo spells it; `index` (string, **required**) — Index family

### `numbeo_indices_rankings`

- **HTTP:** `GET /numbeo/indices/rankings`
- **What:** Get the global Numbeo city ranking for an index family. Returns the global city ranking for a Numbeo index family, either the continuously-updated current index or a historical periodic snapshot.
- **Params:** `index` (string, **required**) — Index family; `period` (string, optional) — Required when scope=historical, e.g. 2026-mid or 2025; `scope` (string, optional) — current (default) or historical

### `numbeo_indices_rankings_by_country`

- **HTTP:** `GET /numbeo/indices/rankings-by-country`
- **What:** Get the global Numbeo country ranking for an index family. Returns the global Numbeo ranking of countries for one index family, selected by the required `index`: `quality-of-life`, `crime`, `health-care`, `pollution`, `traffic` or `property-investment`. Each row has its `rank`, country and a list of named index values, such as the Crime Index and Safety Index for `crime`.
- **Params:** `index` (string, **required**) — Index family

## Geocoding (3)

### `geocoding_lookup`

- **HTTP:** `GET /geocoding/lookup`
- **What:** Lookup Nominatim OSM ids. Looks up OpenStreetMap objects by the required `osm_ids`, a comma-separated list prefixed `N` (node), `W` (way) or `R` (relation), such as `W34633854,N123`. Each place has its display name, category and type, coordinates, bounding box, importance and address parts; `addressdetails` defaults to true, and `extratags`, `namedetails` and `accept_language` are optional. Malformed ids return `400`; no match returns `404`.
- **Params:** `accept_language` (string, optional) — Preferred result language, forwarded to Nominatim; `addressdetails` (boolean, optional) — Include address details, defaults to true; `extratags` (boolean, optional) — Include OSM extra tags; `namedetails` (boolean, optional) — Include multilingual name details; `osm_ids` (string, **required**) — Comma-separated OSM ids such as W34633854,N123,R456

### `geocoding_reverse`

- **HTTP:** `GET /geocoding/reverse`
- **What:** Reverse geocode coordinates. Returns the nearest OpenStreetMap place for the required `lat` and `lon`. `zoom` (0 to 18, default 18) sets the level of detail; `addressdetails` defaults to true, and `extratags`, `namedetails` and `accept_language` are optional. The place has its display name, category and type, OSM type and id, bounding box, importance and address parts. Out-of-range coordinates return `400`; no place found returns `404`.
- **Params:** `accept_language` (string, optional) — Preferred result language, forwarded to Nominatim; `addressdetails` (boolean, optional) — Include address details, defaults to true; `extratags` (boolean, optional) — Include OSM extra tags; `lat` (number, **required**) — Latitude; `lon` (number, **required**) — Longitude; `namedetails` (boolean, optional) — Include multilingual name details; `zoom` (integer, optional) — Nominatim address zoom, defaults to 18

### `geocoding_search`

- **HTTP:** `GET /geocoding/search`
- **What:** Search Nominatim places. Searches OpenStreetMap places by address. Pass either free-text `q` or structured fields (`street`, `city`, `county`, `state`, `country`, `postalcode`), not both. `limit` defaults to 10 and is clamped to 20; `countrycodes` restricts by ISO 3166-1 alpha-2 country. Each result has its display name, coordinates, category, type, bounding box, importance and address parts. No match returns `404`.
- **Params:** `accept_language` (string, optional) — Preferred result language, forwarded to Nominatim; `addressdetails` (boolean, optional) — Include address details, defaults to true; `city` (string, optional) — Structured city; `country` (string, optional) — Structured country; `countrycodes` (string, optional) — Comma-separated ISO 3166-1 alpha-2 country filters; `county` (string, optional) — Structured county; `extratags` (boolean, optional) — Include OSM extra tags; `limit` (integer, optional) — Maximum results, defaults to 10 and clamps to 20; `namedetails` (boolean, optional) — Include multilingual name details; `postalcode` (string, optional) — Structured postal code; `q` (string, optional) — Free-text search query; `state` (string, optional) — Structured state; `street` (string, optional) — Structured street or house number

## Web (3)

### `extract`

- **HTTP:** `POST /extract`
- **What:** Extract schema-conforming JSON from a URL. Reads a public URL as clean Markdown, then returns data that strictly conforms to the supplied bounded JSON Schema. The response includes `truncated`, which is true when the page was too long and only its first part was used.
- **Params:** `extractOption` (object, **required**) — Extraction options
- **REST body:** Send the value of the MCP argument `extractOption` directly as the JSON body; do not wrap it in a `extractOption` property.

### `web_scrape`

- **HTTP:** `POST /web/scrape`
- **What:** Scrape a URL into markdown, HTML, links or metadata. Fetches a single public URL and returns clean content in the requested formats (markdown, html, raw_html, links, metadata). The request body IS the ScrapeOption object itself — e.g. {"url": "https://example.com"} — do not wrap it in an extra key. With render=auto the request starts as a fast HTTP fetch and escalates to a real browser when the page is blocked or rendered with JavaScript. only_main_content (default true) strips navigation, headers, footers and other boilerplate before conversion. Only public pages are supported; respect each site's terms of use and robots directives. A handful of popular sites (Amazon, Reddit, Yelp, LinkedIn, and others) already have a dedicated, more reliable endpoint elsewhere in this API — a failed scrape against one of them names it. A Reddit URL that maps onto a dedicated Reddit endpoint (listings, search, comment threads, user and domain pages) is answered by that endpoint instead, and its response is returned as-is in data with an X-Routed-To header; send dedicated=false to always get the scraped page.
- **Params:** `scrapeOption` (object, **required**) — Scrape options
- **REST body:** Send the value of the MCP argument `scrapeOption` directly as the JSON body; do not wrap it in a `scrapeOption` property.

### `web_techstack`

- **HTTP:** `POST /web/techstack`
- **What:** Tech stack — detect what a website is built with. Fetches a public URL and fingerprints the web technologies it is built with — a BuiltWith / Wappalyzer-style detector. Returns a list of detected `technologies`, each with its `categories`, a `confidence` (`high`, `medium`, `low`), an optional `version`, and the `evidence` that matched. Covers JavaScript frameworks and libraries (React, Vue.js, Angular, Svelte, jQuery), web frameworks / static site generators (Next.js, Nuxt.js, Gatsby, Remix, SvelteKit, Astro, Hugo), CMS and website builders (WordPress, Drupal, Joomla, Ghost, Wix, Squarespace, Webflow), e-commerce (Shopify, WooCommerce, Magento, BigCommerce), analytics, ad pixels, and tag managers (Google Analytics, Google Tag Manager, Meta Pixel, LinkedIn, Bing, TikTok/Pinterest/Reddit pixels, Segment, Hotjar, Microsoft Clarity), CDNs, UI frameworks and fonts, payments (Stripe, PayPal, Klarna), live chat, marketing automation, A/B testing, consent management, CAPTCHAs (reCAPTCHA, hCaptcha, Turnstile), video, and search. It also inspects response headers to identify the web server (nginx, Apache, IIS), the CDN / hosting provider (Cloudflare, CloudFront, Fastly, Vercel, Netlify), and the server-side language / framework (PHP, ASP.NET, Ruby on Rails, Django, Laravel, Express). Results are directional, not exhaustive. The `render` fetch strategy is one of `browser` (headless browser that executes JavaScript — the default, so client-injected scripts like analytics, tag managers and pixels are detected), `auto` (HTTP, escalating to a real browser only when blocked or JS-rendered), or `http` (HTTP only, no JavaScript — fastest, but sees only the server HTML); defaults to `browser`. Only public pages are supported; respect each site's terms of use and robots directives. Also returns `unmatched_evidence` (when present) — third-party script/stylesheet host domains and a `<meta generator>` value the detector saw on the page but doesn't yet have a named signature for; useful for spotting a vendor worth requesting coverage for. `is_infrastructure` flags a URL whose host looks like backend CDN/DNS/cloud-vendor infrastructure rather than a real, human-navigable website. `reachable` is false only when the target could not be fetched at all (even after an automatic www./plain-HTTP retry) — `technologies` may still be partially populated from DNS-based signals alone in that case, and `failure_reason` explains what happened.
- **Params:** `request` (object, **required**) — Target URL (and optional render strategy)
- **REST body:** Send the value of the MCP argument `request` directly as the JSON body; do not wrap it in a `request` property.

## ImportYeti (2)

### `importyeti_company`

- **HTTP:** `GET /importyeti/company`
- **What:** Get an ImportYeti company report. Returns an ImportYeti company report: identity, headline US customs shipment-volume metrics (total shipments, average TEU, last shipment date, estimated shipping spend), its supplier list, and recent bill-of-lading shipment activity.
- **Params:** `slug` (string, **required**) — ImportYeti company slug, the last path segment of a /company/{slug} URL

### `importyeti_search`

- **HTTP:** `GET /importyeti/search`
- **What:** Search ImportYeti companies and suppliers by name. Searches ImportYeti for companies and suppliers matching a name, returning each match's kind (company or supplier), slug, country, address, and headline shipment stats. A "company" result's slug chains into GET /importyeti/company.
- **Params:** `page` (integer, optional) — 1-indexed result page, defaults to 1; `q` (string, **required**) — Company or supplier name to search for

## SimilarWeb (2)

### `similarweb_search`

- **HTTP:** `GET /similarweb/search`
- **What:** Search SimilarWeb Info. Looks up a domain or keyword on SimilarWeb and returns the matching websites, companies (name, domain and logo) and apps on the App Store and Google Play.
- **Params:** `q` (string, **required**) — Domain or keyword to search

### `similarweb_web`

- **HTTP:** `GET /similarweb/web/{domain}`
- **What:** Get SimilarWeb Web Info. Returns SimilarWeb's traffic profile for one domain: global, country and category rank, estimated monthly visits, engagement (bounce rate, pages per visit, time on site), top countries, traffic sources, top keywords and similar sites. `DataSource` shows whether the full source or the narrower public-page fallback answered; the fallback omits several fields.
- **Params:** `domain` (string, **required**) — Domain to fetch SimilarWeb data for

## Brand (1)

### `brand_retrieve`

- **HTTP:** `GET /brand/retrieve`
- **What:** Retrieve brand data by domain. Returns a brand profile for a domain (title, description, brand colors as hex, logos and icons ranked best-first, backdrops, socials, links, and any schema.org organization data). Enrichment-only fields that are not present in the page markup are returned as null.
- **Params:** `domain` (string, **required**) — Domain to retrieve brand data for, e.g. context.dev; `force_language` (string, optional) — Accepted for compatibility; not applied in HTML-only mode; `maxAgeMs` (integer, optional) — Cache freshness window in milliseconds, clamps to 1 day..1 year; `maxSpeed` (boolean, optional) — Optimize for speed by skipping schema.org and footer-link extraction; `timeoutMS` (integer, optional) — Upstream fetch timeout in milliseconds, clamps to 1000..300000
