---
name: zappos-research
description: Researches Zappos's footwear and apparel catalog — the brand directory, product search, and product detail (pricing, images, ratings, fit feedback, color variants) — using the Crawlora API, returning clean JSON. Use when the user asks to find a shoe or apparel item on Zappos, look up or browse a specific Zappos brand's catalog, or pull a Zappos product's pricing/rating/variant/fit detail — instead of scraping zappos.com.
---

# Zappos research

Browse the Zappos brand directory, search products, and pull full product
detail — pricing, images, ratings, reviewer fit feedback, and color
variants — all as normalized JSON from the Crawlora API, with no HTML
scraping.

## When to use this skill

- "Find X on Zappos" / "search Zappos for running shoes."
- "List Zappos's brands" / "does Zappos carry [brand]?" / "browse [brand]'s catalog on Zappos."
- "What does X cost on Zappos?" or "pull the price/rating/color options for this Zappos product."
- "What do reviewers say about the fit of this Zappos shoe (size/width/arch)?"
- Suggest search terms or refine a vague query before searching Zappos.

## Setup (one-time)

- Get a free Crawlora API key (2,000 credits/mo, no card) at [https://crawlora.net](https://crawlora.net?utm_source=github&utm_medium=referral&utm_campaign=crawlora-skills).
- Set `CRAWLORA_API_KEY` in the environment before running the helper.
- The helper reads `CRAWLORA_API_KEY` from the environment and sends requests to `https://api.crawlora.net/api/v1`. Missing/invalid key → `401`.

## How it works

1. **Find the brand directory** — `/zappos/brands` (optional `q` substring
   filter, `page`/`page_size`) lists brands discovered from Zappos's own
   sitemap, each with an `id`/`url` and a derived `name`. Use it when you
   need a brand id or just want to check whether Zappos carries a brand.
2. **Browse a brand's catalog** — `/zappos/brand` (`brand`, `page`) takes
   that id, a `slug/id.zso` path, or a full brand URL copied from
   zappos.com, and returns the brand's product grid with filter facets.
3. **Search** — `/zappos/search` (`term`, `page`) searches the full catalog
   by keyword and returns normalized products (brand, price, sale status,
   rating, review count) plus facets (gender, department, shoe size, and
   more), each with a live result count. `/zappos/suggest` (`query`) returns
   Zappos's own typeahead suggestions if you need to refine a vague term
   before searching.
4. **Product detail** — `/zappos/product/{productId}` (from a search
   result's `product_id`) returns full detail: name, brand, description,
   pricing, images, aggregate rating, up to two featured reviews, reviewer
   fit feedback for size/width/arch, and every sibling color variant with
   its own price. Pass `colorId` to pin a specific color.
5. **Compare** the JSON fields (price, rating, fit feedback, variants)
   across items or brands and answer.

Full endpoint list, methods, and params: [`reference/endpoints.md`](reference/endpoints.md).

## Calling the API

```sh
# List/filter the brand directory (GET, key=value params):
scripts/crawlora.sh /zappos/brands q=nike | jq '.'

# Browse a brand's catalog by id/slug/url:
scripts/crawlora.sh /zappos/brand brand="nike.zso" page=1 | jq '.'

# Search Zappos:
scripts/crawlora.sh /zappos/search term="waterproof hiking boots" | jq '.'

# Product detail, with a specific color variant:
scripts/crawlora.sh /zappos/product/8729238 colorId=6132 | jq '.data'
```

Use `scripts/crawlora.sh` for all requests; it keeps the API key out of command-line arguments.


## Endpoint reference

See [`reference/endpoints.md`](reference/endpoints.md) for every Zappos
endpoint this skill uses (method, path, params, description).

## Examples

- **Brand catalog audit:** `/zappos/brands` with `q="new balance"` to find
  the brand's id/url, then `/zappos/brand` paginated to list its full
  product grid with prices.
- **Search + compare:** `/zappos/search` for a query, inspect the returned
  facets and prices across results, then `/zappos/product/{productId}` on
  the top candidates to compare rating, fit feedback, and color variants
  before recommending one.
- **Fit due-diligence:** `/zappos/product/{productId}` to pull reviewer
  fit feedback (size/width/arch) and featured reviews before answering
  "does this shoe run true to size?"

## Notes & limits

- **Credits / pay-on-success:** billed only on `2xx`; free tier 2,000 credits/mo.
  Key at [https://crawlora.net](https://crawlora.net?utm_source=github&utm_medium=referral&utm_campaign=crawlora-skills).
- **Public data only** — public Zappos brand/search/product pages; respect Zappos's terms.
- **Security:** key lives in `CRAWLORA_API_KEY` only — never hardcode, query-param, or commit it.
- Results are paginated — pass `page` (1-based) to walk `brand`/`brands`/`search`
  results; `brands` also takes `page_size` (default 100, max 1000).
- **Brand `name` is derived**, not an authoritative site-provided label —
  `/zappos/brands` title-cases the brand's own URL slug to produce it.
- A page past the last result, or an unmatched `/zappos/suggest` query,
  returns a normal empty result rather than an error; an unrecognized
  `brand` or `productId` returns `404`.
- **No reviews or store-locator endpoint** — `/zappos/product` only
  surfaces up to two featured reviews and aggregate fit feedback baked
  into the product response; there's no separate paginated reviews
  endpoint or physical-store lookup here.
