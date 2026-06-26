# value-dividend-screener

> Screen US stocks for undervaluation and sustainable dividend income using a multi-factor framework: value (P/E, P/B, EV/EBITDA), dividend quality (yield, FCF payout, 5Y CAGR), and financial health (D/E, FCF, liquidity) — powered by [Finskills API](https://finskills.net).

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)]()
[![Plan](https://img.shields.io/badge/API%20Plan-Pro-orange.svg)](https://finskills.net/register)
[![Category](https://img.shields.io/badge/category-screening-green.svg)]()

---

## What This Skill Does

1. Accepts a stock universe (default: S&P 500 constituents) or user-provided ticker list
2. Fetches fundamentals, dividend history, and current valuation per stock
3. Screens against value, income quality, and financial health criteria (30+ metrics)
4. Computes a 0–100 composite score with Value / Income / Health breakdown
5. Flags dividend-at-risk stocks (high yield + unsustainable payout)
6. Ranks and presents top 10 qualified stocks with full rationale

## Install

```bash
npx skills add https://github.com/finskills/value-dividend-screener --skill value-dividend-screener
```

## Quick Start

```
You: Screen the S&P 500 for undervalued high-quality dividend stocks
Claude: [Fetches constituent list, screens fundamentals + dividends, scores 500 stocks, returns top 10]
```

## Example Triggers

- `"Find me undervalued dividend stocks in the S&P 500"`
- `"Screen for stocks with P/E under 15 and yield over 3%"`
- `"Which of these stocks has the safest dividend: JNJ, PG, KO, MO?"`
- `"Build me a dividend growth watchlist from healthcare and consumer staples"`
- `"Check dividend sustainability for my portfolio holdings"`

## Screening Criteria

| Category | Key Thresholds |
|----------|----------------|
| **Value** | P/E < 20, P/B < 2.5, EV/EBITDA < 12, P/FCF < 18 |
| **Income** | Yield ≥ 2.5%, FCF payout < 75%, 5Y div CAGR > 3% |
| **Health** | D/E < 1.5, current ratio > 1.0, positive FCF |

## API Endpoints Used

| Endpoint | Plan | Data |
|----------|------|------|
| `GET /v1/free/index/SP500/constituents` | Free | Screening universe |
| `GET /v1/stocks/financials/{symbol}` | Pro | Income stmt, balance sheet, FCF |
| `GET /v1/stocks/dividends/{symbol}` | Pro | Dividend history + yield |
| `GET /v1/stocks/quote/{symbol}` | Pro | Price, P/E, P/B, EV/EBITDA |
| `GET /v1/free/stocks/estimates/{symbol}` | Free | Forward EPS, analyst count |
| `GET /v1/stocks/recommendations/{symbol}` | Pro | Analyst rating + price target |

## Requirements

- **Finskills API Key**: [Register at finskills.net](https://finskills.net) (free tier available) — **Pro plan required** for financials and dividends
- **Claude** with skill support

## License

MIT — see [LICENSE](../LICENSE)
