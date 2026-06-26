---
name: quantclaw-data
description: "QuantClaw Data — 200+ financial data modules with CLI, REST API, and MCP interfaces. Real-time prices, technicals, options, macro, alt data, AI/ML models, fixed income, commodities, and more. 187 data sources including FRED, Yahoo Finance, SEC EDGAR, Treasury, IMF, ECB, OPEC. Bloomberg Terminal alternative built on free sources."
metadata:
  openclaw:
    requires:
      bins: ["python3"]
    install:
      - id: quantclaw-deps
        kind: shell
        command: "pip install yfinance numpy scipy pandas statsmodels pandas-datareader requests beautifulsoup4"
        label: "Install Python dependencies"
---

# QuantClaw Data — Financial Intelligence Platform

200+ financial data modules. Bloomberg Terminal alternative built on FREE sources.

## Quick Start

```bash
# Clone
git clone https://github.com/yoniassia/quantclaw-data.git
cd quantclaw-data

# Install deps
pip install yfinance numpy scipy pandas statsmodels pandas-datareader requests beautifulsoup4

# Use CLI
python cli.py price AAPL
python cli.py technicals TSLA
python cli.py screener --sector Technology --min-cap 10B
python cli.py monte-carlo SPY --simulations 10000
python cli.py fama-french NVDA
```

## Access Methods

### CLI (210 commands)
```bash
python cli.py <command> [args]
```

### REST API (54 endpoints)
```
GET https://data.quantclaw.org/api/v1/prices?ticker=AAPL
GET https://data.quantclaw.org/api/v1/technicals?ticker=TSLA
GET https://data.quantclaw.org/api/v1/monte-carlo?ticker=SPY
```

### MCP (210 tools)
Add to your MCP config:
```json
{
  "mcpServers": {
    "quantclaw-data": {
      "command": "node",
      "args": ["mcp-server.js"],
      "cwd": "/path/to/quantclaw-data"
    }
  }
}
```

### Web Dashboard
https://data.quantclaw.org

## Categories

| Category | Modules | Examples |
|----------|---------|---------|
| Core Market Data | 20+ | Prices, profiles, screener, technicals |
| Derivatives & Options | 15+ | Options flow, GEX, vol surface, Greeks |
| Quantitative | 25+ | Fama-French, pairs, Monte Carlo, Kalman |
| Fixed Income & Macro | 20+ | Yield curves, CDS, Fed policy, inflation |
| Alternative Data | 20+ | Satellite, dark pool, insider, sentiment |
| Corporate Events | 15+ | Earnings, M&A, buybacks, activist |
| Intelligence & NLP | 15+ | News sentiment, filing analysis, AI earnings |
| Multi-Asset | 15+ | Crypto, FX, commodities, cross-asset |
| Infrastructure | 10+ | Alerts, backtest, reconciliation, export |

## Data Sources (187)
FRED, Yahoo Finance, SEC EDGAR, US Treasury, IMF, ECB, BOJ, PBOC, OECD, Eurostat, EIA, USDA, CFTC, BLS, Census, World Bank, CoinGecko, DeFi Llama, Binance, OPEC, and 167 more.

## Stats
- 140,888 lines of code
- 175 Python modules
- 54 Next.js API routes
- 210 MCP tools
- 187 unique data sources
- 100% free — no API keys required for core features

## License
MIT
