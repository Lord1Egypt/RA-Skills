---
name: app-store-api
version: 1.0.4
description: Apple App Store data toolkit via ScraperSocial — app metadata, user reviews, keyword search, category charts and storefront locations.
license: MIT-0
author: ScraperSocial
homepage: https://scrapersocial.com
repository: https://github.com/nikhonit/social-media-api-skills
tags:
  - app-store
  - ios
  - aso
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

# App Store API skill

Read public Apple App Store data as clean JSON. This App Store API skill returns app metadata, user reviews, keyword search results, ranked category lists and the storefronts an app is available in — the raw material for app store optimisation, competitor tracking and review analysis. Every endpoint here costs 1 credit, which makes it cheap to poll regularly.

This skill wraps **6 live App Store endpoints** from the [ScraperSocial](https://scrapersocial.com) API. Public data only, returned as clean JSON.

## When to use this skill

- You are doing ASO work: checking how an app ranks for a keyword, or what its listing says.
- You need user reviews for an app to summarise sentiment or track a regression after a release.
- You are building a competitor watchlist and want category charts over time.
- A user pastes an App Store link and asks what the app is or how it is rated.

### Do not use this skill when

- **You need App Store Connect data** — sales, installs, crash reports or anything tied to a developer account. This reads the public storefront only.
- **You need Google Play data.** Use the `google-play-api` skill; the two stores are separate endpoints with different app identifiers.
- **You want download or revenue estimates.** The API returns what the storefront publishes; it does not model private metrics.

## Setup

```bash
export SCRAPERSOCIAL_KEY=sk_live_...   # https://scrapersocial.com/app/keys
```

Signing up at [scrapersocial.com/signup](https://scrapersocial.com/signup) includes 100 free credits, no card required.

## Permissions and scope

These scripts do exactly three things and nothing else: read one environment variable (`SCRAPERSOCIAL_KEY`), send HTTPS requests to `https://api.scrapersocial.com` (the host is a constant in the code, not configurable), and print JSON. They run as `node scripts/<name>.js` with no other shell use, no file writes and no persistence. `call_endpoint.js` accepts only the 6 documented `/v1/app_store/` paths in the table below and refuses anything else before a request is made.

## Scripts

| Script | What it does | Input | Credits |
|---|---|---|---|
| `get_app_info.js` | Get Apple App Store app info. | handle | 1 credit |
| `get_app_list.js` | List Apple App Store app list. | query | 1 credit per app |
| `get_app_reviews.js` | List Apple App Store app reviews. | handle | 1 credit per review |
| `app_search.js` | List Apple App Store app search. | query | 1 credit per app |
| `get_categories.js` | List Apple App Store categories. | none | 1 credit per category |
| `get_locations.js` | Get Apple App Store locations. | none | 1 credit |
| `call_endpoint.js` | Call any `/v1/app_store/` endpoint directly | path + params | varies |

Every script also accepts `--limit`, `--cursor`, `--fields`, `--format` and `--fresh`. `--limit` is clamped to 50: above that the API returns an async job instead of data.

## Example

```bash
node skills/app-store-api/scripts/app_search.js "meditation timer"
```

Every response uses the same envelope:

```json
{ "data": {}, "meta": { "count": 20, "next_cursor": "..." }, "request_id": "a18e4ef88ad4b00b" }
```

`meta` appears on paginated endpoints only. Keep `request_id` — support traces calls with it.

## Endpoints

| Endpoint | Input | Returns | Credits | Paginated |
|---|---|---|---|---|
| `/v1/app_store/app-info` | handle | app | 1 credit | no |
| `/v1/app_store/app-list` | query | app | 1 credit per app | yes |
| `/v1/app_store/app-reviews` | handle | review | 1 credit per review | yes |
| `/v1/app_store/app-search` | query | app | 1 credit per app | yes |
| `/v1/app_store/categories` | none | category | 1 credit per category | yes |
| `/v1/app_store/locations` | none | report | 1 credit | no |

Costs shown per item for paginated endpoints, per call otherwise. Failed calls are not charged.

## FAQ

### How do I get App Store reviews as JSON?

`get_app_reviews.js` takes the app handle and returns reviews at 1 credit per review. Use `--limit` to control volume and `--cursor` to page.

### How do I find an app without knowing its ID?

Use `app_search.js` with a keyword, or `get_app_list.js` for ranked category lists. Both return handles you can pass to `get_app_info.js`.

### Does this cover every country storefront?

`get_locations.js` returns the storefronts the API supports. App availability and rankings differ by storefront.

### Is this an official Apple API?

No. ScraperSocial is independent and not affiliated with Apple. It returns publicly available App Store data only.

## Links

- [App Store data on ScraperSocial](https://scrapersocial.com)
- [All 33 platform skills](https://github.com/nikhonit/social-media-api-skills)
- [OpenAPI spec](https://scrapersocial.com/openapi.json) · [llms.txt](https://scrapersocial.com/llms.txt)

## Disclaimer

ScraperSocial is an independent product and is not affiliated with, endorsed by, or sponsored by any platform named in this repository. All product names, logos and brands are property of their respective owners. These skills return only publicly available data.
