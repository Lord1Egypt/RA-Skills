---
name: twitter-api
version: 1.0.4
description: X (Twitter) data toolkit via ScraperSocial — video transcripts, AI summaries, post stats, profiles, user tweets, list tweets and keyword search.
license: MIT-0
author: ScraperSocial
homepage: https://scrapersocial.com
repository: https://github.com/nikhonit/social-media-api-skills
tags:
  - twitter
  - x
  - tweets
  - transcript
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

# X (Twitter) API skill

Read public X (formerly Twitter) data as clean JSON. This Twitter API skill returns post statistics, profiles, a user's tweets, the tweets in a list, keyword search — and, less commonly available, transcripts and AI summaries of the video attached to a post.

X's own API pricing pushed a lot of people off the platform's data entirely. These endpoints start at 1 credit, which makes ordinary reads viable again.

This skill wraps **7 live X (Twitter) endpoints** from the [ScraperSocial](https://scrapersocial.com) API. Public data only, returned as clean JSON.

## When to use this skill

- A user pastes a post URL and wants its engagement numbers or the video transcribed.
- You are tracking what an account posts, or monitoring a keyword.
- You are researching a profile's reach and posting pattern.
- You need the tweets from a curated list as a monitoring feed.

### Do not use this skill when

- **You need real-time streaming.** These are point queries, not a firehose.
- **You need to post, reply or DM.** Read-only.
- **You need protected accounts or deleted posts.** Public data only.
- **A link appears in passing** with no question attached — `get_transcript.js` at 7 credits and `get_summary.js` at 9 are not calls to make speculatively.

## Setup

```bash
export SCRAPERSOCIAL_KEY=sk_live_...   # https://scrapersocial.com/app/keys
```

Signing up at [scrapersocial.com/signup](https://scrapersocial.com/signup) includes 100 free credits, no card required.

## Permissions and scope

These scripts do exactly three things and nothing else: read one environment variable (`SCRAPERSOCIAL_KEY`), send HTTPS requests to `https://api.scrapersocial.com` (the host is a constant in the code, not configurable), and print JSON. They run as `node scripts/<name>.js` with no other shell use, no file writes and no persistence. `call_endpoint.js` accepts only the 7 documented `/v1/twitter/` paths in the table below and refuses anything else before a request is made.

## Scripts

| Script | What it does | Input | Credits |
|---|---|---|---|
| `get_list_tweets.js` | List X/Twitter list tweets. | url | 1 credit per tweet |
| `get_profile.js` | Follower counts, bio and profile metadata for an account on X. | handle | 5 credits |
| `search.js` | Keyword and advanced-search over public posts on X. | query | 2 credits per result |
| `get_stats.js` | Views, likes, reposts and replies for a single post on X. | url | 1 credit |
| `get_summary.js` | Short AI summary of a video posted on X, built on its transcript. | url | 9 credits |
| `get_transcript.js` | Full transcript of a video attached to a post on X. | url | 7 credits |
| `get_tweets.js` | Latest posts from an account on X with per-post metrics. | handle | 1 credit per tweet |
| `call_endpoint.js` | Call any `/v1/twitter/` endpoint directly | path + params | varies |

Every script also accepts `--limit`, `--cursor`, `--fields`, `--format` and `--fresh`. `--limit` is clamped to 50: above that the API returns an async job instead of data.

## Example

```bash
node skills/twitter-api/scripts/search.js "llm benchmarks"
```

Every response uses the same envelope:

```json
{ "data": {}, "meta": { "count": 20, "next_cursor": "..." }, "request_id": "a18e4ef88ad4b00b" }
```

`meta` appears on paginated endpoints only. Keep `request_id` — support traces calls with it.

## Endpoints

| Endpoint | Input | Returns | Credits | Paginated |
|---|---|---|---|---|
| `/v1/twitter/list-tweets` | url | tweet | 1 credit per tweet | yes |
| `/v1/twitter/profile` | handle | lookup | 5 credits | no |
| `/v1/twitter/search` | query | result | 2 credits per result | yes |
| `/v1/twitter/stats` | url | tweet | 1 credit | no |
| `/v1/twitter/summary` | url | video | 9 credits | no |
| `/v1/twitter/transcript` | url | video | 7 credits | no |
| `/v1/twitter/tweets` | handle | tweet | 1 credit per tweet | yes |

Costs shown per item for paginated endpoints, per call otherwise. Failed calls are not charged.

## FAQ

### How do I get tweet stats as JSON?

`get_stats.js` with the post URL, 1 credit. `get_profile.js` returns an account for 5.

### Can I transcribe the video in a post?

Yes. `get_transcript.js` with the post URL returns the spoken content for 7 credits; `get_summary.js` returns an AI summary for 9.

### How do I monitor a keyword on X?

`search.js` with a query, 2 credits per result. For a curated feed, `get_list_tweets.js` returns the tweets in a list at 1 credit each.

### How does this compare to X's official API?

X's own API is the sanctioned route and the only one that supports posting. This is a read-only alternative with per-call pricing and no monthly tier commitment.

### Is this an official X API?

No. ScraperSocial is independent and not affiliated with X Corp. It returns publicly available data only.

## Links

- [X (Twitter) data on ScraperSocial](https://scrapersocial.com)
- [All 33 platform skills](https://github.com/nikhonit/social-media-api-skills)
- [OpenAPI spec](https://scrapersocial.com/openapi.json) · [llms.txt](https://scrapersocial.com/llms.txt)

## Disclaimer

ScraperSocial is an independent product and is not affiliated with, endorsed by, or sponsored by any platform named in this repository. All product names, logos and brands are property of their respective owners. These skills return only publicly available data.
