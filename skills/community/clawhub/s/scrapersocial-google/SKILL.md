---
name: google-api
version: 1.0.4
description: Google data toolkit via ScraperSocial — search results, Business Profile info, business reviews and updates, and company ad listings.
license: MIT-0
author: ScraperSocial
homepage: https://scrapersocial.com
repository: https://github.com/nikhonit/social-media-api-skills
tags:
  - google
  - serp
  - business-profile
  - reviews
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

# Google API skill

Read public Google results as clean JSON. This Google API skill returns search result pages, Google Business Profile details, the reviews and updates attached to a business, and the ads a company is running — the core inputs for local SEO work, reputation monitoring and competitive research.

This skill wraps **5 live Google endpoints** from the [ScraperSocial](https://scrapersocial.com) API. Public data only, returned as clean JSON.

## When to use this skill

- You need SERP results for a query, as structured data rather than HTML.
- You are monitoring a business's Google reviews or its profile details.
- You want to see what ads a company is running.
- You are doing local SEO and need what Google publishes about a listing.

### Do not use this skill when

- **You need Google Search Console or Analytics data** for a property you own. Those are account-scoped; use Google's own APIs.
- **You need Maps places data.** Use the `google-maps-api` skill — `place`, `photos` and `contacts` live there.
- **You need news results.** Use `google-news-api`. Shopping results are in `google-shopping-api`, and interest-over-time is in `google-trends-api`.
- **You are firing searches speculatively.** Each result costs credits.

## Setup

```bash
export SCRAPERSOCIAL_KEY=sk_live_...   # https://scrapersocial.com/app/keys
```

Signing up at [scrapersocial.com/signup](https://scrapersocial.com/signup) includes 100 free credits, no card required.

## Permissions and scope

These scripts do exactly three things and nothing else: read one environment variable (`SCRAPERSOCIAL_KEY`), send HTTPS requests to `https://api.scrapersocial.com` (the host is a constant in the code, not configurable), and print JSON. They run as `node scripts/<name>.js` with no other shell use, no file writes and no persistence. `call_endpoint.js` accepts only the 5 documented `/v1/google/` paths in the table below and refuses anything else before a request is made.

## Scripts

| Script | What it does | Input | Credits |
|---|---|---|---|
| `get_business_info.js` | Get Google Search business info. | url|handle | 3 credits |
| `get_business_reviews.js` | List Google Search business reviews. | url|handle | 2 credits per review |
| `get_business_updates.js` | List Google Search business updates. | url | 3 credits per post |
| `get_company_ads.js` | List Google Search company ads. | url|handle | 3 credits per ad |
| `search.js` | List Google Search search. | query | 2 credits per page |
| `call_endpoint.js` | Call any `/v1/google/` endpoint directly | path + params | varies |

Every script also accepts `--limit`, `--cursor`, `--fields`, `--format` and `--fresh`. `--limit` is clamped to 50: above that the API returns an async job instead of data.

## Example

```bash
node skills/google-api/scripts/search.js "best running shoes 2026"
```

Every response uses the same envelope:

```json
{ "data": {}, "meta": { "count": 20, "next_cursor": "..." }, "request_id": "a18e4ef88ad4b00b" }
```

`meta` appears on paginated endpoints only. Keep `request_id` — support traces calls with it.

## Endpoints

| Endpoint | Input | Returns | Credits | Paginated |
|---|---|---|---|---|
| `/v1/google/business-info` | url|handle | place | 3 credits | no |
| `/v1/google/business-reviews` | url|handle | review | 2 credits per review | yes |
| `/v1/google/business-updates` | url | post | 3 credits per post | yes |
| `/v1/google/company-ads` | url|handle | ad | 3 credits per ad | yes |
| `/v1/google/search` | query | page | 2 credits per page | yes |

Costs shown per item for paginated endpoints, per call otherwise. Failed calls are not charged.

## FAQ

### How do I get Google search results as JSON?

`search.js` with a query returns results at 2 credits per result. Use `--limit` to keep volume down.

### Can I monitor Google reviews for a business?

Yes. `get_business_reviews.js` takes the business URL or handle and returns reviews at 2 credits each. `get_business_info.js` returns the profile itself.

### Is this an official Google API?

No. ScraperSocial is independent and not affiliated with Google. It returns publicly available data only.

### Which skill do I use for Maps, News, Shopping or Trends?

Each is a separate skill in this repo, because each is a separate set of endpoints: `google-maps-api`, `google-news-api`, `google-shopping-api`, `google-trends-api`.

## Links

- [Google data on ScraperSocial](https://scrapersocial.com)
- [All 33 platform skills](https://github.com/nikhonit/social-media-api-skills)
- [OpenAPI spec](https://scrapersocial.com/openapi.json) · [llms.txt](https://scrapersocial.com/llms.txt)

## Disclaimer

ScraperSocial is an independent product and is not affiliated with, endorsed by, or sponsored by any platform named in this repository. All product names, logos and brands are property of their respective owners. These skills return only publicly available data.
