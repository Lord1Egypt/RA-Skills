---
name: sec-filings
description: "Query SEC filings for any public company by name, ticker, or CIK. (Beta)"
version: 1.0.0-beta.4
metadata:
  openclaw:
    requires:
      bins:
        - curl
---

Use `curl` to call the endpoint below. Server runs at `https://labs.lovelace.ai/sec/api`. Every request requires `entity` (company name, ticker, or CIK).

Each response includes a **company profile** (SIC code, state/country of incorporation, fiscal year end) and, for annual (10-K) and quarterly (10-Q) filings, **extracted financial metrics**: revenue, net income, total assets, and stockholders' equity.

## /filings — list SEC filings

```bash
# By company name
curl "https://labs.lovelace.ai/sec/api/filings?entity=Apple&form_types=10-K&limit=4"

# By ticker
curl "https://labs.lovelace.ai/sec/api/filings?entity=NVDA&limit=5"

# By CIK
curl "https://labs.lovelace.ai/sec/api/filings?entity=320193"

# With date range (both bounds inclusive, YYYY-MM-DD)
curl "https://labs.lovelace.ai/sec/api/filings?entity=Microsoft&form_types=10-K,10-Q&after=2023-01-01"
curl "https://labs.lovelace.ai/sec/api/filings?entity=Microsoft&form_types=10-K&after=2020-01-01&before=2022-12-31"

# Markdown output
curl -H "Accept: text/markdown" "https://labs.lovelace.ai/sec/api/filings?entity=Apple&form_types=10-K&limit=3"
```

### Parameters

| Param | Required | Description |
|-------|----------|-------------|
| `entity` | yes | Company name, ticker symbol, or CIK (max 256 chars) |
| `form_types` | no | Comma-separated list. Omit for all supported types. |
| `limit` | no | Max results (default 10, max 50) |
| `after` | no | Inclusive lower bound on filing date, YYYY-MM-DD |
| `before` | no | Inclusive upper bound on filing date, YYYY-MM-DD |

### Valid form types

Use these values in `form_types` to narrow results. Omit to return all types.

| Value | What it is | When to use |
|-------|-----------|-------------|
| `10-K` | Annual Report | Full-year financial results, risk factors, business overview |
| `10-Q` | Quarterly Report | Quarterly financials and updates between annual reports |
| `8-K` | Current Report | Material events: earnings releases, M&A, leadership changes, etc. |
| `4` | Insider Ownership Changes | Trades or grants of shares by officers, directors, or 10%+ holders |
| `SC 13D` | Activist Stake Disclosure | Filed when an investor acquires >5% with intent to influence the company |
| `SC 13G` | Passive Stake Disclosure | Filed when an investor acquires >5% passively (no influence intent) |
| `13F-HR` | Institutional Holdings | Quarterly snapshot of a fund's equity holdings (≥$100M AUM required) |
| `DEF 14A` | Proxy Statement | Shareholder meeting agenda: board elections, exec pay, governance votes |

### Response

JSON object with top-level identity fields, a `company` profile, and a `filings`
array. Results are sorted most-recent first.

#### Top-level fields

| Field | Description |
|-------|-------------|
| `name` | Canonical entity name (e.g. `"Apple Inc."`) |
| `cik` | SEC CIK (e.g. `"0000320193"`) |
| `alternatives` | Other close-match entities found during search (omitted when empty) |

`name` and `cik` are present even when `filings` is empty, letting you confirm
which entity was found.

`alternatives` is a list of objects, each with `name` and `cik`, representing
other entities the server considered as matches. If the results look wrong, retry
with `?entity=<alternative_cik>` to pin directly to a specific entity — CIK
lookups bypass fuzzy matching entirely.

#### `company` fields

| Field | Description |
|-------|-------------|
| `sic_code` | Standard Industrial Classification code |
| `state_of_incorporation` | State or jurisdiction of incorporation |
| `country_of_incorporation` | Country of incorporation |
| `fiscal_year_end` | Fiscal year end date (MMDD, e.g. `0930` = September 30) |
| `employees` | Total full-time equivalent employees |

All `company` fields are omitted when not available in the KG.

#### `filings` fields

| Field | Description |
|-------|-------------|
| `form_type` | Filing type (e.g. `10-K`, `8-K`) |
| `date` | Filing date (YYYY-MM-DD) |
| `accession_number` | SEC accession number |
| `cik` | Company CIK |
| `description` | Human-readable filing description |
| `edgar_url` | Direct link to the filing index on SEC EDGAR |
| `data` | Extracted financial metrics (10-K/10-Q only; `null` for other form types) |

#### `data` fields (10-K and 10-Q only)

| Field | Description |
|-------|-------------|
| `fiscal_year` | Fiscal year the filing covers (e.g. `2024`) |
| `fiscal_period` | Fiscal period (`FY`, `Q1`, `Q2`, `Q3`, `Q4`) |
| `revenue` | Total revenue (USD) |
| `net_income` | Net income / profit (USD) |
| `total_assets` | Total assets (USD) |
| `stockholders_equity` | Stockholders' equity (USD) |

All `data` fields are omitted when not available in the KG.

```json
{
  "name": "Apple Inc.",
  "cik": "0000320193",
  "company": {
    "sic_code": "3571",
    "state_of_incorporation": "CA",
    "fiscal_year_end": "0928"
  },
  "filings": [
    {
      "form_type": "10-K",
      "date": "2024-11-01",
      "accession_number": "0000320193-24-000123",
      "cik": "0000320193",
      "description": "Annual Report (Form 10-K)",
      "edgar_url": "https://www.sec.gov/Archives/edgar/data/320193/000032019324000123/0000320193-24-000123-index.htm",
      "data": {
        "fiscal_year": 2024,
        "fiscal_period": "FY",
        "revenue": 391035000000,
        "net_income": 93736000000,
        "total_assets": 364980000000,
        "stockholders_equity": 56950000000
      }
    }
  ]
}
```

Add `-H "Accept: text/markdown"` for a human-readable markdown response instead of JSON.

## Example prompts

These prompts work well with this skill:

- *"Show me Apple's last 3 annual reports with revenue and net income"*
- *"What was Microsoft's revenue and net income in their most recent quarter?"*
- *"Compare Amazon and Google's total assets from their latest 10-Ks"*
- *"What 8-Ks has Nvidia filed in the last 90 days?"*
- *"Find all insider trades at Meta since January"*
- *"Who are the large passive shareholders of Microsoft? Show me their SC 13G filings"*
- *"Pull Berkshire Hathaway's last two proxy statements"*
- *"Has Amazon made any material event disclosures this quarter?"*

### Errors

| HTTP status | Meaning |
|-------------|---------|
| 400 | Bad request — missing `entity`, invalid `after`/`before` format, or unrecognised `form_types` |
| 404 | Entity not found — try a different name, the ticker symbol, or the CIK |
| 500 | Internal error — retry once; if it persists the server may be unavailable |
| 503 | Server starting up — retry after a few seconds |

---

By using this skill you agree to the [Lovelace AI Terms and Conditions](https://lovelace.ai/terms-and-conditions).
