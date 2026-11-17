# Shopdora OpenAPI Reference

## General Information

| Item | Description |
|------|------|
| Protocol | HTTPS / HTTP |
| Data Format | JSON |
| Encoding | UTF-8 |
| Base Path | `{HOST}/openapi/standard` |
| Host | `https://openapi.shopdora.cn/openapi/` |
| Request Method | All endpoints use POST |

## Authentication

All endpoints except `/standard/token` require the token in the request header:

```
Authorization: Bearer {access_token}
```

Or alternatively:

```
access_token: {access_token}
```

### Credentials

- `clientId`: Client ID, format `std_xxxxxxxx`
- `clientSecret`: Client secret, displayed only once upon creation/reset
- After resetting the secret, all tokens issued with the old secret become invalid immediately

### IP Whitelist

If configured, only whitelisted IPs can access the API. No restriction if not configured.

## Common Response Structure

```json
{
  "code": "0000",
  "errMsg": "",
  "tips": "",
  "data": {}
}
```

Date format: `yyyy-MM-dd HH:mm:ss`, timezone GMT+8.

## Error Codes

| code | Description |
|------|------|
| 0000 | Success |
| 0001 | Invalid parameter |
| 9990 | Invalid or expired token |
| 9992 | IP not in whitelist |
| 9993 | Rate limit exceeded (per minute) |
| 9996 | Account disabled |
| 9997 | Quota exhausted or no valid quota period |
| 9999 | System busy |

## Quota & Rate Limiting

### Billable Endpoints (per call)

- `POST /standard/token` → Free
- `POST /standard/queryBalance` → Free
- `POST /standard/cate/list` → Free
- `POST /standard/keyword/search` → **Charged**
- `POST /standard/product/search` → **Charged**
- `POST /standard/comment/get` → **Charged**

**Billing rules**: 1 call is deducted when the request succeeds (code=0000) AND returns non-empty data. For paginated endpoints, billing only applies if `list` is non-empty. For comment endpoint, billing only applies if the returned JSON is non-empty. Empty results are not charged.

### Rate-Limited Endpoints

The following endpoints are subject to per-minute rate limits (account-level config, 0 = unlimited):
`/standard/cate/list`, `/standard/keyword/search`, `/standard/product/search`, `/standard/comment/get`

Exceeding the limit returns 9993.

## Supported Sites

| site | Country |
|------|------|
| sg | Singapore |
| tw | Taiwan, China |
| my | Malaysia |
| ph | Philippines |
| th | Thailand |
| vn | Vietnam |
| id | Indonesia |
| br | Brazil |
| mx | Mexico |

---

## API Details

### POST /standard/token — Get Access Token

**No token required.**

Request body:

```json
{
  "clientId": "std_xxxxxxxx",
  "clientSecret": "your_secret"
}
```

Response data:

| Field | Type | Description |
|------|------|------|
| accessToken | string | Access token |
| tokenType | string | Always "Bearer" |
| expiresIn | integer | Validity in seconds, ~31 days by default |

### POST /standard/queryBalance — Query Balance

**Token required. Free, no rate limit.** Request body can be empty `{}`.

Response data:

| Field | Type | Description |
|------|------|------|
| clientId | string | Client ID |
| clientName | string | Client name |
| accountStatus | string | ACTIVE / DISABLED |
| periodId | long | Current quota period ID |
| periodStart | string | Quota period start time |
| periodEnd | string | Quota period end time |
| quotaLimit | integer | Max calls per period |
| quotaUsed | integer | Used calls |
| quotaRemaining | integer | Remaining calls |
| rateLimitPerMinute | integer | Per-minute rate limit, 0 = unlimited |
| rateLimitUsedThisMinute | integer | Calls used in current minute |
| rateLimitRemainingThisMinute | integer | Calls remaining in current minute |
| tokenExpiresIn | string | Current token expiration time |

### POST /standard/cate/list — Browse Categories

**Token required. Free quota, subject to rate limit.**

Request body:

| Field | Type | Required | Description |
|------|------|------|------|
| site | string | Yes | Site code |
| cateId | long | No | Category ID, omit or 0 for full tree |

Response `data` is a JSON string (needs `JSON.parse`). Single node structure:

| Field | Type | Description |
|------|------|------|
| cateId | long | Category ID |
| cateName | string | Category name (Chinese) |
| cateEnName | string | Category name (English) |
| leaf | boolean | Whether it's a leaf node |
| children | array | Child categories |

### POST /standard/keyword/search — Keyword Research

**Token required. Charged, rate-limited.**

Request body:

