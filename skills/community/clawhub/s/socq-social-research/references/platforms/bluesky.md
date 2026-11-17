# Bluesky

Generated from SocQ Capability Registry schema `v1-9a87cca161f6`. Read this file when the request targets Bluesky.

## Endpoint selection

| Endpoint | Use for | Input choice | Standard schema | Cost |
| --- | --- | --- | --- | --- |
| [`bluesky/post`](https://docs.socq.ai/api-manual/bluesky/post) | Collect a public Bluesky post. | url | `post@1.0` | 0.19 credits/request |
| [`bluesky/profile`](https://docs.socq.ai/api-manual/bluesky/profile) | Collect a public Bluesky profile. | username | `account@1.0` | 0.19 credits/request |
| [`bluesky/user-posts`](https://docs.socq.ai/api-manual/bluesky/user-posts) | Collect one page of public Bluesky user posts. | one of: user_id; username | `post@1.0` | 0.19 credits/request |

## Validated examples

### `bluesky/post`

Typed MCP tool: `socq_bluesky_post`

```json
{
  "url": "https://bsky.app/profile/jay.bsky.team/post/3micofpyeys2g"
}
```

### `bluesky/profile`

Typed MCP tool: `socq_bluesky_profile`

```json
{
  "username": "jay.bsky.team"
}
```

### `bluesky/user-posts`

Typed MCP tool: `socq_bluesky_user_posts`

```json
{
  "username": "jay.bsky.team"
}
```
