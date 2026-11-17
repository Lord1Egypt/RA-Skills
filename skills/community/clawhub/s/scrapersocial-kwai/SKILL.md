---
name: kwai-api
version: 1.0.4
description: Kwai data toolkit via ScraperSocial — creator profiles, user post listings and single video lookups.
license: MIT-0
author: ScraperSocial
homepage: https://scrapersocial.com
repository: https://github.com/nikhonit/social-media-api-skills
tags:
  - kwai
  - short-video
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

# Kwai API skill

Read public Kwai data as clean JSON. This Kwai API skill returns a creator profile, that creator's posts, or a single video by URL. Kwai is one of the largest short-video platforms in Latin America and South Asia and is poorly served by Western data tools, which is most of the reason this skill exists.

This skill wraps **3 live Kwai endpoints** from the [ScraperSocial](https://scrapersocial.com) API. Public data only, returned as clean JSON.

## When to use this skill

- You are researching creators or short-video trends in markets where Kwai has real share.
- A user pastes a Kwai link and asks who posted it or what the account is.
- You are benchmarking a creator's Kwai presence against their TikTok or Instagram.

### Do not use this skill when

- **You assumed Kwai mirrors TikTok.** They are different platforms with different creators; do not present one as a proxy for the other.
- **You need transcripts or AI summaries.** Kwai has three endpoints — profile, posts and a single post. There is no transcript capability here.
- **You need to post or interact.** Read-only.

## Setup

```bash
export SCRAPERSOCIAL_KEY=sk_live_...   # https://scrapersocial.com/app/keys
```

Signing up at [scrapersocial.com/signup](https://scrapersocial.com/signup) includes 100 free credits, no card required.

## Permissions and scope

These scripts do exactly three things and nothing else: read one environment variable (`SCRAPERSOCIAL_KEY`), send HTTPS requests to `https://api.scrapersocial.com` (the host is a constant in the code, not configurable), and print JSON. They run as `node scripts/<name>.js` with no other shell use, no file writes and no persistence. `call_endpoint.js` accepts only the 3 documented `/v1/kwai/` paths in the table below and refuses anything else before a request is made.

## Scripts

| Script | What it does | Input | Credits |
|---|---|---|---|
| `get_post.js` | Get Kwai post. | url | 2 credits |
| `get_profile.js` | Get Kwai profile. | url|handle | 2 credits |
| `get_user_posts.js` | List Kwai user posts. | url|handle | 2 credits per post |
| `call_endpoint.js` | Call any `/v1/kwai/` endpoint directly | path + params | varies |

Every script also accepts `--limit`, `--cursor`, `--fields`, `--format` and `--fresh`. `--limit` is clamped to 50: above that the API returns an async job instead of data.

## Example

```bash
node skills/kwai-api/scripts/get_profile.js <kwai-handle>
```

Every response uses the same envelope:

```json
{ "data": {}, "meta": { "count": 20, "next_cursor": "..." }, "request_id": "a18e4ef88ad4b00b" }
```

`meta` appears on paginated endpoints only. Keep `request_id` — support traces calls with it.

## Endpoints

| Endpoint | Input | Returns | Credits | Paginated |
|---|---|---|---|---|
| `/v1/kwai/post` | url | post | 2 credits | no |
| `/v1/kwai/profile` | url|handle | profile | 2 credits | no |
| `/v1/kwai/user-posts` | url|handle | post | 2 credits per post | yes |

Costs shown per item for paginated endpoints, per call otherwise. Failed calls are not charged.

## FAQ

### What can I get from Kwai?

Three things: `get_profile.js` for a creator, `get_user_posts.js` for their posts, and `get_post.js` for one video. Each costs 2 credits.

### Can I transcribe a Kwai video?

Not through this API. Transcripts are available for TikTok, Instagram, Facebook, X and YouTube.

### Is this an official Kwai API?

No. ScraperSocial is independent and not affiliated with Kwai or Kuaishou. It returns publicly available data only.

## Links

- [Kwai data on ScraperSocial](https://scrapersocial.com)
- [All 33 platform skills](https://github.com/nikhonit/social-media-api-skills)
- [OpenAPI spec](https://scrapersocial.com/openapi.json) · [llms.txt](https://scrapersocial.com/llms.txt)

## Disclaimer

ScraperSocial is an independent product and is not affiliated with, endorsed by, or sponsored by any platform named in this repository. All product names, logos and brands are property of their respective owners. These skills return only publicly available data.
