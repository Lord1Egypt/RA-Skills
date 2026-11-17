---
name: wish-research
description: Researches Wish's marketplace — categories, product search, product detail, related items, and reviews — using the Crawlora API, returning clean JSON. Use when the user asks to find a product on Wish, browse Wish categories, compare Wish product prices/ratings, or pull a Wish product's related items and reviews — instead of scraping wish.com.
---

# Wish research

Browse Wish's category tree, search its product catalog, and pull product
detail, related items, and customer reviews — all as normalized JSON from
the Crawlora API, with no HTML scraping.

## When to use this skill

- "What does X cost on Wish?" or "find X on Wish."
- "Browse Wish's categories" / "what's under [department] on Wish?"
- "Pull the detail/price/rating for this Wish product."
- "What are the reviews like for this Wish product?"
- "Find similar or related items to this Wish product."

## Setup (one-time)

- Get a free Crawlora API key (2,000 credits/mo, no card) at [https://crawlora.net](https://crawlora.net?utm_source=github&utm_medium=referral&utm_campaign=crawlora-skills).
- Set `CRAWLORA_API_KEY` in the environment before running the helper.
- The helper reads `CRAWLORA_API_KEY` from the environment and sends requests to `https://api.crawlora.net/api/v1`. Missing/invalid key → `401`.

## How it works

1. **Browse** — `/wish/categories` returns Wish's own top navigation/category
   tree plus each category's nested filter groups where present. It's a
   static, site-wide taxonomy — no input, doesn't vary by search term.
2. **Search** — `/wish/search` (`query`) searches the product catalog by
   keyword, offset-paginated, returning price, currency, rating, review
   count, and merchant id per product. Use `/wish/suggest` (`query`) first
   for typeahead search-term ideas if the user's query is vague.
3. **Detail** — `/wish/product/{id}` (`id` is the 24-character hex
   `product_id` from a search result or product URL) fetches full product
   detail: name, description, sold-out state, aggregate rating, images, and
   every purchasable variation with its own price, currency, inventory, and
   merchant.
4. **Related items** — `/wish/product/{id}/related` returns similar-item
   rails for that product (a general-similarity rail and a faster-shipping
   subset where eligible).
5. **Reviews** — `/wish/product/{id}/reviews` returns the product's
   normalized customer reviews.
6. **Compare** the JSON fields (price, rating, review count, merchant)
   across products or reviews and answer.

Full endpoint list, methods, and params: [`reference/endpoints.md`](reference/endpoints.md).

## Calling the API

```sh
# Search Wish (GET, key=value params):
scripts/crawlora.sh /wish/search query="wireless earbuds" count=30 | jq '.'

# Search-term suggestions:
scripts/crawlora.sh /wish/suggest query="wireless ear" | jq '.'

# Product detail:
scripts/crawlora.sh /wish/product/5f8a1c2e9b3d4a001f7e6c21 | jq '.data'

# Reviews:
scripts/crawlora.sh /wish/product/5f8a1c2e9b3d4a001f7e6c21/reviews count=50 | jq '.'
```

Use `scripts/crawlora.sh` for all requests; it keeps the API key out of command-line arguments.


## Endpoint reference

See [`reference/endpoints.md`](reference/endpoints.md) for every Wish
endpoint this skill uses (method, path, params, description).

## Examples

- **Search and compare:** `/wish/search` for a keyword, compare price,
  rating, and review count across results to shortlist candidates.
- **Product due diligence:** `/wish/product/{id}` for price/rating/variations,
  then `/wish/product/{id}/reviews` to summarize what buyers say before
  recommending it.
- **Find similar items:** `/wish/product/{id}/related` to pull a product's
  similar-item rails when the exact item is sold out or the user wants
  alternatives.

## Notes & limits

- **Credits / pay-on-success:** billed only on `2xx`; free tier 2,000 credits/mo.
  Key at [https://crawlora.net](https://crawlora.net?utm_source=github&utm_medium=referral&utm_campaign=crawlora-skills).
- **Public data only** — public Wish product/category pages; respect Wish's terms.
- **Security:** key lives in `CRAWLORA_API_KEY` only — never hardcode, query-param, or commit it.
- **Product identity is `id`** (a 24-character hex `product_id`), not a SKU
  or ASIN — take it from a search result's `product_id` field or a product
  page's URL; `/wish/product`, `/wish/product/related`, and
  `/wish/product/reviews` all key off it. An unrecognized `id` returns `404`
  on `/wish/product` but a normal empty result on `related`/`reviews`.
- **`/wish/search` pagination is offset-based, not page-based:** `offset`
  must be an exact multiple of `count`, up to `3 * count` (so at most 4
  pages reachable per query) — pass a larger `count` (max 70) rather than
  paging deep.
- **`/wish/product/{id}/reviews` has no offset/cursor** — the upstream
  source doesn't support one, so re-request with a larger `count` (max 200)
  to get more reviews, not a page/offset param.
- A query with no matches, or a product with zero reviews, returns a normal
  empty result rather than an error.
