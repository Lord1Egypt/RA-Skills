---
name: sec-insider-transaction-analysis
description: Analyze reported company insider transactions using Crawlora live SEC and stored Form 3/4/5 records. Use for transaction-code, owner-role, date-window, and share/value evidence briefs with filing coverage, amendments, derivative scope, and economic interpretation limits preserved.
---

# SEC insider transaction analysis

## Access and scope

Set `CRAWLORA_API_KEY` to your Crawlora key. Prefer the listed Crawlora MCP tools
when connected; otherwise use the bundled `scripts/crawlora.sh`, which sends
`x-api-key` to `https://api.crawlora.net/api/v1`. Read
[reference/endpoints.md](reference/endpoints.md) for exact methods and parameters.
Check application `code` as well as HTTP status; payloads are inside `data`.
Stop on authentication errors, back off on `429`, and retry a transient upstream
failure once. Bound calls/pages by the requested scope and credit budget. Retain
source IDs, URLs, source dates, and observation/crawl times separately.

Describe reported insider activity for selected companies and a transaction-date
window. Establish company identity/CIK, dates, owner/role scope, security class,
and whether the question concerns counts, quantities, or reported consideration.

## Collect and reconcile filing evidence

1. Resolve companies through live SEC or dataset company search; issuer CIKs,
   reporting-owner names, and institutional-manager CIKs are different identities.
   Pass one verified company identifier to live `sec_insider` even though `cik`
   and `ticker` are individually optional in its schema.
2. Live insider data is a bounded recent window (`limit` up to 30). Stored insider
   history filters `from`/`to` on transaction dates and returns at most 200 rows,
   newest first. It is not a paginated exhaustive archive. Separate filing dates,
   transaction dates, reporting periods, and crawl/retrieval times.
3. An unknown CIK or absent stored history can return an empty series; that does
   not prove no transaction occurred. Use submissions/filing metadata to investigate
   relevant document coverage rather than turning an empty sample into a finding.
4. Preserve accession/form, owner name/title and returned role flags, security
   title, transaction code, acquired/disposed indicator, shares, price-per-share,
   holdings-after, and source URL. Verify code meaning in the underlying filing
   context; acquisitions can be grants or exercises rather than discretionary buys.
   Keep derivative/non-derivative and share/principal/security units separate.
5. Deduplicate repeated observations using accession and row identity when
   available. Preserve original and amended filings and label possible replacements
   only with evidence; matching owner/date/amount alone cannot resolve every row.
   Stored ingestion idempotence does not automatically reconcile a live/stored join.

```sh
scripts/crawlora.sh /sec/company/search q=Apple
# Use a returned and verified issuer CIK/ticker, for example:
# scripts/crawlora.sh /sec/insider cik="$COMPANY_CIK" limit=30
# scripts/crawlora.sh "/datasets/sec-companies/insider/$COMPANY_CIK" from=2026-01-01 to=2026-10-05 limit=200
```

## Classify and present the observed activity

Group by the actual code, direction, owner/role, class, and transaction date;
retain unknown codes and missing fields. Director/officer/ten-percent-owner
flags may overlap, so their group totals are not automatically additive.
Do not sum distinct share classes or derivatives into a single ownership change.

Compute `shares × price_per_share` only for compatible numeric units and a
meaningful reported price, labeling it estimated reported consideration rather
than profit or net cash flow. Missing prices remain unknown; zero-price context
can describe a grant/transfer rather than a free market purchase. Holdings-after
need their own security/owner/reporting scope and do not guarantee current ownership.
Show counts/amounts for the retrieved window and cap; netting across owners or
unlike codes can conceal economically different events.

Return a company/filing coverage ledger, classified transaction table, explicit
formulas, amendment/duplicate flags, and unknowns. Do not infer intent, illegal
conduct, plan status, full portfolios, or future price performance from reported
activity. Preparing this brief does not authorise trading or account actions.
