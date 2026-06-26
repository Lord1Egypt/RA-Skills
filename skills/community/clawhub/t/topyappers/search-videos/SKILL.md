---
name: search-videos
description: Search for videos from creators across TikTok, Instagram, and YouTube using the TopYappers API. Use when the user wants to find specific video content, search by hashtags, text in captions, engagement metrics, or analyze a creator's video performance.
argument-hint: "[topic, hashtag, or description of videos to find]"
---

# Search Videos

Find video content from creators across TikTok, Instagram, and YouTube. Filter by engagement metrics, hashtags, text search, and sort results.

## Setup

**MCP Endpoint:** `https://mcp.topyappers.com`
**Transport:** HTTP
**Auth:** Bearer token in the `Authorization` header

Get an API key at [topyappers.com/profile](https://www.topyappers.com/profile).

### Claude Code
```
claude mcp add --transport http topyappers https://mcp.topyappers.com \
  --header "Authorization: Bearer YOUR_API_KEY"
```

### .mcp.json / Cursor / Claude Desktop
```json
{
  "mcpServers": {
    "topyappers": {
      "type": "http",
      "url": "https://mcp.topyappers.com",
      "headers": {
        "Authorization": "Bearer YOUR_API_KEY"
      }
    }
  }
}
```

**Tool:** `search_videos`
**Cost:** 1 credit per returned video

## Parameters

All parameters are optional. Combine filters to narrow results.

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `userHandle` | string | Filter by specific creator handle | `"mrbeast"` |
| `userFollowersMin` | integer | Minimum creator followers | `10000` |
| `userFollowersMax` | integer | Maximum creator followers | `1000000` |
| `viewsMin` | integer | Minimum video views | `5000` |
| `viewsMax` | integer | Maximum video views | `500000` |
| `likesMin` | integer | Minimum likes | `100` |
| `likesMax` | integer | Maximum likes | `50000` |
| `commentsMin` | integer | Minimum comments | `10` |
| `commentsMax` | integer | Maximum comments | `5000` |
| `sharesMin` | integer | Minimum shares | `5` |
| `sharesMax` | integer | Maximum shares | `1000` |
| `hashtags` | string | Hashtags, comma-separated | `"fashion,streetwear,ootd"` |
| `textSearch` | string | Keywords in description/caption | `"workout routine"` |
| `sortBy` | string | Sort field | `"views"` |
| `sortOrder` | string | Sort direction | `"desc"` |
| `page` | integer | Page number (default: 1) | `1` |
| `perPage` | integer | Results per page (default: 20, max: 100) | `20` |

### Sort Options

| `sortBy` value | Description |
|----------------|-------------|
| `views` | Sort by view count |
| `likes` | Sort by like count |
| `shares` | Sort by share count |
| `user_followers` | Sort by creator's follower count |

`sortOrder`: `"desc"` (default, highest first) or `"asc"` (lowest first)

## Response Fields

Each video result includes:
- `iv_id` — internal video identifier
- `user_id` — platform user identifier
- `user_handle` — creator handle/username
- `video_id` — platform video identifier
- `source` — platform (`"tiktok"`, `"instagram"`, `"youtube"`)
- `comments` — comment count
- `description` — video caption/description
- `hashtags` — array of associated hashtags
- `likes` — like count
- `shares` — share count
- `subtitles` — subtitle data if available
- `user_followers` — creator's follower count
- `views` — view count
- `date_created_timestamp` — Unix timestamp (seconds)

## Pagination

Response includes:
- `page` — current page
- `perPage` — results per page
- `total` — total matching videos
- `totalPages` — total number of pages

## Example Workflows

### Find a creator's top videos
```
search_videos with:
  userHandle: "creator_name"
  sortBy: "views"
  sortOrder: "desc"
  perPage: 10
```

### Find high-engagement videos in a niche
```
search_videos with:
  hashtags: "skincare"
  viewsMin: 100000
  likesMin: 5000
  sortBy: "likes"
  sortOrder: "desc"
```

### Search videos by topic
```
search_videos with:
  textSearch: "morning routine"
  viewsMin: 50000
  sortBy: "views"
  sortOrder: "desc"
  perPage: 20
```

### Find viral videos from micro-creators
```
search_videos with:
  userFollowersMax: 50000
  viewsMin: 500000
  sortBy: "views"
  sortOrder: "desc"
```

### Find highly-shared content
```
search_videos with:
  sharesMin: 1000
  sortBy: "shares"
  sortOrder: "desc"
  perPage: 20
```

### Analyze competitor content
1. Search for videos with `userHandle: "competitor_handle"`, sorted by views
2. Examine their top-performing content, hashtags, and descriptions
3. Identify patterns in what gets the most engagement

### Research content trends by hashtag
1. Search with `hashtags: "trending_topic"`, `sortBy: "views"`
2. Analyze descriptions, engagement ratios, and posting patterns
3. Use insights to inform content strategy