| Field | Type | Required | Description |
|------|------|------|------|
| site | string | Yes | Site code |
| keyword | string | No | Keyword, space-separated for fuzzy matching |
| cateIds | long[] | No | Category ID list |
| searchVolume | object | No | 30-day search volume range `{"min":1,"max":5}` |
| avgSearchVolume | object | No | Avg daily search volume range |
| searchVolumeIncRate | object | No | Monthly growth rate range, value x 100 |
| sortBy | string | No | Sort: searchVolume (default), searchVolumeIncRate |
| orderBy | integer | No | 1 = descending (default), 2 = ascending |
| pageNum | integer | No | Page number, starts at 1, default 1 |
| pageSize | integer | No | Page size, default 20, max 20 |

Paginated response data:

| Field | Type | Description |
|------|------|------|
| totalCount | integer | Total records |
| totalPage | integer | Total pages |
| currentPage | integer | Current page |
| list | array | Keyword list |

Key list item fields: keywordId, keyword, keywordCh, searchVolume, avgSearchVolume, searchVolumeIncRate, productNum, supplyDemandRatio, cateId, cateChPath, cateZhName, cateEnName, recommendPrice, avgPrice, avgRating, avgCommentNum, advNum, type, dates[], searchVolumeList[], refreshDay, itemFlowDate, updateTime

### POST /standard/product/search — Product Discovery

**Token required. Charged, rate-limited.**

Request body:

| Field | Type | Required | Description |
|------|------|------|------|
| site | string | Yes | Site code |
| month | integer | Yes | 30 = last 30 days, e.g. 202603 = monthly view |
| cateIds | long[] | No | Category ID list |
| keyword | string | No | Product keyword |
| price | object | No | Price range `{"min":100000,"max":5000000}` |
| likedCntM | object | No | Monthly new likes range |
| salesM | object | No | Monthly sales range |
| shelfTimeRange | string | No | Listed within: 7d/15d/1m/3m/6m/1y/2y |
| shelfTimeStart | string | No | Listing start date yyyyMMdd |
| shelfTimeEnd | string | No | Listing end date yyyyMMdd |
| sortBy | string | No | Sort: salesM (default), cateRank, salesGrowthRateM, likedCntM |
| orderBy | integer | No | 1 = descending (default), 2 = ascending |
| pageNum | integer | No | Page number, default 1 |
| pageSize | integer | No | Page size, default 20, max 20 |

Paginated response. Key list item fields: itemId, shopId, shopName, name, imageUrl, catId, cateChPath, catePath, price (÷100000 = local currency), avgPrice, skuAvgPrice, sales, salesM, salesDay, sales7day, salesGrowthRateM (÷100), salesAmountM, salesAmountDay, salesAmountGrowthRateM (÷100), likedCnt, likedCntM, ratingScore (÷10), ratingNumberTotal, ratingNumberM, ratingRateTotal (÷100), ratingRateM (÷100), cateRank, shelfTime, shopType (0=regular/1=preferred/2=MALL), sellerSource, skuCnt, status (1=active/2=delisted/3=deleted/4=Shopee-deleted), brand, brandId, attributes

### POST /standard/comment/get — Review Scraping

**Token required. Charged, rate-limited.**

Request body:

| Field | Type | Required | Description |
|------|------|------|------|
| site | string | Yes | Site code |
| shopId | long | Yes | Shop ID |
| itemId | long | Yes | Product ID |
| limit | integer | Yes | Page size, 1-20 |
| offset | integer | Yes | Offset, 0-3000 |

Response `data` is Shopee's raw JSON, commonly structured as `data.data`. Top-level data includes:
- data.ratings[] - Current page review list
- data.has_more - Whether there are more pages
- data.item_rating_count - Total reviews
- data.item_rating_star - Overall star rating
- data.item_rating_summary - Review summary stats

Key rating fields: cmtid, itemid, shopid, rating_star (1-5), comment, author_username, anonymous, like_count, ctime/mtime/submit_time (Unix seconds), status, images[], image_data[], videos[], detailed_rating (product_quality/seller_service/delivery_service), template_tags[], has_template_tag, is_repeated_purchase, is_super_review, product_items[], region

Pagination: first call offset=0, limit=20. If has_more=true, offset+=limit. Max offset is 3000.

---

## Recommended Call Sequence

1. POST /standard/token → Get access_token
2. POST /standard/queryBalance → Check quota, rate limit, token expiry
3. POST /standard/cate/list → Browse categories (optional)
4. POST /standard/keyword/search → Keyword research (charged)
5. POST /standard/product/search → Product discovery (charged)
6. POST /standard/comment/get → Review scraping (charged)

## Error Handling

| code | Action |
|------|------|
| 9990 | Re-acquire token |
| 9993 | Reduce request rate or retry later |
| 9997 | Contact platform to expand quota or wait for new period |
| 9999 | Exponential backoff retry |
