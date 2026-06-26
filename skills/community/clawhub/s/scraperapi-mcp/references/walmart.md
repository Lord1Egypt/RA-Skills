# Walmart SDE Tools — Detailed Guide

Four MCP tools for structured Walmart data extraction. All return JSON.

## Common Parameters (shared by all Walmart tools)

| Parameter | Type | Description |
|-----------|------|-------------|
| `tld` | string | Walmart TLD: `"com"`, `"ca"`, `"com.mx"` |
| `countryCode` | string | Two-letter country code for geo-specific results |

## Tool: `walmart_search`

Product search results with titles, prices, and product IDs.

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `query` | string | Yes | Product search query |
| `page` | number | No | Page number for pagination |

### Best Practices
- Extract product IDs from results to feed into `walmart_product` or `walmart_reviews`.
- Set `tld` to match the target market — `"com"` for US, `"ca"` for Canada, `"com.mx"` for Mexico.

---

## Tool: `walmart_product`

Product details by product ID — pricing, description, images, ratings.

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `productId` | string | Yes | Walmart product ID |

### Best Practices
- Get product IDs from `walmart_search` results or from Walmart URLs.

---

## Tool: `walmart_category`

Category browse results by category ID — explore products within a department.

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `category` | string | Yes | Walmart category ID |
| `page` | number | No | Page number for pagination |

### Best Practices
- Category IDs can be found in Walmart URLs (e.g., `"4044"` for Electronics).
- Useful for browsing products when you don't have a specific search query.

---

## Tool: `walmart_reviews`

Product reviews by product ID with filtering and sorting.

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `productId` | string | Yes | Walmart product ID |
| `page` | number | No | Page number for pagination |
| `sort` | string | No | Sort order: `"helpful"`, `"recent"` |
| `ratings` | string | No | Comma-separated rating filters (e.g. `"4,5"` for 4+ stars) |
| `verifiedPurchase` | string | No | Filter by verified purchases |

### Best Practices
- Use `sort: "helpful"` for the most useful reviews, `sort: "recent"` for latest.
- Filter with `ratings: "1,2"` to surface negative reviews (useful for risk analysis).

---

## Typical Workflow

1. **Search**: `walmart_search` with `query` to find products
2. **Details**: `walmart_product` with the product ID for full info
3. **Reviews**: `walmart_reviews` with the product ID to analyze customer feedback
4. **Browse**: `walmart_category` to explore products within a department
