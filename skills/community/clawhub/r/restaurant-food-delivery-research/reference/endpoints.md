# restaurant-food-delivery-research — endpoint reference

> Generated from `scripts/tools.json` by `scripts/generate.mjs` — do not edit by hand.

Endpoints this skill uses, grouped by platform. Call them via `scripts/crawlora.sh` (see SKILL.md).

All paths are relative to the API base `https://api.crawlora.net/api/v1` and require the header `x-api-key: $CRAWLORA_API_KEY`. Path params like `{id}` are substituted into the URL; `GET` params go in the query string; `POST` params go in a JSON body.

**285 endpoints across 40 platform group(s).**

## DoorDash (12)

### `doordash_explore`

- **HTTP:** `GET /doordash/explore`
- **What:** Get DoorDash nearby stores explore feed. Returns DoorDash's location-based "nearby stores" browse feed from the Android mobile guest experience. Unlike search or autocomplete, no search query is required. No DoorDash account or caller-supplied token is required.
- **Params:** `latitude` (number, **required**) — Consumer latitude; `longitude` (number, **required**) — Consumer longitude

### `doordash_feed`

- **HTTP:** `GET /doordash/feed`
- **What:** Get DoorDash store discovery feed. Returns nearby stores for a location from the Android mobile guest experience: store ID, name, cover image and tags, plus rating, price range, delivery fee and ETA when the upstream feed surface reports them. Those metric fields are omitted rather than estimated when it does not, so treat their absence as "not reported". No DoorDash account or caller-supplied token is required.
- **Params:** `latitude` (number, **required**) — Consumer latitude; `limit` (integer, optional) — Max stores to return; `longitude` (number, **required**) — Consumer longitude; `offset` (integer, optional) — Number of stores to skip

### `doordash_search`

- **HTTP:** `GET /doordash/search`
- **What:** Search DoorDash pickup restaurants. Searches the Android mobile guest catalog for pickup restaurants near a location and supports optional result filters. No DoorDash account or caller-supplied token is required.
- **Params:** `asapOnly` (boolean, optional) — Keep only stores currently available ASAP; `dashPassOnly` (boolean, optional) — Keep only DashPass-eligible stores; `latitude` (number, **required**) — Consumer latitude; `longitude` (number, **required**) — Consumer longitude; `maxDistanceMiles` (number, optional) — Maximum displayed distance in miles, from 0 to 100; `pickupOnly` (boolean, optional) — Keep only pickup-enabled stores; `query` (string, **required**) — Restaurant, cuisine, or dish query; `tag` (string, optional) — Exact cuisine or store tag, case-insensitive

### `doordash_search_autocomplete`

- **HTTP:** `GET /doordash/search/autocomplete`
- **What:** Get DoorDash pickup search suggestions. Returns pickup restaurant matches from the Android mobile guest search experience near a location. No DoorDash account or caller-supplied token is required.
- **Params:** `latitude` (number, **required**) — Consumer latitude; `longitude` (number, **required**) — Consumer longitude; `query` (string, **required**) — Partial restaurant, cuisine, or dish query

### `doordash_search_filters`

- **HTTP:** `GET /doordash/search/filters`
- **What:** Get DoorDash search filter options. Returns the cuisines and filter values supported by the Android mobile guest search experience for a location. No DoorDash account or caller-supplied token is required.
- **Params:** `latitude` (number, **required**) — Consumer latitude; `longitude` (number, **required**) — Consumer longitude

### `doordash_search_items`

- **HTTP:** `GET /doordash/search/items`
- **What:** Search DoorDash dishes and items. Searches menu items across nearby merchants from the Android mobile guest experience. Nearby candidate stores are selected first, then their menus are read and every item whose name or description matches the query is returned with its parent store. At most five proximity-ranked stores are inspected per request, and a store whose menu cannot be read is skipped, so results are best-effort across that candidate set. An empty result array means no candidate store menu matched, not that no nearby merchant sells the item. No DoorDash account or caller-supplied token is required.
- **Params:** `asapOnly` (boolean, optional) — Keep only stores currently available ASAP; `dashPassOnly` (boolean, optional) — Keep only DashPass-eligible stores; `latitude` (number, **required**) — Consumer latitude; `longitude` (number, **required**) — Consumer longitude; `maxDistanceMiles` (number, optional) — Maximum displayed distance in miles; `pickupOnly` (boolean, optional) — Keep only pickup-enabled stores; `query` (string, **required**) — Dish or item search text; `tag` (string, optional) — Cuisine or store tag used to narrow candidate stores

### `doordash_store`

- **HTTP:** `GET /doordash/store/{store_id}`
- **What:** Get a DoorDash store. Returns public metadata for a DoorDash store by its numeric `store_id`, as seen from the delivery location given by the required `latitude` and `longitude`. The response has the name, URL, images, average rating, rating count, and menu section and item counts. Address, coordinates and price range appear only when DoorDash supplies them. Missing or out-of-range coordinates return `400`.
- **Params:** `latitude` (number, **required**) — Delivery latitude; `longitude` (number, **required**) — Delivery longitude; `store_id` (string, **required**) — Numeric DoorDash store ID

### `doordash_store_fulfillment`

- **HTTP:** `GET /doordash/store/{store_id}/fulfillment`
- **What:** Get DoorDash store fulfillment details. Returns store fulfillment methods, delivery fee info, and scheduling details from the Android mobile guest experience. No DoorDash account or caller-supplied token is required.
- **Params:** `latitude` (number, **required**) — Delivery latitude; `longitude` (number, **required**) — Delivery longitude; `store_id` (string, **required**) — Numeric DoorDash store ID

### `doordash_store_info`

- **HTTP:** `GET /doordash/store/{store_id}/info`
- **What:** Get DoorDash store contact info. Returns a lightweight store info card (map coordinates, address, phone number) from the Android mobile guest experience. This is a distinct upstream contract from the full store endpoint and reliably includes address and coordinates. No DoorDash account or caller-supplied token is required.
- **Params:** `latitude` (number, **required**) — Delivery latitude; `longitude` (number, **required**) — Delivery longitude; `store_id` (string, **required**) — Numeric DoorDash store ID

### `doordash_store_item`

- **HTTP:** `GET /doordash/store/{store_id}/item/{item_id}`
- **What:** Get DoorDash menu item details. Returns details for a specific menu item from the Android mobile guest experience. The item is matched by name, case-insensitively, against the store menu: DoorDash's anonymous menu surface exposes no stable per-item identifier, so use a name returned by the store menu or item search. A name that is not on the menu returns 404; no substitute item is returned. No DoorDash account or caller-supplied token is required.
- **Params:** `item_id` (string, **required**) — Menu item name, matched case-insensitively; `latitude` (number, **required**) — Delivery latitude; `longitude` (number, **required**) — Delivery longitude; `store_id` (string, **required**) — Numeric DoorDash store ID

### `doordash_store_menu`

- **HTTP:** `GET /doordash/store/{store_id}/menu`
- **What:** Get a DoorDash store menu. Returns the location-aware DoorDash mobile menu, grouped into sections with item names, descriptions, and displayed prices. No DoorDash account or caller-supplied token is required.
- **Params:** `latitude` (number, **required**) — Delivery latitude; `longitude` (number, **required**) — Delivery longitude; `store_id` (string, **required**) — Numeric DoorDash store ID

### `doordash_store_reviews`

- **HTTP:** `GET /doordash/store/{store_id}/reviews`
- **What:** Get DoorDash store reviews. Returns store ratings and customer reviews from the Android mobile guest experience for a location. No DoorDash account or caller-supplied token is required.
- **Params:** `latitude` (number, **required**) — Delivery latitude; `longitude` (number, **required**) — Delivery longitude; `store_id` (string, **required**) — Numeric DoorDash store ID

## Yelp (8)

### `yelp_business`

- **HTTP:** `GET /yelp/business/{id}`
- **What:** Get Yelp business detail. Looks up a single Yelp business by alias or encoded id.
- **Params:** `id` (string, **required**) — Yelp business alias or encoded id

### `yelp_business_menu`

- **HTTP:** `GET /yelp/business/{id}/menu`
- **What:** Get Yelp business menu. Fetches menu items for a Yelp business.
- **Params:** `id` (string, **required**) — Yelp business alias or encoded id

### `yelp_business_photos`

- **HTTP:** `GET /yelp/business/{id}/photos`
- **What:** Get Yelp business photos. Fetches the photo gallery for a Yelp business.
- **Params:** `id` (string, **required**) — Yelp business alias or encoded id; `limit` (integer, optional) — Max photos to return, 1-50; `offset` (integer, optional) — Pagination offset

### `yelp_business_review_highlights`

- **HTTP:** `GET /yelp/business/{id}/reviews/highlights`
- **What:** Get Yelp business review highlights. Fetches thematic review snippets (extracted talking points with a supporting quote) for a Yelp business.
- **Params:** `id` (string, **required**) — Yelp business alias or encoded id

### `yelp_business_reviews`

- **HTTP:** `GET /yelp/business/{id}/reviews`
- **What:** Get Yelp business reviews. Fetches reviews for a Yelp business.
- **Params:** `id` (string, **required**) — Yelp business alias or encoded id; `limit` (integer, optional) — Max reviews to return, 1-50; `offset` (integer, optional) — Pagination offset

### `yelp_business_reviews_search`

- **HTTP:** `GET /yelp/business/{id}/reviews/search`
- **What:** Search Yelp business reviews by keyword. Searches a Yelp business's reviews for a keyword, returning a highlighted excerpt per match.
- **Params:** `id` (string, **required**) — Yelp business alias or encoded id; `term` (string, **required**) — Keyword to search reviews for

### `yelp_geocode`

- **HTTP:** `GET /yelp/geocode`
- **What:** Geocode a free-form address. Resolves a free-form address into structured location data (coordinates, city, state, zip, county). Not business-scoped.
- **Params:** `address` (string, **required**) — Free-form address to geocode

### `yelp_search`

- **HTTP:** `GET /yelp/search`
- **What:** Search Yelp businesses. Searches Yelp businesses for a term and location.
- **Params:** `limit` (integer, optional) — Max results to return, 1-50; `location` (string, **required**) — Neighborhood, city, state, or zip code; `offset` (integer, optional) — Pagination offset; `term` (string, **required**) — Search term

## UberEats (5)

### `ubereats_feed`

- **HTTP:** `GET /ubereats/feed`
- **What:** Browse UberEats location feed. Returns restaurants delivering to a specific location: name, rating, review count, delivery estimate, cuisine tags, and cover image.
- **Params:** `latitude` (number, **required**) — Delivery search center latitude; `limit` (integer, optional) — Number of restaurants to return, clamped to 50. Default 20; `longitude` (number, **required**) — Delivery search center longitude; `offset` (integer, optional) — Result offset for the location feed. Default 0

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

### `ubereats_store_reviews`

- **HTTP:** `GET /ubereats/store/{store_id}/reviews`
- **What:** Get UberEats store reviews. Returns the reviews snapshot embedded in an UberEats store page: aggregate rating, review count, and a sample of recent reviews (reviewer name, text, and relative/absolute date). This is a single on-page snapshot, not a full paginated feed. A store with no written reviews returns an empty reviews list.
- **Params:** `store_id` (string, **required**) — UberEats store UUID, as returned by the search endpoint's storeUuid field

## Instacart (6)

### `instacart_departments`

- **HTTP:** `GET /instacart/departments`
- **What:** Get Instacart store department taxonomy. Returns a store's department/category taxonomy (Produce, Dairy & Eggs, Bakery, ...) two levels deep -- department and subcategory. Metadata only, does not return products. Public data sourced from Instacart's own storefront navigation.
- **Params:** `postal_code` (string, **required**) — Postal code to localize the taxonomy for; `shop_id` (string, **required**) — Store's opaque shop id, from GET /instacart/stores; `store_slug` (string, **required**) — Store's retailer slug, from GET /instacart/stores

### `instacart_item`

- **HTTP:** `GET /instacart/item`
- **What:** Get Instacart product detail at a store. Returns a single product's detail at a specific Instacart store: name, size, brand, image, current pricing (with any sale/offer badge), availability, stock level, dietary labels, and nutrition facts. Public data sourced from Instacart's own storefront pages.
- **Params:** `postal_code` (string, **required**) — Postal code to price/localize the lookup for; `product_id` (string, **required**) — Instacart's opaque product id; `retailer_location_id` (string, **required**) — Store's opaque retailer location id, from GET /instacart/stores; `shop_id` (string, **required**) — Store's opaque shop id, from GET /instacart/stores; `store_slug` (string, **required**) — Store's retailer slug, from GET /instacart/stores

### `instacart_search`

- **HTTP:** `GET /instacart/search`
- **What:** Search Instacart product terms at a store. Returns Instacart's own search-term autosuggestions for a keyword within one store -- the same suggestion list shown in the site's own search box dropdown. This is term-level (matching search phrases plus a representative thumbnail), not a paginated product-results list. Public data sourced from Instacart's own storefront search.
- **Params:** `q` (string, **required**) — Free-text search term; `shop_id` (string, **required**) — Store's opaque shop id, from GET /instacart/stores; `store_slug` (string, **required**) — Store's retailer slug, from GET /instacart/stores

### `instacart_search_nearby`

- **HTTP:** `GET /instacart/search-nearby`
- **What:** Search Instacart product terms near a postal code. Returns Instacart's own search-term autosuggestions for a keyword across every retailer serving a postal code at once, rather than one specific store. Public data sourced from Instacart's own cross-retailer search.
- **Params:** `postal_code` (string, **required**) — US postal/ZIP code to search near; `q` (string, **required**) — Free-text search term

### `instacart_stores`

- **HTTP:** `GET /instacart/stores`
- **What:** Find Instacart stores near a postal code. Finds Instacart retailer storefronts (grocery stores, warehouse clubs, and other partner retailers) serving a US postal code, each with the identifiers needed to look up its items and search suggestions. Public data sourced from Instacart's own store-discovery API.
- **Params:** `postal_code` (string, **required**) — US postal/ZIP code to search near

### `instacart_trending`

- **HTTP:** `GET /instacart/trending`
- **What:** Get Instacart trending search terms near a postal code. Returns Instacart's own popular/trending search terms across every retailer serving a postal code -- the same blank-state suggestions shown before a user types anything into the search box. Public data sourced from Instacart's own cross-retailer search.
- **Params:** `postal_code` (string, **required**) — US postal/ZIP code to search near

## OpenTable (4)

### `opentable_restaurant`

- **HTTP:** `GET /opentable/restaurant`
- **What:** Get an OpenTable restaurant's profile and live availability. Returns a restaurant's profile (location, cuisines, hours, price band, review summary) plus real-time bookable timeslots for the given date/time and party size.
- **Params:** `date_time` (string, optional) — Reservation date/time, RFC3339-minute local format; defaults to now; `party_size` (integer, optional) — Party size, default 2; `restaurant_id` (string, **required**) — OpenTable restaurant id

### `opentable_restaurant_menus`

- **HTTP:** `GET /opentable/restaurant/menus`
- **What:** Get an OpenTable restaurant's menus. Returns the menus of one OpenTable restaurant, identified by the required `restaurant_id`. Each menu has a title, a currency and sections, and each section lists items with title, price and description. The price is returned as a string in the menu's currency, for example HK$.
- **Params:** `restaurant_id` (string, **required**) — OpenTable restaurant id

### `opentable_restaurant_reviews`

- **HTTP:** `GET /opentable/restaurant/reviews`
- **What:** Get a page of an OpenTable restaurant's diner reviews. Returns one page of diner reviews for an OpenTable restaurant, identified by the required `restaurant_id`. `page` defaults to 1 and `size` to 20. Each review has its id, author and author's metro area, reservation and posted dates, text, a recommended flag, and ratings for overall, food, service, ambience, value and noise.
- **Params:** `page` (integer, optional) — Page number, default 1; `restaurant_id` (string, **required**) — OpenTable restaurant id; `size` (integer, optional) — Reviews per page, default 20

### `opentable_search`

- **HTTP:** `GET /opentable/search`
- **What:** Search OpenTable restaurants near a location. Searches restaurants by free-text term (cuisine, name, neighborhood) near a latitude/longitude, for a given date/time and party size, including inline live availability per result.
- **Params:** `date_time` (string, optional) — Reservation date/time, RFC3339-minute local format; defaults to now; `latitude` (number, **required**) — Search center latitude; `longitude` (number, **required**) — Search center longitude; `party_size` (integer, optional) — Party size, default 2; `size` (integer, optional) — Max results, default 10; `term` (string, **required**) — Free-text search term

## 7NOW (13)

### `sevennow_catalog`

- **HTTP:** `GET /7now/catalog`
- **What:** Get one 7NOW store's live product catalog. Returns one 7NOW store's browsable category list, a paginated item listing per catalog section (each with real per-item pricing, active promotions, calories, UPC and image), and a live active/out-of-stock inventory count for that store. store_id comes from GET /7now/stores; lat and lon are accepted but inert (store_id alone selects the store). The catalog is genuinely store-scoped, not a national price list. skip/limit page every item section uniformly (limit is capped at 50, defaults to 20).
- **Params:** `lat` (number, optional) — Accepted but inert -- store_id alone selects the store; responses are byte-identical with any value or none. Forwarded upstream for fidelity with 7now.com's own client.; `limit` (integer, optional) — Max items returned per catalog section, 1-50. Defaults to 20.; `lon` (number, optional) — Accepted but inert -- see lat.; `skip` (integer, optional) — Pagination offset, applied uniformly to every catalog section. Defaults to 0.; `store_id` (string, **required**) — 7NOW store id, from GET /7now/stores.

### `sevennow_categories`

- **HTTP:** `GET /7now/categories`
- **What:** List every category id one 7NOW store accepts. Enumerates every value GET /7now/category accepts for a store, so callers do not have to pull the full catalog to discover them. 7NOW has two disjoint id spaces behind that one parameter: `departments` are the store's 10 permanent browsable departments (Fresh Food, Drinks, Snacks, Candy, Ice Cream, Beer & Seltzer, Tobacco, Grocery, Household, Personal Care), and `shelves` are the merchandising rows the homepage currently features ("$2 Deals", "What's New", "Only At 7-Eleven", seasonal ones). Both work as category_id. Shelves rotate with promotions and seasons, so re-read them rather than caching ids long-term. store_id comes from GET /7now/stores; lat and lon are accepted but inert (store_id alone selects the store).
- **Params:** `lat` (number, optional) — Accepted but inert -- store_id alone selects the store; responses are byte-identical with any value or none. Forwarded upstream for fidelity with 7now.com's own client.; `lon` (number, optional) — Accepted but inert -- see lat.; `store_id` (string, **required**) — 7NOW store id, from GET /7now/stores.

### `sevennow_category`

- **HTTP:** `GET /7now/category`
- **What:** Browse one 7NOW store's category by subcategory. Returns one 7NOW store's top-level category broken into its real subcategory groups (e.g. Fresh Food -> Pizza, Wings & Chicken Bites, Subs & Sandwiches, ...), each with its own paginated, priced item list and live availability, plus a category-wide availability summary. Complements GET /7now/catalog, whose per-category section is a single flat list -- this is the same data organized the way 7now.com's own category page groups it. store_id comes from GET /7now/stores and category_id from GET /7now/categories -- which accepts both the store's permanent departments and the merchandising shelves its homepage features, since 7NOW uses one parameter for two id spaces. An invalid or empty category_id returns a normal 200 with an empty subcategories array, not an error.
- **Params:** `category_id` (string, **required**) — Category id, from GET /7now/categories -- either a department or a merchandising shelf.; `limit` (integer, optional) — Max items returned per subcategory group, 1-50. Defaults to 20.; `skip` (integer, optional) — Pagination offset, applied uniformly to every subcategory group. Defaults to 0.; `store_id` (string, **required**) — 7NOW store id, from GET /7now/stores.; `subcategory` (string, optional) — Restrict to one subcategory group by exact name (from a prior call's subcategories[].name).

### `sevennow_combo`

- **HTTP:** `GET /7now/combo`
- **What:** Get one 7NOW bundle deal's pick-from groups. Expands one bundle deal into its structure: each pick-from group's name, how many items the shopper picks from it, and every eligible item with live pricing and availability -- e.g. the "$6.99 Pizza" bundle returns one group, "Eligible Whole Pizzas", holding six priced pizzas. Also returns the bundle's shopper-facing headline and full legal terms. promo_id comes from GET /7now/combos' combos[].promo_id, and store_id from GET /7now/stores. The upstream also accepts a plain item-discount promotion id but answers one with unnamed groups -- for those, GET /7now/promotion's flat item list is the right endpoint. An unknown promo_id returns 404.
- **Params:** `promo_id` (string, **required**) — Promotion id, from GET /7now/combos' combos[].promo_id.; `store_id` (string, **required**) — 7NOW store id, from GET /7now/stores.

### `sevennow_combos`

- **HTTP:** `GET /7now/combos`
- **What:** List a 7NOW store's bundle deals. Lists every bundle deal a store offers -- 7NOW's combo-builder products, where a fixed price buys one item from each of several groups (e.g. "$6.99 Pizza", "Bone In Wing Combo"). GET /7now/search surfaces a combo only when a query happens to match one, so this is the only way to enumerate a store's bundles. Each entry carries the promotion id behind it: pass it to GET /7now/combo for the actual pick-from groups, or to GET /7now/promotion for a flat list of every eligible item. store_id comes from GET /7now/stores; lat and lon are accepted but inert (store_id alone selects the store).
- **Params:** `lat` (number, optional) — Accepted but inert -- store_id alone selects the store; responses are byte-identical with any value or none. Forwarded upstream for fidelity with 7now.com's own client.; `lon` (number, optional) — Accepted but inert -- see lat.; `store_id` (string, **required**) — 7NOW store id, from GET /7now/stores.

### `sevennow_deals`

- **HTTP:** `GET /7now/deals`
- **What:** List every discounted item in one 7NOW store. Returns every currently discounted item in a store, paginated, each with the promotion driving the discount -- its id, shopper-facing description ("2 for $4", "On Sale $7"), promotional price where the offer has a single-unit one, and run dates. A busy store carries several hundred; the response also reports a store-wide availability summary across all of them before paging. This is the store-wide offers listing: the per-category browse endpoints surface promotions only for the items they happen to return, and pulling them all otherwise means walking the entire catalog. Pass a promos[].id to GET /7now/promotion to see every item that same promotion covers. store_id comes from GET /7now/stores; lat and lon are accepted but inert (store_id alone selects the store).
- **Params:** `lat` (number, optional) — Accepted but inert -- store_id alone selects the store; responses are byte-identical with any value or none. Forwarded upstream for fidelity with 7now.com's own client.; `limit` (integer, optional) — Max items returned, 1-100. Defaults to 20.; `lon` (number, optional) — Accepted but inert -- see lat.; `skip` (integer, optional) — Pagination offset. Defaults to 0.; `store_id` (string, **required**) — 7NOW store id, from GET /7now/stores.

### `sevennow_offers`

- **HTTP:** `GET /7now/offers`
- **What:** List a 7NOW store's advertised promotional campaigns. Returns every promotional campaign a store currently advertises -- the headline, body copy, legal terms and artwork behind offers like "$6.99 Pizza" or "2/$5 Gatorade 28oz". This is campaign-level and complements the item-level views: GET /7now/deals answers "which items are discounted and why", while this answers "what is this store advertising, and on what terms". The full legal terms are available nowhere else. Each campaign points somewhere: promo_ids[] feed GET /7now/promotion (or GET /7now/combo when the campaign advertises a bundle), while a category campaign instead carries target_id, a category_id GET /7now/category accepts. store_id comes from GET /7now/stores; lat and lon are accepted but inert (store_id alone selects the store).
- **Params:** `lat` (number, optional) — Accepted but inert -- store_id alone selects the store; responses are byte-identical with any value or none. Forwarded upstream for fidelity with 7now.com's own client.; `lon` (number, optional) — Accepted but inert -- see lat.; `store_id` (string, **required**) — 7NOW store id, from GET /7now/stores.

### `sevennow_popular`

- **HTTP:** `GET /7now/popular`
- **What:** Get 7NOW trending search terms. Returns the trending search terms 7NOW shows in its own search box. Two axes select the index and both matter. vertical picks the catalogue: `convenience` and `restaurant` return different terms for the same store, and `global` is the genuinely national cross-vertical list. store_id (from GET /7now/stores) then narrows to that store's region within the vertical -- a New York store returns index NY_NE, a Florida store SE, and omitting it returns the vertical-wide list. The restaurant vertical is the exception: it ignores store_id entirely, returning identical terms for every store. The response echoes back both the vertical and the regional index the terms came from.
- **Params:** `store_id` (string, optional) — 7NOW store id, from GET /7now/stores. Selects that store's regional index within the chosen vertical; omit for the vertical-wide list. Ignored by the restaurant vertical.; `vertical` (string, optional) — Which trending index to read. One of: convenience, restaurant, global. Defaults to convenience.

### `sevennow_product`

- **HTTP:** `GET /7now/product`
- **What:** Get one 7NOW product's full reference record. Returns one product's complete reference record: description, the full nutrition panel (serving size, calories, fat, cholesterol, sodium, carbohydrates, protein, vitamins and allergen "contains" list), the declared ingredient list, the allergen statement, size and flavor variants, related products, and any attached promotions. product_id comes from GET /7now/search, /7now/catalog or /7now/category. This record is store-independent and deliberately carries no price, availability or stock -- use those three endpoints for per-store pricing and availability. An unknown product_id returns a 404.
- **Params:** `product_id` (string, **required**) — 7NOW product id, from GET /7now/search, /7now/catalog or /7now/category.

### `sevennow_promotion`

- **HTTP:** `GET /7now/promotion`
- **What:** List every item one 7NOW promotion covers. Expands one promotion into every item it applies to in a store, plus the promotion's own offer type, terms, and run dates. GET /7now/deals reads discount-to-item (here is a discounted product, here is why); this reads it the other way round (here is an offer, here is everything it covers) -- e.g. a "2 for $4" tea promotion expands to all five flavours in it. promo_id comes from GET /7now/deals' items[].promos[].id, and store_id from GET /7now/stores. An unknown promo_id returns 404.
- **Params:** `limit` (integer, optional) — Max items returned, 1-100. Defaults to 20.; `promo_id` (string, **required**) — Promotion id, from GET /7now/deals' items[].promos[].id.; `skip` (integer, optional) — Pagination offset. Defaults to 0.; `store_id` (string, **required**) — 7NOW store id, from GET /7now/stores.

### `sevennow_search`

- **HTTP:** `GET /7now/search`
- **What:** Search one 7NOW store's products. Returns one 7NOW store's keyword search results: matching products and combo deals with current pricing (list price, everyday sale price, and any further active promotion), live availability, and a sponsored-brand facet list relevant to the query. store_id comes from GET /7now/stores. A query matching nothing returns a normal 200 with an empty items array, not an error.
- **Params:** `limit` (integer, optional) — Max results returned, 1-50. Defaults to 20.; `q` (string, **required**) — Keyword search term.; `skip` (integer, optional) — Pagination offset. Defaults to 0.; `store_id` (string, **required**) — 7NOW store id, from GET /7now/stores.

### `sevennow_stores`

- **HTTP:** `GET /7now/stores`
- **What:** Find 7NOW delivery stores near an address. Resolves a free-text delivery address, street, city and state, or postal code to the nearest 7NOW-enabled 7-Eleven stores, nearest first. Each store carries its store_id, address, coordinates, straight-line distance in miles from the resolved address, the banner it trades under, its Nielsen DMA, and its per-day alcohol sale windows -- upstream's own encoding of the local law, which is why a day can hold more than one window (a New York store's Sunday runs 0000-0200 and 0800-2359). An empty alcohol_sale_hours means upstream publishes no windows for that store, which is not the same as it selling no alcohol. The response also carries the Uber H3 cell for the resolved address. Use store_id with GET /7now/catalog, /7now/categories, /7now/deals, /7now/offers or /7now/combos to browse that store. An address that cannot be geocoded, or one with no nearby 7NOW coverage, returns a 404.
- **Params:** `address` (string, **required**) — Free-text delivery address, street, city and state, or postal code.

### `sevennow_suggest`

