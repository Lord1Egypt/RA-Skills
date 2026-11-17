# TikTok

Generated from SocQ Capability Registry schema `v1-9a87cca161f6`. Read this file when the request targets TikTok.

## Endpoint selection

| Endpoint | Use for | Input choice | Standard schema | Cost |
| --- | --- | --- | --- | --- |
| [`tiktok/comment-replies`](https://docs.socq.ai/api-manual/tiktok/comment-replies) | Collect public TikTok comment replies. | comment_id, url | `comment@1.0` | 0.5 credits/result |
| [`tiktok/comments`](https://docs.socq.ai/api-manual/tiktok/comments) | TikTok Comments API | urls | `comment@1.0` | 0.25 credits/result |
| [`tiktok/followers-list`](https://docs.socq.ai/api-manual/tiktok/followers-list) | Collect public TikTok follower profiles. | usernames | `relationship@1.0` | 0.5 credits/result |
| [`tiktok/following-list`](https://docs.socq.ai/api-manual/tiktok/following-list) | Collect public TikTok followed profiles. | usernames | `relationship@1.0` | 0.5 credits/result |
| [`tiktok/hashtags`](https://docs.socq.ai/api-manual/tiktok/hashtags) | TikTok Hashtags API | hashtags | `hashtag-trend@1.0` | 0.7 credits/result |
| [`tiktok/live-room-info`](https://docs.socq.ai/api-manual/tiktok/live-room-info) | Collect public TikTok live room metadata and audience metrics. | room_id, user_id | `live-room@1.0` | 0.5 credits/result |
| [`tiktok/popular-songs`](https://docs.socq.ai/api-manual/tiktok/popular-songs) | Get the TikTok App Top 50 or Viral 50 music chart. Choose chart_type top or viral. results_limit defaults to 20, maximum 50. | none | `music@1.0` | 0.5 credits/result |
| [`tiktok/profiles`](https://docs.socq.ai/api-manual/tiktok/profiles) | TikTok Profiles API | usernames | `account@1.0` | 0.6 credits/result |
| [`tiktok/search`](https://docs.socq.ai/api-manual/tiktok/search) | TikTok Search API | query | `reel-video@1.0` | 0.7 credits/result |
| [`tiktok/search-users`](https://docs.socq.ai/api-manual/tiktok/search-users) | Search public TikTok accounts by keyword. | query | `account@1.0` | 0.6 credits/result |
| [`tiktok/song`](https://docs.socq.ai/api-manual/tiktok/song) | Collect public TikTok sound or song details. | one of: music_id; url | `music@1.0` | 0.5 credits/result |
| [`tiktok/song-videos`](https://docs.socq.ai/api-manual/tiktok/song-videos) | Collect public TikTok videos that use a sound. | music_ids | `reel-video@1.0` | 0.5 credits/result |
| [`tiktok/top-search`](https://docs.socq.ai/api-manual/tiktok/top-search) | Search public TikTok videos and photo carousels. | query | `reel-video@1.0` | 0.7 credits/result |
| [`tiktok/trending-feed`](https://docs.socq.ai/api-manual/tiktok/trending-feed) | Collect trending TikTok videos for a region. | region | `reel-video@1.0` | 0.7 credits/result |
| [`tiktok/user-live`](https://docs.socq.ai/api-manual/tiktok/user-live) | Check public TikTok accounts for live streaming status, including offline results. | usernames | `live-status@1.0` | 0.5 credits/result |
| [`tiktok/user-videos`](https://docs.socq.ai/api-manual/tiktok/user-videos) | Collect public videos from TikTok profiles. | usernames | `reel-video@1.0` | 0.5 credits/result |
| [`tiktok/video-transcript`](https://docs.socq.ai/api-manual/tiktok/video-transcript) | Extract transcripts from public TikTok videos. | urls | `transcript@1.0` | 0.5 credits/result |
| [`tiktok/videos`](https://docs.socq.ai/api-manual/tiktok/videos) | TikTok Videos API | urls | `reel-video@1.0` | 0.7 credits/result |

## Validated examples

### `tiktok/comment-replies`

Typed MCP tool: `socq_tiktok_comment_replies`

```json
{
  "url": "https://www.tiktok.com/@scout2015/video/6718335390845095173",
  "comment_id": "1234567890",
  "results_limit": 20
}
```

### `tiktok/comments`

Typed MCP tool: `socq_tiktok_comments`

```json
{
  "urls": [
    "https://www.tiktok.com/@scout2015/video/6718335390845095173"
  ]
}
```

### `tiktok/followers-list`

Typed MCP tool: `socq_tiktok_followers_list`

```json
{
  "usernames": [
    "@tiktok"
  ],
  "results_limit": 20
}
```

### `tiktok/following-list`

Typed MCP tool: `socq_tiktok_following_list`

```json
{
  "usernames": [
    "@tiktok"
  ],
  "results_limit": 20
}
```

### `tiktok/hashtags`

Typed MCP tool: `socq_tiktok_hashtags`

```json
{
  "hashtags": [
    "#travel"
  ]
}
```

### `tiktok/live-room-info`

Typed MCP tool: `socq_tiktok_live_room_info`

```json
{
  "room_id": "7523685855395842871",
  "user_id": "6742945285876515845"
}
```

### `tiktok/popular-songs`

Typed MCP tool: `socq_tiktok_popular_songs`

Choose the TikTok App Top 50 (top, default) or Viral 50 (viral) music chart. results_limit defaults to 20 and accepts integers from 1 to 50.

```json
{
  "chart_type": "top",
  "results_limit": 20
}
```

### `tiktok/profiles`

Typed MCP tool: `socq_tiktok_profiles`

```json
{
  "usernames": [
    "@tiktok"
  ]
}
```

### `tiktok/search`

Typed MCP tool: `socq_tiktok_search`

```json
{
  "query": "AI tools"
}
```

### `tiktok/search-users`

Typed MCP tool: `socq_tiktok_search_users`

```json
{
  "query": "taylor swift",
  "results_limit": 20
}
```

### `tiktok/song`

Typed MCP tool: `socq_tiktok_song`

```json
{
  "music_id": "7439295283975702544"
}
```

### `tiktok/song-videos`

Typed MCP tool: `socq_tiktok_song_videos`

```json
{
  "music_ids": [
    "7439295283975702544"
  ],
  "results_limit": 20
}
```

### `tiktok/top-search`

Typed MCP tool: `socq_tiktok_top_search`

query is required. results_limit defaults to 100. Results can contain videos and photo carousels; region changes content availability and does not guarantee geographic filtering.

```json
{
  "query": "coffee",
  "sort_by": "relevance",
  "results_limit": 20
}
```

### `tiktok/trending-feed`

Typed MCP tool: `socq_tiktok_trending_feed`

```json
{
  "region": "US",
  "results_limit": 20
}
```

### `tiktok/user-live`

Typed MCP tool: `socq_tiktok_user_live`

Provide a non-empty usernames array. Each successful lookup returns one billable status, including is_live=false for offline accounts.

```json
{
  "usernames": [
    "thejustalex"
  ]
}
```

### `tiktok/user-videos`

Typed MCP tool: `socq_tiktok_user_videos`

```json
{
  "usernames": [
    "@tiktok"
  ],
  "results_limit": 20
}
```

### `tiktok/video-transcript`

Typed MCP tool: `socq_tiktok_video_transcript`

```json
{
  "urls": [
    "https://www.tiktok.com/@scout2015/video/6718335390845095173"
  ],
  "language": "en"
}
```

### `tiktok/videos`

Typed MCP tool: `socq_tiktok_videos`

```json
{
  "urls": [
    "https://www.tiktok.com/@scout2015/video/6718335390845095173"
  ]
}
```
