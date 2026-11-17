# short-term-rental-market-research — endpoint reference

> Generated from `scripts/tools.json` by `scripts/generate.mjs` — do not edit by hand.

Only the endpoints used by this workflow. Call them via `scripts/crawlora.sh` (see SKILL.md).

All paths are relative to the API base `https://api.crawlora.net/api/v1` and require the header `x-api-key: $CRAWLORA_API_KEY`. Path params like `{id}` are substituted into the URL; `GET` params go in the query string; `POST` params go in a JSON body.

**8 endpoints across 2 platform group(s).**

## Datasets (4)

### `datasets_airbnb_facets`

- **HTTP:** `GET /datasets/airbnb-markets/facets`
- **What:** Facet the Airbnb markets dataset. Returns suppressed distribution counts over the Airbnb markets dataset, honoring the same filters as search. Facet enum: `country`, `market`, `currency`, `superhost`, `guest_favorite`, `rating_band`, `review_band`, `admin1` (top subdivision), `locality` (settlement), `room_type` (`entire_place`/`private_room`/`hotel`/`shared_room`), `property_type` (Airbnb's canonical listing type from the detail page), `amenities` (each amenity with the count of listings offering it). Enrichment-derived facets include a `coverage` object with the number and share of filtered listings carrying that dimension; buckets stay empty below the 20% minimum visibility gate. Coverage above the gate may still be partial. group_by enum: `country`, `market`, `admin1`, `locality`, `room_type`, `property_type`.
- **Params:** `active_since` (string, optional) — Freshness filter, an ISO-8601 date (YYYY-MM-DD); `country` (string, optional) — Exact ISO-3166-1 alpha-2 country filter, e.g. FR; `facet` (string, **required**) — Facet enum: country, market, currency, superhost, guest_favorite, rating_band, review_band, admin1, locality, room_type, property_type, amenities; `group_by` (string, optional) — Aggregate cell dimension enum: country, market, admin1, locality, room_type, property_type. Defaults to country; `guest_favorite` (boolean, optional) — Count only Guest Favorite listings (an observed lower bound; the badge under-counts); `market` (string, optional) — Exact metro-market filter, max 128 characters; `min_listings` (integer, optional) — Minimum listings per bucket; raises the small-cell suppression floor; `min_rating` (number, optional) — Minimum listing rating, from 0 through 5; `min_review_count` (integer, optional) — Minimum listing review count, 0 or greater; `superhost` (boolean, optional) — Count only Superhost listings

### `datasets_airbnb_item`

- **HTTP:** `GET /datasets/airbnb-markets/items/{country}`
- **What:** Get an Airbnb market from the dataset. Returns one country's full aggregate Airbnb market profile from dataset id enum value `airbnb-markets` — headline supply, Superhost share, Guest Favorite share (`guest_favorite_pct`, an observed lower bound), `avg_person_capacity` (average guests a listing sleeps over the detail-page-enriched sample), ratings, its top metros, bounding box, per-currency nightly-price percentiles, and a USD-normalized `price_usd` percentile block (converted via an approximate dated FX snapshot) for cross-country comparison. Aggregate-only. Returns 404 for a country below the suppression floor.
- **Params:** `country` (string, **required**) — ISO-3166-1 alpha-2 country code, e.g. FR

### `datasets_airbnb_nearby`

- **HTTP:** `GET /datasets/airbnb-markets/nearby`
- **What:** Airbnb market density near a coordinate. Returns an aggregate geohash-grid density map of Airbnb listings within a radius of a coordinate, from dataset id enum value `airbnb-markets`. Each cell reports a centroid, listing count and Superhost share; thin cells are suppressed. Aggregate-only.
- **Params:** `active_since` (string, optional) — Freshness filter, an ISO-8601 date (YYYY-MM-DD); `country` (string, optional) — Exact ISO-3166-1 alpha-2 country filter, e.g. US; `lat` (number, **required**) — Center latitude, from -90 through 90; `lon` (number, **required**) — Center longitude, from -180 through 180; `min_listings` (integer, optional) — Minimum listings per cell; raises the small-cell suppression floor; `min_rating` (number, optional) — Minimum listing rating, from 0 through 5; `precision` (integer, optional) — Geohash precision, from 1 through 12; defaults to a value derived from the radius; `radius_m` (integer, **required**) — Search radius in meters, from 1 through 50000; `superhost` (boolean, optional) — Count only Superhost listings

### `datasets_airbnb_search`

- **HTTP:** `GET /datasets/airbnb-markets/search`
- **What:** Search the Airbnb markets dataset. Returns aggregate Airbnb short-term-rental market rollups from the dataset id enum value `airbnb-markets`. Aggregate-only: each row is a market cell, never an individual listing. Thin cells are suppressed. group_by enum: `country`, `market`, `admin1` (top subdivision), `locality` (settlement), `room_type` (`entire_place`/`private_room`/`hotel`/`shared_room`), `property_type` (Airbnb's canonical listing type from the detail page). Enrichment-derived groupings include a `coverage` object with the number and share of filtered listings carrying that dimension; the 20% minimum gate is not a completeness guarantee, and counts still describe classified rows only. Each cell also carries `median_price_usd`, the median nightly price converted to USD via an approximate dated FX snapshot, for cross-country comparison (combine with `group_by=room_type` for median price by room type); `guest_favorite_pct`, the share of listings carrying the Guest Favorite badge (an observed lower bound, like `superhost_pct`); and `avg_person_capacity`, the average guests a listing sleeps over the detail-page-enriched sample. Sort enum: `listings_desc`, `superhost_pct_desc`, `rating_desc`, `key_asc`. Billing: this search costs 1 credit per record returned, with a minimum of 2 (an empty result costs 2, a full page of 100 costs 100).
- **Params:** `active_since` (string, optional) — Freshness filter, an ISO-8601 date (YYYY-MM-DD); only listings last seen on or after it are counted; `country` (string, optional) — Exact ISO-3166-1 alpha-2 country filter, e.g. FR; `group_by` (string, optional) — Aggregate cell dimension enum: country, market, admin1, locality, room_type, property_type. Defaults to country; `guest_favorite` (boolean, optional) — Count only Guest Favorite listings (an observed lower bound; the badge under-counts); `market` (string, optional) — Exact metro-market filter, e.g. Paris, max 128 characters; `min_listings` (integer, optional) — Minimum listings per cell; raises the small-cell suppression floor (never lowered below the built-in minimum); `min_rating` (number, optional) — Minimum listing rating, from 0 through 5; `min_review_count` (integer, optional) — Minimum listing review count, 0 or greater; `page` (integer, optional) — Page number, defaults to 1; `page_size` (integer, optional) — Page size, defaults to 20 and maxes at 100; page * page_size must be <= 10000; `sort` (string, optional) — Sort enum: listings_desc, superhost_pct_desc, rating_desc, key_asc; `superhost` (boolean, optional) — Count only Superhost listings

## Airbnb (4)

### `airbnb_room`

- **HTTP:** `GET /airbnb/room/{id}`
- **What:** Get Airbnb room. Returns the public details of one Airbnb listing by room id: title, description, property type, location and coordinates, guest capacity, amenities, price and price per night, rating, review count, host, and the Superhost and Guest Favorite flags. Some fields are present only when Airbnb exposes them for the listing.
- **Params:** `id` (string, **required**) — Room id

### `airbnb_room_calendar`

- **HTTP:** `GET /airbnb/room/{id}/calendar`
- **What:** Get Airbnb room calendar. Returns the public availability calendar for one Airbnb room, grouped by month. Each day carries its date, whether it is available and bookable, whether it can be a check-in or check-out day, and the minimum and maximum nights. Months are returned only when Airbnb exposes them for the listing.
- **Params:** `id` (string, **required**) — Room id

### `airbnb_room_reviews`

- **HTTP:** `GET /airbnb/room/{id}/reviews`
- **What:** Get Airbnb room reviews. Returns public guest reviews for one Airbnb room by room id, one page at a time (`page` is 1-based). Each review has the author, date, rating and text. Reviews are returned only when Airbnb exposes them for the listing.
- **Params:** `id` (string, **required**) — Room id; `page` (integer, optional) — 1-based page

### `airbnb_search`

- **HTTP:** `GET /airbnb/search`
- **What:** Search Airbnb stays. Searches public Airbnb stays for a location, with optional check-in and check-out dates, adult count, currency and page. Pass `ne_lat`, `ne_lng`, `sw_lat` and `sw_lng` to bound the search to a map area. Each result has the listing id, title, URL, location and coordinates, price and price per night, rating, review count, host, and the Superhost and Guest Favorite flags.
- **Params:** `adults` (integer, optional) — Adult guests; `check_in` (string, optional) — Check-in date; `check_out` (string, optional) — Check-out date; `currency` (string, optional) — Currency for bounded map search; `location` (string, **required**) — Location; `ne_lat` (number, optional) — Northeast latitude for bounded map search; `ne_lng` (number, optional) — Northeast longitude for bounded map search; `page` (integer, optional) — 1-based page; `sw_lat` (number, optional) — Southwest latitude for bounded map search; `sw_lng` (number, optional) — Southwest longitude for bounded map search; `zoom` (integer, optional) — Map zoom for bounded map search
