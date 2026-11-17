# zappos-research — endpoint reference

> Generated from `scripts/tools.json` by `scripts/generate.mjs` — do not edit by hand.

Endpoints this skill uses, grouped by platform. Call them via `scripts/crawlora.sh` (see SKILL.md).

All paths are relative to the API base `https://api.crawlora.net/api/v1` and require the header `x-api-key: $CRAWLORA_API_KEY`. Path params like `{id}` are substituted into the URL; `GET` params go in the query string; `POST` params go in a JSON body.

**5 endpoints across 1 platform group(s).**

## Zappos (5)

### `zappos_brand`

- **HTTP:** `GET /zappos/brand`
- **What:** Browse a Zappos brand. Returns a Zappos brand page's product grid, with real page-based pagination and per-field filter facets. brand accepts a full brand URL copied from zappos.com, the "slug/id.zso" path from that URL, or just the opaque id from a GET /zappos/brands result's own id field. An unrecognized brand returns 404.
- **Params:** `brand` (string, **required**) — Zappos brand URL, slug/id.zso path, or opaque id; `page` (integer, optional) — Result page, 1-based, defaults to 1

### `zappos_brands`

- **HTTP:** `GET /zappos/brands`
- **What:** List Zappos brands. Returns a page of Zappos brands discovered from Zappos's own published sitemap, closing the discovery gap where a brand id otherwise has to be found elsewhere. Pair a returned id or url with GET /zappos/brand to browse that brand's product grid. name is derived from the brand's own URL slug (title-cased), not an authoritative site-provided label. q, if set, case-insensitively filters to brands whose derived name or slug contains it.
- **Params:** `page` (integer, optional) — Result page, 1-based, defaults to 1; `page_size` (integer, optional) — Results per page, defaults to 100, max 1000; `q` (string, optional) — Case-insensitive substring filter on name or slug

### `zappos_product`

- **HTTP:** `GET /zappos/product/{productId}`
- **What:** Get a Zappos product's full detail. Returns one Zappos product's full detail: name, brand, description, category, breadcrumbs, pricing, images, aggregate rating with a 1-5 star breakdown, up to two featured customer reviews with real author/date/body/rating, reviewer-submitted fit feedback for size/width/arch (each response option's own share of respondents plus the most common answer), and every sibling color variant with its own price. productId is taken from a search result's product_id field or a product page's URL. colorId is optional and selects a specific color variant; an omitted or invalid colorId still resolves the base product using a real color variant rather than failing. An unrecognized productId returns 404.
- **Params:** `colorId` (string, optional) — Zappos color id selecting a specific color variant; `productId` (string, **required**) — Zappos product id, from a search result's product_id field

### `zappos_search`

- **HTTP:** `GET /zappos/search`
- **What:** Search Zappos products. Searches Zappos's product catalog by keyword, with real page-based pagination. Returns products with brand, pricing, sale status, rating, and review count, plus filterable facets (gender, department, shoe size, and more) each with a live result count and its own drill-down URL. Requesting a page beyond the available results returns a normal, empty result rather than an error.
- **Params:** `page` (integer, optional) — Result page, 1-based, defaults to 1; `term` (string, **required**) — Search keyword

### `zappos_suggest`

- **HTTP:** `GET /zappos/suggest`
- **What:** Get Zappos search-box suggestions. Returns Zappos's own search-box suggestions (typeahead) for a partial query: a flat list of suggested search phrases, no product data. A partial query with no real matches returns a normal, empty result rather than an error.
- **Params:** `query` (string, **required**) — Partial search query
