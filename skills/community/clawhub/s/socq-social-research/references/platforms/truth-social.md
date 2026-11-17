# Truth Social

Generated from SocQ Capability Registry schema `v1-9a87cca161f6`. Read this file when the request targets Truth Social.

## Endpoint selection

| Endpoint | Use for | Input choice | Standard schema | Cost |
| --- | --- | --- | --- | --- |
| [`truth-social/post`](https://docs.socq.ai/api-manual/truth-social/post) | Collect a public Truth Social post. | url | `post@1.0` | 0.19 credits/request |
| [`truth-social/profile`](https://docs.socq.ai/api-manual/truth-social/profile) | Collect a public Truth Social profile. | username | `account@1.0` | 0.19 credits/request |
| [`truth-social/user-posts`](https://docs.socq.ai/api-manual/truth-social/user-posts) | Collect one page of public Truth Social user posts. | one of: user_id; username | `post@1.0` | 0.19 credits/request |

## Validated examples

### `truth-social/post`

Typed MCP tool: `socq_truth_social_post`

```json
{
  "url": "https://truthsocial.com/@realDonaldTrump/117091934703272898"
}
```

### `truth-social/profile`

Typed MCP tool: `socq_truth_social_profile`

```json
{
  "username": "realDonaldTrump"
}
```

### `truth-social/user-posts`

Typed MCP tool: `socq_truth_social_user_posts`

```json
{
  "username": "realDonaldTrump"
}
```
