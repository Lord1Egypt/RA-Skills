# shopify-research — endpoint reference

> Generated from `scripts/tools.json` by `scripts/generate.mjs` — do not edit by hand.

Endpoints this skill uses, grouped by platform. Call them via `scripts/crawlora.sh` (see SKILL.md).

All paths are relative to the API base `https://api.crawlora.net/api/v1` and require the header `x-api-key: $CRAWLORA_API_KEY`. Path params like `{id}` are substituted into the URL; `GET` params go in the query string; `POST` params go in a JSON body.

**159 endpoints across 15 platform group(s).**

## Shopify (11)

### `shopify_collection_products`

- **HTTP:** `GET /shopify/collections/{handle}/products`
- **What:** List Shopify collection products. Returns products from a Shopify collection. `sortBy` and dynamic facet-filter query params (e.g. `fit`, `canonicalColour`) only take effect for headless storefronts (`transport_mode: "ssr_embedded"`) and return an invalid-param error if supplied against a classic store, since classic Shopify storefronts have no server-side sort or filter support. `sort_by`, `min_price`, `max_price`, `product_type`, `in_stock_only`, and `option_`-prefixed params (e.g. `option_size=Small,Medium`) drive a separate, independent mechanism -- Shopify's own native Storefront Filtering collection-page feature (`transport_mode: "storefront_filtered"`) -- which works for both classic and headless stores; supplying any of these takes precedence over sortBy/dynamic facet filters.
- **Params:** `handle` (string, **required**) — Collection handle; `in_stock_only` (boolean, optional) — Storefront-filtering transport. true restricts to currently in-stock items only.; `limit` (integer, optional) — Maximum products, defaults to 50 and supports up to 250; `max_price` (number, optional) — Storefront-filtering transport. Maximum price (inclusive), in the storefront's display currency's major unit.; `min_price` (number, optional) — Storefront-filtering transport. Minimum price (inclusive), in the storefront's display currency's major unit.; `option_size` (string, optional) — Storefront-filtering transport. Example dynamic variant-option filter: comma-separated exact display values for the storefront's own size option (e.g. option_size=Small,Medium). Any variant option name is accepted the same way (option_color, ...) -- see facets in an unfiltered response for the live option names/values per store.; `page` (integer, optional) — 1-based page, defaults to 1; `product_type` (string, optional) — Storefront-filtering transport, comma-separated. Exact product-type display strings from the storefront's own Product Type facet -- see facets.product_type in an unfiltered response for the live value set.; `sortBy` (string, optional) — SSR-fallback transport only (transport_mode ssr_embedded). Allowed values: sortLTH, sortHTL, newest. Omit for the storefront's default relevancy order. Rejected as an invalid param for classic-transport stores.; `sort_by` (string, optional) — Storefront-filtering transport. Allowed values: manual, best-selling, title-ascending, title-descending, price-ascending, price-descending, created-ascending, created-descending. Omit for the collection's own default order.; `url` (string, **required**) — Shopify storefront URL

### `shopify_collections`

- **HTTP:** `GET /shopify/collections`
- **What:** List Shopify collections. Returns collections from a public Shopify storefront. Valid empty result pages return `200` with an empty collections array.
- **Params:** `limit` (integer, optional) — Maximum collections, defaults to 50 and supports up to 250; `page` (integer, optional) — 1-based page, defaults to 1; `url` (string, **required**) — Shopify storefront URL

### `shopify_page`

- **HTTP:** `GET /shopify/pages/{handle}`
- **What:** Get Shopify page. Returns one static page from any public Shopify storefront, by path `handle` and the required `url` of the store. The response has the page's title, URL, times and its `content` as plain text. Unknown handles return 404. Localhost, private-network and credentialed URLs are rejected.
- **Params:** `handle` (string, **required**) — Page handle; `url` (string, **required**) — Shopify storefront URL

### `shopify_pages`

- **HTTP:** `GET /shopify/pages`
- **What:** List Shopify pages. Lists static pages from a Shopify storefront given by the required `url`, paged with `page` (from 1) and `limit` (default 50, max 250). Each has `handle`, `title`, `url`, plain-text `content` and dates. If `transport_mode` is `ssr_embedded`, items hold only `handle`, `url` and `updated_at`.
- **Params:** `limit` (integer, optional) — Maximum pages, defaults to 50 and supports up to 250; `page` (integer, optional) — 1-based page, defaults to 1; `url` (string, **required**) — Shopify storefront URL

### `shopify_product`

- **HTTP:** `GET /shopify/products/{handle}`
- **What:** Get Shopify product. Returns one product from any Shopify storefront, given the store URL and the product handle: title, description, product type, tags, price and compare-at price, availability, options, images, and each variant with its own price, availability and barcode. Prices are in decimal currency units; an unknown handle returns `404`.
- **Params:** `handle` (string, **required**) — Product handle; `url` (string, **required**) — Shopify storefront URL

### `shopify_product_recommendations`

- **HTTP:** `GET /shopify/products/{handle}/recommendations`
- **What:** List Shopify product recommendations. Returns recommended products from Shopify's product recommendations.
- **Params:** `handle` (string, **required**) — Product handle; `intent` (string, optional) — Recommendation intent. Allowed values: related, complementary; `limit` (integer, optional) — Maximum products, defaults to 10 and supports up to 20; `url` (string, **required**) — Shopify storefront URL

### `shopify_products`

- **HTTP:** `GET /shopify/products`
- **What:** List Shopify products. Returns products from a public Shopify storefront. Valid empty result pages return `200` with an empty products array. `sortBy` and dynamic facet-filter query params (e.g. `fit`, `canonicalColour`) only take effect for headless storefronts (`transport_mode: "ssr_embedded"`) and return an invalid-param error if supplied against a classic store, since classic Shopify storefronts have no server-side sort or filter support. `sort_by`, `min_price`, `max_price`, `product_type`, `in_stock_only`, and `option_`-prefixed params (e.g. `option_size=Small,Medium`) drive a separate, independent mechanism -- Shopify's own native Storefront Filtering collection-page feature (`transport_mode: "storefront_filtered"`) -- which works for both classic and headless stores; supplying any of these takes precedence over sortBy/dynamic facet filters.
- **Params:** `in_stock_only` (boolean, optional) — Storefront-filtering transport. true restricts to currently in-stock items only.; `limit` (integer, optional) — Maximum products, defaults to 50 and supports up to 250; `max_price` (number, optional) — Storefront-filtering transport. Maximum price (inclusive), in the storefront's display currency's major unit.; `min_price` (number, optional) — Storefront-filtering transport. Minimum price (inclusive), in the storefront's display currency's major unit.; `option_size` (string, optional) — Storefront-filtering transport. Example dynamic variant-option filter: comma-separated exact display values for the storefront's own size option (e.g. option_size=Small,Medium). Any variant option name is accepted the same way (option_color, ...) -- see facets in an unfiltered response for the live option names/values per store.; `page` (integer, optional) — 1-based page, defaults to 1; `product_type` (string, optional) — Storefront-filtering transport, comma-separated. Exact product-type display strings from the storefront's own Product Type facet -- see facets.product_type in an unfiltered response for the live value set.; `sortBy` (string, optional) — SSR-fallback transport only (transport_mode ssr_embedded). Allowed values: sortLTH, sortHTL, newest. Omit for the storefront's default relevancy order. Rejected as an invalid param for classic-transport stores.; `sort_by` (string, optional) — Storefront-filtering transport. Allowed values: manual, best-selling, title-ascending, title-descending, price-ascending, price-descending, created-ascending, created-descending. Omit for the collection's own default order.; `url` (string, **required**) — Shopify storefront URL

### `shopify_search_suggest`

- **HTTP:** `GET /shopify/search/suggest`
- **What:** Get Shopify search suggestions. Returns predictive search suggestions from any Shopify storefront for a query: matching products, collections and suggested queries. Choose which with `types` (default all three) and cap results per type with `limit` (default 10, max 20). Products carry price, availability, images and options; collections carry title, handle, description and product count.
- **Params:** `limit` (integer, optional) — Maximum results per type, defaults to 10 and supports up to 20; `q` (string, **required**) — Search query; `types` (string, optional) — Comma-separated suggestion types. Allowed values: product, collection, query; `url` (string, **required**) — Shopify storefront URL

### `shopify_sitemap_urls`

- **HTTP:** `GET /shopify/sitemap/urls`
- **What:** List Shopify sitemap URLs. Lists URL entries from a Shopify storefront's sitemaps, for the required `url`. `type` filters (`all` by default, `products`, `collections`, `pages`, `blogs`, `agentic_discovery`, `other`) and `limit` caps entries (default 50, max 250). Each has `loc`, `type`, `handle`, `lastmod`, `changefreq` and optional `images`.
- **Params:** `limit` (integer, optional) — Maximum URL entries, defaults to 50 and supports up to 250; `type` (string, optional) — Sitemap type. Allowed values: all, products, collections, pages, blogs, agentic_discovery, other; `url` (string, **required**) — Shopify storefront URL

### `shopify_sitemaps`

- **HTTP:** `GET /shopify/sitemaps`
- **What:** List Shopify sitemaps. Lists the child sitemaps in a Shopify storefront's sitemap index, for the required `url`. Each has a `loc` and a `type` (`products`, `collections`, `pages`, `blogs`, `agentic_discovery` or `other`) inferred from its URL. Localhost, private-network and credentialed URLs are rejected.
- **Params:** `url` (string, **required**) — Shopify storefront URL

### `shopify_store`

- **HTTP:** `GET /shopify/store`
- **What:** Get Shopify store metadata. Resolves a public Shopify storefront and returns its metadata.
- **Params:** `url` (string, **required**) — Shopify storefront URL

## Allbirds (11)

### `allbirds_collection_products`

