# restaurant-menu-benchmarking — endpoint reference

> Generated from `scripts/tools.json` by `scripts/generate.mjs` — do not edit by hand.

Only the endpoints used by this workflow. Call them via `scripts/crawlora.sh` (see SKILL.md).

All paths are relative to the API base `https://api.crawlora.net/api/v1` and require the header `x-api-key: $CRAWLORA_API_KEY`. Path params like `{id}` are substituted into the URL; `GET` params go in the query string; `POST` params go in a JSON body.

**11 endpoints across 4 platform group(s).**

## DoorDash (3)

### `doordash_search`

- **HTTP:** `GET /doordash/search`
- **What:** Search DoorDash pickup restaurants. Searches the Android mobile guest catalog for pickup restaurants near a location and supports optional result filters. No DoorDash account or caller-supplied token is required.
- **Params:** `asapOnly` (boolean, optional) — Keep only stores currently available ASAP; `dashPassOnly` (boolean, optional) — Keep only DashPass-eligible stores; `latitude` (number, **required**) — Consumer latitude; `longitude` (number, **required**) — Consumer longitude; `maxDistanceMiles` (number, optional) — Maximum displayed distance in miles, from 0 to 100; `pickupOnly` (boolean, optional) — Keep only pickup-enabled stores; `query` (string, **required**) — Restaurant, cuisine, or dish query; `tag` (string, optional) — Exact cuisine or store tag, case-insensitive

### `doordash_store`

- **HTTP:** `GET /doordash/store/{store_id}`
- **What:** Get a DoorDash store. Returns public metadata for a DoorDash store by its numeric `store_id`, as seen from the delivery location given by the required `latitude` and `longitude`. The response has the name, URL, images, average rating, rating count, and menu section and item counts. Address, coordinates and price range appear only when DoorDash supplies them. Missing or out-of-range coordinates return `400`.
- **Params:** `latitude` (number, **required**) — Delivery latitude; `longitude` (number, **required**) — Delivery longitude; `store_id` (string, **required**) — Numeric DoorDash store ID

### `doordash_store_menu`

- **HTTP:** `GET /doordash/store/{store_id}/menu`
- **What:** Get a DoorDash store menu. Returns the location-aware DoorDash mobile menu, grouped into sections with item names, descriptions, and displayed prices. No DoorDash account or caller-supplied token is required.
- **Params:** `latitude` (number, **required**) — Delivery latitude; `longitude` (number, **required**) — Delivery longitude; `store_id` (string, **required**) — Numeric DoorDash store ID

## UberEats (3)

### `ubereats_search`

- **HTTP:** `GET /ubereats/search`
- **What:** Search UberEats restaurants. Returns restaurants delivering to a location: name, rating, review count, delivery estimate, cuisine tags, and image. Pass a keyword to search by name/cuisine/dish, or omit it to browse the general feed for that location.
- **Params:** `cursor` (string, optional) — Opaque pagination cursor from a previous keyword-search response; `latitude` (number, **required**) — Delivery search center latitude; `limit` (integer, optional) — Number of restaurants to return, clamped to 50. Default 20; `longitude` (number, **required**) — Delivery search center longitude; `offset` (integer, optional) — Result offset for the location feed (used only when query is omitted). Default 0; `query` (string, optional) — Keyword — restaurant name, cuisine, or dish

### `ubereats_store`

- **HTTP:** `GET /ubereats/store/{store_id}`
- **What:** Get an UberEats store. Returns an UberEats store: address, phone, rating, cuisine tags, hours tagline, and the full menu (sections with items, descriptions, and prices).
- **Params:** `store_id` (string, **required**) — UberEats store UUID, as returned by the search endpoint's storeUuid field

### `ubereats_store_menu`

- **HTTP:** `GET /ubereats/store/{store_id}/menu`
- **What:** Get an UberEats store menu. Returns the full menu for an UberEats store: section titles, items, item descriptions, prices, and availability status.
- **Params:** `store_id` (string, **required**) — UberEats store UUID, as returned by the search endpoint's storeUuid field

