# zara-research — endpoint reference

> Generated from `scripts/tools.json` by `scripts/generate.mjs` — do not edit by hand.

Endpoints this skill uses, grouped by platform. Call them via `scripts/crawlora.sh` (see SKILL.md).

All paths are relative to the API base `https://api.crawlora.net/api/v1` and require the header `x-api-key: $CRAWLORA_API_KEY`. Path params like `{id}` are substituted into the URL; `GET` params go in the query string; `POST` params go in a JSON body.

**6 endpoints across 1 platform group(s).**

## Zara (6)

### `zara_categories`

- **HTTP:** `GET /zara/categories`
- **What:** List Zara's category and subcategory taxonomy. Returns Zara's full category and subcategory navigation tree for the US storefront (WOMAN, MAN, KID, and other top-level sections), sourced directly from Zara's own category navigation data. Each entry's id is the value to pass as categoryId to zara-category-products. Takes no query parameters.
- **Params:** _none_

### `zara_category_products`

- **HTTP:** `GET /zara/category/{categoryId}/products`
- **What:** Browse a Zara category's product listing. Returns a Zara category's full product listing: products with pricing, images, and availability. categoryId is a numeric id from zara-categories. Zara does not paginate this data -- the response always contains the category's complete listing in one call, not one page of it. Each entry represents one purchasable color variant rather than a color-grouped product family.
- **Params:** `categoryId` (string, **required**) — Numeric Zara category id, from zara-categories' id field

### `zara_product`

- **HTTP:** `GET /zara/product/{productId}`
- **What:** Get a Zara product's full detail. Returns one Zara product's full detail: every purchasable color variant with its real marketing description, per-size stock, and full image gallery -- richer than the per-product summaries returned by zara-category-products and zara-search. productId is a numeric id, taken from a search/category result's url field (the digits after "-p" in the product-detail URL). An unrecognized productId returns 404.
- **Params:** `productId` (string, **required**) — Numeric Zara product id, from a search/category result's url field

### `zara_search`

- **HTTP:** `GET /zara/search`
- **What:** Search Zara products. Searches Zara product listings by keyword within one department section, with real offset-based pagination. Returns products with pricing, images, availability, and every purchasable color variant, plus the search facets. This search is best-effort relevance, not a guaranteed keyword match: for an obscure or nonsense keyword, Zara's own search falls back to a broader recommended result set instead of returning an empty list, and there is no reliable field in the response to distinguish a true keyword match from that fallback behavior. Requesting an offset beyond the available results returns a normal, empty result with is_last_page true rather than an error.
- **Params:** `limit` (integer, optional) — Results per request, 1 to 100, defaults to 24; `offset` (integer, optional) — Zero-based result offset, defaults to 0; `query` (string, **required**) — Search keyword; `section` (string, **required**) — Department section to search

### `zara_stores`

- **HTTP:** `GET /zara/stores`
- **What:** Find nearby Zara physical stores. Returns Zara physical retail stores near a location: name, full address, phone, coordinates, opening hours status, pickup/donation eligibility, and a canonical store page URL. lat and lng are both required -- this endpoint does not accept a free-text zip/city search. A location with no stores within the radius returns a normal response with an empty stores array rather than an error.
- **Params:** `donation_only` (boolean, optional) — Only return stores that accept clothing donations; `lat` (number, **required**) — Latitude; `lng` (number, **required**) — Longitude; `pickup_only` (boolean, optional) — Only return stores that support in-store pickup; `radius` (integer, optional) — Search radius in miles, 1 to 500, defaults to 30

### `zara_suggest`

- **HTTP:** `GET /zara/suggest`
- **What:** Get Zara search-box suggestions for a partial keyword. Returns Zara's own search-suggestion (typeahead) results for a partial keyword, the same suggestions shown while typing into Zara's search box. A nonsense query returns a normal response with an empty suggestions array rather than a fallback/recommended set.
- **Params:** `query` (string, **required**) — Partial search keyword
