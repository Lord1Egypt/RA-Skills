# Amazon SDE Tools — Detailed Guide

Three MCP tools for structured Amazon data extraction. All return JSON.

## Common Parameters (shared by all Amazon tools)

| Parameter | Type | Description |
|-----------|------|-------------|
| `tld` | string | Amazon TLD: `"com"`, `"co.uk"`, `"ca"`, `"de"`, etc. |
| `countryCode` | string | Two-letter country code for geo-specific results |
| `language` | string | Language for results (e.g. `"en-US"`) |

## Tool: `amazon_product`

Product details by ASIN — pricing, description, images, ratings, and specifications.

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `asin` | string | Yes | Amazon Standard Identification Number |
| `includeHtml` | boolean | No | Include raw HTML in response |

### Best Practices
- Use the 10-character ASIN (e.g., `"B0BSHF7WHW"`). Find ASINs from Amazon URLs or `amazon_search` results.
- Set `tld` to match the target marketplace — prices and availability differ across `"com"`, `"co.uk"`, `"de"`, etc.

---

## Tool: `amazon_search`

Product search results with titles, prices, ratings, and ASINs.

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `query` | string | Yes | Product search query |
| `page` | number | No | Page number for pagination |
| `sortBy` | string | No | Sort parameter |
| `department` | string | No | Category or department filter |
| `ref` | string | No | Reference parameter |

### Best Practices
- Be specific in queries: `"Sony WH-1000XM5 headphones"` beats `"headphones"`.
- Use `department` to narrow results to a category.
- Extract ASINs from results to feed into `amazon_product` or `amazon_offers`.

---

## Tool: `amazon_offers`

Seller offers and pricing for a product by ASIN — useful for price comparison across sellers.

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `asin` | string | Yes | Amazon Standard Identification Number |
| `condition` | string | No | Comma-separated condition filters (e.g. `"f_new,f_usedverygood"`) |
| `fNew` | boolean | No | Include new item offers |
| `fUsedLikeNew` | boolean | No | Include used (like new) offers |
| `fUsedVeryGood` | boolean | No | Include used (very good) offers |
| `fUsedGood` | boolean | No | Include used (good) offers |
| `fUsedAcceptable` | boolean | No | Include used (acceptable) offers |

### Best Practices
- Use condition filters to narrow results — `fNew: true` for new-only, or combine multiple flags.
- The `condition` string parameter and boolean flags (`fNew`, etc.) are alternative ways to filter; use whichever is more convenient.

---

## Typical Workflow

1. **Search**: `amazon_search` with `query` to find products
2. **Details**: `amazon_product` with the ASIN for full product info
3. **Price comparison**: `amazon_offers` with the ASIN to see all seller listings and conditions
