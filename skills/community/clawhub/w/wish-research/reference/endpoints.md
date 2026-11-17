# wish-research — endpoint reference

> Generated from `scripts/tools.json` by `scripts/generate.mjs` — do not edit by hand.

Endpoints this skill uses, grouped by platform. Call them via `scripts/crawlora.sh` (see SKILL.md).

All paths are relative to the API base `https://api.crawlora.net/api/v1` and require the header `x-api-key: $CRAWLORA_API_KEY`. Path params like `{id}` are substituted into the URL; `GET` params go in the query string; `POST` params go in a JSON body.

**6 endpoints across 1 platform group(s).**

## Wish (6)

### `wish_categories`

- **HTTP:** `GET /wish/categories`
- **What:** Get Wish's category and filter navigation tree. Returns Wish's own top navigation/category tree (e.g. "Popular", "Deals Hub", "Fashion", "Gadgets") plus each category's nested filter groups (e.g. Color, Rating) where present. This is a static, site-wide taxonomy -- it takes no input and its result does not vary by search term or category.
- **Params:** _none_

### `wish_product`

- **HTTP:** `GET /wish/product/{id}`
- **What:** Get a Wish product's full detail. Returns one Wish product's full detail: name, description, sold-out state, aggregate rating, image URLs, and every purchasable variation with its own price, currency, inventory, and merchant. id is taken from a search result's product_id field or a product page's URL. An unrecognized id returns 404.
- **Params:** `id` (string, **required**) — Wish product id, a 24-character hex id from a search result's product_id field

### `wish_product_related`

- **HTTP:** `GET /wish/product/{id}/related`
- **What:** Get a Wish product's related items. Returns a Wish product's related-item rails: shelves of similar products, grouped by rail (e.g. general similar items, a faster-shipping-eligible subset). id is taken from a search result's product_id field or a product page's URL. A faster-shipping rail with no eligible items, or a nonexistent id, returns a normal, empty result rather than an error.
- **Params:** `count` (integer, optional) — Number of items to return per rail, 1 to 70, defaults to 10; `id` (string, **required**) — Wish product id, a 24-character hex id from a search result's product_id field

### `wish_product_reviews`

- **HTTP:** `GET /wish/product/{id}/reviews`
- **What:** Get a Wish product's customer reviews. Returns a Wish product's customer reviews. id is taken from a search result's product_id field or a product page's URL. A product with zero reviews returns a normal, empty result rather than an error. A caller wanting more reviews should re-request with a larger count -- this endpoint does not support an offset/cursor parameter.
- **Params:** `count` (integer, optional) — Number of reviews to return, 1 to 200, defaults to 10; `id` (string, **required**) — Wish product id, a 24-character hex id from a search result's product_id field

### `wish_search`

- **HTTP:** `GET /wish/search`
- **What:** Search Wish products. Searches Wish's product catalog by keyword, with real offset-based pagination. Returns products with price, currency, rating, review count, and merchant id. A query with no matches returns a normal, empty result rather than an error.
- **Params:** `count` (integer, optional) — Number of results per page, 1 to 70, defaults to 30; `offset` (integer, optional) — Result offset, 0-based, defaults to 0, must be an exact multiple of count up to 3 * count; `query` (string, **required**) — Search keyword

### `wish_suggest`

- **HTTP:** `GET /wish/suggest`
- **What:** Get Wish search suggestions. Returns Wish's own search-suggestion (typeahead) result for a partial search term: a flat list of suggested search terms, no product data. A partial term with no matches returns a normal, empty result rather than an error.
- **Params:** `query` (string, **required**) — Partial search term
