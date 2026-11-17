---
name: samsclub-research
description: Researches Sam's Club's catalog — department/category navigation, category product grids, product detail with pricing/availability/ratings, related-item shelves, and curated content pages — using the Crawlora API, returning clean JSON. Use when the user asks to browse Sam's Club departments, list a Sam's Club category's products, look up a Sam's Club product's price/rating, or find items related to a Sam's Club product — instead of scraping samsclub.com.
---

# Sam's Club research

Browse Sam's Club's department taxonomy and category product grids, pull
full product detail (price, availability, rating, item number),
related-item shelves, and curated content/landing pages — all as
normalized JSON from the Crawlora API, with no HTML scraping.

## When to use this skill

- "What departments/categories does Sam's Club have?" / "browse this
  Sam's Club category."
- "What does this Sam's Club product cost, and is it in stock?"
- "What's related to / bought with this Sam's Club product?"
- "What's on Sam's Club's [seasonal savings / New Arrivals] page?"

## Setup (one-time)

- Get a free Crawlora API key (2,000 credits/mo, no card) at [https://crawlora.net](https://crawlora.net?utm_source=github&utm_medium=referral&utm_campaign=crawlora-skills).
- Set `CRAWLORA_API_KEY` in the environment before running the helper.
- The helper reads `CRAWLORA_API_KEY` from the environment and sends requests to `https://api.crawlora.net/api/v1`. Missing/invalid key → `401`.

## How it works

1. **Browse the taxonomy** — `/samsclub/departments` returns every
   top-level department with its subcategory links; each link's `type` is
   `"browse"` (feeds `/samsclub/category`) or `"cp"` (feeds
   `/samsclub/content`).
2. **List a category** — `/samsclub/category` (`id` — a bare category id
   or a full `/browse/{slug}/{id}` URL, paginated with `page`) returns the
   category's product grid: name, brand, pricing, availability, rating,
   image.
3. **Detail** — `/samsclub/product/{id}` (`id` — the numeric product id
   from a product page's `/ip/` URL) fetches full product detail: name,
   brand, description, breadcrumb, pricing, availability, images,
   aggregate rating/review count, and the club's own item number.
4. **Related items** — `/samsclub/product/{id}/related` returns the same
   product's related-item carousels ("Members also considered", "Items
   you may like") as normalized products.
5. **Curated content** — `/samsclub/content/{id}` (`id` — the numeric
   content page id from a `/cp/{slug}/{id}` URL) returns one curated
   landing/hub page: title, breadcrumb, named product shelves, and a
   category-navigation tile grid.

Full endpoint list, methods, and params: [`reference/endpoints.md`](reference/endpoints.md).

## Calling the API

```sh
# Full department/category taxonomy:
scripts/crawlora.sh /samsclub/departments | jq '.'

# List a category's products (id from a /browse/{slug}/{id} link or nav result):
scripts/crawlora.sh /samsclub/category id=980029 page=1 | jq '.'

# Product detail (id is a path param, from a /ip/{slug}/{id} URL):
scripts/crawlora.sh /samsclub/product/prod20355602 | jq '.data'

# Related items for the same product:
scripts/crawlora.sh /samsclub/product/prod20355602/related | jq '.'
```

Use `scripts/crawlora.sh` for all requests; it keeps the API key out of command-line arguments.


## Endpoint reference

See [`reference/endpoints.md`](reference/endpoints.md) for every Sam's
Club endpoint this skill uses (method, path, params, description).

## Examples

- **Department-to-category sweep:** `/samsclub/departments` to find a
  department's `"browse"` link and its category id, then
  `/samsclub/category` paginated with `page` to list products with
  pricing and availability.
- **Product due diligence:** `/samsclub/product/{id}` for price, rating,
  and availability, then `/samsclub/product/{id}/related` to see what
  Sam's Club surfaces alongside it before recommending or comparing.
- **Seasonal hub check:** `/samsclub/departments` to find a `"cp"` link,
  then `/samsclub/content/{id}` to pull that curated page's shelves and
  navigation tiles (e.g. a savings event or "New Arrivals" hub).

## Notes & limits

- **Credits / pay-on-success:** billed only on `2xx`; free tier 2,000 credits/mo.
  Key at [https://crawlora.net](https://crawlora.net?utm_source=github&utm_medium=referral&utm_campaign=crawlora-skills).
- **Public data only** — public samsclub.com pages; respect Sam's Club's terms.
- **Security:** key lives in `CRAWLORA_API_KEY` only — never hardcode, query-param, or commit it.
- **No free-text search endpoint** — discovery is department/category-based
  only: `/samsclub/departments` → `/samsclub/category`, not a keyword search.
- `id` is a **query** param on `/samsclub/category` (accepts a bare numeric
  id or a full `/browse/{slug}/{id}` URL — only the trailing id is used) but
  a **path** param on `/samsclub/product/{id}`,
  `/samsclub/product/{id}/related`, and `/samsclub/content/{id}`.
- **Unknown-id behavior differs by endpoint:** an unrecognized
  `/samsclub/category` id returns a genuine zero-result page (not an
  error); an unrecognized `/samsclub/content/{id}` id returns `404`; an
  unrecognized `/samsclub/product/{id}/related` id still returns generic
  fallback shelves rather than an error.
- `/samsclub/content/{id}` has no pagination — a content page's shelves
  are a fixed, hand-curated set.
