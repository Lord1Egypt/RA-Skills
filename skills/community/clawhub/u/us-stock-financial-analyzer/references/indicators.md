# Financial Indicators Reference

## Data Source Requirements

Input data must include the following fields per stock:

| Field | Type | Description |
|-------|------|-------------|
| ticker | string | Stock ticker symbol (e.g., AAPL) |
| name | string | Company name |
| sector | string | GICS sector classification |
| index | string | Index membership: `sp500` or `nasdaq` |
| market_cap | number | Market capitalization (USD) |
| pe_ratio | number | Price-to-Earnings ratio (TTM) |
| pb_ratio | number | Price-to-Book ratio |
| roe | number | Return on Equity (decimal, e.g., 0.18 = 18%) |
| debt_to_equity | number | Total Debt / Total Equity |
| revenue_growth | number | YoY revenue growth (decimal) |
| net_margin | number | Net profit margin (decimal) |
| current_ratio | number | Current Assets / Current Liabilities |
| dividend_yield | number | Annual dividend yield (decimal) |

## Scoring Model

### Weight Allocation

| Metric | Weight | Direction |
|--------|--------|-----------|
| ROE | 20% | Higher is better |
| PE Ratio | 15% | Lower is better |
| Debt/Equity | 15% | Lower is better |
| Revenue Growth | 15% | Higher is better |
| Net Margin | 15% | Higher is better |
| PB Ratio | 10% | Lower is better |
| Current Ratio | 5% | Higher is better |
| Dividend Yield | 5% | Higher is better |

### Thresholds

| Metric | Good | Warning |
|--------|------|---------|
| PE Ratio | ≤20 | ≤35 |
| PB Ratio | ≤3 | ≤6 |
| ROE | ≥15% | ≥8% |
| Debt/Equity | ≤0.5 | ≤1.5 |
| Revenue Growth | ≥10% | ≥3% |
| Net Margin | ≥15% | ≥5% |
| Current Ratio | ≥2.0 | ≥1.0 |
| Dividend Yield | ≥2% | ≥0.5% |

### Scoring Logic

- Score 100: metric meets "good" threshold
- Score 40–100: metric between "warn" and "good" (linear interpolation)
- Score 0–40: metric beyond "warn" (linear decay)
- Overall score = weighted sum, normalized to 0–100

## Red Flag Detection

A stock is flagged when:
- PE ratio > 35
- Debt/Equity > 1.5
- ROE < 8% (but positive)
- Revenue growth is negative
- Current ratio < 1.0

Stocks with ≥3 red flags are classified as **high-risk**.

## Recommended Data Sources

- SEC EDGAR (free, authoritative): https://www.sec.gov/cgi-bin/browse-edgar
- Yahoo Finance API (via yfinance Python package)
- Financial Modeling Prep API: https://financialmodelingprep.com/
- Alpha Vantage: https://www.alphavantage.co/
- SEC XBRL filings for structured data extraction

## Feishu Permission Model

When sharing analysis reports via Feishu (Lark):

| Role | Permission | Scope |
|------|-----------|-------|
| Analyst | Edit | Own reports |
| Portfolio Manager | Edit + Share | All reports |
| Compliance | View + Comment | All reports |
| Executive | View | Summary reports only |
| External | No access | — |

### Minimum Access Principle

1. Reports default to **owner-only** access
2. Share with specific individuals, not groups, unless a distribution list is approved
3. Grant `view` first; escalate to `edit` only on request with justification
4. Revoke access when project/engagement ends
5. Never grant `share` permission to external users
6. Use Feishu document link type: **organization-internal** by default
7. For cross-org sharing: use `link_share` with `allow_share_disabled` and set expiry
