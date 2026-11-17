---
name: web-utilities-research
description: General-purpose web-intelligence utilities via the Crawlora API — scrape any URL to clean markdown/HTML, extract schema-conforming JSON from a page, fingerprint a site's tech stack, geocode addresses, compare cost of living between cities/countries (Numbeo), look up a company's import/export trade records (ImportYeti), check a domain's traffic (SimilarWeb), or resolve a brand's identity from its domain. Use for one-off utility lookups that don't fit a specific platform skill.
---

# Web intelligence utilities

A grab-bag of general-purpose lookups that don't belong to one platform:
raw URL scraping/extraction, tech-stack fingerprinting, geocoding, cost-of-
living comparisons, import/export trade records, site traffic, and brand
resolution — all as normalized JSON from the Crawlora API.

## When to use this skill

- "Scrape this URL and give me clean markdown/HTML."
- "Pull structured data (a schema) out of this page."
- "What is this website built with?" (tech-stack fingerprint)
- "What's the address/coordinates for X?" (geocoding, forward or reverse)
- "How much more expensive is living in <city A> vs <city B>?" (Numbeo)
- "What does this company import, and from whom?" (ImportYeti — US customs records)
- "How much traffic does this site get?" (SimilarWeb)
- "Resolve this domain to a brand name/logo."

## Setup (one-time)

- Get a free Crawlora API key (2,000 credits/mo, no card) at [https://crawlora.net](https://crawlora.net?utm_source=github&utm_medium=referral&utm_campaign=crawlora-skills).
- Set `CRAWLORA_API_KEY` in the environment before running the helper.
- The helper reads `CRAWLORA_API_KEY` from the environment and sends requests to `https://api.crawlora.net/api/v1`. Missing/invalid key → `401`.

## How it works

1. **Scrape / extract / tech-stack (`POST`)** — `POST /web/scrape` returns a
   URL as markdown/HTML/links/metadata (`{"url": "...", "formats": ["markdown"]}`);
   `POST /extract` returns JSON conforming to a schema you supply
   (`{"url": "...", "schema": {...}}`); `POST /web/techstack` fingerprints
   the technologies a site runs (`{"url": "..."}`). **All three take flat
   top-level fields** — despite the tool catalog naming the body
   `scrapeOption`/`extractOption`/`request`, that name is not a JSON
   wrapper key; pass the fields directly at the top level of the body.
2. **Geocoding** — `/geocoding/search` (`q` or structured `street`/`city`/
   `country`) for forward geocoding; `/geocoding/reverse` (`lat`+`lon`)
   for reverse; `/geocoding/lookup` (`osm_ids`) for a known OpenStreetMap id.
3. **Numbeo (cost of living)** — `/numbeo/cost-of-living/city/{slug}` or
   `/country` for one place's full price breakdown;
   `/numbeo/cost-of-living/rankings` for a ranked list;
   `/numbeo/indices/*` for quality-of-life-style indices (pass an `index` name).
4. **ImportYeti** — `/importyeti/search` (`q`) to find a company, then
   `/importyeti/company` (`slug`) for its US customs import/export record summary.
5. **SimilarWeb** — `/similarweb/web/{domain}` for a site's traffic
   overview; `/similarweb/search` (`q`) to resolve a name to a domain.
6. **Brand** — `/brand/retrieve` (`domain`) resolves a domain to brand
   metadata (name, logo, colors).

Full endpoint list, methods, and params: [`reference/endpoints.md`](reference/endpoints.md).

## Calling the API

```sh
# Scrape a URL to markdown (POST, flat body):
scripts/crawlora.sh -X POST /web/scrape '{"url":"https://example.com","formats":["markdown"]}' | jq '.'

# Tech-stack fingerprint:
scripts/crawlora.sh -X POST /web/techstack '{"url":"https://example.com"}' | jq '.'

# Geocoding:
scripts/crawlora.sh /geocoding/search q="1600 Amphitheatre Parkway, Mountain View, CA" | jq '.'

# Cost of living:
scripts/crawlora.sh /numbeo/cost-of-living/city/Lisbon | jq '.'

# Site traffic + brand:
scripts/crawlora.sh /similarweb/web/example.com | jq '.'
scripts/crawlora.sh /brand/retrieve domain=example.com | jq '.'
```

Use `scripts/crawlora.sh` for all requests; it keeps the API key out of command-line arguments.


## Endpoint reference

See [`reference/endpoints.md`](reference/endpoints.md) for the Web,
Geocoding, Numbeo, ImportYeti, SimilarWeb, and Brand endpoints this skill uses.

## Examples

- **Site research bundle:** `/web/scrape` (content) + `/web/techstack`
  (what it's built with) + `/similarweb/web/{domain}` (traffic) for a
  competitor's website in one pass.
- **Relocation cost check:** `/numbeo/cost-of-living/city/{slug}` for two
  cities, diff rent/groceries/transport line items.
- **Supplier research:** `/importyeti/search` for a brand, then
  `/importyeti/company` for their shipment history and known suppliers.

## Notes & limits

- **Credits / pay-on-success:** billed only on `2xx`; free tier 2,000 credits/mo.
  Key at [https://crawlora.net](https://crawlora.net?utm_source=github&utm_medium=referral&utm_campaign=crawlora-skills).
- **Public data only** — only public, robots-permitting pages are scraped;
  respect each site's terms of use.
- **Security:** key lives in `CRAWLORA_API_KEY` only — never hardcode, query-param, or commit it.
- **`/web/scrape`, `/extract`, and `/web/techstack` take flat top-level
  fields**, live-verified (`url`, `formats` for scrape; `url`, `schema` for
  extract; `url` for techstack) — the tool catalog's `scrapeOption`/
  `extractOption`/`request` names describe the body's *purpose*, not a
  wrapper key to nest under. Less-common fields (`render`, `only_main_content`,
  a full JSON Schema for `/extract`) aren't listed in the tool schema either —
  confirm those at [crawlora.net/docs](https://crawlora.net/docs?utm_source=github&utm_medium=referral&utm_campaign=crawlora-skills)
  or the [playground](https://crawlora.net/playground?utm_source=github&utm_medium=referral&utm_campaign=crawlora-skills) before relying on them.
- ImportYeti and SimilarWeb data reflect each provider's own refresh cadence, not real-time.
