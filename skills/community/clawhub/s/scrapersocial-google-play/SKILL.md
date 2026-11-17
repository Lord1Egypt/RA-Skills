---
name: google-play-api
version: 1.0.4
description: Google Play data toolkit via ScraperSocial — Android app metadata, user reviews, keyword search and store categories.
license: MIT-0
author: ScraperSocial
homepage: https://scrapersocial.com
repository: https://github.com/nikhonit/social-media-api-skills
tags:
  - google-play
  - android
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

# Google Play API skill

Read public Google Play data as clean JSON. This Google Play API skill returns Android app metadata, user reviews, keyword search results and the store's category list — the Android half of app store optimisation work, at 1 credit per call.

This skill wraps **4 live Google Play endpoints** from the [ScraperSocial](https://scrapersocial.com) API. Public data only, returned as clean JSON.

## When to use this skill

- You are doing ASO for an Android app and need listing data or rankings for a keyword.
- You need Play Store reviews to track sentiment after a release.
- A user pastes a Play Store link and asks what the app is or how it is rated.

### Do not use this skill when

- **You need Play Console data** — installs, revenue, crash rates, or anything tied to a developer account. This reads the public storefront only.
- **You need iOS data.** Use the `app-store-api` skill; app identifiers differ between the two stores.

## Setup

```bash
export SCRAPERSOCIAL_KEY=sk_live_...   # https://scrapersocial.com/app/keys
```

Signing up at [scrapersocial.com/signup](https://scrapersocial.com/signup) includes 100 free credits, no card required.

## Permissions and scope

These scripts do exactly three things and nothing else: read one environment variable (`SCRAPERSOCIAL_KEY`), send HTTPS requests to `https://api.scrapersocial.com` (the host is a constant in the code, not configurable), and print JSON. They run as `node scripts/<name>.js` with no other shell use, no file writes and no persistence. `call_endpoint.js` accepts only the 4 documented `/v1/google_play/` paths in the table below and refuses anything else before a request is made.

## Scripts

| Script | What it does | Input | Credits |
|---|---|---|---|
| `get_app_info.js` | Get Google Play app info. | handle | 1 credit |
| `get_app_reviews.js` | List Google Play app reviews. | handle | 1 credit per review |
| `app_search.js` | List Google Play app search. | query | 1 credit per app |
| `get_categories.js` | Get Google Play categories. | none | 1 credit |
| `call_endpoint.js` | Call any `/v1/google_play/` endpoint directly | path + params | varies |

Every script also accepts `--limit`, `--cursor`, `--fields`, `--format` and `--fresh`. `--limit` is clamped to 50: above that the API returns an async job instead of data.

## Example

```bash
node skills/google-play-api/scripts/app_search.js "habit tracker"
```

Every response uses the same envelope:

```json
{ "data": {}, "meta": { "count": 20, "next_cursor": "..." }, "request_id": "a18e4ef88ad4b00b" }
```

`meta` appears on paginated endpoints only. Keep `request_id` — support traces calls with it.

## Endpoints

| Endpoint | Input | Returns | Credits | Paginated |
|---|---|---|---|---|
| `/v1/google_play/app-info` | handle | app | 1 credit | no |
| `/v1/google_play/app-reviews` | handle | review | 1 credit per review | yes |
| `/v1/google_play/app-search` | query | app | 1 credit per app | yes |
| `/v1/google_play/categories` | none | report | 1 credit | no |

Costs shown per item for paginated endpoints, per call otherwise. Failed calls are not charged.

## FAQ

### How do I get Google Play reviews as JSON?

`get_app_reviews.js` with the app handle, 1 credit per review returned. Page with `--cursor`.

### How do I find an app by keyword?

`app_search.js` with a query returns matching apps and their handles, which you pass to `get_app_info.js`.

### Is this an official Google Play API?

No. ScraperSocial is independent and not affiliated with Google. It returns publicly available storefront data only.

## Links

- [Google Play data on ScraperSocial](https://scrapersocial.com)
- [All 33 platform skills](https://github.com/nikhonit/social-media-api-skills)
- [OpenAPI spec](https://scrapersocial.com/openapi.json) · [llms.txt](https://scrapersocial.com/llms.txt)

## Disclaimer

ScraperSocial is an independent product and is not affiliated with, endorsed by, or sponsored by any platform named in this repository. All product names, logos and brands are property of their respective owners. These skills return only publicly available data.
