# eBay SDE Tools — Detailed Guide

Two MCP tools for structured eBay data extraction. All return JSON.

## Common Parameters (shared by all eBay tools)

| Parameter | Type | Description |
|-----------|------|-------------|
| `tld` | string | eBay TLD: `"com"`, `"co.uk"`, `"com.au"`, `"de"`, `"ca"`, `"fr"`, `"it"`, `"es"` |
| `countryCode` | string | Two-letter country code for geo-specific results (e.g. `"us"`, `"uk"`, `"de"`) |

## Tool: `ebay_search`

Product search results with titles, prices, conditions, and item IDs.

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `query` | string | Yes | Search keywords |
| `page` | number | No | Page number for pagination |
| `itemsPerPage` | number | No | Number of items per page |
| `sellerId` | string | No | Filter results by seller ID |
| `condition` | string | No | Comma-separated: `"new"`, `"used"`, `"open_box"`, `"refurbished"`, `"for_parts"`, `"not_working"` |
| `buyingFormat` | string | No | `"buy_it_now"`, `"auction"`, `"accepts_offers"` |
| `showOnly` | string | No | Comma-separated: `"returns_accepted"`, `"authorized_seller"`, `"completed_items"`, `"sold_items"`, `"sale_items"`, `"listed_as_lots"`, `"search_in_description"`, `"benefits_charity"`, `"authenticity_guarantee"` |
| `sortBy` | string | No | `"best_match"`, `"ending_soonest"`, `"newly_listed"`, `"price_lowest"`, `"price_highest"`, `"distance_nearest"` |

### Best Practices
- Use `condition` to filter by item state — combine values like `"new,refurbished"`.
- Use `buyingFormat: "buy_it_now"` to skip auctions and get fixed-price listings.
- Use `showOnly: "sold_items"` to research recent sale prices (market value research).
- `sortBy: "price_lowest"` helps find the best deals quickly.

---

## Tool: `ebay_product`

Product details by eBay item ID.

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `productId` | string | Yes | eBay item ID |

### Best Practices
- Get item IDs from `ebay_search` results or from eBay URLs.
- Set `tld` to match the marketplace the item is listed on.

---

## Typical Workflow

1. **Search**: `ebay_search` with `query` and filters to find items
2. **Details**: `ebay_product` with the item ID for full listing info
3. **Market research**: `ebay_search` with `showOnly: "sold_items"` to analyze recent sale prices
