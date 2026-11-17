---
name: hacker-news-api
version: 1.0.4
description: Hacker News data toolkit via ScraperSocial — stories, full comment threads, user profiles and keyword search.
license: MIT-0
author: ScraperSocial
homepage: https://scrapersocial.com
repository: https://github.com/nikhonit/social-media-api-skills
tags:
  - hacker-news
  - hn
  - tech-news
  - comments
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

# Hacker News API skill

Read public Hacker News data as clean JSON. This Hacker News API skill returns a story, its full comment thread, a user's profile, or keyword search across the site — all at 1 credit, which makes it a good endpoint to smoke-test your key with.

This skill wraps **4 live Hacker News endpoints** from the [ScraperSocial](https://scrapersocial.com) API. Public data only, returned as clean JSON.

## When to use this skill

- A user pastes an HN link and wants the discussion summarised.
- You are researching how a product, company or idea was received by that audience.
- You want to track mentions of a term on Hacker News.

### Do not use this skill when

- **You need the whole firehose or historical bulk.** The official Firebase API and the Algolia HN search API are free and better suited to bulk work.
- **You need to post or vote.** Read-only.

## Setup

```bash
export SCRAPERSOCIAL_KEY=sk_live_...   # https://scrapersocial.com/app/keys
```

Signing up at [scrapersocial.com/signup](https://scrapersocial.com/signup) includes 100 free credits, no card required.

## Permissions and scope

These scripts do exactly three things and nothing else: read one environment variable (`SCRAPERSOCIAL_KEY`), send HTTPS requests to `https://api.scrapersocial.com` (the host is a constant in the code, not configurable), and print JSON. They run as `node scripts/<name>.js` with no other shell use, no file writes and no persistence. `call_endpoint.js` accepts only the 4 documented `/v1/hackernews/` paths in the table below and refuses anything else before a request is made.

## Scripts

| Script | What it does | Input | Credits |
|---|---|---|---|
| `get_profile.js` | Get Hacker News profile. | handle | 1 credit |
| `search.js` | List Hacker News search. | query | 1 credit per story |
| `get_story.js` | Get Hacker News story. | handle | 1 credit |
| `get_story_comments.js` | List Hacker News story comments. | handle | 1 credit per comment |
| `call_endpoint.js` | Call any `/v1/hackernews/` endpoint directly | path + params | varies |

Every script also accepts `--limit`, `--cursor`, `--fields`, `--format` and `--fresh`. `--limit` is clamped to 50: above that the API returns an async job instead of data.

## Example

```bash
node skills/hacker-news-api/scripts/get_profile.js pg
```

Every response uses the same envelope:

```json
{ "data": {}, "meta": { "count": 20, "next_cursor": "..." }, "request_id": "a18e4ef88ad4b00b" }
```

`meta` appears on paginated endpoints only. Keep `request_id` — support traces calls with it.

## Endpoints

| Endpoint | Input | Returns | Credits | Paginated |
|---|---|---|---|---|
| `/v1/hackernews/profile` | handle | profile | 1 credit | no |
| `/v1/hackernews/search` | query | story | 1 credit per story | yes |
| `/v1/hackernews/story` | handle | story | 1 credit | no |
| `/v1/hackernews/story-comments` | handle | comment | 1 credit per comment | yes |

Costs shown per item for paginated endpoints, per call otherwise. Failed calls are not charged.

## FAQ

### How do I get the comments on a Hacker News story?

`get_story_comments.js` with the story handle returns the thread at 1 credit per comment. `get_story.js` returns the story itself.

### Why use this instead of the free official HN API?

Only for consistency with the other platforms here — same envelope, same client, same key. If HN is your only source, the official API is free.

### Is this an official Hacker News API?

No. ScraperSocial is independent and not affiliated with Hacker News or Y Combinator.

## Links

- [Hacker News data on ScraperSocial](https://scrapersocial.com)
- [All 33 platform skills](https://github.com/nikhonit/social-media-api-skills)
- [OpenAPI spec](https://scrapersocial.com/openapi.json) · [llms.txt](https://scrapersocial.com/llms.txt)

## Disclaimer

ScraperSocial is an independent product and is not affiliated with, endorsed by, or sponsored by any platform named in this repository. All product names, logos and brands are property of their respective owners. These skills return only publicly available data.
