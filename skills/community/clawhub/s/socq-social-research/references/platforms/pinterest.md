# Pinterest

Generated from SocQ Capability Registry schema `v1-9a87cca161f6`. Read this file when the request targets Pinterest.

## Endpoint selection

| Endpoint | Use for | Input choice | Standard schema | Cost |
| --- | --- | --- | --- | --- |
| [`pinterest/pins`](https://docs.socq.ai/api-manual/pinterest/pins) | Pinterest Pins API | urls | `post@1.0` | 0.5 credits/result |
| [`pinterest/profiles`](https://docs.socq.ai/api-manual/pinterest/profiles) | Pinterest Profiles API | urls | `account@1.0` | 0.6 credits/result |
| [`pinterest/search`](https://docs.socq.ai/api-manual/pinterest/search) | Pinterest Search API | query | `post@1.0` | 0.6 credits/result |
| [`pinterest/user-pins`](https://docs.socq.ai/api-manual/pinterest/user-pins) | Pinterest User Pins API | urls | `post@1.0` | 0.5 credits/result |

## Validated examples

### `pinterest/pins`

Typed MCP tool: `socq_pinterest_pins`

```json
{
  "urls": [
    "https://www.pinterest.com/pin/123456789012345678/"
  ]
}
```

### `pinterest/profiles`

Typed MCP tool: `socq_pinterest_profiles`

```json
{
  "urls": [
    "https://www.pinterest.com/pinterest/"
  ]
}
```

### `pinterest/search`

Typed MCP tool: `socq_pinterest_search`

```json
{
  "query": "home office ideas"
}
```

### `pinterest/user-pins`

Typed MCP tool: `socq_pinterest_user_pins`

```json
{
  "urls": [
    "https://www.pinterest.com/pinterest/"
  ]
}
```
