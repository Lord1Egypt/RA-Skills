# Publer API Reference

Base URL: `https://app.publer.com/api/v1`

## Authentication

Every request requires:
```
Authorization: Bearer-API YOUR_API_KEY
Publer-Workspace-Id: YOUR_WORKSPACE_ID
Content-Type: application/json
```

- API keys created at Settings → Access & Login → API Keys
- Select only required scopes: `workspaces`, `accounts`, `posts`, `media`, `analytics`
- `Publer-Workspace-Id` required for most endpoints (exceptions: `/users/me`, `/workspaces`)
- Business plan required for API access

## Request / Response Format

- GET: query parameters for filters/pagination
- POST/PUT: JSON body
- DELETE: query parameters (no body)
- Success: returns resource or `{ "job_id": "..." }` for async ops
- Error: `{ "errors": ["Detailed error message"] }`

## HTTP Status Codes

- `200 OK`, `201 Created`, `202 Accepted` (async)
- `400 Bad Request`, `401 Unauthorized`, `403 Forbidden`
- `404 Not Found`, `413 Payload Too Large`
- `422 Unprocessable Entity`, `429 Too Many Requests`
- `500 Internal Server Error`

## Async Operations

Many write operations are asynchronous:
1. Submit request → `{ "success": true, "data": { "job_id": "..." } }`
2. Poll `GET /job_status/{job_id}` until complete

Job status response:
```json
{
  "success": true,
  "data": {
    "status": "complete",
    "result": {
      "status": "working|complete|failed",
      "payload": { "failures": {} },
      "plan": { "rate": "business", "locked": false }
    }
  }
}
```

Job status values: `working`, `complete`, `failed`

Failed job example:
```json
{
  "status": "complete",
  "payload": {
    "failures": [
      {
        "account_id": "63c675b54e299e9cf2b667ea",
        "account_name": "Test Page",
        "provider": "facebook",
        "message": "There's another post at this time. A one minute gap is required between posts"
      }
    ]
  }
}
```

## Rate Limits

- 100 requests per 2-minute fixed window (per user account, across all API keys)
- `429 Too Many Requests` when exceeded: `{ "error": "Rate limit exceeded. Retry later." }`
- Headers: `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset` (UNIX timestamp)
- Use exponential backoff; batch requests using bulk endpoints

---

## Users

### Get Current User
`GET /users/me`

No workspace header required.

**Response:**
```json
{
  "id": "5b1ec026db27977424e8599e",
  "email": "user@example.com",
  "name": "username",
  "first_name": "First",
  "picture": "https://..."
}
```

---

## Workspaces

**Scope:** `workspaces` | No workspace header required.

### List Workspaces
`GET /workspaces`

**Response** (top-level array):
```json
[
  {
    "id": "61a7c2e4f9e8c3b2d1e0f9a8",
    "name": "Marketing Team",
    "plan": "business",
    "picture": "https://...",
    "owner": {
      "id": "5b1ec026db27977424e8599e",
      "email": "user@example.com",
      "name": "username",
      "first_name": "First",
      "picture": "https://..."
    },
    "members": [{}]
  }
]
```

---

## Accounts

**Scope:** `accounts`

### List Accounts
`GET /accounts`

**Response** (top-level array):
```json
[
  {
    "id": "63c675b54e299e9cf2b667ea",
    "provider": "facebook",
    "name": "My Facebook Page",
    "social_id": "123456789",
    "picture": "https://...",
    "type": "page"
  }
]
```

**Provider enum:** `facebook`, `instagram`, `twitter`, `linkedin`, `pinterest`, `youtube`, `tiktok`, `google`, `wordpress`, `telegram`, `mastodon`, `threads`, `bluesky`

**Type enum:** `page`, `profile`, `group`, `business`, `channel`, `location`, `blog`

**Provider → supported types:**
| Provider | Account Types |
|---|---|
| facebook | page, group, profile |
| instagram | business |
| twitter | profile |
| linkedin | page, profile |
| pinterest | business, profile |
| youtube | channel |
| tiktok | profile |
| google | location |
| wordpress | blog |
| telegram | channel |
| mastodon | profile |
| threads | profile |
| bluesky | profile |

