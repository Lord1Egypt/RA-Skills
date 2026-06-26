# API Endpoints

Each CLI command maps to a single SellerSprite Open API endpoint.

## Authentication

All endpoints require `secret-key` header with your API key.

## POST /v1/market/research

Market/category research — browse Amazon category rankings by revenue.

**Command:** `sellersprite market`

**Request Parameters:**

| Parameter | Type | Required | Description |
|---|---|---|---|
| marketplace | string | yes | Marketplace code (US/UK/DE/JP/CA/FR/IT/ES/MX/AU) |
| page | number | no | Page number (default: 1) |
| size | number | no | Results per page, max 100 (default: 20) |

**Response Fields (per item):**

| Field | Type | Description |
|---|---|---|
| nodeId | number | Category node ID |
| nodeLabelName | string | Category name (EN) |
| nodeLabelLocale | string | Category name (localized) |
| nodeLabelPath | string | Full category path (EN) |
| ranking | number | Revenue ranking |
| totalProducts | number | Total products in category |
| brands | number | Number of brands |
| sellers | number | Number of sellers |
| totalUnits | number | Total monthly units sold |
| totalRevenue | number | Total monthly revenue |
| avgUnits | number | Average monthly units per product |
| avgPrice | number | Average price |
| avgRatings | number | Average review count |
| avgRating | number | Average star rating |
| avgBsr | number | Average BSR |
| avgProfit | number | Average profit margin % |
| fbaProportion | number | FBA seller % |
| fbmProportion | number | FBM seller % |
| amazonSelfProportion | number | Amazon self-selling % |
| returnRatio | number | Return rate % |
| searchToPurchaseRatio | number | Search to purchase conversion |

---

## POST /v1/product/research

Product research by keyword — returns product listings with sales data.

**Command:** `sellersprite product`

**Request Parameters:**

| Parameter | Type | Required | Description |
|---|---|---|---|
| marketplace | string | yes | Marketplace code |
| keyword | string | yes | Search keyword |
| matchType | number | no | Match type (default: 2 = broad) |
| page | number | no | Page number (default: 1) |
| size | number | no | Results per page, max 100 (default: 50) |
| month | string | no | Query month (yyyyMM format) |
| order | object | no | Sort order `{ field, desc }` |

**Response Fields (per product):**

| Field | Type | Description |
|---|---|---|
| asin | string | Product ASIN |
| title | string | Product title |
| brand | string | Brand name |
| price | number | Current price |
| units | number | Estimated monthly units |
| revenue | number | Estimated monthly revenue |
| ratings | number | Total review count |
| rating | number | Star rating (0-5) |
| bsr | number | Best Seller Rank |
| fulfillment | string | Fulfillment type (FBA/FBM/AMZ) |
| sellers | number | Number of sellers |
| badge | object | `{ bestSeller, amazonChoice }` booleans |

---

## POST /v1/product/competitor-lookup

Competitor lookup — find competing products for a given ASIN.

**Command:** `sellersprite competitor`

**Request Parameters:**

| Parameter | Type | Required | Description |
|---|---|---|---|
| marketplace | string | yes | Marketplace code |
| asins | string[] | yes | Target ASIN(s) |
| page | number | no | Page number (default: 1) |
| size | number | no | Results per page, max 100 (default: 50) |
| month | string | no | Query month (yyyyMM format) |
| order | object | no | Sort order `{ field, desc }` |

**Response:** Same product fields as `/v1/product/research`.

---

## GET /v1/asin/{marketplace}/{asin}/with-coupon-trend

ASIN details with coupon trend — get product info and historical discount data.

**Command:** `sellersprite asin`

**Path Parameters:**

| Parameter | Type | Description |
|---|---|---|
| marketplace | string | Marketplace code |
| asin | string | Target ASIN |

**Response Fields:**

| Field | Type | Description |
|---|---|---|
| asin | object | Product details (title, brand, price, bsrRank, rating, features, variations, etc.) |
| couponTrends | array | Historical discount data with date, type, asinPrice, couponPrice, finalPrice |

---

## POST /v1/keyword-research

Keyword research — search volume and purchase data for keywords.

**Command:** `sellersprite keyword`

**Request Parameters:**

| Parameter | Type | Required | Description |
|---|---|---|---|
| marketplace | string | yes | Marketplace code |
| keywords | string | yes | Search keyword |
| page | number | no | Page number (default: 1) |
| size | number | no | Results per page, max 100 (default: 20) |
| month | string | no | Query month (yyyyMM format) |
| order | object | no | Sort order `{ field, desc }` |

**Response Fields (per keyword):**

| Field | Type | Description |
|---|---|---|
| keyword | string | Keyword text |
| searches | number | Monthly search volume |
| purchaseRate | number | Purchase conversion % |
| avgPrice | number | Average price for keyword |
| supplyDemandRatio | number | Supply/demand ratio |

---

## GET /v1/visits

Check API quota — remaining calls per module.

**Command:** `sellersprite quota`

**Response:** Array of quota items:

| Field | Type | Description |
|---|---|---|
| module | string | API module identifier |
| moduleMemo | string | Module description |
| remain | number | Remaining calls |

---

## Computed Stats (product command)

The CLI computes these stats from raw product data:

| Field | Description |
|---|---|
| blue_ocean_index | 0-10, higher = more opportunity. Based on competition concentration and rating barriers |
| top10_concentration | % of total units held by top 10 products |
| fba_ratio | % of products fulfilled by FBA/AMZ |
| top_brands | Top 5 brands by monthly units |
| bs_count | Number of Best Seller badges |
| ac_count | Number of Amazon's Choice badges |

---

## Rate Limits

- 40 requests per minute
- Max 100 items per request
- Max 2,000 products per query
