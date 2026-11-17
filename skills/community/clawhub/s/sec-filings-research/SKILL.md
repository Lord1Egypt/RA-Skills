---
name: sec-filings-research
description: Research SEC EDGAR filings and financial disclosures through Crawlora, including company filings, extracted sections, normalized financials, insider transactions, and institutional holdings. Use for sourced filing briefs and period-aware company or disclosure comparisons.
---

# SEC filings research

Answer filing questions with identifiable documents, reporting periods, and
source links. Separate reported facts, management statements, and analytical
interpretations; a filing lookup alone does not support a buy/sell conclusion.

For a period-matched financial statement matrix across multiple public issuers,
use company-fundamentals-comparison. This skill remains the route for filing
search, section extraction, and issuer-specific disclosure context.

## Setup

Set `CRAWLORA_API_KEY` to your key from [crawlora.net](https://crawlora.net).
Run the bundled `scripts/crawlora.sh` from this skill directory or by absolute
path. It uses `x-api-key` at `https://api.crawlora.net/api/v1`; keep the key in
the environment. Read [reference/endpoints.md](reference/endpoints.md) for live
SEC tools and the selected stored company/position datasets.

## Resolve, retrieve, compare

1. Resolve the correct legal entity with `/sec/company/search?q=...`. Preserve
   the CIK, ticker when available, and company name; tickers and names can change.
2. Use `/sec/company/submissions` with `cik` or `ticker`, optional `form`,
   `from`, `to`, and `limit` (max 500). One company identifier is required even
   when the catalog marks each individual field optional. Filing-date filters
   are not reporting-period filters. Resolve accession numbers from results.
3. Retrieve `/sec/filing` with `accession` plus the company identifier. For a
   10-K/10-Q/8-K analysis, `/sec/filing/sections` accepts `items` and `max_chars`
   (default 20,000; max 200,000 per section). Item numbering differs by form;
   read the returned form/title rather than assuming every Item 7 is MD&A.
4. Compare equivalent sections from the requested filings. If `truncated=true`,
   increase the cap within limits or inspect the primary document using
   `/web/scrape`. If text is still unavailable, narrow the claim. Never conclude
   a risk disappeared solely because it is absent from truncated extraction.
5. For numeric comparisons, `/sec/financials` supports `statement=income`,
   `balance`, or `cash_flow`; `period=annual` or `quarterly`; `limit` up to 20.
   Preserve fiscal period, end date, currency, form, and returned source URL.
   Normalized values use latest-filed figures per period and may reflect
   restatements; they are not necessarily what was known on a historical date.
6. Use the specialized surfaces only when needed:

   | Question | Surface and constraint |
   |---|---|
   | Find filings mentioning a topic | `/sec/full-text-search`; confirm hits in the actual filing |
   | Company overview | `/sec/company/intelligence`; requested unavailable enrichments appear in `degraded` |
   | Insider disclosures | `/sec/insider` with company identifier; inspect transaction codes/roles instead of calling every acquisition a market purchase |
   | Manager's holdings | `/sec/institutional-holdings` requires the **manager's CIK**, not the issuer's ticker; returns latest 13F-HR holdings |
   | Cross-company XBRL fact | `/sec/frames` requires `concept` and `period`; match taxonomy/unit and distinguish duration from instant frames |
   | Bulk company/position discovery | Selected `/datasets/sec-companies/*` and `/datasets/sec-institutional-positions/*`; discover facet values and label these stored snapshots |

```sh
scripts/crawlora.sh /sec/company/search q=Apple
scripts/crawlora.sh /sec/company/submissions ticker=AAPL form=10-K limit=2
# Use a returned accession for filing/sections; do not reuse a stale example ID.
scripts/crawlora.sh /sec/financials ticker=AAPL statement=income period=annual limit=2
```

## Evidence and limits

Return a brief or comparison with entity/CIK, accession, form, filing date,
reporting date/period, cited section or fact, source URL, and retrieval time.
Show calculations and distinguish missing values from zeros.

- Match currency, units, duration, and fiscal calendars. A quarterly cash-flow
  disclosure can be year-to-date; do not assume it is a standalone quarter.
  Calendar frames can contain different start/end dates across filers. Verify
  comparability before calculating growth or ranking companies.
- Check amendments and restatements when the question depends on historical
  changes. An incomplete recent-submissions window is not an exhaustive archive.
- 13F is a delayed reporting snapshot with defined coverage, not a current
  complete portfolio or a record of every trade. Do not infer trade dates or
  investor intent from a change in reported holdings alone.
- Dataset results may lag live filings. Keep data-as-of dates distinct from
  collection time. Inspect `degraded` rather than silently filling enrichment gaps.
- Back off on `429`, retry a transient `5xx` once, stop on `401`/`403`, and
  check application `code`. Preserve partial evidence with explicit gaps.

For XBRL context and frame semantics, see the [SEC's API documentation](https://www.sec.gov/search-filings/edgar-application-programming-interfaces).
