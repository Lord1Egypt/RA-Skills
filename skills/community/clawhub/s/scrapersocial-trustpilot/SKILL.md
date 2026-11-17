---
name: trustpilot-api
version: 1.0.4
description: Trustpilot data toolkit via ScraperSocial — company review listings as clean JSON.
license: MIT-0
author: ScraperSocial
homepage: https://scrapersocial.com
repository: https://github.com/nikhonit/social-media-api-skills
tags:
  - trustpilot
  - reviews
  - reputation
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

# Trustpilot API skill

Read public Trustpilot reviews as clean JSON. This Trustpilot API skill has a single endpoint: give it a company URL or handle and it returns their reviews at 1 credit each — the cheapest review source in this repo, and the standard reference for company reputation in Europe.

This skill wraps **1 live Trustpilot endpoint** from the [ScraperSocial](https://scrapersocial.com) API. Public data only, returned as clean JSON.

## When to use this skill

- You are assessing a company's reputation before recommending or transacting with them.
- You are monitoring your own or a competitor's review flow.
- A user asks whether a company is trustworthy and you want evidence rather than an impression.

### Do not use this skill when

- **You need to reply to reviews or flag them.** Read-only; Trustpilot's Business API covers that.
- **You are pulling every review for a large brand.** Charged per review — scope with `--limit`.
- **You need product-level reviews.** This is company-level. Product reviews live in `amazon-api`, `tiktok-shop-api`, `app-store-api` and `google-play-api`.

## Setup

```bash
export SCRAPERSOCIAL_KEY=sk_live_...   # https://scrapersocial.com/app/keys
```

Signing up at [scrapersocial.com/signup](https://scrapersocial.com/signup) includes 100 free credits, no card required.

## Permissions and scope

These scripts do exactly three things and nothing else: read one environment variable (`SCRAPERSOCIAL_KEY`), send HTTPS requests to `https://api.scrapersocial.com` (the host is a constant in the code, not configurable), and print JSON. They run as `node scripts/<name>.js` with no other shell use, no file writes and no persistence. `call_endpoint.js` accepts only the 1 documented `/v1/trustpilot/` paths in the table below and refuses anything else before a request is made.

## Scripts

| Script | What it does | Input | Credits |
|---|---|---|---|
| `get_reviews.js` | List Trustpilot reviews. | url|handle | 1 credit per review |
| `call_endpoint.js` | Call any `/v1/trustpilot/` endpoint directly | path + params | varies |

Every script also accepts `--limit`, `--cursor`, `--fields`, `--format` and `--fresh`. `--limit` is clamped to 50: above that the API returns an async job instead of data.

## Example

```bash
node skills/trustpilot-api/scripts/get_reviews.js <company-domain>
```

Every response uses the same envelope:

```json
{ "data": {}, "meta": { "count": 20, "next_cursor": "..." }, "request_id": "a18e4ef88ad4b00b" }
```

`meta` appears on paginated endpoints only. Keep `request_id` — support traces calls with it.

## Endpoints

| Endpoint | Input | Returns | Credits | Paginated |
|---|---|---|---|---|
| `/v1/trustpilot/reviews` | url|handle | review | 1 credit per review | yes |

Costs shown per item for paginated endpoints, per call otherwise. Failed calls are not charged.

## FAQ

### How do I get Trustpilot reviews as JSON?

`get_reviews.js` with the company URL or handle, 1 credit per review returned.

### Can I get an overall rating?

The review listing carries the rating data Trustpilot publishes alongside each review. There is no separate summary endpoint.

### Is this an official Trustpilot API?

No. ScraperSocial is independent and not affiliated with Trustpilot. It returns publicly available review data only.

## Links

- [Trustpilot data on ScraperSocial](https://scrapersocial.com)
- [All 33 platform skills](https://github.com/nikhonit/social-media-api-skills)
- [OpenAPI spec](https://scrapersocial.com/openapi.json) · [llms.txt](https://scrapersocial.com/llms.txt)

## Disclaimer

ScraperSocial is an independent product and is not affiliated with, endorsed by, or sponsored by any platform named in this repository. All product names, logos and brands are property of their respective owners. These skills return only publicly available data.
