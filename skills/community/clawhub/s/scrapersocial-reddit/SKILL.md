---
name: reddit-api
version: 1.0.4
description: Reddit data toolkit via ScraperSocial — posts, full comment threads, subreddit listings and details, user profiles and keyword search.
license: MIT-0
author: ScraperSocial
homepage: https://scrapersocial.com
repository: https://github.com/nikhonit/social-media-api-skills
tags:
  - reddit
  - subreddit
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

# Reddit API skill

Read public Reddit data as clean JSON. This Reddit API skill returns a post and its full comment tree, subreddit listings and metadata, user profiles and their post history, plus keyword search across posts and subreddits. Reddit is where people say what they actually think about a product, which makes it the highest-signal source in this repo for sentiment and research work.

This skill wraps **8 live Reddit endpoints** from the [ScraperSocial](https://scrapersocial.com) API. Public data only, returned as clean JSON.

## When to use this skill

- A user pastes a Reddit thread and asks what the discussion concluded.
- You are researching how a product, company or topic is talked about by real users.
- You are monitoring a subreddit for mentions of a brand.
- You want to find the right subreddits for a topic.

### Do not use this skill when

- **You need to post, comment or vote.** Read-only. Reddit's own API handles writes.
- **You are pulling a large subreddit's full history.** Listings are charged per item; scope with `--limit` and page deliberately.
- **You need private or quarantined content**, or removed comments. Public data only.
- **A Reddit link appears in passing** with no question attached.

## Setup

```bash
export SCRAPERSOCIAL_KEY=sk_live_...   # https://scrapersocial.com/app/keys
```

Signing up at [scrapersocial.com/signup](https://scrapersocial.com/signup) includes 100 free credits, no card required.

## Permissions and scope

These scripts do exactly three things and nothing else: read one environment variable (`SCRAPERSOCIAL_KEY`), send HTTPS requests to `https://api.scrapersocial.com` (the host is a constant in the code, not configurable), and print JSON. They run as `node scripts/<name>.js` with no other shell use, no file writes and no persistence. `call_endpoint.js` accepts only the 8 documented `/v1/reddit/` paths in the table below and refuses anything else before a request is made.

## Scripts

| Script | What it does | Input | Credits |
|---|---|---|---|
| `get_post.js` | Get Reddit post. | url | 4 credits |
| `get_post_comments.js` | List Reddit post comments. | url | 2 credits per comment |
| `search.js` | List Reddit search. | query | 2 credits per result |
| `get_subreddit.js` | List Reddit subreddit. | handle | 2 credits per post |
| `get_subreddit_details.js` | Get Reddit subreddit details. | handle | 4 credits |
| `subreddit_search.js` | List Reddit subreddit search. | query | 2 credits per result |
| `get_user.js` | Get Reddit user. | handle | 4 credits |
| `get_user_posts.js` | List Reddit user posts. | handle | 2 credits per post |
| `call_endpoint.js` | Call any `/v1/reddit/` endpoint directly | path + params | varies |

Every script also accepts `--limit`, `--cursor`, `--fields`, `--format` and `--fresh`. `--limit` is clamped to 50: above that the API returns an async job instead of data.

## Example

```bash
node skills/reddit-api/scripts/search.js "mechanical keyboards"
```

Every response uses the same envelope:

```json
{ "data": {}, "meta": { "count": 20, "next_cursor": "..." }, "request_id": "a18e4ef88ad4b00b" }
```

`meta` appears on paginated endpoints only. Keep `request_id` — support traces calls with it.

## Endpoints

| Endpoint | Input | Returns | Credits | Paginated |
|---|---|---|---|---|
| `/v1/reddit/post` | url | post | 4 credits | no |
| `/v1/reddit/post-comments` | url | comment | 2 credits per comment | yes |
| `/v1/reddit/search` | query | result | 2 credits per result | yes |
| `/v1/reddit/subreddit` | handle | post | 2 credits per post | yes |
| `/v1/reddit/subreddit-details` | handle | subreddit | 4 credits | no |
| `/v1/reddit/subreddit-search` | query | result | 2 credits per result | yes |
| `/v1/reddit/user` | handle | profile | 4 credits | no |
| `/v1/reddit/user-posts` | handle | post | 2 credits per post | yes |

Costs shown per item for paginated endpoints, per call otherwise. Failed calls are not charged.

## FAQ

### How do I get the comments on a Reddit post?

`get_post_comments.js` with the post URL returns the thread at 2 credits per comment. `get_post.js` returns the post itself for 4.

### How do I monitor a subreddit?

`get_subreddit.js` with the subreddit handle lists posts at 2 credits each. `get_subreddit_details.js` returns the subreddit's own metadata for 4.

### How do I find subreddits about a topic?

`subreddit_search.js` with a query. For post-level search across Reddit, use `search.js`.

### Is this an official Reddit API?

No. ScraperSocial is independent and not affiliated with Reddit. It returns publicly available data only. Reddit's own API remains the sanctioned route, particularly for writes.

## Links

- [Reddit data on ScraperSocial](https://scrapersocial.com)
- [All 33 platform skills](https://github.com/nikhonit/social-media-api-skills)
- [OpenAPI spec](https://scrapersocial.com/openapi.json) · [llms.txt](https://scrapersocial.com/llms.txt)

## Disclaimer

ScraperSocial is an independent product and is not affiliated with, endorsed by, or sponsored by any platform named in this repository. All product names, logos and brands are property of their respective owners. These skills return only publicly available data.
