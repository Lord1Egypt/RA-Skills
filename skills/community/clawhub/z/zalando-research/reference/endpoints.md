# zalando-research — endpoint reference

> Generated from `scripts/tools.json` by `scripts/generate.mjs` — do not edit by hand.

Endpoints this skill uses, grouped by platform. Call them via `scripts/crawlora.sh` (see SKILL.md).

All paths are relative to the API base `https://api.crawlora.net/api/v1` and require the header `x-api-key: $CRAWLORA_API_KEY`. Path params like `{id}` are substituted into the URL; `GET` params go in the query string; `POST` params go in a JSON body.

**6 endpoints across 1 platform group(s).**

## Zalando (6)

### `zalando_categories`

- **HTTP:** `GET /zalando/categories`
- **What:** List a Zalando market's top-level category navigation. Returns a Zalando country storefront's live top-level category navigation, department by department. This is the discovery source for zalando-category's category parameter — category slugs are market-specific (each storefront uses its own local-language slug), so there is no fixed value space to hardcode; this endpoint returns the live values instead. market is required (there is no default storefront) and accepts 25 country storefronts — see zalando-markets for the full current list with domains. department optionally restricts the response to one of women, men, or kids; omitting it returns all three. Scope note: only the top-level nav tabs (e.g. Clothing, Shoes, Sports) are returned, not each tab's own hover-revealed mega-menu of sub-categories.
- **Params:** `department` (string, optional) — Restrict to one Zalando shopping department. Omit to return all three.; `market` (string, **required**) — Zalando country storefront

### `zalando_category`

- **HTTP:** `GET /zalando/category`
- **What:** Browse a Zalando category or brand. Browses a Zalando category or brand listing by URL slug (e.g. shoes, womens-dresses, on-running) and returns the same result cards as zalando-search, plus the category's upstream total_count. Category slugs are market-specific (each storefront uses its own local-language slug, e.g. "shoes" on de/gb, "chaussures" on fr, "scarpe" on it) — use zalando-categories to discover a market's live top-level slugs, or take one from a product's url field. market is required (there is no default storefront) and accepts 25 country storefronts — see zalando-markets for the full current list with domains.
- **Params:** `category` (string, **required**) — Zalando category or brand URL slug, in the target market's own language; `market` (string, **required**) — Zalando country storefront

### `zalando_markets`

- **HTTP:** `GET /zalando/markets`
- **What:** List supported Zalando country storefronts. Returns the Zalando country storefronts currently supported by the required market parameter on zalando-search, zalando-category, and zalando-product, with each market's domain. Static metadata.
- **Params:** _none_

### `zalando_product`

- **HTTP:** `GET /zalando/product`
- **What:** Get a Zalando product. Returns product details for one Zalando product, including brand, description, images, and per-size price/availability/GTIN. Pass the sku returned by zalando-search or zalando-category; market is required and must match the storefront the sku was found in (there is no default, and a sku is generally only listed for sale on the market(s) that carry it) — see zalando-markets for the full reference list.
- **Params:** `market` (string, **required**) — Zalando country storefront the sku was found in; `sku` (string, **required**) — Zalando product SKU (article number) from zalando-search or zalando-category

### `zalando_search`

- **HTTP:** `GET /zalando/search`
- **What:** Search Zalando products. Searches a Zalando country storefront by keyword and returns result cards with price, brand, and image. Returns the first page of results plus the upstream total_count; deeper pagination is not yet supported. market is required (there is no default storefront) and accepts 25 country storefronts — see zalando-markets for the full current list with domains.
- **Params:** `market` (string, **required**) — Zalando country storefront; `q` (string, **required**) — Product search keyword

### `zalando_suggest`

- **HTTP:** `GET /zalando/suggest`
- **What:** Autocomplete a Zalando search query. Returns Zalando's own search-box query completions for a partial keyword, e.g. "running sho" -> "running shoes", "running shoes nike". market is required (there is no default storefront) and accepts 25 country storefronts — see zalando-markets for the full current list with domains.
- **Params:** `market` (string, **required**) — Zalando country storefront; `q` (string, **required**) — Partial search text to complete
