# Tiktok Ad Library

Generated from SocQ Capability Registry schema `v1-9a87cca161f6`. Read this file when the request targets Tiktok Ad Library.

## Endpoint selection

| Endpoint | Use for | Input choice | Standard schema | Cost |
| --- | --- | --- | --- | --- |
| [`tiktok-ad-library/ad`](https://docs.socq.ai/api-manual/tiktok-ad-library/ad) | Collect public TikTok ad details. | url | `ad@1.0` | 0.5 credits/result |
| [`tiktok-ad-library/search`](https://docs.socq.ai/api-manual/tiktok-ad-library/search) | Search public TikTok ads. | query | `ad@1.0` | 0.5 credits/result |

## Validated examples

### `tiktok-ad-library/ad`

Typed MCP tool: `socq_tiktok_ad_library_ad`

```json
{
  "url": "https://library.tiktok.com/ads/detail/?id=1871655924410641"
}
```

### `tiktok-ad-library/search`

Typed MCP tool: `socq_tiktok_ad_library_search`

```json
{
  "query": "Anysphere",
  "results_limit": 12
}
```
