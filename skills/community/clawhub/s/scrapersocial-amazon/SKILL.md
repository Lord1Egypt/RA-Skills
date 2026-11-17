---
name: amazon-api
version: 1.0.4
description: Amazon data toolkit via ScraperSocial — product detail, product search, customer reviews and seller listings as clean JSON.
license: MIT-0
author: ScraperSocial
homepage: https://scrapersocial.com
repository: https://github.com/nikhonit/social-media-api-skills
tags:
  - amazon
  - ecommerce
  - reviews
  - product-data
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

# Amazon API skill

Read public Amazon listing data as clean JSON. This Amazon API skill fetches a product page by URL, searches the catalog by keyword, pulls customer reviews, and lists the sellers offering a given item — useful for price tracking, competitive research, and review-mining without maintaining a scraper against one of the most defended sites on the web.

This skill wraps **4 live Amazon endpoints** from the [ScraperSocial](https://scrapersocial.com) API. Public data only, returned as clean JSON.

## When to use this skill

- A user pastes an Amazon product URL and wants the title, price, rating or specifications.
- You are comparing how a product is priced or positioned across sellers.
- You need the review text for a product to summarise sentiment or pull out recurring complaints.
- You want to find products matching a keyword and rank them.

### Do not use this skill when

- **You need order, account or Seller Central data.** This reads public listing pages only. Use Amazon's own SP-API for anything tied to an account.
- **You need a live price guarantee.** Prices change constantly and responses may be served from cache. Pass `--fresh` when the exact current price matters.
- **You want a plain keyword search endpoint called `search`.** Amazon's search capability here is `product-search`; there is no `/v1/amazon/search`.
- **A product link appears in passing** with no question attached. Calls cost credits.

## Setup

```bash
export SCRAPERSOCIAL_KEY=sk_live_...   # https://scrapersocial.com/app/keys
```

Signing up at [scrapersocial.com/signup](https://scrapersocial.com/signup) includes 100 free credits, no card required.

## Permissions and scope

These scripts do exactly three things and nothing else: read one environment variable (`SCRAPERSOCIAL_KEY`), send HTTPS requests to `https://api.scrapersocial.com` (the host is a constant in the code, not configurable), and print JSON. They run as `node scripts/<name>.js` with no other shell use, no file writes and no persistence. `call_endpoint.js` accepts only the 4 documented `/v1/amazon/` paths in the table below and refuses anything else before a request is made.

## Scripts

| Script | What it does | Input | Credits |
|---|---|---|---|
| `get_product.js` | Get Amazon product. | url | 3 credits |
| `product_search.js` | List Amazon product search. | query | 3 credits per product |
| `get_reviews.js` | List Amazon reviews. | url | 3 credits per review |
| `get_sellers.js` | List Amazon sellers. | url | 3 credits per offer |
| `call_endpoint.js` | Call any `/v1/amazon/` endpoint directly | path + params | varies |

Every script also accepts `--limit`, `--cursor`, `--fields`, `--format` and `--fresh`. `--limit` is clamped to 50: above that the API returns an async job instead of data.

## Example

```bash
node skills/amazon-api/scripts/product_search.js "wireless earbuds"
```

Every response uses the same envelope:

```json
{ "data": {}, "meta": { "count": 20, "next_cursor": "..." }, "request_id": "a18e4ef88ad4b00b" }
```

`meta` appears on paginated endpoints only. Keep `request_id` — support traces calls with it.

## Endpoints

| Endpoint | Input | Returns | Credits | Paginated |
|---|---|---|---|---|
| `/v1/amazon/product` | url | product | 3 credits | no |
| `/v1/amazon/product-search` | query | product | 3 credits per product | yes |
| `/v1/amazon/reviews` | url | review | 3 credits per review | yes |
| `/v1/amazon/sellers` | url | offer | 3 credits per offer | yes |

Costs shown per item for paginated endpoints, per call otherwise. Failed calls are not charged.

## FAQ

### How do I get Amazon product data as JSON?

Run `get_product.js` with the product URL. It returns the listing as structured JSON for 3 credits. For keyword lookups use `product_search.js` instead.

### Can I get Amazon reviews through the API?

Yes. `get_reviews.js` takes a product URL and returns reviews, charged 3 credits per review returned. Cap the volume with `--limit`.

### Is this an official Amazon API?

No. ScraperSocial is independent and not affiliated with Amazon. It returns publicly available listing data only.

### Why is my price slightly stale?

Responses can come from cache, which is what makes them fast. Add `--fresh` to bypass the cache at the same credit cost.

## Links

- [Amazon data on ScraperSocial](https://scrapersocial.com)
- [All 33 platform skills](https://github.com/nikhonit/social-media-api-skills)
- [OpenAPI spec](https://scrapersocial.com/openapi.json) · [llms.txt](https://scrapersocial.com/llms.txt)

## Disclaimer

ScraperSocial is an independent product and is not affiliated with, endorsed by, or sponsored by any platform named in this repository. All product names, logos and brands are property of their respective owners. These skills return only publicly available data.
