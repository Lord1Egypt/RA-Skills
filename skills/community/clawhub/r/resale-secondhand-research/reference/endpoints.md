# resale-secondhand-research — endpoint reference

> Generated from `scripts/tools.json` by `scripts/generate.mjs` — do not edit by hand.

Endpoints this skill uses, grouped by platform. Call them via `scripts/crawlora.sh` (see SKILL.md).

All paths are relative to the API base `https://api.crawlora.net/api/v1` and require the header `x-api-key: $CRAWLORA_API_KEY`. Path params like `{id}` are substituted into the URL; `GET` params go in the query string; `POST` params go in a JSON body.

**66 endpoints across 10 platform group(s).**

## Poshmark (8)

### `poshmark_brand`

- **HTTP:** `GET /poshmark/brand/{name}`
- **What:** Browse Poshmark listings by brand. Returns a page of Poshmark listings for a given brand name (e.g. Nike), the same browsing view as Poshmark's own brand pages. Pass a previous response's next_max_id back as max_id to fetch the next page.
- **Params:** `max_id` (string, optional) — Opaque pagination cursor from a previous response's next_max_id. Omit for the first page; `name` (string, **required**) — Poshmark brand name, matching the path segment of a /brand/{name} URL

### `poshmark_brands`

- **HTTP:** `GET /poshmark/brands`
- **What:** Get the full Poshmark brand directory. Returns Poshmark's full brand directory: every brand Poshmark recognizes (name, slug, logo, known aliases), not just brands with active listings for a given search or category filter. Useful for resolving a brand name to the exact value the brand/search filters expect.
- **Params:** _none_

### `poshmark_categories`

- **HTTP:** `GET /poshmark/categories`
- **What:** Get the Poshmark department/category browse taxonomy. Returns Poshmark's full department/category browse taxonomy (e.g. Women > Shoes, Men > Jackets & Coats). Each entry's path resolves directly against the category endpoint. This is reference data that changes rarely, so responses are cached.
- **Params:** _none_

### `poshmark_category`

- **HTTP:** `GET /poshmark/category/{path}`
- **What:** Browse Poshmark listings by category. Returns a page of Poshmark listings for a given category path (e.g. Women-Shoes, Men-Shirts), the same browsing view as Poshmark's own category pages. Pass a previous response's next_max_id back as max_id to fetch the next page.
- **Params:** `max_id` (string, optional) — Opaque pagination cursor from a previous response's next_max_id. Omit for the first page; `path` (string, **required**) — Poshmark category path segment, e.g. Women-Shoes, Men-Shirts

### `poshmark_closet`

- **HTTP:** `GET /poshmark/closet/{username}`
- **What:** Get Poshmark seller closet (storefront). Returns a Poshmark closet (seller storefront) page: the seller's public profile and reputation stats (followers, ratings, items sold) plus a first page of their currently available listings and total listing count. Pass a previous response's next_max_id back as max_id to fetch the next page of listings; paginated responses omit the seller profile, so fetch without max_id first to get seller fields.
- **Params:** `max_id` (string, optional) — Opaque pagination cursor from a previous response's next_max_id. Omit for the first page; `username` (string, **required**) — Poshmark seller username, the path segment of a /closet/{username} URL

### `poshmark_listing`

- **HTTP:** `GET /poshmark/listing/{id}`
- **What:** Get Poshmark listing detail. Returns a Poshmark item-detail page: the full listing (description, all photos, size/brand/condition, inventory), its seller's profile, public comments, and similar listings Poshmark itself surfaces on the same page.
- **Params:** `id` (string, **required**) — Poshmark listing id, the trailing id segment of a /listing/{slug}-{id} URL

### `poshmark_search`

- **HTTP:** `GET /poshmark/search`
- **What:** Search Poshmark listings. Searches Poshmark for clothing, shoes, and accessory listings, returning listing summaries (title, price, brand, size, condition, seller, images) plus the total matching count and an opaque pagination cursor. Pass a previous response's next_max_id back as max_id to fetch the next page.
- **Params:** `department` (string, optional) — Department filter, e.g. Women, Men, Kids; `max_id` (string, optional) — Opaque pagination cursor from a previous response's next_max_id. Omit for the first page; `query` (string, **required**) — Free-text keyword search

### `poshmark_trend`

- **HTTP:** `GET /poshmark/trend/{id}`
- **What:** Browse a Poshmark trend/showroom collection. Returns a page of Poshmark listings for a curated trend/showroom collection (e.g. "Vintage Celine Handbags"), the same browsing view as Poshmark's own trend pages. Pass a previous response's next_max_id back as max_id to fetch the next page.
- **Params:** `id` (string, **required**) — Poshmark trend/showroom id, the trailing id segment of a /trend/{slug}-{id} URL; `max_id` (string, optional) — Opaque pagination cursor from a previous response's next_max_id. Omit for the first page

## Etsy (7)

### `etsy_listing`

