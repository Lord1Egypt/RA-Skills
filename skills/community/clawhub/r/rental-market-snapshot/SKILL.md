---
name: rental-market-snapshot
description: Build a snapshot of a local rental market from Facebook Marketplace rental listings - typical rent by bedroom count, price spread, what's new this week, and listings that look too good to be true - via SocialAPIs. Use when the user is apartment or room hunting, comparing neighborhoods or cities, pricing a property they rent out, or researching rents for a relocation or investment.
---

# Rental market snapshot

What does a 2-bedroom cost in this city right now, and which listings are worth a call?

Needs `SOCIALAPIS_API_KEY`. Auth, parameters and errors are in the `socialapis` skill ([endpoint reference](https://github.com/SocialAPIsHub/skills/blob/main/skills/socialapis/references/endpoints.md)); with the MCP server connected, use `facebook_marketplace` (rentals action).

## Ask first (only what's missing)

- City (or several to compare) and radius (default 15 km for one city).
- Bedrooms (or "all, broken down"), max budget, bathrooms if it matters.
- Goal: **renting** (find places), **landlord** (set a rent), or **research** (compare areas).

## Budget

1 credit per call. One city broken down by 1 / 2 / 3 bedrooms: about 1 + 3 × 3 = 10 credits. Each extra city about 10 more. Say the total before comparing several cities.

## Steps

1. `/facebook/marketplace/city-coordinates?city=<city>&exactly_one=true` per city.
2. For each bedroom count: `/facebook/marketplace/rentals` with the coordinates, `filter_radius_km`, `filter_bedrooms_min` = `filter_bedrooms_max` = N, optional price bounds, `sort_by=CREATION_TIME_DESCEND`. 2 to 4 pages each (`end_cursor`).
3. **Clean:** parse prices to numbers, convert weekly prices to monthly (×4.33) when the listing says weekly, drop rooms-in-shared-house from apartment stats (and the reverse) unless the user wants both, drop duplicates and placeholder prices.
4. **Compute per bedroom count:** count, median, p25 to p75, and new in the last 7 days when a date is available.
5. For the user's shortlist (renting) or the closest comparables (landlord), open 3 to 5 with `/facebook/marketplace/listing?listing_id=…` for description, photos and exact area.

## Too good to be true

Rent 35%+ under the median for the bedroom count, landlord "abroad", keys by mail, deposit before viewing, copied photos, or a request to continue on WhatsApp or email right away. These are the classic rental scams on Marketplace; call them out.

## Output

```
## Rentals in <city>, <date> (<radius> km)

| Bedrooms | Listings | Median /month | Typical range | New this week |
|---|---|---|---|---|

### Shortlist (renting)   /   Suggested rent (landlord)
| Listing | Rent | Beds/Baths | Area | Why | Link |

### Avoid
<listing + reason>
```

For several cities, add a comparison table (median per bedroom count, one row per city) and a one-line takeaway.

## Limits

- Marketplace is one channel; agencies and other sites aren't included. Say "Marketplace listings", not "the market".
- Asking rents, not signed leases.
- Read-only: never contact landlords.
