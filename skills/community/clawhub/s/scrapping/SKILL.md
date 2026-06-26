---
name: scrapping
description: >
  Use this skill whenever a user wants to get, pull, grab, fetch, or look up public data from social media
  platforms — profiles, posts, videos, comments, followers, engagement stats, transcripts, trending content,
  hashtags, or creator info from TikTok, Instagram, YouTube, Twitter/X, LinkedIn, Facebook, Reddit, Threads,
  Bluesky, Pinterest, Snapchat, Twitch, Kick, Truth Social, or link-in-bio sites (Linktree, Komi, Pillar).
  Also covers ad library lookups (Meta, Google, LinkedIn, Reddit) and TikTok Shop data. Trigger even when
  users say "scrape", "monitor", "search", or "check" a platform. Do NOT trigger for building apps, using
  official platform SDKs/APIs (like PRAW, tweepy, YouTube Data API), analyzing local files, or creating
  dashboards — only when the user needs to retrieve data directly from a social platform.
metadata:
  openclaw:
    requires:
      env:
        - SCRAPECREATORS_API_KEY
      bins:
        - curl
        - jq
    primaryEnv: SCRAPECREATORS_API_KEY
---

# ScrapeCreators API

ScrapeCreators provides 100+ REST endpoints to scrape public data from 20+ social media platforms. One API key, one header, simple curl requests.

## Quick start

### Authentication

Every request needs a single header:

```
x-api-key: YOUR_API_KEY
```

Get your key at https://scrapecreators.com (100 free credits on signup, no card required).

Store the key in an environment variable so it stays out of scripts and doesn't end up in version control or chat history:

```bash
export SCRAPECREATORS_API_KEY="your-key-here"
```

### Your first request

```bash
curl -s -G "https://api.scrapecreators.com/v1/tiktok/profile" \
  --data-urlencode "handle=khaby.lame" \
  -H "x-api-key: $SCRAPECREATORS_API_KEY" | jq .
```

That's the whole pattern. Every endpoint works the same way: `GET` request, query parameters, one auth header.

## Base URL

```
https://api.scrapecreators.com
```

## How credits work

- Most endpoints: **1 request = 1 credit**
- A few specialized endpoints cost more (e.g., audience demographics = 26 credits)
- Credits never expire, no monthly commitment
- Most responses include a `credits_remaining` field
- Check credit costs per endpoint in the docs: https://docs.scrapecreators.com

## Common parameters

These work across most endpoints:

| Parameter | Description |
|-----------|-------------|
| `trim=true` | Returns a trimmed, smaller response — keeps context window manageable and saves tokens when you only need key fields like names, stats, and IDs |
| `cursor` | Pagination cursor returned in previous response — pass it to get the next page. Each page costs 1 credit, so only paginate if the user needs more results. Note: the v3 TikTok profile/videos endpoint uses `max_cursor` instead of `cursor` |
| `includeExtras=true` | Returns additional fields (like counts, descriptions) on YouTube endpoints — without this, channel-videos only returns titles and IDs |
| `sort_by` | Sort results — values depend on endpoint (e.g., `popular`, `relevance`, `total_impressions`, `recency`). Check the platform reference for valid values per endpoint, since passing an invalid value returns a 400 error |

## Pagination

Many endpoints return paginated results. The pattern is:

1. Make the first request without a cursor
2. The response includes a `cursor` (or `next_cursor` or `next_page_id`) field
3. Pass that value as `?cursor=...` in the next request
4. Repeat until cursor is null/empty

```bash
# First page
curl -s -G "https://api.scrapecreators.com/v3/tiktok/profile/videos" \
  --data-urlencode "handle=khaby.lame" \
  -H "x-api-key: $SCRAPECREATORS_API_KEY" | jq .

# Next page (using max_cursor from previous response)
curl -s -G "https://api.scrapecreators.com/v3/tiktok/profile/videos" \
  --data-urlencode "handle=khaby.lame" \
  --data-urlencode "max_cursor=CURSOR_VALUE" \
  -H "x-api-key: $SCRAPECREATORS_API_KEY" | jq .
```