- **HTTP:** `GET /etsy/listing/{id}`
- **What:** Get Etsy listing detail. Returns the details of one Etsy listing by its numeric `id`: title, description, URL, price and currency, quantity, favorites, views, materials, tags, images and category. It also has the shop id and name, listing state, sold-out, customizable and digital flags, when it was made, shipping origin country, and create and update dates.
- **Params:** `id` (string, **required**) — Numeric Etsy listing id

### `etsy_listing_reviews`

- **HTTP:** `GET /etsy/listing/{id}/reviews`
- **What:** Get Etsy listing reviews. Returns buyer reviews for an Etsy listing, identified by the numeric `id`. Start from `offset` (0-based, default 0) and order with `sort` (`newest`, `oldest`, `highest_rating`, `lowest_rating` or `most_relevant`). The response has the average rating and total rating count; each review has buyer, date, rating, text, language and whether the seller replied.
- **Params:** `id` (string, **required**) — Numeric Etsy listing id; `offset` (integer, optional) — 0-based review offset; `sort` (string, optional) — Review sort order

### `etsy_search`

- **HTTP:** `GET /etsy/search`
- **What:** Search Etsy listings. Searches Etsy listings across shops for the required keywords `q`, in Etsy's default relevance order. Page with `offset` (default 0) and `limit` (default 36, max 100). The response gives the total match `count`, and each result has listing id, title, URL, image, price, shop name and rating, quantity and sold-out flag. Read `currency`, since it is not fixed to USD.
- **Params:** `limit` (integer, optional) — Page size (default 36, max 100); `offset` (integer, optional) — 0-based result offset; `q` (string, **required**) — Search keywords

### `etsy_shop`

- **HTTP:** `GET /etsy/shop/{id}`
- **What:** Get Etsy shop profile. Returns an Etsy shop profile: seller, headline, rating, and sold count. Accepts a numeric shop id or a shop name.
- **Params:** `id` (string, **required**) — Numeric Etsy shop id or shop name

### `etsy_shop_listings`

- **HTTP:** `GET /etsy/shop/{id}/listings`
- **What:** Get an Etsy shop's listings. Lists the listings in an Etsy shop, identified by the required `id` (a numeric shop id or a shop name). Narrow with `q` to filter within the shop's own catalogue, and page with `offset` (default 0) and `limit` (default 24). Each listing has its id, title, URL, image, price, currency, quantity, shop rating and sold-out flag.
- **Params:** `id` (string, **required**) — Numeric Etsy shop id or shop name; `limit` (integer, optional) — Page size (default 24); `offset` (integer, optional) — 0-based listing offset; `q` (string, optional) — Keyword filter within the shop's own catalog

### `etsy_shop_reviews`

- **HTTP:** `GET /etsy/shop/{id}/reviews`
- **What:** Get Etsy shop reviews. Returns buyer reviews for an Etsy shop, identified by the required `id` (a numeric shop id or a shop name). Page with `offset` (default 0) and `limit` (default 14). The response has the average rating and total rating count. Each review has buyer, date, rating, text, language, the reviewed listing, and whether the seller replied.
- **Params:** `id` (string, **required**) — Numeric Etsy shop id or shop name; `limit` (integer, optional) — Page size (default 14); `offset` (integer, optional) — 0-based review offset

### `etsy_shop_search`

- **HTTP:** `GET /etsy/shop/search`
- **What:** Search Etsy shops. Searches Etsy shops by the required keyword `q`, returning up to `limit` shops (default 10). Each shop has its id, name, avatar, location, active listing count, open date and a vacation-mode flag.
- **Params:** `limit` (integer, optional) — Max shops to return (default 10); `q` (string, **required**) — Shop search keyword

## Vinted (7)

### `vinted_brand`

- **HTTP:** `GET /vinted/brand`
- **What:** Vinted listings for a brand. Returns Vinted listings for a specific brand, with optional price filtering and sort order. `order` values: `relevance`, `newest_first`, `price_high_to_low`, `price_low_to_high`. Public data, sourced from Vinted's own server-rendered brand page.
- **Params:** `id` (string, **required**) — Numeric Vinted brand ID, from a /vinted/item result's brand link; `order` (string, optional) — Sort order. Allowed values: relevance, newest_first, price_high_to_low, price_low_to_high; `page` (integer, optional) — Page number, starting at 1; `price_from` (number, optional) — Minimum price; `price_to` (number, optional) — Maximum price

### `vinted_brands`

- **HTTP:** `GET /vinted/brands`
- **What:** Vinted popular-brands directory. Returns Vinted's "Popular brands" directory. This is Vinted's own curated list, not an exhaustive list of every brand in its catalog. Each entry's `id` is usable directly as the `id` query parameter to /vinted/brand. Public data, sourced from Vinted's own server-rendered brands page.
- **Params:** _none_

### `vinted_catalog`

- **HTTP:** `GET /vinted/catalog`
- **What:** Vinted listing search. Returns Vinted resale listings matching a text search, with optional price filtering and sort order. `order` values: `relevance`, `newest_first`, `price_high_to_low`, `price_low_to_high`. Public data, sourced from Vinted's own server-rendered catalog page.
- **Params:** `order` (string, optional) — Sort order. Allowed values: relevance, newest_first, price_high_to_low, price_low_to_high; `page` (integer, optional) — Page number, starting at 1; `price_from` (number, optional) — Minimum price; `price_to` (number, optional) — Maximum price; `search_text` (string, **required**) — Search text

