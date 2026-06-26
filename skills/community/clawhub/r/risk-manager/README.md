# risk-manager

> Quantify and manage portfolio risk with historical volatility, VaR, Beta, correlation, and position sizing — powered by [Finskills API](https://finskills.net).

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)]()
[![Plan](https://img.shields.io/badge/API%20Plan-Pro-orange.svg)](https://finskills.net/register)
[![Category](https://img.shields.io/badge/category-risk-red.svg)]()

---

## What This Skill Does

1. Fetches 1-year daily price history for each portfolio holding
2. Calculates individual and portfolio-level risk: Ann. Volatility, Beta, Sharpe, Max Drawdown, VaR (95%/99%)
3. Builds pairwise correlation matrix — flags concentrated risk
4. Provides position sizing guidance (Fixed % and Kelly Criterion)
5. Recommends hedges (SPY puts, TLT, GLD) based on Beta and market breadth

## Install

```bash
npx skills add https://github.com/finskills/risk-manager --skill risk-manager
```

## Quick Start

```
You: My portfolio: AAPL 50sh, NVDA 20sh, TSLA 30sh. How risky is this?
Claude: [Fetches historical data, computes vol/VaR/Beta/correlation, outputs risk dashboard]

You: I want to buy MSFT at $430 with a stop at $415. My account is $100,000 — how many shares?
Claude: [Applies 1-2% risk rule, outputs position size]
```

## Example Triggers

- `"Risk analysis for my portfolio: AAPL 50sh, TSLA 30sh, MSFT 40sh"`
- `"What's my Max Drawdown risk this year?"`
- `"How many NVDA shares should I buy with a $200 stop?"`
- `"Should I hedge my portfolio right now?"`
- `"Calculate VaR for my holdings"`

## API Endpoints Used

| Endpoint | Plan | Data |
|----------|------|------|
| `GET /v1/stocks/history/{symbol}` | Pro | 1-year daily OHLCV |
| `GET /v1/free/market/breadth` | Free | Advance/decline, market health |
| `GET /v1/free/macro/treasury-rates` | Free | Risk-free rate for Sharpe |
| `GET /v1/free/market/short-volume/{symbol}` | Free | Short interest signal |

## Requirements

- **Finskills API Key**: [Register at finskills.net](https://finskills.net) (free tier available) — Pro plan for historical data
- **Claude** with skill support

## License

MIT — see [LICENSE](../LICENSE)