Some v2 endpoints require manual pagination — check the platform reference for specifics.

## Supported platforms and endpoints

Each platform has its own reference file with full endpoint details. Read the relevant one based on the user's request.

| Platform | Reference file | Key endpoints |
|----------|---------------|---------------|
| TikTok | `references/tiktok.md` | Profile, videos, comments, search, trending, shop, songs, transcripts, live, followers/following, audience demographics |
| Instagram | `references/instagram.md` | Profile, posts, reels, comments, search reels, transcripts, story highlights, embed |
| YouTube | `references/youtube.md` | Video details, channel info, channel videos, shorts, search, transcripts |
| Twitter/X | `references/twitter.md` | Profile, community, community tweets |
| LinkedIn | `references/linkedin.md` | Person profile, company page, company posts, post details, ad library search, ad details |
| Facebook | `references/facebook.md` | Posts, comments, reels, ad library, transcripts, group posts, profile |
| Reddit | `references/reddit.md` | Profile, subreddit details/posts/search, post comments, search, ad library |
| Other platforms | `references/other-platforms.md` | Pinterest, Threads, Bluesky, Snapchat, Twitch, Kick, Truth Social, Google (ads + search), link-in-bio platforms (Linktree, Komi, Pillar, Linkbio, Linkme), Amazon Shop |

## Making requests: the pattern

Every call follows the same shape. Always use `-G` with `--data-urlencode` to safely pass query parameters — this prevents shell injection from user-provided values (handles, search queries, URLs) and properly encodes special characters:

```bash
curl -s -G "https://api.scrapecreators.com/v1/{platform}/{endpoint}" \
  --data-urlencode "param=value" \
  -H "x-api-key: $SCRAPECREATORS_API_KEY"
```

Pipe through `jq` to format the JSON, or through `jq '.some.field'` to extract specific data. Using `jq` is important because raw API responses are often large nested JSON — extracting just the fields the user needs makes the output readable and keeps your context window clean.

### Chaining requests

A common pattern is to fetch a profile first (to confirm the account exists and get IDs), then drill into their content:

```bash
# 1. Get profile
PROFILE=$(curl -s -G "https://api.scrapecreators.com/v1/tiktok/profile" \
  --data-urlencode "handle=creator_name" \
  -H "x-api-key: $SCRAPECREATORS_API_KEY")

# 2. Get their recent posts
POSTS=$(curl -s -G "https://api.scrapecreators.com/v3/tiktok/profile/videos" \
  --data-urlencode "handle=creator_name" \
  -H "x-api-key: $SCRAPECREATORS_API_KEY")

# 3. Get comments on a specific video (extract video ID from posts)
VIDEO_ID=$(echo "$POSTS" | jq -r '.aweme_list[0].aweme_id')
COMMENTS=$(curl -s -G "https://api.scrapecreators.com/v1/tiktok/video/comments" \
  --data-urlencode "video_id=$VIDEO_ID" \
  -H "x-api-key: $SCRAPECREATORS_API_KEY")
```

### Saving results

```bash
# Save raw JSON
curl -s -G "https://api.scrapecreators.com/v1/instagram/profile" \
  --data-urlencode "handle=natgeo" \
  -H "x-api-key: $SCRAPECREATORS_API_KEY" > natgeo_profile.json

# Save as CSV (extract specific fields with jq)
curl -s -G "https://api.scrapecreators.com/v3/tiktok/profile/videos" \
  --data-urlencode "handle=creator" \
  -H "x-api-key: $SCRAPECREATORS_API_KEY" \
  | jq -r '.aweme_list[] | [.aweme_id, .desc, .statistics.play_count, .statistics.digg_count] | @csv' \
  > creator_posts.csv
```

## Processing and analyzing scraped data

After fetching data, here are common analysis patterns:

