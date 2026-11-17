---
name: shopify-research
description: Researches independent Shopify-powered storefronts — products, collections, pages, sitemaps, search suggestions, and product recommendations — using the Crawlora API, returning clean JSON for any store by domain, plus 14 pre-wired DTC brand storefronts (Allbirds, Brooklinen, Cole Haan, Everlane, Fashion Nova, Gymshark, J.Crew, Kylie Cosmetics, Oh Polly, Quince, Rothy's, SKIMS, Steve Madden, The Body Shop). Use when the user asks to audit a Shopify store's catalog, crawl its sitemap, look up a product or collection, or pull search/recommendation data — instead of scraping the store's pages directly.
allowed-tools: Bash(scripts/crawlora.sh:*)
---

# Shopify store research

Look up and crawl independent Shopify-powered storefronts — products,
collections, pages, sitemaps, predictive search, and product recommendations
— all as normalized JSON from the Crawlora API, with no HTML scraping. Works
against any Shopify store by domain (not Shop.app; see the separate
`shop-app-research` skill for that), plus 14 brand storefronts with their own
pre-wired, no-`url`-needed endpoints: Allbirds, Brooklinen, Cole Haan,
Everlane, Fashion Nova, Gymshark, J.Crew, Kylie Cosmetics, Oh Polly, Quince,
Rothy's, SKIMS, Steve Madden, and The Body Shop.

## Tool scope and data flow

The optional shell helper is the only command this skill asks to run. It makes
GET requests only to the documented, allowlisted Crawlora routes. When invoked,
it reads `CRAWLORA_API_KEY` and sends it as an `x-api-key` header over HTTPS to
`api.crawlora.net`; it does not send the key to the Shopify storefront. It
briefly writes a mode-600 curl config under `TMPDIR` and removes it when the
command exits. It does not inspect other environment variables, enumerate files,
install software, or run with elevated privileges. Storefront URLs are passed as
ordinary query values; the helper's destination host is fixed. Run it only when
you want to make a Crawlora API request; successful requests can consume credits.

## When to use this skill

- "List the products/collections in this Shopify store."
- "What's on this Shopify store's `/pages/about` page?"
- "Crawl this Shopify store's sitemap for every product URL."
- "What does this Shopify store's search suggest for 'running shoes'?"
- "What products does Shopify recommend alongside this product?"
- Catalog audits, competitive-assortment research, or full-store crawls of a
  Shopify-powered site.

## Setup (one-time)

- Get a free Crawlora API key (2,000 credits/mo, no card) at [https://crawlora.net](https://crawlora.net?utm_source=github&utm_medium=referral&utm_campaign=crawlora-skills).
- Set `CRAWLORA_API_KEY` in the environment before running the helper.
- The helper reads `CRAWLORA_API_KEY` from the environment and sends requests to `https://api.crawlora.net/api/v1`. Missing/invalid key → `401`.

## How it works

Every call takes the storefront's `url` (the store's public domain, e.g.
`https://example.myshopify.com` or a custom domain like
`https://example.com`) plus endpoint-specific params:

1. **Resolve the store** — `/shopify/store` returns normalized storefront
   metadata; if the vanity domain blocks `/products.json`, it falls back to
   the store's public `*.myshopify.com` domain.
2. **Browse the catalog** — `/shopify/collections` and `/shopify/products`
   (paginated, `limit` up to 250) list collections and products; drill into
   one collection's products with `/shopify/collections/{handle}/products`.
3. **Detail** — `/shopify/products/{handle}` for a single product's full
   detail.
4. **Recommendations** — `/shopify/products/{handle}/recommendations`
   (`intent=related|complementary`) for cross-sell/upsell data.
5. **Static content** — `/shopify/pages` and `/shopify/pages/{handle}` for
   the store's static pages (body HTML returned as cleaned text).
6. **Sitemap crawl** — `/shopify/sitemaps` lists the child sitemaps;
   `/shopify/sitemap/urls` (`type=products|collections|pages|blogs|...`)
   returns capped URL entries from them, useful for enumerating a whole
   store without paginating every list endpoint.
7. **Search** — `/shopify/search/suggest` (`q=`, optional `types=`) returns
   predictive-search products, collections, and query suggestions.
8. **Brand-pinned stores** — the same operations exist under a brand prefix
   with no `url` param needed, e.g. `/allbirds/products`,
   `/rothys/products/{handle}`, `/skims/sitemap/urls`. Use these instead of
   `/shopify/...?url=...` when the user names one of the 14 pre-wired
   brands directly.

Full endpoint list, methods, and params: [`reference/endpoints.md`](reference/endpoints.md).

## Calling the API

```sh
# Resolve store metadata:
scripts/crawlora.sh /shopify/store url="https://example.myshopify.com"

# List products / collections (paginated):
scripts/crawlora.sh /shopify/products url="https://example.myshopify.com" limit=100 page=1
scripts/crawlora.sh /shopify/collections url="https://example.myshopify.com"

# Crawl the sitemap for every product URL:
scripts/crawlora.sh /shopify/sitemap/urls url="https://example.myshopify.com" type=products limit=250
```

Use `scripts/crawlora.sh` for all requests; it keeps the API key out of command-line arguments.


## Endpoint reference

See [`reference/endpoints.md`](reference/endpoints.md) for every Shopify
endpoint this skill uses (method, path, params, description), including
the 14 brand-pinned mirrors.

## Examples

- **Catalog audit:** `/shopify/products` (paginate with `page`/`limit`) to
  list a store's full catalog with prices and variants, then flag gaps or
  outliers.
- **Sitemap-driven full crawl:** `/shopify/sitemaps` to find the child
  sitemaps, then `/shopify/sitemap/urls?type=products` to enumerate every
  product URL without walking paginated list endpoints.
- **Search & recommendation research:** `/shopify/search/suggest` for a
  query to see what a store's predictive search surfaces, then
  `/shopify/products/{handle}/recommendations` to map cross-sell links
  between products.

## Notes & limits

- **Credits / pay-on-success:** billed only on `2xx`; free tier 2,000 credits/mo.
  Key at [https://crawlora.net](https://crawlora.net?utm_source=github&utm_medium=referral&utm_campaign=crawlora-skills).
- **Public data only** — public storefront pages; respect each store's terms.
- **Security:** key lives in `CRAWLORA_API_KEY` only — never hardcode, query-param, or commit it.
- **`url` is required on every call** — the store's public domain
  (`*.myshopify.com` or custom domain); there's no default store.
- Results are paginated — pass `page` (and `limit` where supported, up to
  250) to walk collections, products, and pages.
- Product/collection/page lookups take a `handle`, not a numeric ID —
  discover handles via the list endpoints or sitemap crawl first.
- Empty result pages return `200` with an empty array rather than an error —
  check the array length to know when to stop paginating.
