# retail-assortment-gap-analysis — endpoint reference

> Generated from `scripts/tools.json` by `scripts/generate.mjs` — do not edit by hand.

Only the endpoints used by this workflow. Call them via `scripts/crawlora.sh` (see SKILL.md).

All paths are relative to the API base `https://api.crawlora.net/api/v1` and require the header `x-api-key: $CRAWLORA_API_KEY`. Path params like `{id}` are substituted into the URL; `GET` params go in the query string; `POST` params go in a JSON body.

**11 endpoints across 3 platform group(s).**

## Shopify (5)

### `shopify_collection_products`

- **HTTP:** `GET /shopify/collections/{handle}/products`
- **What:** List Shopify collection products. Returns products from a Shopify collection. `sortBy` and dynamic facet-filter query params (e.g. `fit`, `canonicalColour`) only take effect for headless storefronts (`transport_mode: "ssr_embedded"`) and return an invalid-param error if supplied against a classic store, since classic Shopify storefronts have no server-side sort or filter support. `sort_by`, `min_price`, `max_price`, `product_type`, `in_stock_only`, and `option_`-prefixed params (e.g. `option_size=Small,Medium`) drive a separate, independent mechanism -- Shopify's own native Storefront Filtering collection-page feature (`transport_mode: "storefront_filtered"`) -- which works for both classic and headless stores; supplying any of these takes precedence over sortBy/dynamic facet filters.
- **Params:** `handle` (string, **required**) — Collection handle; `in_stock_only` (boolean, optional) — Storefront-filtering transport. true restricts to currently in-stock items only.; `limit` (integer, optional) — Maximum products, defaults to 50 and supports up to 250; `max_price` (number, optional) — Storefront-filtering transport. Maximum price (inclusive), in the storefront's display currency's major unit.; `min_price` (number, optional) — Storefront-filtering transport. Minimum price (inclusive), in the storefront's display currency's major unit.; `option_size` (string, optional) — Storefront-filtering transport. Example dynamic variant-option filter: comma-separated exact display values for the storefront's own size option (e.g. option_size=Small,Medium). Any variant option name is accepted the same way (option_color, ...) -- see facets in an unfiltered response for the live option names/values per store.; `page` (integer, optional) — 1-based page, defaults to 1; `product_type` (string, optional) — Storefront-filtering transport, comma-separated. Exact product-type display strings from the storefront's own Product Type facet -- see facets.product_type in an unfiltered response for the live value set.; `sortBy` (string, optional) — SSR-fallback transport only (transport_mode ssr_embedded). Allowed values: sortLTH, sortHTL, newest. Omit for the storefront's default relevancy order. Rejected as an invalid param for classic-transport stores.; `sort_by` (string, optional) — Storefront-filtering transport. Allowed values: manual, best-selling, title-ascending, title-descending, price-ascending, price-descending, created-ascending, created-descending. Omit for the collection's own default order.; `url` (string, **required**) — Shopify storefront URL

### `shopify_collections`

- **HTTP:** `GET /shopify/collections`
- **What:** List Shopify collections. Returns collections from a public Shopify storefront. Valid empty result pages return `200` with an empty collections array.
- **Params:** `limit` (integer, optional) — Maximum collections, defaults to 50 and supports up to 250; `page` (integer, optional) — 1-based page, defaults to 1; `url` (string, **required**) — Shopify storefront URL

### `shopify_product`

- **HTTP:** `GET /shopify/products/{handle}`
- **What:** Get Shopify product. Returns one product from any Shopify storefront, given the store URL and the product handle: title, description, product type, tags, price and compare-at price, availability, options, images, and each variant with its own price, availability and barcode. Prices are in decimal currency units; an unknown handle returns `404`.
- **Params:** `handle` (string, **required**) — Product handle; `url` (string, **required**) — Shopify storefront URL

### `shopify_products`

