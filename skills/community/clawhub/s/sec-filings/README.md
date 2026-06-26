# sec-filings (ClawHub skill)

Query SEC filings for any US-listed public company by name, ticker, or CIK — with extracted financials.

Powered by [Lovelace](https://lovelace.ai/).

## Install

```bash
openclaw skills install clawhub:sec-filings
```

## What you get

Every response includes:

- **Financial data** — revenue, net income, total assets, and stockholders' equity extracted from 10-K and 10-Q filings
- **Company profile** — SIC code, state/country of incorporation, fiscal year end, and employee count
- **All major form types** — 10-K, 10-Q, 8-K, Form 4, SC 13D/G, 13F-HR, DEF 14A

## Usage

Ask your bot:

- *"What was Apple's revenue and net income in their last annual report?"*
- *"Compare Amazon and Microsoft's total assets from their latest 10-Ks"*
- *"Show me JPMorgan's last 4 quarterly filings with financials"*
- *"What 8-Ks has Nvidia filed in the last 90 days?"*
- *"Find all insider trades at Meta since January"*
- *"Who are the large passive shareholders of Microsoft?"*

## Changelog

### 1.0.0-beta.4
- **More accurate entity search** — when multiple matching entities are found, the server now automatically retries with the correct one if the top match turns out to be a stub (e.g. a duplicate EDGAR record). The response includes an `alternatives` field listing other close matches so agents can pin to a specific CIK if needed.

### 1.0.0-beta.3
- **Financial data extraction** — annual (10-K) and quarterly (10-Q) filings now include extracted metrics: revenue, net income, total assets, and stockholders' equity.
- **Company profile** — every response includes a `company` object with SIC code, state/country of incorporation, fiscal year end, and employee count.

### 1.0.0-beta.2
- Date range filtering via `after` and `before` query parameters (YYYY-MM-DD, both inclusive).
- Improved entity search: ticker symbols, zero-padded CIKs, and fuzzy company name matching.
- Multi-replica HTTP deployment; 15s search timeout with retry.

### 1.0.0-beta.1
- Initial release. `GET /filings` with `entity`, `form_types`, and `limit` parameters.
- Supported form types: 10-K, 10-Q, 8-K, Form 4, SC 13D/G, 13F-HR, DEF 14A.
- JSON and Markdown (`Accept: text/markdown`) response formats.

---

By using this skill you agree to the [Lovelace AI Terms and Conditions](https://lovelace.ai/terms-and-conditions).
