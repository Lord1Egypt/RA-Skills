---
name: shopdora-shopee-en
description: |
  This skill should be used when the user wants to perform cross-border
  e-commerce data analysis on Shopee platforms, including: keyword research,
  product discovery & search, review scraping & analysis, category browsing,
  and balance/account queries.
  Trigger keywords include: keyword research, product research, product discovery,
  comment analysis, review analysis, review scraping, Shopee selection, seller analytics,
  competitor analysis, category browse, check balance, shopee data, shopdora, hot products,
  trending keywords, product search, cross-border ecommerce.
  Also triggered when the user mentions Shopee site codes (sg/tw/my/ph/th/vn/id/br/mx)
  or country names (Singapore/Taiwan/Malaysia/Philippines/Thailand/Vietnam/Indonesia/Brazil/Mexico)
  in the context of data analysis or market research.
agent_created: true
---

# Shopdora - Shopee Product Research & Keyword Analytics Tool

## Overview

Leverage the Shopdora OpenAPI to perform cross-border ecommerce data analysis on Shopee across all supported sites. Capabilities include keyword research, product discovery, review scraping, category browsing, and balance queries.

**Important prerequisite**: Using this skill requires registering an account on the [Shopdora website](https://www.shopdora.com) and activating the API service. This is a paid service — contact the official customer service (WeCom) on the website for pricing details.

---

## Typical Use Cases

You can ask questions in plain English, for example:

- "What are the hottest products in the beauty category on Shopee Thailand?"
- "Show me trending keywords for phone cases on Shopee Singapore"
- "How much quota is left on my account?"
- "Get reviews for product ID xxx from Shopee Taiwan"
- "What categories are available on Shopee Malaysia?"

---

## Prerequisites: Credential Setup

### Check Configuration

Before making any API call, check if the local credential file `~/.shopdora/config.json` exists:

```bash
cat ~/.shopdora/config.json 2>/dev/null
```

### First-Time Setup — Guide the User

If the config file doesn't exist, reply to the user:

> This is a paid service. Please visit https://www.shopdora.com and contact official customer service to get your token. Once you have your `clientId` and `clientSecret`, share them with me and I'll set it up.

After receiving the credentials, create the config file:

```bash
mkdir -p ~/.shopdora
```

Then write the JSON config with the user-provided `clientId` and `clientSecret`.

### Config File Format

```json
{
  "clientId": "std_xxxxxxxx",
  "clientSecret": "your_secret_here"
}
```

---

## Site Name Mapping

Users may refer to sites by name rather than code. Auto-convert using this mapping:

| User might say | Maps to site code |
|---|---|
| Singapore, sg | `sg` |
| Taiwan, tw | `tw` |
| Malaysia, my | `my` |
| Philippines, ph | `ph` |
| Thailand, th | `th` |
| Vietnam, vn | `vn` |
| Indonesia, id | `id` |
| Brazil, br | `br` |
| Mexico, mx | `mx` |

If the user hasn't specified a site, ask which site they want to query.

---

## Core Workflow

**Standard call sequence**: Regardless of the user's request, always follow this order:

1. Check credentials → Read `~/.shopdora/config.json`
2. Get token → Check if `~/.shopdora/token.json` is valid; re-acquire if expired
3. Check local cache → Serve from cache for identical requests within 24 hours (no cost — see "Local Cache" section below)
4. Confirm key parameters → Before calling any paid endpoint, confirm site, keyword, time range, etc. with the user (see "Pre-Call Confirmation" section below)
5. Optional: Query balance → Optionally check balance to confirm sufficient quota before execution
6. Execute request → Call the appropriate endpoint based on user intent (keyword/product/review/category)
7. Cache result & display → Write to cache on success, present results in a table or structured format

---

### Ask When Information is Missing

When encountering unclear or missing information, **you MUST ask the user before proceeding** — never infer:

| Missing info | Alternative behavior example |
|---|---|
| No site specified | Ask: "Which Shopee site would you like to query?" |
| Vague keyword | Ask: "Could you specify the category or product keyword?" |
| Ambiguous time range (e.g., "recent" / "hot") | Ask: "Would you prefer the last 30 days or a specific month?" |

---

## Pre-Call Confirmation (Prevent Wasted Quota)

Before calling any paid endpoint (keyword, product, review), **you MUST confirm key parameters with the user** to avoid wasting quota due to incorrect parameters.

Confirmation example:

> About to call the Keyword Research API (charged):
> - Site: Singapore (sg)
> - Keyword: phone case
> - Search volume range: 1,000 ~ 50,000
> - Sort by: Search volume (descending)
>
> Proceed?

Only call the API after the user confirms.

---

## Failure / Empty Result Handling (NO Auto-Retry)

When a paid endpoint returns a failure or empty result, the following actions are **strictly forbidden**:

- ❌ Automatically changing keywords and retrying
- ❌ Automatically paginating to fetch more data
- ❌ Automatically modifying site, price range, time range, or any parameter and retrying
- ❌ Automatically changing sort order and retrying

Correct approach:

- Empty result → Inform the user that no data was found under the current conditions, and suggest they adjust the criteria and let you know
- Failure (code ≠ 0000) → Handle per the error code table; only auto-retry on token expiration (9990)
- User requests next page or more data → **First inform them of the additional quota cost**, then proceed only after confirmation

For example, when the user says "show next page":

> Fetching the next page will consume 1 quota (X remaining). Continue?

---

## Local Cache (24h)

To reduce redundant quota consumption, all successful paid endpoint responses are cached locally.

**Cache location**: `~/.shopdora/cache/`

**Cache file naming**: `{endpoint}_{site}_{paramMD5}.json`
- Examples: `keyword_sg_a1b2c3d4.json`, `product_th_e5f6g7h8.json`

**Cache logic**:

1. Before calling the API, compute the MD5 of the request parameters (serialize site + all query params as a JSON string, then hash)
2. Check if a corresponding file exists under `~/.shopdora/cache/`
3. If exists and modified within 24 hours → Read from cache, inform user "(from cache, X hours ago)", skip API call
4. If not found or expired → Call API, write/update cache file on success
5. Balance queries (free, not rate-limited) and token acquisition (free) are NOT cached

---

### Workflow 1: Get Access Token

A valid access token is required before any paid API calls.

**Token persistence mechanism**:

The token is stored in `~/.shopdora/token.json`:

```json
{
  "accessToken": "a1b2c3d4e5f6...",
  "tokenType": "Bearer",
  "expiresIn": 2678400,
  "obtainedAt": 1753718400
}
```

**Token acquisition and validation flow**:

1. First, attempt to read `~/.shopdora/token.json`
2. If the file exists, check if `obtainedAt + expiresIn > current timestamp`; use directly if valid
3. If the file doesn't exist or has expired, read credentials from `~/.shopdora/config.json` and call the token endpoint
4. Write the new token and acquisition time to `~/.shopdora/token.json`
5. All subsequent API requests read accessToken from `token.json`

**API call:**

```bash
curl -s -X POST 'https://openapi.shopdora.cn/openapi/standard/token' \
  -H 'Content-Type: application/json' \
  -d '{"clientId":"<read from config>","clientSecret":"<read from config>"}'
```

**Token renewal rules:**

- Token is valid for ~31 days; re-acquire before expiration
- When any API returns `9990`, automatically delete `token.json`, re-acquire the token, and retry the original request
- Check the `tokenExpiresIn` field from `/standard/queryBalance` for the precise expiration time

---

### Workflow 2: Query Balance

Proactively query when the user asks for balance, before bulk calls, or at the start of a session.

**API call:**

```bash
curl -s -X POST 'https://openapi.shopdora.cn/openapi/standard/queryBalance' \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer <access_token>'
```

**Result display format** (must clearly present the following):

```
📊 Account Info
- Client Name: {clientName}
- Account Status: {accountStatus}
- Token Expires: {tokenExpiresIn}

💰 Quota Usage
- Period: {periodStart} ~ {periodEnd}
- Used / Limit: {quotaUsed} / {quotaLimit} ({quotaRemaining} remaining)

⚡ Rate Limit
- Per-minute limit: {rateLimitPerMinute} calls/min
- Used this minute: {rateLimitUsedThisMinute} calls
```

---

### Workflow 3: Keyword Research

Use when the user wants to find trending search terms for a category or product.

**Pre-call check**: Check 24h cache first, then confirm parameters (site, keyword, filters) with the user. Only call API after confirmation. Do NOT auto-retry on failure or empty results.

**Required params**: `site`
**Common optional params**: `keyword`, `cateIds`, `searchVolume`, `sortBy`

**API call:**

First determine the site code using the site name mapping, confirm the user's filter criteria, then call:

```bash
curl -s -X POST 'https://openapi.shopdora.cn/openapi/standard/keyword/search' \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer <access_token>' \
  -d '{
    "site": "<site>",
    "keyword": "<keyword>",
    "searchVolume": {"min": <min>, "max": <max>},
    "sortBy": "<sortBy>",
    "orderBy": 1,
    "pageNum": 1,
    "pageSize": 20
  }'
```

**Result display**: Present keywords in a table with key metrics: searchVolume, searchVolumeIncRate, productNum, avgPrice, avgRating. If there are many results, inform the user that more pages are available (each additional page costs 1 quota).

---

### Workflow 4: Product Discovery

Use when the user wants to discover and analyze trending products or competitors on Shopee.

**Pre-call check**: Check 24h cache first, then confirm parameters (site, keyword/category, price range, time range) with the user. Only call API after confirmation. Do NOT auto-retry on failure or empty results.

**Required params**: `site`, `month`
**Common optional params**: `keyword`, `cateIds`, `price`, `salesM`, `shelfTimeRange`, `sortBy`

**month parameter:**
- `30` → Last 30 days view (most common)
- `202603` → Specific month view

**price parameter:**
- Value = actual price × 100000, e.g. $9.90 → `990000`

**API call:**

```bash
curl -s -X POST 'https://openapi.shopdora.cn/openapi/standard/product/search' \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer <access_token>' \
  -d '{
    "site": "<site>",
    "month": 30,
    "keyword": "<keyword>",
    "sortBy": "salesM",
    "orderBy": 1,
    "pageNum": 1,
    "pageSize": 20
  }'
```

**Result display:**
- Present products in a table with: name, price (divide by 100000 for local currency), salesM, salesGrowthRateM, cateRank, shopType, etc.
- price fields must be **divided by 100000** to display as local currency
- salesGrowthRateM must be **divided by 100** to display as percentage
- ratingScore must be **divided by 10** to display as stars
- shopType conversion: 0 → Regular Shop, 1 → Preferred Shop, 2 → MALL

---

### Workflow 5: Review Scraping & Analysis

Use when the user wants to view buyer reviews for a product or analyze customer feedback.

**Pre-call check**: Check 24h cache first, then confirm parameters (site, shopId, itemId) with the user. Only call API after confirmation. Do NOT auto-retry on failure or empty results.

**Required params**: `site`, `shopId`, `itemId`, `limit`, `offset`

**API call:**

```bash
curl -s -X POST 'https://openapi.shopdora.cn/openapi/standard/comment/get' \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer <access_token>' \
  -d '{
    "site": "<site>",
    "shopId": <shopId>,
    "itemId": <itemId>,
    "limit": 20,
    "offset": 0
  }'
```

**Pagination logic:**
- Max 20 per page, offset starts at 0, max 3000
- Read response `data.data.has_more`; if `true`, offset += limit to fetch next page
- When user requests "more", first inform them of the additional quota cost before fetching

**Result display:**
- First show review summary: total reviews, overall star rating, star distribution
- List each review: star rating, username, content (truncated to 150 chars), likes, whether it has images
- ctime is Unix seconds — convert to readable time
- If the review has `template_tags`, display tag info

---

### Workflow 6: Category Browsing

Use when the user needs to browse a site's product category tree.

**API call:**

```bash
curl -s -X POST 'https://openapi.shopdora.cn/openapi/standard/cate/list' \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer <access_token>' \
  -d '{"site":"<site>","cateId":0}'
```

Note: Response `data` is a JSON string — you must `JSON.parse` before displaying.

**Result display**: Present the category tree with indentation, marking leaf nodes.

---

## Site Code Quick Reference

| Code | Site | Code | Site |
|------|------|------|------|
| sg | Singapore | vn | Vietnam |
| tw | Taiwan, China | id | Indonesia |
| my | Malaysia | br | Brazil |
| ph | Philippines | mx | Mexico |
| th | Thailand | | |

---

## Error Handling

| code | Description | Action |
|------|------|------|
| 0000 | Success | Display results normally |
| 0001 | Invalid parameter | Check and correct request parameters, then retry |
| 9990 | Token invalid | Delete token.json, re-acquire token, retry original request |
| 9992 | IP not whitelisted | Inform user that current IP is not whitelisted; contact platform |
| 9993 | Rate limited | Wait a few seconds and retry automatically, up to 3 times |
| 9997 | Quota exhausted | Inform user that quota is used up; suggest waiting for next period or contacting support for expansion |
| 9999 | System busy | Wait 3 seconds and retry, up to 2 times |

---

## Important Reminders

1. **Paid service**: Keyword research, product discovery, and review scraping each consume 1 quota per successful call (returning non-empty data). Balance queries and category browsing are free.
2. **Pre-call confirmation**: Before any paid API call, you MUST confirm key parameters (site, keyword, time range, etc.) with the user — never auto-infer.
3. **No auto-retry**: On failure or empty results, DO NOT automatically change keywords, paginate, or modify parameters to retry. Only auto-retry on token expiration (9990).
4. **Notify on pagination / additional retrieval**: When the user requests next page or more data, first inform them of the additional quota cost before proceeding.
5. **24h local cache**: All successful paid endpoint responses are cached in `~/.shopdora/cache/`. Identical requests within 24 hours are served from cache without consuming quota.
6. **Quota awareness**: After each paid API call, inform the user of the consumption and remaining quota.
7. **Price fields**: All `price` fields from product/search must be divided by 100000 to show as local currency.
8. **Data freshness**: Keyword data is not real-time; it depends on the platform's refresh cycle.
9. **Pagination limit**: Review offset is capped at 3000.

---

## Reference

For detailed API field definitions, parameter boundaries, and complete response JSON structures, load `references/api_docs.md` using the Read tool.
