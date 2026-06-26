# Redfin SDE Tools — Detailed Guide

Four MCP tools for structured Redfin real estate data extraction. All return JSON.

**Key difference from other SDE tools**: Redfin tools require a full Redfin URL as input (not a search query or product ID). Build or obtain the URL from Redfin's website first.

## Common Parameters (shared by all Redfin tools)

| Parameter | Type | Description |
|-----------|------|-------------|
| `url` | string | **Required.** Full Redfin URL for the target page |
| `tld` | string | Redfin TLD: `"com"` (US) or `"ca"` (Canada) |
| `countryCode` | string | Two-letter country code (e.g. `"us"`, `"ca"`) |

## Tool: `redfin_for_sale`

Structured data for a property listing that is for sale — price, beds, baths, sq ft, description, schools, agents, similar homes, walk score, and more.

### Additional Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `raw` | boolean | No | If true, returns raw extracted JSON instead of parsed data |

### Example URL
```
https://www.redfin.com/NY/New-York/970-Park-Ave-10028/unit-5N/home/193335918
```

### Response Highlights
- Property details: price, beds, baths, sq ft, price per sq ft, year built, property type
- Location: address, latitude, longitude, map URLs, street view URL
- Agents: name, broker, phone number
- Schools: name, rating, distance, grade ranges
- Similar homes: price, beds, baths, sq ft
- Scores: walk score, bike score
- Nearby places and transit options
- Redfin recommended agent info

### Best Practices
- Use `raw: true` when you need the complete unprocessed Redfin data (useful for data analysis or when the parsed response is missing fields you need).
- The URL must be a specific property listing page, not a search results page.

---

## Tool: `redfin_for_rent`

Structured data for a rental property listing — price range, floor plans, amenities, fees, schools, and nearby rentals.

### Additional Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `raw` | boolean | No | If true, returns raw extracted JSON instead of parsed data |

### Response Highlights
- Property details: name, bed/bath/sqft/price ranges, description, available units
- Address: street, city, state, zip
- Floor plans: unit types, bedrooms, baths, rent range, availability
- Amenities and fees/policies
- Schools nearby
- Sale and tax event history
- Nearby rental listings

### Best Practices
- Rental listings often have ranges (min/max) for beds, baths, price, and sqft since a building may have multiple unit types.
- The URL must be a specific rental property page.

---

## Tool: `redfin_search`

Structured search results showing property listings in an area — addresses, prices, beds, baths, sq ft, and listing URLs.

### Response Highlights
- Array of listings, each with: address, beds, baths, sq ft, price, phone, URL
- Prices include currency and charge rate (one-time for sales, per-month for rentals)

### Best Practices
- The URL must be a Redfin search results page (e.g., `https://www.redfin.com/city/30749/NY/New-York/filter/...`).
- Use Redfin's URL filters to narrow results before scraping — filter by price, beds, property type, etc. directly in the URL.
- Extract individual property URLs from results to feed into `redfin_for_sale` or `redfin_for_rent` for full details.

---

## Tool: `redfin_agent`

Structured data for a Redfin real estate agent profile — bio, stats, listings, ratings, and service areas.

### Response Highlights
- Agent details: name, license number, brokerage, contact, languages, bio
- Performance stats: sales volume, deal counts (with numeric values for comparison)
- Current listings: photos, prices, beds, baths, sqft, addresses
- Team listings (if applicable)
- Neighborhoods and service areas
- Rating and review count

### Best Practices
- The URL must be a Redfin agent profile page.
- Use agent stats (sales volume, deal count) for comparing agents objectively.

---

## Typical Workflows

### Property Research
1. **Search**: `redfin_search` with a Redfin search URL to find properties in an area
2. **Details**: `redfin_for_sale` or `redfin_for_rent` with individual property URLs for full info
3. **Agent**: `redfin_agent` with the listing agent's URL to evaluate the agent

### Market Analysis
1. **Search**: `redfin_search` with filtered URLs (by price range, property type, etc.)
2. **Compare**: `redfin_for_sale` on multiple properties to compare details, schools, walk scores
3. **Pricing**: Analyze price per sq ft across listings for market benchmarking

## Supported Markets

Redfin operates in the US (`tld: "com"`) and Canada (`tld: "ca"`). Other TLDs default to US.
