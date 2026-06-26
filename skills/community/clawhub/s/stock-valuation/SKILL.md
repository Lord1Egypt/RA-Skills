---
name: stock-valuation
description: "Generate comprehensive company valuation reports as polished HTML/PDF. Use when user asks for stock valuation, company analysis, investment thesis, or deep-dive on a ticker. Pipeline: (1) run_pipeline.py collects all quantitative data in parallel, (2) agent does web research for Seeking Alpha, X/Twitter, analyst PTs, revenue composition, catalysts/risks, (3) generate_report.py produces polished light-theme HTML with embedded charts, smart callouts, and detailed valuation framework. NOT for quick price checks, daily watchlist alerts, or real-time trading signals."
---

# Stock Valuation Report Generator v3.0

Generate professional valuation reports with ONE command. The pipeline auto-detects peers, runs all 8 data scripts in parallel, and produces a polished HTML report.

## Quick Start (One Prompt)

```
User: "Generate a valuation report for AAPL"
```

Agent steps:

### Step 1: Run Data Pipeline
```bash
uv run --with yfinance,matplotlib,lxml python3 $SKILL_DIR/scripts/run_pipeline.py TICKER
# Outputs: /tmp/TICKER_data.json
```

Options:
```bash
# Specify peers manually
uv run --with yfinance,matplotlib,lxml python3 $SKILL_DIR/scripts/run_pipeline.py AAPL --peers MSFT GOOG META
```

### Step 2: Qualitative Research (MANDATORY)

Run these searches **in parallel** and collect the results into `/tmp/TICKER_research.json`:

#### 2a. Seeking Alpha Research
```
web_search "{TICKER} seekingalpha analysis 2025 2026"
web_search "seekingalpha {TICKER} strong buy OR turning bullish OR high growth"
```
Extract 3-5 articles: title, date, rating (Strong Buy/Buy/Hold/Sell), one-sentence thesis.

#### 2b. X/Twitter Sentiment
```bash
# If bird CLI available:
bird search '$TICKER' -n 15 --plain
# Otherwise:
web_search "{TICKER} stock twitter sentiment price target"
```
Extract 3-5 notable posts: username, bull/bear stance, key argument, any specific price target.

#### 2c. Analyst Consensus
```
web_search "{TICKER} analyst price target consensus 2026"
```
Extract: consensus rating, average/low/high price targets.

#### 2d. Earnings & Revenue
```
web_search "{TICKER} latest earnings call revenue composition segments"
web_fetch "BEST_EARNINGS_URL" --maxChars 6000
```
Extract: revenue by segment (amount, % of total, YoY growth), geographic breakdown, funded accounts/AUM/key KPIs, management guidance.

#### 2e. Catalysts & Risks
Synthesize from all research above. Aim for 5-7 catalysts and 5-7 risks (with mitigants).

#### Save as Research JSON

Save to `/tmp/TICKER_research.json`:
```json
{
  "sa_articles": [
    {"title": "Article Title", "date": "Dec 2025", "rating": "Strong Buy", "summary": "Key thesis in one sentence"}
  ],
  "twitter_sentiment": [
    {"user": "FinanceGuy", "stance": "Bullish", "summary": "Key argument or price target"}
  ],
  "analyst_consensus": {"rating": "Strong Buy", "avg_pt": 200.0, "low_pt": 150.0, "high_pt": 250.0},
  "catalysts": [
    "Q4 earnings beat could trigger re-rating (reporting Mar 19)",
    "Geographic expansion into new markets reducing concentration risk"
  ],
  "risks": [
    "Regulatory risk in key markets. Mitigant: diversified across 6+ jurisdictions",
    "Trading volume cyclicality. Mitigant: interest income provides stable base"
  ],
  "revenue_composition": [
    {"stream": "Product Sales", "amount": "$50B", "pct": "52%", "trend": "Strong growth", "notes": "Core hardware"}
  ],
  "geographic_data": [
    {"market": "Americas", "new_accounts_pct": "45%", "avg_deposit": "$50K", "highlights": "Largest market"}
  ]
}
```

### Step 3: Generate Report
```bash
uv run python3 $SKILL_DIR/scripts/generate_report.py /tmp/TICKER_data.json --research /tmp/TICKER_research.json
# Outputs: /tmp/TICKER_report.html
```

### Step 4: Convert to PDF & Deliver
```bash
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
  --headless --disable-gpu --print-to-pdf=/tmp/TICKER_report.pdf \
  --no-pdf-header-footer /tmp/TICKER_report.html
```
Deliver the PDF (and optionally HTML) to the user.

## Script Reference

| Script | Deps | Output |
|--------|------|--------|
| `run_pipeline.py TICKER [--peers P1 P2] [--output]` | yfinance,matplotlib,lxml | Merged JSON → file |
| `generate_report.py DATA.json [--output] [--research]` | (none) | HTML report |
| `fetch_fundamentals.py TICKER [PEERS...]` | yfinance | Financials, ratios, peer data |
| `fetch_technicals.py TICKER` | yfinance | SMAs, RSI, MACD, 52W range |
| `fetch_historical_valuation.py TICKER` | yfinance,lxml | 5yr P/E history, percentile |
| `dcf_model.py TICKER [--wacc] [--growth-*]` | yfinance | 10yr DCF bear/base/bull |
| `fetch_insiders.py TICKER` | yfinance | Insider txns + institutional holders |
| `fetch_options.py TICKER` | yfinance | P/C ratio, IV, unusual vol |
| `fetch_earnings_calendar.py TICKER` | yfinance | Next earnings date |
| `generate_charts.py TICKER` | yfinance,matplotlib | 4 PNGs → /tmp/ |
| `detect_peers.py TICKER [--count N]` | yfinance | Auto-detected peers |
| `filter_tweets.py` (stdin) | (none) | Filtered tweet JSON |

## Report Sections

The generated report includes all of these (in order):
1. Header (company name, ticker, date, data sources)
2. Earnings Badge (next earnings date)
3. KPI Cards (price, MCap, P/E, margins — 2 rows of 4)
4. Quarterly Trends (with QoQ growth arrows ↑↑/↑/→/↓)
5. Revenue Composition (segment breakdown table + insight callout)
6. Geographic Expansion (market-by-market table)
7. Technical Analysis (6-panel: RSI, SMAs, MACD, 52W range)
8. Charts (2×2 grid: price+SMA, revenue, margins, PE history)
9. Historical Valuation (5Y PE avg, range, percentile + mean reversion callout)
10. Peer Comparison (full table with highlight row + discount callout)
11. Options Sentiment (4 KPI cards + interpretation)
12. Insider Activity
13. Seeking Alpha Research (bullish/cautious grouping + consensus callout)
14. X/Twitter Sentiment (notable takes + consensus callout)
15. Catalysts (5-7 items, most important first)
16. Risks (5-7 items with mitigants)
17. Valuation Framework (P/E multiples, mean reversion, DCF)
18. Price Target Scenarios (bear/base/bull with math)
19. Investment Thesis (specific, opinionated verdict)
20. Disclaimer
21. Footer

## Rules

- **NEVER** include personal position data, portfolio info, or user-identifiable information
- All scripts work with `uv run --with <deps>` (no pip install needed)
- Charts are embedded as base64 in HTML for portability
- If any data script fails, its section shows gracefully degraded (no broken HTML)
