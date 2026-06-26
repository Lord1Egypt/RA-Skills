---
name: slickdeals
description: Search Slickdeals.net for deals, coupons, and promo codes. Use when the user asks for deals, discounts, price comparisons, or to find cheap games, electronics, or other products.
license: Apache-2.0
---

# Slickdeals Skill

Search Slickdeals.net for the best deals, coupons, promo codes, and discounts across electronics, games, home goods, and more.

## Capabilities

- Search for deals by product name, category, or keyword
- Get frontpage deals (top trending deals)
- Filter by store, category, or price range
- Check deal expiration status
- Find coupon codes and promo codes

## Usage

### Search for Deals

```
Use the skill to search Slickdeals for specific products or categories.
```

**Examples:**
- "Find deals on PS5 games"
- "Search for Nintendo Switch deals"
- "Any deals on air fryers?"
- "Find GTA Trilogy deals under $30"
- "Show me frontpage deals"
- "Find laptop deals on Slickdeals"

### Search URL Format

The search URL pattern is:
```
https://slickdeals.net/newsearch.php?q={QUERY}&searcharea=deals&searchin=first
```

For category browsing:
```
https://slickdeals.net/computer-deals/
https://slickdeals.net/electronics-deals/
https://slickdeals.net/video-game-deals/
https://slickdeals.net/home-deals/
```

## Implementation

### Step 1: Search Slickdeals

Use `ollama_web_fetch` to retrieve search results:

```
https://slickdeals.net/newsearch.php?q=URL_ENCODED_QUERY&searcharea=deals&searchin=first
```

### Step 2: Verify Each Deal is Active

**CRITICAL: Before presenting any deal, you MUST verify it is currently active.**

For each search result:
1. Fetch the individual deal page using `ollama_web_fetch`
2. Check for expiration indicators:
   - "expired" or "deal has expired" text on the page
   - "currently unavailable" or "out of stock" on the retailer page
   - Deal posted date older than 30 days (likely expired)
3. Only include deals confirmed as active in your output
4. If no deals are active, say so explicitly — do NOT show expired deals

### Step 3: Parse Active Deals

Extract from confirmed-active deals:
- Deal title
- Current price vs original price
- Discount percentage
- Store name
- Deal score (thumbs up/down)
- Direct link to deal
- Any coupon codes required

### Step 4: Format Output

Present only **active** deals in a clean table format:

| Deal | Price | Discount | Store | Score | Link |
|------|-------|----------|-------|-------|------|
| Title | $XX ($YY) | 50% off | Amazon | +15 | [URL] |

If no active deals are found, respond:
> No active deals found for [query]. The most recent deals have expired. I'll keep an eye out — want me to set up a deal alert?

## Categories

- `video-game-deals` - Video games, consoles, accessories
- `computer-deals` - Laptops, desktops, components
- `electronics-deals` - TVs, phones, audio
- `home-deals` - Appliances, furniture
- `clothing-deals` - Fashion, apparel
- `travel-deals` - Hotels, flights, vacation packages

## Rules

1. **ACTIVE DEALS ONLY**: Never show expired deals. If the deal page says "expired" or the retailer shows "unavailable", exclude it entirely
2. **Verify before presenting**: Fetch each deal page to confirm it's still live
3. **Be honest about availability**: If nothing is active, say so — don't pad results with stale deals
4. **Deal score**: Higher thumbs up = better verified deal
5. **Comments**: Read comments for coupon codes or price match tips
6. **Store filter**: Results often include Amazon, Best Buy, Walmart, Newegg, etc.
7. **Post date awareness**: Deals older than ~30 days are very likely expired — prioritize recent deals

## Limitations

- Slickdeals is a community-driven site; deals may expire quickly
- Some deals require store-specific coupons or subscriptions (Amazon Prime, etc.)
- Regional availability may vary

## Example Queries

| User Request | Search Query |
|--------------|--------------|
| "Find PS5 deals" | `PS5` |
| "Cheap GTA Trilogy" | `GTA Trilogy` |
| "Nintendo Switch games under $30" | `Nintendo Switch games` |
| "Laptop deals" | `laptop` |
| "Air fryer deals" | `air fryer` |
| "Frontpage deals" | Browse `https://slickdeals.net/` |

## Notes

- **MANDATORY**: Verify every deal is active before showing it. Expired deals waste the user's time
- If most/all results are expired, try a broader search or check current retailer prices via web search
- Include the store name and any coupon codes required
- Mention if the deal requires membership (Prime, etc.)
- When Slickdeals search returns no active deals, supplement with current retail pricing from Amazon/Best Buy/etc.