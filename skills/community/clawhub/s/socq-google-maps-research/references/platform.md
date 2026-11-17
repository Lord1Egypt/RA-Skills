# Google Maps

Generated from SocQ Capability Registry schema `v1-9a87cca161f6`. Read this file when the request targets Google Maps.

## Endpoint selection

| Endpoint | Use for | Input choice | Standard schema | Cost |
| --- | --- | --- | --- | --- |
| [`google-maps/place-details`](https://docs.socq.ai/api-manual/google-maps/place-details) | Collect public Google Maps place details. | urls | `place@1.0` | 0.15 credits/result |
| [`google-maps/reviews`](https://docs.socq.ai/api-manual/google-maps/reviews) | Collect public Google Maps reviews. | urls | `review@1.0` | 0.15 credits/result |
| [`google-maps/search`](https://docs.socq.ai/api-manual/google-maps/search) | Search public Google Maps places. | location, query | `place@1.0` | 0.15 credits/result |

## Validated examples

### `google-maps/place-details`

Typed MCP tool: `socq_google_maps_place_details`

```json
{
  "urls": [
    "https://www.google.com/maps/place/Coffee%20Project%20New%20York%20%7C%20East%20Village/data=!4m7!3m6!1s0x89c2599b5a24d7fd:0x9e354f6cf514b9fc!8m2!3d40.7270884!4d-73.9893820!16s%2Fg%2F11c3svpqld!19sChIJ_dckWptZwokR_LkU9WxPNZ4?authuser=0&hl=en&rclk=1"
  ]
}
```

### `google-maps/reviews`

Typed MCP tool: `socq_google_maps_reviews`

```json
{
  "urls": [
    "https://www.google.com/maps/place/Coffee%20Project%20New%20York%20%7C%20East%20Village/data=!4m7!3m6!1s0x89c2599b5a24d7fd:0x9e354f6cf514b9fc!8m2!3d40.7270884!4d-73.9893820!16s%2Fg%2F11c3svpqld!19sChIJ_dckWptZwokR_LkU9WxPNZ4?authuser=0&hl=en&rclk=1"
  ],
  "days_limit": 3650,
  "results_limit": 3
}
```

### `google-maps/search`

Typed MCP tool: `socq_google_maps_search`

```json
{
  "query": "coffee",
  "location": "New York, NY",
  "country": "US",
  "results_limit": 3
}
```
