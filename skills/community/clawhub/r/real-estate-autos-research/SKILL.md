---
name: real-estate-autos-research
description: Researches homes and used cars via the Crawlora API — Zillow and Redfin property search/estimates/market trends, plus CarMax, Autotrader, and Cars.com vehicle search and dealer/listing detail — returning clean JSON. Use when the user wants to search homes or cars, get a property estimate or a region's market trend, or look up a specific listing/vehicle/dealer.
---

# Real estate & auto research

Search homes and used cars, and pull property/vehicle detail, across five
platforms as normalized JSON from the Crawlora API — no scraping listing pages.

## When to use this skill

- "Find homes for sale in <area>" / "what's this property worth?" (Zillow, Redfin)
- "What are home prices doing in this region?" (Redfin market trends)
- "Find similar properties" for comparison.
- "Find <make/model> for sale near <zip>" (CarMax, Autotrader, Cars.com)
- "Look up this vehicle listing / dealer."

## Setup (one-time)

- Get a free Crawlora API key (2,000 credits/mo, no card) at [https://crawlora.net](https://crawlora.net?utm_source=github&utm_medium=referral&utm_campaign=crawlora-skills).
- Set `CRAWLORA_API_KEY` in the environment before running the helper.
- The helper reads `CRAWLORA_API_KEY` from the environment and sends requests to `https://api.crawlora.net/api/v1`. Missing/invalid key → `401`.

## How it works

1. **Zillow** — `/zillow/search` needs more than a `location` string: **resolve
   `/zillow/autocomplete` (`query`) first** to get a `region_id` (and map
   bounds `north`/`south`/`east`/`west` when available), then pass
   `location`+`region_id` (+ `region_type` if returned) to `/zillow/search`;
   `/zillow/property/{zpid}` for detail.
2. **Redfin** — `/redfin/search` (`location` or `region_id`+`region_type`,
   plus filters like `min_beds`/`max_price`) for listings;
   `/redfin/property` (by `property_id` or `url`) for detail;
   `/redfin/estimate` (`property_id`) for a Redfin Estimate;
   `/redfin/similar` for comparable properties; `/redfin/region-trends`
   (`region_id`+`region_type`) for a market's historical trend.
3. **CarMax** — `/carmax/search` (filters: `make`, `model`, `zip`,
   `min_price`/`max_price`, `min_year`/`max_year`); `/carmax/vehicle/{stock_number}`
   for detail (+ `/recommendations`); `/carmax/stores`/`/carmax/store/{id}`
   for dealer locations.
4. **Autotrader** — `/autotrader/search` (filters: `make`, `model`, `zip`,
   `radius`, price/year/mileage bounds, `condition`); `/autotrader/vehicle/{id}`
   for detail; `/autotrader/dealer/{id}` for the seller.
5. **Cars.com** — `/carsdotcom/search` (`zip`, `radius`, `stock_type`);
   `/carsdotcom/vehicle/{listing_id}` for detail.

Full endpoint list, methods, and params: [`reference/endpoints.md`](reference/endpoints.md).

## Calling the API

```sh
# Homes (resolve region_id first, Zillow search needs more than a location string):
scripts/crawlora.sh /zillow/autocomplete query="Austin, TX" | jq '.data'
scripts/crawlora.sh /zillow/search location="Austin, TX" region_id=10221 | jq '.'
scripts/crawlora.sh /redfin/region-trends region_id=30818 region_type=city | jq '.'

# Cars:
scripts/crawlora.sh /carmax/search make=Toyota model=RAV4 zip=94103 | jq '.'
scripts/crawlora.sh /autotrader/search make=Honda model=Civic zip=94103 radius=50 | jq '.'
```

Use `scripts/crawlora.sh` for all requests; it keeps the API key out of command-line arguments.


## Endpoint reference

See [`reference/endpoints.md`](reference/endpoints.md) for every Zillow,
Redfin, CarMax, Autotrader, and Cars.com endpoint this skill uses.

## Examples

- **Home-buying research:** `/zillow/search` + `/redfin/search` for the
  same area, cross-check price/sqft, then `/redfin/region-trends` for
  whether the market is heating up or cooling.
- **Property valuation sanity-check:** `/redfin/estimate` alongside
  `/redfin/similar` (comps) for one address.
- **Car-shopping compare:** `/carmax/search`, `/autotrader/search`, and
  `/carsdotcom/search` for the same make/model/zip, diff price and mileage
  across all three.

## Notes & limits

- **Credits / pay-on-success:** billed only on `2xx`; free tier 2,000 credits/mo.
  Key at [https://crawlora.net](https://crawlora.net?utm_source=github&utm_medium=referral&utm_campaign=crawlora-skills).
- **Public data only** — public listing/estimate pages; not a real-estate or
  financial advisor.
- **Security:** key lives in `CRAWLORA_API_KEY` only — never hardcode, query-param, or commit it.
- **Redfin's region ids are platform-specific** — resolve via `/redfin/search`
  results (which include `region_id`) before calling `/redfin/region-trends` cold.
- **Zillow search requires a `region_id` (from `/zillow/autocomplete`), not just
  a `location` string** — a bare `location` will `400`.
- Search endpoints are paginated (`page`) — walk pages for full coverage.
