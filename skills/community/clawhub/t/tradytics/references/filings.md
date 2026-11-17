# Filings

Every SEC filing of the last three years and each new one seconds after EDGAR accepts it, with 10-K, 10-Q and 8-K sections as text and full-text search.

## List filings

`GET /filings` (scope `research`, cursor-paged)

Filings newest first, for the whole market or a few companies, by form, 8-K item and date.

| Param | In | Type | Description |
| --- | --- | --- | --- |
| `symbol` | query | string | Tickers, comma separated, e.g. `AAPL,NVDA`. Default every filer. |
| `form` | query | string | Form types, comma separated, e.g. `10-K,10-Q,8-K`, `4`, `SCHEDULE 13D`. |
| `item` | query | string | 8-K items, comma separated, e.g. `2.02` (results), `5.02` (officers and directors). |
| `from` | query | string | Filed on or after, `YYYY-MM-DD` or an RFC 3339 time. |
| `to` | query | string | Filed on or before. |
| `limit` | query | integer | Rows per page, up to 1000. Default `100`. |
| `cursor` | query | string | `next_cursor` from the previous page. |

| Field | Type | Description |
| --- | --- | --- |
| `accession` | string | Accession number, the filing's id. |
| `symbol` | string | Ticker of the company it is about, null for a filer without one. |
| `cik` | integer | SEC CIK of that company. |
| `company` | string | Name as filed. |
| `form` | string | Form type, e.g. `10-K`, `8-K/A`. |
| `filed_at` | string | When EDGAR accepted it, UTC. |
| `period_of_report` | string | Period it covers, `YYYY-MM-DD`. |
| `items` | array | 8-K items, e.g. `["2.02", "9.01"]`. |
| `description` | string | What it is: the form, or an 8-K's items in words. |
| `url` | string | The filing on EDGAR. |
| `document_url` | string | Its main document. |

Request: `GET https://tradytics.com/api/public/v1/filings?symbol=AAPL&form=10-K%2C10-Q%2C8-K&apiKey=YOUR_API_KEY`

## Search filings

`GET /filings/search` (scope `research`, cursor-paged)

Full-text search of every filing and exhibit since 2001: the documents that match.

| Param | In | Type | Description |
| --- | --- | --- | --- |
| `q` | query | string | Words, or an exact phrase in quotes; `AND`, `OR`, `NOT`, e.g. `"supply agreement" AND China`. Required. |
| `symbol` | query | string | Tickers, comma separated, e.g. `AAPL,NVDA`. Default every filer. |
| `form` | query | string | Form types, comma separated, e.g. `10-K,10-Q,8-K`, `4`, `SCHEDULE 13D`. |
| `from` | query | string | Filed on or after, `YYYY-MM-DD`. |
| `to` | query | string | Filed on or before, `YYYY-MM-DD`. |
| `limit` | query | integer | Rows per page, up to 100. Default `100`. |
| `cursor` | query | string | `next_cursor` from the previous page. |

| Field | Type | Description |
| --- | --- | --- |
| `accession, symbol, cik, company, form` | mixed | The filing, as in List filings. |
| `filed_date` | string | Filing date, `YYYY-MM-DD`. |
| `document_type` | string | The matching document, e.g. `8-K`, `EX-99.1`. |
| `description` | string | Its description as filed. |
| `url` | string | The matching document. |
| `filing_url` | string | The filing on EDGAR. |

Request: `GET https://tradytics.com/api/public/v1/filings/search?q=%22supply%20agreement%22%20AND%20China&form=8-K&apiKey=YOUR_API_KEY`

## Filing

`GET /filings/{accession}` (scope `research`)

One filing with every document and exhibit in it.

| Param | In | Type | Description |
| --- | --- | --- | --- |
| `accession` | path | string | Accession number, e.g. `0000320193-25-000079`. Required. |

| Field | Type | Description |
| --- | --- | --- |
| `accession` | string | Accession number, the filing's id. |
| `symbol` | string | Ticker of the company it is about, null for a filer without one. |
| `cik` | integer | SEC CIK of that company. |
| `company` | string | Name as filed. |
| `form` | string | Form type, e.g. `10-K`, `8-K/A`. |
| `filed_at` | string | When EDGAR accepted it, UTC. |
| `period_of_report` | string | Period it covers, `YYYY-MM-DD`. |
| `items` | array | 8-K items, e.g. `["2.02", "9.01"]`. |
| `description` | string | What it is: the form, or an 8-K's items in words. |
| `url` | string | The filing on EDGAR. |
| `document_url` | string | Its main document. |
| `documents[]` | array | `sequence`, `type` (e.g. `10-K`, `EX-99.1`, `EX-101.INS`), `description`, `url`, and `size_bytes` when available. |

Request: `GET https://tradytics.com/api/public/v1/filings/0000320193-25-000079?apiKey=YOUR_API_KEY`

## Filing sections

`GET /filings/{accession}/sections` (scope `research`)

Sections of a 10-K, 10-Q or 8-K as plain text. A section asked for the first time can answer `warming_up` for a few seconds.

| Param | In | Type | Description |
| --- | --- | --- | --- |
| `accession` | path | string | Accession number, e.g. `0000320193-25-000079`. Required. |
| `section` | query | string | Comma separated. 10-K and 10-Q: `business`, `risk_factors`, `mda`, `market_risk`, `financial_statements`, `legal_proceedings`, `controls`, `cybersecurity`, `properties`, `market_for_equity`, `other_information`, `exhibits` and the other items by name. 8-K: items like `2.02`. Default business, risk factors and MD&A of a 10-K, MD&A and risk factors of a 10-Q, the items of an 8-K. |

| Field | Type | Description |
| --- | --- | --- |
| `section` | string | Its name, e.g. `risk_factors` or `2.02`. |
| `title` | string | Its heading, e.g. `Risk factors`. |
| `text` | string | The section's text. |

Request: `GET https://tradytics.com/api/public/v1/filings/0000320193-25-000079/sections?section=risk_factors&apiKey=YOUR_API_KEY`
