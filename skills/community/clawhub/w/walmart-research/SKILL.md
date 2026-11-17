---
name: walmart-research
description: Researches Walmart products, prices, sellers, and reviews using the Crawlora API, returning clean JSON. Use when the user asks to find a product, compare prices, track listings, or pull reviews on Walmart — instead of scraping Walmart pages.
---

# Walmart research

Look up and compare Walmart products, prices, and reviews — all as
normalized JSON from the Crawlora API, with no HTML scraping.

## When to use this skill

- "What does X cost on Walmart?" or "compare prices for X on Walmart."
- "Find listings for X on Walmart" / "search Walmart for this product."
- "Pull reviews / ratings for this Walmart product."
- "Track this Walmart product's price / availability."
- Competitive pricing or catalog research on Walmart.

## Setup (one-time)

- Get a free Crawlora API key (2,000 credits/mo, no card) at [https://crawlora.net](https://crawlora.net?utm_source=github&utm_medium=referral&utm_campaign=crawlora-skills).
- Set `CRAWLORA_API_KEY` in the environment before running the helper.
- The helper reads `CRAWLORA_API_KEY` from the environment and sends requests to `https://api.crawlora.net/api/v1`. Missing/invalid key → `401`.

## How it works

1. **Search / discover** — `/walmart/search` (`q` required) to find
   candidate products by keyword.
2. **Detail** — fetch a specific product with `/walmart/product/{item_id}`
   (the numeric id from a Walmart `/ip/{id}` URL) for price, availability,
   brand, images, rating, seller, description, highlights, specifications,
   and variants.
3. **Reviews** — pull the on-page reviews snapshot with
   `/walmart/product/{item_id}/reviews`: average rating, total review count,
   per-star breakdown, recommended percentage, top positive/negative review,
   and a sample of recent reviews.

Full endpoint list, methods, and params: [`reference/endpoints.md`](reference/endpoints.md).

## Calling the API

```sh
# Search Walmart (GET, key=value params):
scripts/crawlora.sh /walmart/search q="standing desk" | jq '.'

# Product detail (item_id is a path segment, not a query param):
scripts/crawlora.sh /walmart/product/414781783 | jq '.data'

# Product reviews:
scripts/crawlora.sh /walmart/product/414781783/reviews | jq '.'
```

Use `scripts/crawlora.sh` for all requests; it keeps the API key out of command-line arguments.


## Endpoint reference

See [`reference/endpoints.md`](reference/endpoints.md) for every Walmart
endpoint this skill uses (method, path, params, description).

## Examples

- **Price check:** `/walmart/search` for a product name, grab the `item_id`
  of the best match, then `/walmart/product/{item_id}` for the current price
  and availability.
- **Review summary:** `/walmart/product/{item_id}/reviews` to summarize a
  product's average rating, rating breakdown, and top positive/negative
  reviews before recommending it.
- **Catalog sweep:** paginate `/walmart/search` with `page` across a set of
  queries to build a candidate list, then fetch `/walmart/product/{item_id}`
  for each to compare prices.

## Notes & limits

- **Credits / pay-on-success:** billed only on `2xx`; free tier 2,000 credits/mo.
  Key at [https://crawlora.net](https://crawlora.net?utm_source=github&utm_medium=referral&utm_campaign=crawlora-skills).
- **Public data only** — public Walmart product/search pages; respect Walmart's terms.
- **Security:** key lives in `CRAWLORA_API_KEY` only — never hardcode, query-param, or commit it.
- Search results are paginated — pass `page` to walk listings.
- **`item_id` is required for detail and reviews** — it's the numeric id in a
  Walmart `/ip/{id}` product URL, not the product slug.
- **Reviews are a single on-page snapshot, not a full paginated feed** — a
  product with no reviews returns zero counts and an empty reviews list.
