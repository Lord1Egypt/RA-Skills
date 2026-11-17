---
name: wayfair-research
description: Browses Wayfair's category taxonomy and pulls category product grids and product detail (price, brand, stock status, rating, variants, images) using the Crawlora API, returning clean JSON. Use when the user asks to browse a Wayfair category, list products in a Wayfair department, or look up a specific Wayfair product by id — instead of scraping wayfair.com. This is a narrow skill — there is no full-text product search or reviews endpoint, only category browsing and product detail.
---

# Wayfair research

Browse Wayfair's category taxonomy, list a category's product grid, and pull
full product detail — all as normalized JSON from the Crawlora API, with no
HTML scraping. This is a narrow skill: discovery is category-based only —
there's no keyword search and no reviews endpoint.

## When to use this skill

- "List Wayfair's categories" / "find the category id for [department]."
- "Browse this Wayfair category" / "what's in Wayfair's [category]?"
- "What does [Wayfair product] cost / what's its rating?"
- "Pull pricing for every item in this Wayfair category page."
- "Look up this Wayfair product by its W-id."

## Setup (one-time)

- Get a free Crawlora API key (2,000 credits/mo, no card) at [https://crawlora.net](https://crawlora.net?utm_source=github&utm_medium=referral&utm_campaign=crawlora-skills).
- Set `CRAWLORA_API_KEY` in the environment before running the helper.
- The helper reads `CRAWLORA_API_KEY` from the environment and sends requests to `https://api.crawlora.net/api/v1`. Missing/invalid key → `401`.

## How it works

1. **Categories** — `/wayfair/categories` lists Wayfair categories
   discovered from Wayfair's own sitemap, paginated (`page`, `page_size`),
   optionally filtered with `q` (matches derived name or department). Names
   are derived from the category's URL slug, not an authoritative
   site-provided label.
2. **Browse a category** — `/wayfair/category` (`category`) returns that
   category's product grid, page-based (`page`). `category` accepts a bare
   id (`478390`), a `c`-prefixed id (`c478390`), a slug
   (`office-chairs-c478390`), or a full wayfair.com category URL — only the
   trailing id is used. Products come back with name, brand, pricing, and
   image.
3. **Detail** — `/wayfair/product/{id}` (id is the product's own
   `W`-prefixed id, e.g. `W100794312`, taken from a category result's
   `product_id` field) fetches full detail: name, brand, price, stock
   status, aggregate rating with a 1-5 star breakdown, images, every
   selectable variant option (color, finish, etc.), and site-selected
   feature highlights. An unrecognized id returns `404`.
4. **Compare** the JSON fields (price, rating, stock status) across items
   and answer.

Full endpoint list, methods, and params: [`reference/endpoints.md`](reference/endpoints.md).

## Calling the API

```sh
# Find a category id by name:
scripts/crawlora.sh /wayfair/categories q="office chairs" | jq '.'

# Browse a category's product grid:
scripts/crawlora.sh /wayfair/category category=office-chairs-c478390 page=1 | jq '.'

# Product detail (id is a path param):
scripts/crawlora.sh /wayfair/product/W100794312 | jq '.data'
```

Use `scripts/crawlora.sh` for all requests; it keeps the API key out of command-line arguments.


## Endpoint reference

See [`reference/endpoints.md`](reference/endpoints.md) for every Wayfair
endpoint this skill uses (method, path, params, description).

## Examples

- **Browse a furniture category:** `/wayfair/categories` with `q` to find
  the department's category id, then `/wayfair/category` paginated with
  `page` to list the products in it.
- **Price sweep of a category page:** `/wayfair/category` for a given
  `category`, then `/wayfair/product/{id}` for each returned `product_id`
  to pull price, stock status, and rating detail not present in the grid
  view.

## Notes & limits

- **Credits / pay-on-success:** billed only on `2xx`; free tier 2,000 credits/mo.
  Key at [https://crawlora.net](https://crawlora.net?utm_source=github&utm_medium=referral&utm_campaign=crawlora-skills).
- **Public data only** — public Wayfair category/product pages; respect Wayfair's terms.
- **Security:** key lives in `CRAWLORA_API_KEY` only — never hardcode, query-param, or commit it.
- **No full-text search and no reviews endpoint** — discovery is via the
  category taxonomy only (`/wayfair/categories` → `/wayfair/category`);
  there's no keyword `search` endpoint and product reviews aren't exposed,
  only the aggregate rating on `/wayfair/product/{id}`.
- Results are paginated — pass `page` (and `page_size` on `categories`) to walk listings.
- **Product identity is the `W`-prefixed id** (e.g. `W100794312`), not a
  SKU — take it from a category result's `product_id` field or a product
  page's URL.
- Category names on `/wayfair/categories` are derived from the URL slug
  (title-cased), not an authoritative site label — treat them as
  best-effort, not exact.
