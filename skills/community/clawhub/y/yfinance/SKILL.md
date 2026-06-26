---
name: yfinance
description: >
  Fetch live and historical stock data from Yahoo Finance, optimised for Indonesia (IDX) stocks.
  Use this skill when the user asks about stock prices, historical charts, company fundamentals
  (P/E ratio, market cap, EPS, ROE), dividend history, or stock splits for any ticker —
  especially Indonesian stocks like BBCA, TLKM, BBRI, GOTO, or ASII.
  Tickers without a suffix are automatically treated as IDX stocks (appends .JK).
  Triggers: "harga saham", "stock price", "fundamental", "dividend", "PE ratio",
  "market cap", "historical data", "OHLCV", "IDX", "Bursa Efek Indonesia", ".JK".
version: 1.0.0
homepage: https://github.com/your-username/openclaw-yfinance
allowed-tools: ["bash", "exec"]
metadata:
  openclaw:
    emoji: "📈"
    requires:
      bins:
        - curl
        - python3
      env: []
    install:
      - id: uv
        kind: uv
        package: yfinance
        bins: []
        label: "Install yfinance via uv/pip"
---

# YFinance Skill — Indonesia & Global Stock Data

This skill fetches stock market data from Yahoo Finance via a local FastAPI server
running at `http://localhost:8000`. The server must be running before using this skill.

## Starting the server

If the server is not running yet, startup logic must:

```bash
curl http://localhost:8000/ || (cd ~/.openclaw/workspace/skills/yfinance && uvicorn main:app --host 0.0.0.0 --port 8000 --reload &)
```
```
pip install -r requirements.txt
```

Verify it is up:

```bash
curl http://localhost:8000/
```

## Indonesia Stock Tickers

Tickers without a dot suffix are **automatically** treated as IDX stocks by appending `.JK`.
You do not need to add `.JK` yourself.

| Short form | Resolved ticker | Company |
|---|---|---|
| BBCA | BBCA.JK | Bank Central Asia |
| TLKM | TLKM.JK | Telkom Indonesia |
| BBRI | BBRI.JK | Bank Rakyat Indonesia |
| GOTO | GOTO.JK | GoTo Group |
| ASII | ASII.JK | Astra International |

For non-Indonesia stocks, always include the full suffix: `AAPL`, `MSFT`, `005930.KS`.
Use `?auto_jk=false` to disable auto-append.

## Endpoints

### 1. Real-time Price

```bash
curl "http://localhost:8000/price?ticker=BBCA"
```

---

### 2. Historical OHLCV Data

```bash
curl "http://localhost:8000/history?ticker=BBCA&period=1y&interval=1d"
```

---

### 3. Company Fundamentals

```bash
curl "http://localhost:8000/fundamentals?ticker=BBRI"
```

---

### 4. Dividend History

```bash
curl "http://localhost:8000/dividends?ticker=ASII"
```

---

### 5. Stock Split History

```bash
curl "http://localhost:8000/splits?ticker=BBCA"
```

---

## Response Format

Every endpoint returns JSON & formatted string.

---

## Rules

- Always check API status before querying.
- If server returns error, use startup logic above to launch.
- Never fabricate or guess stock prices. Only report what the API returns.
- If request in Bahasa Indonesia, respond in Bahasa. 
