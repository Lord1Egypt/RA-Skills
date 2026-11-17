# sec-insider-transaction-analysis — endpoint reference

> Generated from `scripts/tools.json` by `scripts/generate.mjs` — do not edit by hand.

Only the endpoints used by this workflow. Call them via `scripts/crawlora.sh` (see SKILL.md).

All paths are relative to the API base `https://api.crawlora.net/api/v1` and require the header `x-api-key: $CRAWLORA_API_KEY`. Path params like `{id}` are substituted into the URL; `GET` params go in the query string; `POST` params go in a JSON body.

**7 endpoints across 2 platform group(s).**

## SEC EDGAR (4)

### `sec_company_search`

- **HTTP:** `GET /sec/company/search`
- **What:** Resolve a ticker or company name to EDGAR companies. Resolves a ticker symbol or company-name query to SEC EDGAR companies (CIK, ticker, name).
- **Params:** `limit` (integer, optional) — Max matches, default 10, max 100; `q` (string, **required**) — Ticker symbol or company name

### `sec_company_submissions`

- **HTTP:** `GET /sec/company/submissions`
- **What:** List a company's EDGAR filings. Returns a company's recent SEC filings (form, dates, primary document URL) filtered by form type and date range, plus company profile fields as reported by EDGAR: entity_type, former_names, exchanges, category, fiscal_year_end, state_of_incorporation. Provide cik or ticker.
- **Params:** `cik` (string, optional) — SEC CIK (numeric or zero-padded); `form` (string, optional) — Filter by form type, e.g. 10-K, 10-Q, 8-K; `from` (string, optional) — Earliest filing date (YYYY-MM-DD); `limit` (integer, optional) — Max filings, default 50, max 500; `ticker` (string, optional) — Ticker symbol (alternative to cik); `to` (string, optional) — Latest filing date (YYYY-MM-DD)

### `sec_filing`

- **HTTP:** `GET /sec/filing`
- **What:** Get a single filing by accession number. Returns a single SEC filing's metadata and primary document URL. Provide accession plus cik or ticker.
- **Params:** `accession` (string, **required**) — Accession number; `cik` (string, optional) — SEC CIK (numeric or zero-padded); `ticker` (string, optional) — Ticker symbol (alternative to cik)

### `sec_insider`

- **HTTP:** `GET /sec/insider`
- **What:** Insider transactions (Forms 3/4/5). Returns a company's recent insider transactions from Form 3/4/5 ownership filings (owner, role, security, shares, price). Provide cik or ticker.
- **Params:** `cik` (string, optional) — SEC CIK (numeric or zero-padded); `limit` (integer, optional) — Max transactions, default 10, max 30; `ticker` (string, optional) — Ticker symbol (alternative to cik)

## Datasets (3)

### `datasets_sec_companies_insider`

- **HTTP:** `GET /datasets/sec-companies/insider/{cik}`
- **What:** Get a SEC company's insider-transaction history. Returns a company's insider (Form 3/4/5) transaction history from the SEC companies dataset, most recent transaction first. An unknown CIK or a company with no reported transactions returns an empty series rather than a 404.
- **Params:** `cik` (string, **required**) — SEC CIK, numeric or zero-padded; `code` (string, optional) — Exact transaction code filter, e.g. P (open-market purchase), S (sale); `from` (string, optional) — Inclusive start date (YYYY-MM-DD, UTC) filtering transaction date; `limit` (integer, optional) — Maximum transactions returned (most recent first), default 50, max 200; `to` (string, optional) — Inclusive end date (YYYY-MM-DD, UTC) filtering transaction date

### `datasets_sec_companies_item`

- **HTTP:** `GET /datasets/sec-companies/items/{cik}`
- **What:** Get a company from the SEC companies dataset. Returns one SEC-reporting company by CIK from dataset id `sec-companies`, including its filing-history summary, financial-statement rollups, and trailing-90-day insider-activity summary. Returns 404 when the CIK is not in the dataset.
- **Params:** `cik` (string, **required**) — SEC CIK, numeric or zero-padded, e.g. 320193 or 0000320193

### `datasets_sec_companies_search`

- **HTTP:** `GET /datasets/sec-companies/search`
- **What:** Search the SEC companies dataset. Searches SEC-reporting companies — filing history, financial-statement rollups (latest annual/quarterly revenue, net income, total assets) and trailing-90-day insider (Form 3/4/5) activity. Sort enum: `relevance`, `name_asc`, `revenue_desc`, `net_income_desc`, `filing_recent_desc`, `insider_activity_desc`. `entity_type`, `sic`, `sic_description`, `exchange`, and `state_of_incorporation` are open filters over the exact values EDGAR reports for each filer (not a fixed enum) — discover real values via the matching facet. Billing: this search costs 1 credit per record returned, with a minimum of 2 (an empty result costs 2, a full page of 100 costs 100).
- **Params:** `cik` (string, optional) — Exact CIK filter, numeric or zero-padded, e.g. 320193 or 0000320193; `entity_type` (string, optional) — Exact entity-type filter as reported by EDGAR (e.g. operating), max 64 characters; `exchange` (string, optional) — Exact exchange filter as reported by EDGAR, e.g. Nasdaq, NYSE, max 64 characters; `form_filed` (string, optional) — Exact form-type filter; keeps only companies that have ever filed this form, e.g. 10-K, 8-K; `has_financials` (boolean, optional) — When true, keep only companies that have XBRL financial statements; `max_revenue` (number, optional) — Maximum latest-annual revenue in USD (normalized), 0 or greater; `min_insider_txn_count_90d` (integer, optional) — Minimum insider (Form 3/4/5) transaction count in the trailing 90 days, 0 or greater; `min_net_income` (number, optional) — Minimum latest-annual net income in USD (normalized; negative allowed); `min_revenue` (number, optional) — Minimum latest-annual revenue in USD (normalized from the filer's reporting currency at reference rates), 0 or greater; `min_total_assets` (number, optional) — Minimum latest-annual total assets in USD (normalized), 0 or greater; `page` (integer, optional) — Page number, defaults to 1; `page_size` (integer, optional) — Page size, defaults to 20 and maxes at 100; page * page_size must be <= 10000; `q` (string, optional) — Full-text query over the company name, or an exact ticker match, max 256 characters; `reporting_currency` (string, optional) — Exact reporting-currency filter, ISO-4217 code, e.g. USD, JPY, EUR; `sic` (string, optional) — Exact SIC industry-code filter, e.g. 3571, max 32 characters; `sic_description` (string, optional) — Exact SIC description filter, e.g. Electronic Computers, max 128 characters; `sort` (string, optional) — Sort enum: relevance, name_asc, revenue_desc, net_income_desc, filing_recent_desc, insider_activity_desc; `state_of_incorporation` (string, optional) — Exact state/country-of-incorporation filter as reported by EDGAR, e.g. DE, CA, max 32 characters; `ticker` (string, optional) — Exact ticker filter (case-insensitive), e.g. AAPL, max 32 characters