### `vinted_categories`

- **HTTP:** `GET /vinted/categories`
- **What:** Vinted top-level catalog categories. Returns Vinted's top-level catalog categories (e.g. Women, Men, Kids, Home, Electronics, Sports, Entertainment, Hobbies & collectibles). This is the root level only -- Vinted's full category tree goes several levels deeper on the live site, but deeper levels aren't server-rendered so aren't covered here. Each entry's `id` is usable directly as the `id` query parameter to /vinted/category. Public data, sourced from Vinted's own server-rendered catalog navigation.
- **Params:** _none_

### `vinted_category`

- **HTTP:** `GET /vinted/category`
- **What:** Vinted listings for a category. Returns Vinted listings for a specific category, with optional price filtering and sort order. `order` values: `relevance`, `newest_first`, `price_high_to_low`, `price_low_to_high`. Public data, sourced from Vinted's own server-rendered category page.
- **Params:** `id` (string, **required**) — Numeric Vinted category ID, from a /vinted/item result's categories breadcrumb link; `order` (string, optional) — Sort order. Allowed values: relevance, newest_first, price_high_to_low, price_low_to_high; `page` (integer, optional) — Page number, starting at 1; `price_from` (number, optional) — Minimum price; `price_to` (number, optional) — Maximum price

### `vinted_item`

- **HTTP:** `GET /vinted/item`
- **What:** A single Vinted listing's detail. Returns a single Vinted listing's detail: title, description, brand, size, condition, material, color, price, category breadcrumb, and photos. Public data, sourced from Vinted's own server-rendered item page.
- **Params:** `id` (string, **required**) — Numeric Vinted item ID, from a /vinted/catalog result's id field

### `vinted_member`

- **HTTP:** `GET /vinted/member`
- **What:** A Vinted seller's public storefront profile. Returns a Vinted seller's public storefront profile: username, self-disclosed coarse location, rating, and follower/following counts. Deliberately excludes online-presence and activity data (last-seen timestamps, upload-frequency badges) present on the live page. Public data, sourced from Vinted's own server-rendered member page.
- **Params:** `id` (string, **required**) — Numeric Vinted member ID, from a /vinted/item result's seller link

## StockX (5)

### `stockx_brands`

- **HTTP:** `GET /stockx/brands`
- **What:** Get StockX brand catalog. Returns StockX's full brand catalog (name and URL slug for every brand in its own brand directory), suitable for building GET /stockx/search's brand parameter or GET /stockx/search's model parameter's required single-brand context.
- **Params:** _none_

### `stockx_categories`

- **HTTP:** `GET /stockx/categories`
- **What:** Get StockX category/subcategory taxonomy. Returns StockX's full category/subcategory reference: the 7 top-level categories accepted by GET /stockx/search's category parameter, each with its subcategories (e.g. Shoes -> Boots, Cleats, Clogs).
- **Params:** _none_

### `stockx_product`

- **HTTP:** `GET /stockx/product/{slug}`
- **What:** Get StockX product detail. Returns a StockX product: identity (title, brand, model, colorway, style id, retail price, release date, description, image), current market data (lowest ask, highest bid, last sale, trailing average price/sales count, delivery-speed ask tiers), individual seller listings (price, condition, size), related-product recommendations (other colorways/siblings StockX surfaces on the product page), and any promotional badges.
- **Params:** `slug` (string, **required**) — StockX product URL slug (the urlKey), the path segment of a https://stockx.com/{slug} product page

### `stockx_releases`

- **HTTP:** `GET /stockx/releases`
- **What:** Get StockX upcoming release calendar. Returns a date-ordered page (release date ascending) of StockX's upcoming release calendar: new and restocked products releasing on or after the given date, with product summaries, headline pricing, and each item's published release date.
- **Params:** `from` (string, optional) — Only include releases on or after this date (YYYY-MM-DD, UTC). Defaults to today; `limit` (integer, optional) — Results per page, defaults to 20, maximum 100; `page` (integer, optional) — 1-indexed result page, defaults to 1

### `stockx_search`

- **HTTP:** `GET /stockx/search`
- **What:** Search/browse StockX products. Browses StockX's product catalog by category with optional free-text keyword search and facet filters (gender, brand, color, shoe height, activity, availability), returning product summaries with headline pricing plus the total matching count.
- **Params:** `activity` (string, optional) — Filter by activity, comma-separated for multiple values; `available_now` (boolean, optional) — Only include products with at least one active ask; `below_retail` (boolean, optional) — Only include products currently trading below original retail price; `brand` (string, optional) — Filter by one or more brand slugs, comma-separated, e.g. jordan,nike; `category` (string, **required**) — StockX top-level category; `color` (string, optional) — Filter by color, comma-separated for multiple values; `gender` (string, optional) — Filter by gender, comma-separated for multiple values; `limit` (integer, optional) — Results per page, defaults to 20, maximum 100; `model` (string, optional) — Filter by a single model slug, e.g. air-force-1. Requires exactly one value in brand; `page` (integer, optional) — 1-indexed result page, defaults to 1; `query` (string, optional) — Free-text keyword search within the category, e.g. a model name or colorway; `shoe_height` (string, optional) — Filter by shoe height, comma-separated for multiple values; `sort` (string, optional) — Result sort order, defaults to featured; `xpress_ship` (boolean, optional) — Only include products with StockX Xpress Ship availability

