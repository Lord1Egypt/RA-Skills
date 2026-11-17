---
name: supply-chain-concentration-analysis
description: Analyze observed supplier and origin concentration using Crawlora ImportYeti company reports and public company evidence. Use for a sourced supply-chain exposure brief with importer/supplier identity, shipment measures, periods, incomplete tables, and procurement-volume limits preserved.
---

# Supply-chain concentration analysis

## Access and scope

Set `CRAWLORA_API_KEY` to your Crawlora key. Prefer the listed Crawlora MCP tools
when connected; otherwise use the bundled `scripts/crawlora.sh`, which sends
`x-api-key` to `https://api.crawlora.net/api/v1`. Read
[reference/endpoints.md](reference/endpoints.md) for exact methods and parameters.
Check application `code` as well as HTTP status; payloads are inside `data`.
Stop on authentication errors, back off on `429`, and retry a transient upstream
failure once. Bound calls/pages by the requested scope and credit budget. Retain
source IDs, URLs, source dates, and observation/crawl times separately.

Describe observed supplier/origin exposure for specified importers. Establish
company identity, product scope, time window, and intended measure before
interpreting a customs report as a supply-chain picture.

## Resolve entities and comparable report measures

- Search ImportYeti by company name and verify address/country/domain. Only
  `kind=company` results chain into company detail; no supplier-detail endpoint
  is available here. A supplier/trading intermediary is not automatically a
  manufacturing site. Preserve the canonical report URL when a loose slug resolves.
- Retain supplier names/slugs, reported shipment counts, product categories,
  recent bill-of-lading IDs/dates, origin breakdown, headline totals, TEU,
  weights, container/quantity strings, and estimated shipping spend separately.
  They do not share one denominator or necessarily the same observation period.
- Deduplicate recent shipment evidence using bill-of-lading and actual row scope;
  supplier aliases and subsidiaries need identity evidence before aggregation.
  A shared address/domain can indicate a related entity rather than the same factory.
- Tables can be missing because extraction/templates changed. Empty suppliers,
  regions or shipments do not establish zero activity. The HS/HTS list is a
  selected top-ten surface, not a complete tariff/product classification.

```sh
scripts/crawlora.sh /importyeti/search q="Target" page=1
# Verify a returned company-kind entity and canonical slug before its report:
# scripts/crawlora.sh /importyeti/company slug="$COMPANY_SLUG"
```

## Quantify only the supported exposure

A supplier share requires compatible shipment measure, reporting period and a
complete denominator. Do not divide a lifetime supplier count by a recent-shipment
sample or use a selected table subtotal as the importer's total procurement.
If only a partial comparable table exists, show observed sample shares and
coverage instead. Preserve source region percentages with their source scope;
don't force unlike tables to reconcile to 100%.

Counts, TEU, weight, cartons, containers and estimated freight costs are not
interchangeable product units or purchase values. Public shipment coverage is
incomplete and can omit transport modes, confidential records and alternate names.
Do not infer that absent records mean no supplier relationship, or that apparent
concentration establishes capacity, quality, geopolitical causality, or disruption.
Use verified company pages for attributed capability/context claims, leaving
certifications, current availability and alternatives unverified when unsupported.

Return entity/period/measure ledgers, observed supplier and origin breakdowns,
source-supported concentration measures, sample gaps, and qualification questions.
This is an exposure brief, not a procurement audit or guarantee. Do not contact
suppliers, submit inquiries, place orders, or invent unmasked contact details.
