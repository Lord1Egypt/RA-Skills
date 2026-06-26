# OpenClaw YFinance Connector

A FastAPI REST server that wraps `yfinance` to serve Yahoo Finance stock data,
**optimised for Indonesia (IDX) stocks** with full OpenClaw + ClawHub compatibility.

---

## Features

| Endpoint | Description |
|---|---|
| `GET /price` | Real-time / latest price, change %, day range, volume |
| `GET /history` | Historical OHLCV — daily, weekly, intraday |
| `GET /fundamentals` | P/E, P/B, EPS, Market Cap, ROE, ROA, Debt/Equity, … |
| `GET /dividends` | Full dividend payment history |
| `GET /splits` | Full stock split history |

Every endpoint returns **both** a structured `json` field and a human-readable `formatted` string.

---

## Indonesia Stock Support

Tickers without a dot suffix are **automatically** treated as IDX stocks by
appending `.JK`. You can disable this per-request with `?auto_jk=false`.

```
BBCA   →  BBCA.JK   (BCA)
TLKM   →  TLKM.JK   (Telkom Indonesia)
BBRI   →  BBRI.JK   (BRI)
GOTO   →  GOTO.JK   (GoTo Group)
ASII   →  ASII.JK   (Astra International)
```

For non-Indonesia stocks, pass the full ticker: `AAPL`, `MSFT`, `005930.KS`

---

## File Structure

```
yfinance/
├── SKILL.md          ← OpenClaw skill definition (required for ClawHub)
├── main.py           ← FastAPI server
├── openapi.json      ← OpenClaw connector spec
├── requirements.txt  ← Python dependencies
└── README.md         ← This file
```

---

## Quick Start

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the server

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### 3. Interactive docs

Open `http://localhost:8000/docs` for Swagger UI.

---

## OpenClaw Setup (Skill)

### Install as a local skill

```bash
# Copy the skill folder to your OpenClaw workspace
cp -r ./yfinance ~/.openclaw/workspace/skills/yfinance

# Sync with ClawHub (if logged in)
clawhub sync
```

### Install from ClawHub (once published)

```bash
clawhub install yfinance
```

### Verify skill is loaded

In your OpenClaw Telegram bot, ask:
```
What is the current price of BBCA?
```

---

## OpenClaw Setup (Connector / Tool)

If you prefer to register this as an OpenClaw **connector** via `openapi.json`:

1. Update the server URL in `openapi.json`:
```json
"servers": [
  {
    "url": "http://YOUR_VM_PUBLIC_IP:8000"
  }
]
```

2. Import `openapi.json` in the OpenClaw web UI under **Connectors → Add**

3. Make sure **port 8000** is open in your Azure VM Network Security Group (NSG)

---

## Example Requests

### Current price — BBCA (BCA)
```
GET /price?ticker=BBCA
```

### 1-year daily history — Telkom
```
GET /history?ticker=TLKM&period=1y&interval=1d
```

### Custom date range — GOTO
```
GET /history?ticker=GOTO&start=2024-01-01&end=2024-12-31
```

### Fundamentals — BBRI
```
GET /fundamentals?ticker=BBRI
```

### Dividends — ASII
```
GET /dividends?ticker=ASII
```

### Global stock (no .JK auto-append)
```
GET /price?ticker=AAPL&auto_jk=false
```

---

## Response Shape

Every endpoint returns:

```json
{
  "json": { "ticker": "BBCA.JK", "price": 9500.0, "change_pct": 1.23 },
  "formatted": "─────────────────────────────\n  Bank Central Asia (BBCA.JK)\n  IDR  9,500.00  ▲ +1.23%\n  ..."
}
```

---

## Publishing to ClawHub

```bash
# Login with GitHub account (at least 1 week old)
clawhub login

# Publish the skill
clawhub publish ~/.openclaw/workspace/skills/yfinance \
  --slug yfinance \
  --name "YFinance — Indonesia & Global Stock Data" \
  --version 1.0.0 \
  --tags latest
```

> The `--slug` must be unique across the entire ClawHub registry.

---

## Deployment (Azure VM)

### Run as background process

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 &
curl http://localhost:8000/
```

### Keep alive with systemd

```bash
sudo nano /etc/systemd/system/yfinance.service
```

```ini
[Unit]
Description=YFinance FastAPI Server
After=network.target

[Service]
User=azureuser
WorkingDirectory=/home/azureuser/yfinance-connector
ExecStart=uvicorn main:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable yfinance
sudo systemctl start yfinance
sudo systemctl status yfinance
```

### Run with Docker

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY main.py .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## Troubleshooting

| Problem | Fix |
|---|---|
| `Connection refused` on port 8000 | Start the uvicorn server |
| OpenClaw can't reach the API | Use VM public IP, not `localhost`, in `openapi.json` |
| Ticker returns no data | Verify ticker on finance.yahoo.com |
| Stale/wrong price | Yahoo Finance delays IDX data ~15 minutes |
| `Permission denied` on skill folder | `chmod -R 755 ~/.openclaw/workspace/skills/yfinance` |
| Skill not picked up by OpenClaw | Restart OpenClaw — skills load at session start |

---

## Notes

- Yahoo Finance data is **delayed ~15 minutes** for most markets including IDX.
- Intraday intervals (`1m`, `5m`, etc.) are only available for the last 7–60 days.
- `yfinance` availability depends on Yahoo Finance's servers; rate limiting may apply.
- OpenClaw picks up workspace skills on the **next session** after install.