---

## Posts

**Scope:** `posts`

### List Posts
`GET /posts`

**Query Parameters:**
| Param | Type | Required | Description |
|---|---|---|---|
| `state` | string | No | Single state filter |
| `state[]` | array | No | Multiple state filters |
| `from` | date | Co-req with `to` | ISO date, posts on/after |
| `to` | date | Co-req with `from` | ISO date, posts on/before |
| `page` | integer | No | 0-based, default 0 |
| `account_ids[]` | array | No | Filter by account IDs |
| `query` | string | No | Full-text search |
| `postType` | string | No | Filter by post type |
| `member_id` | string | No | Filter by workspace member |

**State values:** `all`, `scheduled`, `scheduled_approved`, `scheduled_pending`, `scheduled_declined`, `scheduled_reauth`, `scheduled_locked`, `published`, `published_posted`, `published_deleted`, `published_hidden`, `draft`, `draft_dated`, `draft_undated`, `draft_private`, `draft_public`, `failed`, `recycling`, `recycling_active`, `recycling_paused`, `recycling_expired`, `recycling_failed`, `recycling_pending`, `recycling_declined`, `recycling_reauth`, `recycling_locked`, `recurring`

**Post type values:** `status`, `link`, `photo`, `gif`, `video`, `reel`, `story`, `short`, `poll`, `document`, `carousel`, `article`

**Response:**
```json
{
  "posts": [
    {
      "id": "68176f0e8bee9dc9b0ce3427",
      "text": "Post content",
      "url": "https://example.com",
      "state": "scheduled",
      "type": "status",
      "account_id": "63c675b54e299e9cf2b667ea",
      "network": "facebook",
      "user": { "id": "...", "name": "...", "picture": "..." },
      "scheduled_at": "2025-05-15T14:30:00.000+02:00",
      "post_link": "https://facebook.com/post/123",
      "has_media": true
    }
  ],
  "total": 42,
  "page": 1,
  "per_page": 20,
  "total_pages": 3
}
```

---

### Create / Schedule Posts
`POST /posts/schedule` — schedule or save as draft
`POST /posts/schedule/publish` — publish immediately

Both are async and return a job ID.

**Common request structure:**
```json
{
  "bulk": {
    "state": "scheduled",
    "posts": [
      {
        "networks": {
          "facebook": {
            "type": "status",
            "text": "Post content"
          }
        },
        "accounts": [
          {
            "id": "63c675b54e299e9cf2b667ea",
            "scheduled_at": "2025-05-15T14:30:00Z"
          }
        ]
      }
    ]
  }
}
```

Use `"default"` as the network key to apply same content to all accounts.

**`state` values for creation:**
| State | Description |
|---|---|
| `scheduled` | Schedule for specific time (requires `scheduled_at`, must be ≥1 min in future) |
| `draft` / `draft_public` | Workspace-visible draft |
| `draft_private` | Creator-only draft |
| `recurring` | Repeating post (requires `recurring` object) |

**Per-account fields:**
```json
{
  "id": "ACCOUNT_ID",
  "scheduled_at": "2025-05-15T14:30:00Z",
  "labels": [],
  "previewed_media": true,
  "comments": [
    {
      "text": "First comment text",
      "language": "en",
      "delay": { "duration": 1, "unit": "Minute" },
      "media": { "type": "photo", "path": "..." }
    }
  ],
  "share": {
    "text": "Share text",
    "account_ids": ["OTHER_ACCOUNT_ID"],
    "after": { "duration": 1, "unit": "Minute" }
  },
  "delete": {
    "hide": true,
    "delay": { "duration": 1, "unit": "Minute" }
  }
}
```

**Auto-scheduling** (requires posting schedule configured in account first):
```json
{
  "auto": true,
  "share_next": false,
  "range": {
    "start_date": "2025-05-23T07:45:00.000Z",
    "end_date": "2025-05-31T07:45:00.000Z"
  }
}
```