### Extract key metrics
```bash
# Get engagement stats from a profile
curl -s -G "https://api.scrapecreators.com/v1/tiktok/profile" \
  --data-urlencode "handle=creator" \
  -H "x-api-key: $SCRAPECREATORS_API_KEY" \
  | jq '{followers: .statsV2.followerCount, following: .statsV2.followingCount, likes: .statsV2.heartCount}'
```

### Aggregate across posts
```bash
# Average engagement across recent posts
curl -s -G "https://api.scrapecreators.com/v3/tiktok/profile/videos" \
  --data-urlencode "handle=creator" \
  -H "x-api-key: $SCRAPECREATORS_API_KEY" \
  | jq '[.aweme_list[] | .statistics.digg_count] | (add / length)'
```

### Get video transcripts for content analysis
```bash
# Fetch transcript of a TikTok video
curl -s -G "https://api.scrapecreators.com/v1/tiktok/video/transcript" \
  --data-urlencode "video_id=VIDEO_ID" \
  -H "x-api-key: $SCRAPECREATORS_API_KEY" | jq -r '.data.transcript'
```

### Search and filter
```bash
# Find TikTok creators by niche with audience filters
curl -s -G "https://api.scrapecreators.com/v1/tiktok/creators/popular" \
  --data-urlencode "min_followers=100000" \
  --data-urlencode "audience_country=US" \
  -H "x-api-key: $SCRAPECREATORS_API_KEY" | jq '.data'
```

## Important notes

- **Public data only** — the API scrapes publicly available information. No private accounts or DMs.
- **No rate limits** — run as many concurrent requests as needed.
- **29-second timeout** — requests that take longer will time out (AWS Lambda limit). Most complete in ~3 seconds.
- **AI transcript limit** — videos over 2 minutes that need AI-generated transcripts won't return transcripts. YouTube transcripts have their own dedicated endpoint and are unaffected.
- **Versioned endpoints** — some endpoints have moved beyond v1: TikTok profile videos is now v3 (uses `max_cursor` instead of `cursor`), TikTok video info is v2, Instagram user posts / reels search / post comments are v2. Check the platform reference files for current versions.
- **Response format** — all responses are JSON. Use `trim=true` to reduce payload size when you only need key fields.

## Error handling

If a request fails:
1. Check the HTTP status code
2. The response body usually contains an error message
3. Common issues: invalid API key (401), endpoint not found (404), timeout on slow requests (502/503)

```bash
# Check status code
curl -s -G -o response.json -w "%{http_code}" \
  "https://api.scrapecreators.com/v1/tiktok/profile" \
  --data-urlencode "handle=creator" \
  -H "x-api-key: $SCRAPECREATORS_API_KEY"
```

## Choosing the right endpoint

When the user describes what they need, match it to the right platform and endpoint:

- **"Get info about a creator/account"** → `/{platform}/profile`
- **"Get their posts/videos/content"** → `/{platform}/profile/videos` (TikTok) or `/{platform}/channel-videos` (YouTube) or `/{platform}/user/posts` (Instagram) or `/{platform}/posts` (Facebook)
- **"Get comments on a post"** → `/{platform}/video/comments` or `/{platform}/post/comments`
- **"Search for content about X"** → `/{platform}/search/keyword` (TikTok) or `/{platform}/search` (others)
- **"Get the transcript of a video"** → `/{platform}/video/transcript` (TikTok/YouTube) or `/v2/instagram/media/transcript` (Instagram) or `/facebook/transcript` (Facebook)
- **"Who follows them / who do they follow"** → `/{platform}/user/followers` or `/following`
- **"What's trending"** → `/tiktok/videos/popular`, `/tiktok/get-trending-feed`, `/tiktok/hashtags/popular`
- **"Find ads by a company"** → `/facebook/adLibrary/search/ads`, `/linkedin/ads/search`, `/google/company/ads`, or `/reddit/ads/search`
- **"Get product details from TikTok Shop"** → `/tiktok/product`, `/tiktok/shop/search`

When in doubt, check the platform reference file for the full endpoint list.

## Full API docs

For the complete interactive documentation with response schemas and playground: https://docs.scrapecreators.com
