---
name: creatorcrawl
description: Access live TikTok data via the CreatorCrawl API. Look up creator profiles, search videos, pull comments and transcripts, track trending hashtags, discover popular songs. Use whenever someone asks about TikTok creators, videos, trends, or social media research.
version: 1.0.0
user-invocable: true
metadata: {"openclaw":{"requires":{"env":["CREATORCRAWL_API_KEY"],"bins":["curl"]},"primaryEnv":"CREATORCRAWL_API_KEY","emoji":"📱","homepage":"https://creatorcrawl.com"}}
---

# CreatorCrawl TikTok Data

Access live TikTok data: creator profiles, video analytics, comments, transcripts, search, trending content, and songs. 19 endpoints, structured JSON responses, no scraping required.

## Setup

Get a free API key at https://creatorcrawl.com (250 free credits, no card required). Set the `CREATORCRAWL_API_KEY` environment variable.

## How to call the API

Use curl for all requests. Authenticate with the `x-api-key` header. Base URL: `https://creatorcrawl.com`.

```bash
curl -s -H "x-api-key: $CREATORCRAWL_API_KEY" \
  "https://creatorcrawl.com/api/tiktok/profile?handle=charlidamelio"
```

All responses are JSON. Errors return `{ "success": false, "error": "message" }` with status 400 (bad params), 401 (unauthorized), 402 (no credits), or 502 (upstream).

## Endpoints

### Profiles

**GET /api/tiktok/profile** — Get a creator's profile, stats, and recent videos.
| Param | Required | Description |
|-------|----------|-------------|
| handle | yes | TikTok handle (without @) |

Returns: user info (id, uniqueId, nickname, signature, verified), stats (followerCount, followingCount, heartCount, videoCount), and recent videos.

**GET /api/tiktok/profile/videos** — Get a creator's videos with pagination and sorting.
| Param | Required | Description |
|-------|----------|-------------|
| handle | yes | TikTok handle |
| sort_by | no | `latest` or `popular` |
| max_cursor | no | Pagination cursor from previous response |
| region | no | 2-letter country code |

Returns: aweme_list with statistics (play_count, digg_count, comment_count, share_count), author info, music info. Paginate with `max_cursor`.

**GET /api/tiktok/user/followers** — Get a creator's followers (paginated).
| Param | Required | Description |
|-------|----------|-------------|
| handle | yes (or user_id) | TikTok handle |
| user_id | yes (or handle) | User ID (faster) |
| min_time | no | Pagination cursor |

**GET /api/tiktok/user/following** — Get accounts a creator follows.
| Param | Required | Description |
|-------|----------|-------------|
| handle | yes | TikTok handle |
| min_time | no | Pagination cursor |

**GET /api/tiktok/user/live** — Check if a creator is live streaming.
| Param | Required | Description |
|-------|----------|-------------|
| handle | yes | TikTok handle |

### Videos

**GET /api/tiktok/video** — Get full video details.
| Param | Required | Description |
|-------|----------|-------------|
| url | yes | TikTok video URL |
| get_transcript | no | `true` to include transcript |
| region | no | 2-letter country code |

Returns: aweme_detail with statistics, author, music, video dimensions, hashtags, and optional transcript.

**GET /api/tiktok/video/comments** — Get video comments (paginated).
| Param | Required | Description |
|-------|----------|-------------|
| url | yes | TikTok video URL |
| cursor | no | Pagination cursor |

Returns: comments with text, digg_count, reply_comment_total, nested replies.

**GET /api/tiktok/video/transcript** — Get video transcript text.
| Param | Required | Description |
|-------|----------|-------------|
| url | yes | TikTok video URL |
| language | no | 2-letter language code (en, es, fr) |
| use_ai_as_fallback | no | `true` for AI transcription (under 2 min videos) |

### Search

**GET /api/tiktok/search/keyword** — Search videos by keyword.
| Param | Required | Description |
|-------|----------|-------------|
| query | yes | Search keyword |
| date_posted | no | `yesterday`, `this-week`, `this-month`, `last-3-months`, `last-6-months`, `all-time` |
| sort_by | no | `relevance`, `most-liked`, `date-posted` |
| region | no | 2-letter country code |
| cursor | no | Pagination cursor |

**GET /api/tiktok/search/hashtag** — Search videos by hashtag.
| Param | Required | Description |
|-------|----------|-------------|
| hashtag | yes | Hashtag without # |
| region | no | 2-letter country code |
| cursor | no | Pagination cursor |

**GET /api/tiktok/search/users** — Search TikTok users.
| Param | Required | Description |
|-------|----------|-------------|
| query | yes | Search query |
| cursor | no | Pagination cursor |

**GET /api/tiktok/search/top** — Top search results (videos + photo carousels).
| Param | Required | Description |
|-------|----------|-------------|
| query | yes | Search keyword |
| publish_time | no | `yesterday`, `this-week`, `this-month`, `last-3-months`, `last-6-months`, `all-time` |
| sort_by | no | `relevance`, `most-liked`, `date-posted` |
| region | no | 2-letter country code |
| cursor | no | Pagination cursor |

### Trending

**GET /api/tiktok/get-trending-feed** — Get trending feed for a region.
| Param | Required | Description |
|-------|----------|-------------|
| region | yes | 2-letter country code (US, GB, FR, etc.) |

**GET /api/tiktok/videos/popular** — Get popular videos across TikTok.
| Param | Required | Description |
|-------|----------|-------------|
| period | no | `7` or `30` (days) |
| page | no | Page number |
| orderBy | no | `like`, `hot`, `comment`, `repost` |
| countryCode | no | Country code |

**GET /api/tiktok/creators/popular** — Discover popular creators with filters.
| Param | Required | Description |
|-------|----------|-------------|
| page | no | Page number |
| sortBy | no | `engagement`, `follower`, `avg_views` |
| followerCount | no | `10K-100K`, `100K-1M`, `1M-10M`, `10M+` |
| creatorCountry | no | Creator's country code |
| audienceCountry | no | Audience country code |

**GET /api/tiktok/hashtags/popular** — Get trending hashtags.
| Param | Required | Description |
|-------|----------|-------------|
| period | no | `7`, `30`, or `120` (days) |
| page | no | Page number |
| countryCode | no | Country code |
| newOnBoard | no | Only newly trending |
| industry | no | e.g. `beauty-and-personal-care`, `food-and-beverage`, `tech-and-electronics` |

### Songs

**GET /api/tiktok/song** — Get song details by clip ID.
| Param | Required | Description |
|-------|----------|-------------|
| clipId | yes | Clip ID (not song ID) |

**GET /api/tiktok/song/videos** — Get videos using a specific song.
| Param | Required | Description |
|-------|----------|-------------|
| clipId | yes | Clip ID from song URL |
| cursor | no | Pagination cursor |

**GET /api/tiktok/songs/popular** — Get popular/surging songs (can take up to 30s).
| Param | Required | Description |
|-------|----------|-------------|
| page | no | Page number |
| timePeriod | no | `7`, `30`, or `130` (days) |
| rankType | no | `popular` or `surging` |
| newOnBoard | no | New to top 100 |
| commercialMusic | no | Approved for business use |
| countryCode | no | Country code |

## Pagination

Paginated endpoints return a cursor field (`cursor`, `min_time`, or `max_cursor` depending on the endpoint). Pass it back as a query param for the next page. Stop when the cursor is empty/null or no more items are returned.

## Pricing

1 credit per API call. Free signup gives 250 credits. Paid packs: Starter ($29/5k credits), Pro ($99/20k credits), Scale ($299/100k credits). Credits never expire, no rate limits.