**Recycling:**
```json
{
  "recycling": {
    "solo": true,
    "gap": 2,
    "gap_freq": "Week",
    "start_date": "2025-06-01",
    "expire_count": "3",
    "expire_date": "2025-07-15"
  }
}
```
`gap_freq` values: `Day`, `Week`, `Month` (capitalized)

**Recurring** (`state` must be `"recurring"`):
```json
{
  "recurring": {
    "start_date": "2025-05-01T03:45-04:00",
    "end_date": "2025-06-01T03:45-04:00",
    "repeat": "weekly",
    "days_of_week": [1, 5],
    "repeat_rate": 1,
    "time": "09:00"
  }
}
```
`repeat` values: `daily`, `weekly`, `monthly`
`days_of_week`: 1=Monday, 7=Sunday

**Media in posts** (inside the network object):
```json
"media": [
  {
    "id": "MEDIA_ID",
    "type": "image",
    "alt_text": "Accessibility description"
  }
]
```

**Response:**
```json
{ "success": true, "data": { "job_id": "6810dec617eae6d55d7a5e5b" } }
```

---

### Update Post
`PUT /posts/{id}`

**Request body:**
```json
{ "post": { "text": "Updated content", "title": "Optional title" } }
```

Published post updates are limited by network:
| Network | Updatable Fields |
|---|---|
| LinkedIn | Text |
| YouTube | Title (max 100 chars), description (max 5000 chars) |
| Google Business | Text (max 1500 chars) |
| Facebook | Text, title (video only) |
| WordPress | Title, content |
| Telegram | Text (status/link only) |
| Mastodon | Text, title |
| Twitter, Pinterest, Instagram, Threads, Bluesky | Labels only |

Recurring post updates apply to future child posts only.

---

### Delete Posts
`DELETE /posts`

**Query Parameters:** `post_ids[]` — array of post IDs (required)

**Response:** `{ "deleted_ids": ["post_id_1", "post_id_2"] }`

**Rules:** Cannot delete queued posts (except reminders). Private drafts: creator only. Pending-state deletions notify the creator.

---

### Network-Specific Fields

Inside the network object, some platforms support additional fields:

**Pinterest:** `"board_id": "board_id_here"`

**Google Business:**
```json
"cta": { "type": "LEARN_MORE", "url": "https://example.com" },
"location_id": "location_id_here"
```

**YouTube:**
```json
"title": "Video Title",
"privacy": "public|private|unlisted",
"category": "22"
```

**Telegram:** `"disable_notification": false`

**Mastodon:**
```json
"visibility": "public|unlisted|private|direct",
"content_warning": "Optional CW text"
```

---

## Content Types by Network

| Network | Supported Types |
|---|---|
| Facebook | status, photo, video, link, carousel, story, reel, gif |
| Instagram | photo, video, carousel, story, reel |
| Twitter/X | status, photo, video, link, gif, poll |
| LinkedIn | status, photo, video, link, document, poll, gif |
| Pinterest | photo, video, carousel |
| Google Business | status, photo, event, offer |
| YouTube | video, short |
| TikTok | video, photo, carousel |
| WordPress | article |
| Telegram | status, photo, video, link, gif |
| Mastodon | status, photo, video, link, gif, poll |
| Threads | status, photo, video, link |
| Bluesky | status, photo, video, link |

**Note:** Threads cannot schedule posts for specific times via API.

---

## Media

**Scope:** `media`

### List Media
`GET /media`

| Param | Type | Required | Description |
|---|---|---|---|
| `ids[]` | array | No | Specific IDs (ignores other filters) |
| `page` | integer | No | 0-based, default 0 |
| `types[]` | array | Yes | `photo`, `video`, `gif` |
| `used[]` | boolean[] | Yes | Filter by usage status |
| `source[]` | array | No | `canva`, `vista`, `postnitro`, `contentdrips`, `openai`, `favorites`, `upload` |
| `search` | string | No | Full-text search on name/caption |

