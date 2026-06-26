# sector-rotation-analyst

> Track which sectors lead and lag the S&P 500, map the economic cycle phase, and get overweight/underweight recommendations — powered by [Finskills API](https://finskills.net).

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)]()
[![Plan](https://img.shields.io/badge/API%20Plan-Pro-orange.svg)](https://finskills.net/register)
[![Category](https://img.shields.io/badge/category-sector--rotation-purple.svg)]()

---

## What This Skill Does

1. Fetches all 11 GICS sector ETF performances (1D/1W/1M/3M/YTD)
2. Ranks sectors by absolute and relative (vs SPY) performance
3. Maps performance to the economic cycle phase (Early Recovery → Contraction)
4. Expands the top 3 sectors with ETF holdings and catalysts
5. Outputs OW/N/UW tactical sector recommendations

## Install

```bash
npx skills add https://github.com/finskills/sector-rotation-analyst --skill sector-rotation-analyst
```

## Quick Start

```
You: Which sectors are outperforming the market right now?
Claude: [Fetches sector data, ranks all 11 sectors, outputs rotation report with recommendations]
```

## Example Triggers

- `"Which sectors are leading this month?"`
- `"Where should I rotate into based on the economic cycle?"`
- `"What are the top holdings in the energy sector ETF?"`
- `"Is the market in an early recovery or late expansion phase?"`
- `"Show me sector performance vs the S&P 500"`

## API Endpoints Used

| Endpoint | Plan | Data |
|----------|------|------|
| `GET /v1/market/sectors` | Pro | All 11 sector performances |
| `GET /v1/free/etf/holdings/{etf}` | Free | Top stocks in each sector ETF |
| `GET /v1/free/index/SP500/constituents` | Free | S&P 500 sector weights |
| `GET /v1/market/summary` | Pro | Benchmark comparison |

## Requirements

- **Finskills API Key**: [Register at finskills.net](https://finskills.net) (free tier available) — Pro plan for sector and market summary data

## License

MIT — see [LICENSE](../LICENSE)
