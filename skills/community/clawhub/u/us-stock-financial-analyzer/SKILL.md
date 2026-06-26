---
name: us-stock-financial-analyzer
description: >
  Automated financial indicator analysis for S&P 500 and NASDAQ stocks. Score and rank stocks
  by weighted financial health metrics (PE, PB, ROE, debt/equity, revenue growth, net margin,
  current ratio, dividend yield). Detect red flags and generate sector-level rankings.
  Use when: (1) analyzing stock financial health from CSV/JSON data, (2) comparing stocks across
  S&P 500 or NASDAQ, (3) generating financial screening reports, (4) identifying high-risk stocks
  by red-flag count, (5) ranking sectors by average financial score, (6) configuring Feishu/Lark
  document permissions for financial reports.
---

# US Stock Financial Analyzer

Analyze S&P 500 and NASDAQ stock financial data with weighted scoring, red-flag detection, and sector rankings.

## Quick Start

1. Prepare input data (CSV or JSON) with required fields. See [references/indicators.md](references/indicators.md) for schema.
2. Run analysis:

```bash
python3 scripts/analyze_financials.py data.csv --output markdown --index all
```

3. For JSON output (pipeline integration):

```bash
python3 scripts/analyze_financials.py data.json --format json --output json --index sp500
```

## Input Format

CSV example:
```csv
ticker,name,sector,index,market_cap,pe_ratio,pb_ratio,roe,debt_to_equity,revenue_growth,net_margin,current_ratio,dividend_yield
AAPL,Apple Inc.,Technology,nasdaq,2800000000000,28.5,45.2,0.147,1.76,0.08,0.25,0.93,0.006
```

JSON example:
```json
[{"ticker":"MSFT","name":"Microsoft Corp.","sector":"Technology","index":"sp500","market_cap":2600000000000,"pe_ratio":32,"pb_ratio":11.5,"roe":0.38,"debt_to_equity":0.42,"revenue_growth":0.12,"net_margin":0.34,"current_ratio":1.77,"dividend_yield":0.008}]
```

## Analysis Workflow

1. **Load data** — CSV or JSON, auto-detected by file extension
2. **Filter by index** — `--index sp500|nasdaq|all`
3. **Score each stock** — weighted metrics normalized to 0–100
4. **Detect red flags** — PE>35, D/E>1.5, low ROE, negative growth, current ratio<1
5. **Rank sectors** — average score by GICS sector
6. **Output** — Markdown report or structured JSON

## Scoring Model

8 metrics weighted by financial significance. ROE gets highest weight (20%); dividend yield lowest (5%). See [references/indicators.md](references/indicators.md) for full thresholds and scoring logic.

## Feishu Permission Configuration

When sharing reports via Feishu, apply minimum access:

1. Default to **owner-only** on new documents
2. Share with named individuals (not groups) unless approved
3. Grant `view` first; `edit` only with justification
4. Set `organization-internal` link type by default
5. Disable `allow_share` for external collaborators
6. Set access expiry for cross-org sharing

See [references/indicators.md](references/indicators.md) for the full permission matrix.

## Data Sources

Recommended free sources: SEC EDGAR, Yahoo Finance (yfinance), Financial Modeling Prep, Alpha Vantage. See [references/indicators.md](references/indicators.md) for URLs and details.
