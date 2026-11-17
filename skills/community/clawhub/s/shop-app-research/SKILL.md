---
name: shop-app-research
description: Researches products, variants, shops, and reviews on Shop.app — Shopify's own cross-store shopping/discovery app, distinct from individual Shopify storefronts — using the Crawlora API, returning clean JSON. Use when the user asks to find a product across Shop.app merchants, compare shop offerings, pull Shop.app reviews, or browse a Shop.app merchant's catalog/collections — instead of scraping Shop.app pages.
---

# Shop.app research

Search, browse, and analyze products, variants, shops, and reviews on
Shop.app — Shopify's cross-store shopping/discovery app (not to be confused
with an individual Shopify storefront) — all as normalized JSON from the
Crawlora API, with no HTML scraping.

## When to use this skill

- "Find X on Shop.app" / "search Shop.app for running shoes."
- "What's the price range / how many shops sell X on Shop.app?"
- "Look up this Shop.app shop" / "list a merchant's Shop.app catalog or collections."
- "Pull reviews for this Shop.app product or shop."
- "Get variants / options / availability for this Shop.app product."
- Cross-store discovery, market-snapshot, or merchant due-diligence research on Shop.app.

## Setup (one-time)

- Get a free Crawlora API key (2,000 credits/mo, no card) at [https://crawlora.net](https://crawlora.net?utm_source=github&utm_medium=referral&utm_campaign=crawlora-skills).
- Set `CRAWLORA_API_KEY` in the environment before running the helper.
- The helper reads `CRAWLORA_API_KEY` from the environment and sends requests to `https://api.crawlora.net/api/v1`. Missing/invalid key → `401`.

## How it works

1. **Search / discover** — `/shop-app/search` (`query`, plus `deep_search`,
   `in_stock`, `on_sale`, `limit` up to 50) to find candidate products by
   keyword. `/shop-app/suggestions` returns autocomplete query ideas, and
   `/shop-app/categories` lists public product categories to browse instead
   of searching.
2. **Market snapshot** — `/shop-app/analysis` runs the same search but
   returns an aggregated snapshot (price ranges, currencies, sale counts,
   discounts, top shops) instead of raw listings — use it for "what's the
   price range for X on Shop.app" without paginating results yourself.
3. **Product detail** — `/shop-app/products/{id}` for normalized product
   details (add `variant_id` to pin a specific variant).
4. **Variants** — `/shop-app/products/{id}/variant` for the exact variant
   matching `selected_options`, or `/shop-app/products/{id}/variants` for
   adjacent variants, to compare options and prices.
5. **Related products & reviews** — `/shop-app/products/{id}/related` and
   `/shop-app/products/{id}/reviews`.
6. **Resolve the shop** — `/shop-app/products/{id}/shop` finds the merchant
   behind a product; `/shop-app/shops/{handle}` fetches the merchant profile
   directly, and `/shop-app/shops/{handle}/locations` lists retail locations.
7. **Browse a shop's catalog** — `/shop-app/shops/{handle}/products`
   (sortable via `sort_by`) or `/shop-app/shops/{handle}/collections/{collection_id}/products`
   for one collection; `/shop-app/shops/{handle}/typeahead` searches inside a
   single shop; `/shop-app/shops/{handle}/reviews` pulls merchant reviews.

Full endpoint list, methods, and params: [`reference/endpoints.md`](reference/endpoints.md).

## Calling the API

```sh
# Search Shop.app (GET, key=value params):
scripts/crawlora.sh /shop-app/search query="running shoes" in_stock=true | jq '.'

# Product detail:
scripts/crawlora.sh /shop-app/products/12345 | jq '.data'

# Browse a shop's catalog, sorted low-to-high:
scripts/crawlora.sh /shop-app/shops/some-shop-handle/products sort_by=PRICE_LOW_TO_HIGH | jq '.'
```

Use `scripts/crawlora.sh` for all requests; it keeps the API key out of command-line arguments.


## Endpoint reference

See [`reference/endpoints.md`](reference/endpoints.md) for every Shop.app
endpoint this skill uses (method, path, params, description).

## Examples

- **Market snapshot before buying:** `/shop-app/analysis` with `query="wireless earbuds"`
  and `on_sale=true` to see the current price range, discounts, and top
  shops selling discounted units.
- **Merchant due-diligence:** `/shop-app/shops/{handle}` +
  `/shop-app/shops/{handle}/reviews` to summarize a Shop.app merchant's
  profile and recent reviews before recommending it.
- **Collection audit:** `/shop-app/shops/{handle}/products` (paginate via
  `limit`) or a specific `/shop-app/shops/{handle}/collections/{collection_id}/products`
  to list a merchant's catalog with prices and flag items above/below a
  threshold.

## Notes & limits

- **Credits / pay-on-success:** billed only on `2xx`; free tier 2,000 credits/mo.
  Key at [https://crawlora.net](https://crawlora.net?utm_source=github&utm_medium=referral&utm_campaign=crawlora-skills).
- **Public data only** — public Shop.app product/shop pages; respect Shop.app's terms.
- **Security:** key lives in `CRAWLORA_API_KEY` only — never hardcode, query-param, or commit it.
- Results are limited, not offset-paginated — `search`, `analysis`, `related`,
  `reviews`, `shop/collection products`, and `suggestions`/`typeahead` all cap
  out via `limit` (each endpoint has its own max, from 20 up to 100 for variants).
- **`selected_options` is a JSON object**, not flat key=value pairs — pass it
  as a JSON string (e.g. `selected_options='{"Color":"Black"}'`), or use
  repeated `option.Name=value` / `option[Name]=value` filters instead.
- `sort_by` on shop/collection product listings only accepts `MOST_SALES`,
  `PRICE_LOW_TO_HIGH`, `PRICE_HIGH_TO_LOW`, or `RELEVANCE`.
