# YouTube

Generated from SocQ Capability Registry schema `v1-9a87cca161f6`. Read this file when the request targets YouTube.

## Endpoint selection

| Endpoint | Use for | Input choice | Standard schema | Cost |
| --- | --- | --- | --- | --- |
| [`youtube/channel-live-videos`](https://docs.socq.ai/api-manual/youtube/channel-live-videos) | Collect public YouTube channel live videos. | urls | `reel-video@1.0` | 0.5 credits/result |
| [`youtube/channel-videos`](https://docs.socq.ai/api-manual/youtube/channel-videos) | YouTube Channel Videos API | urls | `reel-video@1.0` | 0.5 credits/result |
| [`youtube/channels`](https://docs.socq.ai/api-manual/youtube/channels) | YouTube Channels API | urls | `account@1.0` | 0.26 credits/result |
| [`youtube/comment-replies`](https://docs.socq.ai/api-manual/youtube/comment-replies) | Collect public YouTube comment replies. | one of: comment_id + url; continuation_token | `comment@1.0` | 0.5 credits/result |
| [`youtube/comments`](https://docs.socq.ai/api-manual/youtube/comments) | YouTube Comments API | urls | `comment@1.0` | 0.3 credits/result |
| [`youtube/community-posts`](https://docs.socq.ai/api-manual/youtube/community-posts) | Collect public YouTube community posts. | urls | `post@1.0` | 0.5 credits/result |
| [`youtube/hashtag-search`](https://docs.socq.ai/api-manual/youtube/hashtag-search) | Search public YouTube videos by hashtag. | hashtags | `reel-video@1.0` | 0.5 credits/result |
| [`youtube/playlist-videos`](https://docs.socq.ai/api-manual/youtube/playlist-videos) | Collect videos from a public YouTube playlist. | urls | `reel-video@1.0` | 0.5 credits/result |
| [`youtube/search`](https://docs.socq.ai/api-manual/youtube/search) | YouTube Search API | query | `reel-video@1.0` | 0.5 credits/result |
| [`youtube/shorts`](https://docs.socq.ai/api-manual/youtube/shorts) | YouTube Shorts API | urls | `reel-video@1.0` | 0.5 credits/result |
| [`youtube/transcripts`](https://docs.socq.ai/api-manual/youtube/transcripts) | YouTube Transcripts API | urls | `transcript@1.0` | 0.5 credits/result |
| [`youtube/videos`](https://docs.socq.ai/api-manual/youtube/videos) | YouTube Videos API | urls | `reel-video@1.0` | 0.5 credits/result |

## Validated examples

### `youtube/channel-live-videos`

Typed MCP tool: `socq_youtube_channel_live_videos`

```json
{
  "urls": [
    "https://www.youtube.com/@YouTube"
  ],
  "results_limit": 20
}
```

### `youtube/channel-videos`

Typed MCP tool: `socq_youtube_channel_videos`

```json
{
  "urls": [
    "https://www.youtube.com/@YouTube"
  ]
}
```

### `youtube/channels`

Typed MCP tool: `socq_youtube_channels`

```json
{
  "urls": [
    "https://www.youtube.com/@YouTube"
  ]
}
```

### `youtube/comment-replies`

Typed MCP tool: `socq_youtube_comment_replies`

```json
{
  "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
  "comment_id": "Ugzge340dBgB75hWBm54AaABAg",
  "results_limit": 20
}
```

### `youtube/comments`

Typed MCP tool: `socq_youtube_comments`

```json
{
  "urls": [
    "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
  ]
}
```

### `youtube/community-posts`

Typed MCP tool: `socq_youtube_community_posts`

```json
{
  "urls": [
    "https://www.youtube.com/@YouTube"
  ],
  "results_limit": 20
}
```

### `youtube/hashtag-search`

Typed MCP tool: `socq_youtube_hashtag_search`

```json
{
  "hashtags": [
    "#technology"
  ],
  "results_limit": 20
}
```

### `youtube/playlist-videos`

Typed MCP tool: `socq_youtube_playlist_videos`

```json
{
  "urls": [
    "https://www.youtube.com/playlist?list=PLBCF2DAC6FFB574DE"
  ],
  "results_limit": 100
}
```

### `youtube/search`

Typed MCP tool: `socq_youtube_search`

```json
{
  "query": "AI agents tutorial"
}
```

### `youtube/shorts`

Typed MCP tool: `socq_youtube_shorts`

```json
{
  "urls": [
    "https://www.youtube.com/@YouTube"
  ]
}
```

### `youtube/transcripts`

Typed MCP tool: `socq_youtube_transcripts`

```json
{
  "urls": [
    "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
  ],
  "language": "en"
}
```

### `youtube/videos`

Typed MCP tool: `socq_youtube_videos`

```json
{
  "urls": [
    "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
  ]
}
```
