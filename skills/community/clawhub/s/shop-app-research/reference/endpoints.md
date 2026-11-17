# shop-app-research — endpoint reference

> Generated from `scripts/tools.json` by `scripts/generate.mjs` — do not edit by hand.

Endpoints this skill uses, grouped by platform. Call them via `scripts/crawlora.sh` (see SKILL.md).

All paths are relative to the API base `https://api.crawlora.net/api/v1` and require the header `x-api-key: $CRAWLORA_API_KEY`. Path params like `{id}` are substituted into the URL; `GET` params go in the query string; `POST` params go in a JSON body.

**16 endpoints across 1 platform group(s).**

## Shop.app (16)

### `shop_app_analysis`

- **HTTP:** `GET /shop-app/analysis`
- **What:** Analyze Shop.app query results. Returns a market snapshot derived from Shop.app search results, including price ranges, currencies, sale counts, discounts, and top shops. Limit defaults to 20 and accepts values up to 50.
- **Params:** `deep_search` (boolean, optional) — Accepted for compatibility; Shop.app no longer offers a separate deep search mode, so results are unchanged; `in_stock` (boolean, optional) — Request in-stock products; `limit` (integer, optional) — Maximum products to analyze, defaults to 20 and supports up to 50; `on_sale` (boolean, optional) — Request sale products; `query` (string, **required**) — Search query

### `shop_app_categories`

- **HTTP:** `GET /shop-app/categories`
- **What:** List Shop.app categories. Returns the Shop.app product category tree, with no parameters. Each category has its `id`, `gid`, `name`, `slug`, `image`, `has_children`, nested `children` and a `path` of ancestors. Ids are taken from Shopify product category GIDs where present.
- **Params:** _none_

### `shop_app_collection_products`

- **HTTP:** `GET /shop-app/shops/{handle}/collections/{collection_id}/products`
- **What:** List Shop.app collection products. Lists products in one collection of a Shop.app merchant, by shop `handle` and `collection_id`. `limit` defaults to 30 (max 60), `sort_by` is `MOST_SALES` (default), `PRICE_LOW_TO_HIGH`, `PRICE_HIGH_TO_LOW` or `RELEVANCE`, and `in_stock` defaults to true. Each card has its title, price, original price, image and URL.
- **Params:** `collection_id` (string, **required**) — Collection id; `handle` (string, **required**) — Shop handle; `in_stock` (boolean, optional) — Request in-stock products; `limit` (integer, optional) — Maximum products, defaults to 30 and supports up to 60; `sort_by` (string, optional) — Sort mode

### `shop_app_product`

- **HTTP:** `GET /shop-app/products/{id}`
- **What:** Get Shop.app product. Returns a Shop.app product by `id`: title, description, price and original price, currency, availability, images, option groups, rating, review count with reviews, related products and the selling shop. Pass `variant_id` to mark a variant as selected. Missing products return an error.
- **Params:** `id` (string, **required**) — Product id; `variant_id` (string, optional) — Variant id

### `shop_app_product_related`

- **HTTP:** `GET /shop-app/products/{id}/related`
- **What:** List Shop.app related products. Lists products related to a Shop.app product, by `id`. `limit` defaults to 20 and is capped at 50. Each card has the product's id, title, price, original price, currency, `on_sale` flag, image, shop name and URL. A product page with no related items returns an error.
- **Params:** `id` (string, **required**) — Product id; `limit` (integer, optional) — Maximum products, defaults to 20 and supports up to 50

### `shop_app_product_reviews`

- **HTTP:** `GET /shop-app/products/{id}/reviews`
- **What:** List Shop.app product reviews. Lists customer reviews for a Shop.app product, by `id`, up to `limit` (default 20, max 50). Each review has its rating, title, body, author, date, helpful count and variant label, where present. A product with no reviews returns an error.
- **Params:** `id` (string, **required**) — Product id; `limit` (integer, optional) — Maximum reviews, defaults to 20 and supports up to 50

### `shop_app_product_shop`

- **HTTP:** `GET /shop-app/products/{id}/shop`
- **What:** Get the Shop.app shop for a product. Finds the Shop.app merchant that sells a product, by the product `id`. Returns the shop's handle, name, description, logo, banner, rating, review count, storefront URL, and its collections. Unknown products, or ones with no public shop, return not found.
- **Params:** `id` (string, **required**) — Product id

### `shop_app_product_variant`

- **HTTP:** `GET /shop-app/products/{id}/variant`
- **What:** Get a Shop.app product variant by selected options. Returns the exact public product variant matching selected options. selected_options must be a JSON object when provided. Repeated option filters may also be sent as option.Name=value or option[Name]=value.
- **Params:** `id` (string, **required**) — Product id; `selected_options` (string, optional) — Selected options JSON object

