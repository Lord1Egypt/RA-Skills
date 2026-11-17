# sec-filings-research — endpoint reference

> Generated from `scripts/tools.json` by `scripts/generate.mjs` — do not edit by hand.

Only the endpoints used by this workflow. Call them via `scripts/crawlora.sh` (see SKILL.md).

All paths are relative to the API base `https://api.crawlora.net/api/v1` and require the header `x-api-key: $CRAWLORA_API_KEY`. Path params like `{id}` are substituted into the URL; `GET` params go in the query string; `POST` params go in a JSON body.

**18 endpoints across 3 platform group(s).**

## Datasets (7)

### `datasets_sec_companies_facets`

- **HTTP:** `GET /datasets/sec-companies/facets`
- **What:** Facet the SEC companies dataset. Returns terms-aggregation counts for one facet of the SEC companies dataset, scoped to the same filters as search. Facet enum: `sic`, `sic_description`, `exchange`, `state_of_incorporation`, `entity_type`, `reporting_currency`, `revenue_band`, `forms_filed`. `revenue_band` buckets latest-annual revenue into: `unknown`, `under_1m`, `1m_10m`, `10m_100m`, `100m_1b`, `1b_10b`, `over_10b`.
- **Params:** `entity_type` (string, optional) — Exact entity-type filter, max 64 characters; `exchange` (string, optional) — Exact exchange filter as reported by EDGAR, max 64 characters; `facet` (string, **required**) — Facet enum: sic, sic_description, exchange, state_of_incorporation, entity_type, reporting_currency, revenue_band, forms_filed; `form_filed` (string, optional) — Exact form-type filter, e.g. 10-K, 8-K; `has_financials` (boolean, optional) — When true, keep only companies that have XBRL financial statements; `min_revenue` (number, optional) — Minimum latest-annual revenue in USD (normalized at reference rates), 0 or greater; `q` (string, optional) — Full-text query over the company name, or an exact ticker match, max 256 characters; `reporting_currency` (string, optional) — Exact reporting-currency filter, ISO-4217 code, e.g. USD, JPY, EUR; `sic` (string, optional) — Exact SIC industry-code filter, max 32 characters; `state_of_incorporation` (string, optional) — Exact state/country-of-incorporation filter, max 32 characters; `ticker` (string, optional) — Exact ticker filter (case-insensitive), max 32 characters

### `datasets_sec_companies_financials`

- **HTTP:** `GET /datasets/sec-companies/financials/{cik}`
- **What:** Get a SEC company's financial-statement history. Returns a company's financial-statement history (income statement, balance sheet, cash flow) from the SEC companies dataset, newest fiscal year first. An unknown CIK or a company with no XBRL data returns an empty series rather than a 404 — most filers without a current ticker have no financial-statement history at all. `lines` keys are the same concept names the live `/sec/financials` endpoint uses (e.g. `revenue`, `net_income`, `total_assets`); `ratios` keys include `gross_margin`, `operating_margin`, `net_margin`, `revenue_growth_yoy`, `current_ratio`, `debt_to_equity`, `free_cash_flow` where derivable. statement enum: `income`, `balance`, `cash_flow`. period enum: `annual`, `quarterly`.
- **Params:** `cik` (string, **required**) — SEC CIK, numeric or zero-padded; `from` (integer, optional) — Inclusive lower bound on fiscal_year; `limit` (integer, optional) — Maximum points returned (most recent fiscal years first), default 100, max 400; `period` (string, optional) — Period-type enum: annual, quarterly. Omit to return both.; `statement` (string, optional) — Statement enum: income, balance, cash_flow. Omit to return all three.; `to` (integer, optional) — Inclusive upper bound on fiscal_year

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

### `datasets_sec_institutional_positions_facets`

- **HTTP:** `GET /datasets/sec-institutional-positions/facets`
- **What:** Facet the SEC institutional positions dataset. Returns terms-aggregation counts for one facet of the SEC institutional positions dataset, scoped to the same filters as search. Facet enum: `manager`, `issuer`.
- **Params:** `cusip` (string, optional) — Exact CUSIP filter, max 16 characters; `facet` (string, **required**) — Facet enum: manager, issuer; `issuer_name` (string, optional) — Issuer-name text filter (best-effort match), max 256 characters; `manager_cik` (string, optional) — Exact institutional-manager CIK filter, numeric or zero-padded

### `datasets_sec_institutional_positions_search`

- **HTTP:** `GET /datasets/sec-institutional-positions/search`
- **What:** Search the SEC institutional positions dataset. Searches institutional investment managers' quarterly 13F portfolio holdings stored in a search index. Filter by manager_cik for a manager's full reported portfolio (an exact, reliable filter), or by issuer_name/cusip for a best-effort view of which managers reported a position in an issuer — SEC publishes no authoritative CUSIP-to-CIK mapping, so the issuer side is never a guaranteed-resolved join. Sort enum: `value_desc`, `value_asc`, `shares_desc`. Billing: this search costs 1 credit per record returned, with a minimum of 2 (an empty result costs 2, a full page of 100 costs 100).
- **Params:** `cusip` (string, optional) — Exact CUSIP filter, max 16 characters; `issuer_name` (string, optional) — Issuer-name text filter (best-effort match, not a resolved CIK join), max 256 characters; `manager_cik` (string, optional) — Exact institutional-manager CIK filter, numeric or zero-padded; `page` (integer, optional) — Page number, defaults to 1; `page_size` (integer, optional) — Page size, defaults to 20 and maxes at 100; page * page_size must be <= 10000; `sort` (string, optional) — Sort enum: value_desc, value_asc, shares_desc

## SEC EDGAR (10)

### `sec_company_intelligence`