## Mercari (5)

### `mercari_autocomplete`

- **HTTP:** `GET /mercari/autocomplete`
- **What:** Mercari search autocomplete. Returns Mercari's own search-suggestion list for a partial keyword, in its own relevance order. An empty suggestion list is a normal outcome for obscure or gibberish input.
- **Params:** `query` (string, **required**) — Partial keyword to get suggestions for

### `mercari_home`

- **HTTP:** `GET /mercari/home`
- **What:** Get Mercari home feed. Returns Mercari's own curated home-feed recommendations: listing summaries (title, price, thumbnail, condition, seller).
- **Params:** _none_

### `mercari_item`

- **HTTP:** `GET /mercari/item/{id}`
- **What:** Get Mercari item detail. Returns a Mercari item-detail page: description, all photos, price, condition, category, hashtags, the shipping origin state, and a "similar items" carousel of related listings.
- **Params:** `id` (string, **required**) — Mercari item id, e.g. from a search result's id field

### `mercari_master`

- **HTTP:** `GET /mercari/master`
- **What:** Get Mercari full taxonomy (categories, brands, sizes). Returns Mercari's full reference taxonomy in one call: every category (with parent linkage), every recognized brand, and every clothing/shoe/apparel size. Large (tens of thousands of brand entries) and effectively static -- cache this response rather than polling it.
- **Params:** _none_

### `mercari_search`

- **HTTP:** `GET /mercari/search`
- **What:** Search Mercari listings. Searches Mercari's live resale marketplace by free-text keyword, returning listing summaries (title, price, thumbnail, condition, seller) plus the total matching count.
- **Params:** `query` (string, **required**) — Free-text keyword search

## Depop (10)

### `depop_brands`

- **HTTP:** `GET /depop/brands`
- **What:** Depop's full brand directory. Returns Depop's full brand directory (id, name, slug), not just brands with active listings for a given search -- resolves the search endpoint's otherwise-opaque brand_ids filter to human-readable names. Public data sourced from Depop's own brand-directory API.
- **Params:** _none_

### `depop_categories`

- **HTTP:** `GET /depop/categories`
- **What:** Get Depop's category taxonomy. Returns Depop's full department, category, and subcategory taxonomy -- every value usable with /depop/search's and /depop/shop/{username}'s category/subcategory filters. Tries a live refresh from Depop's own category-filter API first and falls back to a static snapshot on any failure, so this never errors.
- **Params:** _none_

### `depop_item`

- **HTTP:** `GET /depop/item/{slug}`
- **What:** Get Depop item detail. Returns a Depop item-detail page: description, all photos, price, condition, brand, size, seller info, and a "similar items" carousel when the page has one.
- **Params:** `slug` (string, **required**) — Depop item URL slug, e.g. from a search result's id field

### `depop_item_similar`

- **HTTP:** `GET /depop/item/{slug}/similar`
- **What:** Get Depop items similar to a listing. Returns items similar to a given Depop listing, via Depop's dedicated similar-items API -- richer and paginated (up to 150 per page) compared to the small, non-paginated "similar items" carousel already included in item detail. Public data sourced from Depop's own similar-items API.
- **Params:** `after` (string, optional) — Opaque pagination cursor from a previous response's next_cursor field. Omit for the first page.; `limit` (integer, optional) — Max results per page, 1-150; `slug` (string, **required**) — Depop item URL slug, e.g. from a search result's id field

### `depop_search`

