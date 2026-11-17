# Kwai

Generated from SocQ Capability Registry schema `v1-9a87cca161f6`. Read this file when the request targets Kwai.

## Endpoint selection

| Endpoint | Use for | Input choice | Standard schema | Cost |
| --- | --- | --- | --- | --- |
| [`kwai/post`](https://docs.socq.ai/api-manual/kwai/post) | Collect a public Kwai post. | url | `post@1.0` | 0.19 credits/request |
| [`kwai/profile`](https://docs.socq.ai/api-manual/kwai/profile) | Collect a public Kwai profile. | one of: url; username | `account@1.0` | 0.19 credits/request |
| [`kwai/user-posts`](https://docs.socq.ai/api-manual/kwai/user-posts) | Collect one page of public Kwai user posts. | one of: url; username | `post@1.0` | 0.19 credits/request |

## Validated examples

### `kwai/post`

Typed MCP tool: `socq_kwai_post`

```json
{
  "url": "https://www.kwai.com/@ShortShortz8/photo/5235021727595785285"
}
```

### `kwai/profile`

Typed MCP tool: `socq_kwai_profile`

```json
{
  "url": "https://www.kwai.com/@ShortShortz8"
}
```

### `kwai/user-posts`

Typed MCP tool: `socq_kwai_user_posts`

```json
{
  "url": "https://www.kwai.com/@ShortShortz8"
}
```
