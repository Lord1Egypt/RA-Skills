---
name: tiktok-api
version: 1.0.4
description: TikTok data toolkit via ScraperSocial — video transcripts, AI summaries, post and channel stats, comments, follower lists, song lookups, keyword and hashtag search.
license: MIT-0
author: ScraperSocial
homepage: https://scrapersocial.com
repository: https://github.com/nikhonit/social-media-api-skills
tags:
  - tiktok
  - transcript
  - hashtags
  - creator-analytics
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

# TikTok API skill

Read public TikTok data as clean JSON. This TikTok API skill turns a video URL into a full transcript or an AI summary, pulls engagement stats for any post or creator, walks comment threads, lists follower and following graphs, and searches TikTok by keyword, hashtag, user or song — without a headless browser, a login, or a scraping stack to maintain.

The transcript endpoint is the one most people come for: give it a video URL and it returns the spoken words, which is what makes TikTok content searchable, summarisable and usable as model input.

This skill wraps **16 live TikTok endpoints** from the [ScraperSocial](https://scrapersocial.com) API. Public data only, returned as clean JSON.

## When to use this skill

- A user gives you a TikTok video URL and asks what is said in it, or asks for a summary.
- You are researching a creator: follower counts, posting cadence, which videos performed.
- You need the comments on a video, for sentiment or for finding recurring questions.
- You are tracking a hashtag, a trend or a sound and want the videos ranked under it.
- You want to find creators or videos by keyword rather than by URL.

### Do not use this skill when

- **A TikTok link appears in passing** and the user has not asked anything about it. Every call spends credits — a mention is not a request.
- **The user asks something answerable from the page they already pasted.** If they pasted the caption and want it rephrased, no API call is needed.
- **You need private data**: non-public accounts, DMs, analytics only the account owner sees, or anything behind a login. The API returns public data only and will 404 rather than guess.
- **You need to post, comment, follow or upload.** This is read-only.
- **You need a guaranteed-complete follower list for a large account.** Follower endpoints are paginated and charged per item; pulling millions of rows is slow and expensive. Sample, or ask the user first.

## Setup

```bash
export SCRAPERSOCIAL_KEY=sk_live_...   # https://scrapersocial.com/app/keys
```

Signing up at [scrapersocial.com/signup](https://scrapersocial.com/signup) includes 100 free credits, no card required.

## Permissions and scope

These scripts do exactly three things and nothing else: read one environment variable (`SCRAPERSOCIAL_KEY`), send HTTPS requests to `https://api.scrapersocial.com` (the host is a constant in the code, not configurable), and print JSON. They run as `node scripts/<name>.js` with no other shell use, no file writes and no persistence. `call_endpoint.js` accepts only the 16 documented `/v1/tiktok/` paths in the table below and refuses anything else before a request is made.

## Scripts

| Script | What it does | Input | Credits |
|---|---|---|---|
| `get_channel.js` `--section=reposts` | List TikTok channel reposts. | handle | 3 credits per video |
| `get_channel.js` `--section=stats` | Follower counts and profile metadata for a TikTok account. | handle | 3 credits |
| `get_channel.js` `--section=top-videos` | List TikTok channel top videos. | handle | 3 credits per video |
| `get_channel.js` `--section=videos` | Latest videos from a TikTok account with per-video metrics. | handle | 3 credits per video |
| `get_audience.js` `--section=followers` | List TikTok followers. | handle | 3 credits per profile |
| `get_audience.js` `--section=following` | List TikTok following. | handle | 3 credits per profile |
| `search.js` | Keyword search over TikTok videos. | query | 4 credits per result |
| `search.js` `--section=hashtag-search` | Videos posted under a TikTok hashtag. | query | 3 credits per result |
| `search.js` `--section=top-search` | List TikTok top search. | query | 4 credits per result |
| `search.js` `--section=user-search` | List TikTok user search. | query | 3 credits per profile |
| `get_song.js` | Get TikTok song. | url | 3 credits |
| `get_song.js` `--section=videos` | List TikTok song videos. | url | 3 credits per video |
| `get_transcript.js` | Full transcript of a TikTok video with timestamped segments. | url | 8 credits |
| `get_transcript.js` `--section=summary` | Short AI summary of a TikTok video, built on its transcript. | url | 10 credits |
| `get_comments.js` | Paginated comments on a TikTok video; charged per comment returned. | url | 2 credits per comment |
| `get_stats.js` | Views, likes, comments and shares for a single TikTok video. | url | 3 credits |
| `call_endpoint.js` | Call any `/v1/tiktok/` endpoint directly | path + params | varies |

Every script also accepts `--limit`, `--cursor`, `--fields`, `--format` and `--fresh`. `--limit` is clamped to 50: above that the API returns an async job instead of data.

## Example

```bash
node skills/tiktok-api/scripts/search.js "sourdough starter"
```

Every response uses the same envelope:

```json
{ "data": {}, "meta": { "count": 20, "next_cursor": "..." }, "request_id": "a18e4ef88ad4b00b" }
```

`meta` appears on paginated endpoints only. Keep `request_id` — support traces calls with it.

## Endpoints

| Endpoint | Input | Returns | Credits | Paginated |
|---|---|---|---|---|
| `/v1/tiktok/channel-reposts` | handle | video | 3 credits per video | yes |
| `/v1/tiktok/channel-stats` | handle | profile | 3 credits | no |
| `/v1/tiktok/channel-top-videos` | handle | video | 3 credits per video | yes |
| `/v1/tiktok/channel-videos` | handle | video | 3 credits per video | yes |
| `/v1/tiktok/comments` | url | comment | 2 credits per comment | yes |
| `/v1/tiktok/followers` | handle | profile | 3 credits per profile | yes |
| `/v1/tiktok/following` | handle | profile | 3 credits per profile | yes |
| `/v1/tiktok/hashtag-search` | query | result | 3 credits per result | yes |
| `/v1/tiktok/search` | query | result | 4 credits per result | yes |
| `/v1/tiktok/song` | url | song | 3 credits | no |
| `/v1/tiktok/song-videos` | url | video | 3 credits per video | yes |
| `/v1/tiktok/stats` | url | video | 3 credits | no |
| `/v1/tiktok/summary` | url | video | 10 credits | no |
| `/v1/tiktok/top-search` | query | result | 4 credits per result | yes |
| `/v1/tiktok/transcript` | url | video | 8 credits | no |
| `/v1/tiktok/user-search` | query | profile | 3 credits per profile | yes |

Costs shown per item for paginated endpoints, per call otherwise. Failed calls are not charged.

## FAQ

### How do I get a TikTok transcript from a URL?

Run `get_transcript.js` with the video URL. It returns the spoken content as text, 8 credits per video. Videos with no speech return an empty transcript rather than an error.

### What is the difference between transcript and summary?

`--section` on the same script: the default returns the raw transcript, `--section=summary` returns an AI-written summary of the video. Summary costs 10 credits and reads the video itself, so you do not need to fetch the transcript first.

### Can I search TikTok without a video URL?

Yes. `search.js` covers keyword search, `--section=top-search` for top results, `--section=hashtag-search` for a hashtag, and `--section=user-search` for creators.

### Is this an official TikTok API?

No. ScraperSocial is independent and not affiliated with TikTok. It returns publicly available data only. For posting, ad management or owned-account analytics, use TikTok's own developer platform.

### What does it cost?

Between 2 and 10 credits depending on the endpoint — the table above lists each one. Signup includes 100 free credits with no card, which is enough to try every endpoint here.

## Links

- [TikTok data on ScraperSocial](https://scrapersocial.com)
- [All 33 platform skills](https://github.com/nikhonit/social-media-api-skills)
- [OpenAPI spec](https://scrapersocial.com/openapi.json) · [llms.txt](https://scrapersocial.com/llms.txt)

## Disclaimer

ScraperSocial is an independent product and is not affiliated with, endorsed by, or sponsored by any platform named in this repository. All product names, logos and brands are property of their respective owners. These skills return only publicly available data.
