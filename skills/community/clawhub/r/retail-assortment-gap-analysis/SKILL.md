---
name: retail-assortment-gap-analysis
description: Compare competing retail assortments through Crawlora catalogs. Use to find observed gaps in categories, brands, product attributes, variants, and price bands, with explicit catalog coverage and product-matching evidence.
---

# Retail assortment gap analysis

Compare defined category samples or complete collections and identify evidence-backed
assortment gaps. Keep a product absent from the collected sample distinct from one
confirmed absent from a fully enumerated catalog.
For a new physical-product launch idea across marketplaces and review evidence,
use consumer-product-opportunity. This workflow compares existing or supplied
retailer assortments.

## Setup and API contract

Set `CRAWLORA_API_KEY` to your key from [crawlora.net](https://crawlora.net).
Run the bundled `scripts/crawlora.sh` from this skill directory or by absolute
path. It sends `x-api-key` to `https://api.crawlora.net/api/v1`; keep the key in
the environment. Read [reference/endpoints.md](reference/endpoints.md) for the
selected endpoints, required parameters, limits, and response behavior.
Check the application `code` as well as HTTP status; successful payloads are
inside `data`. Stop on `401`/`403`, back off on `429`, and retry a transient
`5xx` once. A failed or partial fetch is not an empty market or catalog.
Bound requests to the user's scope and credit budget. For repeated collection,
save the query, source IDs, pagination progress, and retrieval timestamps with
the results so interrupted work can resume; do not create monitors implicitly.

## Define and collect the comparison

1. Agree on stores, target market, category boundaries, price-band edges, and
   counting unit: parent products or sellable variants. Fix store, country,
   language, currency, and retrieval window before collecting data. Use the user's
   own assortment when supplied, alongside public competitor records.
2. For Shopify, resolve a storefront with `/shopify/store`, discover handles via
   `/shopify/collections`, and enumerate `/shopify/collections/{handle}/products`.
   `/shopify/products` provides the broader storefront catalog. Keep `url` fixed
   across pages and detail calls. Use returned product handles for detail.
   Classic transport does not support server-side sort/facets; do not pass
   `sortBy` unless `transport_mode` is `ssr_embedded` and the reference permits it.
3. For Target, discover `/target/categories`, browse `/target/category-products`,
   and retain returned dynamic filter option IDs. Preserve the same `store_id`
   when supplied by the user for browsing and `/target/product?tcin=...` detail.
   This skill has no Target store-discovery tool: report the default store context
   if a verified ID is unavailable, rather than inventing a local store match.
4. For IKEA, `/ikea/search` finds seed products; fetch detail to take category keys from
   its category paths for `/ikea/category` pagination and item numbers for detail.
   Keep `country` and `language` fixed. Keyword search is a candidate sample,
   not an exhaustive assortment even when its returned page is full.
5. Record pages/offsets, filters, declared totals, unique IDs, and stopping reason.
   Follow each endpoint's pagination limits; Shopify supports up to 250 per page,
   Target category browsing caps at page 50, IKEA category uses offset/size.
   A request budget or endpoint cap means partial coverage. Deduplicate overlapping
   collections and stop if pages repeat rather than assuming new coverage.

```sh
scripts/crawlora.sh /ikea/search q=desk country=us language=en size=10
scripts/crawlora.sh /target/categories
# For a user-selected Shopify store, use its URL unchanged through discovery:
# scripts/crawlora.sh /shopify/collections url="$STOREFRONT_URL" limit=50 page=1
```

## Normalize and identify gaps

- Build a shared category/attribute mapping while preserving each store's original
  taxonomy. Store-specific category IDs and labels are not cross-store keys.
- Match identical products using a returned GTIN or verified brand/model/variant
  combination. Treat retailer-local IDs as local. A similar title is only a
  candidate match; private-label alternatives belong in an attribute comparison.
- Count parent products once for breadth; count sizes/colors only in the variant
  view. A sold-out variant is an availability gap, not a missing catalog product.
- Use consistent currency, tax context, pack quantity, dimensions, and sale versus
  regular price basis. Do not compare a multipack with a single item by sticker
  price alone. Avoid counting a product's minimum variant price as every variant's
  price. Keep missing brand, attributes, or prices in an unknown bucket.
- Calculate category/brand/price-band shares with explicit denominators and unknown
  counts. For incomplete coverage, label differences as observed sample gaps.
  A niche carried by a competitor is not proof of sales, demand, or profitability.

## Deliverable

Return a coverage ledger, comparable assortment matrix, and prioritized gap list.
For each proposed gap show category/attribute, stores observed, product and variant
counts, price basis, example source URLs/IDs, collection time, confidence, and what
would validate demand. Explain whether evidence supports absence, out-of-stock,
unknown coverage, or a taxonomy mismatch. Do not turn a snapshot into a trend;
changes require comparable saved snapshots and the same collection scope.
