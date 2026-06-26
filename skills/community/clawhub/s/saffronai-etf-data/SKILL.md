---
name: saffronai-etf-data
description: Fetch Indian ETF tracker data (symbol, lastPrice, iNAV, timestamps) from SaffronAI (saffronai.in) and return it as JSON or filtered rows. Use when the user asks for ETF last price/iNAV for Indian ETFs (NSE symbols like NIFTYBEES, GOLDBEES, SILVERBEES) or wants the full ETF tracker snapshot.
---

# SaffronAI ETF Data

Fetch ETF data from SaffronAI’s public endpoint:

- CSV: `https://www.saffronai.in/api/etf-data` (no auth required; returns `text/csv`)

## Quick commands

### 1) Fetch the full snapshot (JSON)

```bash
python3 {baseDir}/scripts/saffronai_etf.py fetch
```

### 2) Get one symbol (case-insensitive)

```bash
python3 {baseDir}/scripts/saffronai_etf.py get NIFTYBEES
```

### 3) Get multiple symbols

```bash
python3 {baseDir}/scripts/saffronai_etf.py get NIFTYBEES GOLDBEES SILVERBEES
```

### 4) Output as CSV (passthrough)

```bash
python3 {baseDir}/scripts/saffronai_etf.py fetch --format csv
```

## Notes

- The upstream response is CSV; the script converts to JSON for easy downstream use.
- Columns observed: `symbol, companyName, assets, lastPrice, inav, inav_source, lastUpdateTime, timestamp`.
- Treat fields as strings unless you explicitly coerce numbers (some rows may have blanks).
