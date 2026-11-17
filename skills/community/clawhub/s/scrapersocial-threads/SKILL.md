---
name: threads-api
version: 1.0.4
description: Threads data toolkit via ScraperSocial — profiles, user post timelines, post stats, keyword search and user search.
license: MIT-0
author: ScraperSocial
homepage: https://scrapersocial.com
repository: https://github.com/nikhonit/social-media-api-skills
tags:
  - threads
  - meta
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

# Threads API skill

Read public Threads data as clean JSON. This Threads API skill returns a profile, a user's posts, stats for a single post, and both keyword and user search. Threads is young enough that tooling for it is thin, so a straightforward JSON read is worth more here than on the established networks.

This skill wraps **5 live Threads endpoints** from the [ScraperSocial](https://scrapersocial.com) API. Public data only, returned as clean JSON.

## When to use this skill

- You are tracking what an account posts on Threads.
- You are monitoring a keyword or brand mention on the network.
- A user pastes a Threads post and asks about its engagement.

### Do not use this skill when

- **You need comments or reply threads.** Threads has no comments endpoint in this API — profile, posts, stats and search only. Do not promise a reply tree you cannot fetch.
- **You expect view counts.** Threads does not publish every metric, so some fields other platforms expose are simply absent.
- **You need to post or reply.** Read-only; Meta's own Threads API covers publishing.

## Setup

```bash
export SCRAPERSOCIAL_KEY=sk_live_...   # https://scrapersocial.com/app/keys
```

Signing up at [scrapersocial.com/signup](https://scrapersocial.com/signup) includes 100 free credits, no card required.

## Permissions and scope

These scripts do exactly three things and nothing else: read one environment variable (`SCRAPERSOCIAL_KEY`), send HTTPS requests to `https://api.scrapersocial.com` (the host is a constant in the code, not configurable), and print JSON. They run as `node scripts/<name>.js` with no other shell use, no file writes and no persistence. `call_endpoint.js` accepts only the 5 documented `/v1/threads/` paths in the table below and refuses anything else before a request is made.

## Scripts

| Script | What it does | Input | Credits |
|---|---|---|---|
| `get_posts.js` | Recent public posts from a Threads account, newest first. | handle | 3 credits per post |
| `get_profile.js` | Public profile for a Threads account: follower count, bio, verification status, and profile link. | handle | 4 credits |
| `search.js` | Public Threads posts matching a keyword or hashtag. | query | 4 credits per result |
| `get_stats.js` | Engagement stats and text for a single Threads post: likes, replies, reposts, quotes, media, and author. | url | 3 credits |
| `user_search.js` | List Threads user search. | query | 4 credits per profile |
| `call_endpoint.js` | Call any `/v1/threads/` endpoint directly | path + params | varies |

Every script also accepts `--limit`, `--cursor`, `--fields`, `--format` and `--fresh`. `--limit` is clamped to 50: above that the API returns an async job instead of data.

## Example

```bash
node skills/threads-api/scripts/search.js "design systems"
```

Every response uses the same envelope:

```json
{ "data": {}, "meta": { "count": 20, "next_cursor": "..." }, "request_id": "a18e4ef88ad4b00b" }
```

`meta` appears on paginated endpoints only. Keep `request_id` — support traces calls with it.

## Endpoints

| Endpoint | Input | Returns | Credits | Paginated |
|---|---|---|---|---|
| `/v1/threads/posts` | handle | post | 3 credits per post | yes |
| `/v1/threads/profile` | handle | profile | 4 credits | no |
| `/v1/threads/search` | query | result | 4 credits per result | yes |
| `/v1/threads/stats` | url | post | 3 credits | no |
| `/v1/threads/user-search` | query | profile | 4 credits per profile | yes |

Costs shown per item for paginated endpoints, per call otherwise. Failed calls are not charged.

## FAQ

### What can I get from Threads?

Five endpoints: `get_profile.js`, `get_posts.js`, `get_stats.js`, `search.js` and `user_search.js`, costing 3–4 credits each.

### Can I get replies to a Threads post?

No. There is no comments or replies endpoint for Threads in this API. Facebook, Instagram, YouTube, LinkedIn, Reddit, TikTok and Hacker News do have one.

### Why are some engagement fields missing?

Threads does not publish everything other networks do — view counts in particular. The API returns what is public rather than estimating.

### Is this an official Threads API?

No. ScraperSocial is independent and not affiliated with Meta. It returns publicly available data only.

## Links

- [Threads data on ScraperSocial](https://scrapersocial.com)
- [All 33 platform skills](https://github.com/nikhonit/social-media-api-skills)
- [OpenAPI spec](https://scrapersocial.com/openapi.json) · [llms.txt](https://scrapersocial.com/llms.txt)

## Disclaimer

ScraperSocial is an independent product and is not affiliated with, endorsed by, or sponsored by any platform named in this repository. All product names, logos and brands are property of their respective owners. These skills return only publicly available data.
