---
name: startup-acquisition-research
description: Screen startups listed for sale using Crawlora's TrustMRR marketplace, stored company records, and daily metric history. Use for acquisition candidate shortlists, asking-price comparisons, revenue-history checks, and evidence-based diligence questions.
---

# Startup acquisition research

Screen candidates against the buyer's constraints and identify what still needs
verification. Separate payment-provider-verified revenue, seller claims, automated
summaries/scores, and your calculations.

## Setup

Set `CRAWLORA_API_KEY` to your key from [crawlora.net](https://crawlora.net).
Run the bundled `scripts/crawlora.sh` from this skill directory or by absolute
path. It sends `x-api-key` to `https://api.crawlora.net/api/v1`; keep the key in
the environment. Read [reference/endpoints.md](reference/endpoints.md) for
TrustMRR live tools, stored records/history, and website research.

## Screen, refresh, inspect history

1. Translate the brief into asking-price range, recurring/non-recurring model,
   customer type, category, operating requirements, and evidence requirements.
   Do not impose an arbitrary deal score or investment recommendation.
2. Discover exact dataset labels through `/datasets/trustmrr/facets`, then search
   `/datasets/trustmrr/search` with `on_sale=true`, `status=active`, and relevant
   filters such as `max_asking_price`, `min_mrr`, or `target_audience`. Dataset
   category labels and live `/trustmrr/categories` slugs need not be identical.
3. Retrieve `/datasets/trustmrr/items/{slug}` and refresh serious candidates with
   `/trustmrr/startup/{slug}`. Verify current sale status/asking price and record
   any disagreement with the stored snapshot. `/trustmrr/acquire` and
   `/trustmrr/marketplace` provide discovery snapshots, not an exhaustive census.
4. Read `/datasets/trustmrr/history/{slug}` with optional inclusive UTC `from`/`to`
   dates and `limit` (max 1000). Points are oldest first; a limit selects the most
   recent points in the range. Newly observed businesses can return an empty or
   short series. Do not invent earlier history or treat missing dates as zeros.
5. Compare MRR, trailing-30-day revenue, all-time revenue, asking price, and
   growth with their dates and definitions intact. Consecutive `revenue_30d`
   points overlap: summing them does not produce monthly or annual revenue.
   If calculating price / (12 × MRR), label that denominator explicitly; do not
   assume the upstream `multiple` uses the same formula. Zero/unknown denominators
   produce an unavailable multiple. MRR=0 need not mean a non-recurring business
   has no revenue. Merchant-of-record volumes need separate interpretation.
6. Inspect the actual product and public pricing via `/web/scrape` where needed.
   Convert gaps into diligence questions: profit/costs, refunds, retention,
   customer concentration, founder workload, ownership, and transferability.
   Those facts are not established by revenue verification or an AI summary.

```sh
scripts/crawlora.sh /datasets/trustmrr/search \
  on_sale=true status=active max_asking_price=100000 page_size=5
# Resolve a slug from results before requesting its live detail and history.
```

## Evidence and output

Return a candidate table with source links, business/model, current sale status,
asking price, dated revenue metrics, history coverage, explicitly defined
calculations, fit rationale, discrepancies, and open diligence questions.

- Payment-provider verification is not a financial audit, profit verification,
  or proof that the business can be transferred. See [TrustMRR's FAQ](https://trustmrr.com/faq)
  for the platform's verification and marketplace context.
- Asking prices are seller requests, not completed transaction prices. Upstream
  deal scores and sponsored placement are discovery signals, not independent value.
- Recorded growth can reflect a small baseline, a promotion, or changing coverage.
  Present observations without projecting guaranteed future returns.
- Bound search to `page_size<=100`, the 10,000-result window, and the brief.
  Back off on `429`, retry transient `5xx` once, stop on `401`/`403`, and check
  application `code`. Research does not place offers or contact sellers.
