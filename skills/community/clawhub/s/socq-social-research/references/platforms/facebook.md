# Facebook

Generated from SocQ Capability Registry schema `v1-9a87cca161f6`. Read this file when the request targets Facebook.

## Endpoint selection

| Endpoint | Use for | Input choice | Standard schema | Cost |
| --- | --- | --- | --- | --- |
| [`facebook/ad-transcript`](https://docs.socq.ai/api-manual/facebook/ad-transcript) | Extract transcripts from public Facebook ads. | urls | `transcript@1.0` | 0.5 credits/result |
| [`facebook/comment-replies`](https://docs.socq.ai/api-manual/facebook/comment-replies) | Collect public Facebook comment replies. | one of: comment_id + url; expansion_token + feedback_id | `comment@1.0` | 0.3 credits/result |
| [`facebook/comments`](https://docs.socq.ai/api-manual/facebook/comments) | Facebook Comments API | urls | `comment@1.0` | 0.3 credits/result |
| [`facebook/company-reviews`](https://docs.socq.ai/api-manual/facebook/company-reviews) | Collect public Facebook company reviews. | urls | `review@1.0` | 0.5 credits/result |
| [`facebook/event-details`](https://docs.socq.ai/api-manual/facebook/event-details) | Collect public Facebook event details. | urls | `event@1.0` | 0.5 credits/result |
| [`facebook/events-search`](https://docs.socq.ai/api-manual/facebook/events-search) | Search public Facebook events by keyword. | query | `event@1.0` | 0.6 credits/result |
| [`facebook/group-posts`](https://docs.socq.ai/api-manual/facebook/group-posts) | Collect posts from public Facebook groups. | urls | `post@1.0` | 1.2 credits/result |
| [`facebook/pages`](https://docs.socq.ai/api-manual/facebook/pages) | Facebook Page API | urls | `account@1.0` | 2.4 credits/result |
| [`facebook/posts`](https://docs.socq.ai/api-manual/facebook/posts) | Facebook Posts API | urls | `post@1.0` | 1 credits/result |
| [`facebook/profile-events`](https://docs.socq.ai/api-manual/facebook/profile-events) | Collect public Facebook profile events. | urls | `event@1.0` | 0.6 credits/result |
| [`facebook/profile-photos`](https://docs.socq.ai/api-manual/facebook/profile-photos) | Collect public Facebook profile photos. | urls | `reel-video@1.0` | 0.5 credits/result |
| [`facebook/profiles`](https://docs.socq.ai/api-manual/facebook/profiles) | Collect public Facebook profile details. | urls | `account@1.0` | 1.2 credits/result |
| [`facebook/reels`](https://docs.socq.ai/api-manual/facebook/reels) | Collect public Facebook profile reels. | urls | `reel-video@1.0` | 0.7 credits/result |
| [`facebook/video-transcript`](https://docs.socq.ai/api-manual/facebook/video-transcript) | Extract transcripts from public Facebook videos and reels. | urls | `transcript@1.0` | 0.7 credits/result |

## Validated examples

### `facebook/ad-transcript`

Typed MCP tool: `socq_facebook_ad_transcript`

```json
{
  "urls": [
    "https://www.facebook.com/ads/library/?id=123456789012345"
  ]
}
```

### `facebook/comment-replies`

Typed MCP tool: `socq_facebook_comment_replies`

```json
{
  "url": "https://www.facebook.com/NASA/posts/would-you-lie-in-bed-for-60-days-for-scientific-research11-volunteers-did-exactl/1271494461012594/",
  "comment_id": "Y29tbWVudDoxMjcxNDk0NDYxMDEyNTk0XzU4NzcxOTAzMTA0Mjk5MQ==",
  "results_limit": 20
}
```

### `facebook/comments`

Typed MCP tool: `socq_facebook_comments`

```json
{
  "urls": [
    "https://www.facebook.com/nasa/posts/1234567890"
  ]
}
```

### `facebook/company-reviews`

Typed MCP tool: `socq_facebook_company_reviews`

```json
{
  "urls": [
    "https://www.facebook.com/PepsiCo/reviews/"
  ],
  "results_limit": 20
}
```

### `facebook/event-details`

Typed MCP tool: `socq_facebook_event_details`

```json
{
  "urls": [
    "https://www.facebook.com/events/2255360061870188/"
  ]
}
```

### `facebook/events-search`

Typed MCP tool: `socq_facebook_events_search`

```json
{
  "query": "technology conference",
  "results_limit": 20
}
```

### `facebook/group-posts`

Typed MCP tool: `socq_facebook_group_posts`

```json
{
  "urls": [
    "https://www.facebook.com/groups/1270525996445602/"
  ]
}
```

### `facebook/pages`

Typed MCP tool: `socq_facebook_pages`

Provide public Facebook page/profile URLs in urls. Keyword search, username-only input, and individual post/reel URLs are not supported. Legacy query and usernames fields are ignored when valid urls are supplied.

```json
{
  "urls": [
    "https://www.facebook.com/nasa"
  ]
}
```

### `facebook/posts`

Typed MCP tool: `socq_facebook_posts`

Provide public Facebook page/profile URLs in urls. Keyword search, username-only input, and individual post/reel URLs are not supported. Legacy query and usernames fields are ignored when valid urls are supplied.

```json
{
  "urls": [
    "https://www.facebook.com/nasa"
  ]
}
```

### `facebook/profile-events`

Typed MCP tool: `socq_facebook_profile_events`

```json
{
  "urls": [
    "https://www.facebook.com/NASA"
  ],
  "results_limit": 20
}
```

### `facebook/profile-photos`

Typed MCP tool: `socq_facebook_profile_photos`

```json
{
  "urls": [
    "https://www.facebook.com/NASA"
  ],
  "results_limit": 20
}
```

### `facebook/profiles`

Typed MCP tool: `socq_facebook_profiles`

```json
{
  "urls": [
    "https://www.facebook.com/NASA"
  ]
}
```

### `facebook/reels`

Typed MCP tool: `socq_facebook_reels`

Provide Facebook page/profile URLs to collect their reels. A single /reel/... video URL is not a profile URL.

```json
{
  "urls": [
    "https://www.facebook.com/NASA"
  ],
  "results_limit": 20
}
```

### `facebook/video-transcript`

Typed MCP tool: `socq_facebook_video_transcript`

```json
{
  "urls": [
    "https://www.facebook.com/reel/1535656380759655"
  ]
}
```
