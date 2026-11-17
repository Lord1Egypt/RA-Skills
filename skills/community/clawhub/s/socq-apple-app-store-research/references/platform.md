# Apple App Store

Generated from SocQ Capability Registry schema `v1-9a87cca161f6`. Read this file when the request targets Apple App Store.

## Endpoint selection

| Endpoint | Use for | Input choice | Standard schema | Cost |
| --- | --- | --- | --- | --- |
| [`apple-app-store/app-detail`](https://docs.socq.ai/api-manual/apple-app-store/app-detail) | Collect public Apple App Store app details. | urls | `app@1.0` | 0.15 credits/result |
| [`apple-app-store/app-reviews`](https://docs.socq.ai/api-manual/apple-app-store/app-reviews) | Collect public Apple App Store reviews. | urls | `review@1.0` | 0.15 credits/result |
| [`apple-app-store/rankings`](https://docs.socq.ai/api-manual/apple-app-store/rankings) | Collect public Apple App Store category rankings. | urls | `app@1.0` | 0.15 credits/result |

## Validated examples

### `apple-app-store/app-detail`

Typed MCP tool: `socq_apple_app_store_app_detail`

```json
{
  "urls": [
    "https://apps.apple.com/us/app/chatgpt/id6448311069"
  ]
}
```

### `apple-app-store/app-reviews`

Typed MCP tool: `socq_apple_app_store_app_reviews`

```json
{
  "urls": [
    "https://apps.apple.com/us/app/chatgpt/id6448311069"
  ],
  "results_limit": 3
}
```

### `apple-app-store/rankings`

Typed MCP tool: `socq_apple_app_store_rankings`

```json
{
  "urls": [
    "https://apps.apple.com/us/iphone/charts/6007"
  ],
  "results_limit": 3
}
```
