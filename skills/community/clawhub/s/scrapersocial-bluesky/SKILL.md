---
name: bluesky-api
version: 1.0.4
description: Bluesky data toolkit via ScraperSocial — public profiles, user post timelines and keyword search across the network.
license: MIT-0
author: ScraperSocial
homepage: https://scrapersocial.com
repository: https://github.com/nikhonit/social-media-api-skills
tags:
  - bluesky
  - atproto
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

# Bluesky API skill

Read public Bluesky data as clean JSON. This Bluesky API skill returns a profile, a user's posts, or keyword search results across the network — at 1 credit per call, which makes it one of the cheapest ways to monitor a conversation on an open social platform.

This skill wraps **3 live Bluesky endpoints** from the [ScraperSocial](https://scrapersocial.com) API. Public data only, returned as clean JSON.

## When to use this skill

- You are tracking what a specific Bluesky account is posting.
- You want keyword search across public posts, for monitoring a brand or topic.
- A user pastes a Bluesky handle and asks who it is or what they post about.

### Do not use this skill when

- **You need to post, reply or follow.** This is read-only. Bluesky's own AT Protocol API handles writes and is free for authenticated users.
- **You need the full firehose.** These are point queries, not a streaming feed. For real-time ingestion at volume, connect to the protocol directly.
- **You need private or blocked-account data.** Public data only.

## Setup

```bash
export SCRAPERSOCIAL_KEY=sk_live_...   # https://scrapersocial.com/app/keys
```

Signing up at [scrapersocial.com/signup](https://scrapersocial.com/signup) includes 100 free credits, no card required.

## Permissions and scope

These scripts do exactly three things and nothing else: read one environment variable (`SCRAPERSOCIAL_KEY`), send HTTPS requests to `https://api.scrapersocial.com` (the host is a constant in the code, not configurable), and print JSON. They run as `node scripts/<name>.js` with no other shell use, no file writes and no persistence. `call_endpoint.js` accepts only the 3 documented `/v1/bluesky/` paths in the table below and refuses anything else before a request is made.

## Scripts

| Script | What it does | Input | Credits |
|---|---|---|---|
| `get_profile.js` | Get Bluesky profile. | handle | 1 credit |
| `search.js` | List Bluesky search. | query | 1 credit per post |
| `get_user_posts.js` | List Bluesky user posts. | handle | 1 credit per post |
| `call_endpoint.js` | Call any `/v1/bluesky/` endpoint directly | path + params | varies |

Every script also accepts `--limit`, `--cursor`, `--fields`, `--format` and `--fresh`. `--limit` is clamped to 50: above that the API returns an async job instead of data.

## Example

```bash
node skills/bluesky-api/scripts/get_profile.js bsky.app
```

Every response uses the same envelope:

```json
{ "data": {}, "meta": { "count": 20, "next_cursor": "..." }, "request_id": "a18e4ef88ad4b00b" }
```

`meta` appears on paginated endpoints only. Keep `request_id` — support traces calls with it.

## Endpoints

| Endpoint | Input | Returns | Credits | Paginated |
|---|---|---|---|---|
| `/v1/bluesky/profile` | handle | profile | 1 credit | no |
| `/v1/bluesky/search` | query | post | 1 credit per post | yes |
| `/v1/bluesky/user-posts` | handle | post | 1 credit per post | yes |

Costs shown per item for paginated endpoints, per call otherwise. Failed calls are not charged.

## FAQ

### How do I get Bluesky posts for a user?

`get_user_posts.js` with the handle returns their public posts, 1 credit per post returned.

### Do I need a Bluesky account?

No. These endpoints read public data and authenticate against ScraperSocial, not Bluesky.

### Is this an official Bluesky API?

No. ScraperSocial is independent and not affiliated with Bluesky. Bluesky also publishes its own open API, which is a better fit if you need writes or the firehose.

### What does it cost?

1 credit per call, or per item on the paginated endpoints. The 100 free signup credits go a long way here.

## Links

- [Bluesky data on ScraperSocial](https://scrapersocial.com)
- [All 33 platform skills](https://github.com/nikhonit/social-media-api-skills)
- [OpenAPI spec](https://scrapersocial.com/openapi.json) · [llms.txt](https://scrapersocial.com/llms.txt)

## Disclaimer

ScraperSocial is an independent product and is not affiliated with, endorsed by, or sponsored by any platform named in this repository. All product names, logos and brands are property of their respective owners. These skills return only publicly available data.