- **HTTP:** `GET /7now/suggest`
- **What:** Get 7NOW search-term suggestions. Returns search-term completions for a partial query, e.g. "chi" -> "chips ahoy", "chips", "chicken". No store is required. q must be at least 3 characters -- shorter values return a typed invalid-param error, matching upstream's own enforced minimum. vertical selects which search index to complete against, and the indexes are materially different rather than variations on one list: for "chi", `convenience` answers "chips ahoy, chips, chicken wings" while `restaurant` answers "chipotle, chinese food, chili". `global` is a sparse cross-vertical index -- many prefixes legitimately return no suggestions there.
- **Params:** `q` (string, **required**) — Partial search term, at least 3 characters.; `vertical` (string, optional) — Which search index to complete against. One of: convenience, restaurant, global. Defaults to convenience.

## Arbys (5)

### `arbys_categories`

- **HTTP:** `GET /arbys/categories`
- **What:** List Arby's menu categories. Returns Arby's US menu's top-level categories -- Slow Roasted Beef, Crispy Juicy Chicken, Meals, Sides & Snacks, Beverages, Desserts, Kids Menu and others. Each entry's slug is the value GET /arbys/menu takes. store_id (optional, default 0) selects which pricing snapshot categories' item counts are read from; the default 0 is Arby's own reference catalog and carries no prices at all -- pass a store_id you already know (for example one you have seen on arbys.com after picking a location) to price GET /arbys/menu's items against a specific store. There is no location-lookup endpoint in this family.
- **Params:** `store_id` (integer, optional) — Optional. Store id to read the catalog from, default 0 (Arby's priceless national reference catalog).

### `arbys_directory`

- **HTTP:** `GET /arbys/directory`
- **What:** Browse Arby's US store directory by state and city. Returns one level of Arby's US store directory: every state Arby's serves with its store count (no params), one state's cities (state given), or one city's stores (state and city given) -- id, address, and phone only, pair with GET /arbys/location for hours/amenities/status. Unlike GET /arbys/locations, this needs no coordinate; it is a plain browse of the whole ~3,200-store US chain.
- **Params:** `city` (string, optional) — Optional. City name, requires state. Omit to list every city in the state.; `state` (string, optional) — Optional. Two-letter US state abbreviation. Omit to list every state.

### `arbys_location`

- **HTTP:** `GET /arbys/location`
- **What:** Look up one Arby's restaurant by store id. Returns one Arby's restaurant directly by its store id (e.g. one found via GET /arbys/locations), with the same address, hours, amenities, and capability fields as that endpoint's results, minus distance (there is no search center for a direct lookup).
- **Params:** `store_id` (integer, **required**) — A real Arby's store id, e.g. one returned by GET /arbys/locations

### `arbys_locations`

- **HTTP:** `GET /arbys/locations`
- **What:** Find Arby's restaurants near a coordinate. Returns Arby's restaurants within a radius of a coordinate, nearest first, with address, phone, coordinates, distance, open/closed status, hours, amenities, and pickup/delivery capability flags. Each result's store_id also prices GET /arbys/menu and GET /arbys/categories. To search from a free-text address instead of coordinates, resolve it first with GET /geocoding/search.
- **Params:** `latitude` (number, **required**) — Search center latitude; `limit` (integer, optional) — Optional. Maximum stores per page, 1-50, default 10.; `longitude` (number, **required**) — Search center longitude; `page` (integer, optional) — Optional. Zero-based page index, default 0.; `radius` (integer, optional) — Optional. Search radius in miles, 1-50, default 50. Upstream hard-blocks any radius over 50.

### `arbys_menu`

- **HTTP:** `GET /arbys/menu`
- **What:** List one Arby's menu category's items with full nutrition and price. Returns the items in one Arby's menu category, each with its stable product code, name, description, image, tags, availability, a full per-serving nutrition panel (calories, total and saturated fat, trans fat, cholesterol, sodium, carbohydrate, fiber, sugar, protein and serving weight), and a price when store_id resolves to a priced catalog. Category slugs come from GET /arbys/categories. store_id (optional, default 0) is Arby's own priceless national reference catalog; pass a store_id you already know to get that store's pricing instead -- there is no location-lookup endpoint in this family, so store_id is a passthrough value, not something this API can look up for you. A price of exactly 0 on an item is a genuine free add-on, distinct from the default catalog's complete absence of pricing.
- **Params:** `category` (string, **required**) — Category slug from /arbys/categories; `store_id` (integer, optional) — Optional. Same store id semantics as /arbys/categories.

## Burger King (4)

### `burgerking_availability`

- **HTTP:** `GET /burgerking/availability`
- **What:** Get one Burger King restaurant's real-time fulfillment status. Returns one restaurant's live open/closed status per order channel (curbside, delivery, drive-thru, eat-in, mobile-order drive-thru, takeout), distinct from /burgerking/locations' published weekly schedule. Each channel carries whether it is taking orders right now, its current open window when open, and the following window's start/end -- a channel with no current or next window at all means this restaurant does not offer it, not merely that it is closed. Also returns the restaurant's own local time, timezone and an overall available flag. Setting forecast=true additionally returns a multi-day forward schedule per channel, including two catering-only channels not present in the current-status list.
- **Params:** `forecast` (boolean, optional) — Include a multi-day forward schedule per channel (default false); `market` (string, optional) — RBI market the store belongs to, one of `US`, `CA` (default `US`); `store_id` (string, **required**) — Burger King's numeric store id, from /burgerking/locations

### `burgerking_locations`

- **HTTP:** `GET /burgerking/locations`
- **What:** Find Burger King restaurants near a location. Returns Burger King restaurants near a latitude/longitude. Each restaurant carries its internal id and numeric store id (the value /burgerking/menu and /burgerking/availability take), full address with coordinates, phone, the operating franchise group, amenity flags (breakfast, delivery, drive-thru, playground, takeout, wifi, halal, dark kitchen) and the full published week of hours for dining room, drive-thru, delivery and curbside separately. A coordinate with no nearby Burger King returns an empty list rather than an error. Setting include_availability=true additionally returns each restaurant's live per-channel open/closed status in one call, the same shape /burgerking/availability returns -- note that path is capped at a fixed page (up to 20 restaurants) rather than honoring max_results beyond that. Setting delivery_only=true instead restricts results to restaurants that Burger King's own delivery service actually considers deliverable to this coordinate -- a genuine delivery-zone match, not the same set as filtering has_delivery=true. include_availability and delivery_only cannot be combined.
- **Params:** `delivery_only` (boolean, optional) — Restrict to restaurants that actually deliver to this coordinate, a genuine delivery-zone match distinct from the has_delivery flag (default false); `include_availability` (boolean, optional) — Include each restaurant's live per-channel open/closed status (default false); `latitude` (number, **required**) — Search center latitude; `longitude` (number, **required**) — Search center longitude; `market` (string, optional) — RBI market to search, one of `US`, `CA` (default `US`); `max_results` (integer, optional) — Maximum restaurants to return, 1-50 (default 20); `radius` (integer, optional) — Search radius in meters, 1-50000 (default 8000)

### `burgerking_menu`

- **HTTP:** `GET /burgerking/menu`
- **What:** Get one Burger King restaurant's full priced menu. Returns one restaurant's full menu grouped into categories (e.g. "Breakfast Sandwiches", "Flame Grilled Burgers"). Every entry is an item, a combo, or a picker (a variant-choice product such as "choose your drink size") and carries a delivery and pickup price -- these genuinely differ -- plus calories, detailed nutrition facts and flagged allergens when Burger King publishes them, and an image. Prices and availability reflect this specific restaurant, not a national default.
- **Params:** `market` (string, optional) — RBI market the store belongs to, one of `US`, `CA` (default `US`); `store_id` (string, **required**) — Burger King's numeric store id, from /burgerking/locations

### `burgerking_product`

- **HTTP:** `GET /burgerking/product`
- **What:** Get one Burger King item, combo, or picker's full detail and customization tree. Returns one menu entry's full detail (name, description, price, image, nutrition, allergens) plus its customization tree, when it has one -- a combo's courses and their swappable entree/side/drink choices, a picker's size/variant choices, or a customizable item's ingredient toggle groups (e.g. "Bacon": no/regular/extra) and their price deltas. Options recurses through the full upstream structure, so a combo's entree choice carries its own ingredient toggles too, not just the combo's own top-level courses. A plain, non-customizable item returns an empty options list.
- **Params:** `item_id` (string, **required**) — The item, combo, or picker id, from /burgerking/menu; `market` (string, optional) — RBI market the store belongs to, one of `US`, `CA` (default `US`); `store_id` (string, **required**) — Burger King's numeric store id, from /burgerking/locations

## Chick-fil-A (8)

### `chick_fil_a_content`

- **HTTP:** `GET /chick-fil-a/content`
- **What:** Browse Chick-fil-A press releases, legal documents and press-kit assets. Returns one page of a Chick-fil-A editorial corpus. `type` selects which: `press-room` (289 press releases), `story` (189 blog articles), `page` (147 standalone corporate pages such as hunger relief and community programmes), `legal` (28 terms, policies and promotion rules) or `downloadable-asset` (45 press-kit media entries, which carry a title and link only and never a body). Between them these are every content-bearing corpus Chick-fil-A publishes outside the menu and restaurant catalogs. Article bodies are opt-in via include_body because a single press release runs to roughly 22KB, so a default-on page of 20 would be several hundred KB; without it the endpoint returns titles, links, publish dates and excerpts.
- **Params:** `include_body` (boolean, optional) — Include the full article body (default false -- bodies are large); `page` (integer, optional) — 1-based page number (default 1); `per_page` (integer, optional) — Entries per page, 1-100 (default 20); `search` (string, optional) — Free-text filter. Results are relevance-ranked when present; otherwise newest first.; `type` (string, **required**) — Which corpus. One of press-room, story, page, legal, downloadable-asset.

### `chick_fil_a_content_taxonomy`

- **HTTP:** `GET /chick-fil-a/content-taxonomy`
- **What:** List the category and tag vocabularies Chick-fil-A classifies its content under. Returns one page of a content taxonomy's terms, each with its id, name, slug, parent and the number of entries carrying it. Every id is a ready-to-use `category` or `tag` filter value on GET /chick-fil-a/content, which is what makes the editorial corpora navigable rather than only pageable. `taxonomy` selects the vocabulary: `press_category` (16 terms) and `press_tag` (96) classify press releases, `story_category` (9) and `story_tag` (74) classify blog stories, `legal_category` (8) and `downloadable_asset_category` (7) classify those corpora, and `campaign` (9) is applied across several at once. Terms are ordered by name.
- **Params:** `page` (integer, optional) — 1-based page number (default 1); `per_page` (integer, optional) — Terms per page, 1-100 (default 20); `taxonomy` (string, **required**) — Which vocabulary. One of press_category, press_tag, story_category, story_tag, legal_category, downloadable_asset_category, campaign.

### `chick_fil_a_faq`

- **HTTP:** `GET /chick-fil-a/faq`
- **What:** Browse Chick-fil-A customer FAQs. Returns one page of Chick-fil-A's published customer FAQ corpus (522 entries at time of writing) across 30 categories -- Chick-fil-A One membership, points and rewards, digital ordering and payment, delivery support, sweepstakes terms, and more. Each entry carries the question, the answer as plain text, the answer's original HTML (a fair number of answers use links, lists and tables that plain text loses), and its resolved categories. Every categories[].id is a ready-to-use value for the category filter. search matches over question and answer text and is relevance-ranked; without it entries come back alphabetically so a caller can page through the whole corpus deterministically.
- **Params:** `category` (string, optional) — Comma-separated faq_category term ids, up to 20, from any prior response's categories[].id; `page` (integer, optional) — 1-based page number (default 1); `per_page` (integer, optional) — Entries per page, 1-100 (default 20); `search` (string, optional) — Free-text filter over question and answer text. Results are relevance-ranked when present.

### `chick_fil_a_location`

- **HTTP:** `GET /chick-fil-a/location`
- **What:** Get one Chick-fil-A restaurant's address and hours. Returns one Chick-fil-A restaurant's street address, opening hours, cuisine description and photo, selected by either its numeric id or its slug (supply exactly one of the two -- passing both is rejected). opening_hours carries one entry per day; a day Chick-fil-A publishes as closed (notably every Sunday, and every day for a seasonal or food-truck location that is not currently operating) comes back with closed=true and empty opens/closes rather than a placeholder time. This response carries a postal address but no latitude/longitude -- Chick-fil-A does not publish coordinates for its restaurants, and this endpoint does not synthesize them.
- **Params:** `id` (integer, optional) — Numeric WordPress post id. Supply either id or slug, not both.; `slug` (string, optional) — Restaurant slug, e.g. from a directory response. Supply either id or slug, not both.

### `chick_fil_a_locations`

- **HTTP:** `GET /chick-fil-a/locations`
- **What:** Browse Chick-fil-A restaurant locations. Returns one page of Chick-fil-A's restaurant directory (3,467 restaurants at time of writing): each restaurant's id, slug, name, US state and its page URL. search filters by free text over restaurant names and is relevance-ranked; without it restaurants come back alphabetically so a caller can page through the whole directory deterministically. This index deliberately carries no address or hours -- Chick-fil-A does not expose them on the directory listing. Pass a slug from here to GET /chick-fil-a/location to get street address and opening hours for one restaurant.
- **Params:** `page` (integer, optional) — 1-based page number (default 1); `per_page` (integer, optional) — Restaurants per page, 1-100 (default 20); `search` (string, optional) — Free-text filter over restaurant names. Results are relevance-ranked when present.

### `chick_fil_a_menu`

- **HTTP:** `GET /chick-fil-a/menu`
- **What:** Browse the Chick-fil-A menu. Returns one page of Chick-fil-A's published menu catalog (567 items at time of writing): item name, slug, Chick-fil-A's own item tag, an ordering deep link, and the taxonomy term ids the item belongs to. Every id in a response's menu_taxonomy_ids, menu_item_type_ids, menu_item_group_ids and nutrition_table_menu_ids is a ready-to-use filter value for a follow-up call, and GET /chick-fil-a/menu-taxonomy lists each taxonomy's terms with their names. search filters by free text and is ranked by relevance; without it items come back alphabetically so a caller can page through the whole catalog deterministically. Note this catalog carries no prices or nutrition values -- Chick-fil-A does not publish either through this source.
- **Params:** `menu_item_group` (string, optional) — Comma-separated menu_item_group term ids (the grouping a variant belongs to), up to 20; `menu_item_type` (string, optional) — Comma-separated menu_item_type term ids (ITEM, ITEM_GROUPING, MODIFIER), up to 20; `menu_taxonomy` (string, optional) — Comma-separated menu_taxonomy term ids (menu section, e.g. Breakfast, Beverages), up to 20; `nutrition_table_menu` (string, optional) — Comma-separated nutrition_table_menu term ids (published nutrition-table grouping), up to 20; `page` (integer, optional) — 1-based page number (default 1); `per_page` (integer, optional) — Items per page, 1-100 (default 20); `search` (string, optional) — Free-text filter over item names. Results are relevance-ranked when present.

### `chick_fil_a_menu_item`

- **HTTP:** `GET /chick-fil-a/menu-item`
- **What:** Get one Chick-fil-A menu item. Returns one Chick-fil-A menu item, selected by either its numeric id or its slug (supply exactly one of the two -- passing both is rejected). Unlike the listing endpoint, this resolves the item's taxonomy term ids to names, so menu_sections, item_types, item_groups and nutrition_tables each come back as {id, name, slug} triples rather than bare ids. Term resolution is best-effort: if the taxonomy lookups fail the item is still returned with ids and empty names rather than failing the whole call. This item detail carries no price and no nutrition values -- Chick-fil-A does not publish either through this source.
- **Params:** `id` (integer, optional) — Numeric WordPress post id. Supply either id or slug, not both.; `slug` (string, optional) — Item slug, e.g. from a listing response. Supply either id or slug, not both.

### `chick_fil_a_menu_taxonomy`

- **HTTP:** `GET /chick-fil-a/menu-taxonomy`
- **What:** List one Chick-fil-A menu taxonomy's terms. Returns one page of terms for a single Chick-fil-A menu taxonomy, with each term's id, name, slug, parent and how many menu items carry it. This is how to discover the filter ids GET /chick-fil-a/menu accepts. taxonomy must be one of `menu_taxonomy` (customer-facing menu section -- Breakfast, Beverages, Catering Entrées, ... 36 terms), `menu_item_type` (`ITEM`, `ITEM_GROUPING`, `MODIFIER` -- 3 terms), `menu_item_group` (the grouping a variant belongs to, e.g. "Bacon, Egg & Cheese Biscuit" -- 100+ terms), or `nutrition_table_menu` (the grouping used by Chick-fil-A's published nutrition tables -- 18 terms). Terms come back alphabetically.
- **Params:** `page` (integer, optional) — 1-based page number (default 1); `per_page` (integer, optional) — Terms per page, 1-100 (default 20); `taxonomy` (string, **required**) — Which taxonomy to list. One of menu_taxonomy, menu_item_type, menu_item_group, nutrition_table_menu.

## Chipotle (8)

### `chipotle_ingredients`

- **HTTP:** `GET /chipotle/ingredients`
- **What:** Get Chipotle's ingredient content catalog. Returns Chipotle's raw-ingredient content pages -- sourcing story, marketing copy, imagery -- and the per-item recipe breakdown. ingredients[] has one entry per raw ingredient (Avocado, Yellow Onion, ...), each with its facts/sourcing copy and the menu_item_ids it appears in. ingredient_groups[] is the reverse view: one entry per recipe category (proteins, rice and beans, ...) listing each item's exact ingredient_keys, joinable against ingredients[].key for the human-readable name. Nothing else in this family exposes either ingredient content or recipe-level composition.
- **Params:** `channel` (string, optional) — Ordering surface. One of web, web-mobile. Default web-mobile.; `region` (string, optional) — Country catalog. One of US, CA. Default US.

### `chipotle_meals`

- **HTTP:** `GET /chipotle/meals`
- **What:** Get Chipotle's preset meal definitions. Returns Chipotle's preset meal definitions -- the named combinations its ordering flow offers (Build-Your-Own Chicken and similar), each with an id, name, type and a description listing what the meal contains. Takes no parameters.
- **Params:** _none_

### `chipotle_menu`

- **HTTP:** `GET /chipotle/menu`
- **What:** Get Chipotle's national menu catalog. Returns Chipotle's restaurant-independent menu catalog -- every item it sells nationally, split into entrees, sides and drinks, with each item's category, type, primary filling and full customization tree. Takes no parameters. Prices are deliberately omitted from this response: Chipotle prices per restaurant, so the upstream returns every price as zero here, and surfacing a field of zeros would read as "free" rather than "unpriced". Use GET /chipotle/restaurant/menu for real prices.
- **Params:** _none_

### `chipotle_menu_metadata`

- **HTTP:** `GET /chipotle/menu/metadata`
- **What:** Get Chipotle's menu presentation metadata. Returns Chipotle's menu presentation metadata -- the data no other Chipotle endpoint carries. Categories are the menu nav sections (Burrito, Bowl, Salad, ...) with their own description, imagery and the customization sections each offers. Items carry per-item nutrition (calories and portion) and dietary tag codes. Item sections and item groups describe the customization pick-groups and shared item aliases (e.g. cauliflower rice offered as both an entree side and a taco filling). Dietary tag groups are the full tag taxonomy (Plant Based, Lifestyle, I'm Avoiding, ...) that item dietary tag codes join against for a human-readable name and badge. Join on item_id against /chipotle/menu or /chipotle/restaurant/menu for prices; this endpoint has none.
- **Params:** `channel` (string, optional) — Ordering surface. One of web, web-mobile. Default web-mobile.; `region` (string, optional) — Country catalog. One of US, CA. Default US.

### `chipotle_restaurant`

- **HTTP:** `GET /chipotle/restaurant`
- **What:** Get one Chipotle restaurant. Returns one Chipotle restaurant by its numeric restaurant number. Note this single-restaurant route returns a leaner record than GET /chipotle/restaurants: the proximity search accepts an embeds parameter that pulls in hours and capability flags, and no such parameter exists here, so those fields may be absent. If you need the full record for a known restaurant, call /chipotle/restaurants with a tight radius around it instead.
- **Params:** `restaurant_number` (string, **required**) — Chipotle's numeric restaurant id

### `chipotle_restaurant_meals`

- **HTTP:** `GET /chipotle/restaurant/meals`
- **What:** List one Chipotle restaurant's preset meals with prices. Returns the preset meals one Chipotle restaurant sells -- group Build-Your-Own packs, the High Protein line and limited-time Influencer meals -- each with its dine-in and delivery price at that restaurant, calorie label, dietary and macro tags, the components that make it up, merchandising tags and images. Prices are genuinely restaurant-specific: the same Build-Your-Own Chicken pack is priced differently from one location to another, so this is the endpoint to use for real pricing rather than /chipotle/meals, which lists the national meal definitions with no prices at all. Calorie labels are a range for build-your-own meals and a single figure for fixed ones, so they are returned as strings. Restaurant numbers come from GET /chipotle/restaurants.
- **Params:** `meal_type` (string, optional) — Filter to one meal family. One of BuildYourOwn, HighProtein, Influencer.; `restaurant_number` (string, **required**) — Chipotle's numeric restaurant id, from /chipotle/restaurants

### `chipotle_restaurant_menu`

- **HTTP:** `GET /chipotle/restaurant/menu`
- **What:** Get one Chipotle restaurant's menu with prices. Returns one restaurant's live online menu split into entrees, sides, drinks and non-food items. This is the only Chipotle endpoint that carries prices: every item has both a dine-in price and a delivery price, which genuinely differ. Each item also carries its full customization tree -- contents (the individual fillings, salsas and sides that make it up, each with their own price pair) and content_groups (how many picks each group allows). Prices are per-restaurant, so two restaurants will legitimately return different numbers for the same item.
- **Params:** `include_unavailable` (boolean, optional) — Include items the restaurant currently has unavailable (default false); `restaurant_number` (string, **required**) — Chipotle's numeric restaurant id

### `chipotle_restaurants`

- **HTTP:** `GET /chipotle/restaurants`
- **What:** Find Chipotle restaurants near a location. Returns Chipotle restaurants near a latitude/longitude, ordered by distance. Each restaurant carries its number (the id every other Chipotle endpoint takes), name, status, full postal address with coordinates, published open/close hours per day, nearest cross streets, timezone, and capability flags (Chipotlane pickup, online ordering, catering, curbside pickup, dining room open, walk-up window). A coordinate with no Chipotle nearby returns an empty list rather than an error.
- **Params:** `latitude` (number, **required**) — Search center latitude; `longitude` (number, **required**) — Search center longitude; `page` (integer, optional) — 0-based page index (default 0); `page_size` (integer, optional) — Restaurants per page, 1-50 (default 10); `radius` (integer, optional) — Search radius in meters, 1-80000 (default 8000)

## Culvers (7)

### `culvers_calendar`

- **HTTP:** `GET /culvers/calendar`
- **What:** Get one Culver's restaurant's flavor-of-the-day and daily soup schedule. Returns the full published schedule for one Culver's restaurant: the flavor of the day for every upcoming calendar date, plus the soups served on each date. Culver's publishes roughly a two-month forward window, and the schedule is genuinely per-restaurant -- two restaurants on the same date routinely feature different soups. slug comes from GET /culvers/directory. GET /culvers/store returns only today's and tomorrow's flavor; use this endpoint for the whole calendar.
- **Params:** `slug` (string, **required**) — Restaurant slug from /culvers/directory

### `culvers_categories`

- **HTTP:** `GET /culvers/categories`
- **What:** List Culver's national menu categories. Returns Culver's national menu's category list -- ButterBurgers, Chicken, Fish & Seafood, Combos & Baskets, Sides, Frozen Custard, Beverages and others -- each with its slug (the value GET /culvers/menu takes), a featured flag, and sort order.
- **Params:** _none_

### `culvers_directory`

- **HTTP:** `GET /culvers/directory`
- **What:** Browse Culver's restaurant-URL index. Returns one page of Culver's restaurant index, which covers about 1,121 restaurants. `page` starts at 1 and `page_size` runs 1 to 500 (default 100). Each entry has a `slug`, the value the `/culvers/store` endpoint takes, and the restaurant's URL. The total and page counts are included.
- **Params:** `page` (integer, optional) — Optional. 1-based page, default 1.; `page_size` (integer, optional) — Optional. Entries per page, 1-500, default 100.

### `culvers_flavor`

- **HTTP:** `GET /culvers/flavor`
- **What:** Get one Culver's Fresh Frozen Custard flavor's detail. Returns one Fresh Frozen Custard flavor's full detail, including its declared allergens, a component-by-component ingredient breakdown, and Culver's own flavor-category labels. slug comes from GET /culvers/calendar (flavors[].slug) or GET /culvers/store (flavors_of_the_day[].slug).
- **Params:** `slug` (string, **required**) — Flavor slug from /culvers/calendar or /culvers/store

### `culvers_item`

- **HTTP:** `GET /culvers/item`
- **What:** Look up one Culver's menu item's full detail. Returns one Culver's menu item's full detail, including its size/topping modifier tree with each option's own calories and nutrition link. category and item slugs come from GET /culvers/categories and GET /culvers/menu.
- **Params:** `category` (string, **required**) — Category slug from /culvers/categories; `item` (string, **required**) — Item slug from /culvers/menu

### `culvers_menu`

- **HTTP:** `GET /culvers/menu`
- **What:** List one Culver's menu category's items. Returns the items in one Culver's menu category, each with name, description, image, and a link to Culver's nutrition guide. Category slugs come from GET /culvers/categories. Prices are not published on the national catalog -- Culver's only prices items once a specific restaurant is selected; see GET /culvers/item for full modifier/topping detail.
- **Params:** `category` (string, **required**) — Category slug from /culvers/categories

### `culvers_store`

- **HTTP:** `GET /culvers/store`
- **What:** Look up one Culver's restaurant by its directory slug. Returns one Culver's restaurant's address, phone, coordinates, open/closed status, fulfillment hours, handoff options, online-order link, and today's flavor(s) of the day. slug comes from GET /culvers/directory.
- **Params:** `slug` (string, **required**) — Restaurant slug from /culvers/directory

## Deliveroo (5)

### `deliveroo_fulfillment_times`

- **HTTP:** `GET /deliveroo/fulfillment-times`
- **What:** Get Deliveroo's live delivery and pickup scheduling windows for a location. Returns the exact same "Choose a day" / "Choose a time" scheduled-ordering data the real site's own order-ahead picker shows for a location, for both delivery and pickup: an ASAP option plus every day currently open for a scheduled order, each with its real time slots and UNIX timestamps.
- **Params:** `latitude` (number, **required**) — Search center latitude; `longitude` (number, **required**) — Search center longitude; `market` (string, optional) — Deliveroo national market to search (default uk)

### `deliveroo_restaurant`

- **HTTP:** `GET /deliveroo/restaurant`
- **What:** Get one Deliveroo restaurant, grocery, or shopping partner's detail. Returns one Deliveroo partner's detail by uname -- restaurant, grocery, or shopping store alike, distinguished by branch_type: name, address, currency, branch/fulfillment type, rating, review count, a hero image, and whether it currently accepts orders.
- **Params:** `market` (string, optional) — Deliveroo national market the uname was found in (default uk); `uname` (string, **required**) — Restaurant slug, from a search response's uname field

### `deliveroo_restaurant_menu`

- **HTTP:** `GET /deliveroo/restaurant/menu`
- **What:** Get one Deliveroo restaurant, grocery, or shopping partner's priced catalog. Returns one partner's full menu or catalog grouped into categories -- restaurant menus, grocery aisles, and shopping-store catalogs all use this same endpoint (see /deliveroo/search's collection parameter). Every item carries a name, description, product-meta text when the upstream provides it (calorie counts on restaurant items, per-unit pricing like "380g · £15.79/kg" on grocery/shopping items), price, availability, and its resolved customization options (e.g. "Choose your meal", "Add ingredients?") with each option's own price and required/multi-select bounds.
- **Params:** `market` (string, optional) — Deliveroo national market the uname was found in (default uk); `uname` (string, **required**) — Restaurant slug, from a search response's uname field

### `deliveroo_search`

- **HTTP:** `GET /deliveroo/search`
- **What:** Search Deliveroo restaurants, groceries, or shopping stores near a location. Returns the restaurants (or, with collection set, grocery/shopping stores) Deliveroo's own catalog serves for a latitude/longitude in the given market -- the location's entire feed, not a curated subset (confirmed live: up to 2,700+ results for a single coordinate). Each result carries its uname (the value the restaurant and menu endpoints take), name, image, branch_type, and, when available, rating, delivery time, and distance. Optional collection, cuisine, dietary, dish, min_rating, max_delivery_minutes, max_delivery_fee_pounds, has_offer, deliveroos_choice, and sort parameters narrow and order the same feed -- call /deliveroo/search/filters for the current, complete, location-scoped list of every valid cuisine/dietary/dish value with live result counts. A location with no coverage returns an empty list rather than an error.
- **Params:** `collection` (string, optional) — Optional, passed straight through to the upstream. Selects the Deliveroo partner vertical: omit for restaurants/takeaways (default), grocery for supermarkets and convenience stores, shopping for non-food retail -- both confirmed live; other values may exist and are not rejected. Every result uses the same uname contract for /deliveroo/restaurant and /deliveroo/restaurant/menu.; `cuisine` (array, optional) — Optional, repeatable Deliveroo cuisine filter, e.g. cuisine=american&cuisine=asian. Passed straight through to the upstream; call /deliveroo/search/filters for the current, complete, location-scoped list of valid values. An unrecognized value is silently ignored by the upstream, not rejected.; `deliveroos_choice` (boolean, optional) — When true, only returns results in Deliveroo's own Deliveroo's Choice curated collection. Combines with collection (e.g. collection=grocery&deliveroos_choice=true narrows to Deliveroo's Choice within the grocery vertical) rather than conflicting with it.; `dietary` (array, optional) — Optional, repeatable Deliveroo dietary filter passed straight through to the upstream, e.g. dietary=vegan. Call /deliveroo/search/filters for the current, complete list of valid values. An unrecognized value is silently ignored by the upstream, not rejected.; `dish` (array, optional) — Optional, repeatable Deliveroo dish-level filter passed straight through to the upstream, e.g. dish=pizza&dish=sushi. Call /deliveroo/search/filters for the current, complete, location-scoped list of valid values. An unrecognized value is silently ignored by the upstream, not rejected.; `has_offer` (boolean, optional) — When true, only returns results currently running an offer/promotion; `latitude` (number, **required**) — Search center latitude; `limit` (integer, optional) — Restaurants to return, clamped to 100 (default 20); `longitude` (number, **required**) — Search center longitude; `market` (string, optional) — Deliveroo national market to search (default uk); `max_delivery_fee_pounds` (integer, optional) — Maximum delivery fee in GBP; `max_delivery_minutes` (integer, optional) — Maximum estimated delivery time in minutes; `min_rating` (number, optional) — Minimum star rating filter; `sort` (string, optional) — Result ordering; `top_rated` (boolean, optional) — When true, only returns results Deliveroo itself marks top-rated (its own 4.5+ threshold). Equivalent to min_rating=4.5; ignored if min_rating is also set.

### `deliveroo_search_filters`

- **HTTP:** `GET /deliveroo/search/filters`
- **What:** Get Deliveroo's live search filter and sort catalog for a location. Returns the exact same sort and filter catalog -- every cuisine, dietary tag, dish, delivery-time tier, delivery-fee tier, star-rating tier, and offer flag, each with a live result count for this location -- that the real search page's own filter dropdowns are populated from. Every option's query_param/query_value pair is the literal query string /deliveroo/search accepts for that filter.
- **Params:** `latitude` (number, **required**) — Search center latitude; `longitude` (number, **required**) — Search center longitude; `market` (string, optional) — Deliveroo national market to search (default uk)

## Dominos (6)

### `dominos_coupons`

- **HTTP:** `GET /dominos/coupons`
- **What:** Get one Domino's store's available coupons and deals. Returns one Domino's US store's available coupons and deals: standalone coupons (code, name, description, price, valid service methods, and any alternate promo/marketing codes that resolve to the same coupon), plus tiered volume-discount coupon groups (e.g. "order 7+ pizzas, get 15% off"). Reads the same structured menu response as GET /dominos/menu, so it costs no additional upstream request. A store can genuinely have zero active coupons -- an empty list is not an error. Store ids come from GET /dominos/store-locator. An unknown store id returns 404.
- **Params:** `store_id` (string, **required**) — Domino's store id, from /dominos/store-locator

### `dominos_customization`

- **HTTP:** `GET /dominos/customization`
- **What:** Get one Domino's store's full build-your-own customization catalog. Returns one Domino's US store's full build-your-own customization catalog, grouped by product category (Domino's own names, e.g. "BuildYourOwnDomino" for pizza, "GSalad" for garden salads): every selectable size, crust/flavor style, topping, and side, each with its own code, name, description, dietary/placement flags (e.g. Meat, Vege, Sauce, WholeOnly), and any other attributes Domino's attaches (e.g. ExclusiveGroup for mutually-exclusive options). Also returns cooking instructions (bake level, cut style, seasoning), grouped. Store ids come from GET /dominos/store-locator. An unknown store id returns 404.
- **Params:** `store_id` (string, **required**) — Domino's store id, from /dominos/store-locator

### `dominos_menu`

- **HTTP:** `GET /dominos/menu`
- **What:** Get one Domino's store's full structured menu. Returns one Domino's US store's full menu, as a flat list of categories (each with a stable code/name path, e.g. "Pizza > Specialty Pizzas") and their items. Each item carries its code, name, description, and product type, plus every purchasable variant (size/style) with its own code, name, and price. Store ids come from GET /dominos/store-locator. An unknown store id returns 404.
- **Params:** `store_id` (string, **required**) — Domino's store id, from /dominos/store-locator

### `dominos_nutrition`

- **HTTP:** `GET /dominos/nutrition`
- **What:** Get calorie information for one Domino's product configuration. Returns calorie information (Domino's own "Cal-O-Meter" data) for one product at one store. For a named/fixed menu item (a specialty pizza, bread, wing, pasta, sandwich, salad, drink, or dessert -- any item code from GET /dominos/menu), give only store_id and product_code; the item's default configuration is used. For a build-your-own pizza, also give size, base, and any topping codes -- calories are computed for that exact configuration, matching Domino's own live calculator. size and base must be given together; toppings requires both. Reads live, not from a cache -- each call creates and discards one anonymous cart server-side, so it is slower than this family's other endpoints. An unknown product code, or an invalid size/base/topping combination, returns an error.
- **Params:** `base` (string, optional) — Build-your-own crust code. Required together with size.; `product_code` (string, **required**) — A product code from /dominos/menu's items[].code -- a named/fixed item, or a build-your-own base (e.g. S_PIZZA); `size` (string, optional) — Build-your-own size code, from /dominos/menu's variants. Required together with base.; `store_id` (string, **required**) — Domino's store id, from /dominos/store-locator; `toppings` (array, optional) — Repeatable. Topping codes to add to a build-your-own pizza. Only used together with size+base.

### `dominos_store`

- **HTTP:** `GET /dominos/store`
- **What:** Get one Domino's store's full profile record. Returns one Domino's US store's full profile -- richer than /dominos/store-locator's per-store summary. Includes the store's complete weekly hours (general hours and each service method's own hours, Monday-first, with every open/close window per day), Domino's own free-text hours summary per service method, per-service-method estimated wait windows, open/online status, per-service-method order availability (delivery, carryout, drive-up carryout, dine-in), contactless option status, and delivery/carryout order minimums. Store ids come from GET /dominos/store-locator. An unknown store id returns 404.
- **Params:** `store_id` (string, **required**) — Domino's store id, from /dominos/store-locator

### `dominos_store_locator`

- **HTTP:** `GET /dominos/store-locator`
- **What:** Find Domino's stores near an address, city/state, or ZIP code. Returns Domino's US stores that can serve a location: store id, address with coordinates, phone, open/online status, per-service-method availability (delivery, carryout, drive-up carryout), contactless option status, Domino's own hours summary per service method, and estimated wait windows. At least one of postal_code, or both city and state, is required; address is an optional street line that improves precision when combined with city/state. The response's query field echoes how Domino's own address resolver actually interpreted the input, including its granularity (e.g. resolved to a specific street range vs. only a city/region).
- **Params:** `address` (string, optional) — Optional street address line; `city` (string, optional) — City name (required together with state if postal_code is not given); `postal_code` (string, optional) — US ZIP code (can be used alone instead of city/state); `service_method` (string, optional) — One of: Delivery, Carryout. Default Delivery; `state` (string, optional) — Two-letter US state code (required together with city if postal_code is not given)

## Dunkin (4)

### `dunkin_directory`

- **HTTP:** `GET /dunkin/directory`
- **What:** Browse the Dunkin store directory. Returns one level of Dunkin's store directory tree. Omit path for the root, which lists every US state Dunkin operates in; pass a state's path (e.g. "ny") to list its cities, or a state/city path (e.g. "ny/new-york") to list its stores. Each child carries its name, path, URL and how many stores sit under that branch. A child with is_store true is a store rather than another directory level -- pass its path (a store id) to GET /dunkin/store. This is a directory browse, not a proximity search: use GET /dunkin/nearby for a radius lookup.
- **Params:** `path` (string, optional) — Directory path from a previous response's children[].path: a state code (e.g. \

### `dunkin_menu`

- **HTTP:** `GET /dunkin/menu`
- **What:** Get Dunkin's national menu. Returns Dunkin's national menu: item names, descriptions and photos grouped into categories (Iced Drinks, Hot Drinks, Frozen Drinks, Sandwiches & Wraps, Savory Bites, Donuts & Bakery, Snacks and Sides). Dunkin publishes one shared menu across every US store, so this takes no store parameter. Does not carry prices or nutrition -- pricing varies by market/franchisee and isn't part of this content.
- **Params:** _none_

### `dunkin_nearby`

- **HTTP:** `GET /dunkin/nearby`
- **What:** Find Dunkin stores near a coordinate, nearest first. Returns Dunkin restaurants within a radius of a latitude/longitude, ordered nearest first, each with its distance in miles and kilometres, full address, phone, coordinates, the published week of hours, whether it's permanently closed, amenities, payment methods, pickup/delivery service types, which third-party delivery platforms are active, its Google Place id, timezone, and website/menu/order URLs. This is the proximity search the directory browse cannot do -- GET /dunkin/directory walks a state to city to store tree, which requires knowing the administrative path in advance. Each result carries the store id as `path`, which GET /dunkin/store also takes, so the two chain directly. `total_in_radius` reports how many stores fall inside the radius overall, which is usually far more than one page; use `offset` to walk it. A coordinate with no Dunkin nearby returns an empty list rather than an error.
- **Params:** `latitude` (number, **required**) — Search center latitude; `limit` (integer, optional) — Maximum stores to return, 1-50 (default 10); `longitude` (number, **required**) — Search center longitude; `offset` (integer, optional) — Result offset for paging through total_in_radius (default 0); `radius` (integer, optional) — Search radius in miles, 1-100 (default 25)

### `dunkin_store`

- **HTTP:** `GET /dunkin/store`
- **What:** Get one Dunkin store's detail. Returns one Dunkin store: name, full postal address, phone, coordinates, opening hours for every day of the week, whether it's permanently closed, amenities (curbside pickup, drive-thru, wifi, kosher, turbo oven, K-Cup pods), Dunkin's own free-text feature labels, accepted payment methods, pickup/delivery service types, which third-party delivery platforms are active, the Google Place id, and the store's website/menu/order URLs. path is a store id -- from a /dunkin/directory child with is_store true, a /dunkin/nearby result's path, or the trailing digits of a dunkindonuts.com store URL. An unknown id returns a 404.
- **Params:** `path` (string, **required**) — A Dunkin store id, from a /dunkin/directory child with is_store true, a /dunkin/nearby result's path, or the trailing digits of a dunkindonuts.com store URL

## FiveGuys (10)

### `fiveguys_directory`

- **HTTP:** `GET /fiveguys/directory`
- **What:** Browse the Five Guys restaurant directory by state and city. Returns one level of Five Guys' US restaurant directory: the 50 states at the root, one state's cities when path is a state (e.g. `il`), and that city's restaurants when path is a city (e.g. `il/chicago`). Each child carries the path to pass back as this endpoint's `path`, and a `location_count` of how many restaurants sit under it. At the deepest level children are restaurants themselves (`is_location` true) -- pass their path to GET /fiveguys/store for the full profile. Use this to enumerate or browse locations; use GET /fiveguys/search or /fiveguys/nearby to find them by query or coordinate instead.
- **Params:** `path` (string, optional) — Optional. Directory path from a previous response's children[].path, e.g. \

### `fiveguys_faq`

- **HTTP:** `GET /fiveguys/faq`
- **What:** List Five Guys' published customer FAQ. Returns one page of Five Guys' published customer FAQ corpus -- 142 entries across 17 categories (Menu, Nutritional and Allergens, Ordering, Gift Card, Careers, Franchise, App, Company, The Crew, and others), filterable by category id and free text, in English (default) or Spanish via `lang`. Get valid category values from GET /fiveguys/faq-categories using the same `lang` -- category ids are language-specific.
- **Params:** `category` (string, optional) — Optional. Comma-separated faq_category term ids, from GET /fiveguys/faq-categories.; `lang` (string, optional) — Optional. Content language: en (default) or es.; `page` (integer, optional) — Optional. 1-based page number, default 1.; `per_page` (integer, optional) — Optional. Entries per page, 1-100, default 20.; `search` (string, optional) — Optional. Free-text filter over question and answer text.

### `fiveguys_faq_categories`

- **HTTP:** `GET /fiveguys/faq-categories`
- **What:** List Five Guys FAQ categories. Returns every published Five Guys FAQ category with its id, name, slug, and entry count -- use an id here as GET /fiveguys/faq's category filter. Available in English (default) and Spanish via `lang`; ids differ between languages, so pass the same `lang` to both endpoints.
- **Params:** `lang` (string, optional) — Optional. Content language: en (default) or es. Category ids differ per language -- feed ids from a given language back into GET /fiveguys/faq with the same lang.

### `fiveguys_menu`

- **HTTP:** `GET /fiveguys/menu`
- **What:** List Five Guys menu categories and items. Returns Five Guys' public menu content: every category (Burgers, Fries, Shakes, Hot Dogs, Sandwiches, Drinks, Toppings) -- each with its own short description and cover image, plus its items' name, description, calories, and image -- or one category's items when category is given. Five Guys publishes no per-item price on this surface -- pricing is store-scoped and lives only behind its ordering flow, which this endpoint does not cover. Available in English (default) and Spanish via `lang`. Calories are shown exactly as published: a single value for most items, or a range (e.g. fries' "530-1100") for build-your-own items whose calories vary by size and toppings. Some items (drink categories, a few build-your-own items) publish no calorie figure at all; their calories field is omitted rather than estimated.
- **Params:** `category` (string, optional) — Optional. One category slug to return only that category's items. Omit to return the full menu across every category. With lang=en (the default) one of: burgers, fries, shakes, dogs, sandwiches, drinks, toppings. With lang=es the slugs differ -- read them from a lang=es response's categories[].slug.; `lang` (string, optional) — Optional. Content language: en (default) or es.

### `fiveguys_nearby`

- **HTTP:** `GET /fiveguys/nearby`
- **What:** Find Five Guys restaurants near a coordinate. Returns Five Guys restaurants within a radius of a latitude/longitude. Each result carries a full profile: a short area/plaza label distinguishing it from other locations, address, phone, weekly in-store hours plus a separate delivery-hours schedule when published, price tier, restaurant-amenity labels (e.g. Takeout, Dine In, Curbside), pickup/delivery service labels, order/delivery/menu URLs, a Google Place id, and distance in miles/kilometers from the given coordinate. `total_results` reports how many restaurants fall inside the radius overall, usually more than one page; use `offset` to page. A coordinate with no Five Guys nearby returns an empty list rather than an error.
- **Params:** `latitude` (number, **required**) — Search center latitude; `limit` (integer, optional) — Maximum restaurants to return, 1-50 (default 10); `longitude` (number, **required**) — Search center longitude; `offset` (integer, optional) — Result offset for paging through total_results (default 0); `radius` (integer, optional) — Search radius in miles, 1-100 (default 25)

### `fiveguys_nutrition`

- **HTTP:** `GET /fiveguys/nutrition`
- **What:** Get the current Five Guys nutrition & allergen PDF guide's location. Resolves the live location of Five Guys' current dated nutrition & allergen guide PDF (calories, full macro nutrition and allergen data per item) directly from fiveguys.com -- the guide's own file path changes when Five Guys republishes it (observed monthly), so this endpoint always discovers the current link rather than returning a fixed one. Returns the PDF's direct download URL plus best-effort size and last-modified metadata read from the PDF's own response headers. This endpoint returns metadata and a link to the guide, not its table parsed into structured fields -- pair it with GET /fiveguys/menu for structured per-item calories.
- **Params:** _none_

### `fiveguys_ordering_locations`

- **HTTP:** `GET /fiveguys/ordering-locations`
- **What:** Find Five Guys restaurants near a coordinate with ordering details. Returns Five Guys restaurants near a latitude/longitude as Five Guys' own ordering platform publishes them, with commerce detail no other endpoint in this family carries: per-store delivery fee, delivery and pickup order minimums, whether the store is currently accepting orders at all, the handoff modes an order placed now could actually use (delivery, pickup, curbside, dine-in, drive-thru, dispatch), group-order/coupon/loyalty support, how many days ahead an order may be scheduled, and the store's own order URL. Set `include_hours` to also return each store's dated business and delivery calendars -- concrete dated windows rather than the recurring weekly schedule the locator endpoints publish, so they reflect holiday and special hours a weekly schedule cannot express. This is a different upstream from GET /fiveguys/nearby, which returns the marketing/locator record: the two describe the same restaurants but do not share ids, and this one carries a per-store name ("Five Guys Austin Arbor") where the locator publishes the generic brand name. Use each result's `id` with GET /fiveguys/ordering-menu for that store's priced menu. A coordinate with no Five Guys nearby returns an empty list rather than an error.
- **Params:** `days` (integer, optional) — Days of calendar to return from today, 1-30 (default 7). Only meaningful with include_hours.; `include_hours` (boolean, optional) — Include each store's dated business and delivery calendars; `latitude` (number, **required**) — Search center latitude; `limit` (integer, optional) — Maximum restaurants to return, 1-50 (default 10); `longitude` (number, **required**) — Search center longitude; `radius` (integer, optional) — Search radius in miles, 1-50 (default 20)

### `fiveguys_ordering_menu`

- **HTTP:** `GET /fiveguys/ordering-menu`
- **What:** Get one Five Guys store's priced menu from the ordering platform. Returns one restaurant's full menu exactly as Five Guys' own ordering platform sells it, including real per-item prices -- the one field no other endpoint in this family can surface (GET /fiveguys/menu is fiveguys.com's own marketing content and carries no price at all). Categories and items are returned with name, description, price, calories (a single value or a real range, e.g. a fountain drink sized at checkout), an image, and whether the platform currently has the item available. id is the ordering platform's own restaurant id from GET /fiveguys/ordering-locations' locations[].id -- it is not a Yext entity id and does not correspond to any id from GET /fiveguys/search, /fiveguys/nearby, /fiveguys/directory, or /fiveguys/store.
- **Params:** `id` (string, **required**) — The ordering platform's restaurant id, from GET /fiveguys/ordering-locations' locations[].id

### `fiveguys_search`

- **HTTP:** `GET /fiveguys/search`
- **What:** Search Five Guys restaurants by free-text location. Returns Five Guys restaurants matching a free-text location query -- a city, a zip/postal code, a street address, or a landmark -- the same way restaurants.fiveguys.com's own locator search box works. Yext's own query understanding geocodes the text server-side, so no separate geocoding call is needed. Each result carries a full profile: a short area/plaza label distinguishing it from other locations, address, phone, weekly in-store hours plus a separate delivery-hours schedule when published, price tier, restaurant-amenity labels (e.g. Takeout, Dine In, Curbside), pickup/delivery service labels, order/delivery/menu URLs, a Google Place id, and distance in miles/kilometers from the resolved query location. `total_results` reports how many restaurants matched overall, usually more than one page; use `offset` to page. A query that resolves to nowhere Five Guys operates returns an empty list rather than an error.
- **Params:** `limit` (integer, optional) — Maximum restaurants to return, 1-50 (default 10); `offset` (integer, optional) — Result offset for paging through total_results (default 0); `query` (string, **required**) — Free-text location: a city, a zip/postal code, a street address, or a landmark

### `fiveguys_store`

- **HTTP:** `GET /fiveguys/store`
- **What:** Get one Five Guys restaurant by its locator path. Returns one Five Guys restaurant's full published profile by its locator slug -- address, phone, weekly in-store hours, separate delivery hours, coordinate, Google Place id, restaurant-amenity labels, and order/delivery/menu URLs. Get a path from GET /fiveguys/search or /fiveguys/nearby's `locations[].path`, or from GET /fiveguys/directory's `children[].path` where `is_location` is true. It also returns three detail-only extras that search and nearby results do not carry: `description` (this restaurant's own blurb, templated but genuinely per-location), `photos` (its published gallery images, omitted for the many locations that publish none), and `breadcrumbs` (the directory trail above it, each entry's `path` feeding straight back into GET /fiveguys/directory). Two fields available on search and nearby results are not published on this surface and are omitted here: `price_range` and `pickup_and_delivery_services`. A `profile` block, populated best-effort from a second Yext key, adds further per-restaurant detail no other field in this family carries: `google_attributes` (structured amenity flags, richer than `services`), `review_page_url`/`review_invite_url`, `featured_message`/`featured_message_url`, `google_cid`/`facebook_store_id`, `routable_latitude`/`routable_longitude` (a driving destination, distinct from the display coordinate), `payment_options`, `meals_served`, `services`, `permanently_closed`, `directory_listing_url`, `franchisee_group` (the operator of this specific restaurant -- a corporate code or a franchisee's own company name), `facebook_vanity_url` (this location's own Facebook handle), and `faq` (this restaurant's own generated question set, distinct from the national corpus GET /fiveguys/faq serves). Passing a state or city path returns 404 -- use GET /fiveguys/directory for those.
- **Params:** `id` (string, optional) — The restaurant's entity id, e.g. \; `path` (string, optional) — The restaurant's locator slug, e.g. \

## Foodpanda (5)

### `foodpanda_restaurant`

- **HTTP:** `GET /foodpanda/restaurant`
- **What:** Get one foodpanda restaurant's detail. Returns one foodpanda restaurant's detail by code: name, address, coordinates, budget tier, rating and review count, cuisines, minimum order amount, minimum delivery fee, delivery/pickup availability, timezone, and a hero image. Supplying latitude and longitude only affects the (optional) computed fields the upstream itself returns for that coordinate; it does not filter or reject the lookup.
- **Params:** `code` (string, **required**) — Restaurant code, from /foodpanda/search's code field; `latitude` (number, optional) — Caller latitude, optional; `longitude` (number, optional) — Caller longitude, optional; `market` (string, optional) — Delivery Hero market the restaurant belongs to. Defaults to sg.

### `foodpanda_restaurant_menu`

- **HTTP:** `GET /foodpanda/restaurant/menu`
- **What:** Get one foodpanda restaurant's menu with prices. Returns one restaurant's full menu grouped into categories, plus opening hours, price range, cuisines served, and aggregate rating. Every item carries a title, description, image, sold-out flag, and price -- original_price plus discounted_price when the item is currently discounted.
- **Params:** `code` (string, **required**) — Restaurant code, from /foodpanda/search's code field; `market` (string, optional) — Delivery Hero market the restaurant belongs to. Defaults to sg.

### `foodpanda_restaurant_reviews`

- **HTTP:** `GET /foodpanda/restaurant/reviews`
- **What:** Get a sample of one foodpanda restaurant's customer reviews. Returns a sample of real customer reviews for one restaurant -- author name, publish date, review text, and a 1-5 rating. This is the curated sample the restaurant's own storefront page embeds for search-engine rich results, not the full review corpus a logged-in customer would see in the app; the number returned scales with the restaurant's popularity rather than being a fixed cap, and can be empty for a restaurant with few or no reviews.
- **Params:** `code` (string, **required**) — Restaurant code, from /foodpanda/search's code field; `market` (string, optional) — Delivery Hero market the restaurant belongs to. Defaults to sg.

### `foodpanda_search`

- **HTTP:** `GET /foodpanda/search`
- **What:** Search foodpanda restaurants near a location. Returns restaurants delivering to a latitude/longitude in a foodpanda market, optionally filtered by a numeric cuisine id (call foodpanda_search_cuisines for the live, location-scoped set of valid ids). Each restaurant carries its code (the value the restaurant and menu endpoints take), name, address, coordinates, budget tier, rating, cuisines, minimum order amount and delivery fee, delivery/pickup availability, and a hero image. A location with no coverage returns an empty list rather than an error.
- **Params:** `cuisine_id` (integer, optional) — Numeric cuisine id to filter by. Cuisine ids are location- and market-scoped, not a fixed global enum -- call foodpanda_search_cuisines with the same market/latitude/longitude to get the valid id set for this location; `latitude` (number, **required**) — Search center latitude; `limit` (integer, optional) — Restaurants to return, clamped to 50 (default 20); `longitude` (number, **required**) — Search center longitude; `market` (string, optional) — Delivery Hero market. Defaults to sg.; `offset` (integer, optional) — Result offset for pagination (default 0)

### `foodpanda_search_cuisines`

- **HTTP:** `GET /foodpanda/search/cuisines`
- **What:** Get foodpanda's live cuisine filter catalog for a location. Returns foodpanda's own live cuisine catalog for a latitude/longitude in a foodpanda market -- the exact facet list (with real, live restaurant counts) the site's own search page cuisine filter sidebar is populated from. Every entry's id is a valid value for /foodpanda/search's cuisine_id parameter. Cuisine ids are location- and market-scoped, not a fixed global enum: the same coordinate in a different neighborhood, or a different market, can return a different id/count set entirely, so call this endpoint with the same market/latitude/longitude you intend to search rather than reusing ids captured elsewhere.
- **Params:** `latitude` (number, **required**) — Search center latitude; `longitude` (number, **required**) — Search center longitude; `market` (string, optional) — Delivery Hero market. Defaults to sg.

## Grubhub (7)

### `grubhub_availability`

- **HTTP:** `GET /grubhub/availability`
- **What:** Check ordering availability for a batch of Grubhub restaurants. Returns current ordering state for up to 20 restaurants in one call, relative to a diner location. Each entry reports whether the restaurant is open overall and per channel (these can differ), whether delivery and pickup are offered at all as distinct from open right now, whether it delivers to the supplied coordinate, blackout and overloaded flags, distance, delivery and pickup time estimates, delivery fee, order minimum, cuisines, and the next time an order can be sent per channel -- useful when a restaurant is currently closed. The response echoes the requested ids so a caller can tell which ones Grubhub returned nothing for.
- **Params:** `latitude` (number, **required**) — Diner location latitude -- availability is relative to it; `longitude` (number, **required**) — Diner location longitude; `restaurant_ids` (string, **required**) — Comma-separated Grubhub restaurant ids, up to 20

### `grubhub_offers`

- **HTTP:** `GET /grubhub/offers`
- **What:** Get one Grubhub restaurant's currently active promotions. Returns the promotional offers a Grubhub restaurant is currently running -- free items, BOGO deals, spend-and-save discounts -- the same data that drives the "2 offers available" badge on the site's own restaurant cards. An empty list is the common, legitimate case: most restaurants have no active promotion at any given moment. `amount.value` is 0 for a free-item offer since the item itself is the value, not a monetary discount; `amount.amount_maximum` then caps the item's dollar value, and `amount.order_minimum` is the spend threshold required to unlock it.
- **Params:** `latitude` (number, **required**) — Diner location latitude; `longitude` (number, **required**) — Diner location longitude; `restaurant_id` (string, **required**) — Grubhub restaurant id

### `grubhub_restaurant`

- **HTTP:** `GET /grubhub/restaurant`
- **What:** Get one Grubhub restaurant's detail. Returns one Grubhub restaurant: name, address with coordinates, timezone, phone, cuisines, star rating, price tier, whether online ordering is available, whether it offers delivery and pickup, delivery fee, coupon availability, restaurant tags and the full published week of service hours. Note this endpoint publishes fewer economics than GET /grubhub/search -- delivery minimum and the delivery/pickup time estimates come back empty here, so use the search endpoint when you need those.
- **Params:** `restaurant_id` (string, **required**) — Grubhub's numeric restaurant id, from /grubhub/search

### `grubhub_restaurant_menu`

- **HTTP:** `GET /grubhub/restaurant/menu`
- **What:** Get one Grubhub restaurant's menu with prices. Returns one restaurant's full menu grouped into categories. Every item carries a base price, a delivery price and a pickup price, which genuinely differ, plus a min and max price bounding items whose price varies with the options chosen. Items also carry a description, a popularity flag, availability, tags and an image. Amounts are given both in minor units (cents) and as a decimal value.
- **Params:** `include_unavailable` (boolean, optional) — Include items the restaurant currently has unavailable (default false); `restaurant_id` (string, **required**) — Grubhub's numeric restaurant id, from /grubhub/search

### `grubhub_restaurant_reviews`

- **HTTP:** `GET /grubhub/restaurant/reviews`
- **What:** Get one Grubhub restaurant's reviews and rating histogram. Returns one restaurant's customer reviews plus its 1-5 star rating histogram. Each review carries the star rating, the written body, the reviewer's display name and how many reviews they have written, the review date, Grubhub's own sentiment classification, the diner type, and the specific menu items the review is attached to -- Grubhub ties each review to what the diner actually ordered. sort accepts `timeCreated_desc` (most recent, the default) and `ratingValue_desc` (highest rated). Note the written-review corpus and the headline rating shown in search are separate systems upstream, so a restaurant can report a large rating count in search while returning few or no written reviews here.
- **Params:** `page` (integer, optional) — 1-based page number (default 1); `page_size` (integer, optional) — Reviews per page, 1-50 (default 20); `restaurant_id` (string, **required**) — Grubhub's numeric restaurant id, from /grubhub/search; `sort` (string, optional) — One of timeCreated_desc, ratingValue_desc. Default timeCreated_desc.

### `grubhub_search`

- **HTTP:** `GET /grubhub/search`
- **What:** Search Grubhub restaurants near a location. Returns restaurants delivering to (or offering pickup at) a latitude/longitude, optionally filtered by keyword over restaurant names, cuisines and dishes. Each restaurant carries its id (the value every other Grubhub endpoint takes), name, full address with coordinates, phone, cuisines, star rating and rating count, Grubhub's 1-4 price tier, distance, open state, delivery and pickup fees and minimums, service fee, delivery and pickup time estimates, coupon availability and total menu item count. A location Grubhub does not serve returns an empty list rather than an error.
- **Params:** `latitude` (number, **required**) — Search center latitude; `longitude` (number, **required**) — Search center longitude; `order_method` (string, optional) — One of delivery, pickup. Default delivery.; `page` (integer, optional) — 1-based page number (default 1); `page_size` (integer, optional) — Restaurants per page, 1-50 (default 20); `search` (string, optional) — Keyword over restaurant names, cuisines and dishes

### `grubhub_timepicker`

- **HTTP:** `GET /grubhub/timepicker`
- **What:** Get one Grubhub restaurant's future orderable time-slot calendar. Returns every future delivery or pickup time slot Grubhub will accept an order for, up to 7 days ahead. This is what powers the site's own "schedule my order" picker: `/grubhub/availability` tells you whether a restaurant is orderable right now plus one "next" time, while this returns the full future slot calendar a caller would need to build an actual date-and-time picker. Slots are grouped by date and given as full timestamps carrying the restaurant's real UTC offset for that instant, so a caller never has to resolve daylight-saving transitions themselves. Requesting `location_mode=DELIVERY` returns delivery slots only; `PICKUP` returns pickup slots only -- the upstream only computes one side per call.
- **Params:** `days` (integer, optional) — How many days ahead to fetch, 1-7 (default 7); `latitude` (number, **required**) — Diner location latitude; `location_mode` (string, **required**) — Which slot grid to return; `longitude` (number, **required**) — Diner location longitude; `restaurant_id` (string, **required**) — Grubhub restaurant id

## JimmyJohns (5)

### `jimmy_johns_menu`

- **HTTP:** `GET /jimmy-johns/menu`
- **What:** Get one Jimmy John's restaurant's full menu. Returns one Jimmy John's restaurant's full menu as a category tree: every category and its products, with name, description, calorie range, base cost and image. restaurant_id comes from GET /jimmy-johns/nearby. Many sandwiches price entirely through a size selection rather than a base cost, so cost is commonly 0 for those items -- see GET /jimmy-johns/modifiers for the real per-size price.
- **Params:** `restaurant_id` (integer, **required**) — Olo restaurant id from /jimmy-johns/nearby

### `jimmy_johns_modifiers`

- **HTTP:** `GET /jimmy-johns/modifiers`
- **What:** Get one Jimmy John's menu product's customization options. Returns one menu product's full customization tree: size, bread, and per-ingredient choices (extra/regular/light/none), each with its real price and calorie delta. Groups nest -- picking a size choice can reveal a bread group, which can reveal one group per ingredient -- so a size step, a bread step, and every "Customize Sandwich" ingredient all live in one recursive tree. product_id comes from GET /jimmy-johns/menu.
- **Params:** `product_id` (integer, **required**) — Product id from a /jimmy-johns/menu product

### `jimmy_johns_nearby`

- **HTTP:** `GET /jimmy-johns/nearby`
- **What:** Find Jimmy John's restaurants near a coordinate. Returns Jimmy John's restaurants within a radius of a coordinate, nearest first, using Jimmy John's own Olo-backed ordering API (a separate host from the locator this family's sitemap and store endpoints read). Each result carries restaurant_id -- pass it to GET /jimmy-johns/menu for that restaurant's full menu. The upstream's own radius parameter does not narrow its result set, so distance filtering and sorting happen here.
- **Params:** `latitude` (number, **required**) — Search center latitude; `limit` (integer, optional) — Maximum restaurants to return, 1-50 (default 10); `longitude` (number, **required**) — Search center longitude; `radius` (integer, optional) — Search radius in miles, 1-100 (default 15)

### `jimmy_johns_sitemap`

- **HTTP:** `GET /jimmy-johns/sitemap`
- **What:** Browse Jimmy John's store-URL index. Returns one page of Jimmy John's sitemap-declared store index -- 9,700+ URLs at time of writing. Jimmy John's publishes three page variants per store (sandwiches, delivery, catering) and all three appear in the sitemap, so each entry carries a kind and the store number they share; filter with the kind parameter to enumerate one variant per restaurant. `sandwiches` is the canonical variant. A page past the end returns an empty list rather than an error, so a caller can walk to exhaustion.
- **Params:** `kind` (string, optional) — Filter by page variant. One of sandwiches, delivery, catering. Default all.; `page` (integer, optional) — 1-based page within the shard (default 1); `page_size` (integer, optional) — Entries per page, 1-500 (default 100); `shard` (integer, optional) — Sitemap shard index (default 0)

### `jimmy_johns_store`

- **HTTP:** `GET /jimmy-johns/store`
- **What:** Get one Jimmy John's store's detail. Returns one Jimmy John's store: name, postal address, phone, coordinates, cuisine description and the published week of opening hours. Store paths come from GET /jimmy-johns/sitemap. Note Jimmy John's main site is behind a bot challenge that serves a page with HTTP 200, so this family reads the separate locator subdomain instead. For menu data, see GET /jimmy-johns/nearby and GET /jimmy-johns/menu, which read a separate ordering API.
- **Params:** `path` (string, **required**) — Store path from a /jimmy-johns/sitemap entry

## Just Eat (4)

### `justeat_restaurant`

- **HTTP:** `GET /justeat/restaurant`
- **What:** Get one Just Eat restaurant's detail. Returns one Just Eat restaurant by `unique_name`, the slug found in a search result. The response has the restaurant id, name, address, city, postal code, country, image, primary cuisine, rating and rating count, and `is_active`, which says whether it currently accepts orders. `rating` can read `0` even when the site shows one. An unknown `unique_name` returns `404`.
- **Params:** `unique_name` (string, **required**) — Restaurant slug, from a search response's unique_name field

### `justeat_restaurant_menu`

- **HTTP:** `GET /justeat/restaurant/menu`
- **What:** Get one Just Eat restaurant's menu with prices. Returns one restaurant's full menu grouped into categories. Every item carries a name, description, image, price, and calorie/energy text when the upstream provides it. Items with customization options (e.g. "Dip 1/2") carry a modifier_groups list with each option's own price. Non-restaurant stores (groceries, alcohol, pharmacy, electronics, and similar) return every item under a single "All items" category rather than the site's own finer-grained grouping.
- **Params:** `unique_name` (string, **required**) — Restaurant slug, from a search response's unique_name field

### `justeat_search`

- **HTTP:** `GET /justeat/search`
- **What:** Search Just Eat restaurants near a UK postcode. Returns Just Eat's full restaurant listing for a UK postcode -- every restaurant the site's own area page carries, ordered as Just Eat's default "best match" sort presents them (or by sort_by, if set), not a curated subset. Each restaurant carries its unique_name (the value the restaurant and menu endpoints take), name, image, rating, delivery time window, and open-now status. A postcode with no coverage returns an empty list rather than an error.
- **Params:** `filter` (array, optional) — Repeatable. Just Eat's own area-page filter slugs (e.g. open_now, or a cuisine tile's slug), passed through as-is and OR'd together. Also reaches non-restaurant categories -- groceries, alcohol, pharmacy, electronics, and more -- via the same mechanism, e.g. filter=groceries. The valid slug set is specific to the postcode you are searching -- call /justeat/search/filters with the same postcode for the current, complete, location-scoped list with live result counts. An unrecognized slug narrows to a smaller or empty result rather than erroring.; `limit` (integer, optional) — Restaurants to return, clamped to 100 (default 20); `postcode` (string, **required**) — UK postcode to search near; `sort_by` (string, optional) — Result order, matching the area page's own Sort by control. Default best_match.

### `justeat_search_filters`

- **HTTP:** `GET /justeat/search/filters`
- **What:** Get Just Eat's live filter slug catalog for a UK postcode. Returns the exact filter slugs Just Eat's own area page currently offers for a UK postcode -- star-rating thresholds, boolean toggles (open_now, new, free_delivery, halal, vegan, ...), cuisine tiles (pizza, chinese, italian, ...), and non-restaurant top-nav verticals (groceries, alcohol, pharmacy, electronics, flowers, gifts, and more) alike -- each with the live count of restaurants it currently narrows this postcode's listing to. Every filter value is the literal string /justeat/search's repeatable filter parameter accepts. The slug set is genuinely postcode-dependent: a rural postcode's own area page offers fewer cuisine tiles than central London's, because Just Eat's own frontend never advertises a filter with zero local coverage -- call this endpoint again for a different postcode rather than assume one location's slug set applies everywhere.
- **Params:** `postcode` (string, **required**) — UK postcode to look up

## KFC (7)

### `kfc_delivery_estimate`

- **HTTP:** `GET /kfc/delivery-estimate`
- **What:** Check KFC delivery serviceability and estimated fee for one store and address. Checks whether a KFC restaurant's delivery integration can deliver to a given address and, when it can, the estimated delivery fee (broken down by fee line item) and pickup/dropoff time. This reads the same checkout-time estimate KFC's own site calls -- it does not add an item to a cart or place an order, and takes no payment or account information. serviceable is true only when the upstream returned a real estimate; a false value with reason populated covers every other case seen live: the delivery provider not enabled at this store, the address being outside the delivery zone, or the delivery marketplace itself reporting the store temporarily inactive. order_subtotal materially affects the fee estimate (KFC's own fee schedules can vary by order size), so it is required rather than defaulted. pickup_at defaults to 30 minutes from now (an "order now" style estimate) when omitted.
- **Params:** `address1` (string, **required**) — Delivery address line 1; `address2` (string, optional) — Delivery address line 2; `city` (string, **required**) — Delivery address city; `country_code` (string, optional) — Delivery address country code (default US); `delivery_provider` (string, optional) — Delivery provider to check (default DOORDASH); `latitude` (number, **required**) — Delivery address latitude; `longitude` (number, **required**) — Delivery address longitude; `order_subtotal` (number, **required**) — Order subtotal before fees, in dollars; `pickup_at` (string, optional) — RFC3339 pickup time (default 30 minutes from now); `postal_code` (string, **required**) — Delivery address postal code; `state` (string, **required**) — Delivery address state, two-letter code; `store_number` (string, **required**) — KFC's alphanumeric store number, from /kfc/stores or /kfc/nearby

### `kfc_menu`

- **HTTP:** `GET /kfc/menu`
- **What:** Get one KFC restaurant's full priced menu. Returns one restaurant's full menu grouped into categories (e.g. "Deals", "Combos", "Tenders"). Every entry is a product, a bundle (a combo or family meal), or a standalone priced variant -- type tells callers which -- and carries a price in USD cents plus a decimal dollar value, and an image when the upstream publishes one. Prices reflect this specific restaurant and order channel, not a national default. channel selects which order channel the menu is priced for (web ordering by default); prices can genuinely differ by channel (e.g. a delivery-marketplace channel vs. web).
- **Params:** `channel` (string, optional) — Order channel the menu is priced for (default WEB); `store_number` (string, **required**) — KFC's alphanumeric store number, from /kfc/stores or /kfc/nearby

### `kfc_nearby`

- **HTTP:** `GET /kfc/nearby`
- **What:** Find KFC restaurants near a location. Returns KFC restaurants near a latitude/longitude, nearest first. A coordinate with no nearby KFC returns an empty list rather than an error. Each restaurant carries its store number, full address with coordinates, phone, whether it currently accepts online orders, its timezone, and its distance from the search point in miles. occasion restricts results to restaurants that offer a given order channel (e.g. only drive-thru locations).
- **Params:** `latitude` (number, **required**) — Search center latitude; `longitude` (number, **required**) — Search center longitude; `max_results` (integer, optional) — Maximum restaurants to return, 1-50 (default 20); `occasion` (string, optional) — Restrict to restaurants offering this order channel; `radius_miles` (number, optional) — Search radius in miles, 0.1-100 (default 10)

### `kfc_promotion`

- **HTTP:** `GET /kfc/promotion`
- **What:** Look up one KFC promotion by its redemption code or serialized code. Returns one promotion by its redemption code (the code a customer types in at checkout) or its serialized code (a unique per-print QR/serial code, e.g. from a printed coupon, that resolves to a shared redemption code and its promotion). Exactly one of code or serialized_code is required. A serialized-code lookup additionally returns that code's own usage metadata (redemption_code, times_used, code_status, group_status, effective_date, expiration_date) alongside the promotion. An unknown or expired code returns a 404 rather than a null success payload.
- **Params:** `code` (string, optional) — The redemption code as a customer would type it in at checkout. Use a value returned by kfc-promotions when available. Exactly one of code or serialized_code is required; `serialized_code` (string, optional) — A unique per-print serialized/QR code that resolves to a shared redemption code. Exactly one of code or serialized_code is required

### `kfc_promotions`

- **HTTP:** `GET /kfc/promotions`
- **What:** Get one KFC restaurant's current public promotions. Returns one restaurant's current public promotions -- current deals and offers KFC's storefront marks as public, with each promotion's id, internal and display name, description, whether it applies automatically, and active redemption codes when KFC exposes them. The returned codes can be passed to kfc-promotion. A store with no active public promotions returns an empty list rather than an error.
- **Params:** `store_number` (string, **required**) — KFC's alphanumeric store number, from /kfc/stores or /kfc/nearby

### `kfc_store`

- **HTTP:** `GET /kfc/store`
- **What:** Get one KFC restaurant by its store number. Returns one KFC restaurant's detail by its exact store number, from /kfc/stores or /kfc/nearby, including its recurring open hours per order channel (carryout, delivery, dine-in, drive-thru, catering carryout). A channel this restaurant does not offer at all is omitted from hours rather than reported as always-closed.
- **Params:** `store_number` (string, **required**) — KFC's alphanumeric store number, from /kfc/stores or /kfc/nearby

### `kfc_stores`

- **HTTP:** `GET /kfc/stores`
- **What:** Search KFC restaurants by city, state, postal code, name, franchise code, or store number. Returns KFC restaurants matching a city/state/postal code/name/franchise code/store number filter. At least one filter is required -- an unfiltered call would enumerate every US restaurant in one response, which this endpoint intentionally does not expose. Each restaurant carries its store number (the value /kfc/menu and /kfc/promotions take), full address with coordinates, phone, whether it currently accepts online orders, and its timezone. appear_in_store_results (default true) excludes internal/test records KFC's own storefront does not surface in customer-facing search -- a raw filter can otherwise return non-orderable administrative entries alongside real restaurants.
- **Params:** `appear_in_store_results` (boolean, optional) — Restrict to restaurants shown in customer-facing search, excluding internal/test entries (default true); `city` (string, optional) — Restaurant city; `franchise_code` (string, optional) — Exact franchise/operator code; `max_results` (integer, optional) — Maximum restaurants to return, 1-50 (default 20); `name` (string, optional) — Restaurant name, partial match; `postal_code` (string, optional) — Restaurant postal code; `sort` (string, optional) — Sort order; `state` (string, optional) — Restaurant state, two-letter code; `store_number` (string, optional) — Exact store number

## Kroger (10)

### `kroger_categories`

- **HTTP:** `GET /kroger/categories`
- **What:** Get Kroger's product-browse category taxonomy. Returns Kroger's full product-browse category taxonomy: every slug/category_id pair kroger-search and kroger-category accept, each with its department and full breadcrumb. This is how to discover valid slug/category_id values -- previously the only way was to already have one from a search response's facet group. Sourced from Kroger's own site navigation menu; covers every category a shopper can browse to from Kroger's site menu (321 at time of writing across 7 departments). Takes no parameters.
- **Params:** _none_

### `kroger_category`

- **HTTP:** `GET /kroger/category`
- **What:** Browse a Kroger category. Browses a Kroger product category and returns product cards plus facet groups, in the same shape as kroger-search. slug and category_id together identify the category (e.g. "pet" and "27" for kroger.com/pl/pet/27) -- call kroger-categories to discover every valid slug/category_id pair. It uses category_id as a taxonomy filter, with real pagination, and the source field reports which path answered. Facet filters and sort apply to the primary path only: when any of them is set, a failure of that path returns an error rather than silently falling back to unfiltered results.
- **Params:** `brands` (string, optional) — Comma-separated brand names to filter by, taken verbatim from a previous response's facets; `category_id` (string, **required**) — Category numeric taxonomy id. Obtain valid slug/category_id pairs from kroger-categories; `flavor` (string, optional) — Comma-separated flavor facet values; `more_options` (string, optional) — Comma-separated more-options facet values; `nutrition` (string, optional) — Comma-separated nutrition/dietary facet values; `page` (integer, optional) — One-based result page; `price_max` (number, optional) — Upper bound of the price filter; required to filter on price; `price_min` (number, optional) — Lower bound of the price filter; defaults to 0; `savings` (string, optional) — Comma-separated savings facet values; `scent` (string, optional) — Comma-separated scent facet values; `slug` (string, **required**) — Category URL slug segment. Obtain valid slug/category_id pairs from kroger-categories; `sort` (string, optional) — Result order. One of: relevance, name_asc, popularity_desc

### `kroger_coupons`

- **HTTP:** `GET /kroger/coupons`
- **What:** Get Kroger digital coupons. Returns a page of Kroger's public digital coupons: savings value, requirement text and quantity, brand, categories, redemption modalities, promotional tags, image, and start/end/expiry dates. Optionally narrow to one product (upc) or brand. This is the anonymous public coupon catalog -- per-account clipping state is not returned.
- **Params:** `brand` (string, optional) — Narrow to one brand's coupons; `location_id` (string, optional) — Kroger store/location id that scopes coupons; `page` (integer, optional) — One-based result page; `page_size` (integer, optional) — Coupons per page, 1-200; `upc` (string, optional) — Narrow to coupons applying to one Kroger product

### `kroger_product`

- **HTTP:** `GET /kroger/product`
- **What:** Get a Kroger product. Returns product detail for one Kroger item: title, description, image, brand, category trail, price/availability, and rating.
- **Params:** `upc` (string, **required**) — Kroger product UPC/id (the last path segment of the product page URL)

### `kroger_product_reviews`

- **HTTP:** `GET /kroger/product/reviews`
- **What:** Get a Kroger product's customer reviews. Returns one page of a Kroger product's customer reviews -- review text, star rating, recommendation flag, helpful-vote counts, and customer photo URLs -- alongside the product's full star histogram. Customer display names are deliberately not returned.
- **Params:** `page` (integer, optional) — One-based review page; `page_size` (integer, optional) — Reviews per page, 1-100; `upc` (string, **required**) — Kroger product UPC/id

### `kroger_products`

- **HTTP:** `GET /kroger/products`
- **What:** Get full Kroger product detail in bulk. Returns full detail for up to 50 Kroger products in one call. Carries materially more than kroger-product: a nutrition-facts panel with ingredients, allergens and dietary flags; store-specific price and stock level; a full star-rating histogram; the merchandising hierarchy; and every image perspective. location_id scopes price and stock to one store.
- **Params:** `location_id` (string, optional) — Kroger store/location id that scopes price and stock; `upcs` (string, **required**) — Comma-separated Kroger product UPCs, up to 50

### `kroger_related_tags`

- **HTTP:** `GET /kroger/related-tags`
- **What:** Get Kroger search-refinement tags. Returns the search-refinement chips Kroger shows above its own results for a query (e.g. "chips ahoy" returns "chewy", "chunky", "thins"). Each tag carries the full follow-on query it maps to, so results feed straight back into kroger-search.
- **Params:** `location_id` (string, optional) — Kroger store/location id that scopes results; `query` (string, **required**) — Search term to get refinement tags for

### `kroger_search`

- **HTTP:** `GET /kroger/search`
- **What:** Search Kroger products. Searches Kroger products by keyword and returns product cards (price, unit price, brand, size, stock level) plus the facet groups Kroger offers for the query (brands, nutrition, savings, price range and more). It supports real pagination, and the source field reports which path answered. Facet filters and sort apply to the primary path only: when any of them is set, a failure of that path returns an error rather than silently falling back to unfiltered results.
- **Params:** `brands` (string, optional) — Comma-separated brand names to filter by, taken verbatim from a previous response's facets; `flavor` (string, optional) — Comma-separated flavor facet values; `more_options` (string, optional) — Comma-separated more-options facet values; `nutrition` (string, optional) — Comma-separated nutrition/dietary facet values; `page` (integer, optional) — One-based result page; `price_max` (number, optional) — Upper bound of the price filter; required to filter on price; `price_min` (number, optional) — Lower bound of the price filter; defaults to 0; `query` (string, **required**) — Search keyword; `savings` (string, optional) — Comma-separated savings facet values; `scent` (string, optional) — Comma-separated scent facet values; `sort` (string, optional) — Result order. One of: relevance, name_asc, popularity_desc

### `kroger_store`

- **HTTP:** `GET /kroger/store`
- **What:** Get one Kroger store's detail. Returns one Kroger store's public detail: postal address, geographic coordinates, phone number, displayed opening hours (including any daily break hours), and whether it has a drive-thru. store_id is the same store/location id kroger-products and kroger-suggest accept.
- **Params:** `store_id` (string, **required**) — Kroger store/location id

### `kroger_suggest`

- **HTTP:** `GET /kroger/suggest`
- **What:** Get Kroger search-box suggestions. Returns Kroger's own search-box suggestions for a (possibly empty) query, sourced directly from Kroger's public suggestions API rather than the rendered search page. An empty query returns Kroger's default "trending" shopping shortcuts instead of an error. location_id scopes results to one Kroger store and defaults to a confirmed-working store id when omitted.
- **Params:** `location_id` (string, optional) — Kroger store/location id; `query` (string, optional) — Partial search text; omit for trending default suggestions

## McDonalds (6)

### `mcdonalds_categories`

- **HTTP:** `GET /mcdonalds/categories`
- **What:** List McDonald's menu categories. Returns one market's McDonald's menu categories -- 13 in the United States at time of writing, including breakfast, burgers, chicken-and-fish-sandwiches, mcnuggets-and-mccrispy-strips, snack-wrap, fries-sides, happy-meal, sweets-treats, mccafe-coffees, drinks, sauces-and-condiments and the two value menus; other markets publish their own, from 6 in Switzerland to 17 in Australia. Each entry's slug is the value GET /mcdonalds/menu takes. Slugs are not portable between markets, so pass the same country back. Eight markets publish a reachable menu, fewer than the ten the restaurant locator covers.
- **Params:** `country` (string, optional) — Market (default us). One of us, ca, gb, au, ie, nz, ch, se.

### `mcdonalds_item`

- **HTTP:** `GET /mcdonalds/item`
- **What:** Get one McDonald's item's nutrition. Returns one McDonald's item's published nutrition detail: the full per-serving nutrient list (calories, protein, carbohydrates, total and saturated fat, trans fat, cholesterol, sodium, fibre, sugars, vitamins and minerals -- 21 values for a Big Mac), each with a stable machine key, a unit and a percent-daily-value where McDonald's prints one; plus the item's marketing description, allergen statement, full ingredient statement and image. Item ids come from GET /mcdonalds/menu and are market-specific, so pass the same country back. Seven markets serve this endpoint, fewer than the eight publishing a menu -- Great Britain has a menu but no nutrition surface. Combo meals legitimately carry no nutrient list. Prices are not available on this surface.
- **Params:** `country` (string, optional) — Market (default us). One of us, ca, au, ie, nz, ch, se. Must match the market the item id came from.; `item_id` (string, **required**) — McDonald's numeric product id, from /mcdonalds/menu

### `mcdonalds_item_list`

- **HTTP:** `GET /mcdonalds/item-list`
- **What:** Get nutrition and allergen detail for a batch of McDonald's items. Returns the same published nutrition detail as GET /mcdonalds/item for up to 20 items in one call, plus the per-component ingredient and allergen breakdown that the single-item endpoint does not expose -- a composite item's overall allergen statement is the union of its parts' (a burger's bun, patty, cheese and condiment each carry their own ingredient statement and allergens), so this is the source to use when the full breakdown matters, not just the item-level summary. Item ids come from GET /mcdonalds/menu and are market-specific, so pass the same country back. The response echoes the requested ids so a caller can tell which ones McDonald's returned nothing for.
- **Params:** `country` (string, optional) — Market (default us). One of us, ca, au, ie, nz, ch, se. Must match the market the item ids came from.; `item_ids` (string, **required**) — Comma-separated McDonald's numeric product ids, up to 20

### `mcdonalds_menu`

- **HTTP:** `GET /mcdonalds/menu`
- **What:** List one McDonald's menu category's items. Returns the items in one McDonald's menu category: each item's numeric id, name, product page URL and image. The item id is what GET /mcdonalds/item takes for full nutrition. Category slugs come from GET /mcdonalds/categories and must be paired with the country they came from -- both slugs and item ids are market-specific. Prices are not available; McDonald's does not publish them on this surface. A calorie label is included per item where the category page prints one, which is often blank.
- **Params:** `category` (string, **required**) — Category slug from /mcdonalds/categories; `country` (string, optional) — Market (default us). One of us, ca, gb, au, ie, nz, ch, se. Must match the market the slug came from.

### `mcdonalds_restaurant_menu`

- **HTTP:** `GET /mcdonalds/restaurant-menu`
- **What:** Get one McDonald's restaurant's priced menu. Returns one restaurant's full menu with real prices: item name, image and independently-priced eat-in, pickup and delivery listings, since a McDonald's restaurant genuinely sells a different catalog (and different prices) per channel -- delivery is typically marked up over eat-in/pickup, and some items are channel-exclusive. Where McDonald's publishes a curated substitute or add-on list for an item (a meal's drink upgrade, a dip-able item's sauce choices), each real alternative is included with its own eat-in/pickup price delta -- plain entree or side substitution is not covered, since McDonald's does not publish a curated candidate list for it. This is the only endpoint in this family that publishes prices; every other McDonald's endpoint's source never does. US restaurants only. The store id comes from GET /mcdonalds/restaurants' store_id field.
- **Params:** `store_id` (string, **required**) — McDonald's numeric store number, from /mcdonalds/restaurants

### `mcdonalds_restaurants`

- **HTTP:** `GET /mcdonalds/restaurants`
- **What:** Find McDonald's restaurants near a location. Returns McDonald's restaurants near a latitude/longitude, in any of ten markets. Each restaurant carries its store id, name, street address, city, state, postal code, phone, coordinates, timezone, open status, today's dining and drive-thru hours, the full published week of hours, and McDonald's own amenity codes (for example DRIVETHRU, WIFI, MOBILEOFFERS, GIFTCARDS). A delivery deep link is included where McDonald's publishes one; note it points at a third-party delivery platform. A coordinate with no McDonald's nearby returns an empty list rather than an error. Set country to search outside the United States -- the locator covers more markets than the menu and item endpoints do, so a country valid here is not necessarily valid there.
- **Params:** `country` (string, optional) — Market to search (default us). One of us, gb, ca, au, de, ie, nz, ch, nl, se.; `latitude` (number, **required**) — Search center latitude; `longitude` (number, **required**) — Search center longitude; `max_results` (integer, optional) — Maximum restaurants to return, 1-50 (default 10); `radius` (integer, optional) — Search radius in miles, 1-100 (default 20)

## Panera (13)

### `panera_at_work_locations`

- **HTTP:** `GET /panera/at-work-locations`
- **What:** Get Panera Bread's Panera at Work workplace-delivery locations. Returns the full national Panera at Work location list -- a separate B2B workplace-delivery drop-off program from ordinary cafe pickup/delivery covered by GET /panera/locations. Each location carries its address, coordinates, delivery contact, lead time, the cafe id that services it, and its scheduled drop-off/order-cutoff times per weekday. This is a small, national dataset -- no query parameters are needed.
- **Params:** _none_

### `panera_cafe`

- **HTTP:** `GET /panera/cafe`
- **What:** Get one Panera Bread cafe's detail and hours. Returns one Panera Bread cafe's address, phone, coordinates, amenity flags, per-fulfillment-channel availability (dine-in, storefront/pickup, rapid pickup, drive-thru, curbside, delivery -- each with its own available/open-now/lead-time-minutes and weekly hours where Panera publishes them) and the published storefront hours for the next calendar week with concrete dates. Cafe ids come from GET /panera/locations. An unknown cafe id returns a 404.
- **Params:** `cafe_id` (integer, **required**) — Panera cafe id, from /panera/locations

### `panera_catering_delivery_info`

- **HTTP:** `GET /panera/catering-delivery-info`
- **What:** Get one Panera Bread cafe's catering delivery fee, minimum order, hours and lead times. Returns one cafe's catering delivery fee, minimum order amount, weekly delivery hours, order-size lead-time tiers (e.g. a $750+ order needs a longer lead time than a smaller one), and upcoming available delivery dates with their order windows. This is Panera's catering delivery flow specifically -- catering pickup happens at the cafe itself, whose hours are already covered by GET /panera/cafe. Returns 404 if the cafe does not offer catering delivery.
- **Params:** `cafe_id` (integer, **required**) — Panera cafe id, from /panera/locations

### `panera_catering_menu`

- **HTTP:** `GET /panera/catering-menu`
- **What:** Get one Panera Bread cafe's catering menu with prices, nutrition and allergens. Returns one cafe's catering category list and its full catering item catalog, priced for that specific cafe -- Panera's catering ordering flow is a separate application from its retail site, with its own category structure, pricing and item availability (confirmed live: the same item priced differently between a placeholder default cafe and a real cafe). Categories are a flat list (catering does not publish a category hierarchy the way the retail menu does). Each item carries its price, product type, portion label, whether it is customizable, a full published nutrient panel (calories, calories from fat, fat, saturated fat, trans fat, cholesterol, sodium, carbohydrates, dietary fiber, total sugars, protein, caffeine -- richer than the retail menu's calories/caffeine-only surface), its allergen statement (contains / may-contain, each with an id and display name), and a live in_stock flag from this cafe's current catering stockout feed for today. Cafe ids come from GET /panera/locations.
- **Params:** `cafe_id` (integer, **required**) — Panera cafe id, from /panera/locations