- **HTTP:** `GET /sec/company/intelligence`
- **What:** Company 360 overview from SEC data. Aggregates a company's profile, a latest-annual financial snapshot, the latest 10-K/10-Q/8-K, and recent material events into one call. Provide cik or ticker. Optionally fuse live cross-source data with enrich (a comma list of market, news, hiring): market and news are keyed on the ticker; hiring needs ats plus that ATS's careers slug (or tenant/datacenter/site for Workday). Enrichment is best-effort — requested-but-unavailable sources are listed under degraded and never fail the SEC-native response.
- **Params:** `ats` (string, optional) — ATS provider for hiring enrichment; `careers_slug` (string, optional) — Careers board slug for hiring (greenhouse/lever/ashby/smartrecruiters); `cik` (string, optional) — SEC CIK (numeric or zero-padded); `datacenter` (string, optional) — Workday datacenter shard (hiring, when ats=workday); `enrich` (string, optional) — Comma list of cross-source enrichments; `site` (string, optional) — Workday career site (hiring, when ats=workday); `tenant` (string, optional) — Workday tenant (hiring, when ats=workday); `ticker` (string, optional) — Ticker symbol (alternative to cik)

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

### `sec_filing_sections`

- **HTTP:** `GET /sec/filing/sections`
- **What:** Extract 10-K/10-Q/8-K item sections. Extracts item sections (e.g. 1A Risk Factors, 7 MD&A) from a 10-K/10-Q/8-K primary document as clean text. Provide accession plus cik or ticker.
- **Params:** `accession` (string, **required**) — Accession number; `cik` (string, optional) — SEC CIK (numeric or zero-padded); `items` (string, optional) — Comma-separated item numbers to return, e.g. 1A,7; `max_chars` (integer, optional) — Max characters per section, default 20000, max 200000; `ticker` (string, optional) — Ticker symbol (alternative to cik)

### `sec_financials`

- **HTTP:** `GET /sec/financials`
- **What:** Normalized income statement, balance sheet, or cash flow. Returns a company's financial statements across recent periods, resolving EDGAR's inconsistent XBRL tags to a stable schema. Provide cik or ticker.
- **Params:** `cik` (string, optional) — SEC CIK (numeric or zero-padded); `limit` (integer, optional) — Number of periods, default 5, max 20; `period` (string, optional) — Period basis, default annual; `statement` (string, optional) — Statement, default income; `ticker` (string, optional) — Ticker symbol (alternative to cik)

### `sec_frames`

- **HTTP:** `GET /sec/frames`
- **What:** Cross-company values for one XBRL concept and period. Returns every filer's reported value for one XBRL concept in one reporting period (an EDGAR "frame").
- **Params:** `concept` (string, **required**) — XBRL concept tag, e.g. Assets, Revenues; `limit` (integer, optional) — Max companies, default 200, max 2000; `period` (string, **required**) — Reporting frame, e.g. CY2024, CY2024Q1, CY2024Q4I; `taxonomy` (string, optional) — XBRL taxonomy, default us-gaap; `unit` (string, optional) — Unit of measure, default USD

### `sec_full_text_search`

- **HTTP:** `GET /sec/full-text-search`
- **What:** Full-text search across EDGAR filings. Searches the full text of SEC EDGAR filings, filtered by form and date, with pagination. Free where incumbents gate full-text search behind paid tiers.
- **Params:** `forms` (string, optional) — Filter by form types, comma-separated; `from` (string, optional) — Earliest filing date (YYYY-MM-DD); `page` (integer, optional) — 1-based page number, default 1; `q` (string, **required**) — Search query (supports quoted phrases); `to` (string, optional) — Latest filing date (YYYY-MM-DD)

### `sec_insider`

- **HTTP:** `GET /sec/insider`
- **What:** Insider transactions (Forms 3/4/5). Returns a company's recent insider transactions from Form 3/4/5 ownership filings (owner, role, security, shares, price). Provide cik or ticker.
- **Params:** `cik` (string, optional) — SEC CIK (numeric or zero-padded); `limit` (integer, optional) — Max transactions, default 10, max 30; `ticker` (string, optional) — Ticker symbol (alternative to cik)

### `sec_institutional_holdings`

- **HTTP:** `GET /sec/institutional-holdings`
- **What:** Institutional holdings (13F-HR). Returns the latest 13F-HR holdings for an institutional manager (by CIK): issuer, value, shares, sorted by value.
- **Params:** `cik` (string, **required**) — Institutional manager CIK; `limit` (integer, optional) — Max holdings, default 50, max 1000

## Web (1)

### `web_scrape`

- **HTTP:** `POST /web/scrape`
- **What:** Scrape a URL into markdown, HTML, links or metadata. Fetches a single public URL and returns clean content in the requested formats (markdown, html, raw_html, links, metadata). The request body IS the ScrapeOption object itself — e.g. {"url": "https://example.com"} — do not wrap it in an extra key. With render=auto the request starts as a fast HTTP fetch and escalates to a real browser when the page is blocked or rendered with JavaScript. only_main_content (default true) strips navigation, headers, footers and other boilerplate before conversion. Only public pages are supported; respect each site's terms of use and robots directives. A handful of popular sites (Amazon, Reddit, Yelp, LinkedIn, and others) already have a dedicated, more reliable endpoint elsewhere in this API — a failed scrape against one of them names it. A Reddit URL that maps onto a dedicated Reddit endpoint (listings, search, comment threads, user and domain pages) is answered by that endpoint instead, and its response is returned as-is in data with an X-Routed-To header; send dedicated=false to always get the scraped page.
- **Params:** `scrapeOption` (object, **required**) — Scrape options
- **REST body:** Send the value of the MCP argument `scrapeOption` directly as the JSON body; do not wrap it in a `scrapeOption` property.
