---
name: tiktok-shop-api
version: 1.0.4
description: TikTok Shop data toolkit via ScraperSocial — product detail, product reviews, shop catalogues, creator showcases and product search.
license: MIT-0
author: ScraperSocial
homepage: https://scrapersocial.com
repository: https://github.com/nikhonit/social-media-api-skills
tags:
  - tiktok-shop
  - ecommerce
  - product-reviews
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

# TikTok Shop API skill

Read public TikTok Shop data as clean JSON. This TikTok Shop API skill returns a product, its reviews, a shop's catalogue, a creator's showcase, and keyword product search — all at 3 credits. TikTok Shop is where a large share of social commerce now happens, and it is barely covered by conventional e-commerce data tools.

This skill wraps **5 live TikTok Shop endpoints** from the [ScraperSocial](https://scrapersocial.com) API. Public data only, returned as clean JSON.

## When to use this skill

- You are researching what sells on TikTok Shop in a category.
- You need reviews for a TikTok Shop product to gauge sentiment or quality.
- You are tracking which products a creator promotes in their showcase.
- You are comparing a product's TikTok Shop listing against other marketplaces.

### Do not use this skill when

- **You need seller-account data** — orders, fulfilment, payouts. That is account-scoped; TikTok's Shop Partner API covers it.
- **You confused this with the main TikTok skill.** Videos, transcripts and creator stats live in `tiktok-api`; this skill is the commerce surface only.
- **You need guaranteed live stock or price.** Responses may be cached; use `--fresh` when it matters.

## Setup

```bash
export SCRAPERSOCIAL_KEY=sk_live_...   # https://scrapersocial.com/app/keys
```

Signing up at [scrapersocial.com/signup](https://scrapersocial.com/signup) includes 100 free credits, no card required.

## Permissions and scope

These scripts do exactly three things and nothing else: read one environment variable (`SCRAPERSOCIAL_KEY`), send HTTPS requests to `https://api.scrapersocial.com` (the host is a constant in the code, not configurable), and print JSON. They run as `node scripts/<name>.js` with no other shell use, no file writes and no persistence. `call_endpoint.js` accepts only the 5 documented `/v1/tiktokshop/` paths in the table below and refuses anything else before a request is made.

## Scripts

| Script | What it does | Input | Credits |
|---|---|---|---|
| `get_product.js` | Get TikTok Shop product. | url | 3 credits |
| `get_product_reviews.js` | List TikTok Shop product reviews. | url | 3 credits per review |
| `get_products.js` | List TikTok Shop products. | url | 3 credits per product |
| `search.js` | List TikTok Shop search. | query | 3 credits per product |
| `get_user_showcase.js` | List TikTok Shop user showcase. | handle | 3 credits per product |
| `call_endpoint.js` | Call any `/v1/tiktokshop/` endpoint directly | path + params | varies |

Every script also accepts `--limit`, `--cursor`, `--fields`, `--format` and `--fresh`. `--limit` is clamped to 50: above that the API returns an async job instead of data.

## Example

```bash
node skills/tiktok-shop-api/scripts/search.js "phone case"
```

Every response uses the same envelope:

```json
{ "data": {}, "meta": { "count": 20, "next_cursor": "..." }, "request_id": "a18e4ef88ad4b00b" }
```

`meta` appears on paginated endpoints only. Keep `request_id` — support traces calls with it.

## Endpoints

| Endpoint | Input | Returns | Credits | Paginated |
|---|---|---|---|---|
| `/v1/tiktokshop/product` | url | product | 3 credits | no |
| `/v1/tiktokshop/product-reviews` | url | review | 3 credits per review | yes |
| `/v1/tiktokshop/products` | url | product | 3 credits per product | yes |
| `/v1/tiktokshop/search` | query | product | 3 credits per product | yes |
| `/v1/tiktokshop/user-showcase` | handle | product | 3 credits per product | yes |

Costs shown per item for paginated endpoints, per call otherwise. Failed calls are not charged.

## FAQ

### How do I search TikTok Shop products?

`search.js` with a query returns matching products at 3 credits each.

### How do I get reviews for a product?

`get_product_reviews.js` with the product URL, 3 credits per review returned.

### What is a creator showcase?

`get_user_showcase.js` returns the products a given creator features — useful for tracking affiliate promotion.

### Is this an official TikTok Shop API?

No. ScraperSocial is independent and not affiliated with TikTok or ByteDance. It returns publicly available listing data only.

## Links

- [TikTok Shop data on ScraperSocial](https://scrapersocial.com)
- [All 33 platform skills](https://github.com/nikhonit/social-media-api-skills)
- [OpenAPI spec](https://scrapersocial.com/openapi.json) · [llms.txt](https://scrapersocial.com/llms.txt)

## Disclaimer

ScraperSocial is an independent product and is not affiliated with, endorsed by, or sponsored by any platform named in this repository. All product names, logos and brands are property of their respective owners. These skills return only publicly available data.