### `panera_geocode`

- **HTTP:** `GET /panera/geocode`
- **What:** Geocode a free-text address for Panera Bread's locator. Resolves a free-text address, city, or postal code to coordinates using Panera Bread's own locator geocoder -- the same lookup its site uses to center a cafe search. Returns latitude/longitude plus the resolved city, state, country and formatted address. An address Panera cannot resolve returns a single result with resolved false rather than an error.
- **Params:** `address` (string, **required**) — Free-text address, city, or postal code

### `panera_item_detail`

- **HTTP:** `GET /panera/item-detail`
- **What:** Get one Panera Bread menu item's full detail. Returns one menu item's full description, ingredient statement, a full per-serving nutrient panel (richer than GET /panera/menu's calories/caffeine-only surface), its allergen statement, and every selectable size with its own price and calories. item_id may be negative -- GET /panera/menu itself surfaces negative item ids for some items, and they resolve fine here. Returns 404 if Panera publishes no detail page for the given item id at this cafe.
- **Params:** `cafe_id` (integer, **required**) — Panera cafe id, from /panera/locations; `item_id` (integer, **required**) — Menu item id, from /panera/menu

### `panera_item_options`

- **HTTP:** `GET /panera/item-options`
- **What:** Get one Panera Bread menu item's selectable option groups. Returns one item's selectable option groups: for a combo, each group is a slot to fill (for example "pick 4 sandwiches", "pick 1 soup"), listing every eligible choice; for a single customizable item, each group is one topping/add-in/amount choice (for example No, Light, Regular, Extra). Each group has min_allowed and max_allowed (how many selections it requires). Each option is one selectable choice, with its own selectable variants (amount tiers) each carrying an item_id and price -- price 0 for a variant included at no extra charge. Panera does not publish a resolved display name for options or groups on this surface, so each option carries its raw upstream image_key as the caller-facing identifier instead of a name. An item that is not customizable, or an unknown item id, returns an empty groups list rather than an error -- Panera's own API does not distinguish the two cases. Item ids come from GET /panera/menu.
- **Params:** `cafe_id` (integer, **required**) — Panera cafe id, from /panera/locations; `item_id` (integer, **required**) — Menu item id, from /panera/menu

### `panera_locations`

- **HTTP:** `GET /panera/locations`
- **What:** Browse Panera Bread's US cafe locator. Returns one level of Panera Bread's US cafe locator tree. Omit both state and city to list every US state and territory Panera serves, each with its cafe count. Pass state to list every city in that state, each with its full cafe list -- id, name, street address, city, state, postal code, phone, coordinates and per-cafe amenity flags (for example hasDriveThru, hasDelivery, hasCurbside, hasKiosk). Pass both state and city to narrow to that one city's cafes. A state Panera does not serve, or a city with no match, returns an empty list rather than an error.
- **Params:** `city` (string, optional) — City name. Requires state. Omit to list every city in the state.; `state` (string, optional) — Two-letter US state abbreviation. Omit to list every state.

### `panera_menu`

- **HTTP:** `GET /panera/menu`
- **What:** Get one Panera Bread cafe's full menu with prices, nutrition and allergens. Returns one cafe's full category tree (with subcategories) and its complete item catalog, priced for that specific cafe -- Panera's prices are genuinely per-cafe, not a national list (the same salad has been confirmed live at different prices in Chicago and New York). Each item carries its price, product type, whether it is customizable, its published nutrients (only Calories and Caffeine are published -- a fuller macro/micronutrient breakdown is not available), its allergen statement (contains / may-contain, each with an id and display name), Panera's own wellness/dietary labels (for example Vegan, Vegetarian, Gluten Conscious), and a live in_stock flag reflecting this cafe's current stockouts. Cafe ids come from GET /panera/locations. An unknown cafe id returns a 404.
- **Params:** `cafe_id` (integer, **required**) — Panera cafe id, from /panera/locations

### `panera_quantity_rules`

- **HTTP:** `GET /panera/quantity-rules`
- **What:** Get one Panera Bread cafe's order-quantity limits. Returns one cafe's active order-quantity limits -- promotional or supply-constrained items Panera caps per order (for example a seasonal souffle limited to 6 within a 2-day window). Each rule has a scope (item or group), the item ids it applies to, and one or more day-offset windows each with its own max_quantity. A cafe with no active limits returns an empty rules list, not an error. Cafe ids come from GET /panera/locations.
- **Params:** `cafe_id` (integer, **required**) — Panera cafe id, from /panera/locations

### `panera_retired_products`

- **HTTP:** `GET /panera/retired-products`
- **What:** Get Panera Bread's retired and seasonal menu items. Returns items no longer on the active menu, resolved through the given cafe's own version map -- either permanently retired (availability_stage RETIRED) or currently out of seasonal rotation (SEASONAL, may return). Each item carries its name, description, portion label and image key. Cafe ids come from GET /panera/locations.
- **Params:** `cafe_id` (integer, **required**) — Panera cafe id, from /panera/locations

### `panera_time_slots`

- **HTTP:** `GET /panera/time-slots`
- **What:** Get one Panera Bread cafe's available order time-slot windows. Returns one cafe's available pickup/delivery order time-slot windows for one date, plus that date's overall open/close time. Unlike GET /panera/cafe's published storefront hours, this reflects live order-slot availability, not just when the cafe is open -- an empty windows list is a legitimate outcome (e.g. the cafe is closed that day), not an error. date must be YYYY-MM-DD, interpreted in the cafe's own local timezone.
- **Params:** `cafe_id` (integer, **required**) — Panera cafe id, from /panera/locations; `date` (string, **required**) — Date, YYYY-MM-DD

### `panera_upsell_suggestions`

- **HTTP:** `GET /panera/upsell-suggestions`
- **What:** Get one Panera Bread cafe's per-item upsell suggestions. Returns Panera's own suggested add-ons per menu item (for example "Extra Turkey" and "Extra Bacon" for a Bacon Turkey Bravo sandwich). Item ids on this surface are in a separate id space from /panera/menu's item_id, but both the item and its suggestions carry their own resolved names, so no cross-reference is needed. Cafe ids come from GET /panera/locations.
- **Params:** `cafe_id` (integer, **required**) — Panera cafe id, from /panera/locations

## Pandamart (6)

### `pandamart_search`

- **HTTP:** `GET /pandamart/search`
- **What:** Search pandamart darkstores near a location. Returns pandamart grocery/convenience darkstores delivering to a latitude/longitude. Each store carries its code (the value the store and products endpoints take), name, address, coordinates, budget tier, chain, minimum order amount and delivery fee, delivery/pickup availability, and a hero image. A location with no coverage returns an empty list rather than an error.
- **Params:** `latitude` (number, **required**) — Search center latitude; `limit` (integer, optional) — Darkstores to return, clamped to 50 (default 20); `longitude` (number, **required**) — Search center longitude; `market` (string, optional) — Delivery Hero market. One of sg, pk, bd, hk, my, ph. Defaults to sg.; `offset` (integer, optional) — Result offset for pagination (default 0)

### `pandamart_store`

- **HTTP:** `GET /pandamart/store`
- **What:** Get one pandamart darkstore's detail. Returns one pandamart darkstore's detail by code: name, address, coordinates, budget tier, chain, minimum order amount, minimum delivery fee, delivery/pickup availability, timezone, and a hero image. Supplying latitude and longitude only affects the (optional) computed fields the upstream itself returns for that coordinate; it does not filter or reject the lookup.
- **Params:** `code` (string, **required**) — Darkstore code, from /pandamart/search's code field; `latitude` (number, optional) — Caller latitude, optional; `longitude` (number, optional) — Caller longitude, optional; `market` (string, optional) — Delivery Hero market the store belongs to. One of sg, pk, bd, hk, my, ph. Defaults to sg.

### `pandamart_store_categories`

- **HTTP:** `GET /pandamart/store/categories`
- **What:** Get one pandamart darkstore's category tree. Returns one darkstore's full category tree: every category and sub-category, each with the upstream-reported product count and (for top-level categories) an image. This lists what categories exist and how large they are -- it does not fetch the items inside any one category. Sub-category product counts are frequently 0 upstream; only top-level counts are reliably populated.
- **Params:** `code` (string, **required**) — Darkstore code, from /pandamart/search's code field; `market` (string, optional) — Delivery Hero market the store belongs to. One of sg, pk, bd, hk, my, ph. Defaults to sg.

### `pandamart_store_product`

- **HTTP:** `GET /pandamart/store/product`
- **What:** Get one pandamart product's full detail. Returns one product's full detail by ID: the same fields a shelf/search result carries plus category_id and, for weighable/grocery items, per-unit pricing and nutrition attributes. Resolves the store's page slug internally, so only the darkstore code and product ID are needed.
- **Params:** `code` (string, **required**) — Darkstore code, from /pandamart/search's code field; `market` (string, optional) — Delivery Hero market the store belongs to. One of sg, pk, bd, hk, my, ph. Defaults to sg.; `product_id` (string, **required**) — Product ID, from a search/products/categories response's id field

### `pandamart_store_products`

- **HTTP:** `GET /pandamart/store/products`
- **What:** Get one pandamart darkstore's product showcase. Returns one darkstore's product showcase: every named shelf its own home page displays (deals, new arrivals, category highlights, etc.), each with real prices, stock, and availability. This is the curated set of shelves the store's home page surfaces, not the full category-browsable catalog.
- **Params:** `code` (string, **required**) — Darkstore code, from /pandamart/search's code field; `market` (string, optional) — Delivery Hero market the store belongs to. One of sg, pk, bd, hk, my, ph. Defaults to sg.

### `pandamart_store_search`

- **HTTP:** `GET /pandamart/store/search`
- **What:** Search for products within one pandamart darkstore. Searches by keyword within one darkstore's own catalog -- the pandamart equivalent of the search box on a darkstore page. Unlike the product showcase's curated shelves, this reaches the store's full catalog by keyword. Returns matching products with real prices, stock, and availability, plus total_products and has_more for pagination via page/limit.
- **Params:** `code` (string, **required**) — Darkstore code, from /pandamart/search's code field; `limit` (integer, optional) — Products per page, clamped to 10-50 (default 20); `market` (string, optional) — Delivery Hero market the store belongs to. One of sg, pk, bd, hk, my, ph. Defaults to sg.; `page` (integer, optional) — 1-based result page (default 1); `query` (string, **required**) — Product search text; `sort` (string, optional) — Result order. One of RELEVANCE, PRICE_ASC, PRICE_DESC. Defaults to RELEVANCE.

## Papa John's (23)

### `papajohns_allergens`

- **HTTP:** `GET /papajohns/allergens`
- **What:** Get Papa John's full allergen guide. Returns Papa John's complete published item x allergen matrix (crusts, sauces, cheeses, meats, veggies, and more), grouped by section, each item flagged for peanut, tree nut, egg, milk, wheat, soy, fish, shellfish, and sesame content.
- **Params:** _none_

### `papajohns_colombia_menu`

- **HTTP:** `GET /papajohns/colombia/menu`
- **What:** Get the Papa John's Colombia priced menu (COP). Returns Papa John's **Colombia** menu with prices in Colombian pesos. Every product lists its priced SKU variants across the four axes Colombia sells on — size, dough, crust and sauce — each with its own price and availability. Colombia runs its own ordering platform, independent of the six markets behind GET /papajohns/intl/menu and of Peru and El Salvador, so it has its own endpoint. Prices are Colombian pesos and are not comparable with any other market. The full catalog is paged through before returning, so the response is complete rather than a first page.
- **Params:** `category` (string, optional) — Return only categories whose name contains this text, case-insensitive, e.g. Pizzas or Bebidas; `include_variants` (boolean, optional) — Include every priced SKU variant. Default true; set false for a lighter response carrying only each product's cheapest price.

### `papajohns_deals`

- **HTTP:** `GET /papajohns/deals`
- **What:** List a Papa John's restaurant's current promotions. Returns the promotions a Papa John's US or Canada restaurant is currently running. Each offer carries its redemption code, title, description, offer price and — where the deal advertises a saving — the struck-through regular price, plus its artwork and deal-builder link. Pass a store_id from GET /papajohns/store or GET /papajohns/nearby: promotions are store-specific, and the national response is largely placeholders prompting the customer to choose a store, which are omitted here rather than returned as real offers.
- **Params:** `store_id` (string, optional) — Restaurant id from GET /papajohns/store or GET /papajohns/nearby. Omit for national promotions.

### `papajohns_directory`

- **HTTP:** `GET /papajohns/directory`
- **What:** Browse the Papa John's store directory. Returns one level of Papa John's store directory. Omit path for the root country index, then pass a child's path to descend through state, city, and store levels. Each child includes its name, path, URL, store count when available, and whether it is a store leaf. Pass a store child's path to GET /papajohns/store. This is a directory browse; use GET /papajohns/nearby for a coordinate search.
- **Params:** `path` (string, optional) — Directory path from a previous response's children[].path; omit for the root country index

### `papajohns_elsalvador_menu`

- **HTTP:** `GET /papajohns/elsalvador/menu`
- **What:** Get the Papa John's El Salvador priced menu (USD). Returns Papa John's **El Salvador** menu with prices in US dollars. Each pizza lists its full size and crust price matrix — every combination of size (Grande, Gigante) and crust (Masa Original, Masa Delgada, Orilla Rellena de Queso) with that combination's own price — while sides, desserts and extras carry a single price. El Salvador runs its own ordering platform, independent of the six markets behind GET /papajohns/intl/menu and of Colombia and Peru, so it has its own endpoint. This is El Salvador's national menu; the site itself notes that choosing a restaurant can reveal further items.
- **Params:** `category` (string, optional) — Return only categories whose name contains this text, case-insensitive. One of: Pizzas, Entradas, Postres, Extras

### `papajohns_india_deal`

- **HTTP:** `GET /papajohns/india/deal`
- **What:** Get one Papa John's India deal's composition (INR). Returns one Papa John's **India** combo or offer with its full composition: each slot in the deal (with its quantity, size, and whether it can be skipped) and every menu item eligible to fill that slot, with each choice's own price in Indian Rupees. This is materially more than the deal row in GET /papajohns/india/menu, which carries only the deal's name, price, and pricing rule. price_type is one of fixedPrice, BuyXGetY, HalfAndHalf, or variablePrice; only fixedPrice deals report a non-zero price. India market only.
- **Params:** `deal_id` (string, **required**) — Deal id from GET /papajohns/india/menu (items with kind=deal)

### `papajohns_india_menu`

- **HTTP:** `GET /papajohns/india/menu`
- **What:** Get the Papa John's India priced menu (INR). Returns Papa John's **India** menu with live prices in Indian Rupees, from papajohns.in's own ordering backend. This is the India market only -- prices, items, and availability are India-specific and are not comparable to Papa John's US/Canada data (see GET /papajohns/nutrition for US national reference data). Returns every category with its items and deals: list price, strike-through price where a discount is active, dietary tags (Veg, Non Veg, Spicy), images, and the store/channel/day combinations where an item is blacked out. Set include_options=true to also get each item's full size, crust, topping, sauce, and drizzle tree with per-option prices -- this makes the response very large, so prefer GET /papajohns/india/menu/item for one item's options. Pricing is franchise-wide rather than per-store; store_id, channel_id, and day filter item availability, not price, and only take effect when all three are supplied.
- **Params:** `category_id` (string, optional) — Return only this category id; `channel_id` (string, optional) — Order channel. One of: 1 (Delivery), 2 (Take Away), 3 (Dine In), 4 (Drive Through Pickup). Only applies together with store_id and day.; `day` (string, optional) — Weekday. One of: 0 (Sunday), 1 (Monday), 2 (Tuesday), 3 (Wednesday), 4 (Thursday), 5 (Friday), 6 (Saturday). Only applies together with store_id and channel_id.; `include_options` (boolean, optional) — Include every item's full size/crust/topping option tree with prices. Default false.; `store_id` (string, optional) — Hide items blacked out at this store id (see GET /papajohns/india/stores). Only applies together with channel_id and day.; `tag` (string, optional) — Return only items carrying this tag, e.g. Veg, Non Veg, Spicy. Case-insensitive.

### `papajohns_india_menu_item`

- **HTTP:** `GET /papajohns/india/menu/item`
- **What:** Get one Papa John's India item with its full options (INR). Returns one Papa John's **India** menu item with its complete customization tree: every size, and for each size every crust, topping, dipping sauce, drizzle, and base sauce with that option's own price in Indian Rupees. The option group flagged base_price carries the item's base price for that size (the crust group on pizzas) rather than an add-on charge; half_price is the surcharge when the option is applied to one half of a pizza. India market only -- prices are Indian Rupees. Use GET /papajohns/india/menu to discover item ids.
- **Params:** `item_id` (string, **required**) — Item id (saleitem_id) from GET /papajohns/india/menu

### `papajohns_india_stores`

- **HTTP:** `GET /papajohns/india/stores`
- **What:** List Papa John's India restaurants. Returns every Papa John's **India** restaurant with its address, phone, coordinates, and weekly opening hours broken down per order channel (delivery, take away, dine in, drive-through pickup). These store ids are what GET /papajohns/india/menu's store_id availability filter is keyed on. India market only -- for US/Canada stores use GET /papajohns/directory, GET /papajohns/store, or GET /papajohns/nearby.
- **Params:** `channel_id` (string, optional) — Return only hours for this order channel. One of: 1 (Delivery), 2 (Take Away), 3 (Dine In), 4 (Drive Through Pickup).

### `papajohns_intl_deals`

- **HTTP:** `GET /papajohns/intl/deals`
- **What:** List Papa John's active promotions (international). Returns the promotions currently running in one of six international markets: Chile, Costa Rica, Guatemala, Panama, Portugal, and Spain, for either delivery or pickup. Each promotion carries its headline product, description, artwork, the weekdays it runs on, and its start and end dates. Offers that upstream has marked inactive are omitted rather than returned as live.
- **Params:** `dispatch_method` (string, **required**) — One of: pj_delivery (delivery offers), in_store (pickup/dine-in offers); `market` (string, **required**) — Market. One of: chile, costa-rica, guatemala, panama, portugal, spain

### `papajohns_intl_ingredients`

- **HTTP:** `GET /papajohns/intl/ingredients`
- **What:** Get a Papa John's menu's ingredient catalog (international). Returns every topping, sauce, and cheese a pizza can be built with on one menu, in one of six international markets: Chile, Costa Rica, Guatemala, Panama, Portugal, and Spain. Each ingredient reports its family (meat, vegetable, base sauce, and so on), whether it is included on pizzas by default, whether it is charged at the premium rather than the normal rate, and whether it can be applied to just one half. The response also carries what one extra ingredient costs at each size, for both the normal and premium rates. Menu ids come from GET /papajohns/intl/stores.
- **Params:** `category` (string, optional) — Return only one ingredient category. One of: base_cheese, base_sauce, extra_cheese, extra_sauce, meat, not_ingredient, premium, vegetable; `market` (string, **required**) — Market. One of: chile, costa-rica, guatemala, panama, portugal, spain; `menu_id` (string, **required**) — Menu id from a restaurant returned by GET /papajohns/intl/stores

### `papajohns_intl_menu`

- **HTTP:** `GET /papajohns/intl/menu`
- **What:** Get a Papa John's restaurant's priced menu (international). Returns one Papa John's restaurant's full menu with that restaurant's own prices, in one of six international markets: Chile, Costa Rica, Guatemala, Panama, Portugal, and Spain. Prices are per restaurant, not national, so two restaurants in the same market can differ. Each pizza lists every size and crust combination it is sold in with that combination's own price and, where published, its calorie and portion figures; sides, drinks and desserts list their own portions. Machine codes for size and crust are returned alongside the market's own display labels in the local language. Currency is whatever the market trades in -- euros in Spain and Portugal, Chilean pesos in Chile, and so on -- so do not compare figures across markets. Use GET /papajohns/intl/stores to find a store_id. For India use GET /papajohns/india/menu; for the US and Canada see GET /papajohns/nutrition.
- **Params:** `food_type` (string, optional) — Return only products carrying this dietary or heat marker. One of: hot, mild, spicy, vegetarian. Products upstream does not mark are excluded.; `kind` (string, optional) — Return only one product kind. One of: pizza, side; `market` (string, **required**) — Market. One of: chile, costa-rica, guatemala, panama, portugal, spain; `store_id` (string, **required**) — Restaurant id from GET /papajohns/intl/stores. Prices are specific to this restaurant.

### `papajohns_intl_offer`

- **HTTP:** `GET /papajohns/intl/offer`
- **What:** Get one Papa John's offer's composition (international). Returns one promotional offer's full composition in one of six international markets: Chile, Costa Rica, Guatemala, Panama, Portugal, and Spain. This is what a promotion banner from GET /papajohns/intl/deals actually contains: the offer's own price, each choice step a customer works through in order (e.g. "pick your family pizza", "pick a side"), and every product eligible at that step with the surcharge picking it adds. It also carries the offer's ingredient rules -- how many extras are free, the minimum and maximum that may be chosen, and which ingredient families are allowed. Offer ids come from the offer_id field on a deal.
- **Params:** `market` (string, **required**) — Market. One of: chile, costa-rica, guatemala, panama, portugal, spain; `offer_id` (string, **required**) — Offer id from the offer_id field on GET /papajohns/intl/deals

### `papajohns_intl_product`

- **HTTP:** `GET /papajohns/intl/product`
- **What:** Get one Papa John's product (international). Returns one product's own catalog record in one of six international markets: Chile, Costa Rica, Guatemala, Panama, Portugal, and Spain -- its description, imagery, dietary markers, and customization rules (whether toppings may be changed, how many extra ingredients are included free, and whether it can be used as one half of a half-and-half pizza). This record carries no price, because pricing is per restaurant: use GET /papajohns/intl/menu for prices. Product ids come from that same endpoint.
- **Params:** `market` (string, **required**) — Market. One of: chile, costa-rica, guatemala, panama, portugal, spain; `product_id` (string, **required**) — Product id from GET /papajohns/intl/menu

### `papajohns_intl_stores`

- **HTTP:** `GET /papajohns/intl/stores`
- **What:** Find Papa John's restaurants in an international market. Returns Papa John's restaurants in one of six international markets: Chile, Costa Rica, Guatemala, Panama, Portugal, and Spain -- either every restaurant near a coordinate, or one known restaurant looked up by id. Each restaurant carries its address, coordinates, phone, per-weekday opening hours split by fulfillment channel, accepted payment methods, delivery zones with their minimum-order and free-delivery thresholds, and live delivery/pickup open flags. Restaurants come back ranked by distance with no radius limit, five at a time by default; page and limit walk the rest, and the response reports total_count, the market's whole restaurant total. The returned id is what GET /papajohns/intl/menu prices against, and menu_id is what GET /papajohns/intl/ingredients reads. This covers those six markets only -- for India use GET /papajohns/india/stores, and for the US and Canada use GET /papajohns/directory, GET /papajohns/store, or GET /papajohns/nearby.
- **Params:** `fulfillment` (string, optional) — One of: delivery (default, every nearby restaurant), pickup (only restaurants accepting pickup orders). Ignored when store_id is supplied.; `latitude` (string, optional) — Latitude to search around. Required unless store_id is supplied.; `limit` (integer, optional) — Restaurants per page, 1-100. Ignored for a store_id lookup and for pickup, neither of which is paginated.; `longitude` (string, optional) — Longitude to search around. Required unless store_id is supplied.; `market` (string, **required**) — Market. One of: chile, costa-rica, guatemala, panama, portugal, spain; `page` (integer, optional) — One-based page of the distance-ranked restaurants. Ignored for a store_id lookup and for pickup, neither of which is paginated.; `store_id` (string, optional) — Look up one known restaurant by id instead of searching a coordinate. Supply either store_id, or both latitude and longitude.

### `papajohns_menu`

- **HTTP:** `GET /papajohns/menu`
- **What:** Get a Papa John's restaurant's priced menu. Returns a Papa John's US or Canada restaurant's full menu with that restaurant's own prices. Prices are per restaurant, not national -- the same 14-inch pizza can differ by several dollars between two stores -- so pass a store_id from GET /papajohns/store or GET /papajohns/nearby. Omitting it returns the national default menu, flagged as national_default in the response. Each category is returned with its sections and product groups, and every orderable SKU carries its price, calories, serving size, slice count and image. Set include_options to also get each product group's customization axes: every size and crust it is sold in, and every preparation instruction (how much cheese, how well done) with its choices. This is the US and Canada menu -- for India use GET /papajohns/india/menu, and for Chile, Costa Rica, Guatemala, Panama, Portugal or Spain use GET /papajohns/intl/menu.
- **Params:** `category` (string, optional) — Return only one category. One of: dippingsauces, desserts, drinks, extras, papabowls, pizza, sandwiches, sides, wings; `include_options` (boolean, optional) — Include each product group's sizes, crusts and preparation instructions. Default false.; `store_id` (string, optional) — Restaurant id from GET /papajohns/store or GET /papajohns/nearby. Omit for the national default menu.

### `papajohns_menu_item`

- **HTTP:** `GET /papajohns/menu/item`
- **What:** Get one Papa John's menu item with its options. Returns one Papa John's US or Canada menu SKU with that restaurant's price for it, together with the full customization axes of the product group it belongs to: every size and crust the product is sold in, and every preparation instruction with its choices and default. The response also names the category and section the item sits under. Pass a store_id so the price is that restaurant's; omitting it returns the national default price. SKUs come from GET /papajohns/menu.
- **Params:** `sku` (string, **required**) — Product sku from GET /papajohns/menu; `store_id` (string, optional) — Restaurant id from GET /papajohns/store or GET /papajohns/nearby. Omit for the national default price.

### `papajohns_nearby`

- **HTTP:** `GET /papajohns/nearby`
- **What:** Find Papa John's stores near a coordinate. Returns Papa John's stores within a radius of a latitude/longitude, ordered nearest first, with distance, address, phone, hours, timezone, price range, fulfillment services, payment options, and ordering link. The response includes total_in_radius and offset paging. A coordinate with no nearby stores returns an empty list.
- **Params:** `latitude` (number, **required**) — Search center latitude; `limit` (integer, optional) — Maximum stores to return, 1-50 (default 10); `longitude` (number, **required**) — Search center longitude; `offset` (integer, optional) — Result offset, 0 or greater (default 0); `radius` (integer, optional) — Search radius in miles, 1-100 (default 25)

### `papajohns_nutrition`

- **HTTP:** `GET /papajohns/nutrition`
- **What:** Get one Papa John's nutritional-details category. Returns Papa John's own published nutrition-facts panel for every item in one category -- full pizzas by name, or a single ingredient family (crust, cheese, sauce, toppings). Each item lists every published size/crust variant with serving size and a full nutrition-facts breakdown (calories, fat, cholesterol, sodium, carbohydrate, fiber, sugars, protein). This is Papa John's national reference data, not priced per-store data -- see GET /papajohns/directory for store lookup.
- **Params:** `category` (string, **required**) — One of: cheese, crust, desserts, dipping-sauces, drinks, extras, papa-bowls, papadias, pizzas, sandwiches, sauce, sides, toppings, wings

### `papajohns_peru_menu`

- **HTTP:** `GET /papajohns/peru/menu`
- **What:** Get the Papa John's Peru priced menu (PEN). Returns Papa John's **Peru** menu with prices in Peruvian soles, covering the full catalog with categories, images and per-product pricing. Peru runs its own ordering platform, independent of the six markets behind GET /papajohns/intl/menu and of Colombia and El Salvador, so it has its own endpoint. Prices are Peruvian soles and are not comparable with any other market.
- **Params:** `category` (string, optional) — Return only categories whose name contains this text, case-insensitive, e.g. Promociones or Combos

### `papajohns_poland_menu`

- **HTTP:** `GET /papajohns/poland/menu`
- **What:** Get the Papa John's Poland priced menu (PLN). Returns Papa John's **Poland** menu with prices in Polish zloty. Russia and Poland run one franchise platform of their own, separate from the six markets behind GET /papajohns/intl/menu and from Colombia, Peru and El Salvador, so each has its own endpoint. The catalog is national -- it does not vary by city -- and every product lists its priced variants with size, dough and any stuffed crust. Prices are zloty and are not comparable with any other market.
- **Params:** `category` (string, optional) — Return only sections whose name or slug contains this text, case-insensitive. Slugs work in either market, e.g. pizza, combo, deserty, napitki, sauce, zakuski

### `papajohns_russia_menu`

- **HTTP:** `GET /papajohns/russia/menu`
- **What:** Get the Papa John's Russia priced menu (RUB). Returns Papa John's **Russia** menu with prices in Russian roubles. Russia and Poland run one franchise platform of their own, separate from the six markets behind GET /papajohns/intl/menu and from Colombia, Peru and El Salvador, so each has its own endpoint. The catalog is national -- it does not vary by city -- and every product lists its priced variants with size, dough and any stuffed crust. Prices are roubles and are not comparable with any other market.
- **Params:** `category` (string, optional) — Return only sections whose name or slug contains this text, case-insensitive. Slugs work in either market, e.g. pizza, combo, deserty, napitki, sauce, zakuski

### `papajohns_store`

- **HTTP:** `GET /papajohns/store`
- **What:** Get one Papa John's store. Returns one Papa John's store's published profile: address, phone, coordinates, general and pickup hours, timezone, Google Place id, and ordering link. The path comes from a store child returned by GET /papajohns/directory. Passing a directory path returns 404.
- **Params:** `path` (string, **required**) — Store path from a /papajohns/directory child marked is_store=true

## Pizza Hut (6)

### `pizzahut_bundle_choices`

- **HTTP:** `GET /pizzahut/bundle-choices`
- **What:** Get one Pizza Hut deal/combo's full choice-builder tree. Returns one deal/combo's full choice-builder tree -- every named slot it offers (e.g. "1st Pizza", "Wings or Fries", "1st Dip") and every product variant a caller can pick to fill that slot, each with the real price delta selecting it adds over the bundle's base price (zero for a variant already covered by the deal, positive for an upgrade such as a larger size or a specialty pizza). This is a different structure from /pizzahut/modifiers -- that endpoint customizes toppings/sauces on one product variant, while this endpoint swaps whole product variants in and out of a multi-item combo. bundle_code comes from /pizzahut/menu's code field on a type=bundle item.
- **Params:** `bundle_code` (string, **required**) — A deal/combo's bundle code, from /pizzahut/menu's code field on a type=bundle item; `channel` (string, optional) — Order channel the deal and pricing reflect (default WEB); `store_number` (string, **required**) — Pizza Hut's store number, from /pizzahut/stores

### `pizzahut_delivery_estimate`

- **HTTP:** `GET /pizzahut/delivery-estimate`
- **What:** Check Pizza Hut delivery serviceability and estimated fee for one store and address. Checks whether a Pizza Hut restaurant's delivery integration can deliver to a given address and, when it can, the estimated delivery fee (broken down by fee line item) and pickup/dropoff time. This is a checkout-time estimate -- it does not add an item to a cart or place an order, and takes no payment or account information. serviceable is true only when the upstream returned a real estimate; a false value with reason populated covers every other case seen live, such as the requested delivery_provider not being enabled at that store. For the default INTERNAL provider, a serviceable result does not by itself confirm the address is within a real deliverable radius -- see this endpoint's markdown doc for the caveat. order_subtotal materially affects the fee estimate, so it is required rather than defaulted. pickup_at defaults to 30 minutes from now (an "order now" style estimate) when omitted.
- **Params:** `address1` (string, **required**) — Delivery address line 1; `address2` (string, optional) — Delivery address line 2; `city` (string, **required**) — Delivery address city; `country_code` (string, optional) — Delivery address country code (default US); `delivery_provider` (string, optional) — Delivery provider to check (default INTERNAL); `latitude` (number, **required**) — Delivery address latitude; `longitude` (number, **required**) — Delivery address longitude; `order_subtotal` (number, **required**) — Order subtotal before fees, in dollars; `pickup_at` (string, optional) — RFC3339 pickup time (default 30 minutes from now); `postal_code` (string, **required**) — Delivery address postal code; `state` (string, **required**) — Delivery address state, two-letter code; `store_number` (string, **required**) — Pizza Hut's store number, from /pizzahut/stores

### `pizzahut_menu`

- **HTTP:** `GET /pizzahut/menu`
- **What:** Get one Pizza Hut restaurant's full priced menu. Returns one restaurant's full menu grouped into categories (e.g. "Pizza", "Wings", "Deals"). Every entry is a product, a bundle (a deal or combo), or a standalone priced variant -- type tells callers which -- and carries a price in USD cents plus a decimal dollar value, and an image when the upstream publishes one. A product item also lists variants: every other priced size/crust/style option beyond its default (e.g. a pizza's Personal Pan through Large Original Stuffed Crust). Prices reflect this specific restaurant and order channel, not a national default. channel selects which order channel the menu is priced for (web ordering by default); prices can genuinely differ by channel (e.g. a delivery-marketplace channel vs. web). Some restaurants also carry products with no category at all (e.g. individual dip cup flavors); these are returned separately as uncategorized_items rather than silently dropped.
- **Params:** `channel` (string, optional) — Order channel the menu is priced for (default WEB); `store_number` (string, **required**) — Pizza Hut's store number, from /pizzahut/stores

### `pizzahut_modifiers`

- **HTTP:** `GET /pizzahut/modifiers`
- **What:** Get one Pizza Hut product variant's full customization tree. Returns one product variant's full build-your-own customization tree -- every slot (e.g. "Pizza Sauce", "Pizza Cheese", "Pizza Toppings", "Crust Finishers"), every modifier within it (a specific topping, sauce flavor, or seasoning), and every weight/placement option (e.g. Light, Regular, Extra, or a Left/Right/Whole pizza-half placement) with its own real price delta -- zero for an amount already included by default, a positive upcharge for an "extra" option. variant_code comes from /pizzahut/menu's variant_code or variants[].variant_code fields.
- **Params:** `channel` (string, optional) — Order channel the customization tree and pricing reflect (default WEB); `store_number` (string, **required**) — Pizza Hut's store number, from /pizzahut/stores; `variant_code` (string, **required**) — A product's specific size/crust/style variant code, from /pizzahut/menu

### `pizzahut_store`

- **HTTP:** `GET /pizzahut/store`
- **What:** Get one Pizza Hut restaurant by its store number. Returns one Pizza Hut restaurant's detail by its exact store number, from /pizzahut/stores, including its recurring open hours per order channel (carryout, delivery, dine-in, drive-thru, catering carryout) plus each channel's ordering constraints -- minimum/maximum order amount, whether tipping is offered, and accepted payment methods. A channel this restaurant does not offer at all is omitted from hours rather than reported as always-closed.
- **Params:** `store_number` (string, **required**) — Pizza Hut's store number, from /pizzahut/stores

### `pizzahut_stores`

- **HTTP:** `GET /pizzahut/stores`
- **What:** Search Pizza Hut restaurants by city, state, postal code, name, franchise code, or store number. Returns Pizza Hut restaurants matching a city/state/postal code/name/franchise code/store number filter. At least one filter is required -- an unfiltered call would enumerate every US restaurant in one response, which this endpoint intentionally does not expose. Each restaurant carries its store number (the value /pizzahut/menu and /pizzahut/store take), full address with coordinates, phone, whether it currently accepts online orders, and its timezone.
- **Params:** `accepting_online_orders` (boolean, optional) — Restrict to restaurants currently accepting (true) or not accepting (false) online orders. Unfiltered (upstream default) unless set; `appear_in_store_results` (boolean, optional) — Restrict to restaurants Pizza Hut's own storefront marks customer-facing. Unfiltered (upstream default) unless set -- passing true returns zero results for every region tested during research, so it is not defaulted on; `city` (string, optional) — Restaurant city; `franchise_code` (string, optional) — Exact franchise/operator code; `is_archived` (boolean, optional) — Set true to include archived/closed restaurant records, which the upstream default (unset) already excludes. Set false to make that exclusion explicit; `max_results` (integer, optional) — Maximum restaurants to return, 1-50 (default 20); `name` (string, optional) — Restaurant name, partial match; `postal_code` (string, optional) — Restaurant postal code; `sort` (string, optional) — Sort order; `state` (string, optional) — Restaurant state, two-letter code; `store_number` (string, optional) — Exact store number

## Popeyes (8)

### `popeyes_faq`

- **HTTP:** `GET /popeyes/faq`
- **What:** List Popeyes' published customer-support FAQ. Returns a page of Popeyes' published customer-support FAQ -- questions and answers such as "How do I remove items from my cart?". This is public help-center content, not account/order-specific support state, and does not require an order id or any customer identifier.
- **Params:** `limit` (integer, optional) — Maximum FAQ entries to return, 1-100 (default 20); `offset` (integer, optional) — Number of FAQ entries to skip, for paging (default 0)

### `popeyes_location`

- **HTTP:** `GET /popeyes/location`
- **What:** Look up one Popeyes restaurant directly by store id. Returns one restaurant's full detail -- the same fields /popeyes/locations returns per restaurant (address, coordinates, phone, operator, amenity flags, full published hours) -- looked up directly by its numeric store id instead of a coordinate/radius search. Useful when the store id is already known, e.g. from a prior /popeyes/locations call. An unknown store id returns a 404.
- **Params:** `market` (string, optional) — Restaurant market: `US` (default) or `CA`; `store_id` (string, **required**) — Popeyes' numeric store id, from /popeyes/locations

### `popeyes_locations`

- **HTTP:** `GET /popeyes/locations`
- **What:** Find Popeyes restaurants near a location. Returns Popeyes restaurants near a latitude/longitude. Each restaurant carries its internal id and numeric store id (the value /popeyes/menu takes), full address with coordinates, phone, the operating franchise group, amenity flags (breakfast, delivery, drive-thru, playground, takeout, wifi, halal, dark kitchen) and the full published week of hours for dining room, drive-thru, delivery and curbside separately. A coordinate with no nearby Popeyes returns an empty list rather than an error.
- **Params:** `latitude` (number, **required**) — Search center latitude; `longitude` (number, **required**) — Search center longitude; `market` (string, optional) — Restaurant market: `US` (default) or `CA`; `max_results` (integer, optional) — Maximum restaurants to return, 1-50 (default 20); `radius` (integer, optional) — Search radius in meters, 1-50000 (default 8000)

### `popeyes_menu`

- **HTTP:** `GET /popeyes/menu`
- **What:** Get one Popeyes restaurant's menu with real per-store pricing. Returns one restaurant's menu grouped into categories (e.g. "Big Box", "Chicken Wraps"). Every entry is an item, a combo, a picker (a variant-choice product such as "choose your side") or a bundle, and carries a price reflecting this specific restaurant when Popeyes reports one for that exact entry -- a missing price does not mean the item is free, it means this restaurant's pricing call did not cover that entry. Some menu entries are published directly at the top level outside any named section; these are grouped into a synthetic "Featured" category (featured true). Entries of type ITEM also carry published nutrition facts and allergen data when Popeyes reports them for that item; COMBO/PICKER/BUNDLE entries do not carry their own nutrition/allergen data.
- **Params:** `market` (string, optional) — Restaurant market: `US` (default) or `CA`; `store_id` (string, **required**) — Popeyes' numeric store id, from /popeyes/locations

### `popeyes_offers`

- **HTTP:** `GET /popeyes/offers`
- **What:** List Popeyes' promotional deals and coupons. Returns a page of Popeyes' promotional offers/deals catalog -- named value deals (e.g. "3Pc Signature Chicken for $5"), percentage-off combos, and paper coupons. This is CMS content describing the offer catalog, the same kind of public data /popeyes/menu already reads from -- not a personalized or store-specific list, and not account/loyalty state. A missing price does not mean free; a price of 0 means the offer's discount is not expressed as a flat price (see offer_tag/name instead, e.g. a percentage-off deal). requires_authentication reflects the offer's own published redemption rules, not any account state this endpoint reads. The catalog spans hundreds of entries including ones no longer running; there is no upstream "currently active" flag, so pages should be read as reference data, not a guarantee every entry is live right now.
- **Params:** `limit` (integer, optional) — Maximum offers to return, 1-100 (default 20); `market` (string, optional) — Restaurant market: US (default) or CA; `offset` (integer, optional) — Number of offers to skip, for paging (default 0)

### `popeyes_promotions`

- **HTTP:** `GET /popeyes/promotions`
- **What:** List Popeyes Rewards' bonus-points promotion catalog. Returns a page of Popeyes Rewards' bonus-points promotion catalog -- flat or multiplied points bonuses tied to a qualifying purchase (e.g. "Get Double Bonus Points on Your Cart, minimum $20"), distinct from /popeyes/offers (priced menu deals) and /popeyes/quests (multi-step challenges). This is public CMS content, not a signed-in member's own applied-promotions state. points_multiplier and bonus_points are mutually exclusive in practice -- a promotion is either an "Nx points" campaign or a flat bonus. start_date/end_date bound the promotion's published active window when Popeyes sets one; both empty means no published window restriction, not that the promotion is permanently active.
- **Params:** `limit` (integer, optional) — Maximum promotions to return, 1-100 (default 20); `market` (string, optional) — Restaurant market: US (default) or CA; `offset` (integer, optional) — Number of promotions to skip, for paging (default 0)

### `popeyes_quests`

- **HTTP:** `GET /popeyes/quests`
- **What:** List Popeyes Rewards' loyalty-challenge catalog. Returns a page of Popeyes Rewards' loyalty-challenge catalog -- named multi-step challenges and their reward (e.g. "Make Two Purchases, Get FREE Chicken Sandwich in the form of 550 Bonus Points"). This is public CMS content describing the challenge and its incentive, the same class of public promotional data as /popeyes/offers -- not scoped to any signed-in member and does not report which quests a given account has completed or activated. step_count is how many steps make up the quest; this build does not expose each step's own purchase-requirement rules.
- **Params:** `limit` (integer, optional) — Maximum quests to return, 1-100 (default 20); `market` (string, optional) — Restaurant market: US (default) or CA; `offset` (integer, optional) — Number of quests to skip, for paging (default 0)

### `popeyes_rewards`

- **HTTP:** `GET /popeyes/rewards`
- **What:** List Popeyes Rewards' points-redemption catalog. Returns a page of Popeyes Rewards' points-redemption catalog -- menu items and combos a member can redeem directly for a fixed number of loyalty points (e.g. "600 points for Cheese Bites"), distinct from /popeyes/offers (priced deals), /popeyes/quests (challenges) and /popeyes/promotions (bonus-points campaigns). This is public CMS content, not a signed-in member's own points balance or redemption history. points is the loyalty points cost to redeem; other per-account/per-order redemption restrictions Popeyes may publish on a reward are not exposed by this endpoint.
- **Params:** `limit` (integer, optional) — Maximum rewards to return, 1-100 (default 20); `market` (string, optional) — Restaurant market: US (default) or CA; `offset` (integer, optional) — Number of rewards to skip, for paging (default 0)

## Raising Cane's (6)

### `raisingcanes_directory`

- **HTTP:** `GET /raisingcanes/directory`
- **What:** Browse the Raising Cane's store directory. Returns one level of Raising Cane's store directory tree. Omit path for the root, which lists the US states Raising Cane's operates in; pass a child's path to descend (state to cities, city to stores). Each child carries its name, path, URL and how many stores sit under that branch. A child with is_store true is a store record rather than another directory level -- pass its path to GET /raisingcanes/store. This is a directory browse, not a proximity search: use GET /raisingcanes/nearby for a radius lookup.
- **Params:** `path` (string, optional) — Directory path from a previous response's children[].path, e.g. la. Omit for the root state index.

### `raisingcanes_menu`

- **HTTP:** `GET /raisingcanes/menu`
- **What:** Get Raising Cane's full published menu. Returns Raising Cane's full published menu: every section (Combos, Tailgates, Extras, Drinks) and every item, each with its name, Raising Cane's own item description (commonly ending in a calorie count or range), and image. This is a single fixed national menu page, not a per-store or per-region menu -- it takes no parameters. Raising Cane's does not publish price on this page; pricing lives behind the separate order.raisingcanes.com ordering flow, which needs a selected store and is out of scope here.
- **Params:** _none_

### `raisingcanes_nearby`

- **HTTP:** `GET /raisingcanes/nearby`
- **What:** Find Raising Cane's stores near a coordinate, nearest first. Returns Raising Cane's restaurants within a radius of a latitude/longitude, ordered nearest first, each with its distance in miles and kilometres, address, coordinates, timezone, price tier and which pickup/delivery services it offers. This proximity result carries less detail than GET /raisingcanes/store (Raising Cane's own nearby-search key is not configured with hours or phone) -- each result's `path` chains straight into GET /raisingcanes/store for the full record. `total_in_radius` reports how many stores fall inside the radius overall, which is usually far more than one page; use `offset` to walk it. A coordinate with no Raising Cane's nearby returns an empty list rather than an error.
- **Params:** `latitude` (number, **required**) — Search center latitude; `limit` (integer, optional) — Maximum stores to return, 1-50 (default 10); `longitude` (number, **required**) — Search center longitude; `offset` (integer, optional) — Result offset for paging through total_in_radius (default 0); `radius` (integer, optional) — Search radius in miles, 1-100 (default 25)

### `raisingcanes_promotion`

- **HTTP:** `GET /raisingcanes/promotion`
- **What:** Get one Raising Cane's promotion's terms. Returns one Raising Cane's promotion's published official terms: title and official-rules text (eligibility, prize details, effective date), exactly as the promotion's own page publishes them, as separate paragraphs in publication order. Promotion paths come from GET /raisingcanes/promotions entries. A path with no promotion at it (expired, mistyped, or the empty path some index entries carry) returns a 404.
- **Params:** `path` (string, **required**) — Promotion page slug from a /raisingcanes/promotions entry's path

### `raisingcanes_promotions`

- **HTTP:** `GET /raisingcanes/promotions`
- **What:** Browse Raising Cane's promotions index. Returns Raising Cane's full promotions index: every current and past sweepstakes, giveaway, and other promotion the site links to, grouped under Raising Cane's own category headings (e.g. "Sweepstakes & Giveaways", "Lucky Promotions", "First Promotions"). Each entry's path chains into GET /raisingcanes/promotion for that promotion's full official-rules text. Some entries carry an empty path -- Raising Cane's own index links a since-expired promotion back to the homepage rather than removing the entry; treat an empty path as no longer resolvable rather than a bug.
- **Params:** _none_

### `raisingcanes_store`

- **HTTP:** `GET /raisingcanes/store`
- **What:** Get one Raising Cane's store's detail. Returns one Raising Cane's store: name, full postal address, phone, coordinates, its general weekly hours plus separately published dine-in and drive-thru hours, Raising Cane's own per-store amenity labels (e.g. DRIVE_THRU, CURBSIDE_PICKUP), which pickup/delivery services it offers, and its Google Place id. Store paths come from GET /raisingcanes/directory entries whose is_store is true. Passing a directory path here returns a 404 rather than a hollow record.
- **Params:** `path` (string, **required**) — Store path from a /raisingcanes/directory child with is_store true

## Shake Shack (4)

### `shakeshack_locations`

- **HTTP:** `GET /shakeshack/locations`
- **What:** Browse Shake Shack's store index. Returns one page of Shake Shack's store index, parsed off the single, fully server-rendered /locations page. That page carries two independent sections: an interactive map (coordinates, no structured address) and an accessible "Full List of Locations" text index (structured address, no coordinates). Each entry's source field says which section it came from -- "map" or "list" -- not a business classification; both round-trip through GET /shakeshack/store by path, which always returns full structured address and coordinates regardless of source.
- **Params:** `page` (integer, optional) — 1-based page (default 1); `page_size` (integer, optional) — Entries per page, 1-500 (default 100)

### `shakeshack_menu`

- **HTTP:** `GET /shakeshack/menu`
- **What:** Get one Shake Shack location's full menu. Returns one Shake Shack location's full menu as a category tree: every category and its products, with name, description, base calories, allergens, a promotional/dietary badge when published (e.g. "LIMITED TIME ONLY", "VEGETARIAN"), image, and a full customization tree (size, additions, removals, allergen flags), each choice carrying its own price and calorie delta. location_id comes from GET /shakeshack/nearby. Many items, most notably burgers, price entirely through a required size selection rather than a base price, so price is commonly 0 for those items -- the real price lives on the size modifier's own choices.
- **Params:** `location_id` (integer, **required**) — Location id from /shakeshack/nearby

### `shakeshack_nearby`

- **HTTP:** `GET /shakeshack/nearby`
- **What:** Find Shake Shack locations near a coordinate. Returns Shake Shack locations within a radius of a coordinate, nearest first, using Shake Shack's own Olo-backed ordering API (a separate source from GET /shakeshack/locations, which reads the main site's store directory instead). Each result carries location_id, real-time weekly hours, which fulfillment modes are currently enabled (dine-in, pickup, delivery, curbside, drive-thru, walk-up, drive-up), and Shake Shack's own delivery fee schedule. Pass location_id to GET /shakeshack/menu for that location's full menu.
- **Params:** `latitude` (number, **required**) — Search center latitude; `limit` (integer, optional) — Maximum locations to return, 1-50 (default 10); `longitude` (number, **required**) — Search center longitude; `radius` (integer, optional) — Search radius in miles, 1-50 (default 15)

### `shakeshack_store`

- **HTTP:** `GET /shakeshack/store`
- **What:** Get one Shake Shack store's detail. Returns one Shake Shack store: postal address, coordinates, phone (when published), a Monday-first week of opening hours (omitted for a location that publishes no schedule, seen on venue/kiosk-shaped locations such as inside a stadium), and the order types Shake Shack publishes for it, e.g. "Dine In", "Delivery". Store paths come from GET /shakeshack/locations, either the aliased "location/<slug>" form or the legacy "node/<id>" form -- both resolve to the same record, and the response's own path field always reports the canonical alias. A path with neither shape, or one that does not resolve to a real store page, returns a 404.
- **Params:** `path` (string, **required**) — Store path from a /shakeshack/locations entry

## Sonic (12)

### `sonic_availability`

- **HTTP:** `GET /sonic/availability`
- **What:** List a Sonic Drive-In restaurant's order-ahead time slots. Returns the bookable order-ahead windows for one Sonic Drive-In restaurant, grouped by service channel and local date. Each window has a UTC start_time and end_time. Also returns the store's timezone, how long each window lasts (slot_duration_minutes), the prep/handoff buffer before the first bookable window (lead_time_minutes), and service_types -- every channel the store supports, which is a superset of the channels that currently have windows. fulfillment selects the request method and accepts exactly `PICKUP` or `DELIVERY`; note the per-window service_type is a separate, finer vocabulary and can be `ORDER_AHEAD`, `CURBSIDE_PICKUP`, `DRIVE_THROUGH`, `STORE`, `PICKUP` or `DELIVERY`. A closed or fully-booked restaurant returns an empty channels array with total_slots 0, not an error. An unknown store_id returns 404.
- **Params:** `fulfillment` (string, optional) — Fulfillment method: PICKUP or DELIVERY. Defaults to PICKUP.; `store_id` (string, **required**) — Sonic store number, e.g. from /sonic/nearby

### `sonic_categories`

- **HTTP:** `GET /sonic/categories`
- **What:** List Sonic Drive-In menu categories. Returns Sonic Drive-In's national menu's top-level categories -- Breakfast, Value, Limited Time, Combos, Burgers, Chicken, Hot Dogs, Sandwiches, Snacks & Sides, Sweets, Tea & Coffee, Lemonades & Limeades, Sodas, Slushes, Refreshers, Wacky Pack Kids Meals and others -- each with its slug (the value GET /sonic/menu takes) and a page_count of subcategory/item pages nested under it.
- **Params:** _none_

### `sonic_deals`

- **HTTP:** `GET /sonic/deals`
- **What:** List Sonic Drive-In's current promotions. Returns the promotions currently published on Sonic Drive-In's national deals page -- each with its marketing headline, public name, description, legal terms, call-to-action label and link, and creative image. This page is not listed in Sonic's own sitemap, so GET /sonic/sitemap will never surface it. Deals are national marketing offers, not per-store pricing; there is no price field in this source. Between campaigns Sonic can publish the page with no promotions at all, which returns an empty deals array with count 0 rather than an error.
- **Params:** _none_

### `sonic_directory`

- **HTTP:** `GET /sonic/directory`
- **What:** Browse Sonic Drive-In's restaurant directory by country, state and city. Returns Sonic Drive-In's restaurant directory as a country to state to city tree, with a restaurant count at every level. Use it to discover which states and cities have restaurants before calling GET /sonic/locations or GET /sonic/nearby. Each city carries both its display name and the slug that composes into a store path. Counts here describe listed restaurants and are internally consistent (the city counts sum to total_count); GET /sonic/locations enumerates a larger set of store pages, so the two totals intentionally differ.
- **Params:** _none_

### `sonic_item`

- **HTTP:** `GET /sonic/item`
- **What:** Look up one Sonic Drive-In menu item's detail. Returns one menu page's detail: name, description, image, and a link to Sonic's site-wide nutrition/allergen guide PDF. path must be a "menu" section path with kind category, subcategory, or item from GET /sonic/sitemap (or a path copied from a GET /sonic/menu-adjacent page you already know).
- **Params:** `path` (string, **required**) — A menu page path from /sonic/sitemap (section=menu)

### `sonic_location_suggest`

- **HTTP:** `GET /sonic/location-suggest`
- **What:** Complete an address into coordinates for Sonic Drive-In store search. Completes a partial address, place, city, state or ZIP into ranked matches, each already carrying the latitude and longitude that GET /sonic/nearby takes -- so a caller can run a Sonic restaurant search from free text instead of coordinates. Each suggestion's layer describes its granularity and is one of `address`, `locality`, `state`, `postalCode` or `place`, and confidence is one of `exact`, `interpolated` or `fallback`. Results are restricted to one country (default US). A query that matches nothing returns an empty suggestions array with count 0, not an error.
- **Params:** `country` (string, optional) — ISO 3166-1 alpha-2 country code to restrict results to. Defaults to US.; `limit` (integer, optional) — Maximum suggestions, 1-25. Defaults to 5. Upstream may return fewer.; `query` (string, **required**) — Partial address, place, city, state or ZIP to complete

### `sonic_locations`

- **HTTP:** `GET /sonic/locations`
- **What:** List Sonic Drive-In restaurants with ready-made store paths. Returns Sonic Drive-In's restaurant listing one page at a time, each entry already split into its country, state, city and address parts plus a ready-made path value that GET /sonic/store takes -- so enumerating restaurants needs no path parsing. Filter by state and/or city to narrow the list; city slugs come from GET /sonic/directory. Results are sorted by path so paging is reproducible. This listing covers more store pages than GET /sonic/directory counts, since the directory counts listed restaurants while this enumerates every published store page; a filter that matches nothing returns an empty locations array with total 0, not an error. If Sonic's live store-locator service refuses the request, the list is built from Sonic's public store sitemap instead (same entry shape; it can omit stores without a published page, and source_url shows which source answered).
- **Params:** `city` (string, optional) — City slug to filter by, from /sonic/directory; `page` (integer, optional) — 1-based page number. Defaults to 1.; `page_size` (integer, optional) — Entries per page, 1-500. Defaults to 100.; `state` (string, optional) — Two-letter state or province code to filter by

### `sonic_menu`

- **HTTP:** `GET /sonic/menu`
- **What:** List one Sonic Drive-In menu category's items. Returns the items in one Sonic Drive-In menu category, each with its name and published calorie count. Category slugs come from GET /sonic/categories. Some entries are themselves a nested size/variant group (e.g. "Coffee" expands to Small/Medium/Large/Rt.44 orderable sizes) rather than a single orderable product -- there is no price or full nutrition panel in this source, only calories; see GET /sonic/item for description, image, and a link to Sonic's nutrition guide.
- **Params:** `category` (string, **required**) — Category slug from /sonic/categories

### `sonic_nearby`

- **HTTP:** `GET /sonic/nearby`
- **What:** Find Sonic Drive-In restaurants near a coordinate. Returns Sonic Drive-In restaurants within a radius of a latitude/longitude, nearest first, one page at a time. Each result carries the same detail as GET /sonic/store -- address, phone, coordinates, open/closed status, amenities, weekly hours per fulfillment channel, and delivery-provider deep links -- plus distance_miles from the search centre, so ranking or mapping results needs no follow-up call per store. Use this instead of paging GET /sonic/sitemap when you know roughly where you are looking. An area with no restaurants returns an empty stores array with total_stores 0, not an error.
- **Params:** `latitude` (number, **required**) — Latitude of the search centre, -90 to 90; `limit` (integer, optional) — Stores per page, 1-50. Defaults to 10.; `longitude` (number, **required**) — Longitude of the search centre, -180 to 180; `page` (integer, optional) — Zero-based page number. Defaults to 0.; `radius` (integer, optional) — Search radius in miles, 1-100. Defaults to 25.

### `sonic_nutrition_documents`

- **HTTP:** `GET /sonic/nutrition-documents`
- **What:** List Sonic Drive-In's official nutrition and allergen documents. Returns the nutrition, allergen and ingredient documents Sonic Drive-In publishes nationally -- the printable menu, the Spanish-language menu, the nutrition guide, allergen information, and the ingredient statement -- each with a directly fetchable URL, file name, MIME type, size in bytes, and the date it was last republished. These are the only structured nutrition source Sonic publishes; per-item macro and micronutrient values are not available anywhere on the public site, and GET /sonic/menu carries calories only. Files are large print-ready PDFs (several megabytes each), so check size_bytes before downloading.
- **Params:** _none_

### `sonic_sitemap`

- **HTTP:** `GET /sonic/sitemap`
- **What:** Browse Sonic Drive-In's menu-page or store-locator sitemap. Returns one page of Sonic Drive-In's own sitemap: section=menu lists every menu category/subcategory/item page (298 pages), section=locations lists every store-directory page (state/city/store, ~3,365 stores). Each entry's path is what GET /sonic/item (menu section) or GET /sonic/store (locations section, kind=store) takes.
- **Params:** `kind` (string, optional) — Optional. Filter by page kind. menu: index, category, subcategory, item. locations: index, state, city, store.; `page` (integer, optional) — Optional. 1-based page, default 1.; `page_size` (integer, optional) — Optional. Entries per page, 1-500, default 100.; `section` (string, **required**) — Which sitemap to read

### `sonic_store`

- **HTTP:** `GET /sonic/store`
- **What:** Look up one Sonic Drive-In restaurant by its locator path. Returns one Sonic Drive-In restaurant's address, phone, coordinates, open/closed status, amenities, weekly hours broken down per fulfillment channel (order-ahead, pickup, curbside, in-store, delivery, drive-through), and delivery-provider deep links (DoorDash, GrubHub, Uber Eats, Postmates). path must be a "locations" section, kind=store path from GET /sonic/sitemap.
- **Params:** `path` (string, **required**) — A store path from /sonic/sitemap (section=locations, kind=store)

## Starbucks (5)

### `starbucks_menu`

- **HTTP:** `GET /starbucks/menu`
- **What:** Browse the full Starbucks menu. Returns Starbucks' full menu as a category tree: top-level categories, their child categories, and every product with its product number, form, product type, sizes, default size, availability, and image. Pair a product's product_number and form with /starbucks/product to fetch full detail including nutrition. store_number optionally scopes the menu to one store, using a store number from /starbucks/stores; a store-scoped menu marks items that store does not carry with availability NotAvailableHere, while the unscoped menu reports everything as Available. market selects which country catalog to return, one of us or ca, defaulting to us; the two differ substantially (roughly 282 US products vs 253 CA, with exclusives on both sides). Only these two markets are available.
- **Params:** `market` (string, optional) — Starbucks country site to read. One of: us, ca. Defaults to us; `store_number` (string, optional) — Starbucks store number to scope availability to, e.g. 101-54

### `starbucks_nearest_store`

- **HTTP:** `GET /starbucks/nearest-store`
- **What:** Locate the closest Starbucks to a coordinate. Returns the coordinates and distance of the single closest Starbucks store to a point. Both lat and lng are required. This endpoint returns coordinates only, not store details: it is what Starbucks' own store locator uses to centre its map. Use /starbucks/stores for full store records. A point with no nearby store returns a well-formed result with found set to false rather than an error. market selects which Starbucks country site answers, one of us or ca, defaulting to us.
- **Params:** `lat` (number, **required**) — Latitude; `lng` (number, **required**) — Longitude; `market` (string, optional) — Starbucks country site to read. One of: us, ca. Defaults to us

### `starbucks_nutrition`

- **HTTP:** `POST /starbucks/product/{product_number}/{form}/nutrition`
- **What:** Recalculate nutrition for a customized Starbucks drink. Recalculates calories, fat, sugars, and protein for a customized build of a Starbucks beverage: swap the milk, change the number of espresso shots or syrup pumps, and get the real figures for that exact drink rather than the standard recipe. Starbucks only offers this for four hot espresso beverages; product_number and form must be one of 406/hot (Caffe Americano), 407/hot (Caffe Latte), 408/hot (Caffe Mocha), or 413/hot (Caramel Macchiato). Any other product returns an invalid-parameter error naming the four that work. size_sku comes from a /starbucks/product result's sizes[].sku. modifiers is the COMPLETE build, not a change-set: start from that size's default_recipe, adjust what you want, and send the whole list back; an empty list is rejected. Each modifier needs a sku, an optional quantity (defaults to 1, and is the dial that matters for countable modifiers like espresso shots), and an optional replaced_sku when substituting a pick-one slot such as the milk. This returns Starbucks' own four-value dynamic-nutrition panel, which is smaller than the full per-size panel /starbucks/product returns for the standard build.
- **Params:** `form` (string, **required**) — Product form. Only hot is supported for this endpoint; `product_number` (string, **required**) — Starbucks numeric product id. One of: 406, 407, 408, 413; `request` (object, **required**) — The size and the complete modifier build
- **REST body:** Send the value of the MCP argument `request` directly as the JSON body; do not wrap it in a `request` property.

### `starbucks_product`

- **HTTP:** `GET /starbucks/product/{product_number}/{form}`
- **What:** Get one Starbucks product with nutrition. Returns one Starbucks product's full detail: name, description, product type, image, Rewards star cost, customization options, and every size with its own nutrition panel (serving size, calories, calories from fat, and per-fact values for total fat with saturated and trans fat subfacts, cholesterol, sodium, total carbohydrates, protein, and caffeine). product_number is the numeric id from a /starbucks/menu result or a product page URL. form is that product's form; allowed values are hot, iced, single, packaged, whole-bean, and via. store_number optionally scopes availability to one store. Starbucks does not expose dollar pricing on this surface, so no price is returned; star_cost is the Rewards star cost. market selects which country catalog to resolve against, one of us or ca, defaulting to us. Each size also carries its default_recipe, the standard build, which is the required starting point for the /starbucks/product/{product_number}/{form}/nutrition endpoint. An unknown product number, or a form that product is not sold in, returns not found.
- **Params:** `form` (string, **required**) — Product form. One of: hot, iced, single, packaged, whole-bean, via; `market` (string, optional) — Starbucks country site to read. One of: us, ca. Defaults to us; `product_number` (string, **required**) — Starbucks numeric product id; `store_number` (string, optional) — Starbucks store number to scope availability to, e.g. 101-54

### `starbucks_stores`

- **HTTP:** `GET /starbucks/stores`
- **What:** Find nearby Starbucks stores worldwide. Returns Starbucks store locations near a point: store number, name, phone, full address, coordinates, weekly opening hours, amenities, and pick-up options. Either place, or both lat and lng, is required. place is free-text (city, address, or postal code) and is geocoded by Starbucks itself, so it works worldwide. market selects which Starbucks country site answers, one of us or ca, defaulting to us; this is not cosmetic even for stores, because the same store reports different operational data depending on the host. There is no filter parameter: Starbucks' own API accepts a features amenity filter but silently ignores it, so it is deliberately not offered here; filter on each store's returned amenities instead. A place Starbucks cannot resolve returns a well-formed empty result with place_not_found set to true rather than an error. The upstream returns at most 50 stores per request and supports no pagination; result_capped is true when that ceiling was reached. Store discovery works worldwide, but hours, amenities, and phone numbers are populated per market and may be absent outside the US and UK.
- **Params:** `lat` (number, optional) — Latitude, requires lng; `lng` (number, optional) — Longitude, requires lat; `market` (string, optional) — Starbucks country site to read. One of: us, ca. Defaults to us; `place` (string, optional) — Free-text city, address, or postal code, geocoded by Starbucks

## Subway (6)

### `subway_available_times`

- **HTTP:** `GET /subway/available-times`
- **What:** Get one Subway store's available pickup times. Returns one Subway store's forward-looking pickup schedule -- every time slot the store is currently accepting orders for, as RFC3339 UTC instants, earliest first. Slots begin at the store's next orderable time (roughly half an hour out, not immediately) and run through closing, so the list reflects real remaining capacity for today rather than the store's advertised opening hours. Store IDs come from a GET /subway/store or GET /subway/nearby result's store_id field. A store that is closed or past its last slot for the day returns an empty slots array, which is a valid answer rather than an error. interval_minutes reports the spacing between consecutive slots as measured from the response itself.
- **Params:** `limit` (integer, optional) — Maximum slots to return (1-200). Defaults to every slot the store offers.; `store_id` (string, **required**) — Store ID from a /subway/store or /subway/nearby result's store_id

### `subway_combos`

- **HTTP:** `GET /subway/combos`
- **What:** Get one Subway store's bundle/combo categories. Returns one Subway store's bundle and combo categories with the price ranges they advertise -- min_bundled_price (cheapest as a bundle) and a_la_carte_price (cheapest bought separately). Unlike GET /subway/menu, which is US-only, this works in other markets: confirmed against US, GB and DE stores. It is NOT an itemised menu -- the upstream route behind it carries categories and prices only, with no individual products, no nutrition panels and no allergen disclosures. Use GET /subway/menu for a full itemised menu where it is available. A store with no bundles configured returns an empty categories array, which is a valid answer rather than an error. Store IDs come from a GET /subway/store or GET /subway/nearby result's store_id field.
- **Params:** `culture` (string, optional) — Preferred translation culture for display names, e.g. en-US, en-GB, de-DE. Falls back to the category's default name.; `store_id` (string, **required**) — Store ID from a /subway/store or /subway/nearby result's store_id

### `subway_menu`

- **HTTP:** `GET /subway/menu`
- **What:** Get one Subway store's full menu. Returns one Subway store's complete menu: every category, every product, and for each purchasable size (Footlong, 6-inch, etc.) its price, full nutrition panel (calories, fat, sodium, protein and more) and allergen disclosures. Store IDs come from a GET /subway/store result's store_id field. This endpoint currently covers US stores only: the menu is not available for non-US stores, which return 404 -- see GET /subway/combos for the bundle/combo categories that are available in other markets. Categories carry is_main_category: true for human-browsable menu sections (Sandwiches, Drinks, Salads, ...) and false for Subway's own internal build/customization groupings, which are included for completeness but are not meant to be shown as menu sections on their own.
- **Params:** `store_id` (string, **required**) — Store ID from a /subway/store result's store_id

### `subway_nearby`

- **HTTP:** `GET /subway/nearby`
- **What:** Search Subway stores near a coordinate or address. Returns Subway stores nearest first to a coordinate or a free-text address/city/ZIP, with live open/closed status, payment methods, catering link, and feature flags. This is the proximity search GET /subway/sitemap cannot do directly -- the sitemap enumerates the whole world for bulk scraping, this answers "what is near this point" with distance and live attributes the sitemap/store locator does not carry. Each store's store_id is the same value GET /subway/menu takes, and can be passed back here as store_id to re-read one store's live attributes directly.
- **Params:** `features` (string, optional) — Comma-separated. Restricts results to stores with ALL listed features. Allowed values: HAS_BREAKFAST, IS_REMOTEORDER_ACCEPTED, HAS_HALAL, HAS_DRIVETHROUGH, HAS_CATERING, HAS_CURBSIDE, IS_OPERATING.; `latitude` (number, optional) — Search center latitude. Set together with longitude, or set query or store_id instead -- exactly one search mode.; `limit` (integer, optional) — Maximum stores to return, 1-20 (default 10); `longitude` (number, optional) — Search center longitude.; `offset` (string, optional) — Opaque pagination cursor from a previous response's next_offset; `query` (string, optional) — Free-text address, city or ZIP to search near. Alternative to latitude/longitude and store_id.; `store_id` (string, optional) — Look up one store directly by its store_id, from GET /subway/store or a prior /subway/nearby result. Alternative to latitude/longitude and query.

### `subway_sitemap`

- **HTTP:** `GET /subway/sitemap`
- **What:** Browse Subway's global store-URL index. Returns one page of Subway's sitemap-declared store index -- 22,700+ URLs across 2 shards at time of writing, covering a country/region/city/street tree worldwide. This is the cheapest way to enumerate Subway locations. Each entry carries its URL, the locator path GET /subway/store takes, and a depth: the deepest entries are store pages, shallower ones are country, region and city directory pages listed in the same sitemap. A page past the end returns an empty list rather than an error, so a caller can walk to exhaustion.
- **Params:** `page` (integer, optional) — 1-based page within the shard (default 1); `page_size` (integer, optional) — Entries per page, 1-500 (default 100); `shard` (integer, optional) — Sitemap shard index (default 0). shard_count in the response says how many exist.

### `subway_store`

- **HTTP:** `GET /subway/store`
- **What:** Get one Subway store's detail. Returns one Subway store's detail: address, coordinates, phone (display and E.164), opening hours, and the locator's own entity profile -- IANA timezone, Google Place ID and CID for joining to Google Maps data, franchise number, price range, published services and meal types, and explicit online-ordering/catering/drive-through flags. Boolean flags are omitted entirely when the locator does not publish them, so an absent flag is not a false one. open reflects the location's published status (a store flagged closed long-term), which is distinct from whether it is currently within its opening hours. store_id is the value GET /subway/menu and GET /subway/available-times take. Paths come from a GET /subway/sitemap entry.
- **Params:** `path` (string, **required**) — Store path from a /subway/sitemap entry

## Swiggy (4)

### `swiggy_collections`

- **HTTP:** `GET /swiggy/collections`
- **What:** List Swiggy's curated collections for a location. Returns the curated dish/cuisine collections Swiggy's own homepage surfaces for a latitude/longitude (e.g. "Idli", "Biryani", "Dosa"). Each collection's id is the value /swiggy/search's collection_id param takes to browse restaurants within it. The response also carries is_serviceable, which says whether Swiggy delivers to the requested coordinates at all: false means the coordinates are outside Swiggy's delivery coverage, so the empty collections list is a coverage answer rather than a location that simply has no curated collections.
- **Params:** `latitude` (number, **required**) — Search center latitude; `longitude` (number, **required**) — Search center longitude

### `swiggy_restaurant`

- **HTTP:** `GET /swiggy/restaurant`
- **What:** Get one Swiggy restaurant's detail. Returns one Swiggy restaurant's detail by id: name, city, area, address, postal code, coordinates, phone, cuisines, cost for two, rating and total rating count, delivery time, weekly opening hours with the current open/closed callout, plus the promotions Swiggy currently shows on that restaurant's page (headline discount, conditions, and coupon code when one is needed). Swiggy has no lighter restaurant-detail-only source -- this reads the same upstream as /swiggy/restaurant/menu, just without the menu items.
- **Params:** `latitude` (number, **required**) — Caller latitude (required by Swiggy's own menu API); `longitude` (number, **required**) — Caller longitude (required by Swiggy's own menu API); `restaurant_id` (string, **required**) — Restaurant id, from /swiggy/search's id field

### `swiggy_restaurant_menu`

- **HTTP:** `GET /swiggy/restaurant/menu`
- **What:** Get one Swiggy restaurant's menu with prices. Returns one restaurant's full menu grouped into categories, plus its restaurant summary. Every item carries a name, description, category, price, discounted_price when currently discounted, veg/non-veg flag, stock status, an image, and Swiggy's own per-dish rating and review count where it carries one. A category nested under a parent group on the live site (e.g. "Whopper" under "Burgers, Wraps & Tacos") is flattened to one level: its title is the parent's, with subcategory set to its own name. The response also carries the restaurant's current promotions in offers, the same block /swiggy/restaurant returns.
- **Params:** `latitude` (number, **required**) — Caller latitude (required by Swiggy's own menu API); `longitude` (number, **required**) — Caller longitude (required by Swiggy's own menu API); `restaurant_id` (string, **required**) — Restaurant id, from /swiggy/search's id field

### `swiggy_search`

- **HTTP:** `GET /swiggy/search`
- **What:** Search Swiggy restaurants near a location. Returns restaurants delivering to a latitude/longitude, optionally filtered by a keyword or browsed within a curated collection. With no query and no collection_id this browses the nearby-restaurant listing; with a query it runs a keyword search across restaurant names, cuisines, and dishes; with a collection_id (from /swiggy/collections) it browses restaurants within that curated collection. query and collection_id are mutually exclusive. Keyword search has two result tabs, selected with tab: dish (the default) returns restaurants that serve a matching dish, each with the matching dishes, their prices, and Swiggy's own per-dish rating where it has one, in a dishes array; restaurant returns restaurants whose own name or cuisine matches, a wider set with no dishes. tab, veg, min_rating and offers are only valid together with query. sort works with either query (relevance, delivery_time, rating) or collection_id (those three plus cost_low_to_high and cost_high_to_low), and is rejected on a plain nearby browse. Each restaurant carries its id (the value the restaurant and menu endpoints take), name, cuisines, cost for two, rating, delivery time, open/closed status, a hero image, and, where one is shown, an external_rating block with the third-party aggregate score, count, and source. Where the result card advertises a promotion it also carries offers, the same title/description/tag shape /swiggy/restaurant returns (a listing card never carries a coupon code, and a card showing both a discount and a separate free-delivery benefit returns them as two entries). is_promoted is present and true only for a result Swiggy itself labels a sponsored placement rather than an organic one. unavailable_message is present only when Swiggy says the restaurant cannot currently be ordered from and carries its own reason; it is not the inverse of is_open, since Swiggy reports a restaurant as open while still refusing orders for the requested location. A plain nearby browse also returns is_serviceable, which says whether Swiggy delivers to the requested coordinates at all: false means the coordinates are outside Swiggy's delivery coverage, so the empty restaurants list is a coverage answer rather than a no-matches answer, while an empty list without the field means no matches in a served area. It is omitted on keyword search and on a collection_id browse, neither of which carries Swiggy's own coverage marker.
- **Params:** `collection_id` (string, optional) — Optional curated collection id from /swiggy/collections's id field. Browses restaurants within that collection instead of the plain nearby listing. Mutually exclusive with query.; `latitude` (number, **required**) — Search center latitude; `longitude` (number, **required**) — Search center longitude; `min_rating` (number, optional) — Only return restaurants rated at or above this score (0-5). Only valid together with query.; `offers` (boolean, optional) — Only return restaurants currently running an offer. Only valid together with query.; `offset` (string, optional) — Opaque pagination cursor from a prior response's next_offset (not meaningful when query is set); `query` (string, optional) — Optional keyword to search restaurants and dishes by, at least 2 characters. Mutually exclusive with collection_id.; `sort` (string, optional) — Optional sort order. With query: relevance, delivery_time, rating. With collection_id: those three plus cost_low_to_high and cost_high_to_low. Not valid on a plain nearby browse.; `tab` (string, optional) — Which keyword-search result tab to read: dish (default, restaurants serving a matching dish, each with a dishes array) or restaurant (restaurants whose own name/cuisine matches). Only valid together with query.; `veg` (boolean, optional) — Only return vegetarian results: veg dishes on tab=dish, pure-veg restaurants on tab=restaurant. Only valid together with query.

## TacoBell (8)

### `taco_bell_app_menu`

- **HTTP:** `GET /taco-bell/app-menu`
- **What:** Get one Taco Bell restaurant's full app-ordering catalog, combos included. Returns one Taco Bell US restaurant's complete app-ordering catalog by store number: every category, every individually orderable product, AND every combo (kind "bundle") it carries. This is the only endpoint in this family that publishes combos at all -- each one resolved down to its full slot composition (choices[], each with min/max selections and the product codes it defaults to when not customized), not just a name and price. Also returns the store's named ordering windows (dayparts) and, per item, which dayparts it is orderable in. Store numbers come from GET /taco-bell/stores.
- **Params:** `store_number` (string, **required**) — Taco Bell store number, from /taco-bell/stores

### `taco_bell_categories`

- **HTTP:** `GET /taco-bell/categories`
- **What:** List Taco Bell menu categories. Returns Taco Bell's US menu categories -- 17 at time of writing, including tacos, burritos, quesadillas, nachos, bowls, breakfast, drinks, snacks-sweets, specialties, party-packs, vegetarian, boxes-and-combos and the value menus. Each entry's slug is the value GET /taco-bell/menu takes. A category flagged hidden_from_menu is one Taco Bell does not surface in its own navigation; it is still fetchable. Takes no parameters.
- **Params:** _none_

### `taco_bell_menu`

- **HTTP:** `GET /taco-bell/menu`
- **What:** List one Taco Bell menu category's items with prices and calories. Returns the items in one Taco Bell US menu category, each with its product code, name, price, calorie count, product and food type, image, and flags for whether it is customizable, has a meatless variant, and is currently available in store. Category slugs come from GET /taco-bell/categories, and the endpoint accepts either the bare slug (`tacos`) or the full path form (`/food/tacos`). Taco Bell is one of the few brands publishing both price and calories in the same payload.
- **Params:** `category` (string, **required**) — Category slug from /taco-bell/categories

### `taco_bell_nutrition`

- **HTTP:** `GET /taco-bell/nutrition`
- **What:** Get one Taco Bell menu item's full nutrition panel, allergens and ingredients. Returns the complete nutrition-facts panel for one Taco Bell US menu item -- fats (total, saturated, trans, poly- and monounsaturated), cholesterol, sodium, potassium, carbohydrates, fiber, sugars including added sugars, protein, and the vitamin and mineral figures -- plus serving size and weight and the item's declared allergens. Values are unrounded as published, in the panel's own units: grams for fats, carbohydrates and protein, milligrams for cholesterol, sodium, potassium, calcium, iron and caffeine, and micrograms for vitamin D. This goes well beyond the calorie count on /taco-bell/menu and /taco-bell/product, which is all the menu pages themselves carry. The full component-by-component ingredient statement is available via include_ingredients; it runs to several kilobytes per item, so it is off by default.
- **Params:** `category` (string, **required**) — Category slug from /taco-bell/categories; `include_ingredients` (boolean, optional) — Include the full ingredient statement (default false -- it is long); `product` (string, **required**) — Product slug, the last segment of a /food/{category}/{product} URL

### `taco_bell_product`

- **HTTP:** `GET /taco-bell/product`
- **What:** Get one Taco Bell menu item's full detail, including its customization matrix. Returns one Taco Bell US menu item in full: product code, name, description, price, rounded and unrounded calorie counts, every published image rendition, and cross-sell/upsell references. The distinguishing part is `customizations` -- the option groups the item accepts (proteins, included ingredients, add-ons, sauces, shells, upgrades, and Supreme/Fresco add and remove sets), each option carrying its own calorie delta and add-on price. Calorie deltas can be negative, since the Fresco style replaces sauces. Slugs come from GET /taco-bell/menu, and both the bare slug and the full path form are accepted.
- **Params:** `category` (string, **required**) — Category slug from /taco-bell/categories; `product` (string, **required**) — Product slug, the last segment of a /food/{category}/{product} URL

### `taco_bell_store`

- **HTTP:** `GET /taco-bell/store`
- **What:** Get one Taco Bell restaurant's full record, including the whole week's hours and dayparts. Returns one Taco Bell US restaurant by store number: address and coordinates, phone, open status, timezone, delivery and online-ordering state, Taco Bell's per-store capability flags, mobile-pickup status and geofencing radius. Where GET /taco-bell/stores gives only today's window for each nearby restaurant, this returns the full published week, Monday-first, and each day's dayparts. Dayparts matter for ordering: Taco Bell's menu availability is daypart-scoped, so breakfast items and Balance Of Day items are orderable in different windows of the same day. Store numbers come from GET /taco-bell/stores.
- **Params:** `store_number` (string, **required**) — Taco Bell store number, from /taco-bell/stores

### `taco_bell_store_menu`

- **HTTP:** `GET /taco-bell/store-menu`
- **What:** Get one Taco Bell restaurant's full live catalog in a single call. Returns one Taco Bell US restaurant's entire menu -- every category and item in one call, each with its price, calories, product and food type, image, and whether it is currently carried and displayed at THIS store. Where GET /taco-bell/menu returns one category's items from the national default catalog, this is store-scoped: some items are absent or hidden at some restaurants, and this is the only endpoint that shows that per store. Also returns the store's current happy-hour discount window, published nowhere else in this family. The response can be cached at the edge for up to 24 hours, so treat it as a recent snapshot of what the store carries rather than a live per-second signal; for a store's serving-time windows (breakfast vs. Balance Of Day, etc.) use GET /taco-bell/store instead. Store numbers come from GET /taco-bell/stores.
- **Params:** `store_number` (string, **required**) — Taco Bell store number, from /taco-bell/stores

### `taco_bell_stores`

- **HTTP:** `GET /taco-bell/stores`
- **What:** Find Taco Bell restaurants near a location. Returns Taco Bell US restaurants near a latitude/longitude, ordered by distance. Each store carries its store number, full postal address with coordinates, phone, distance, open status, timezone, today's published opening and closing hours, and Taco Bell's own per-store capability flags (breakfast, drive-thru, delivery, mobile ordering, open late, pickup shelves, Live Mas Cafe, online). A coordinate with no Taco Bell nearby returns an empty list rather than an error.
- **Params:** `latitude` (number, **required**) — Search center latitude; `longitude` (number, **required**) — Search center longitude; `page` (integer, optional) — 0-based page index (default 0); `page_size` (integer, optional) — Stores per page, 1-50 (default 10)

## Whataburger (2)

### `whataburger_sitemap`

- **HTTP:** `GET /whataburger/sitemap`
- **What:** Browse Whataburger's store-URL index. Returns one page of Whataburger's sitemap-declared store index -- about 3,950 URLs at time of writing. Unlike some other store locators in this API, Whataburger publishes a single flat sitemap file rather than a sharded index. Each entry carries a kind: "store" is a restaurant's canonical detail page, "curbside" and "delivery" are separate pages Whataburger publishes for that same restaurant's curbside or delivery service, and "directory" is a state- or city-level listing page with no address of its own. Filter with kind to enumerate one page variant. A page past the end returns an empty list rather than an error, so a caller can walk to exhaustion.
- **Params:** `kind` (string, optional) — Filter by page kind. One of store, curbside, delivery, directory. Default all.; `page` (integer, optional) — 1-based page (default 1); `page_size` (integer, optional) — Entries per page, 1-500 (default 100)

### `whataburger_store`

- **HTTP:** `GET /whataburger/store`
- **What:** Get one Whataburger store's detail. Returns one Whataburger store: postal address, coordinates, phone, published week of opening hours, the restaurant services (curbside, delivery) Whataburger lists for it, and a per-channel hours breakdown (dine-in, drive-thru, curbside, delivery) where the channel's hours genuinely differ from the store's top-level hours. Store paths come from GET /whataburger/sitemap -- a store's canonical, curbside and delivery page paths all describe the same physical restaurant and return the same address; the response's own path field always reports the canonical page. Passing a state or city directory path returns a 404 rather than a hollow record. Note there is no menu source, so this family is a locator only.
- **Params:** `path` (string, **required**) — Store path from a /whataburger/sitemap entry

## Wingstop (6)

### `wingstop_delivery_store`

- **HTTP:** `GET /wingstop/delivery-store`
- **What:** Find the Wingstop store that delivers to an address. Given a delivery address, returns the single Wingstop store that will deliver there, plus its drive time. Returns 404 when no Wingstop store delivers to that address. The returned slug can be passed directly as GET /wingstop/menu's path with service_mode=delivery.
- **Params:** `address1` (string, **required**) — Delivery address line 1; `city` (string, **required**) — Delivery address city; `country_code` (string, optional) — Delivery address country code. Defaults to US.; `latitude` (number, **required**) — Delivery address latitude; `longitude` (number, **required**) — Delivery address longitude; `postal_code` (string, **required**) — Delivery address postal code; `state` (string, **required**) — Delivery address state (region)

### `wingstop_directory`

- **HTTP:** `GET /wingstop/directory`
- **What:** Browse the Wingstop store directory. Returns one level of Wingstop's store directory tree. Omit path for the root, which lists the single US country node; descend country to states, states to cities, cities to stores. Each child carries its name, path, url and kind (country, state, city, or store). A child with is_store true (kind store) is a store record rather than another directory level -- pass its path to GET /wingstop/store.
- **Params:** `path` (string, optional) — Directory path from a previous response's children[].path, e.g. us/tx. Omit for the root.

### `wingstop_flavors`

- **HTTP:** `GET /wingstop/flavors`
- **What:** Get Wingstop's flavor catalog. Returns Wingstop's full sauce and dry-rub flavor catalog: name, description, image, a 0 (no heat) to 5 (hottest) heat scale, whether it's a dry rub or wet sauce, and new/popular/limited-time badges. Includes retired flavors (is_active false) still present in Wingstop's own feed.
- **Params:** _none_

### `wingstop_menu`

- **HTTP:** `GET /wingstop/menu`
- **What:** Get one Wingstop store's priced menu. Returns one Wingstop store's full priced, categorized menu for carryout or delivery: every category, each listing's variants (a standalone item has one variant; a size/flavor family such as "6 pc Wing Combo" has one variant per size or preparation) with price, description and calorie range, plus store-level pricing context (currency, tax rate, prep lead time). Store paths come from GET /wingstop/directory entries whose is_store is true, or a GET /wingstop/store response's own path.
- **Params:** `path` (string, **required**) — Store path from a /wingstop/directory child with is_store true, or a /wingstop/store response's own path; `service_mode` (string, optional) — One of: carryout, delivery. Defaults to carryout.

### `wingstop_nearby`

- **HTTP:** `GET /wingstop/nearby`
- **What:** Search Wingstop stores near a coordinate. Returns Wingstop stores within a radius of a coordinate, sorted nearest first, with enough detail per store (address, phone, general hours, fulfillment channels) that a follow-up GET /wingstop/store call is often unnecessary. Each result's slug can be passed directly as GET /wingstop/menu's path.
- **Params:** `latitude` (number, **required**) — Search center latitude; `longitude` (number, **required**) — Search center longitude; `radius` (integer, optional) — Search radius in miles, 1-100. Defaults to 20.

### `wingstop_store`

- **HTTP:** `GET /wingstop/store`
- **What:** Get one Wingstop store's detail. Returns one Wingstop store: name, full postal address, phone, coordinates, its general weekly hours plus a per-channel breakdown (pickup, delivery, takeout, drive-through), which pickup/delivery services it offers, its operating status, price tier and Google Place id. Store paths come from GET /wingstop/directory entries whose is_store is true. Passing a directory path here returns a 404 rather than a hollow record.
- **Params:** `path` (string, **required**) — Store path from a /wingstop/directory child with is_store true

## Wolt (8)

### `wolt_cities`

- **HTTP:** `GET /wolt/cities`
- **What:** List every city Wolt operates in, with coordinates. Returns Wolt's own live directory of every city it operates in, each with the coordinate pair the rest of the Wolt endpoints take, plus its slug, country codes, and timezone. Every other Wolt endpoint is resolved purely from a coordinate, so this is the discovery step that makes them usable without an external geocoder. Optionally restrict to one country, or pass a reference coordinate to have each city carry its distance and the list returned nearest-first.
- **Params:** `country` (string, optional) — Optional ISO 3166-1 country code to restrict the directory to, alpha-2 (FI) or alpha-3 (FIN), case-insensitive.; `latitude` (number, optional) — Optional reference latitude. Must be given together with longitude.; `longitude` (number, optional) — Optional reference longitude. Must be given together with latitude.

### `wolt_collections`

- **HTTP:** `GET /wolt/collections`
- **What:** Get Wolt's curated homepage restaurant/store collections for a location. Returns Wolt's own curated homepage restaurant/store lists for a location (e.g. top-rated, newest, hot-this-week -- whichever collections Wolt's own ops team currently curates for that market), read from Wolt's anonymous homepage endpoint. Each restaurant carries the same fields /wolt/search returns. The response also carries is_serviceable, which says whether Wolt delivers to the requested coordinates at all: false means the coordinates are outside Wolt's delivery coverage, so the empty collections list is a coverage answer rather than a served location whose homepage happens to carry no curated lists.
- **Params:** `latitude` (number, **required**) — Search center latitude; `longitude` (number, **required**) — Search center longitude

### `wolt_restaurant`

- **HTTP:** `GET /wolt/restaurant`
- **What:** Get one Wolt restaurant or store's detail. Returns one Wolt restaurant or store's public detail by its slug: name, address, coordinates, timezone, phone, website, rating, currency, price range, cuisine tags, category ids (the values /wolt/search's category parameter accepts), opening hours, delivery hours, delivery methods, pickup availability, order minimum, and service fee estimate.
- **Params:** `slug` (string, **required**) — Wolt restaurant/store slug, from /wolt/search's slug field

### `wolt_restaurant_availability`

- **HTTP:** `GET /wolt/restaurant/availability`
- **What:** Get one Wolt restaurant or store's live availability and delivery estimate. Returns one restaurant/store's live availability for a delivery coordinate: whether it is open and online right now, the next open and close times, delivery and pickup time estimates in minutes, the delivery fee, the order minimum, the venue's distance, and any discount campaign labels Wolt currently shows on its public page. Coordinates are optional but change the answer materially -- Wolt resolves delivery availability, the fee, the estimate, and the distance against them; without coordinates the venue's generic, location-independent status is returned and delivery_method_default is UNAVAILABLE.
- **Params:** `latitude` (number, optional) — Optional delivery-address latitude. Must be given together with longitude.; `longitude` (number, optional) — Optional delivery-address longitude. Must be given together with latitude.; `slug` (string, **required**) — Wolt restaurant/store slug, from /wolt/search's slug field

### `wolt_restaurant_menu`

- **HTTP:** `GET /wolt/restaurant/menu`
- **What:** Get one Wolt restaurant or store's menu. Returns one restaurant/store's menu grouped into categories, plus its restaurant summary. Each item carries a name, description, price, dietary tags, and image, read from Wolt's own anonymous menu API in a single call. The response's loading_strategy field reports whether the items are included: full means every category carries its items, while partial means Wolt does not bulk-load this venue's assortment, so the categories come back real but with empty item lists and the venue's items are reachable only by keyword through /wolt/restaurant/menu/search. Large stores of any type -- supermarkets, pharmacies, drugstores, DIY and toy stores -- are commonly partial; restaurants are full.
- **Params:** `slug` (string, **required**) — Wolt restaurant/store slug, from /wolt/search's slug field

### `wolt_restaurant_menu_search`

- **HTTP:** `GET /wolt/restaurant/menu/search`
- **What:** Search one Wolt restaurant or store's menu by keyword. Searches one restaurant's or store's own items by keyword, using Wolt's own in-venue item search. This is the only way to reach the items of a large grocery or retail store: /wolt/restaurant/menu returns those venues' categories with no items, because Wolt itself only loads such an assortment a slice at a time. Matching works across languages, so an English keyword finds locally-named products. Each item carries a name, description, price, dietary tags, image, and -- for packaged retail products -- a barcode, pack size, and per-unit comparison price. A keyword is required; a no-match keyword returns an empty item list rather than an error.
- **Params:** `limit` (integer, optional) — Max items returned. Defaults to 30, maximum 100.; `query` (string, **required**) — Keyword to match against this venue's own item names and descriptions; `slug` (string, **required**) — Wolt restaurant/store slug, from /wolt/search's slug field

### `wolt_search`

- **HTTP:** `GET /wolt/search`
- **What:** Search Wolt restaurants and stores near a coordinate. Returns restaurants and stores near a coordinate, optionally filtered by a keyword or browsed by category. With none of those, this reads Wolt's own plain location browse; with a query it uses Wolt's own keyword search across restaurant/store names, dishes, and cuisines; with a category it browses Wolt's own per-category listing (the same page a homepage cuisine tile links to) -- call /wolt/search/filters for the current, complete, location-scoped list of valid category values. category and query cannot be combined. A keyword search additionally accepts sort, product_line, and open_now; those three apply to keyword search only and return a 400 without query. Each result carries its slug (the value the restaurant and menu endpoints take), name, address, coordinates, tags, price range, rating, and delivery estimate; the two browse modes additionally carry each venue's own category ids. The response also carries is_serviceable, which says whether Wolt delivers to the requested coordinates at all: false means the coordinates are outside Wolt's delivery coverage, so the empty results list is a coverage answer rather than a no-matches answer. A keyword that simply matches nothing inside a covered area returns an empty list with is_serviceable true. Call /wolt/cities for the coordinates of every city Wolt operates in.
- **Params:** `category` (string, optional) — Optional Wolt category id to browse by instead of a keyword search, e.g. pizza, sushi, vegan. Call /wolt/search/filters for the current, complete, location-scoped list of valid values. Cannot be combined with query. A value Wolt does not recognize at all returns a 404; a real category this particular market does not use returns an empty list, since the taxonomy is location-scoped and markets differ.; `latitude` (number, **required**) — Search center latitude; `limit` (integer, optional) — Max restaurants/stores returned. Defaults to 30, maximum 100.; `longitude` (number, **required**) — Search center longitude; `open_now` (boolean, optional) — When true, restrict results to venues currently delivering. Only applies together with query.; `product_line` (string, optional) — Optional store-type filter. Only applies together with query. Which store types a market actually stocks varies by country; one absent from the searched market returns no results rather than an error.; `query` (string, optional) — Optional keyword to search restaurant/store names, dishes, or cuisines by. Cannot be combined with category.; `sort` (string, optional) — Optional result ordering. Only applies together with query -- Wolt exposes sorting on its keyword search only, not on its plain browse or category listings.

### `wolt_search_filters`

- **HTTP:** `GET /wolt/search/filters`
- **What:** Get Wolt's live search category catalog for a location. Returns the current, location-scoped catalog of every value /wolt/search's category parameter accepts, each with a live restaurant count when Wolt's own homepage currently features that category as one of its curated tiles -- the same data Wolt's own search page's cuisine tiles are populated from.
- **Params:** `latitude` (number, **required**) — Search center latitude; `longitude` (number, **required**) — Search center longitude

## Zomato (6)

### `zomato_cities`

- **HTTP:** `GET /zomato/cities`
- **What:** List Zomato's curated directory of major cities. Returns Zomato's own curated directory of major Indian cities -- the discovery source for the city value used by zomato-search, zomato-restaurant, zomato-restaurant-menu, zomato-collections, and zomato-collection. This is Zomato's own "popular locations" directory, not an exhaustive list of every city Zomato serves -- some smaller markets resolve to a real Zomato city page without appearing here. A city slug from a caller's own prior knowledge (a restaurant URL's first path segment) can still be valid even if this endpoint does not return it.
- **Params:** `q` (string, optional) — Case-insensitive substring match against a city's name or slug. Omit to list every city in the directory.

### `zomato_collection`

- **HTTP:** `GET /zomato/collection`
- **What:** Get one Zomato curated collection's restaurant list. Returns one Zomato curated collection's restaurant list (name, cuisines, locality, rating, and headline review count where Zomato's own response includes them). Reads the same underlying page-render source as /zomato/restaurant and /zomato/restaurant/menu, pointed at the collection's own page instead of a restaurant's.
- **Params:** `url` (string, **required**) — Canonical public Zomato collection URL, from /zomato/collections's url field

### `zomato_collections`

- **HTTP:** `GET /zomato/collections`
- **What:** List Zomato's curated restaurant collections for a city. Returns Zomato's own curated "best of" restaurant collections for a city (e.g. "Best pubs & bars", "Iconic restaurants", "Insta-worthy spots") -- distinct editorial groupings of restaurants, not a keyword/geo search. Each collection's url is the value /zomato/collection takes. Zomato curates collections for larger cities only; a real city it curates none for returns a 404.
- **Params:** `city` (string, **required**) — Zomato public city slug, e.g. \

### `zomato_restaurant`

- **HTTP:** `GET /zomato/restaurant`
- **What:** Get one Zomato restaurant's detail. Returns one Zomato restaurant's public detail by its canonical URL: name, address, locality, city, postcode, coordinates, phone, cuisines, headline rating plus Zomato's separate dining and delivery rating aggregates, the full weekly opening-hours table, open/closed and delivery-only/dark-kitchen status, and delivery metadata (ETA, minimum order, pickup availability). Zomato has no lighter restaurant-detail-only source -- this reads the same upstream as /zomato/restaurant/menu, just without the menu items.
- **Params:** `url` (string, **required**) — Canonical public Zomato restaurant URL, from /zomato/search's url field

### `zomato_restaurant_menu`

- **HTTP:** `GET /zomato/restaurant/menu`
- **What:** Get one Zomato restaurant's menu. Returns one restaurant's menu grouped into categories, plus its restaurant summary. A category is named by Zomato's own sub-heading when it has one (e.g. "Veg Burgers") and otherwise by the menu section it sits under (e.g. "Burgers"), since most restaurants name only the section level. Each item carries a name, description, veg/non-veg flag, image, and price when Zomato's own anonymous response includes one -- confirmed live, item prices are commonly gated behind login for the delivery-ordering flow, so price is frequently absent even though the item itself is public.
- **Params:** `url` (string, **required**) — Canonical public Zomato restaurant URL, from /zomato/search's url field

### `zomato_search`

- **HTTP:** `GET /zomato/search`
- **What:** Search Zomato restaurants in a city. Returns restaurants in a Zomato city, optionally filtered by a keyword. With no query this reads Zomato's own city-wide delivery listing, which pages through an opaque cursor (~12 restaurants per page: pass a response's next_cursor back as cursor until has_more is false, which marks the end of the city's listing) and accepts Zomato's own sort and Pure Veg filters; with a query it uses Zomato's own keyword search across restaurant names, dishes, and cuisines, which returns a single unpaginated result set. Each restaurant carries its url (the value the restaurant and menu endpoints take), name, cuisines, cost for two, rating, distance from the city location, delivery time, whether Zomato currently delivers from it, whether the placement is promoted (sponsored), and — on the plain city-wide listing — Zomato's own headline offer badges.
- **Params:** `city` (string, **required**) — Zomato public city slug, e.g. \; `cursor` (string, optional) — Opaque pagination cursor from a previous city-wide listing response's next_cursor. Carries its own sort/pure_veg selection, so pass it on its own.; `pure_veg` (boolean, optional) — When true, restricts the city-wide listing to restaurants Zomato itself marks Pure Veg (used only when query is omitted); `query` (string, optional) — Optional keyword to search restaurant names, dishes, or cuisines by. Omit for the plain city-wide delivery listing.; `sort` (string, optional) — Sort order for the city-wide listing (used only when query is omitted)

## Wendys (10)

### `wendys_categories`

- **HTTP:** `GET /wendys/categories`
- **What:** List Wendy's national menu categories. Returns every category on Wendy's national (restaurant-agnostic) menu, grouped by which of Wendy's own top-level day-parts (Lunch/Dinner, Breakfast) it appears under -- a few categories such as Coffee and Beverages appear under both. No restaurant selection is required; this is the same catalog a signed-out visitor sees before ever picking a location. Each category's slug is what GET /wendys/menu takes.
- **Params:** _none_

### `wendys_directory`

- **HTTP:** `GET /wendys/directory`
- **What:** Browse the Wendy's store directory. Returns one level of Wendy's store directory tree. Omit path for the root, which lists Canada and the United States; pass a child's path to descend (country to states, state to cities, city to stores -- a single-store city links directly to its store page one level early). Each child carries its name, path, URL and, at the country/state/city levels, how many stores sit under that branch. A child with is_store true is a store page rather than another directory level -- pass its path to GET /wendys/store.
- **Params:** `path` (string, optional) — Directory path from a previous response's children[].path, e.g. united-states/oh. Omit for the root country index.

### `wendys_item`

- **HTTP:** `GET /wendys/item`
- **What:** Get one Wendy's menu item's (or combo's) detail. Returns one item's full detail. A simple item (is_combo false) returns its description, base price, calories, every size/weight variant (e.g. Small/Medium/Large fries, each with its own price and calories, with is_default marking the one Wendy's own page pre-selects), and every modifier component -- default (comes with the item), extra (a paid add-on) and required (the caller must pick one option from a named group, e.g. a salad's dressing) -- each with its own ingredient description and allergen list, since Wendy's publishes allergens per-component rather than as one whole-item field. The top-level allergens field is the union across default components and each required group's default-selected option only. A combo (is_combo true) instead returns combo_slots: its entree/side/drink composition and every product each slot can be built from, since a combo's own price and calories vary by what is chosen. A combo slot's product ids are the same items sold standalone in their own categories -- call this endpoint again on one of those for its own full component/allergen detail. Category and item slugs come from GET /wendys/categories and GET /wendys/menu.
- **Params:** `category` (string, **required**) — Category slug from /wendys/categories; `item` (string, **required**) — Item slug from /wendys/menu's items[].slug

### `wendys_menu`

- **HTTP:** `GET /wendys/menu`
- **What:** List one Wendy's menu category's items. Returns every item in one category of Wendy's national menu: id, name, slug, Wendy's own displayed price and calorie strings, whether it is a combo (its GET /wendys/item response returns combo_slots instead of components/variants), a limited-time-offer flag, and whether it has required customization (e.g. a salad's dressing choice). Category slugs come from GET /wendys/categories.
- **Params:** `category` (string, **required**) — Category slug from /wendys/categories

### `wendys_nearby`

- **HTTP:** `GET /wendys/nearby`
- **What:** Find Wendy's stores near a coordinate or address. Returns Wendy's stores within a radius of a search location, nearest first, via order.wendys.com's own restaurant-selector proximity search (the "Use Current Location" / "City, State, or Zipcode" flow at order.wendys.com's start-an-order screen) -- a materially richer, real-distance source than locations.wendys.com's classic-Yext locator (GET /wendys/directory, /wendys/store), which publishes no geosearch of its own. The search location is either a latitude/longitude pair or a free-text address query param (city/state, zip code, or full street address) that Wendy's own service geocodes server-side -- exactly one form is required; address takes priority if both are given. Each store carries its address, coordinates, phone, distance in miles, open/closed status, its published week of general and breakfast hours, and a few order-availability flags (breakfast, carry-out, mobile order, drive-thru, delivery, wifi) the ordering app itself uses to decide whether to offer the store for the current order type.
- **Params:** `address` (string, optional) — Free-text city/state, zip code, or street address to search near. An alternative to latitude/longitude -- required unless both of those are given.; `latitude` (number, optional) — Search center latitude. Required unless address is given.; `limit` (integer, optional) — Maximum stores to return, 1-50, default 25; `longitude` (number, optional) — Search center longitude. Required unless address is given.; `radius` (integer, optional) — Search radius in miles, 1-100, default 20

### `wendys_nutrition`

- **HTTP:** `GET /wendys/nutrition`
- **What:** Get one Wendy's menu item's full nutrition-facts panel. Returns one item's (or combo's) complete nutrition-facts panel -- calories, fat, cholesterol, sodium, carbohydrate, protein, vitamins and minerals -- as real numbers, plus declared allergens. A simple item's panel is for its default configuration (default bun/size, default condiments, no extras, no required-group substitutions). A combo's panel (is_combo true) is the *combined* total across every slot's default option in one request, the same way a caller building the full order would sum it themselves -- combo_selections lists which option each slot was computed for. GET /wendys/item and GET /wendys/menu only ever carry a calorie count, because that is all Wendy's own menu pages themselves publish inline; the full panel is fetched separately by Wendy's own "Nutrition" tab, and this endpoint resolves and calls that same source so a caller does not have to reverse-engineer it. A nutrient Wendy's does not publish is omitted from the response rather than reported as zero. Category and item slugs come from GET /wendys/categories and GET /wendys/menu.
- **Params:** `category` (string, **required**) — Category slug from /wendys/categories; `item` (string, **required**) — Item slug from /wendys/menu's items[].slug -- a combo slug is accepted

### `wendys_restaurant`

- **HTTP:** `GET /wendys/restaurant`
- **What:** Get one Wendy's restaurant's detail by store id. Returns one restaurant's detail looked up by its numeric store id -- the same id GET /wendys/nearby's stores[].store_id returns -- via order.wendys.com's own restaurant-selector API, rather than a locations.wendys.com Yext locator path (see GET /wendys/store, which needs a directory path instead). Publishes richer per-store data than the Yext locator: whether each fulfillment mode (carry-out, dine-in, drive-thru) is physically offered at all (not just currently open, as GET /wendys/nearby's flags reflect), plus feature flags (wifi, mobile order/pay, Coke Freestyle, digital coupons, loyalty, gift cards) and the published week of general and breakfast hours.
- **Params:** `store_id` (string, **required**) — Numeric store id, e.g. from /wendys/nearby's stores[].store_id

### `wendys_store`

- **HTTP:** `GET /wendys/store`
- **What:** Get one Wendy's store's detail. Returns one Wendy's store: name, full postal address, phone, coordinates, the published week of general restaurant hours and, separately, drive-thru hours (Wendy's often publishes these on different schedules), which third-party delivery platforms the store's own page links to, and the restaurant id and ordering URL used to start an order there. Store paths come from GET /wendys/directory entries whose is_store is true. Passing a directory path here returns a 404 rather than a hollow record.
- **Params:** `path` (string, **required**) — Store path from a /wendys/directory child with is_store true

### `wendys_store_menu`

- **HTTP:** `GET /wendys/store-menu`
- **What:** Get one Wendy's restaurant's full priced/offered menu. Returns one restaurant's own priced, offered item list -- real local pricing (including full combo bundle prices, which GET /wendys/item deliberately does not compute, since a combo's own price varies by what's chosen in each slot) and any store-specific promotional items, rather than Wendy's own generic/average national-menu listing (GET /wendys/menu, /wendys/item). A request with just a store id returns real data, no session or account required.
- **Params:** `store_id` (string, **required**) — Numeric store id, e.g. from /wendys/nearby's stores[].store_id or /wendys/restaurant's store_id

### `wendys_time_slots`

- **HTTP:** `GET /wendys/time-slots`
- **What:** Get one Wendy's restaurant's available mobile-order time slots. Returns one restaurant's available mobile-order arrival ("check-in") time slots -- the times a caller can schedule a mobile pickup order for, distinct from the restaurant's general open/close hours (GET /wendys/restaurant, /wendys/store). A request with just a store id returns real available slots, no session or account required.
- **Params:** `store_id` (string, **required**) — Numeric store id, e.g. from /wendys/nearby's stores[].store_id or /wendys/restaurant's store_id

## Zaxbys (3)

### `zaxbys_menu`

- **HTTP:** `GET /zaxbys/menu`
- **What:** Get Zaxby's national reference menu. Returns Zaxby's full national reference menu: every category and product, with description, calories, image, and a full recursive customization tree (size/protein/sauce choices, each with its own real price delta). This is national reference data, not store-priced -- most items list cost 0 because real pricing is store-specific and requires a signed-in ordering session this endpoint does not have. Many items price entirely through a required customization selection rather than a base cost, so cost 0 on an item is expected, not a bug.
- **Params:** _none_

### `zaxbys_nearby`

- **HTTP:** `GET /zaxbys/nearby`
- **What:** Find Zaxby's stores near a coordinate. Returns Zaxby's stores within a radius of a coordinate, nearest first: full address, phone, coordinates, current open status, per-channel hours (dine-in, drive-thru, carryout, pickup, delivery), and fulfillment/amenity flags. Each result's store_id pairs with GET /zaxbys/store for the same record on its own.
- **Params:** `latitude` (number, **required**) — Search center latitude; `limit` (integer, optional) — Maximum stores to return, 1-50 (default 10); `longitude` (number, **required**) — Search center longitude; `radius` (integer, optional) — Search radius in miles, 1-100 (default 25)

### `zaxbys_store`

- **HTTP:** `GET /zaxbys/store`
- **What:** Get one Zaxby's store's full detail. Returns one Zaxby's store's full detail by its store id: address, phone, coordinates, current open status, per-channel hours, and fulfillment/amenity flags. store_id comes from a GET /zaxbys/nearby result.
- **Params:** `store_id` (integer, **required**) — zapi.zaxbys.com's own numeric store id, from a /zaxbys/nearby result
