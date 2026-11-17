---
name: instagram-api
version: 1.0.4
description: Instagram data toolkit via ScraperSocial — reel transcripts, AI summaries, profile and post stats, comments, hashtag and location analytics, keyword search.
license: MIT-0
author: ScraperSocial
homepage: https://scrapersocial.com
repository: https://github.com/nikhonit/social-media-api-skills
tags:
  - instagram
  - reels
  - transcript
  - hashtags
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

# Instagram API skill

Read public Instagram data as clean JSON. This Instagram API skill transcribes reels, summarises them, returns profile and post statistics, walks comment threads, and analyses hashtags and locations — including post counts, top posts and reels for a tag or place. It also covers keyword, profile and reel search.

Instagram is one of the harder platforms to read programmatically. These endpoints return structured JSON without a logged-in session or a browser farm.

This skill wraps **23 live Instagram endpoints** from the [ScraperSocial](https://scrapersocial.com) API. Public data only, returned as clean JSON.

## When to use this skill

- A user pastes a reel URL and asks what is said in it, or wants it summarised.
- You are researching a creator or brand account: followers, posting pattern, engagement.
- You need comments on a post for sentiment or FAQ mining.
- You are tracking a hashtag or a location and want its stats and top posts.

### Do not use this skill when

- **Watch the price on media endpoints.** `get_transcript.js` and `get_download.js` cost 40 credits, and `--section=summary` costs 42 — the most expensive calls in the API. Never fire them speculatively; confirm the user actually wants the video's content first.
- **An Instagram link appears in passing** with no question attached.
- **You need private accounts, stories from private users, or DMs.** Public data only.
- **You run the account yourself.** Meta's Graph API gives owners richer insights for free.
- **You need to post, comment or follow.** Read-only.

## Setup

```bash
export SCRAPERSOCIAL_KEY=sk_live_...   # https://scrapersocial.com/app/keys
```

Signing up at [scrapersocial.com/signup](https://scrapersocial.com/signup) includes 100 free credits, no card required.

## Permissions and scope

These scripts do exactly three things and nothing else: read one environment variable (`SCRAPERSOCIAL_KEY`), send HTTPS requests to `https://api.scrapersocial.com` (the host is a constant in the code, not configurable), and print JSON. They run as `node scripts/<name>.js` with no other shell use, no file writes and no persistence. `call_endpoint.js` accepts only the 23 documented `/v1/instagram/` paths in the table below and refuses anything else before a request is made.

## Scripts

| Script | What it does | Input | Credits |
|---|---|---|---|
| `get_profile.js` `--section=about` | Get Instagram profile about. | handle | 3 credits |
| `get_profile.js` `--section=full` | Get Instagram profile full. | handle | 3 credits |
| `get_profile.js` `--section=search` | List Instagram profile search. | query | 2 credits per profile |
| `get_profile.js` `--section=similar` | Get Instagram similar. | handle | 2 credits |
| `get_profile.js` `--section=tagged` | List Instagram tagged. | handle | 2 credits per post |
| `get_channel.js` `--section=posts` | Latest posts from an Instagram account with per-post metrics. | handle | 2 credits per post |
| `get_channel.js` `--section=reels` | Latest reels from an Instagram account with per-reel metrics. | handle | 3 credits per reel |
| `get_channel.js` `--section=stats` | Follower counts, bio and profile metadata for an Instagram account. | handle | 3 credits |
| `get_hashtag.js` `--section=analytics` | Get Instagram hashtag analytics. | query | 3 credits |
| `get_hashtag.js` `--section=posts` | List Instagram hashtag posts. | query | 2 credits per post |
| `get_hashtag.js` `--section=reels` | List Instagram hashtag reels. | query | 2 credits per reel |
| `get_hashtag.js` `--section=search` | List Instagram hashtag search. | query | 2 credits per hashtag |
| `get_hashtag.js` `--section=stats` | Get Instagram hashtag stats. | query | 2 credits |
| `get_location.js` `--section=posts` | List Instagram location posts. | query | 2 credits per post |
| `get_location.js` `--section=search` | List Instagram location search. | query | 2 credits per place |
| `get_location.js` `--section=stats` | Get Instagram location stats. | query | 2 credits |
| `search.js` `--section=keyword-search` | List Instagram keyword search. | query | 2 credits per result |
| `search.js` `--section=reels-search` | Keyword search over Instagram reels. | query | 3 credits per result |
| `get_comments.js` | Paginated comments on an Instagram post; charged per comment returned. | url | 3 credits per comment |
| `get_transcript.js` | Full transcript of an Instagram reel with timestamped segments. | url | 40 credits |
| `get_transcript.js` `--section=summary` | Short AI summary of an Instagram reel, built on its transcript. | url | 42 credits |
| `get_download.js` | Resolves a downloadable media URL for an Instagram reel (URL expires within 1h). | url | 40 credits |
| `get_stats.js` | Likes, comments and view counts for an Instagram post or reel. | url | 1 credit |
| `call_endpoint.js` | Call any `/v1/instagram/` endpoint directly | path + params | varies |

Every script also accepts `--limit`, `--cursor`, `--fields`, `--format` and `--fresh`. `--limit` is clamped to 50: above that the API returns an async job instead of data.

## Example

```bash
node skills/instagram-api/scripts/get_hashtag.js latteart --section=posts
```

Every response uses the same envelope:

```json
{ "data": {}, "meta": { "count": 20, "next_cursor": "..." }, "request_id": "a18e4ef88ad4b00b" }
```

`meta` appears on paginated endpoints only. Keep `request_id` — support traces calls with it.

## Endpoints

| Endpoint | Input | Returns | Credits | Paginated |
|---|---|---|---|---|
| `/v1/instagram/channel-posts` | handle | post | 2 credits per post | yes |
| `/v1/instagram/channel-reels` | handle | reel | 3 credits per reel | yes |
| `/v1/instagram/channel-stats` | handle | profile | 3 credits | no |
| `/v1/instagram/comments` | url | comment | 3 credits per comment | yes |
| `/v1/instagram/download` | url | video | 40 credits | no |
| `/v1/instagram/hashtag-analytics` | query | hashtag | 3 credits | no |
| `/v1/instagram/hashtag-posts` | query | post | 2 credits per post | yes |
| `/v1/instagram/hashtag-reels` | query | reel | 2 credits per reel | yes |
| `/v1/instagram/hashtag-search` | query | hashtag | 2 credits per hashtag | yes |
| `/v1/instagram/hashtag-stats` | query | hashtag | 2 credits | no |
| `/v1/instagram/keyword-search` | query | result | 2 credits per result | yes |
| `/v1/instagram/location-posts` | query | post | 2 credits per post | yes |
| `/v1/instagram/location-search` | query | place | 2 credits per place | yes |
| `/v1/instagram/location-stats` | query | place | 2 credits | no |
| `/v1/instagram/profile-about` | handle | profile | 3 credits | no |
| `/v1/instagram/profile-full` | handle | profile | 3 credits | no |
| `/v1/instagram/profile-search` | query | profile | 2 credits per profile | yes |
| `/v1/instagram/reels-search` | query | result | 3 credits per result | yes |
| `/v1/instagram/similar` | handle | profile | 2 credits | no |
| `/v1/instagram/stats` | url | post | 1 credit | no |
| `/v1/instagram/summary` | url | reel | 42 credits | no |
| `/v1/instagram/tagged` | handle | post | 2 credits per post | yes |
| `/v1/instagram/transcript` | url | reel | 40 credits | no |

Costs shown per item for paginated endpoints, per call otherwise. Failed calls are not charged.

## FAQ

### How do I transcribe an Instagram reel?

`get_transcript.js` with the reel URL, 40 credits. `--section=summary` returns an AI summary instead, for 42. Both read the video directly. These are the priciest calls here — check before spending.

### How do I get an Instagram profile as JSON?

`get_profile.js --section=full` returns the full profile, `--section=about` a lighter version. This script has no default section, so `--section` is required.

### Can I get hashtag statistics?

Yes. `get_hashtag.js --section=stats` returns counts, `--section=analytics` a richer breakdown, and `--section=posts` or `--section=reels` the content ranked under the tag.

### Why does a post return 404?

It is private, deleted, or from an account that blocks public reads. The API returns `not_found` rather than guessing, and failed calls are not charged.

### Is this an official Instagram API?

No. ScraperSocial is independent and not affiliated with Meta. It returns publicly available data only.

## Links

- [Instagram data on ScraperSocial](https://scrapersocial.com)
- [All 33 platform skills](https://github.com/nikhonit/social-media-api-skills)
- [OpenAPI spec](https://scrapersocial.com/openapi.json) · [llms.txt](https://scrapersocial.com/llms.txt)

## Disclaimer

ScraperSocial is an independent product and is not affiliated with, endorsed by, or sponsored by any platform named in this repository. All product names, logos and brands are property of their respective owners. These skills return only publicly available data.
