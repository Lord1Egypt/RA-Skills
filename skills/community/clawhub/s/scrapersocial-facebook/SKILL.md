---
name: facebook-api
version: 1.0.4
description: Facebook data toolkit via ScraperSocial — video transcripts, AI summaries, post and page stats, comments, reels, ads, marketplace, events, groups and reviews.
license: MIT-0
author: ScraperSocial
homepage: https://scrapersocial.com
repository: https://github.com/nikhonit/social-media-api-skills
tags:
  - facebook
  - transcript
  - ads
  - marketplace
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

# Facebook API skill

Read public Facebook data as clean JSON. This Facebook API skill is the broadest surface in the repo after LinkedIn: video transcripts and AI summaries, post and page statistics, comment threads and replies, reels and photos, the ad library, Marketplace listings, events, group posts, follower graphs and page reviews.

If you have tried to get this data yourself, you know the problem — Facebook is aggressive about blocking automated reads. These endpoints return structured JSON without a browser, a session cookie or a proxy pool.

This skill wraps **23 live Facebook endpoints** from the [ScraperSocial](https://scrapersocial.com) API. Public data only, returned as clean JSON.

## When to use this skill

- A user pastes a Facebook video URL and wants a transcript or a summary of it.
- You are researching a page: follower counts, engagement, what it posts, what people say in reviews.
- You need comment threads on a post, including replies, for sentiment analysis.
- You are doing competitive ad research through the ad library.
- You are monitoring Marketplace listings or public events for a keyword.

### Do not use this skill when

- **A Facebook link appears in passing** with no question attached. Transcript and summary are among the priciest calls in the API (15 and 17 credits) — do not fire them speculatively.
- **You need private data**: friends-only posts, private groups, DMs, or Page Insights that only admins see. Public data only.
- **You manage the page yourself.** Meta's Graph API gives owners richer data for free.
- **You need to post, comment or reply.** Read-only.
- **The user only wants the caption they already pasted.** No call needed.

## Setup

```bash
export SCRAPERSOCIAL_KEY=sk_live_...   # https://scrapersocial.com/app/keys
```

Signing up at [scrapersocial.com/signup](https://scrapersocial.com/signup) includes 100 free credits, no card required.

## Permissions and scope

These scripts do exactly three things and nothing else: read one environment variable (`SCRAPERSOCIAL_KEY`), send HTTPS requests to `https://api.scrapersocial.com` (the host is a constant in the code, not configurable), and print JSON. They run as `node scripts/<name>.js` with no other shell use, no file writes and no persistence. `call_endpoint.js` accepts only the 23 documented `/v1/facebook/` paths in the table below and refuses anything else before a request is made.

## Scripts

| Script | What it does | Input | Credits |
|---|---|---|---|
| `get_stats.js` | Reactions, comments and shares for a Facebook post or video. | url | 5 credits |
| `get_stats.js` `--section=page-stats` | Followers, likes and metadata for a Facebook page. | url|handle | 10 credits |
| `get_transcript.js` | Full transcript of a Facebook video with timestamped segments. | url | 15 credits |
| `get_transcript.js` `--section=summary` | Short AI summary of a Facebook video, built on its transcript. | url | 17 credits |
| `get_comments.js` | Paginated comments on a Facebook post; charged per comment returned. | url | 3 credits per comment |
| `get_comments.js` `--section=comment-replies` | List Facebook comment replies. | url | 3 credits per reply |
| `get_posts.js` `--section=channel-posts` | Latest posts from a Facebook page with per-post metrics. | url|handle | 3 credits per post |
| `get_posts.js` `--section=group-posts` | List Facebook group posts. | url|handle | 3 credits per post |
| `get_posts.js` `--section=photos` | List Facebook photos. | url|handle | 3 credits per photo |
| `get_posts.js` `--section=reels` | List Facebook reels. | url|handle | 3 credits per reel |
| `get_audience.js` `--section=followers` | List Facebook followers. | url|handle | 3 credits per profile |
| `get_audience.js` `--section=following` | List Facebook following. | url|handle | 3 credits per profile |
| `get_page.js` `--section=ads` | List Facebook page ads. | url|handle | 4 credits per ad |
| `get_page.js` `--section=events` | List Facebook page events. | url|handle | 3 credits per event |
| `get_page.js` `--section=search` | List Facebook page search. | query | 4 credits per page |
| `get_ads.js` `--section=ad` | Get Facebook ad. | url | 5 credits |
| `get_ads.js` `--section=search` | List Facebook ads search. | query | 4 credits per ad |
| `get_marketplace.js` `--section=item` | Get Facebook marketplace item. | url | 3 credits |
| `get_marketplace.js` `--section=search` | List Facebook marketplace search. | query | 3 credits per listing |
| `get_events.js` `--section=event` | Get Facebook event. | url | 3 credits |
| `get_events.js` `--section=search` | List Facebook events search. | query | 3 credits per event |
| `get_reviews.js` | List Facebook reviews. | url|handle | 3 credits per review |
| `get_download.js` | Resolves a downloadable media URL for a Facebook video (URL expires within 1h). | url | 10 credits |
| `call_endpoint.js` | Call any `/v1/facebook/` endpoint directly | path + params | varies |

Every script also accepts `--limit`, `--cursor`, `--fields`, `--format` and `--fresh`. `--limit` is clamped to 50: above that the API returns an async job instead of data.

## Example

```bash
node skills/facebook-api/scripts/get_page.js "specialty coffee roasters" --section=search
```

Every response uses the same envelope:

```json
{ "data": {}, "meta": { "count": 20, "next_cursor": "..." }, "request_id": "a18e4ef88ad4b00b" }
```

`meta` appears on paginated endpoints only. Keep `request_id` — support traces calls with it.

## Endpoints

| Endpoint | Input | Returns | Credits | Paginated |
|---|---|---|---|---|
| `/v1/facebook/ad` | url | ad | 5 credits | no |
| `/v1/facebook/ads-search` | query | ad | 4 credits per ad | yes |
| `/v1/facebook/channel-posts` | url|handle | post | 3 credits per post | yes |
| `/v1/facebook/comment-replies` | url | reply | 3 credits per reply | yes |
| `/v1/facebook/comments` | url | comment | 3 credits per comment | yes |
| `/v1/facebook/download` | url | video | 10 credits | no |
| `/v1/facebook/event` | url | event | 3 credits | no |
| `/v1/facebook/events-search` | query | event | 3 credits per event | yes |
| `/v1/facebook/followers` | url|handle | profile | 3 credits per profile | yes |
| `/v1/facebook/following` | url|handle | profile | 3 credits per profile | yes |
| `/v1/facebook/group-posts` | url|handle | post | 3 credits per post | yes |
| `/v1/facebook/marketplace-item` | url | listing | 3 credits | no |
| `/v1/facebook/marketplace-search` | query | listing | 3 credits per listing | yes |
| `/v1/facebook/page-ads` | url|handle | ad | 4 credits per ad | yes |
| `/v1/facebook/page-events` | url|handle | event | 3 credits per event | yes |
| `/v1/facebook/page-search` | query | page | 4 credits per page | yes |
| `/v1/facebook/page-stats` | url|handle | page | 10 credits | no |
| `/v1/facebook/photos` | url|handle | photo | 3 credits per photo | yes |
| `/v1/facebook/reels` | url|handle | reel | 3 credits per reel | yes |
| `/v1/facebook/reviews` | url|handle | review | 3 credits per review | yes |
| `/v1/facebook/stats` | url | post | 5 credits | no |
| `/v1/facebook/summary` | url | video | 17 credits | no |
| `/v1/facebook/transcript` | url | video | 15 credits | no |

Costs shown per item for paginated endpoints, per call otherwise. Failed calls are not charged.

## FAQ

### How do I transcribe a Facebook video?

`get_transcript.js` with the video URL returns the spoken content for 15 credits. `--section=summary` returns an AI summary instead, for 17 credits — it reads the video directly, so you do not need the transcript first.

### Can I get Facebook page statistics?

Yes. `get_stats.js --section=page-stats` returns page-level metrics for 10 credits. Plain `get_stats.js` returns post-level stats for a single post URL, for 5.

### Does this cover the Facebook ad library?

Yes. `get_ads.js --section=search` searches the ad library by keyword, `get_ads.js --section=ad` fetches a single ad by URL, and `get_page.js --section=ads` lists the ads running for a given page. This script has no default section, so `--section` is required.

### Is this an official Facebook or Meta API?

No. ScraperSocial is independent and not affiliated with Meta. It returns publicly available data only. If you administer the page, Meta's Graph API is the better and cheaper route.

### Why did I get a 404 for a post that exists?

The post is private, deleted, or the URL is a redirect. The API returns `not_found` rather than guessing, and failed calls are not charged.

## Links

- [Facebook data on ScraperSocial](https://scrapersocial.com)
- [All 33 platform skills](https://github.com/nikhonit/social-media-api-skills)
- [OpenAPI spec](https://scrapersocial.com/openapi.json) · [llms.txt](https://scrapersocial.com/llms.txt)

## Disclaimer

ScraperSocial is an independent product and is not affiliated with, endorsed by, or sponsored by any platform named in this repository. All product names, logos and brands are property of their respective owners. These skills return only publicly available data.
