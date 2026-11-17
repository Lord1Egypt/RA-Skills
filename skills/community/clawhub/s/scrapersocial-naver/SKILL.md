---
name: naver-api
version: 1.0.4
description: Naver data toolkit via ScraperSocial — blog, cafe article, local business and shopping search across Korea's dominant portal.
license: MIT-0
author: ScraperSocial
homepage: https://scrapersocial.com
repository: https://github.com/nikhonit/social-media-api-skills
tags:
  - naver
  - korea
  - blog
  - shopping
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

# Naver API skill

Read public Naver results as clean JSON. This Naver API skill covers the four searches that matter on Korea's dominant portal: blog posts, cafe articles, local businesses and shopping listings. If you are researching the Korean market, Google data will not represent it — Naver is where the audience and the content actually are.

This skill wraps **4 live Naver endpoints** from the [ScraperSocial](https://scrapersocial.com) API. Public data only, returned as clean JSON.

## When to use this skill

- You are researching the Korean market and need sources Google does not index well.
- You are tracking a brand's presence in Naver blogs or cafe communities.
- You need Korean local business listings or shopping prices.

### Do not use this skill when

- **You expect Google-equivalent coverage in English.** Results are Korean-language and Korean-market; query accordingly.
- **You need Naver's own account or ad data.** Not covered; Naver publishes its own developer APIs for that.

## Setup

```bash
export SCRAPERSOCIAL_KEY=sk_live_...   # https://scrapersocial.com/app/keys
```

Signing up at [scrapersocial.com/signup](https://scrapersocial.com/signup) includes 100 free credits, no card required.

## Permissions and scope

These scripts do exactly three things and nothing else: read one environment variable (`SCRAPERSOCIAL_KEY`), send HTTPS requests to `https://api.scrapersocial.com` (the host is a constant in the code, not configurable), and print JSON. They run as `node scripts/<name>.js` with no other shell use, no file writes and no persistence. `call_endpoint.js` accepts only the 4 documented `/v1/naver/` paths in the table below and refuses anything else before a request is made.

## Scripts

| Script | What it does | Input | Credits |
|---|---|---|---|
| `blog_search.js` | List Naver blog search. | query | 2 credits per post |
| `cafearticle_search.js` | List Naver cafearticle search. | query | 2 credits per post |
| `local_search.js` | List Naver local search. | query | 2 credits per place |
| `shop_search.js` | List Naver shop search. | query | 2 credits per product |
| `call_endpoint.js` | Call any `/v1/naver/` endpoint directly | path + params | varies |

Every script also accepts `--limit`, `--cursor`, `--fields`, `--format` and `--fresh`. `--limit` is clamped to 50: above that the API returns an async job instead of data.

## Example

```bash
node skills/naver-api/scripts/blog_search.js "서울 카페"
```

Every response uses the same envelope:

```json
{ "data": {}, "meta": { "count": 20, "next_cursor": "..." }, "request_id": "a18e4ef88ad4b00b" }
```

`meta` appears on paginated endpoints only. Keep `request_id` — support traces calls with it.

## Endpoints

| Endpoint | Input | Returns | Credits | Paginated |
|---|---|---|---|---|
| `/v1/naver/blog-search` | query | post | 2 credits per post | yes |
| `/v1/naver/cafearticle-search` | query | post | 2 credits per post | yes |
| `/v1/naver/local-search` | query | place | 2 credits per place | yes |
| `/v1/naver/shop-search` | query | product | 2 credits per product | yes |

Costs shown per item for paginated endpoints, per call otherwise. Failed calls are not charged.

## FAQ

### What can I search on Naver?

Four endpoints, 2 credits per result each: `blog_search.js`, `cafearticle_search.js`, `local_search.js` and `shop_search.js`.

### Should I query in Korean?

Yes. Naver indexes Korean-language content, and Korean queries return substantially better results.

### What is a cafe article?

Naver Cafe is a large community forum platform. `cafearticle_search.js` searches posts inside those communities — often the most candid source on a brand in Korea.

### Is this an official Naver API?

No. ScraperSocial is independent and not affiliated with Naver. It returns publicly available data only.

## Links

- [Naver data on ScraperSocial](https://scrapersocial.com)
- [All 33 platform skills](https://github.com/nikhonit/social-media-api-skills)
- [OpenAPI spec](https://scrapersocial.com/openapi.json) · [llms.txt](https://scrapersocial.com/llms.txt)

## Disclaimer

ScraperSocial is an independent product and is not affiliated with, endorsed by, or sponsored by any platform named in this repository. All product names, logos and brands are property of their respective owners. These skills return only publicly available data.
