---
name: zara-research
description: Researches Zara's catalog — category taxonomy, category listings, product detail, keyword search, search suggestions, and nearby physical stores — using the Crawlora API, returning clean JSON. Use when the user asks to find a product on Zara, browse a Zara category, search Zara's catalog by keyword, pull a Zara product's colors/sizes/images, or find a nearby Zara store — instead of scraping zara.com.
---

# Zara research

Browse Zara's category taxonomy, list or search products, and pull full
product detail (color variants, per-size stock, images) and nearby
physical stores — all as normalized JSON from the Crawlora API, with no
HTML scraping.

## When to use this skill

- "What does X cost on Zara?" or "find X on Zara."
- "Browse Zara's {section} category" / "what's in Zara's WOMAN/MAN/KID line?"
- "Search Zara for {keyword}."
- "Pull the colors/sizes/images for this Zara product."
- "Find the nearest Zara store to {location}."

## Setup (one-time)

- Get a free Crawlora API key (2,000 credits/mo, no card) at [https://crawlora.net](https://crawlora.net?utm_source=github&utm_medium=referral&utm_campaign=crawlora-skills).
- Set `CRAWLORA_API_KEY` in the environment before running the helper.
- The helper reads `CRAWLORA_API_KEY` from the environment and sends requests to `https://api.crawlora.net/api/v1`. Missing/invalid key → `401`.

## How it works

1. **Browse categories** — `/zara/categories` returns Zara's full US
   storefront category/subcategory tree (WOMAN, MAN, KID, etc). Each
   entry's `id` is the `categoryId` to pass to category-products.
2. **List or search** — `/zara/category/{categoryId}/products` returns a
   category's complete product listing in one call (Zara doesn't paginate
   this endpoint), or `/zara/search` (`query`, `section`) runs a keyword
   search with real offset-based pagination. Both return normalized
   products with pricing, images, and availability, one entry per
   purchasable color variant rather than one per color-grouped product.
   Use `/zara/suggest` (`query`) for typeahead search-term ideas before
   committing to a keyword.
3. **Detail** — `/zara/product/{productId}` (numeric id, taken from a
   search/category result's `url` field, the digits after `-p`) fetches
   every purchasable color variant with its real marketing description,
   per-size stock, and full image gallery — richer than the listing/search
   summaries.
4. **Stores** — `/zara/stores` finds nearby physical Zara stores by
   `lat`/`lng` (both required — no free-text zip/city search), with
   optional `radius`, `pickup_only`, and `donation_only` filters.

Full endpoint list, methods, and params: [`reference/endpoints.md`](reference/endpoints.md).

## Calling the API

```sh
# List categories to find a categoryId:
scripts/crawlora.sh /zara/categories | jq '.'

# Browse a category's full listing (no pagination):
scripts/crawlora.sh /zara/category/2417941/products | jq '.'

# Keyword search within a section, paginated:
scripts/crawlora.sh /zara/search query="linen shirt" section="MAN" limit=24 offset=0 | jq '.'

# Product detail (colors, sizes, images):
scripts/crawlora.sh /zara/product/12345678 | jq '.data'
```

Use `scripts/crawlora.sh` for all requests; it keeps the API key out of command-line arguments.


## Endpoint reference

See [`reference/endpoints.md`](reference/endpoints.md) for every Zara
endpoint this skill uses (method, path, params, description).

## Examples

- **Category browse with pricing:** `/zara/categories` to find a section's
  `categoryId`, then `/zara/category/{categoryId}/products` for the full
  listing — no paging needed, the response is already complete.
- **Search and compare:** `/zara/suggest` to refine a keyword, then
  `/zara/search` (paginated via `limit`/`offset`) for candidates, then
  `/zara/product/{productId}` on the top picks to compare colors, per-size
  stock, and images before recommending one.
- **Local store check:** `/zara/stores` with `lat`/`lng` (and optionally
  `radius`, `pickup_only`, `donation_only`) to list nearby stores before
  telling a shopper where to try something on.

## Notes & limits

- **Credits / pay-on-success:** billed only on `2xx`; free tier 2,000 credits/mo.
  Key at [https://crawlora.net](https://crawlora.net?utm_source=github&utm_medium=referral&utm_campaign=crawlora-skills).
- **Public data only** — public Zara product/category/store pages; respect Zara's terms.
- **Security:** key lives in `CRAWLORA_API_KEY` only — never hardcode, query-param, or commit it.
- **No reviews or Q&A endpoint** — this build only covers categories,
  listings, product detail, search, suggest, and stores.
- **Category listings aren't paginated** — `/zara/category/{categoryId}/products`
  always returns the category's complete listing in one call; only
  `/zara/search` has real pagination (`limit`/`offset`, zero-based offset,
  defaults `limit=24`, `offset=0`).
- **Search is best-effort, not exact-match** — for an obscure or nonsense
  `query`, Zara's own search falls back to a broader recommended set
  instead of an empty result, and there's no field to distinguish that
  fallback from a true keyword match. An offset past the last result
  returns a normal empty page with `is_last_page: true`, not an error.
- **One entry per color variant, not per product** — both
  `/zara/category/{categoryId}/products` and `/zara/search` list each
  purchasable color as its own entry; `/zara/product/{productId}` groups
  all of a product's colors together.
- **Product identity comes from the result URL** — `productId` for
  `/zara/product/{productId}` is the numeric id in a search/category
  result's `url` field (the digits after `-p`), not a SKU; an unrecognized
  id returns `404`.
- **Stores requires coordinates** — `/zara/stores` needs `lat` and `lng`
  directly; there's no zip/city text search. `radius` defaults to 30
  miles (1–500). A location with no stores in range returns a normal
  response with an empty `stores` array, not an error.
</content>
