---
name: google-shopping-api
version: 1.0.4
description: Google Shopping data toolkit via ScraperSocial — product search across merchants with pricing as clean JSON.
license: MIT-0
author: ScraperSocial
homepage: https://scrapersocial.com
repository: https://github.com/nikhonit/social-media-api-skills
tags:
  - google-shopping
  - ecommerce
  - price-data
  - social-media
  - api
  - mcp
allowed-tools: Bash(node:*)
metadata:
  openclaw:
    primaryEnv: SCRAPERSOCIAL_KEY
    homepage: https://scrapersocial.com
    requires:
      env:
        - SCRAPERSOCIAL_KEY
    network:
      allow:
        - api.scrapersocial.com
    shell:
      only: scripts/*.js
---

# Google Shopping API skill

Read public Google Shopping results as clean JSON. This Google Shopping API skill is a single endpoint: search products by keyword and get back listings with merchants and prices, at 3 credits per product — useful for price comparison, market research and competitive monitoring.

This skill wraps **1 live Google Shopping endpoint** from the [ScraperSocial](https://scrapersocial.com) API. Public data only, returned as clean JSON.

## When to use this skill

- You are comparing prices for a product across merchants.
- You need to see how a product is listed and priced in the shopping index.
- A user asks where to buy something and at what price.

### Do not use this skill when

- **You need a single merchant's catalogue.** Go to that merchant — `amazon-api` and `tiktok-shop-api` cover theirs.
- **You need guaranteed live prices.** Results may be cached and merchant prices move; pass `--fresh` when accuracy matters more than speed.
- **You need Merchant Center data for your own store.** That is account-scoped; use Google's own API.

## Setup

```bash
export SCRAPERSOCIAL_KEY=sk_live_...   # https://scrapersocial.com/app/keys
```

Signing up at [scrapersocial.com/signup](https://scrapersocial.com/signup) includes 100 free credits, no card required.

## Permissions and scope

These scripts do exactly three things and nothing else: read one environment variable (`SCRAPERSOCIAL_KEY`), send HTTPS requests to `https://api.scrapersocial.com` (the host is a constant in the code, not configurable), and print JSON. They run as `node scripts/<name>.js` with no other shell use, no file writes and no persistence. `call_endpoint.js` accepts only the 1 documented `/v1/google_shopping/` paths in the table below and refuses anything else before a request is made.

## Scripts

| Script | What it does | Input | Credits |
|---|---|---|---|
| `product_search.js` | List Google Shopping product search. | query | 3 credits per product |
| `call_endpoint.js` | Call any `/v1/google_shopping/` endpoint directly | path + params | varies |

Every script also accepts `--limit`, `--cursor`, `--fields`, `--format` and `--fresh`. `--limit` is clamped to 50: above that the API returns an async job instead of data.

## Example

```bash
node skills/google-shopping-api/scripts/product_search.js "mechanical keyboard"
```

Every response uses the same envelope:

```json
{ "data": {}, "meta": { "count": 20, "next_cursor": "..." }, "request_id": "a18e4ef88ad4b00b" }
```

`meta` appears on paginated endpoints only. Keep `request_id` — support traces calls with it.

## Endpoints

| Endpoint | Input | Returns | Credits | Paginated |
|---|---|---|---|---|
| `/v1/google_shopping/product-search` | query | product | 3 credits per product | yes |

Costs shown per item for paginated endpoints, per call otherwise. Failed calls are not charged.

## FAQ

### How do I search Google Shopping as JSON?

`product_search.js` with a query, 3 credits per product returned. Use `--limit` to bound the cost.

### Are the prices live?

They reflect what the shopping index published when the page was read, and may be cached. Use `--fresh` to bypass the cache at the same credit cost.

### Is this an official Google API?

No. ScraperSocial is independent and not affiliated with Google. It returns publicly available data only.

## Links

- [Google Shopping data on ScraperSocial](https://scrapersocial.com)
- [All 33 platform skills](https://github.com/nikhonit/social-media-api-skills)
- [OpenAPI spec](https://scrapersocial.com/openapi.json) · [llms.txt](https://scrapersocial.com/llms.txt)

## Disclaimer

ScraperSocial is an independent product and is not affiliated with, endorsed by, or sponsored by any platform named in this repository. All product names, logos and brands are property of their respective owners. These skills return only publicly available data.
