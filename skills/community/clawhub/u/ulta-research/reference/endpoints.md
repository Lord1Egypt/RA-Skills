# ulta-research — endpoint reference

> Generated from `scripts/tools.json` by `scripts/generate.mjs` — do not edit by hand.

Endpoints this skill uses, grouped by platform. Call them via `scripts/crawlora.sh` (see SKILL.md).

All paths are relative to the API base `https://api.crawlora.net/api/v1` and require the header `x-api-key: $CRAWLORA_API_KEY`. Path params like `{id}` are substituted into the URL; `GET` params go in the query string; `POST` params go in a JSON body.

**8 endpoints across 1 platform group(s).**

## Ulta Beauty (8)

### `ulta_categories`

- **HTTP:** `GET /ulta/categories`
- **What:** List Ulta Beauty storefront categories. Lists Ulta Beauty's own storefront category navigation: department, group, name, and a URL usable directly as GET /ulta/category's own category parameter. Closes the discovery gap of not already knowing a category path. department, if set, filters to just that department's entries. group is empty for a department's own top-level link or a group's own heading link, and set to that group's name for the leaf categories nested under it. The exact same real category can legitimately appear more than once under a different department/group when the site's own navigation cross-lists it.
- **Params:** `department` (string, optional) — Filter to one department

### `ulta_category`

- **HTTP:** `GET /ulta/category`
- **What:** Browse an Ulta Beauty category page. Browses an Ulta Beauty category page's product grid, with real page-based pagination and the category's own guided-navigation refinement options. category accepts a category path or full URL copied from Ulta's own site navigation (e.g. shop/makeup/eyes/mascara). filter narrows results using Ulta's own guided-navigation facet-code shape (e.g. BENEFIT--WATERPROOF, or a comma-joined combination of codes) -- discover valid codes for a category from that category's own response facets field, whose value is ready to use directly as this parameter. An unrecognized category returns 404.
- **Params:** `category` (string, **required**) — Ulta category path or URL; `filter` (string, optional) — Guided-navigation facet code(s), comma-joined for multiple; `page` (integer, optional) — Result page, 1-based, defaults to 1

### `ulta_product`

- **HTTP:** `GET /ulta/product/{productId}`
- **What:** Get an Ulta Beauty product's full detail. Returns one Ulta Beauty product's full detail: name, brand, description, category, pricing, rating, review count, images, and every purchasable color/shade variant. productId is taken from a search result's product_id field or a product page's URL (e.g. pimprod2020260). sku is optional and selects a specific color/shade variant; an omitted or invalid sku still resolves the base product using its own default variant. An unrecognized productId returns 404.
- **Params:** `productId` (string, **required**) — Ulta product id, from a search result's product_id field; `sku` (string, optional) — Numeric Ulta sku id selecting a specific color/shade variant

### `ulta_product_questions`

- **HTTP:** `GET /ulta/product/questions`
- **What:** Get an Ulta Beauty product's customer questions and answers. Returns one page of an Ulta Beauty product's customer questions, each with every answer it received. product_id is taken from a search result's product_id field or a product page's URL. A product with zero questions, or a well-formed but unrecognized product_id, returns a normal, empty result rather than an error.
- **Params:** `page` (integer, optional) — Result page, 1-based, defaults to 1; `product_id` (string, **required**) — Ulta product id, from a search result's product_id field

### `ulta_product_reviews`

- **HTTP:** `GET /ulta/product/reviews`
- **What:** Get an Ulta Beauty product's customer reviews. Returns one page of an Ulta Beauty product's customer reviews, plus the retailer's own site-wide rating summary (rating count, average rating, recommended ratio, rating histogram) for the product. product_id is taken from a search result's product_id field or a product page's URL. A product with zero reviews, or a well-formed but unrecognized product_id, returns a normal, empty result rather than an error.
- **Params:** `page` (integer, optional) — Result page, 1-based, defaults to 1; `product_id` (string, **required**) — Ulta product id, from a search result's product_id field

### `ulta_search`

- **HTTP:** `GET /ulta/search`
- **What:** Search Ulta Beauty products. Searches Ulta Beauty's product catalog by keyword, with real page-based pagination. Returns products with brand, pricing, rating, and review count. An unrecognized/nonsense keyword returns a genuine empty result rather than a fallback set. Requesting a page beyond the available results returns a normal, empty result rather than an error.
- **Params:** `page` (integer, optional) — Result page, 1-based, defaults to 1; `query` (string, **required**) — Search keyword

### `ulta_stores`

- **HTTP:** `GET /ulta/stores`
- **What:** Find nearby Ulta Beauty physical stores. Returns Ulta Beauty physical retail store locations near a point: name, phone, full address, hours, services, and coordinates. Either search, or both lat and lng, is required. search is a free-text zip code, city, or address that is first resolved to coordinates; if it does not resolve to any location, a well-formed empty result is returned rather than an error. lat and lng, when given directly, skip that resolution step. radius_meters is optional (1000 to 50000, defaults to 25000). A location with no stores within the radius returns a well-formed empty result rather than an error.
- **Params:** `lat` (number, optional) — Latitude, requires lng; `lng` (number, optional) — Longitude, requires lat; `radius_meters` (integer, optional) — Search radius in meters, 1000 to 50000, defaults to 25000; `search` (string, optional) — Free-text zip code, city, or address to resolve to coordinates

### `ulta_suggest`

- **HTTP:** `GET /ulta/suggest`
- **What:** Get Ulta Beauty search suggestions. Returns Ulta Beauty's own search-suggestion (typeahead) result for a partial search term: suggested search terms, each with its own top product matches, plus a featured top result matching what a real user sees at the top of the dropdown. A partial term with no matches returns a normal, empty result rather than an error.
- **Params:** `query` (string, **required**) — Partial search term
