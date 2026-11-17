# Instagram

Generated from SocQ Capability Registry schema `v1-9a87cca161f6`. Read this file when the request targets Instagram.

## Endpoint selection

| Endpoint | Use for | Input choice | Standard schema | Cost |
| --- | --- | --- | --- | --- |
| [`instagram/audio-reels`](https://docs.socq.ai/api-manual/instagram/audio-reels) | Collect public Instagram reels by audio identifier. | audio_ids | `reel-video@1.0` | 0.5 credits/result |
| [`instagram/comments`](https://docs.socq.ai/api-manual/instagram/comments) | Instagram Comments API | urls | `comment@1.0` | 0.3 credits/result |
| [`instagram/followers-count`](https://docs.socq.ai/api-manual/instagram/followers-count) | Instagram Followers Count API | one of: urls; usernames | `account@1.0` | 0.52 credits/result |
| [`instagram/followers-list`](https://docs.socq.ai/api-manual/instagram/followers-list) | Collect public profiles from an Instagram account follower list. | usernames | `relationship@1.0` | 0.3 credits/result |
| [`instagram/following-list`](https://docs.socq.ai/api-manual/instagram/following-list) | Collect public profiles followed by an Instagram account. | usernames | `relationship@1.0` | 0.3 credits/result |
| [`instagram/hashtag-posts`](https://docs.socq.ai/api-manual/instagram/hashtag-posts) | Collect public Instagram posts matching a hashtag. | hashtags | `post@1.0` | 0.5 credits/result |
| [`instagram/highlight-items`](https://docs.socq.ai/api-manual/instagram/highlight-items) | Collect public Instagram highlight items. | highlight_ids | `highlight@1.0` | 0.5 credits/result |
| [`instagram/post-info`](https://docs.socq.ai/api-manual/instagram/post-info) | Collect public Instagram post details. | urls | `post@1.0` | 0.5 credits/result |
| [`instagram/posts`](https://docs.socq.ai/api-manual/instagram/posts) | Instagram Post API | one of: urls; usernames | `post@1.0` | 0.34 credits/result |
| [`instagram/profiles`](https://docs.socq.ai/api-manual/instagram/profiles) | Collect public Instagram profile metadata and statistics. | usernames | `account@1.0` | 0.6 credits/result |
| [`instagram/reels`](https://docs.socq.ai/api-manual/instagram/reels) | Instagram Reel API | one of: urls; usernames | `reel-video@1.0` | 0.52 credits/result |
| [`instagram/reels-search`](https://docs.socq.ai/api-manual/instagram/reels-search) | Search public Instagram reels. | query | `reel-video@1.0` | 0.5 credits/result |
| [`instagram/search`](https://docs.socq.ai/api-manual/instagram/search) | Instagram Search API | query | `account@1.0` | 0.54 credits/result |
| [`instagram/story-highlights`](https://docs.socq.ai/api-manual/instagram/story-highlights) | Collect public Instagram story highlights. | usernames | `highlight@1.0` | 0.5 credits/result |
| [`instagram/tagged-posts`](https://docs.socq.ai/api-manual/instagram/tagged-posts) | Collect public posts that tag an Instagram profile. | usernames | `post@1.0` | 0.5 credits/result |
| [`instagram/transcript`](https://docs.socq.ai/api-manual/instagram/transcript) | Extract transcripts from public Instagram posts and reels. | urls | `transcript@1.0` | 0.7 credits/result |
| [`instagram/trending-reels`](https://docs.socq.ai/api-manual/instagram/trending-reels) | Collect public trending Instagram reels. | none | `reel-video@1.0` | 0.5 credits/result |

## Validated examples

### `instagram/audio-reels`

Typed MCP tool: `socq_instagram_audio_reels`

```json
{
  "audio_ids": [
    "123456789012345"
  ],
  "results_limit": 20
}
```

### `instagram/comments`

Typed MCP tool: `socq_instagram_comments`

```json
{
  "urls": [
    "https://www.instagram.com/p/ABC123xyz/"
  ]
}
```

### `instagram/followers-count`

Typed MCP tool: `socq_instagram_followers_count`

Provide usernames or public Instagram profile URLs. query is ignored and cannot be used as the only input.

```json
{
  "usernames": [
    "instagram"
  ]
}
```

### `instagram/followers-list`

Typed MCP tool: `socq_instagram_followers_list`

```json
{
  "usernames": [
    "instagram"
  ],
  "results_limit": 100
}
```

### `instagram/following-list`

Typed MCP tool: `socq_instagram_following_list`

```json
{
  "usernames": [
    "instagram"
  ],
  "results_limit": 100
}
```

### `instagram/hashtag-posts`

Typed MCP tool: `socq_instagram_hashtag_posts`

An explicit no-posts response completes successfully with an empty results.items list. Other access or service errors remain failures. Empty results follow the normal empty-result billing policy.

```json
{
  "hashtags": [
    "#travel"
  ],
  "results_limit": 20
}
```

### `instagram/highlight-items`

Typed MCP tool: `socq_instagram_highlight_items`

```json
{
  "highlight_ids": [
    "18067016518767507"
  ]
}
```

### `instagram/post-info`

Typed MCP tool: `socq_instagram_post_info`

```json
{
  "urls": [
    "https://www.instagram.com/p/ABC123xyz/"
  ]
}
```

### `instagram/posts`

Typed MCP tool: `socq_instagram_posts`

```json
{
  "usernames": [
    "instagram"
  ]
}
```

### `instagram/profiles`

Typed MCP tool: `socq_instagram_profiles`

```json
{
  "usernames": [
    "instagram"
  ]
}
```

### `instagram/reels`

Typed MCP tool: `socq_instagram_reels`

Provide usernames or public Instagram profile URLs. query is ignored and cannot be used as the only input.

```json
{
  "usernames": [
    "instagram"
  ]
}
```

### `instagram/reels-search`

Typed MCP tool: `socq_instagram_reels_search`

```json
{
  "query": "street photography",
  "results_limit": 20
}
```

### `instagram/search`

Typed MCP tool: `socq_instagram_search`

query is required and accepts keywords, not task instructions. Separate multiple terms with commas; punctuation such as @, #, quotes, periods, slashes and hyphens is unsupported. results_limit is 1 to 250. urls and usernames are deprecated and ignored.

```json
{
  "query": "travel photography"
}
```

### `instagram/story-highlights`

Typed MCP tool: `socq_instagram_story_highlights`

```json
{
  "usernames": [
    "instagram"
  ]
}
```

### `instagram/tagged-posts`

Typed MCP tool: `socq_instagram_tagged_posts`

```json
{
  "usernames": [
    "instagram"
  ],
  "results_limit": 20
}
```

### `instagram/transcript`

Typed MCP tool: `socq_instagram_transcript`

```json
{
  "urls": [
    "https://www.instagram.com/reel/DHsD6HGqJhp/"
  ]
}
```

### `instagram/trending-reels`

Typed MCP tool: `socq_instagram_trending_reels`

```json
{}
```
