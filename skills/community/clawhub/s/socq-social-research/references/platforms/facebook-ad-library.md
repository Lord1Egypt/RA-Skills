# Facebook Ad Library

Generated from SocQ Capability Registry schema `v1-9a87cca161f6`. Read this file when the request targets Facebook Ad Library.

## Endpoint selection

| Endpoint | Use for | Input choice | Standard schema | Cost |
| --- | --- | --- | --- | --- |
| [`facebook-ad-library/ad`](https://docs.socq.ai/api-manual/facebook-ad-library/ad) | Facebook Ad Library Ad API | url | `ad@1.0` | 0.6 credits/result |
| [`facebook-ad-library/company-ads`](https://docs.socq.ai/api-manual/facebook-ad-library/company-ads) | Facebook Ad Library Company Ads API | page_id | `ad@1.0` | 0.5 credits/result |
| [`facebook-ad-library/company-search`](https://docs.socq.ai/api-manual/facebook-ad-library/company-search) | Facebook Ad Library Company Search API | query | `advertiser@1.0` | 0.5 credits/result |
| [`facebook-ad-library/search`](https://docs.socq.ai/api-manual/facebook-ad-library/search) | Facebook Ad Library Search API | query | `ad@1.0` | 0.5 credits/result |

## Validated examples

### `facebook-ad-library/ad`

Typed MCP tool: `socq_facebook_ad_library_ad`

```json
{
  "url": "https://www.facebook.com/ads/library/?id=123456789012345"
}
```

### `facebook-ad-library/company-ads`

Typed MCP tool: `socq_facebook_ad_library_company_ads`

```json
{
  "page_id": "20531316728"
}
```

### `facebook-ad-library/company-search`

Typed MCP tool: `socq_facebook_ad_library_company_search`

```json
{
  "query": "Nike"
}
```

### `facebook-ad-library/search`

Typed MCP tool: `socq_facebook_ad_library_search`

```json
{
  "query": "running shoes"
}
```