**Response:**
```json
{
  "media": [
    {
      "id": "5f5fe854421aa9792e762b70",
      "type": "photo",
      "name": "Beach sunset",
      "caption": "Caption text",
      "path": "https://cdn.publer.com/uploads/...",
      "thumbnails": [{ "id": "...", "small": "...", "real": "..." }],
      "created_at": "2023-05-15T10:30:00Z",
      "updated_at": "2023-05-15T10:30:00Z",
      "favorite": true,
      "in_library": false
    }
  ],
  "total": 10
}
```

---

### Upload Media (Direct)
`POST /media` — multipart/form-data, max 200MB

**Form fields:** `file` (binary), `direct_upload` (boolean, default false — set true if you need the final CDN URL), `in_library` (boolean, default false)

**Response:**
```json
{
  "id": "6813892b5ec8b1e65235ae9e",
  "path": "https://cdn.publer.io/uploads/...",
  "thumbnail": "https://cdn.publer.io/uploads/...",
  "validity": {},
  "width": 1451,
  "height": 1005,
  "source": null,
  "type": "photo",
  "name": "filename.png",
  "caption": null
}
```

`validity` object indicates per-network/per-type compatibility (e.g. `validity.instagram.reel = false`). Check before using media in posts.

---

### Upload Media (From URL)
`POST /media/from-url` — async, returns job_id

**Request body:**
```json
{
  "media": [
    { "url": "https://example.com/image.jpg", "name": "My image", "caption": "Optional", "source": "unsplash" }
  ],
  "type": "single",
  "direct_upload": false,
  "in_library": false
}
```

`type` values: `single`, `bulk`. Returns `{ "job_id": "..." }` — poll `/job_status/{job_id}`.

---

### Get Media Options
`GET /workspaces/{workspace_id}/media_options`

Workspace ID is in the **path** (not the header). Returns Facebook albums, Pinterest boards, and watermarks.

**Query Parameters:** `accounts[]` — filter by account IDs

**Response** (top-level array):
```json
[
  {
    "id": "ACCOUNT_ID",
    "albums": [{ "id": "album_id", "name": "Album Name", "type": "facebook" }],
    "watermarks": [
      {
        "id": "wm_id", "name": "My Watermark",
        "opacity": 75, "size": 15,
        "position": "bottom_right",
        "default": true, "image": "https://..."
      }
    ]
  }
]
```

---

## Media Specifications

**Supported formats:**
- Images: JPG, PNG, GIF, WEBP
- Videos: MP4, MOV, AVI, WEBM
- Documents: PDF only, max 100MB, LinkedIn only

**Image specs:**
| Network | Optimal Size | Aspect Ratio | Max Size |
|---|---|---|---|
| Facebook | 1200x630px | 1.91:1 | 8MB |
| Instagram | 1080x1080px | 1:1 to 4:5 | 8MB |
| Twitter | 1200x675px | 16:9 | 5MB |
| LinkedIn | 1200x627px | 1.91:1 | 5MB |
| Pinterest | 1000x1500px | 2:3 | 20MB |
| Google Business | 1200x900px | 4:3 | 5MB |
| Telegram | 1280x720px | 16:9 | 10MB |
| Threads | 1080x1080px | 1:1 to 4:5 | 8MB |
| Bluesky | 1200x675px | 16:9 | 5MB |

**Video specs:**
| Network | Optimal Size | Aspect Ratio | Duration | Max Size |
|---|---|---|---|---|
| Facebook | 1280x720px | 16:9 | 1s-240m | 10GB |
| Instagram | 1080x1920px | 9:16 | 3s-60m | 650MB |
| Twitter | 1280x720px | 16:9 | 0.5s-140s | 512MB |
| LinkedIn | 1920x1080px | 16:9 | 3s-15m | 5GB |
| Pinterest | 1080x1920px | 9:16 | 4s-15m | 2GB |
| TikTok | 1080x1920px | 9:16 | 3s-10m | 500MB |
| YouTube | 1920x1080px | 16:9 | up to 12h | 256GB |
| Telegram | 1280x720px | 16:9 | no limit | 2GB |
| Threads | 1080x1920px | 9:16 | 3s-5m | 650MB |

