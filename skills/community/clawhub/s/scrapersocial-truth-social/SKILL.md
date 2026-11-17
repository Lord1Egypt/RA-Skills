---
name: truth-social-api
version: 1.0.4
description: Truth Social data toolkit via ScraperSocial — public profiles and user post timelines as clean JSON.
license: MIT-0
author: ScraperSocial
homepage: https://scrapersocial.com
repository: https://github.com/nikhonit/social-media-api-skills
tags:
  - truth-social
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

# Truth Social API skill

Read public Truth Social data as clean JSON. This Truth Social API skill has two endpoints: a public profile and a user's posts, at 2 credits each. Coverage of this network by mainstream data tools is thin, which matters for anyone doing balanced media monitoring rather than monitoring only the platforms that are easy to read.

This skill wraps **2 live Truth Social endpoints** from the [ScraperSocial](https://scrapersocial.com) API. Public data only, returned as clean JSON.

## When to use this skill

- You are doing cross-platform media or discourse monitoring and need this network represented.
- You are tracking what a specific public account posts.
- A user pastes a Truth Social link and asks what the account is.

### Do not use this skill when

- **You need search.** There is no search endpoint here — you need a known handle. Profile and posts only.
- **You need to post or interact.** Read-only.
- **You need private accounts.** Public data only.

## Setup

```bash
export SCRAPERSOCIAL_KEY=sk_live_...   # https://scrapersocial.com/app/keys
```

Signing up at [scrapersocial.com/signup](https://scrapersocial.com/signup) includes 100 free credits, no card required.

## Permissions and scope

These scripts do exactly three things and nothing else: read one environment variable (`SCRAPERSOCIAL_KEY`), send HTTPS requests to `https://api.scrapersocial.com` (the host is a constant in the code, not configurable), and print JSON. They run as `node scripts/<name>.js` with no other shell use, no file writes and no persistence. `call_endpoint.js` accepts only the 2 documented `/v1/truthsocial/` paths in the table below and refuses anything else before a request is made.

## Scripts

| Script | What it does | Input | Credits |
|---|---|---|---|
| `get_profile.js` | Get Truth Social profile. | handle | 2 credits |
| `get_user_posts.js` | List Truth Social user posts. | handle | 2 credits per post |
| `call_endpoint.js` | Call any `/v1/truthsocial/` endpoint directly | path + params | varies |

Every script also accepts `--limit`, `--cursor`, `--fields`, `--format` and `--fresh`. `--limit` is clamped to 50: above that the API returns an async job instead of data.

## Example

```bash
node skills/truth-social-api/scripts/get_profile.js <truthsocial-handle>
```

Every response uses the same envelope:

```json
{ "data": {}, "meta": { "count": 20, "next_cursor": "..." }, "request_id": "a18e4ef88ad4b00b" }
```

`meta` appears on paginated endpoints only. Keep `request_id` — support traces calls with it.

## Endpoints

| Endpoint | Input | Returns | Credits | Paginated |
|---|---|---|---|---|
| `/v1/truthsocial/profile` | handle | profile | 2 credits | no |
| `/v1/truthsocial/user-posts` | handle | post | 2 credits per post | yes |

Costs shown per item for paginated endpoints, per call otherwise. Failed calls are not charged.

## FAQ

### What can I get from Truth Social?

Two endpoints: `get_profile.js` for a public profile and `get_user_posts.js` for that account's posts, 2 credits each.

### Can I search Truth Social by keyword?

No. This API covers profile and posts only, so you need the handle up front.

### Is this an official Truth Social API?

No. ScraperSocial is independent and not affiliated with Truth Social or TMTG. It returns publicly available data only.

## Links

- [Truth Social data on ScraperSocial](https://scrapersocial.com)
- [All 33 platform skills](https://github.com/nikhonit/social-media-api-skills)
- [OpenAPI spec](https://scrapersocial.com/openapi.json) · [llms.txt](https://scrapersocial.com/llms.txt)

## Disclaimer

ScraperSocial is an independent product and is not affiliated with, endorsed by, or sponsored by any platform named in this repository. All product names, logos and brands are property of their respective owners. These skills return only publicly available data.
