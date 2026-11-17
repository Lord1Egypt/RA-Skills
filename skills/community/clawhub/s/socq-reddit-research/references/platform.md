# Reddit

Generated from SocQ Capability Registry schema `v1-9a87cca161f6`. Read this file when the request targets Reddit.

## Endpoint selection

| Endpoint | Use for | Input choice | Standard schema | Cost |
| --- | --- | --- | --- | --- |
| [`reddit/comments`](https://docs.socq.ai/api-manual/reddit/comments) | Reddit Comments API | urls | `comment@1.0` | 0.3 credits/result |
| [`reddit/posts`](https://docs.socq.ai/api-manual/reddit/posts) | Reddit Posts API | urls | `post@1.0` | 0.5 credits/result |
| [`reddit/search`](https://docs.socq.ai/api-manual/reddit/search) | Reddit Search API | query | `post@1.0` | 0.6 credits/result |
| [`reddit/subreddit-details`](https://docs.socq.ai/api-manual/reddit/subreddit-details) | Collect public Reddit community metadata. | urls | `account@1.0` | 0.5 credits/result |
| [`reddit/subreddit-posts`](https://docs.socq.ai/api-manual/reddit/subreddit-posts) | Reddit Subreddit Posts API | urls | `post@1.0` | 0.5 credits/result |
| [`reddit/subreddit-search`](https://docs.socq.ai/api-manual/reddit/subreddit-search) | Search public posts inside one Reddit community. | query, urls | `post@1.0` | 0.6 credits/result |

## Validated examples

### `reddit/comments`

Typed MCP tool: `socq_reddit_comments`

```json
{
  "urls": [
    "https://www.reddit.com/r/technology/comments/abc123/example_post/"
  ]
}
```

### `reddit/posts`

Typed MCP tool: `socq_reddit_posts`

```json
{
  "urls": [
    "https://www.reddit.com/r/technology/comments/abc123/example_post/"
  ]
}
```

### `reddit/search`

Typed MCP tool: `socq_reddit_search`

```json
{
  "query": "AI agents"
}
```

### `reddit/subreddit-details`

Typed MCP tool: `socq_reddit_subreddit_details`

```json
{
  "urls": [
    "https://www.reddit.com/r/technology/"
  ]
}
```

### `reddit/subreddit-posts`

Typed MCP tool: `socq_reddit_subreddit_posts`

```json
{
  "urls": [
    "https://www.reddit.com/r/technology/"
  ]
}
```

### `reddit/subreddit-search`

Typed MCP tool: `socq_reddit_subreddit_search`

```json
{
  "query": "AI agents",
  "urls": [
    "https://www.reddit.com/r/technology/"
  ],
  "results_limit": 20
}
```