- **HTTP:** `GET /allbirds/collections/{handle}/products`
- **What:** List Allbirds collection products. Returns products from one Allbirds (https://www.allbirds.com) collection. The storefront URL is fixed server-side; `handle` is the collection's URL slug.
- **Params:** `handle` (string, **required**) — Collection handle; `limit` (integer, optional) — Maximum products, defaults to 50 and supports up to 250; `page` (integer, optional) — 1-based page, defaults to 1

### `allbirds_collections`

- **HTTP:** `GET /allbirds/collections`
- **What:** List Allbirds collections. Returns collections from Allbirds (https://www.allbirds.com). The storefront URL is fixed server-side. Valid empty result pages return `200` with an empty collections array.
- **Params:** `limit` (integer, optional) — Maximum collections, defaults to 50 and supports up to 250; `page` (integer, optional) — 1-based page, defaults to 1

### `allbirds_page`

- **HTTP:** `GET /allbirds/pages/{handle}`
- **What:** Get a Allbirds static page. Returns one static page from the Allbirds store by its `handle`: title, URL, publish and update times, and `content` as plain text rather than HTML. `id` is omitted on some pages. A handle that does not exist returns 404.
- **Params:** `handle` (string, **required**) — Page handle

### `allbirds_pages`

- **HTTP:** `GET /allbirds/pages`
- **What:** List Allbirds static pages. Lists static pages from the Allbirds store, paged with `page` (default 1) and `limit` (default 50, max 250). Each item has `handle`, `title`, `url`, `id`, publish and update times and plain-text `content`. In some responses items carry only `handle`, `url` and `updated_at`.
- **Params:** `limit` (integer, optional) — Maximum static pages, defaults to 50 and supports up to 250; `page` (integer, optional) — 1-based page, defaults to 1

### `allbirds_product`

- **HTTP:** `GET /allbirds/products/{handle}`
- **What:** Get a Allbirds product. Returns product detail for one Allbirds (https://www.allbirds.com) product handle. The storefront URL is fixed server-side; `handle` is the product's URL slug.
- **Params:** `handle` (string, **required**) — Product handle

### `allbirds_product_recommendations`

- **HTTP:** `GET /allbirds/products/{handle}/recommendations`
- **What:** List Allbirds product recommendations. Returns recommended products for one Allbirds (https://www.allbirds.com) product handle. The storefront URL is fixed server-side.
- **Params:** `handle` (string, **required**) — Product handle; `intent` (string, optional) — Recommendation intent. Allowed values: related, complementary; `limit` (integer, optional) — Maximum products, defaults to 10 and supports up to 20

### `allbirds_products`

- **HTTP:** `GET /allbirds/products`
- **What:** List Allbirds products. Returns products from Allbirds's (https://www.allbirds.com) public product catalog. The storefront URL is fixed server-side. Valid empty result pages return `200` with an empty products array.
- **Params:** `limit` (integer, optional) — Maximum products, defaults to 50 and supports up to 250; `page` (integer, optional) — 1-based page, defaults to 1

### `allbirds_search_suggest`

- **HTTP:** `GET /allbirds/search/suggest`
- **What:** Get Allbirds search suggestions. Returns products, collections, and query suggestions from Allbirds's (https://www.allbirds.com) predictive search. The storefront URL is fixed server-side.
- **Params:** `limit` (integer, optional) — Maximum results per type, defaults to 10 and supports up to 20; `q` (string, **required**) — Search query; `types` (string, optional) — Comma-separated suggestion types. Allowed values: product, collection, query

### `allbirds_sitemap_urls`

- **HTTP:** `GET /allbirds/sitemap/urls`
- **What:** List Allbirds sitemap URLs. Lists URL entries from the Allbirds store sitemaps, filtered by `type` (`all`, `products`, `collections`, `pages`, `blogs`, `agentic_discovery` or `other`; default `all`). `limit` defaults to 50 and is capped at 250. Each entry has `loc`, `type`, `handle`, `lastmod`, `changefreq` and optional `images`.
- **Params:** `limit` (integer, optional) — Maximum URL entries, defaults to 50 and supports up to 250; `type` (string, optional) — Sitemap type. Allowed values: all, products, collections, pages, blogs, agentic_discovery, other

### `allbirds_sitemaps`

- **HTTP:** `GET /allbirds/sitemaps`
- **What:** List Allbirds sitemaps. Lists the child sitemaps in the Allbirds store's sitemap index, each with its `loc` and a `type` of `products`, `collections`, `pages`, `blogs`, `agentic_discovery` or `other`. Takes no parameters. The types match the `type` filter of `allbirds-sitemap-urls`.
- **Params:** _none_

### `allbirds_store`

- **HTTP:** `GET /allbirds/store`
- **What:** Get Allbirds store metadata. Returns storefront metadata for Allbirds (https://www.allbirds.com). The storefront URL is fixed server-side, so no `url` parameter is accepted.
- **Params:** _none_

## Brooklinen (11)

### `brooklinen_collection_products`

- **HTTP:** `GET /brooklinen/collections/{handle}/products`
- **What:** List Brooklinen collection products. Returns products from one Brooklinen (https://www.brooklinen.com) collection. The storefront URL is fixed server-side; `handle` is the collection's URL slug.
- **Params:** `handle` (string, **required**) — Collection handle; `limit` (integer, optional) — Maximum products, defaults to 50 and supports up to 250; `page` (integer, optional) — 1-based page, defaults to 1

### `brooklinen_collections`

- **HTTP:** `GET /brooklinen/collections`
- **What:** List Brooklinen collections. Returns collections from Brooklinen (https://www.brooklinen.com). The storefront URL is fixed server-side. Valid empty result pages return `200` with an empty collections array.
- **Params:** `limit` (integer, optional) — Maximum collections, defaults to 50 and supports up to 250; `page` (integer, optional) — 1-based page, defaults to 1

### `brooklinen_page`

- **HTTP:** `GET /brooklinen/pages/{handle}`
- **What:** Get a Brooklinen static page. Returns one Brooklinen static page by its `handle`: id, title, URL, plain-text content, and created, published and updated times. A missing handle returns 404. When `transport_mode` is `ssr_embedded`, the content is plain text from the page's rich-text blocks and `id` is omitted.
- **Params:** `handle` (string, **required**) — Page handle

### `brooklinen_pages`

- **HTTP:** `GET /brooklinen/pages`
- **What:** List Brooklinen static pages. Lists Brooklinen static pages, `limit` per page (default 50, max 250) and `page` starting at 1. Each page has its handle, title, URL, plain-text content and timestamps. When `transport_mode` is `ssr_embedded`, items carry only `handle`, `url` and `updated_at`; request each handle singly for content.
- **Params:** `limit` (integer, optional) — Maximum static pages, defaults to 50 and supports up to 250; `page` (integer, optional) — 1-based page, defaults to 1

### `brooklinen_product`

- **HTTP:** `GET /brooklinen/products/{handle}`
- **What:** Get a Brooklinen product. Returns product detail for one Brooklinen (https://www.brooklinen.com) product handle. The storefront URL is fixed server-side; `handle` is the product's URL slug.
- **Params:** `handle` (string, **required**) — Product handle

### `brooklinen_product_recommendations`

- **HTTP:** `GET /brooklinen/products/{handle}/recommendations`
- **What:** List Brooklinen product recommendations. Returns recommended products for one Brooklinen (https://www.brooklinen.com) product handle. The storefront URL is fixed server-side.
- **Params:** `handle` (string, **required**) — Product handle; `intent` (string, optional) — Recommendation intent. Allowed values: related, complementary; `limit` (integer, optional) — Maximum products, defaults to 10 and supports up to 20

### `brooklinen_products`

- **HTTP:** `GET /brooklinen/products`
- **What:** List Brooklinen products. Returns products from Brooklinen's (https://www.brooklinen.com) product catalog. The storefront URL is fixed server-side. Valid empty result pages return `200` with an empty products array.
- **Params:** `limit` (integer, optional) — Maximum products, defaults to 50 and supports up to 250; `page` (integer, optional) — 1-based page, defaults to 1

### `brooklinen_search_suggest`

- **HTTP:** `GET /brooklinen/search/suggest`
- **What:** Get Brooklinen search suggestions. Returns products, collections, and query suggestions from Brooklinen's (https://www.brooklinen.com) predictive search. The storefront URL is fixed server-side.
- **Params:** `limit` (integer, optional) — Maximum results per type, defaults to 10 and supports up to 20; `q` (string, **required**) — Search query; `types` (string, optional) — Comma-separated suggestion types. Allowed values: product, collection, query

### `brooklinen_sitemap_urls`

- **HTTP:** `GET /brooklinen/sitemap/urls`
- **What:** List Brooklinen sitemap URLs. Lists URL entries from Brooklinen's sitemaps, filtered by `type` (`all` by default, or `products`, `collections`, `pages`, `blogs`, `agentic_discovery`, `other`) and capped by `limit` (default 50, max 250). Each entry has its `loc`, type, handle, `lastmod`, `changefreq` and, where present, images with caption and title.
- **Params:** `limit` (integer, optional) — Maximum URL entries, defaults to 50 and supports up to 250; `type` (string, optional) — Sitemap type. Allowed values: all, products, collections, pages, blogs, agentic_discovery, other

### `brooklinen_sitemaps`

- **HTTP:** `GET /brooklinen/sitemaps`
- **What:** List Brooklinen sitemaps. Lists the child sitemaps that Brooklinen publishes, with no parameters. Each entry has its `loc` URL and a `type` of `products`, `collections`, `pages`, `blogs`, `agentic_discovery` or `other`, which tells you which sitemap to pass to the sitemap URL endpoint.
- **Params:** _none_

### `brooklinen_store`

- **HTTP:** `GET /brooklinen/store`
- **What:** Get Brooklinen store metadata. Returns storefront metadata for Brooklinen (https://www.brooklinen.com). The storefront URL is fixed server-side, so no `url` parameter is accepted.
- **Params:** _none_

## Cole Haan (11)

### `colehaan_collection_products`

- **HTTP:** `GET /colehaan/collections/{handle}/products`
- **What:** List Cole Haan collection products. Returns products from one Cole Haan (https://www.colehaan.com) collection. The storefront URL is fixed server-side; `handle` is the collection's URL slug.
- **Params:** `handle` (string, **required**) — Collection handle; `limit` (integer, optional) — Maximum products, defaults to 50 and supports up to 250; `page` (integer, optional) — 1-based page, defaults to 1

### `colehaan_collections`

- **HTTP:** `GET /colehaan/collections`
- **What:** List Cole Haan collections. Returns collections from Cole Haan (https://www.colehaan.com). The storefront URL is fixed server-side. Valid empty result pages return `200` with an empty collections array.
- **Params:** `limit` (integer, optional) — Maximum collections, defaults to 50 and supports up to 250; `page` (integer, optional) — 1-based page, defaults to 1

### `colehaan_page`

- **HTTP:** `GET /colehaan/pages/{handle}`
- **What:** Get a Cole Haan static page. Returns one Cole Haan static page by its `handle`: id, title, URL, plain-text content, and created, published and updated times. A missing handle returns 404. When `transport_mode` is `ssr_embedded`, `id` is omitted and the content is plain text taken from the page's rich-text blocks.
- **Params:** `handle` (string, **required**) — Page handle

### `colehaan_pages`

- **HTTP:** `GET /colehaan/pages`
- **What:** List Cole Haan static pages. Lists Cole Haan static pages, with `page` (from 1) and `limit` (default 50, max 250). Each page has handle, title, URL, plain-text content and timestamps. If `transport_mode` is `ssr_embedded`, items carry only `handle`, `url` and `updated_at`, so fetch a single page for its content.
- **Params:** `limit` (integer, optional) — Maximum static pages, defaults to 50 and supports up to 250; `page` (integer, optional) — 1-based page, defaults to 1

### `colehaan_product`

- **HTTP:** `GET /colehaan/products/{handle}`
- **What:** Get a Cole Haan product. Returns product detail for one Cole Haan (https://www.colehaan.com) product handle. The storefront URL is fixed server-side; `handle` is the product's URL slug.
- **Params:** `handle` (string, **required**) — Product handle

### `colehaan_product_recommendations`

- **HTTP:** `GET /colehaan/products/{handle}/recommendations`
- **What:** List Cole Haan product recommendations. Returns recommended products for one Cole Haan (https://www.colehaan.com) product handle. The storefront URL is fixed server-side.
- **Params:** `handle` (string, **required**) — Product handle; `intent` (string, optional) — Recommendation intent. Allowed values: related, complementary; `limit` (integer, optional) — Maximum products, defaults to 10 and supports up to 20

### `colehaan_products`

- **HTTP:** `GET /colehaan/products`
- **What:** List Cole Haan products. Returns products from Cole Haan's (https://www.colehaan.com) product catalog. The storefront URL is fixed server-side. Valid empty result pages return `200` with an empty products array.
- **Params:** `limit` (integer, optional) — Maximum products, defaults to 50 and supports up to 250; `page` (integer, optional) — 1-based page, defaults to 1

### `colehaan_search_suggest`

- **HTTP:** `GET /colehaan/search/suggest`
- **What:** Get Cole Haan search suggestions. Returns products, collections, and query suggestions from Cole Haan's (https://www.colehaan.com) predictive search. The storefront URL is fixed server-side.
- **Params:** `limit` (integer, optional) — Maximum results per type, defaults to 10 and supports up to 20; `q` (string, **required**) — Search query; `types` (string, optional) — Comma-separated suggestion types. Allowed values: product, collection, query

### `colehaan_sitemap_urls`

- **HTTP:** `GET /colehaan/sitemap/urls`
- **What:** List Cole Haan sitemap URLs. Returns capped URL entries from Cole Haan's (https://www.colehaan.com) child sitemaps matching the requested type. The storefront URL is fixed server-side.
- **Params:** `limit` (integer, optional) — Maximum URL entries, defaults to 50 and supports up to 250; `type` (string, optional) — Sitemap type. Allowed values: all, products, collections, pages, blogs, agentic_discovery, other

### `colehaan_sitemaps`

- **HTTP:** `GET /colehaan/sitemaps`
- **What:** List Cole Haan sitemaps. Returns child sitemap URLs from Cole Haan's (https://www.colehaan.com) `/sitemap.xml` index with inferred sitemap types. The storefront URL is fixed server-side.
- **Params:** _none_

### `colehaan_store`

- **HTTP:** `GET /colehaan/store`
- **What:** Get Cole Haan store metadata. Returns storefront metadata for Cole Haan (https://www.colehaan.com). The storefront URL is fixed server-side, so no `url` parameter is accepted.
- **Params:** _none_

## Everlane (11)

### `everlane_collection_products`

- **HTTP:** `GET /everlane/collections/{handle}/products`
- **What:** List Everlane collection products. Returns products from one Everlane (https://www.everlane.com) collection. The storefront URL is fixed server-side; `handle` is the collection's URL slug.
- **Params:** `handle` (string, **required**) — Collection handle; `limit` (integer, optional) — Maximum products, defaults to 50 and supports up to 250; `page` (integer, optional) — 1-based page, defaults to 1

### `everlane_collections`

- **HTTP:** `GET /everlane/collections`
- **What:** List Everlane collections. Returns collections from Everlane (https://www.everlane.com). The storefront URL is fixed server-side. Valid empty result pages return `200` with an empty collections array.
- **Params:** `limit` (integer, optional) — Maximum collections, defaults to 50 and supports up to 250; `page` (integer, optional) — 1-based page, defaults to 1

### `everlane_page`

- **HTTP:** `GET /everlane/pages/{handle}`
- **What:** Get a Everlane static page. Returns one Everlane static page by its required `handle`: title, URL, plain-text content, and created, updated and published dates. An unknown handle returns `404`. In a fallback mode flagged by `transport_mode: "ssr_embedded"`, the response omits `id`.
- **Params:** `handle` (string, **required**) — Page handle

### `everlane_pages`

- **HTTP:** `GET /everlane/pages`
- **What:** List Everlane static pages. Lists Everlane static pages, 50 per page by default (`limit`, max 250), with `page` starting at 1. Each page has its handle, title, URL, plain-text content, and created, updated and published dates. In a fallback mode flagged by `transport_mode: "ssr_embedded"`, items carry only `handle`, `url` and `updated_at`.
- **Params:** `limit` (integer, optional) — Maximum static pages, defaults to 50 and supports up to 250; `page` (integer, optional) — 1-based page, defaults to 1

### `everlane_product`

- **HTTP:** `GET /everlane/products/{handle}`
- **What:** Get a Everlane product. Returns product detail for one Everlane (https://www.everlane.com) product handle. The storefront URL is fixed server-side; `handle` is the product's URL slug.
- **Params:** `handle` (string, **required**) — Product handle

### `everlane_product_recommendations`

- **HTTP:** `GET /everlane/products/{handle}/recommendations`
- **What:** List Everlane product recommendations. Returns recommended products for one Everlane (https://www.everlane.com) product handle. The storefront URL is fixed server-side.
- **Params:** `handle` (string, **required**) — Product handle; `intent` (string, optional) — Recommendation intent. Allowed values: related, complementary; `limit` (integer, optional) — Maximum products, defaults to 10 and supports up to 20

### `everlane_products`

- **HTTP:** `GET /everlane/products`
- **What:** List Everlane products. Returns products from Everlane's (https://www.everlane.com) public product catalog. The storefront URL is fixed server-side. Valid empty result pages return `200` with an empty products array.
- **Params:** `limit` (integer, optional) — Maximum products, defaults to 50 and supports up to 250; `page` (integer, optional) — 1-based page, defaults to 1

### `everlane_search_suggest`

- **HTTP:** `GET /everlane/search/suggest`
- **What:** Get Everlane search suggestions. Returns products, collections, and query suggestions from Everlane's (https://www.everlane.com) predictive search. The storefront URL is fixed server-side.
- **Params:** `limit` (integer, optional) — Maximum results per type, defaults to 10 and supports up to 20; `q` (string, **required**) — Search query; `types` (string, optional) — Comma-separated suggestion types. Allowed values: product, collection, query

### `everlane_sitemap_urls`

- **HTTP:** `GET /everlane/sitemap/urls`
- **What:** List Everlane sitemap URLs. Lists URL entries from Everlane's sitemaps, filtered by `type` (`all` by default, or `products`, `collections`, `pages`, `blogs`, `agentic_discovery`, `other`) and capped by `limit` (default 50, max 250). Each entry has its `loc`, inferred type, handle, last modified date, change frequency, and images with caption and title when present.
- **Params:** `limit` (integer, optional) — Maximum URL entries, defaults to 50 and supports up to 250; `type` (string, optional) — Sitemap type. Allowed values: all, products, collections, pages, blogs, agentic_discovery, other

### `everlane_sitemaps`

- **HTTP:** `GET /everlane/sitemaps`
- **What:** List Everlane sitemaps. Lists the child sitemaps in Everlane's sitemap index. Each entry has its `loc` URL and an inferred `type`: `products`, `collections`, `pages`, `blogs`, `agentic_discovery` or `other`. It takes no parameters.
- **Params:** _none_

### `everlane_store`

- **HTTP:** `GET /everlane/store`
- **What:** Get Everlane store metadata. Returns storefront metadata for Everlane (https://www.everlane.com). The storefront URL is fixed server-side, so no `url` parameter is accepted.
- **Params:** _none_

## Fashion Nova (11)

### `fashionnova_collection_products`

- **HTTP:** `GET /fashionnova/collections/{handle}/products`
- **What:** List Fashion Nova collection products. Returns products from one Fashion Nova (https://www.fashionnova.com) collection. The storefront URL is fixed server-side; `handle` is the collection's URL slug.
- **Params:** `handle` (string, **required**) — Collection handle; `limit` (integer, optional) — Maximum products, defaults to 50 and supports up to 250; `page` (integer, optional) — 1-based page, defaults to 1

### `fashionnova_collections`

- **HTTP:** `GET /fashionnova/collections`
- **What:** List Fashion Nova collections. Returns collections from Fashion Nova (https://www.fashionnova.com). The storefront URL is fixed server-side. Valid empty result pages return `200` with an empty collections array.
- **Params:** `limit` (integer, optional) — Maximum collections, defaults to 50 and supports up to 250; `page` (integer, optional) — 1-based page, defaults to 1

### `fashionnova_page`

- **HTTP:** `GET /fashionnova/pages/{handle}`
- **What:** Get a Fashion Nova static page. Returns one Fashion Nova static page by its required `handle`: title, URL, plain-text content, and created, updated and published dates. An unknown handle returns `404`. In a fallback mode flagged by `transport_mode: "ssr_embedded"`, the response omits `id`.
- **Params:** `handle` (string, **required**) — Page handle

### `fashionnova_pages`

- **HTTP:** `GET /fashionnova/pages`
- **What:** List Fashion Nova static pages. Lists Fashion Nova static pages, 50 per page by default (`limit`, max 250), with `page` starting at 1. Each page has its handle, title, URL, plain-text content, and created, updated and published dates. When `transport_mode` is `ssr_embedded`, items carry only `handle`, `url` and `updated_at`. An empty result returns an empty `pages` array.
- **Params:** `limit` (integer, optional) — Maximum static pages, defaults to 50 and supports up to 250; `page` (integer, optional) — 1-based page, defaults to 1

### `fashionnova_product`

- **HTTP:** `GET /fashionnova/products/{handle}`
- **What:** Get a Fashion Nova product. Returns product detail for one Fashion Nova (https://www.fashionnova.com) product handle. The storefront URL is fixed server-side; `handle` is the product's URL slug.
- **Params:** `handle` (string, **required**) — Product handle

### `fashionnova_product_recommendations`

- **HTTP:** `GET /fashionnova/products/{handle}/recommendations`
- **What:** List Fashion Nova product recommendations. Returns recommended products for one Fashion Nova (https://www.fashionnova.com) product handle. The storefront URL is fixed server-side.
- **Params:** `handle` (string, **required**) — Product handle; `intent` (string, optional) — Recommendation intent. Allowed values: related, complementary; `limit` (integer, optional) — Maximum products, defaults to 10 and supports up to 20

### `fashionnova_products`

- **HTTP:** `GET /fashionnova/products`
- **What:** List Fashion Nova products. Returns products from Fashion Nova's (https://www.fashionnova.com) public product catalog. The storefront URL is fixed server-side. Valid empty result pages return `200` with an empty products array.
- **Params:** `limit` (integer, optional) — Maximum products, defaults to 50 and supports up to 250; `page` (integer, optional) — 1-based page, defaults to 1

### `fashionnova_search_suggest`

- **HTTP:** `GET /fashionnova/search/suggest`
- **What:** Get Fashion Nova search suggestions. Returns products, collections, and query suggestions from Fashion Nova's (https://www.fashionnova.com) predictive search. The storefront URL is fixed server-side.
- **Params:** `limit` (integer, optional) — Maximum results per type, defaults to 10 and supports up to 20; `q` (string, **required**) — Search query; `types` (string, optional) — Comma-separated suggestion types. Allowed values: product, collection, query

### `fashionnova_sitemap_urls`

- **HTTP:** `GET /fashionnova/sitemap/urls`
- **What:** List Fashion Nova sitemap URLs. Returns capped URL entries from Fashion Nova's (https://www.fashionnova.com) child sitemaps matching the requested type. The storefront URL is fixed server-side.
- **Params:** `limit` (integer, optional) — Maximum URL entries, defaults to 50 and supports up to 250; `type` (string, optional) — Sitemap type. Allowed values: all, products, collections, pages, blogs, agentic_discovery, other

### `fashionnova_sitemaps`

- **HTTP:** `GET /fashionnova/sitemaps`
- **What:** List Fashion Nova sitemaps. Returns child sitemap URLs from Fashion Nova's (https://www.fashionnova.com) `/sitemap.xml` index with inferred sitemap types. The storefront URL is fixed server-side.
- **Params:** _none_

### `fashionnova_store`

- **HTTP:** `GET /fashionnova/store`
- **What:** Get Fashion Nova store metadata. Returns storefront metadata for Fashion Nova (https://www.fashionnova.com). The storefront URL is fixed server-side, so no `url` parameter is accepted.
- **Params:** _none_

## Gymshark (10)

### `gymshark_collection_products`

- **HTTP:** `GET /gymshark/collections/{handle}/products`
- **What:** List Gymshark collection products. Returns products from one Gymshark (https://row.gymshark.com) collection. The storefront URL is fixed server-side; `handle` is the collection's URL slug.
- **Params:** `handle` (string, **required**) — Collection handle; `limit` (integer, optional) — Maximum products, defaults to 50 and supports up to 250; `page` (integer, optional) — 1-based page, defaults to 1

### `gymshark_collections`

- **HTTP:** `GET /gymshark/collections`
- **What:** List Gymshark collections. Returns collections from Gymshark (https://row.gymshark.com). The storefront URL is fixed server-side. Valid empty result pages return `200` with an empty collections array.
- **Params:** `limit` (integer, optional) — Maximum collections, defaults to 50 and supports up to 250; `page` (integer, optional) — 1-based page, defaults to 1

### `gymshark_page`

- **HTTP:** `GET /gymshark/pages/{handle}`
- **What:** Get a Gymshark static page. Returns one Gymshark static page by its `handle`, such as `sports-bras`: title, handle, URL, plain-text content, and created, published and updated times. Page HTML is not returned. An unknown handle returns a 404. `id` is absent when `transport_mode` is `ssr_embedded`.
- **Params:** `handle` (string, **required**) — Page handle

### `gymshark_pages`

- **HTTP:** `GET /gymshark/pages`
- **What:** List Gymshark static pages. Lists Gymshark static pages, 50 per page by default (`limit` up to 250) with a 1-based `page`. Each has its handle, title, URL, plain-text content and timestamps. When `transport_mode` is `ssr_embedded`, items carry only `handle`, `url` and `updated_at`.
- **Params:** `limit` (integer, optional) — Maximum static pages, defaults to 50 and supports up to 250; `page` (integer, optional) — 1-based page, defaults to 1

### `gymshark_product`

- **HTTP:** `GET /gymshark/products/{handle}`
- **What:** Get a Gymshark product. Returns product detail for one Gymshark (https://row.gymshark.com) product handle. The storefront URL is fixed server-side; `handle` is the product's URL slug.
- **Params:** `handle` (string, **required**) — Product handle

### `gymshark_product_recommendations`

- **HTTP:** `GET /gymshark/products/{handle}/recommendations`
- **What:** List Gymshark product recommendations. Returns recommended products for one Gymshark (https://row.gymshark.com) product handle. The storefront URL is fixed server-side.
- **Params:** `handle` (string, **required**) — Product handle; `intent` (string, optional) — Recommendation intent. Allowed values: related, complementary; `limit` (integer, optional) — Maximum products, defaults to 10 and supports up to 20

### `gymshark_products`

- **HTTP:** `GET /gymshark/products`
- **What:** List Gymshark products. Returns products from Gymshark's (https://row.gymshark.com) public product catalog. The storefront URL is fixed server-side. Valid empty result pages return `200` with an empty products array.
- **Params:** `limit` (integer, optional) — Maximum products, defaults to 50 and supports up to 250; `page` (integer, optional) — 1-based page, defaults to 1

### `gymshark_sitemap_urls`

- **HTTP:** `GET /gymshark/sitemap/urls`
- **What:** List Gymshark sitemap URLs. Lists URL entries from Gymshark's sitemaps, filtered by `type` (`all` by default, `products`, `collections`, `pages`, `blogs`, `agentic_discovery` or `other`) and capped by `limit` (default 50, max 250). Each has its `loc`, type, handle, last modified date, change frequency and any images.
- **Params:** `limit` (integer, optional) — Maximum URL entries, defaults to 50 and supports up to 250; `type` (string, optional) — Sitemap type. Allowed values: all, products, collections, pages, blogs, agentic_discovery, other

### `gymshark_sitemaps`

- **HTTP:** `GET /gymshark/sitemaps`
- **What:** List Gymshark sitemaps. Lists the child sitemaps in Gymshark's sitemap index. Each entry has its `loc` and a type of `products`, `collections`, `pages`, `blogs`, `agentic_discovery` or `other`. The type is worked out from the sitemap URL.
- **Params:** _none_

### `gymshark_store`

- **HTTP:** `GET /gymshark/store`
- **What:** Get Gymshark store metadata. Returns storefront metadata for Gymshark (https://row.gymshark.com). The storefront URL is fixed server-side, so no `url` parameter is accepted.
- **Params:** _none_

## J.Crew (8)

### `jcrew_categories`

- **HTTP:** `GET /jcrew/categories`
- **What:** List J.Crew or J.Crew Factory categories. Lists every category and subcategory from the storefront's own header navigation, flattened into department/section/category triples -- resolves the category-discovery gap jcrew-category's own category parameter otherwise leaves as "find one from a storefront URL". Each entry's category value is exactly what jcrew-category's own category parameter accepts. Filter to one department with department (e.g. women, men); omit for every department. Departments vary slightly by site (jcrew.com has an extra "home" department factory.jcrew.com doesn't) -- see the response's own departments field for the live list.
- **Params:** `department` (string, optional) — Department to filter to, e.g. women, men, boys, girls, accessories, shoes, home (jcrew only) -- omit for every department; `site` (string, optional) — Storefront to list

### `jcrew_category`

- **HTTP:** `GET /jcrew/category`
- **What:** Browse a J.Crew or J.Crew Factory category. Returns one page (up to 60 products) of a category/browse listing for a category path. category is the slash-separated path segment after the storefront's own /plp/ (e.g. womens/categories/clothing/sweaters) -- use jcrew-categories to discover every valid value instead of guessing from storefront URLs. site selects the storefront (default jcrew). page selects the SFCC-native page (default 1); result_count reports the upstream's true total regardless of page size. A hub-level (non-leaf) category path returns a well-formed empty result rather than an error.
- **Params:** `category` (string, **required**) — Slash-separated category path -- see jcrew-categories; `page` (integer, optional) — One-based page; `site` (string, optional) — Storefront to browse

### `jcrew_product`

- **HTTP:** `GET /jcrew/product`
- **What:** Get a J.Crew or J.Crew Factory product. Returns full product detail for one style: name, brand, description, category, list price, aggregate rating, every purchasable color, and every color+size combination as a separate priced/stocked SKU. pid is a style id (e.g. CX415), as returned by jcrew-search's products[].id field. site must match the storefront the pid belongs to (default jcrew). A single call covers every color and size of the style -- no per-color lookup needed.
- **Params:** `pid` (string, **required**) — Style id, from a search result's id field; `site` (string, optional) — Storefront the pid belongs to

### `jcrew_product_reviews`

- **HTTP:** `GET /jcrew/product/reviews`
- **What:** Get reviews for a J.Crew or J.Crew Factory product. Returns one page of a product's customer reviews (author, location, date, rating, headline, body, and verified-purchase flag), plus the product's overall rating summary (average rating, rating count, per-star histogram, and recommended ratio). pid is a style id (e.g. CX415), as returned by jcrew-search's products[].id field. site must match the storefront the pid belongs to (default jcrew). A product with no reviews yet, or a well-formed but unrecognized pid, returns a well-formed empty result, not an error.
- **Params:** `page` (integer, optional) — One-based page, 10 reviews per page; `pid` (string, **required**) — Style id, from a search result's id field; `site` (string, optional) — Storefront the pid belongs to

### `jcrew_search`

- **HTTP:** `GET /jcrew/search`
- **What:** Search J.Crew or J.Crew Factory products. Searches the product catalog for either storefront (select with site, default jcrew). Returns product summaries with USD pricing, gender, and a description, plus the search index's own facets (gender, fabric, category, size, color, price range, and others) with live per-option counts. sort selects relevance (default), price_asc, or price_desc. filter narrows results by one or more facet name:value pairs (comma-separated, e.g. productGender:Men,styleFabric:Cashmere) taken from a prior response's own facets[].name/facets[].options[].value fields -- not curated against a fixed list, since the facet set is large and can change. This is best-effort relevance, not a guaranteed keyword match: for an obscure alphanumeric keyword the search index falls back to its own semantically-related results instead of an empty list, and there is no reliable field in the response to distinguish a true keyword match from that fallback.
- **Params:** `filter` (string, optional) — Comma-separated facet name:value pairs, e.g. productGender:Men,styleFabric:Cashmere; `keyword` (string, **required**) — Search keyword; `page` (integer, optional) — One-based page; `per_page` (integer, optional) — Results per page; `site` (string, optional) — Storefront to search; `sort` (string, optional) — Sort order

### `jcrew_size_chart`

- **HTTP:** `GET /jcrew/size-chart`
- **What:** Get the size chart for a J.Crew or J.Crew Factory product. Returns real body measurements per size (chest, waist, hip, sleeve, length, or a subset depending on the style/category), in both inches and centimeters. pid is a style id, as returned by jcrew-search's products[].id field. site must match the storefront the pid belongs to (default jcrew). A measurement value of 0 means that column doesn't apply to this style (e.g. hip on a top) -- the upstream itself doesn't distinguish that from a genuine zero, so this endpoint passes it through as-is.
- **Params:** `pid` (string, **required**) — Style id, from a search result's id field; `site` (string, optional) — Storefront the pid belongs to

### `jcrew_stores`

- **HTTP:** `GET /jcrew/stores`
- **What:** Find J.Crew or J.Crew Factory store locations. Returns one storefront's full open-store directory (address, phone, coordinates, services, weekly hours). site selects the storefront and accepts jcrew or factory; defaults to jcrew. Give lat and lng together to sort by distance from that point (each store's distance_miles is then populated); omit both for the upstream's own order.
- **Params:** `lat` (number, optional) — Latitude to sort distance from (must be given together with lng); `lng` (number, optional) — Longitude to sort distance from (must be given together with lat); `site` (string, optional) — Storefront whose stores to return

### `jcrew_suggest`

- **HTTP:** `GET /jcrew/suggest`
- **What:** Get J.Crew or J.Crew Factory search-box suggestions. Returns the storefront's own search-box suggestions (typeahead) for a partial query -- a flat list of suggested search phrases, each with its own live total result count on the search index. Select the storefront with site (default jcrew). Not product data.
- **Params:** `query` (string, **required**) — Partial search query; `site` (string, optional) — Storefront to search

## Kylie Cosmetics (11)

### `kyliecosmetics_collection_products`

- **HTTP:** `GET /kyliecosmetics/collections/{handle}/products`
- **What:** List Kylie Cosmetics collection products. Returns products from one Kylie Cosmetics (https://www.kyliecosmetics.com) collection. The storefront URL is fixed server-side; `handle` is the collection's URL slug.
- **Params:** `handle` (string, **required**) — Collection handle; `limit` (integer, optional) — Maximum products, defaults to 50 and supports up to 250; `page` (integer, optional) — 1-based page, defaults to 1

### `kyliecosmetics_collections`

- **HTTP:** `GET /kyliecosmetics/collections`
- **What:** List Kylie Cosmetics collections. Returns collections from Kylie Cosmetics (https://www.kyliecosmetics.com). The storefront URL is fixed server-side. Valid empty result pages return `200` with an empty collections array.
- **Params:** `limit` (integer, optional) — Maximum collections, defaults to 50 and supports up to 250; `page` (integer, optional) — 1-based page, defaults to 1

### `kyliecosmetics_page`

- **HTTP:** `GET /kyliecosmetics/pages/{handle}`
- **What:** Get a Kylie Cosmetics static page. Returns one static page from the Kylie Cosmetics store by `handle`. The response has the page id, title, URL, handle, plain-text content, and created, updated and published times. Content is text, not HTML. In some cases `transport_mode` is `ssr_embedded` and `id` is omitted. An unknown handle returns `404`.
- **Params:** `handle` (string, **required**) — Page handle

### `kyliecosmetics_pages`

- **HTTP:** `GET /kyliecosmetics/pages`
- **What:** List Kylie Cosmetics static pages. Lists static pages from the Kylie Cosmetics store, paged with `page` (default 1) and `limit` (default 50, max 250). Each page has its id, handle, title, URL, plain-text content and timestamps. When `transport_mode` is `ssr_embedded`, items carry only `handle`, `url` and `updated_at`.
- **Params:** `limit` (integer, optional) — Maximum static pages, defaults to 50 and supports up to 250; `page` (integer, optional) — 1-based page, defaults to 1

### `kyliecosmetics_product`

- **HTTP:** `GET /kyliecosmetics/products/{handle}`
- **What:** Get a Kylie Cosmetics product. Returns product detail for one Kylie Cosmetics (https://www.kyliecosmetics.com) product handle. The storefront URL is fixed server-side; `handle` is the product's URL slug.
- **Params:** `handle` (string, **required**) — Product handle

### `kyliecosmetics_product_recommendations`

- **HTTP:** `GET /kyliecosmetics/products/{handle}/recommendations`
- **What:** List Kylie Cosmetics product recommendations. Returns recommended products for one Kylie Cosmetics (https://www.kyliecosmetics.com) product handle. The storefront URL is fixed server-side.
- **Params:** `handle` (string, **required**) — Product handle; `intent` (string, optional) — Recommendation intent. Allowed values: related, complementary; `limit` (integer, optional) — Maximum products, defaults to 10 and supports up to 20

### `kyliecosmetics_products`

- **HTTP:** `GET /kyliecosmetics/products`
- **What:** List Kylie Cosmetics products. Returns products from Kylie Cosmetics's (https://www.kyliecosmetics.com) public product catalog. The storefront URL is fixed server-side. Valid empty result pages return `200` with an empty products array.
- **Params:** `limit` (integer, optional) — Maximum products, defaults to 50 and supports up to 250; `page` (integer, optional) — 1-based page, defaults to 1

### `kyliecosmetics_search_suggest`

- **HTTP:** `GET /kyliecosmetics/search/suggest`
- **What:** Get Kylie Cosmetics search suggestions. Returns products, collections, and query suggestions from Kylie Cosmetics's (https://www.kyliecosmetics.com) predictive search. The storefront URL is fixed server-side.
- **Params:** `limit` (integer, optional) — Maximum results per type, defaults to 10 and supports up to 20; `q` (string, **required**) — Search query; `types` (string, optional) — Comma-separated suggestion types. Allowed values: product, collection, query

### `kyliecosmetics_sitemap_urls`

- **HTTP:** `GET /kyliecosmetics/sitemap/urls`
- **What:** List Kylie Cosmetics sitemap URLs. Returns capped URL entries from Kylie Cosmetics's (https://www.kyliecosmetics.com) child sitemaps matching the requested type. The storefront URL is fixed server-side.
- **Params:** `limit` (integer, optional) — Maximum URL entries, defaults to 50 and supports up to 250; `type` (string, optional) — Sitemap type. Allowed values: all, products, collections, pages, blogs, agentic_discovery, other

### `kyliecosmetics_sitemaps`

- **HTTP:** `GET /kyliecosmetics/sitemaps`
- **What:** List Kylie Cosmetics sitemaps. Returns child sitemap URLs from Kylie Cosmetics's (https://www.kyliecosmetics.com) `/sitemap.xml` index with inferred sitemap types. The storefront URL is fixed server-side.
- **Params:** _none_

### `kyliecosmetics_store`

- **HTTP:** `GET /kyliecosmetics/store`
- **What:** Get Kylie Cosmetics store metadata. Returns storefront metadata for Kylie Cosmetics (https://www.kyliecosmetics.com). The storefront URL is fixed server-side, so no `url` parameter is accepted.
- **Params:** _none_

## Oh Polly (11)

### `ohpolly_collection_products`

- **HTTP:** `GET /ohpolly/collections/{handle}/products`
- **What:** List Oh Polly collection products. Returns products from one Oh Polly (https://www.ohpolly.com) collection. The storefront URL is fixed server-side; `handle` is the collection's URL slug.
- **Params:** `handle` (string, **required**) — Collection handle; `limit` (integer, optional) — Maximum products, defaults to 50 and supports up to 250; `page` (integer, optional) — 1-based page, defaults to 1

### `ohpolly_collections`

- **HTTP:** `GET /ohpolly/collections`
- **What:** List Oh Polly collections. Returns collections from Oh Polly (https://www.ohpolly.com). The storefront URL is fixed server-side. Valid empty result pages return `200` with an empty collections array.
- **Params:** `limit` (integer, optional) — Maximum collections, defaults to 50 and supports up to 250; `page` (integer, optional) — 1-based page, defaults to 1

### `ohpolly_page`

- **HTTP:** `GET /ohpolly/pages/{handle}`
- **What:** Get a Oh Polly static page. Returns one Oh Polly static page by its `handle`: title, page URL, plain-text content, and created, published and updated times. Content is cleaned text, not HTML. An unknown handle returns 404. The store is fixed to Oh Polly, so no store URL is needed. Some responses include `transport_mode` set to `ssr_embedded` and omit `id`.
- **Params:** `handle` (string, **required**) — Page handle

### `ohpolly_pages`

- **HTTP:** `GET /ohpolly/pages`
- **What:** List Oh Polly static pages. Lists Oh Polly's static pages, paged with `page` (default 1) and `limit` (default 50, max 250). Each page has its handle, title, URL, plain-text content and timestamps. In some responses `transport_mode` is `ssr_embedded` and items carry only `handle`, `url` and `updated_at`, so fetch a single page for its content.
- **Params:** `limit` (integer, optional) — Maximum static pages, defaults to 50 and supports up to 250; `page` (integer, optional) — 1-based page, defaults to 1

### `ohpolly_product`

- **HTTP:** `GET /ohpolly/products/{handle}`
- **What:** Get a Oh Polly product. Returns product detail for one Oh Polly (https://www.ohpolly.com) product handle. The storefront URL is fixed server-side; `handle` is the product's URL slug.
- **Params:** `handle` (string, **required**) — Product handle

### `ohpolly_product_recommendations`

- **HTTP:** `GET /ohpolly/products/{handle}/recommendations`
- **What:** List Oh Polly product recommendations. Returns recommended products for one Oh Polly (https://www.ohpolly.com) product handle. The storefront URL is fixed server-side.
- **Params:** `handle` (string, **required**) — Product handle; `intent` (string, optional) — Recommendation intent. Allowed values: related, complementary; `limit` (integer, optional) — Maximum products, defaults to 10 and supports up to 20

### `ohpolly_products`

- **HTTP:** `GET /ohpolly/products`
- **What:** List Oh Polly products. Returns products from Oh Polly's (https://www.ohpolly.com) public product catalog. The storefront URL is fixed server-side. Valid empty result pages return `200` with an empty products array.
- **Params:** `limit` (integer, optional) — Maximum products, defaults to 50 and supports up to 250; `page` (integer, optional) — 1-based page, defaults to 1

### `ohpolly_search_suggest`

- **HTTP:** `GET /ohpolly/search/suggest`
- **What:** Get Oh Polly search suggestions. Returns products, collections, and query suggestions from Oh Polly's (https://www.ohpolly.com) predictive search. The storefront URL is fixed server-side.
- **Params:** `limit` (integer, optional) — Maximum results per type, defaults to 10 and supports up to 20; `q` (string, **required**) — Search query; `types` (string, optional) — Comma-separated suggestion types. Allowed values: product, collection, query

### `ohpolly_sitemap_urls`

- **HTTP:** `GET /ohpolly/sitemap/urls`
- **What:** List Oh Polly sitemap URLs. Returns capped URL entries from Oh Polly's (https://www.ohpolly.com) child sitemaps matching the requested type. The storefront URL is fixed server-side.
- **Params:** `limit` (integer, optional) — Maximum URL entries, defaults to 50 and supports up to 250; `type` (string, optional) — Sitemap type. Allowed values: all, products, collections, pages, blogs, agentic_discovery, other

### `ohpolly_sitemaps`

- **HTTP:** `GET /ohpolly/sitemaps`
- **What:** List Oh Polly sitemaps. Returns child sitemap URLs from Oh Polly's (https://www.ohpolly.com) `/sitemap.xml` index with inferred sitemap types. The storefront URL is fixed server-side.
- **Params:** _none_

### `ohpolly_store`

- **HTTP:** `GET /ohpolly/store`
- **What:** Get Oh Polly store metadata. Returns storefront metadata for Oh Polly (https://www.ohpolly.com). The storefront URL is fixed server-side, so no `url` parameter is accepted.
- **Params:** _none_

## Quince (9)

### `quince_categories`

- **HTTP:** `GET /quince/categories`
- **What:** List Quince's product facet taxonomy. Returns Quince's full product facet taxonomy: every business department (Women, Men, Kids & Baby, Home, CPG, Emerging), department, category, material, primary color, and size value Quince currently has products for, each with its own live product count. The returned business_departments[].value/categories[].value/materials[].value/colors[].value/sizes[].value values are exactly what quince-search accepts as its own department/category/material/color/size parameters. sizes spans every product type Quince sells (apparel letter sizes, shoe sizes, rug/furniture dimensions, bedding sizes, and more) since it is one catalog-wide facet.
- **Params:** _none_

### `quince_navigation`

- **HTTP:** `GET /quince/navigation`
- **What:** Get Quince's header navigation menu. Returns Quince's full header navigation mega-menu: top-level tabs (Women, Men, Home, Baby & Kids, Travel, Bags & Accessories, Jewelry, Beauty & Wellness, Gifts, plus promotional tabs like New Arrivals/Best Sellers/$50 Cashmere), each broken into the same named subcategory groups (for example Apparel, Jewelry, Shoes) shown in Quince's own nav dropdown, with a directly browsable slug on every category and link. This is a distinct taxonomy from quince-categories' facets: navigation is Quince's own curated site structure, while quince-categories reports live per-value product counts for quince-search's own filter parameters.
- **Params:** _none_

### `quince_product`

- **HTTP:** `GET /quince/product`
- **What:** Get a Quince product. Returns product-detail data for one Quince product: title, description, review summary, every selectable option (color swatches with hex codes, sizes), and every color/size variant with its own price, original ("traditional retail") price, stock status, and SKU. handle is the product's URL path on quince.com (for example women/cashmere/cashmere-crewneck-sweater), returned by quince-search's own products[].handle field.
- **Params:** `handle` (string, **required**) — Product URL handle, from a search result's products[].handle field

### `quince_product_faq`

- **HTTP:** `GET /quince/product/faq`
- **What:** Get a Quince product's FAQ content. Returns a Quince product's own question/answer content (e.g. sizing, care, fit), from the same structured product data quince-product-reviews uses. handle is the same value quince-product accepts. Not every product carries FAQ content -- a product with none returns a well-formed empty result.
- **Params:** `handle` (string, **required**) — Product URL handle, from a search result's products[].handle field

### `quince_product_reviews`

- **HTTP:** `GET /quince/product/reviews`
- **What:** Get Quince product reviews. Returns a sample of a Quince product's customer reviews (author, date, rating, review body), plus the product's overall aggregate rating and review count. handle is the same value quince-product accepts. The reviews returned are a sample (25 reviews on every product sampled), not a paginated feed of the full review history. A product with no reviews yet returns a well-formed empty result.
- **Params:** `handle` (string, **required**) — Product URL handle, from a search result's products[].handle field

### `quince_search`

- **HTTP:** `GET /quince/search`
- **What:** Search or browse Quince products. Searches or browses Quince's (quince.com) product catalog. q, department, category, material, color, size, min_price, and max_price are all optional and combine as an AND -- unlike some other families' search/category-browse split, a free-text q can be combined with any of the facet filters in the same request, or every field can be omitted to browse the full catalog by Quince's own relevance/popularity ranking. department accepts one of the values quince-categories' own business_departments[].value field returns (for example Women, Men, Kids & Baby, Home, CPG, Emerging); category, material, color, and size similarly accept values from quince-categories' own categories[].value/materials[].value/colors[].value/sizes[].value fields (or quince-navigation's own browsable category/subcategory slugs for a curated, hierarchical alternative to the flat category facet). Keyword search uses typo-tolerant relevance ranking, not a guaranteed exact match. A query with genuinely zero matches (for example a nonsense string) returns a well-formed empty result rather than an error.
- **Params:** `category` (string, optional) — Category facet filter, from quince-categories' own categories[].value field; `color` (string, optional) — Primary color facet filter, from quince-categories' own colors[].value field; `department` (string, optional) — Business department facet filter, from quince-categories' own business_departments[].value field; `limit` (integer, optional) — Results per page, defaults to 24, maximum 100; `material` (string, optional) — Material facet filter, from quince-categories' own materials[].value field; `max_price` (number, optional) — Maximum price (inclusive), in USD; `min_price` (number, optional) — Minimum price (inclusive), in USD; `page` (integer, optional) — One-based page number, defaults to 1; `q` (string, optional) — Free-text search query; `size` (string, optional) — Size facet filter, from quince-categories' own sizes[].value field

### `quince_sitemap_urls`

- **HTTP:** `GET /quince/sitemap/urls`
- **What:** List Quince sitemap URLs. Returns capped URL entries from Quince's own sitemaps matching the requested type. Each entry's handle is populated from the URL's own path (tracking/variant query parameters stripped) -- for type products, this is directly the value quince-product's own handle parameter expects.
- **Params:** `limit` (integer, optional) — Maximum URL entries, defaults to 50 and supports up to 250; `type` (string, optional) — Sitemap type. Allowed values: all, products, collections, subcollections, pages

### `quince_sitemaps`

- **HTTP:** `GET /quince/sitemaps`
- **What:** List Quince sitemaps. Returns Quince's US-region child sitemaps (products, collections, subcollections, and static pages) with an inferred type, from quince.com's own public sitemap index.
- **Params:** _none_

### `quince_suggest`

- **HTTP:** `GET /quince/suggest`
- **What:** Get Quince search suggestions. Returns Quince's own search-box typeahead suggestions for a partial query: a flat list of suggested search phrases, no product data. Pass a suggestion straight through to quince-search's own q parameter for product results. A query with no genuine matches returns a well-formed empty result rather than an error.
- **Params:** `q` (string, **required**) — Search query prefix

## Rothy's (11)

### `rothys_collection_products`

- **HTTP:** `GET /rothys/collections/{handle}/products`
- **What:** List Rothy's collection products. Returns products from one Rothy's (https://www.rothys.com) collection. The storefront URL is fixed server-side; `handle` is the collection's URL slug.
- **Params:** `handle` (string, **required**) — Collection handle; `limit` (integer, optional) — Maximum products, defaults to 50 and supports up to 250; `page` (integer, optional) — 1-based page, defaults to 1

### `rothys_collections`

- **HTTP:** `GET /rothys/collections`
- **What:** List Rothy's collections. Returns collections from Rothy's (https://www.rothys.com). The storefront URL is fixed server-side. Valid empty result pages return `200` with an empty collections array.
- **Params:** `limit` (integer, optional) — Maximum collections, defaults to 50 and supports up to 250; `page` (integer, optional) — 1-based page, defaults to 1

### `rothys_page`

- **HTTP:** `GET /rothys/pages/{handle}`
- **What:** Get a Rothy's static page. Returns a single Rothy's static page for the given `handle`: its title, URL, created, published and updated times, and body as plain text in `content`. A handle that does not exist returns 404. In `ssr_embedded` mode `id` is absent, because that source has no numeric id.
- **Params:** `handle` (string, **required**) — Page handle

### `rothys_pages`

- **HTTP:** `GET /rothys/pages`
- **What:** List Rothy's static pages. Lists static pages from Rothy's. `page` starts at 1 and `limit` defaults to 50, up to 250. Each item has `handle`, `title`, `url`, plain-text `content` and dates. A valid but empty page returns an empty `pages` array. With `transport_mode` set to `ssr_embedded`, items hold only `handle`, `url` and `updated_at`.
- **Params:** `limit` (integer, optional) — Maximum static pages, defaults to 50 and supports up to 250; `page` (integer, optional) — 1-based page, defaults to 1

### `rothys_product`

- **HTTP:** `GET /rothys/products/{handle}`
- **What:** Get a Rothy's product. Returns product detail for one Rothy's (https://www.rothys.com) product handle. The storefront URL is fixed server-side; `handle` is the product's URL slug.
- **Params:** `handle` (string, **required**) — Product handle

### `rothys_product_recommendations`

- **HTTP:** `GET /rothys/products/{handle}/recommendations`
- **What:** List Rothy's product recommendations. Returns recommended products for one Rothy's (https://www.rothys.com) product handle. The storefront URL is fixed server-side.
- **Params:** `handle` (string, **required**) — Product handle; `intent` (string, optional) — Recommendation intent. Allowed values: related, complementary; `limit` (integer, optional) — Maximum products, defaults to 10 and supports up to 20

### `rothys_products`

- **HTTP:** `GET /rothys/products`
- **What:** List Rothy's products. Returns products from Rothy's's (https://www.rothys.com) public product catalog. The storefront URL is fixed server-side. Valid empty result pages return `200` with an empty products array.
- **Params:** `limit` (integer, optional) — Maximum products, defaults to 50 and supports up to 250; `page` (integer, optional) — 1-based page, defaults to 1

### `rothys_search_suggest`

- **HTTP:** `GET /rothys/search/suggest`
- **What:** Get Rothy's search suggestions. Returns products, collections, and query suggestions from Rothy's's (https://www.rothys.com) predictive search. The storefront URL is fixed server-side.
- **Params:** `limit` (integer, optional) — Maximum results per type, defaults to 10 and supports up to 20; `q` (string, **required**) — Search query; `types` (string, optional) — Comma-separated suggestion types. Allowed values: product, collection, query

### `rothys_sitemap_urls`

- **HTTP:** `GET /rothys/sitemap/urls`
- **What:** List Rothy's sitemap URLs. Lists URL entries from Rothy's sitemaps for one `type` (`all` by default, or `products`, `collections`, `pages`, `blogs`, `agentic_discovery`, `other`), up to `limit` entries (default 50, max 250). Each has `loc`, `type`, `handle`, `lastmod`, `changefreq` and optional `images`.
- **Params:** `limit` (integer, optional) — Maximum URL entries, defaults to 50 and supports up to 250; `type` (string, optional) — Sitemap type. Allowed values: all, products, collections, pages, blogs, agentic_discovery, other

### `rothys_sitemaps`

- **HTTP:** `GET /rothys/sitemaps`
- **What:** List Rothy's sitemaps. Lists the child sitemaps in Rothy's sitemap index, each with its `loc` and a `type` (`products`, `collections`, `pages`, `blogs`, `agentic_discovery` or `other`) inferred from the URL. No parameters are needed.
- **Params:** _none_

### `rothys_store`

- **HTTP:** `GET /rothys/store`
- **What:** Get Rothy's store metadata. Returns storefront metadata for Rothy's (https://www.rothys.com). The storefront URL is fixed server-side, so no `url` parameter is accepted.
- **Params:** _none_

## SKIMS (11)

### `skims_collection_products`

- **HTTP:** `GET /skims/collections/{handle}/products`
- **What:** List SKIMS collection products. Returns products from one SKIMS (https://skims.com) collection. The storefront URL is fixed server-side; `handle` is the collection's URL slug.
- **Params:** `handle` (string, **required**) — Collection handle; `limit` (integer, optional) — Maximum products, defaults to 50 and supports up to 250; `page` (integer, optional) — 1-based page, defaults to 1

### `skims_collections`

- **HTTP:** `GET /skims/collections`
- **What:** List SKIMS collections. Returns collections from SKIMS (https://skims.com). The storefront URL is fixed server-side. Valid empty result pages return `200` with an empty collections array.
- **Params:** `limit` (integer, optional) — Maximum collections, defaults to 50 and supports up to 250; `page` (integer, optional) — 1-based page, defaults to 1

### `skims_page`

- **HTTP:** `GET /skims/pages/{handle}`
- **What:** Get a SKIMS static page. Returns one SKIMS static page by its `handle`: id, title, URL, plain-text `content` and the created, published and updated timestamps. Page text is cleaned, not raw HTML. An unknown handle returns 404. When the reduced form is served, `transport_mode` is `ssr_embedded` and `id` is omitted.
- **Params:** `handle` (string, **required**) — Page handle

### `skims_pages`

- **HTTP:** `GET /skims/pages`
- **What:** List SKIMS static pages. Lists SKIMS static pages, 50 per request by default (`limit` up to 250), with `page` starting at 1. Each page has its handle, title, URL, plain-text content and timestamps. An empty result is a normal 200. When `transport_mode` is `ssr_embedded`, items carry only `handle`, `url` and `updated_at`.
- **Params:** `limit` (integer, optional) — Maximum static pages, defaults to 50 and supports up to 250; `page` (integer, optional) — 1-based page, defaults to 1

### `skims_product`

- **HTTP:** `GET /skims/products/{handle}`
- **What:** Get a SKIMS product. Returns product detail for one SKIMS (https://skims.com) product handle. The storefront URL is fixed server-side; `handle` is the product's URL slug.
- **Params:** `handle` (string, **required**) — Product handle

### `skims_product_recommendations`

- **HTTP:** `GET /skims/products/{handle}/recommendations`
- **What:** List SKIMS product recommendations. Returns recommended products for one SKIMS (https://skims.com) product handle. The storefront URL is fixed server-side.
- **Params:** `handle` (string, **required**) — Product handle; `intent` (string, optional) — Recommendation intent. Allowed values: related, complementary; `limit` (integer, optional) — Maximum products, defaults to 10 and supports up to 20

### `skims_products`

- **HTTP:** `GET /skims/products`
- **What:** List SKIMS products. Returns products from SKIMS's (https://skims.com) public product catalog. The storefront URL is fixed server-side. Valid empty result pages return `200` with an empty products array.
- **Params:** `limit` (integer, optional) — Maximum products, defaults to 50 and supports up to 250; `page` (integer, optional) — 1-based page, defaults to 1

### `skims_search_suggest`

- **HTTP:** `GET /skims/search/suggest`
- **What:** Get SKIMS search suggestions. Returns products, collections, and query suggestions from SKIMS's (https://skims.com) predictive search. The storefront URL is fixed server-side.
- **Params:** `limit` (integer, optional) — Maximum results per type, defaults to 10 and supports up to 20; `q` (string, **required**) — Search query; `types` (string, optional) — Comma-separated suggestion types. Allowed values: product, collection, query

### `skims_sitemap_urls`

- **HTTP:** `GET /skims/sitemap/urls`
- **What:** List SKIMS sitemap URLs. Lists URL entries from SKIMS sitemaps, filtered by `type` (`all` by default, or `products`, `collections`, `pages`, `blogs`, `agentic_discovery`, `other`). Stops at `limit` entries (default 50, max 250). Each entry has `loc`, its type, handle, `lastmod`, `changefreq` and, where present, images with caption and title.
- **Params:** `limit` (integer, optional) — Maximum URL entries, defaults to 50 and supports up to 250; `type` (string, optional) — Sitemap type. Allowed values: all, products, collections, pages, blogs, agentic_discovery, other

### `skims_sitemaps`

- **HTTP:** `GET /skims/sitemaps`
- **What:** List SKIMS sitemaps. Lists the child sitemaps in the SKIMS sitemap index, each with its `loc` URL and a `type` of `products`, `collections`, `pages`, `blogs`, `agentic_discovery` or `other`. Takes no parameters. Use it to see which sitemap files exist before listing their URLs.
- **Params:** _none_

### `skims_store`

- **HTTP:** `GET /skims/store`
- **What:** Get SKIMS store metadata. Returns storefront metadata for SKIMS (https://skims.com). The storefront URL is fixed server-side, so no `url` parameter is accepted.
- **Params:** _none_

## Steve Madden (11)

### `stevemadden_collection_products`

- **HTTP:** `GET /stevemadden/collections/{handle}/products`
- **What:** List Steve Madden collection products. Returns products from one Steve Madden (https://www.stevemadden.com) collection. The storefront URL is fixed; `handle` is the collection's URL slug.
- **Params:** `handle` (string, **required**) — Collection handle; `limit` (integer, optional) — Maximum products, defaults to 50 and supports up to 250; `page` (integer, optional) — 1-based page, defaults to 1

### `stevemadden_collections`

- **HTTP:** `GET /stevemadden/collections`
- **What:** List Steve Madden collections. Returns collections from Steve Madden (https://www.stevemadden.com). The storefront URL is fixed. Valid empty result pages return `200` with an empty collections array.
- **Params:** `limit` (integer, optional) — Maximum collections, defaults to 50 and supports up to 250; `page` (integer, optional) — 1-based page, defaults to 1

### `stevemadden_page`

- **HTTP:** `GET /stevemadden/pages/{handle}`
- **What:** Get a Steve Madden static page. Returns one Steve Madden static page by its `handle`: id, title, URL, plain-text `content` and the created, published and updated timestamps. Page text is cleaned, not raw HTML. An unknown handle returns 404. When the reduced form is served, `transport_mode` is `ssr_embedded` and `id` is omitted.
- **Params:** `handle` (string, **required**) — Page handle

### `stevemadden_pages`

- **HTTP:** `GET /stevemadden/pages`
- **What:** List Steve Madden static pages. Lists Steve Madden static pages, 50 per request by default (`limit` up to 250), with `page` starting at 1. Each page has its handle, title, URL, plain-text content and timestamps. An empty result is a normal 200. When `transport_mode` is `ssr_embedded`, items carry only `handle`, `url` and `updated_at`.
- **Params:** `limit` (integer, optional) — Maximum static pages, defaults to 50 and supports up to 250; `page` (integer, optional) — 1-based page, defaults to 1

### `stevemadden_product`

- **HTTP:** `GET /stevemadden/products/{handle}`
- **What:** Get a Steve Madden product. Returns product detail for one Steve Madden (https://www.stevemadden.com) product handle. The storefront URL is fixed; `handle` is the product's URL slug.
- **Params:** `handle` (string, **required**) — Product handle

### `stevemadden_product_recommendations`

- **HTTP:** `GET /stevemadden/products/{handle}/recommendations`
- **What:** List Steve Madden product recommendations. Returns recommended products for one Steve Madden (https://www.stevemadden.com) product handle. The storefront URL is fixed.
- **Params:** `handle` (string, **required**) — Product handle; `intent` (string, optional) — Recommendation intent. Allowed values: related, complementary; `limit` (integer, optional) — Maximum products, defaults to 10 and supports up to 20

### `stevemadden_products`

- **HTTP:** `GET /stevemadden/products`
- **What:** List Steve Madden products. Returns products from Steve Madden's (https://www.stevemadden.com) public product catalog. The storefront URL is fixed. Valid empty result pages return `200` with an empty products array.
- **Params:** `limit` (integer, optional) — Maximum products, defaults to 50 and supports up to 250; `page` (integer, optional) — 1-based page, defaults to 1

### `stevemadden_search_suggest`

- **HTTP:** `GET /stevemadden/search/suggest`
- **What:** Get Steve Madden search suggestions. Returns products, collections, and query suggestions from Steve Madden's (https://www.stevemadden.com) predictive search. The storefront URL is fixed.
- **Params:** `limit` (integer, optional) — Maximum results per type, defaults to 10 and supports up to 20; `q` (string, **required**) — Search query; `types` (string, optional) — Comma-separated suggestion types. Allowed values: product, collection, query

### `stevemadden_sitemap_urls`

- **HTTP:** `GET /stevemadden/sitemap/urls`
- **What:** List Steve Madden sitemap URLs. Returns capped URL entries from Steve Madden's (https://www.stevemadden.com) child sitemaps matching the requested type. The storefront URL is fixed server-side.
- **Params:** `limit` (integer, optional) — Maximum URL entries, defaults to 50 and supports up to 250; `type` (string, optional) — Sitemap type. Allowed values: all, products, collections, pages, blogs, agentic_discovery, other

### `stevemadden_sitemaps`

- **HTTP:** `GET /stevemadden/sitemaps`
- **What:** List Steve Madden sitemaps. Returns child sitemap URLs from Steve Madden's (https://www.stevemadden.com) `/sitemap.xml` index with inferred sitemap types. The storefront URL is fixed server-side.
- **Params:** _none_

### `stevemadden_store`

- **HTTP:** `GET /stevemadden/store`
- **What:** Get Steve Madden store metadata. Returns storefront metadata for Steve Madden (https://www.stevemadden.com). The storefront URL is fixed, so no `url` parameter is accepted.
- **Params:** _none_

## The Body Shop (11)

### `thebodyshop_collection_products`

- **HTTP:** `GET /thebodyshop/collections/{handle}/products`
- **What:** List The Body Shop collection products. Returns products from one The Body Shop (https://www.thebodyshop.com) collection. The storefront URL is fixed; `handle` is the collection's URL slug.
- **Params:** `handle` (string, **required**) — Collection handle; `limit` (integer, optional) — Maximum products, defaults to 50 and supports up to 250; `page` (integer, optional) — 1-based page, defaults to 1

### `thebodyshop_collections`

- **HTTP:** `GET /thebodyshop/collections`
- **What:** List The Body Shop collections. Returns collections from The Body Shop (https://www.thebodyshop.com). The storefront URL is fixed. Valid empty result pages return `200` with an empty collections array.
- **Params:** `limit` (integer, optional) — Maximum collections, defaults to 50 and supports up to 250; `page` (integer, optional) — 1-based page, defaults to 1

### `thebodyshop_page`

- **HTTP:** `GET /thebodyshop/pages/{handle}`
- **What:** Get a The Body Shop static page. Returns one The Body Shop static page by its `handle`: id, title, URL, plain-text `content` and the created, published and updated timestamps. Page text is cleaned, not raw HTML. An unknown handle returns 404. When the reduced form is served, `transport_mode` is `ssr_embedded` and `id` is omitted.
- **Params:** `handle` (string, **required**) — Page handle

### `thebodyshop_pages`

- **HTTP:** `GET /thebodyshop/pages`
- **What:** List The Body Shop static pages. Lists The Body Shop static pages, 50 per request by default (`limit` up to 250), with `page` starting at 1. Each page has its handle, title, URL, plain-text content and timestamps. An empty result is a normal 200. When `transport_mode` is `ssr_embedded`, items carry only `handle`, `url` and `updated_at`.
- **Params:** `limit` (integer, optional) — Maximum static pages, defaults to 50 and supports up to 250; `page` (integer, optional) — 1-based page, defaults to 1

### `thebodyshop_product`

- **HTTP:** `GET /thebodyshop/products/{handle}`
- **What:** Get a The Body Shop product. Returns product detail for one The Body Shop (https://www.thebodyshop.com) product handle. The storefront URL is fixed server-side; `handle` is the product's URL slug.
- **Params:** `handle` (string, **required**) — Product handle

### `thebodyshop_product_recommendations`

- **HTTP:** `GET /thebodyshop/products/{handle}/recommendations`
- **What:** List The Body Shop product recommendations. Returns recommended products for one The Body Shop (https://www.thebodyshop.com) product handle. The storefront URL is fixed server-side.
- **Params:** `handle` (string, **required**) — Product handle; `intent` (string, optional) — Recommendation intent. Allowed values: related, complementary; `limit` (integer, optional) — Maximum products, defaults to 10 and supports up to 20

### `thebodyshop_products`

- **HTTP:** `GET /thebodyshop/products`
- **What:** List The Body Shop products. Returns products from The Body Shop's (https://www.thebodyshop.com) public product catalog. The storefront URL is fixed server-side. Valid empty result pages return `200` with an empty products array.
- **Params:** `limit` (integer, optional) — Maximum products, defaults to 50 and supports up to 250; `page` (integer, optional) — 1-based page, defaults to 1

### `thebodyshop_search_suggest`

- **HTTP:** `GET /thebodyshop/search/suggest`
- **What:** Get The Body Shop search suggestions. Returns products, collections, and query suggestions from The Body Shop's (https://www.thebodyshop.com) predictive search. The storefront URL is fixed server-side.
- **Params:** `limit` (integer, optional) — Maximum results per type, defaults to 10 and supports up to 20; `q` (string, **required**) — Search query; `types` (string, optional) — Comma-separated suggestion types. Allowed values: product, collection, query

### `thebodyshop_sitemap_urls`

- **HTTP:** `GET /thebodyshop/sitemap/urls`
- **What:** List The Body Shop sitemap URLs. Returns capped URL entries from The Body Shop's (https://www.thebodyshop.com) child sitemaps matching the requested type. The storefront URL is fixed server-side.
- **Params:** `limit` (integer, optional) — Maximum URL entries, defaults to 50 and supports up to 250; `type` (string, optional) — Sitemap type. Allowed values: all, products, collections, pages, blogs, agentic_discovery, other

### `thebodyshop_sitemaps`

- **HTTP:** `GET /thebodyshop/sitemaps`
- **What:** List The Body Shop sitemaps. Returns child sitemap URLs from The Body Shop's (https://www.thebodyshop.com) `/sitemap.xml` index with inferred sitemap types. The storefront URL is fixed server-side.
- **Params:** _none_

### `thebodyshop_store`

- **HTTP:** `GET /thebodyshop/store`
- **What:** Get The Body Shop store metadata. Returns storefront metadata for The Body Shop (https://www.thebodyshop.com). The storefront URL is fixed server-side, so no `url` parameter is accepted.
- **Params:** _none_
