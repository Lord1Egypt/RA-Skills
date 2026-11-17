---
name: google-news-api
version: 1.0.4
description: Google News data toolkit via ScraperSocial — keyword search across news headlines and sources as clean JSON.
license: MIT-0
author: ScraperSocial
homepage: https://scrapersocial.com
repository: https://github.com/nikhonit/social-media-api-skills
tags:
  - google-news
  - news
  - headlines
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

# Google News API skill

Read public Google News results as clean JSON. This Google News API skill is a single endpoint: search the news index by keyword and get back headlines, sources and links at 1 credit per article — a cheap way to give an agent current-events awareness or to monitor coverage of a company.

This skill wraps **1 live Google News endpoint** from the [ScraperSocial](https://scrapersocial.com) API. Public data only, returned as clean JSON.

## When to use this skill

- A user asks what the news says about a topic, company or person.
- You are monitoring press coverage for a brand.
- You need recent headlines as context before answering a time-sensitive question.

### Do not use this skill when

- **You need full article text.** This returns headlines and links, not article bodies.
- **You need a persistent alert.** This is a point query; scheduling and deduplication are yours to build.
- **The user's question is not time-sensitive.** Do not spend credits on background you do not need.

## Setup

```bash
export SCRAPERSOCIAL_KEY=sk_live_...   # https://scrapersocial.com/app/keys
```

Signing up at [scrapersocial.com/signup](https://scrapersocial.com/signup) includes 100 free credits, no card required.

## Permissions and scope

These scripts do exactly three things and nothing else: read one environment variable (`SCRAPERSOCIAL_KEY`), send HTTPS requests to `https://api.scrapersocial.com` (the host is a constant in the code, not configurable), and print JSON. They run as `node scripts/<name>.js` with no other shell use, no file writes and no persistence. `call_endpoint.js` accepts only the 1 documented `/v1/google_news/` paths in the table below and refuses anything else before a request is made.

## Scripts

| Script | What it does | Input | Credits |
|---|---|---|---|
| `search.js` | List Google News search. | query | 1 credit per article |
| `call_endpoint.js` | Call any `/v1/google_news/` endpoint directly | path + params | varies |

Every script also accepts `--limit`, `--cursor`, `--fields`, `--format` and `--fresh`. `--limit` is clamped to 50: above that the API returns an async job instead of data.

## Example

```bash
node skills/google-news-api/scripts/search.js "semiconductor export controls"
```

Every response uses the same envelope:

```json
{ "data": {}, "meta": { "count": 20, "next_cursor": "..." }, "request_id": "a18e4ef88ad4b00b" }
```

`meta` appears on paginated endpoints only. Keep `request_id` — support traces calls with it.

## Endpoints

| Endpoint | Input | Returns | Credits | Paginated |
|---|---|---|---|---|
| `/v1/google_news/search` | query | article | 1 credit per article | yes |

Costs shown per item for paginated endpoints, per call otherwise. Failed calls are not charged.

## FAQ

### How do I search news as JSON?

`search.js` with a query, 1 credit per article returned. Set `--limit` to keep volume predictable.

### Does it return the full article?

No — headline, source and link. Fetch the article yourself if you need the body.

### Is this an official Google News API?

No. ScraperSocial is independent and not affiliated with Google. It returns publicly available data only.

## Links

- [Google News data on ScraperSocial](https://scrapersocial.com)
- [All 33 platform skills](https://github.com/nikhonit/social-media-api-skills)
- [OpenAPI spec](https://scrapersocial.com/openapi.json) · [llms.txt](https://scrapersocial.com/llms.txt)

## Disclaimer

ScraperSocial is an independent product and is not affiliated with, endorsed by, or sponsored by any platform named in this repository. All product names, logos and brands are property of their respective owners. These skills return only publicly available data.
