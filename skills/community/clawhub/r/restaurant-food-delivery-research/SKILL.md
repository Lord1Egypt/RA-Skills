---
name: restaurant-food-delivery-research
description: Researches restaurants and grocery/food delivery via the Crawlora API — Yelp reviews, OpenTable reservations, DoorDash and Uber Eats restaurant search/menus, and Instacart grocery search — returning clean JSON. Use when the user wants restaurant reviews or menus, delivery options near a location, or grocery product/store search.
---

# Restaurant & food-delivery research

Look up restaurant reviews, reservations, and delivery menus, plus grocery
search across restaurant, delivery, and grocery platforms as normalized JSON from the Crawlora API — no
scraping delivery-app pages.

## When to use this skill

- "What are the reviews / menu for this restaurant?" (Yelp, OpenTable)
- "Can I book a table at <restaurant>?" (OpenTable availability)
- "What's available for delivery near me?" (DoorDash, Uber Eats)
- "What's on this restaurant's delivery menu / what does this dish cost?"
- "Search groceries at this Instacart store."

## Setup (one-time)

- Get a free Crawlora API key (2,000 credits/mo, no card) at [https://crawlora.net](https://crawlora.net?utm_source=github&utm_medium=referral&utm_campaign=crawlora-skills).
- Set `CRAWLORA_API_KEY` in the environment before running the helper.
- The helper reads `CRAWLORA_API_KEY` from the environment and sends requests to `https://api.crawlora.net/api/v1`. Missing/invalid key → `401`.

## How it works

Most of these platforms are **location-scoped** — every search/store call
needs a `latitude`/`longitude` (or `postal_code`), not just a keyword.

1. **Yelp** — `/yelp/search` (`term`+`location`) or geocode an address first
   with `/yelp/geocode`; `/yelp/business/{id}` for detail, `/reviews` (+
   `/reviews/search`, `/reviews/highlights`), `/menu`, `/photos`.
2. **OpenTable** — `/opentable/search` (`term`+`latitude`+`longitude`) to
   find a restaurant, then `/opentable/restaurant` (`restaurant_id`,
   optional `date_time`+`party_size` for availability context), `/menus`, `/reviews`.
3. **DoorDash** — `/doordash/search` (`query`+`latitude`+`longitude`,
   required) or `/doordash/feed`/`/doordash/explore` to browse nearby
   restaurants; `/doordash/store/{store_id}` (+ `/menu`, `/info`, `/reviews`)
   for one restaurant — **every store call also needs `latitude`+`longitude`**.
4. **Uber Eats** — `/ubereats/search` (`latitude`+`longitude`, `query`
   optional) or `/ubereats/feed`; `/ubereats/store/{store_id}` (+ `/menu`,
   `/reviews`).
5. **Instacart** — resolve a store first via `/instacart/stores`
   (`postal_code`) to get its `shop_id`/`store_slug`, then
   `/instacart/search` (`shop_id`+`store_slug`+`q`) for product-term
   suggestions, `/instacart/departments` for its category taxonomy,
   `/instacart/trending` (`postal_code`) for popular items.

Full endpoint list, methods, and params: [`reference/endpoints.md`](reference/endpoints.md).

## Calling the API

```sh
# Yelp:
scripts/crawlora.sh /yelp/search term="ramen" location="San Francisco, CA" | jq '.'

# DoorDash (lat/lon required):
scripts/crawlora.sh /doordash/search query="pizza" latitude=37.7749 longitude=-122.4194 | jq '.'

# OpenTable:
scripts/crawlora.sh /opentable/search term="Italian" latitude=37.7749 longitude=-122.4194 | jq '.'

# Instacart (resolve store first):
scripts/crawlora.sh /instacart/stores postal_code=94103 | jq '.'
```

Use `scripts/crawlora.sh` for all requests; it keeps the API key out of command-line arguments.


## Endpoint reference

See [`reference/endpoints.md`](reference/endpoints.md) for the full supported restaurant, chain-menu, delivery, and grocery catalog.

## Examples

- **Cross-app delivery compare:** `/doordash/search` and `/ubereats/search`
  for the same coordinate + cuisine, compare which restaurants/prices show up.
- **Restaurant due diligence:** `/yelp/business/{id}` (rating, review
  highlights) + `/opentable/restaurant/reviews` before booking.
- **Grocery run:** `/instacart/stores` to find the nearest store, then
  `/instacart/departments` to browse its categories.

## Notes & limits

- **Credits / pay-on-success:** billed only on `2xx`; free tier 2,000 credits/mo.
  Key at [https://crawlora.net](https://crawlora.net?utm_source=github&utm_medium=referral&utm_campaign=crawlora-skills).
- **Public data only** — public listing/menu/review pages; no ordering or
  payment actions are performed.
- **Security:** key lives in `CRAWLORA_API_KEY` only — never hardcode, query-param, or commit it.
- **Location is required, not optional**, for DoorDash, Uber Eats, and
  OpenTable search/store calls — geocode an address first (e.g. via
  `/yelp/geocode` or the `geocoding_*` endpoints in `web-utilities-research`)
  if you only have a street address.
- **Instacart is store-scoped** — you need a `shop_id`+`store_slug` (from
  `/instacart/stores`) before `search`/`item`/`departments` will work.