- **HTTP:** `GET /shopify/products`
- **What:** List Shopify products. Returns products from a public Shopify storefront. Valid empty result pages return `200` with an empty products array. `sortBy` and dynamic facet-filter query params (e.g. `fit`, `canonicalColour`) only take effect for headless storefronts (`transport_mode: "ssr_embedded"`) and return an invalid-param error if supplied against a classic store, since classic Shopify storefronts have no server-side sort or filter support. `sort_by`, `min_price`, `max_price`, `product_type`, `in_stock_only`, and `option_`-prefixed params (e.g. `option_size=Small,Medium`) drive a separate, independent mechanism -- Shopify's own native Storefront Filtering collection-page feature (`transport_mode: "storefront_filtered"`) -- which works for both classic and headless stores; supplying any of these takes precedence over sortBy/dynamic facet filters.
- **Params:** `in_stock_only` (boolean, optional) — Storefront-filtering transport. true restricts to currently in-stock items only.; `limit` (integer, optional) — Maximum products, defaults to 50 and supports up to 250; `max_price` (number, optional) — Storefront-filtering transport. Maximum price (inclusive), in the storefront's display currency's major unit.; `min_price` (number, optional) — Storefront-filtering transport. Minimum price (inclusive), in the storefront's display currency's major unit.; `option_size` (string, optional) — Storefront-filtering transport. Example dynamic variant-option filter: comma-separated exact display values for the storefront's own size option (e.g. option_size=Small,Medium). Any variant option name is accepted the same way (option_color, ...) -- see facets in an unfiltered response for the live option names/values per store.; `page` (integer, optional) — 1-based page, defaults to 1; `product_type` (string, optional) — Storefront-filtering transport, comma-separated. Exact product-type display strings from the storefront's own Product Type facet -- see facets.product_type in an unfiltered response for the live value set.; `sortBy` (string, optional) — SSR-fallback transport only (transport_mode ssr_embedded). Allowed values: sortLTH, sortHTL, newest. Omit for the storefront's default relevancy order. Rejected as an invalid param for classic-transport stores.; `sort_by` (string, optional) — Storefront-filtering transport. Allowed values: manual, best-selling, title-ascending, title-descending, price-ascending, price-descending, created-ascending, created-descending. Omit for the collection's own default order.; `url` (string, **required**) — Shopify storefront URL

### `shopify_store`

- **HTTP:** `GET /shopify/store`
- **What:** Get Shopify store metadata. Resolves a public Shopify storefront and returns its metadata.
- **Params:** `url` (string, **required**) — Shopify storefront URL

## Target (3)

### `target_categories`

- **HTTP:** `GET /target/categories`
- **What:** List all Target categories. Lists Target's top-level category menu in `categories`, plus the grouped shop-all directory in `groups`. Each category has an `id` (the one used by `/target/category-products`), name, canonical URL and, when Target supplies one, an image URL. The response also gives `count` and `group_count`. Takes no parameters.
- **Params:** _none_

### `target_category_products`

- **HTTP:** `GET /target/category-products`
- **What:** Browse Target category products. Returns paginated products for any category id from target-categories. Each response also contains every available dynamic filter group and option. Pass selected option ids through filter_ids as a comma-separated list. The sort enum accepts `relevance`, `featured`, `price-low`, `price-high`, `rating`, `bestselling`, and `newest`.
- **Params:** `category_id` (string, **required**) — Target category id; `filter_ids` (string, optional) — Comma-separated Target filter option ids; `page` (integer, optional) — One-based page (1-50); `sort` (string, optional) — Result order; `store_id` (integer, optional) — Target store id used for pricing

### `target_product`

- **HTTP:** `GET /target/product`
- **What:** Get a Target product. Returns product details for one Target item, including product content, images, price, rating, category, and availability flags for the selected store.
- **Params:** `store_id` (integer, optional) — Target store id used for pricing and availability; `tcin` (string, **required**) — Numeric Target item id (TCIN)

## IKEA (3)

### `ikea_category`

- **HTTP:** `GET /ikea/category`
- **What:** Browse an IKEA category. Returns one page of an IKEA category's product listing, with real offset/size pagination and sort. category is IKEA's own category key (e.g. 20649), taken from a category URL's trailing -{key}/ segment, a product's own category_path field, or GET /ikea/categories, which discovers every valid category value.
- **Params:** `category` (string, **required**) — IKEA category key; `country` (string, optional) — Lowercase 2-letter IKEA site country code; `language` (string, optional) — Lowercase 2-letter IKEA site language code; `offset` (integer, optional) — Zero-based result offset; `size` (integer, optional) — Result count (1-100); `sort` (string, optional) — Result order

### `ikea_product`

- **HTTP:** `GET /ikea/product`
- **What:** Get an IKEA product's detail. Returns one IKEA item's full detail: name, price, rating, every product image, quick facts, and category breadcrumb path. item_no is IKEA's own item number (8 digits, optionally prefixed with "s" for a combination/set article), taken from a search result's item_no field or an ikea.com product page's own URL.
- **Params:** `country` (string, optional) — Lowercase 2-letter IKEA site country code; `item_no` (string, **required**) — IKEA item number; `language` (string, optional) — Lowercase 2-letter IKEA site language code

### `ikea_search`

- **HTTP:** `GET /ikea/search`
- **What:** Search IKEA products. Searches IKEA products and returns name, price, rating, images, colors, and variant data. q is a free-text query; an IKEA item number also resolves as its own single result. country and language select IKEA's per-country site (default us/en). A zero total with an empty products list is a valid no-results response.
- **Params:** `country` (string, optional) — Lowercase 2-letter IKEA site country code; `language` (string, optional) — Lowercase 2-letter IKEA site language code; `q` (string, **required**) — Free-text product search query; `size` (integer, optional) — Result count (1-100)
