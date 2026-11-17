# samsclub-research — endpoint reference

> Generated from `scripts/tools.json` by `scripts/generate.mjs` — do not edit by hand.

Endpoints this skill uses, grouped by platform. Call them via `scripts/crawlora.sh` (see SKILL.md).

All paths are relative to the API base `https://api.crawlora.net/api/v1` and require the header `x-api-key: $CRAWLORA_API_KEY`. Path params like `{id}` are substituted into the URL; `GET` params go in the query string; `POST` params go in a JSON body.

**5 endpoints across 1 platform group(s).**

## Sam's Club (5)

### `samsclub_category`

- **HTTP:** `GET /samsclub/category`
- **What:** Browse a Sam's Club category or collection. Returns a Sam's Club category or collection page's product grid, with real page-based pagination. id accepts a bare numeric category id (from a nav link's /browse/{id} URL) or a full /browse/{slug}/{id} URL copied from samsclub.com -- only the trailing id is used. Returns products with name, brand, pricing, availability, rating, and image. An id samsclub.com does not recognize returns a genuine zero-result response rather than an error.
- **Params:** `id` (string, **required**) — Sam's Club category id, or a /browse/{slug}/{id} URL; `page` (integer, optional) — Result page, 1-based, defaults to 1

### `samsclub_content`

- **HTTP:** `GET /samsclub/content/{id}`
- **What:** Get a Sam's Club curated content or landing page. Returns one Sam's Club curated content/landing page (e.g. a seasonal savings hub or a "New Arrivals" page) -- distinct data from GET /samsclub/category's flat, paginated product grid. id accepts a bare numeric content page id (from a nav link's /cp/{id} URL) or a full /cp/{slug}/{id} URL copied from samsclub.com -- only the trailing id is used. Returns a title, breadcrumb, named curated product shelves, and a category-navigation tile grid. There is no pagination -- a content page's shelves are a fixed, hand-curated set. An id samsclub.com does not recognize returns a 404, unlike GET /samsclub/category's zero-result response for the same situation.
- **Params:** `id` (string, **required**) — Numeric Sam's Club content page id, from a /cp/{slug}/{id} URL

### `samsclub_departments`

- **HTTP:** `GET /samsclub/departments`
- **What:** List Sam's Club departments and categories. Returns Sam's Club's full department/category taxonomy, as shown on its own "All Departments" page: every top-level department with its own subcategory list. Each link's type is "browse" (pairs directly with GET /samsclub/category), "cp" (a content/landing page that does not reliably carry a product grid), or empty (an unrecognized link shape).
- **Params:** _none_

### `samsclub_product`

- **HTTP:** `GET /samsclub/product/{id}`
- **What:** Get a Sam's Club product's full detail. Returns one Sam's Club product's full detail: name, brand, description, category breadcrumb, pricing, availability, images, aggregate rating and review count, and the club's own item number. id is the numeric product id from a Sam's Club product page's /ip/ URL.
- **Params:** `id` (string, **required**) — Numeric Sam's Club product id, from a product page's /ip/{slug}/{id} URL

### `samsclub_product_related`

- **HTTP:** `GET /samsclub/product/{id}/related`
- **What:** Get a Sam's Club product's related items. Returns the related-item carousels shown on a Sam's Club product page, each a named shelf (e.g. "Members also considered", "Items you may like") of products with pricing, rating, and image. id is the numeric product id from a Sam's Club product page's /ip/ URL. An unrecognized id is not distinguished from a known one -- it still returns generic fallback shelves rather than an error.
- **Params:** `id` (string, **required**) — Numeric Sam's Club product id, from a product page's /ip/{slug}/{id} URL
