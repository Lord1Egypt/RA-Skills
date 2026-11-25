---
name: used-car-scout
description: Scout used cars, trucks and motorcycles on Facebook Marketplace near a city - shortlist by budget, year and mileage, compare each car to similar listings, and flag likely scams - using SocialAPIs. Use when the user is shopping for a vehicle, wants to know if a car listing is priced fairly, or is researching a local used-car market (dealers vs private sellers).
---

# Used car scout

Turn "I want a 2018+ Corolla under $14k near Austin" into a ranked shortlist with a fair-price check on every car.

Needs `SOCIALAPIS_API_KEY`. Auth, parameters and errors are in the `socialapis` skill ([endpoint reference](https://github.com/SocialAPIsHub/skills/blob/main/skills/socialapis/references/endpoints.md)); with the MCP server connected, use `facebook_marketplace` (vehicles action).

## Ask first (only what's missing)

- Make and model (or a type: "small SUV", "pickup"), year range, max mileage.
- Budget (max, and a min if they want to avoid junk), city, radius (default 80 km for cars).
- Private sellers only? (`is_c2c_listing_only=true`)

## Budget

1 credit per call. Typical run: 1 (coordinates) + 3 to 6 (vehicle search pages) + 1 per shortlisted car for details + 1 per seller check. About 10 to 20 credits for a shortlist of 5. Tell the user before checking more than 10 cars in depth.

## Steps

1. `/facebook/marketplace/city-coordinates?city=<city>&exactly_one=true`.
2. `/facebook/marketplace/vehicles` with the coordinates, `filter_radius_km`, `filter_price_lower_bound` / `upper_bound`, `sort_by=CREATION_TIME_DESCEND`, and `is_c2c_listing_only` if asked. Page with `end_cursor` until about 60 to 100 listings.
3. **Filter locally** on title, year and mileage (the search has no make/model/year filters): keep the requested model and year range, drop mileage above the limit, drop "salvage", "rebuilt", "parts", "lease takeover", "down payment" listings unless the user wants them.
4. **Price each car against its peers.** Group the full collected sample by model + year (±1 year). For each kept car compute "vs group median" and "price per 10k km/miles" vs the group. Need at least 4 peers for a comparison; otherwise say "not enough comparables".
5. **Shortlist** the 5 to 8 best value cars (lowest price for the year and mileage, sensible mileage for the age: roughly 12k to 15k miles / 20k to 25k km per year is normal).
6. For each shortlisted car: `/facebook/marketplace/listing?listing_id=…` (description, photos, location) and `/facebook/marketplace/seller?seller_id=…` (join date, rating).
7. Read the description for: title status (clean / salvage), owners, service history, accident mentions, "needs work".

## Scam and risk flags

- Price 30%+ under the peer median.
- Seller account created recently, no ratings, and far away "but can ship".
- Asks for a deposit before viewing, payment off-platform, or the car is "with a shipping company".
- Mileage missing or "0", VIN refused, title "in hand soon".
- Dealer posing as a private seller (many car listings from one seller id).

Flag; don't accuse.

## Output

```
## <model> <years>, under <budget>, within <radius> of <city> (<date>)
Scanned <n> listings, <k> matched your filters.

| # | Car | Price | Mileage | vs similar | Seller | Flags | Link |
|---|---|---|---|---|---|---|---|

### Best pick
<one paragraph: why, what to ask the seller>

### Questions to ask before viewing
- title status, service records, accidents, why selling, can I bring a mechanic
```

Add a short market note: median price by year for the model, and how many listings are dealers vs private.

## Limits

- Asking prices only; final prices are usually lower.
- Mileage and year come from what sellers type. Odd values exist; drop or flag them.
- Never message sellers or arrange viewings; only read listings.