## Chipotle (3)

### `chipotle_menu`

- **HTTP:** `GET /chipotle/menu`
- **What:** Get Chipotle's national menu catalog. Returns Chipotle's restaurant-independent menu catalog -- every item it sells nationally, split into entrees, sides and drinks, with each item's category, type, primary filling and full customization tree. Takes no parameters. Prices are deliberately omitted from this response: Chipotle prices per restaurant, so the upstream returns every price as zero here, and surfacing a field of zeros would read as "free" rather than "unpriced". Use GET /chipotle/restaurant/menu for real prices.
- **Params:** _none_

### `chipotle_restaurant_menu`

- **HTTP:** `GET /chipotle/restaurant/menu`
- **What:** Get one Chipotle restaurant's menu with prices. Returns one restaurant's live online menu split into entrees, sides, drinks and non-food items. This is the only Chipotle endpoint that carries prices: every item has both a dine-in price and a delivery price, which genuinely differ. Each item also carries its full customization tree -- contents (the individual fillings, salsas and sides that make it up, each with their own price pair) and content_groups (how many picks each group allows). Prices are per-restaurant, so two restaurants will legitimately return different numbers for the same item.
- **Params:** `include_unavailable` (boolean, optional) — Include items the restaurant currently has unavailable (default false); `restaurant_number` (string, **required**) — Chipotle's numeric restaurant id

### `chipotle_restaurants`

- **HTTP:** `GET /chipotle/restaurants`
- **What:** Find Chipotle restaurants near a location. Returns Chipotle restaurants near a latitude/longitude, ordered by distance. Each restaurant carries its number (the id every other Chipotle endpoint takes), name, status, full postal address with coordinates, published open/close hours per day, nearest cross streets, timezone, and capability flags (Chipotlane pickup, online ordering, catering, curbside pickup, dining room open, walk-up window). A coordinate with no Chipotle nearby returns an empty list rather than an error.
- **Params:** `latitude` (number, **required**) — Search center latitude; `longitude` (number, **required**) — Search center longitude; `page` (integer, optional) — 0-based page index (default 0); `page_size` (integer, optional) — Restaurants per page, 1-50 (default 10); `radius` (integer, optional) — Search radius in meters, 1-80000 (default 8000)

## McDonalds (2)

### `mcdonalds_categories`

- **HTTP:** `GET /mcdonalds/categories`
- **What:** List McDonald's menu categories. Returns one market's McDonald's menu categories -- 13 in the United States at time of writing, including breakfast, burgers, chicken-and-fish-sandwiches, mcnuggets-and-mccrispy-strips, snack-wrap, fries-sides, happy-meal, sweets-treats, mccafe-coffees, drinks, sauces-and-condiments and the two value menus; other markets publish their own, from 6 in Switzerland to 17 in Australia. Each entry's slug is the value GET /mcdonalds/menu takes. Slugs are not portable between markets, so pass the same country back. Eight markets publish a reachable menu, fewer than the ten the restaurant locator covers.
- **Params:** `country` (string, optional) — Market (default us). One of us, ca, gb, au, ie, nz, ch, se.

### `mcdonalds_menu`

- **HTTP:** `GET /mcdonalds/menu`
- **What:** List one McDonald's menu category's items. Returns the items in one McDonald's menu category: each item's numeric id, name, product page URL and image. The item id is what GET /mcdonalds/item takes for full nutrition. Category slugs come from GET /mcdonalds/categories and must be paired with the country they came from -- both slugs and item ids are market-specific. Prices are not available; McDonald's does not publish them on this surface. A calorie label is included per item where the category page prints one, which is often blank.
- **Params:** `category` (string, **required**) — Category slug from /mcdonalds/categories; `country` (string, optional) — Market (default us). One of us, ca, gb, au, ie, nz, ch, se. Must match the market the slug came from.
