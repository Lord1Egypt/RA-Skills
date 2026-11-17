# Rednote

Generated from SocQ Capability Registry schema `v1-9a87cca161f6`. Read this file when the request targets Rednote.

## Endpoint selection

| Endpoint | Use for | Input choice | Standard schema | Cost |
| --- | --- | --- | --- | --- |
| [`rednote/comment-replies`](https://docs.socq.ai/api-manual/rednote/comment-replies) | Collect one page of public Rednote comment replies. | comment_id, url | `comment@1.0` | 1 credits/request |
| [`rednote/home-recommendations`](https://docs.socq.ai/api-manual/rednote/home-recommendations) | Collect public Rednote home recommendations. | none | `post@1.0` | 1 credits/request |
| [`rednote/note-comments`](https://docs.socq.ai/api-manual/rednote/note-comments) | Collect one page of public Rednote note comments. | url | `comment@1.0` | 1 credits/request |
| [`rednote/note-detail`](https://docs.socq.ai/api-manual/rednote/note-detail) | Collect public Rednote note details. | url | `post@1.0` | 1 credits/request |
| [`rednote/search-notes`](https://docs.socq.ai/api-manual/rednote/search-notes) | Search public Rednote notes. | query | `post@1.0` | 1 credits/request |
| [`rednote/search-users`](https://docs.socq.ai/api-manual/rednote/search-users) | Search public Rednote users. | query | `account@1.0` | 1 credits/request |
| [`rednote/user-notes`](https://docs.socq.ai/api-manual/rednote/user-notes) | Collect one page of public Rednote user notes. | one of: url; user_id | `post@1.0` | 1 credits/request |
| [`rednote/user-profile`](https://docs.socq.ai/api-manual/rednote/user-profile) | Collect a public Rednote profile. | one of: url; user_id | `account@1.0` | 1 credits/request |

## Validated examples

### `rednote/comment-replies`

Typed MCP tool: `socq_rednote_comment_replies`

```json
{
  "url": "https://www.xiaohongshu.com/explore/6a6174d6000000001d02013b?xsec_token=AB4sNisHvFy2q4C5ujG23AV858osk5rYC63eCgf8YTVOI%3D&xsec_source=pc_feed",
  "comment_id": "6a6327f6000000002b026c1d"
}
```

### `rednote/home-recommendations`

Typed MCP tool: `socq_rednote_home_recommendations`

```json
{
  "category": "homefeed_recommend",
  "media_type": "all",
  "results_limit": 3
}
```

### `rednote/note-comments`

Typed MCP tool: `socq_rednote_note_comments`

```json
{
  "url": "https://www.xiaohongshu.com/explore/6a6174d6000000001d02013b?xsec_token=AB4sNisHvFy2q4C5ujG23AV858osk5rYC63eCgf8YTVOI%3D&xsec_source=pc_feed"
}
```

### `rednote/note-detail`

Typed MCP tool: `socq_rednote_note_detail`

```json
{
  "url": "https://www.xiaohongshu.com/explore/6a2f423d000000001003cb36?xsec_token=ABtexB6bX5HgLD42SFrK1scGUmSO8YV5_isaLrDy9sLxQ%3D"
}
```

### `rednote/search-notes`

Typed MCP tool: `socq_rednote_search_notes`

```json
{
  "query": "旅行攻略",
  "sort_by": "general",
  "media_type": "all"
}
```

### `rednote/search-users`

Typed MCP tool: `socq_rednote_search_users`

```json
{
  "query": "摄影"
}
```

### `rednote/user-notes`

Typed MCP tool: `socq_rednote_user_notes`

```json
{
  "user_id": "65d8c7d40000000005033a6b"
}
```

### `rednote/user-profile`

Typed MCP tool: `socq_rednote_user_profile`

```json
{
  "user_id": "65d8c7d40000000005033a6b"
}
```
