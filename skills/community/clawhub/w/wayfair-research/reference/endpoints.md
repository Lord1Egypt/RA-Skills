# wayfair-research — endpoint reference

> Generated from `scripts/tools.json` by `scripts/generate.mjs` — do not edit by hand.

Endpoints this skill uses, grouped by platform. Call them via `scripts/crawlora.sh` (see SKILL.md).

All paths are relative to the API base `https://api.crawlora.net/api/v1` and require the header `x-api-key: $CRAWLORA_API_KEY`. Path params like `{id}` are substituted into the URL; `GET` params go in the query string; `POST` params go in a JSON body.

**3 endpoints across 1 platform group(s).**

## Wayfair (3)

### `wayfair_categories`

- **HTTP:** `GET /wayfair/categories`
- **What:** List Wayfair categories. Returns a page of Wayfair categories discovered from Wayfair's own published sitemap, closing the discovery gap where a category id otherwise has to be found elsewhere. Pair a returned id with GET /wayfair/category to browse that category's product grid. name is derived from the category's own URL slug (title-cased), not an authoritative site-provided label. q, if set, case-insensitively filters to categories whose derived name or department contains it.
- **Params:** `page` (integer, optional) — Result page, 1-based, defaults to 1; `page_size` (integer, optional) — Results per page, defaults to 100, max 1000; `q` (string, optional) — Case-insensitive substring filter on name or department

### `wayfair_category`

- **HTTP:** `GET /wayfair/category`
- **What:** Browse a Wayfair category. Returns a Wayfair category page's product grid, with real page-based pagination. category accepts a bare Wayfair category id ("478390"), a "c"-prefixed id ("c478390"), a category slug ("office-chairs-c478390"), or a full category URL copied from wayfair.com. Returns products with name, brand, pricing, and image.
- **Params:** `category` (string, **required**) — Wayfair category id, slug, or URL; `page` (integer, optional) — Result page, 1-based, defaults to 1

### `wayfair_product`

- **HTTP:** `GET /wayfair/product/{id}`
- **What:** Get a Wayfair product's full detail. Returns one Wayfair product's full detail: name, brand, price, stock status, aggregate rating with a 1-5 star breakdown, images, every selectable variant option (e.g. color, finish), and site-selected feature highlights. id is the product's own "W"-prefixed id (e.g. W100794312), taken from a category result's product_id field or a product page's URL. An unrecognized id returns 404.
- **Params:** `id` (string, **required**) — Wayfair product id, starting with W