---

## Analytics

**Scope:** `analytics`

### List Available Charts
`GET /analytics/charts`

**Query Parameters:** `account_type` — filter by platform type

**Account type values:** `ig_business`, `fb_page`, `twitter`, `linkedin`, `youtube`, `tiktok`, `google`, `pin_business`, `pin_personal`, `threads`, `wordpress_oauth`, `in_profile`, `in_page`, `mastodon`, `bluesky`

**Response** (top-level array):
```json
[
  {
    "id": "followers",
    "title": "Followers",
    "group_id": "growth",
    "tooltip": "...",
    "type": "vertical",
    "last_value": true,
    "show_percentage": false
  }
]
```

`group_id` values: `growth`, `insights`, `demographics`
`type` values: `vertical`, `horizontal`, `side_by_side`

Always fetch chart IDs dynamically — they can change over time.

---

### Get Chart Data
`GET /analytics/:account_id/chart_data`

`account_id` optional in path. Omit for workspace aggregate.

**Query Parameters:** `chart_ids[]` (required), `from`/`to` (co-required, YYYY-MM-DD)

**Response:**
```json
{
  "current": {
    "followers": { "data": [{ "date": "2025-01-01", "value": 100 }], "last_value": 5000 }
  },
  "previous": { "followers": { ... } }
}
```

Batch chart IDs by logical group (growth, then insights, then demographics) for best performance.

---

### Get Post Insights
`GET /analytics/:account_id/post_insights`

`account_id` optional. `from`/`to` both required.

**Query Parameters:** `from`, `to`, `competitors` (`true`/`false`), `competitor_id`, `query`, `postType`, `sort_by`, `sort_type` (`ASC`/`DESC`), `page` (0-based, 10/page), `member_id`

**`sort_by` values:** `scheduled_at`, `reach`, `engagement`, `engagement_rate`, `click_through_rate`, `reach_rate`, `postType`, `likes`, `video_views`, `comments`, `shares`, `saves`, `link_clicks`, `post_clicks`

**Response:**
```json
{
  "posts": [
    {
      "id": "...", "text": "...", "title": "...",
      "scheduled_at": "...", "post_type": "...", "account_id": "...",
      "details": { "labels": [{ "id": "...", "name": "...", "color": "..." }] },
      "analytics": {
        "reach": 1200, "engagement": 150, "engagement_rate": 12.5,
        "likes": 80, "comments": 20, "shares": 15, "saves": 10,
        "video_views": 0, "link_clicks": 25, "post_clicks": 30,
        "click_through_rate": 2.1, "reach_rate": 4.0
      }
    }
  ],
  "total": 42
}
```

Formulas: engagement_rate = engagement/reach×100, CTR = link_clicks/reach×100, reach_rate = reach/followers×100

---

### Get Hashtag Insights
`GET /analytics/:account_id/hashtag_insights`

`account_id` optional. `from`/`to` optional (defaults to workspace range).

**Query Parameters:** `from`, `to`, `sort_by` (`posts`, `reach`, `likes`, `comments`, `shares`, `video_views`), `sort_type` (`ASC`/`DESC`), `page` (0-based, 10/page), `query`, `member_id`

**Response:**
```json
{
  "records": [
    {
      "hashtag": "socialmedia",
      "posts": 15,
      "recent_posts": [{ "id": "...", "text": "...", "scheduled_at": "..." }],
      "reach": 5000, "likes": 200, "comments": 50, "shares": 30,
      "engagement": 280, "video_views": 0, "link_clicks": 45,
      "post_clicks": 60, "saves": 25, "hashtag_score": 8.5
    }
  ],
  "total": 25
}
```

`hashtag_score` = (total hashtag engagement / total post engagement) × 100

---

### Get Hashtag Performing Posts
`GET /analytics/:account_id/hashtag_performing_posts`

**Query Parameters:** `hashtag` (required, include `#`), `from`, `to`, `sort_by`, `sort_type`, `member_id`, `query`