### `shop_app_product_variants`

- **HTTP:** `GET /shop-app/products/{id}/variants`
- **What:** List Shop.app product variants. Returns adjacent variants for a Shop.app product. selected_options must be a JSON object when provided. Repeated option filters may also be sent as option.Name=value or option[Name]=value.
- **Params:** `id` (string, **required**) — Product id; `limit` (integer, optional) — Maximum variants, defaults to 50 and supports up to 100; `selected_options` (string, optional) — Selected options JSON object

### `shop_app_search`

- **HTTP:** `GET /shop-app/search`
- **What:** Search Shop.app products. Searches Shop.app product results. Limit defaults to 20 and accepts values up to 50.
- **Params:** `deep_search` (boolean, optional) — Accepted for compatibility; Shop.app no longer offers a separate deep search mode, so results are unchanged; `in_stock` (boolean, optional) — Request in-stock products; `limit` (integer, optional) — Maximum products, defaults to 20 and supports up to 50; `on_sale` (boolean, optional) — Request sale products; `query` (string, **required**) — Search query

### `shop_app_shop`

- **HTTP:** `GET /shop-app/shops/{handle}`
- **What:** Get Shop.app shop. Returns a Shop.app merchant profile by shop `handle`: name, description, logo, banner, rating, review count, storefront and Shop.app URLs, and collection summaries when the shop page lists them. Unknown handles return an error.
- **Params:** `handle` (string, **required**) — Shop handle

### `shop_app_shop_locations`

- **HTTP:** `GET /shop-app/shops/{handle}/locations`
- **What:** List Shop.app shop locations. Returns the public retail locations of a Shop.app merchant by shop handle, up to `limit` (default 10, max 50). Each location has its id, name, latitude and longitude, and street address; the response also carries the total count and a cursor for the next page. A shop with no public retail locations returns an error.
- **Params:** `handle` (string, **required**) — Shop handle; `limit` (integer, optional) — Maximum locations, defaults to 10 and supports up to 50

### `shop_app_shop_products`

- **HTTP:** `GET /shop-app/shops/{handle}/products`
- **What:** List Shop.app shop products. Lists products from a Shop.app merchant, by shop `handle`. `limit` defaults to 30 (max 60), `sort_by` is `MOST_SALES` (default), `PRICE_LOW_TO_HIGH`, `PRICE_HIGH_TO_LOW` or `RELEVANCE`, and `in_stock` defaults to true. Each card has its id, title, price, original price, image and URL. An invalid `sort_by` is rejected.
- **Params:** `handle` (string, **required**) — Shop handle; `in_stock` (boolean, optional) — Request in-stock products; `limit` (integer, optional) — Maximum products, defaults to 30 and supports up to 60; `sort_by` (string, optional) — Sort mode

### `shop_app_shop_reviews`

- **HTTP:** `GET /shop-app/shops/{handle}/reviews`
- **What:** List Shop.app shop reviews. Lists customer reviews for a Shop.app merchant, by shop `handle`, up to `limit` (default 20, max 50). Each review has its rating, body, author, date, helpful count and the product reviewed. Also returns `total_count` and `next_cursor`. Unknown shops return not found.
- **Params:** `handle` (string, **required**) — Shop handle; `limit` (integer, optional) — Maximum reviews, defaults to 20 and supports up to 50

### `shop_app_shop_typeahead`

- **HTTP:** `GET /shop-app/shops/{handle}/typeahead`
- **What:** Suggest products and collections inside a Shop.app shop. Returns search suggestions inside one Shop.app shop, for the shop `handle` and required `query`. `limit` defaults to 20, which is also the maximum. Suggestions are `type` term, product or collection, with text, position and a product or collection object where relevant. Unknown shops return not found.
- **Params:** `handle` (string, **required**) — Shop handle; `limit` (integer, optional) — Maximum suggestions, defaults to 20 and supports up to 20; `query` (string, **required**) — Typeahead query

### `shop_app_suggestions`

- **HTTP:** `GET /shop-app/suggestions`
- **What:** Suggest Shop.app searches. Returns Shop.app autocomplete suggestions for the required `query`. `limit` defaults to 10 and is capped at 20. Each suggestion is either a search query or a shop, with its `text`, `type`, URL and, for shops, the shop handle, name, rating and image.
- **Params:** `limit` (integer, optional) — Maximum suggestions, defaults to 10 and supports up to 20; `query` (string, **required**) — Search query
