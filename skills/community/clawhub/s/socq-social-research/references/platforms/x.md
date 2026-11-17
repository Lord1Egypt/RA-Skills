# X

Generated from SocQ Capability Registry schema `v1-9a87cca161f6`. Read this file when the request targets X.

## Endpoint selection

| Endpoint | Use for | Input choice | Standard schema | Cost |
| --- | --- | --- | --- | --- |
| [`x/community`](https://docs.socq.ai/api-manual/x/community) | Get public X community metadata, member counts, rules and membership policies. | urls | `community@1.0` | 0.5 credits/result |
| [`x/community-posts`](https://docs.socq.ai/api-manual/x/community-posts) | Collect public posts from X communities in creation-time order. | urls | `post@1.0` | 0.7 credits/result |
| [`x/followers-list`](https://docs.socq.ai/api-manual/x/followers-list) | Collect public X follower profiles. | usernames | `relationship@1.0` | 0.5 credits/result |
| [`x/following-list`](https://docs.socq.ai/api-manual/x/following-list) | Collect public X followed profiles. | usernames | `relationship@1.0` | 0.5 credits/result |
| [`x/mentions`](https://docs.socq.ai/api-manual/x/mentions) | Collect public posts that mention an X account. | usernames | `post@1.0` | 0.7 credits/result |
| [`x/post-quotes`](https://docs.socq.ai/api-manual/x/post-quotes) | Collect public quotes of X posts. | urls | `post@1.0` | 0.5 credits/result |
| [`x/post-replies`](https://docs.socq.ai/api-manual/x/post-replies) | Collect public replies to X posts. | urls | `comment@1.0` | 0.5 credits/result |
| [`x/post-retweeters`](https://docs.socq.ai/api-manual/x/post-retweeters) | Collect public profiles that reposted X posts. | urls | `relationship@1.0` | 0.5 credits/result |
| [`x/posts`](https://docs.socq.ai/api-manual/x/posts) | X Posts API | urls | `post@1.0` | 0.5 credits/result |
| [`x/profiles`](https://docs.socq.ai/api-manual/x/profiles) | X Profiles API | usernames | `account@1.0` | 0.6 credits/result |
| [`x/search`](https://docs.socq.ai/api-manual/x/search) | X Search API | query | `post@1.0` | 0.7 credits/result |
| [`x/search-users`](https://docs.socq.ai/api-manual/x/search-users) | Search public X accounts by keyword. | query | `account@1.0` | 0.6 credits/result |
| [`x/thread-context`](https://docs.socq.ai/api-manual/x/thread-context) | Collect the target X post, its ancestors and replies while preserving thread relationships. | urls | `thread-post@1.0` | 0.5 credits/result |
| [`x/trends`](https://docs.socq.ai/api-manual/x/trends) | Collect public X trends by location identifier. | woeids | `hashtag-trend@1.0` | 0.5 credits/result |
| [`x/user-posts`](https://docs.socq.ai/api-manual/x/user-posts) | X User Posts API | usernames | `post@1.0` | 0.5 credits/result |

## Validated examples

### `x/community`

Typed MCP tool: `socq_x_community`

Provide public X community URLs in urls, using /i/communities/{numeric_id}.

```json
{
  "urls": [
    "https://x.com/i/communities/1493446837214187523"
  ]
}
```

### `x/community-posts`

Typed MCP tool: `socq_x_community_posts`

Provide public X community URLs in urls. results_limit applies to each URL, defaults to 100, and must be a multiple of 20 between 20 and 2000.

```json
{
  "urls": [
    "https://x.com/i/communities/1493446837214187523"
  ],
  "results_limit": 20
}
```

### `x/followers-list`

Typed MCP tool: `socq_x_followers_list`

```json
{
  "usernames": [
    "@X"
  ],
  "results_limit": 200
}
```

### `x/following-list`

Typed MCP tool: `socq_x_following_list`

```json
{
  "usernames": [
    "@X"
  ],
  "results_limit": 200
}
```

### `x/mentions`

Typed MCP tool: `socq_x_mentions`

```json
{
  "usernames": [
    "@OpenAI"
  ],
  "results_limit": 20
}
```

### `x/post-quotes`

Typed MCP tool: `socq_x_post_quotes`

```json
{
  "urls": [
    "https://x.com/X/status/1234567890123456789"
  ],
  "results_limit": 20
}
```

### `x/post-replies`

Typed MCP tool: `socq_x_post_replies`

```json
{
  "urls": [
    "https://x.com/X/status/1234567890123456789"
  ],
  "results_limit": 20
}
```

### `x/post-retweeters`

Typed MCP tool: `socq_x_post_retweeters`

```json
{
  "urls": [
    "https://x.com/X/status/1234567890123456789"
  ],
  "results_limit": 100
}
```

### `x/posts`

Typed MCP tool: `socq_x_posts`

```json
{
  "urls": [
    "https://x.com/X/status/1234567890123456789"
  ]
}
```

### `x/profiles`

Typed MCP tool: `socq_x_profiles`

```json
{
  "usernames": [
    "@X"
  ]
}
```

### `x/search`

Typed MCP tool: `socq_x_search`

```json
{
  "query": "AI agents"
}
```

### `x/search-users`

Typed MCP tool: `socq_x_search_users`

```json
{
  "query": "OpenAI",
  "results_limit": 20
}
```

### `x/thread-context`

Typed MCP tool: `socq_x_thread_context`

Provide X post URLs in urls. results_limit applies to each URL, defaults to 100, and accepts integers from 1 to 2000. Results retain the target post and its thread relationships.

```json
{
  "urls": [
    "https://x.com/OpenAI/status/1890818505164038356"
  ],
  "results_limit": 20
}
```

### `x/trends`

Typed MCP tool: `socq_x_trends`

```json
{
  "woeids": [
    "1"
  ],
  "results_limit": 100
}
```

### `x/user-posts`

Typed MCP tool: `socq_x_user_posts`

```json
{
  "usernames": [
    "@X"
  ]
}
```
