# Google Ad Library

Generated from SocQ Capability Registry schema `v1-9a87cca161f6`. Read this file when the request targets Google Ad Library.

## Endpoint selection

| Endpoint | Use for | Input choice | Standard schema | Cost |
| --- | --- | --- | --- | --- |
| [`google-ad-library/ad`](https://docs.socq.ai/api-manual/google-ad-library/ad) | Collect public Google ad details. | url | `ad@1.0` | 0.5 credits/result |
| [`google-ad-library/advertiser-search`](https://docs.socq.ai/api-manual/google-ad-library/advertiser-search) | Search public Google advertisers. | query | `advertiser@1.0` | 0.5 credits/result |
| [`google-ad-library/company-ads`](https://docs.socq.ai/api-manual/google-ad-library/company-ads) | Collect public Google company ads. | one of: advertiser_id; domain | `ad@1.0` | 0.5 credits/result |

## Validated examples

### `google-ad-library/ad`

Typed MCP tool: `socq_google_ad_library_ad`

```json
{
  "url": "https://adstransparency.google.com/advertiser/AR01614014350098432001/creative/CR10449491775734153217"
}
```

### `google-ad-library/advertiser-search`

Typed MCP tool: `socq_google_ad_library_advertiser_search`

```json
{
  "query": "Nike",
  "region": "US"
}
```

### `google-ad-library/company-ads`

Typed MCP tool: `socq_google_ad_library_company_ads`

```json
{
  "domain": "lululemon.com",
  "results_limit": 40
}
```
