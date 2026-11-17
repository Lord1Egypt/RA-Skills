---
name: quiver-quant
description: Query alternative financial data from Quiver Quantitative — Congress trading, corporate lobbying, government contracts, insider transactions. Use when tracking politician stock trades, company lobbying spend, or unusual market signals from D.C. Requires QUIVER_API_KEY environment variable.
license: MIT
---
# Quiver Quantitative

Access alternative data from quiverquant.com to track non-traditional market signals.

## Setup
Set your API key: `export QUIVER_API_KEY=your_key`

## Usage

### Congress Trading
Track trades by Senators and Representatives.
```
python scripts/query_quiver.py congress
python scripts/query_quiver.py congress --ticker NVDA
python scripts/query_quiver.py congress --politician "Nancy Pelosi"
```

### Corporate Lobbying
```
python scripts/query_quiver.py lobbying AAPL
```

### Government Contracts
```
python scripts/query_quiver.py contracts LMT
```

### Insider Trading
```
python scripts/query_quiver.py insiders TSLA
```

All output is JSON. Pipe through jq for filtering.