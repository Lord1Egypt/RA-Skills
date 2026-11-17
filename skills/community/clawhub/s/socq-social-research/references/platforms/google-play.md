# Google Play

Generated from SocQ Capability Registry schema `v1-9a87cca161f6`. Read this file when the request targets Google Play.

## Endpoint selection

| Endpoint | Use for | Input choice | Standard schema | Cost |
| --- | --- | --- | --- | --- |
| [`google-play/app-detail`](https://docs.socq.ai/api-manual/google-play/app-detail) | Collect public Google Play app details. | urls | `app@1.0` | 0.15 credits/result |
| [`google-play/app-rankings`](https://docs.socq.ai/api-manual/google-play/app-rankings) | Collect public Google Play category rankings. | urls | `app@1.0` | 0.15 credits/result |
| [`google-play/app-reviews`](https://docs.socq.ai/api-manual/google-play/app-reviews) | Collect public Google Play app reviews. | urls | `review@1.0` | 0.15 credits/result |

## Validated examples

### `google-play/app-detail`

Typed MCP tool: `socq_google_play_app_detail`

```json
{
  "urls": [
    "https://play.google.com/store/apps/details?id=com.openai.chatgpt"
  ]
}
```

### `google-play/app-rankings`

Typed MCP tool: `socq_google_play_app_rankings`

```json
{
  "urls": [
    "https://play.google.com/store/apps/collection/topselling_free"
  ],
  "results_limit": 3
}
```

### `google-play/app-reviews`

Typed MCP tool: `socq_google_play_app_reviews`

```json
{
  "urls": [
    "https://play.google.com/store/apps/details?id=com.openai.chatgpt"
  ],
  "country": "US",
  "results_limit": 3
}
```
