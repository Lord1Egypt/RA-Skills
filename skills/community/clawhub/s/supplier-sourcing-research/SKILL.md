---
name: supplier-sourcing-research
description: Discover and compare suppliers behind brands using Crawlora's ImportYeti company reports and public business websites. Use for supplier shortlists, observed sourcing relationships, shipment-activity comparisons, and questions to qualify potential manufacturers.
---

# Supplier sourcing research

Build a supplier shortlist with identifiable companies, observed trade evidence,
product fit, and unresolved qualification questions. Shipment records establish
observations, not manufacturing quality, available capacity, or willingness to sell.

## Setup

Set `CRAWLORA_API_KEY` to your key from [crawlora.net](https://crawlora.net).
Run the bundled `scripts/crawlora.sh` from this skill directory or by absolute
path. It sends `x-api-key` to `https://api.crawlora.net/api/v1`; keep the key in
the environment. Read [reference/endpoints.md](reference/endpoints.md) for the
selected ImportYeti, search, and website-extraction tools.

## Find and qualify suppliers

1. Establish the product, reference brands, desired geography, and qualification
   criteria. ImportYeti search is by company/supplier name; for a product-only
   brief, first identify relevant importers or brands through web search.
2. Search `/importyeti/search` with `q` and optional 1-based `page`. Resolve names
   against country, address, and official domain before assigning a result to a
   brand. Similar names and importer subsidiaries are not interchangeable.
3. Inspect `kind`. Only `company` results chain into `/importyeti/company?slug=...`.
   **Supplier results have no supplier-detail endpoint in this API.** Use their
   returned search fields and public websites; do not feed a supplier slug to
   the company endpoint. An unknown/empty kind needs manual identity verification.
4. From a company report, retain supplier names/slugs, country, product categories,
   shipment counts, and relevant recent shipment descriptions. Preserve bill-of-
   lading IDs and dates when present. Search/report dates may use different
   day/month orders; retain ambiguous raw dates rather than silently swapping
   them. Keep `url`/`source_url` and collection time.
5. Compare candidates within compatible coverage windows. Counts, TEU, weights,
   containers, and estimated freight spend are different measures; do not treat
   them as product units, purchase value, or share of a brand's total sourcing.
   Deduplicate repeated shipment evidence by bill of lading where possible.
6. Check shortlisted suppliers' official sites using Bing and `/web/scrape` or
   `/extract` (flat JSON bodies). Separate claimed capabilities/certifications
   from independently verified facts. Record MOQ, lead time, certifications,
   capacity, and current availability as unknown unless directly supported.

```sh
scripts/crawlora.sh /importyeti/search q=nike page=1
# Use a returned kind=company slug after checking the entity's identity:
# scripts/crawlora.sh /importyeti/company slug=RETURNED_COMPANY_SLUG
```

## Evidence and output

Return supplier, country/address, observed customer relationship, relevant product
evidence, shipment metric/date scope, official website, fit rationale, and open
qualification questions. Link claims to reports or company pages. Label a freight
forwarder or trading intermediary when evidence supports it; do not assume every
named shipper operates a factory.

- Public shipment coverage is incomplete. Missing air/land records, confidential
  records, or alternate names can hide a relationship; absence is not proof of
  no trade. See [ImportYeti's coverage notes](https://www.importyeti.com/our-data).
- Empty supplier/shipment tables may reflect extraction gaps. Report unavailable
  detail rather than concluding the importer has no suppliers. HS codes are a
  selected upstream list, not a complete product or tariff classification.
- Preserve masked contact fields. Use only publicly provided business channels;
  preparing a shortlist does not send inquiries or initiate orders.
- Bound search pages and report lookups. Stop at `total_pages`, no progress, or
  the requested shortlist size. Back off on `429`, retry transient `5xx` once,
  stop on `401`/`403`, and check application `code` before using `data`.