- **HTTP:** `GET /depop/search`
- **What:** Search Depop listings. Searches Depop's resale-fashion marketplace by free-text keyword, with optional price, condition, colour, category, subcategory, gender, kids-department, brand, discount, and sort filters, returning listing summaries (title, price, brand, condition, like count, photos, sizes), a pagination cursor, and the total matching count.
- **Params:** `after` (string, optional) — Opaque pagination cursor from a previous response's next_cursor field. Omit for the first page.; `brand_ids` (string, optional) — Comma-separated Depop internal numeric brand ids. Not documented by Depop -- find a brand's id by browsing its depop.com/brands/<slug>/ page.; `category` (string, optional) — Depop category slug: tops, bottoms, dresses, coats-jackets, jumpsuit-and-playsuit, suits, footwear, accessories, nightwear, underwear, swim-beach-wear, fancy-dress, sleepsuits-and-bodysuits, bundles, beauty, face-masks, home, tech-accessories, film, art, books-and-magazine, music, party-supplies, sports-equipment-accesories, toys, umbrella. See GET /depop/categories for a machine-readable enumeration with names and subcategories.; `colours` (string, optional) — Comma-separated colour filter: black, grey, white, brown, tan, cream, yellow, red, burgundy, orange, pink, purple, blue, navy, green, khaki, multi; `condition` (string, optional) — Comma-separated condition filter: brand_new, used_like_new, used_excellent, used_good, used_fair; `gender` (string, optional) — Department filter: female, male; `is_kids` (boolean, optional) — Kids-department filter: true restricts results to kids items only, false excludes them, omitted returns both.; `on_sale` (boolean, optional) — Restrict results to discounted listings; `price_max` (number, optional) — Maximum listing price in USD; `price_min` (number, optional) — Minimum listing price in USD; `query` (string, **required**) — Free-text keyword search; `sizes` (string, optional) — Comma-separated Depop size composite ids (format {size_set_id}.{id}, e.g. \; `sort` (string, optional) — Sort order: relevance, price_low_to_high, price_high_to_low; `subcategory` (string, optional) — Comma-separated Depop subcategory slug(s), scoped within category. See GET /depop/categories for the full list per category.

### `depop_search_facets`

- **HTTP:** `GET /depop/search/facets`
- **What:** Depop search result-count breakdowns. Returns result-count breakdowns per department/category/subcategory for a search query, via Depop's dedicated aggregates API -- a distinct upstream call from search itself, not embedded in its response. Public data sourced from Depop's own search-aggregates API.
- **Params:** `query` (string, **required**) — Free-text keyword search

### `depop_search_sellers`

- **HTTP:** `GET /depop/search-sellers`
- **What:** Search Depop sellers by name. Finds Depop users/sellers by name or username. A matched result's username can be passed directly to GET /depop/shop/{username} for that seller's full shop. Public data sourced from Depop's own user-search API.
- **Params:** `query` (string, **required**) — Seller name or username to search for

### `depop_shop`

- **HTTP:** `GET /depop/shop/{username}`
- **What:** Get a Depop seller's shop. Returns a Depop seller's public shop: profile (rating, sold count, followers, bio) plus current listings, with optional price, condition, colour, category, subcategory, gender, discount, and sort filters. Public data sourced from Depop's own shop pages.
- **Params:** `category` (string, optional) — Depop category slug: tops, bottoms, dresses, coats-jackets, jumpsuit-and-playsuit, suits, footwear, accessories, nightwear, underwear, swim-beach-wear, fancy-dress, sleepsuits-and-bodysuits, bundles, beauty, face-masks, home, tech-accessories, film, art, books-and-magazine, music, party-supplies, sports-equipment-accesories, toys, umbrella. See GET /depop/categories for a machine-readable enumeration with names and subcategories.; `colours` (string, optional) — Comma-separated colour filter: black, grey, white, brown, tan, cream, yellow, red, burgundy, orange, pink, purple, blue, navy, green, khaki, multi; `condition` (string, optional) — Comma-separated condition filter: brand_new, used_like_new, used_excellent, used_good, used_fair; `gender` (string, optional) — Department filter: female, male; `on_sale` (boolean, optional) — Restrict results to discounted listings; `price_max` (number, optional) — Maximum listing price in USD; `price_min` (number, optional) — Minimum listing price in USD; `sizes` (string, optional) — Comma-separated Depop size composite ids (format {size_set_id}.{id}, e.g. \; `sort` (string, optional) — Sort order: relevance, price_low_to_high, price_high_to_low, recently_listed; `subcategory` (string, optional) — Comma-separated Depop subcategory slug(s), scoped within category. See GET /depop/categories for the full list per category.; `username` (string, **required**) — Depop seller username, e.g. from a shop page URL segment

### `depop_sizes`

- **HTTP:** `GET /depop/sizes`
- **What:** Get Depop's size taxonomy. Returns Depop's full, multi-region size taxonomy -- every composite id usable with /depop/search's and /depop/shop/{username}'s sizes filter. Public data sourced from Depop's own size-filter API.
- **Params:** _none_

### `depop_suggest`

- **HTTP:** `GET /depop/suggest`
- **What:** Depop search-box autocomplete. Returns Depop's own search-box autocomplete suggestions for a partial query, including the category a suggestion maps to when relevant. Public data sourced from Depop's own search-suggestions API.
- **Params:** `query` (string, **required**) — Partial search query to autocomplete

## Whatnot (4)

### `whatnot_browse`

- **HTTP:** `GET /whatnot/browse`
- **What:** Browse Whatnot live shows by category. Returns the live and upcoming shows currently listed under a Whatnot category: seller, title, status, start time, thumbnail, and tags.
- **Params:** `category` (string, **required**) — Whatnot category slug. See GET /whatnot/categories for the full list.

### `whatnot_categories`

- **HTTP:** `GET /whatnot/categories`
- **What:** Get Whatnot's category list. Returns Whatnot's full top-level category list (e.g. "Trading Card Games", "Sneakers & Streetwear"). Each entry's slug is usable directly with /whatnot/browse's category filter.
- **Params:** _none_

### `whatnot_live`

- **HTTP:** `GET /whatnot/live/{id}`
- **What:** Get a Whatnot live show's current shop feed. Returns a Whatnot live show's current shop feed: every product, auction, and giveaway listing currently visible in the show, each with its seller's rating.
- **Params:** `id` (string, **required**) — Whatnot live show id, e.g. from a browse result's id field

### `whatnot_seller`

- **HTTP:** `GET /whatnot/seller/{username}`
- **What:** Get a Whatnot seller profile and shows. Returns public seller profile details and one page of the seller's livestreams. Use next_cursor as cursor to continue while has_more is true. The endpoint does not include shop products.
- **Params:** `cursor` (string, optional) — Opaque cursor from a prior response's next_cursor; `username` (string, **required**) — Whatnot seller username

## GOAT (10)

### `goat_collection`

- **HTTP:** `GET /goat/collection`
- **What:** Get a GOAT curated product collection. Returns a page of one of GOAT's curated product collections (an editorial rail like "top trending" or "new arrivals"), as shown in GOAT's own product-page "you may also like" rails and homepage modules. Collection slugs are not enumerable by this API -- capture one from a live GOAT page.
- **Params:** `exclude_product_ids` (string, optional) — Omit specific products by id, comma-separated; `limit` (integer, optional) — Results per page, defaults to 12, maximum 100; `page` (integer, optional) — 1-indexed result page, defaults to 1; `slug` (string, **required**) — GOAT collection slug, e.g. as seen in a curated rail on GOAT's own site

### `goat_countries`

- **HTTP:** `GET /goat/countries`
- **What:** Get GOAT countries. Returns every country GOAT recognizes -- the accepted values for GET /goat/product/{slug}'s country_code parameter -- with the currency and size unit (us, uk, eu) GOAT localizes to for each, plus whether GOAT ships and accepts returns there. Every country is listed, not only the shippable ones, because country_code localizes pricing and is accepted for all of them; filter on ships_to if you want only GOAT's shipping destinations.
- **Params:** _none_

### `goat_curated`

- **HTTP:** `GET /goat/curated`
- **What:** Get GOAT curated links. Returns the shelf of editorially curated links GOAT is currently promoting in its own search box: seasonal collections, specific product searches, and browse-all entry points. Every link is actionable against this API -- a collection link carries a value for GET /goat/collection, a search link carries a query for GET /goat/search.
- **Params:** _none_

### `goat_listings_count`

- **HTTP:** `GET /goat/listings/count`
- **What:** Get GOAT live listing count. Returns how many listings GOAT currently has live across its whole marketplace. This is the only way to see GOAT's true catalog size, because GET /goat/search's total_results saturates at 10000 on a broad query and cannot report a total above that ceiling.
- **Params:** _none_

### `goat_product`

- **HTTP:** `GET /goat/product/{slug}`
- **What:** Get GOAT product detail. Returns a GOAT product: identity/descriptive metadata (name, brand, SKU, colorway, designer, silhouette, taxonomy, materials, release date, retail price, editorial story, images, full size range, other products featured alongside it), plus live per-size/condition pricing and stock status (lowest price, GOAT Instant Ship price, last sold price, highest current buyer offer).
- **Params:** `country_code` (string, optional) — ISO 3166-1 alpha-2 country code used to localize per-size pricing, defaults to US; `slug` (string, **required**) — GOAT product URL slug, the path segment of a https://www.goat.com/sneakers/{slug} product page

### `goat_product_recommended`

- **HTTP:** `GET /goat/product/{slug}/recommended`
- **What:** Get GOAT recommended products for a product. Returns the recommended/related products GOAT's own product page shows for a given product (other colorways, similar products) -- descriptive metadata only, no live pricing.
- **Params:** `count` (integer, optional) — Number of recommended products to return, defaults to 8, maximum 24; `slug` (string, **required**) — GOAT product URL slug to find related products for

### `goat_search`

- **HTTP:** `GET /goat/search`
- **What:** Search GOAT products. Searches or browses GOAT's sneaker/streetwear/collectibles catalog by free-text query and/or facet filters (category, footwear sub-type, activity, color, gender, condition, brand, release year, price range, release-date range, silhouette, designer, in-stock/under-retail/instant-ship, curated collection), returning product summaries (brand, silhouette, category, image, stock status, headline pricing across all sizes) plus the total matching count. Query is optional -- a facet filter alone browses the catalog the same way GOAT's own category/brand pages do.
- **Params:** `activities` (string, optional) — Filter by activity (sneakers only), comma-separated for multiple values; `brands` (string, optional) — Filter by one or more brand slugs, comma-separated, e.g. air-jordan,nike. GET /goat/search/facets lists GOAT's top brands; long-tail brands are valid here even when absent from that list; `categories` (string, optional) — Filter by category, comma-separated for multiple values. See GET /goat/search/facets for the current live list; `collection_slug` (string, optional) — Scope results to a GOAT curated collection (see GET /goat/collection), combinable with query, every other filter, and sort; `colors` (string, optional) — Filter by color, comma-separated for multiple values; `conditions` (string, optional) — Filter by item condition, comma-separated for multiple values; `designers` (string, optional) — Filter by one or more designers, comma-separated, matching GOAT's own naming (see a product's designer field); `genders` (string, optional) — Filter by gender, comma-separated for multiple values; `in_stock` (boolean, optional) — Only include products currently in stock; `instant_ship` (boolean, optional) — Only include products with GOAT Instant Ship availability; `limit` (integer, optional) — Results per page, defaults to 12, maximum 100; `page` (integer, optional) — 1-indexed result page, defaults to 1; `price_cents_max` (integer, optional) — Only include results priced at or below this amount, in cents; `price_cents_min` (integer, optional) — Only include results priced at or above this amount, in cents; `product_types` (string, optional) — Filter by footwear sub-type, comma-separated for multiple values; `query` (string, optional) — Free-text search query, e.g. a model name, colorway, or style code. Optional -- omit to browse by facet filters alone; `released_after` (string, optional) — Only include products released on or after this date (YYYY-MM-DD, UTC); `released_before` (string, optional) — Only include products released on or before this date (YYYY-MM-DD, UTC); `silhouettes` (string, optional) — Filter by one or more silhouettes, comma-separated, matching GOAT's own naming (see a product's silhouette field); `sort` (string, optional) — Result sort order, defaults to relevance; `under_retail` (boolean, optional) — Only include products currently trading below original retail price; `years` (string, optional) — Filter by season year(s), comma-separated, e.g. 2025,2026. See GET /goat/search/facets for the current live list

### `goat_search_facets`

- **HTTP:** `GET /goat/search/facets`
- **What:** Get GOAT search facet values. Returns the accepted values for goat_search's filter parameters: categories, colors, genders, conditions, brands, and years are returned live so a value GOAT adds is discoverable without any client-side change, while product_types and activities are served from a maintained list because GOAT exposes no live facet for them. brands is GOAT's top brands ordered by product count, not the complete brand list -- when brands_truncated is true, brands beyond the ones listed exist and remain valid goat_search values.
- **Params:** _none_

### `goat_suggest`

- **HTTP:** `GET /goat/suggest`
- **What:** Autocomplete a GOAT search. Returns GOAT's own search-box autocomplete for a partial query: matching curated collections and matching products. The collections carry the slug values accepted by GET /goat/collection and by GET /goat/search's collection_slug parameter, making this the way to discover collection slugs.
- **Params:** `limit` (integer, optional) — Maximum curated collections to return. Defaults to 8, maximum 20. Does not affect the product count, which upstream fixes at 25; `query` (string, **required**) — Partial search text to autocomplete

### `goat_trending_searches`

- **HTTP:** `GET /goat/searches/trending`
- **What:** Get GOAT trending searches. Returns the search terms GOAT is currently surfacing as popular, in GOAT's own ranking order -- the same list its own search box shows. Each term is free text ready to pass to GET /goat/search's query parameter.
- **Params:** _none_

## Leboncoin (2)

### `leboncoin_listing`

- **HTTP:** `GET /leboncoin/listing`
- **What:** Get a Leboncoin public listing. Returns public metadata for one supplied Leboncoin ad URL. It excludes seller identity and contacts, precise location, payment, delivery, and account data.
- **Params:** `url` (string, **required**) — Canonical public ad URL returned by leboncoin-search

### `leboncoin_search`

- **HTTP:** `GET /leboncoin/search`
- **What:** Search Leboncoin public listings. Returns public listing cards from one Leboncoin location page. This endpoint excludes contacts, seller profiles, accounts, and transaction data.
- **Params:** `location` (string, **required**) — Public Leboncoin location slug

## Reverb (8)

### `reverb_categories`

- **HTTP:** `GET /reverb/categories`
- **What:** List Reverb's category/product-type taxonomy. Returns Reverb's full category/product-type taxonomy -- the value space reverb-search's own category/product_type parameters accept. product_types is a fixed, exhaustive 14-value closed set; categories is the full, exhaustive leaf-category value space as of the request (306 values as of 2026-10-15). A leaf category's slug is NOT always globally unique across product types -- always pass a category's own product_type field alongside its slug to reverb-search, not category alone, when disambiguation matters.
- **Params:** _none_

### `reverb_listing`

- **HTTP:** `GET /reverb/listing`
- **What:** Get a Reverb listing. Returns full listing-detail data for one Reverb listing: description, every photo, shipping/payment/return policies, and the seller's shop reputation -- richer than the flattened summary reverb-search returns per listing. id is the listing's numeric id, from a search result's own listings[].id field.
- **Params:** `id` (integer, **required**) — Listing id, from a search result's own listings[].id field

### `reverb_makes`

- **HTTP:** `GET /reverb/makes`
- **What:** List Reverb's manufacturer/make list. Returns Reverb's full manufacturer/make list -- the value space reverb-search's own make parameter accepts (2,795 values as of 2026-10-15). Does not include a model list -- Reverb's own /api/listings silently ignores a model filter value, so reverb-search has no Model parameter and a model list would have no corresponding filter to use it with.
- **Params:** _none_

### `reverb_price_guide`

- **HTTP:** `GET /reverb/price-guide`
- **What:** Get a gear model's Reverb Price Guide detail. Returns one gear model's Reverb Price Guide detail: its specific finish/year variants, monthly average sale-price history, and a page of individual recent sales. slug is the model's slug, from reverb-price-guide-search's own models[].slug field. canonical_product_id optionally scopes to one specific variant from this model's own canonical_products[].id field (from a prior call without it); omitting it aggregates price history and recent sales across every variant, a broader, more heavily-sampled view. condition optionally scopes by Reverb's own Price Guide condition scale (listed below) -- a separate, 6-value enum from reverb-search's own listing condition field. range selects how far back the price history/recent-sales window looks. An unknown slug returns a typed not-found error.
- **Params:** `canonical_product_id` (string, optional) — Specific finish/year variant id, from this model's own canonical_products[].id field; `condition` (string, optional) — Price Guide condition filter; `limit` (integer, optional) — Recent sales to return, defaults to 24, maximum 100; `range` (string, optional) — Date-range window, defaults to years_1; `slug` (string, **required**) — Model slug, from reverb-price-guide-search's own models[].slug field

### `reverb_price_guide_search`

- **HTTP:** `GET /reverb/price-guide-search`
- **What:** Search Reverb's Price Guide model catalog. Searches Reverb's Price Guide (reverb.com/price-guide) for gear models by free-text brand/model query (e.g. "fender stratocaster"). Each result's slug is the value reverb-price-guide's own slug parameter accepts. query is full-text relevance search, not an exact match -- unlike reverb-search's own query, a nonsensical query is not guaranteed to return an empty result; the upstream can fall back to loosely related or generically popular models instead, so a low result count should be treated cautiously rather than read as "no real matches.".
- **Params:** `limit` (integer, optional) — Results to return, defaults to 24, maximum 100; `query` (string, **required**) — Free-text brand/model search query

### `reverb_search`

- **HTTP:** `GET /reverb/search`
- **What:** Search or browse Reverb musical-instrument listings. Searches or browses Reverb's (reverb.com) marketplace for new and used musical instruments and gear. query, category, product_type, make, min_price, and max_price are all optional and combine as an AND -- a free-text query can be combined with category/product_type/make/price filters in the same request, or every field can be omitted to browse the full active catalog. category accepts a leaf slug from reverb-categories' own categories[].slug field; product_type is a fixed, closed 14-value enum (listed below) that should be passed together with category from the SAME reverb-categories entry, since a category slug alone is not always globally unique (e.g. "cables" exists under both Accessories and Home Audio). An unrecognized category value is silently ignored by the upstream (returns the unfiltered catalog, not zero results or an error) -- a known upstream quirk. make accepts a manufacturer name from reverb-makes' own makes[] field and is a confirmed, real filter. A query with genuinely zero matches returns a well-formed empty result rather than an error.
- **Params:** `category` (string, optional) — Category facet filter, from reverb-categories' own categories[].slug field -- pass together with product_type from the same entry; `limit` (integer, optional) — Results per page, defaults to 24, maximum 50 (the upstream's own silent cap); `make` (string, optional) — Manufacturer name filter, from reverb-makes' own makes[] field; `max_price` (number, optional) — Maximum price (inclusive), in USD; `min_price` (number, optional) — Minimum price (inclusive), in USD; `page` (integer, optional) — One-based page number, defaults to 1; `product_type` (string, optional) — Product-type filter; `query` (string, optional) — Free-text search query

### `reverb_shop`

- **HTTP:** `GET /reverb/shop`
- **What:** Get a Reverb shop's profile and active listings. Returns a Reverb shop's public profile plus a page of its current active listings (Reverb's own "shop" view of a seller). slug is the shop's slug, from a listing's own shop link or reverb.com/shop/{slug}. query is an optional free-text filter scoping the listings sub-page to a keyword within that shop. An unknown slug returns a typed not-found error.
- **Params:** `limit` (integer, optional) — Listings per page, defaults to 24, maximum 50; `page` (integer, optional) — One-based page number for the shop's listings, defaults to 1; `query` (string, optional) — Free-text filter scoping the shop's own listings sub-page; `slug` (string, **required**) — Shop slug

### `reverb_shop_feedback`

- **HTTP:** `GET /reverb/shop-feedback`
- **What:** Get a Reverb shop's buyer feedback. Returns a page of a Reverb shop's individual buyer feedback entries (rating, message, and the order each review was left for) -- reputation detail reverb-shop does not carry (reverb-shop only exposes the aggregate feedback_count/rating_percentage). slug is the shop's slug, from a listing's own shop link or reverb.com/shop/{slug}. An unknown slug returns a typed not-found error.
- **Params:** `page` (integer, optional) — One-based page number, defaults to 1; `slug` (string, **required**) — Shop slug