Returns top-level array of up to 6 posts, each with `id`, `text`, `title`, `scheduled_at`, `account_id`, `hashtags[]`, `analytics` object, `details`.

---

### Get Best Times to Post
`GET /analytics/:account_id/best_times`

`account_id` optional. `from`/`to` required.

**Query Parameters:** `from`, `to`, `competitors` (`true`/`false`), `competitor_id`

**Response:** Object keyed by day (`"Monday"`–`"Sunday"`), each an array of 24 hourly scores (index 0–23). Higher = better posting time. Scores are relative, not percentages.

```json
{
  "Monday": [0, 0, 0, 0, 0, 0, 5, 12, 18, 25, 22, 15, 8, 10, 16, 20, 18, 14, 12, 8, 5, 3, 1, 0],
  "Tuesday": [...]
}
```

---

### Get Members Analytics
`GET /analytics/members`

**Query Parameters:** `from` (required), `to` (required), `account_id` (optional)

**Response** (top-level array):
```json
[
  {
    "engagements": 1250, "posts": 42, "reach": 15000,
    "account_ids": ["63c675b54e299e9cf2b667ea"],
    "user": { "id": "...", "name": "John Smith", "picture": "..." }
  }
]
```

`reach` may be omitted for unsupported networks — handle gracefully.

---

## Competitors

**Scope:** `analytics`

### List Competitors
`GET /competitors/:account_id`

`account_id` optional in path.

**Response** (top-level array):
```json
[
  {
    "provider": "instagram", "name": "Competitor Brand",
    "social_id": "123456", "picture": "https://...",
    "type": "business", "competitor_sync_in_queue": false,
    "username": "competitorbrand", "verified": false
  }
]
```

`username` available for twitter/instagram/facebook. `verified` available for twitter/facebook.

---

### Get Competitor Analytics
`GET /competitors/:account_id/analytics`

`account_id` optional (path or query param).

**Query Parameters:** `competitor_id`, `query`, `from`, `to`, `page` (0-based), `sort_by`, `sort_type` (`asc`/`desc` — lowercase)

**`sort_by` values:** `followers`, `reach`, `engagement`, `posts_count`, `videos_count`, `photos_count`, `links_count`, `statuses_count`

**Response:**
```json
{
  "insights": [
    {
      "account": { "id": "...", "name": "...", "provider": "...", "competitor_sync_in_queue": false, "picture": "...", "my_account": false },
      "followers": 50000, "followers_growth": 1200,
      "engagement": 3500, "engagement_rate": 7.0, "reach": 45000,
      "posts_count": 30, "videos_count": 8, "photos_count": 15,
      "links_count": 5, "statuses_count": 2
    }
  ],
  "total": 5
}
```

`reach` not available for Instagram/Facebook. `my_account: true` flags your own account.

---

## Daily Post Limits (Business Plan)

Rolling 24-hour UTC window, per connected profile.

| Platform | Business Plan |
|---|---|
| Facebook Posts & Reels | 36/day |
| Instagram Posts & Reels | 25/day |
| Twitter/X | 100/day |
| LinkedIn Profile | 14/day |
| LinkedIn Page | 24/day |
| TikTok | 25/day |
| Pinterest | 36/day |
| YouTube | 15/day |
| Threads | 250/day |
| Bluesky | 100/day |
| Mastodon | 100/day |
| Google Business | 15/day |
| Telegram | 15/day |
| WordPress | 24/day |

---

## Error Handling

| Code | Meaning | Action |
|---|---|---|
| 401 | Missing/invalid API key | Verify key and `Bearer-API` header format |
| 403 | Wrong scope or missing `Publer-Workspace-Id` | Check scopes and headers |
| 404 | Resource not found | Confirm ID is correct |
| 413 | File too large (>200MB) | Use URL upload method instead |
| 422 | Validation error | Surface `errors[]` array to user |
| 429 | Rate limited | Wait for `X-RateLimit-Reset`, use exponential backoff |
| 500 | Publer server error | Retry or check Publer status page |
