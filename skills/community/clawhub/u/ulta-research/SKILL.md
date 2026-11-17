---
name: ulta-research
description: Researches Ulta Beauty's catalog — categories, products, shades, questions, reviews, and nearby stores — using the Crawlora API, returning clean JSON. Use when the user asks to find a beauty product on Ulta, browse an Ulta category, pull product Q&A/reviews before recommending an item, or find a nearby Ulta store — instead of scraping ulta.com.
---

# Ulta Beauty research

Browse and search Ulta Beauty's catalog and pull product detail, shade
variants, questions, reviews, and nearby store locations — all as
normalized JSON from the Crawlora API, with no HTML scraping.

## When to use this skill

- "Find [product] on Ulta" or "what does Ulta sell for [need]?"
- "Browse Ulta's [department] category" / "filter by [brand/benefit]."
- "What do customers ask and say about this Ulta product before I
  recommend it?" (Q&A + reviews)
- "Find shade/sku options for this Ulta product."
- "Is there an Ulta store near [zip/city]?"

## Setup (one-time)

- Get a free Crawlora API key (2,000 credits/mo, no card) at [https://crawlora.net](https://crawlora.net?utm_source=github&utm_medium=referral&utm_campaign=crawlora-skills).
- Set `CRAWLORA_API_KEY` in the environment before running the helper.
- The helper reads `CRAWLORA_API_KEY` from the environment and sends requests to `https://api.crawlora.net/api/v1`. Missing/invalid key → `401`.

## How it works

1. **Discover categories** — `/ulta/categories` lists the storefront
   navigation (department, group, and a `category` value ready to pass to
   `/ulta/category`).
2. **Browse or search** — `/ulta/category` (`category`) paginates a
   category's product grid and returns guided-navigation `filter` facet
   codes to narrow it; `/ulta/search` (`query`) does keyword search
   instead. `/ulta/suggest` (`query`) returns typeahead suggestions plus
   each suggestion's top product matches, useful for finding query ideas
   or a featured best match for a partial term.
3. **Detail** — `/ulta/product/{productId}` fetches full product detail:
   name, brand, description, pricing, rating, and every purchasable
   color/shade variant; pass `sku` to pin a specific shade.
4. **Q&A and reviews** — `/ulta/product/questions` and
   `/ulta/product/reviews` (both keyed by `product_id`) pull paginated
   customer questions/answers and written reviews plus the rating summary.
5. **Nearby stores** — `/ulta/stores` resolves a `search` string (zip,
   city, address) or explicit `lat`/`lng` to nearby physical Ulta
   locations, with hours, services, and phone.

Full endpoint list, methods, and params: [`reference/endpoints.md`](reference/endpoints.md).

## Calling the API

```sh
# Search Ulta by keyword:
scripts/crawlora.sh /ulta/search query="vitamin c serum" | jq '.'

# Browse a category, filtered:
scripts/crawlora.sh /ulta/category category="shop/skin-care/serums" filter="BENEFIT--BRIGHTENING" | jq '.'

# Product detail (path param) for a specific shade:
scripts/crawlora.sh /ulta/product/pimprod2020260 sku=2540468 | jq '.data'

# Nearby stores:
scripts/crawlora.sh /ulta/stores search="60614" | jq '.'
```

Use `scripts/crawlora.sh` for all requests; it keeps the API key out of command-line arguments.


## Endpoint reference

See [`reference/endpoints.md`](reference/endpoints.md) for every Ulta
Beauty endpoint this skill uses (method, path, params, description).

## Examples

- **Filtered category browse:** `/ulta/categories` to find a
  department's `category` value, then `/ulta/category` paginated with
  `filter` set to a facet code from that category's own response, to
  narrow by benefit/brand.
- **Product due diligence:** `/ulta/product/{productId}` for
  price/rating/shades, then `/ulta/product/questions` and
  `/ulta/product/reviews` (both by `product_id`) to summarize what
  shoppers ask and say before recommending it.
- **Find a store:** `/ulta/stores` with `search` set to a zip code or
  city, then check `hours`/`services` on the closest result.

## Notes & limits

- **Credits / pay-on-success:** billed only on `2xx`; free tier 2,000 credits/mo.
  Key at [https://crawlora.net](https://crawlora.net?utm_source=github&utm_medium=referral&utm_campaign=crawlora-skills).
- **Public data only** — public Ulta Beauty product/category/store pages; respect Ulta's terms.
- **Security:** key lives in `CRAWLORA_API_KEY` only — never hardcode, query-param, or commit it.
- Results are paginated — pass `page` (1-based) to walk `category`, `search`,
  `questions`, and `reviews` listings.
- **Product identity is `product_id`** (aka `productId`, from a search
  result's `product_id` field or the product URL) — `/ulta/product/{productId}`,
  `/ulta/product/questions`, and `/ulta/product/reviews` all key off it;
  `sku` is optional and only narrows `/ulta/product/{productId}` to one
  shade/color variant.
- `/ulta/stores` needs either `search` or both `lat` and `lng`; an
  unresolved `search` or an empty radius returns a well-formed empty
  result, not an error — same for a nonsense `search`/`query` on
  `/ulta/search` and `/ulta/suggest`.
- An unrecognized `category` on `/ulta/category` returns `404`, but an
  unrecognized `product_id` on `/ulta/product/questions` or
  `/ulta/product/reviews` returns a normal empty result instead.
