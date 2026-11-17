---
name: snapchat-api
version: 1.0.4
description: Snapchat data toolkit via ScraperSocial — public creator profile lookups as clean JSON.
license: MIT-0
author: ScraperSocial
homepage: https://scrapersocial.com
repository: https://github.com/nikhonit/social-media-api-skills
tags:
  - snapchat
  - creator
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

# Snapchat API skill

Read public Snapchat profiles as clean JSON. This Snapchat API skill has a single endpoint: give it a handle and it returns the public profile for 2 credits. Snapchat publishes very little publicly, which is exactly why a reliable profile lookup is worth having — it is usually the only programmatic read available.

This skill wraps **1 live Snapchat endpoint** from the [ScraperSocial](https://scrapersocial.com) API. Public data only, returned as clean JSON.

## When to use this skill

- You are verifying that a Snapchat handle exists and belongs to the creator you think it does.
- You are building a cross-platform creator profile and Snapchat is one of the channels.

### Do not use this skill when

- **You expect posts, stories or engagement data.** One endpoint, profile only. Snapchat does not publish the rest.
- **You need Snap Ads or account analytics.** Those are account-scoped; use Snap's own APIs.
- **You need to send snaps or messages.** Read-only.

## Setup

```bash
export SCRAPERSOCIAL_KEY=sk_live_...   # https://scrapersocial.com/app/keys
```

Signing up at [scrapersocial.com/signup](https://scrapersocial.com/signup) includes 100 free credits, no card required.

## Permissions and scope

These scripts do exactly three things and nothing else: read one environment variable (`SCRAPERSOCIAL_KEY`), send HTTPS requests to `https://api.scrapersocial.com` (the host is a constant in the code, not configurable), and print JSON. They run as `node scripts/<name>.js` with no other shell use, no file writes and no persistence. `call_endpoint.js` accepts only the 1 documented `/v1/snapchat/` paths in the table below and refuses anything else before a request is made.

## Scripts

| Script | What it does | Input | Credits |
|---|---|---|---|
| `get_profile.js` | Get Snapchat profile. | handle | 2 credits |
| `call_endpoint.js` | Call any `/v1/snapchat/` endpoint directly | path + params | varies |

Every script also accepts `--limit`, `--cursor`, `--fields`, `--format` and `--fresh`. `--limit` is clamped to 50: above that the API returns an async job instead of data.

## Example

```bash
node skills/snapchat-api/scripts/get_profile.js <snapchat-handle>
```

Every response uses the same envelope:

```json
{ "data": {}, "meta": { "count": 20, "next_cursor": "..." }, "request_id": "a18e4ef88ad4b00b" }
```

`meta` appears on paginated endpoints only. Keep `request_id` — support traces calls with it.

## Endpoints

| Endpoint | Input | Returns | Credits | Paginated |
|---|---|---|---|---|
| `/v1/snapchat/profile` | handle | profile | 2 credits | no |

Costs shown per item for paginated endpoints, per call otherwise. Failed calls are not charged.

## FAQ

### What does the Snapchat endpoint return?

`get_profile.js` with the handle returns the public profile for 2 credits.

### Can I get someone's stories or snaps?

No. Stories and snaps are not public data and are not available through this API.

### Is this an official Snapchat API?

No. ScraperSocial is independent and not affiliated with Snap Inc. It returns publicly available profile data only.

## Links

- [Snapchat data on ScraperSocial](https://scrapersocial.com)
- [All 33 platform skills](https://github.com/nikhonit/social-media-api-skills)
- [OpenAPI spec](https://scrapersocial.com/openapi.json) · [llms.txt](https://scrapersocial.com/llms.txt)

## Disclaimer

ScraperSocial is an independent product and is not affiliated with, endorsed by, or sponsored by any platform named in this repository. All product names, logos and brands are property of their respective owners. These skills return only publicly available data.
