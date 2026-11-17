---
name: zalando-research
description: Researches products, prices, brands, and categories on Zalando (the European fashion marketplace) using the Crawlora API, returning clean JSON. Use when the user asks to find a product, browse a category or brand, autocomplete a search, or resolve a Zalando storefront market — instead of scraping Zalando pages.
---

# Zalando research

Look up and compare products, categories, and search results on Zalando —
all as normalized JSON from the Crawlora API, with no HTML scraping.

## When to use this skill

- "What does X cost on Zalando?" or "find X on Zalando in the German store."
- "Search Zalando for X" / "what's in the running-shoes category on Zalando?"
- "Look up this Zalando product by SKU."
- "Autocomplete this Zalando search query."
- "Which Zalando country storefronts are available?"
- Competitive pricing or catalog research scoped to Zalando.

## Setup (one-time)

- Get a free Crawlora API key (2,000 credits/mo, no card) at [https://crawlora.net](https://crawlora.net?utm_source=github&utm_medium=referral&utm_campaign=crawlora-skills).
- Set `CRAWLORA_API_KEY` in the environment before running the helper.
- The helper reads `CRAWLORA_API_KEY` from the environment and sends requests to `https://api.crawlora.net/api/v1`. Missing/invalid key → `401`.

## How it works

1. **Resolve the market** — every other Zalando endpoint **requires `market`**
   (a country storefront code like `de`, `fr`, `com`) with no default. If
   unsure which code to use, list them via `/zalando/markets`.
2. **Search** — `/zalando/search` (`q`+`market`) to find candidate products
   by keyword; returns normalized result cards with price, brand, and image
   plus `total_count`. Only the first page is available.
3. **Autocomplete** — `/zalando/suggest` (`q`+`market`) to complete a partial
   search term (e.g. "running sho" → "running shoes") before searching.
4. **Product detail** — `/zalando/product` (`sku`+`market`) to fetch brand,
   description, images, and per-size price/availability/GTIN for one product,
   using a `sku` from search or category results.
5. **Category browse** — `/zalando/category` (`category`+`market`) to browse
   a category or brand listing by market-specific URL slug, returning the
   same result cards as search plus `total_count`.

Full endpoint list, methods, and params: [`reference/endpoints.md`](reference/endpoints.md).

## Calling the API

```sh
# Resolve storefronts, then search a market (GET, key=value params):
scripts/crawlora.sh /zalando/markets | jq '.'
scripts/crawlora.sh /zalando/search q="running shoes" market=de | jq '.'

# Product detail (sku from a search/category result, same market):
scripts/crawlora.sh /zalando/product sku=AD116A0FL-Q11 market=de | jq '.data'

# Browse a category, and autocomplete a partial query:
scripts/crawlora.sh /zalando/category category=shoes market=de | jq '.'
scripts/crawlora.sh /zalando/suggest q="running sho" market=de | jq '.'
```

Use `scripts/crawlora.sh` for all requests; it keeps the API key out of command-line arguments.


## Endpoint reference

See [`reference/endpoints.md`](reference/endpoints.md) for every Zalando
endpoint this skill uses (method, path, params, description).

## Examples

- **Storefront-aware price check:** `/zalando/markets` to confirm the right
  code, then `/zalando/search` in that market to pull current prices for a
  keyword.
- **Category audit:** `/zalando/category` with a market-specific slug (e.g.
  `shoes` on `de`/`gb`, `chaussures` on `fr`) to list a category's catalog
  and flag items above/below a price threshold.
- **Search-to-detail drill-down:** `/zalando/search` to find candidate SKUs,
  then `/zalando/product` on the best match for full price/size/availability.

## Notes & limits

- **Credits / pay-on-success:** billed only on `2xx`; free tier 2,000 credits/mo.
  Key at [https://crawlora.net](https://crawlora.net?utm_source=github&utm_medium=referral&utm_campaign=crawlora-skills).
- **Public data only** — public product/listing pages; respect Zalando's terms.
- **Security:** key lives in `CRAWLORA_API_KEY` only — never hardcode, query-param, or commit it.
- **Zalando always needs `market`** (no default storefront) — resolve valid
  codes via `/zalando/markets` if unsure. A `sku` is generally only listed
  for sale on the market(s) it was found in, so keep `market` consistent
  between search/category and product-detail calls.
- Category slugs are market-specific (each storefront uses its own
  local-language slug) — take them from that market's own site navigation
  or a product's `url` field, not from another market.
- `/zalando/search` and `/zalando/category` return only the first page of
  results; deeper pagination is not yet supported.
