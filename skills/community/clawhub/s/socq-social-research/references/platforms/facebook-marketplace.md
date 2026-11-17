# Facebook Marketplace

Generated from SocQ Capability Registry schema `v1-9a87cca161f6`. Read this file when the request targets Facebook Marketplace.

## Endpoint selection

| Endpoint | Use for | Input choice | Standard schema | Cost |
| --- | --- | --- | --- | --- |
| [`facebook-marketplace/item`](https://docs.socq.ai/api-manual/facebook-marketplace/item) | Facebook Marketplace Item API | urls | `listing@1.0` | 0.6 credits/result |
| [`facebook-marketplace/location-search`](https://docs.socq.ai/api-manual/facebook-marketplace/location-search) | Facebook Marketplace Location Search API | query | `marketplace-location@1.0` | 0.3 credits/result |
| [`facebook-marketplace/search`](https://docs.socq.ai/api-manual/facebook-marketplace/search) | Facebook Marketplace Search API | latitude, longitude, query | `listing@1.0` | 0.7 credits/result |

## Validated examples

### `facebook-marketplace/item`

Typed MCP tool: `socq_facebook_marketplace_item`

```json
{
  "urls": [
    "https://www.facebook.com/marketplace/item/123456789012345/"
  ]
}
```

### `facebook-marketplace/location-search`

Typed MCP tool: `socq_facebook_marketplace_location_search`

```json
{
  "query": "San Francisco"
}
```

### `facebook-marketplace/search`

Typed MCP tool: `socq_facebook_marketplace_search`

```json
{
  "query": "standing desk",
  "latitude": 37.7749,
  "longitude": -122.4194
}
```
