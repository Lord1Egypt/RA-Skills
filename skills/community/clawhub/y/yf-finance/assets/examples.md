# Worked Examples

Real input/output examples for the most common use cases.
All outputs were captured from `yf-cli 0.2.0`.

---

## 1. Get Current Price and Daily Change for AAPL

**Command**
```bash
yf quote AAPL
```

**Output**
```
┏━━━━━━━━┳━━━━━━━━┳━━━━━━━━┳━━━━━━━━┳━━━━━━━━┳━━━━━━━┳━━━━━━━━┳━━━━━━━━┳━━━━━━━┓
┃        ┃        ┃        ┃        ┃        ┃       ┃        ┃        ┃   Mkt ┃
┃ Symbol ┃  Price ┃ Change ┃  Chg % ┃   Open ┃  High ┃    Low ┃ Volume ┃   Cap ┃
┡━━━━━━━━╇━━━━━━━━╇━━━━━━━━╇━━━━━━━━╇━━━━━━━━╇━━━━━━━╇━━━━━━━━╇━━━━━━━━╇━━━━━━━┩
│ AAPL   │ 269.41 │  -2.09 │ -0.77% │ 271.44 │ 272.8 │ 269.31 │      — │ 3959… │
└────────┴────────┴────────┴────────┴────────┴───────┴────────┴────────┴───────┘
```

**Multiple tickers at once**
```bash
yf quote AAPL MSFT GOOGL
```

---

## 2. Pull 1-Year Weekly OHLCV for TSLA as JSON

**Command**
```bash
yf history TSLA --period 1y --interval 1wk --output json
```

**JSON structure** — keyed by OHLCV field, each containing a date → value map:
```json
{
  "Open":   { "2025-04-21": 230.26, "2025-04-28": 288.98, "..." : "..." },
  "High":   { "2025-04-21": 286.85, "2025-04-28": 294.86, "..." : "..." },
  "Low":    { "2025-04-21": 222.79, "2025-04-28": 270.78, "..." : "..." },
  "Close":  { "2025-04-21": 284.95, "2025-04-28": 287.21, "..." : "..." },
  "Volume": { "2025-04-21": 631033300, "2025-04-28": 603713200, "..." : "..." },
  "Dividends":    { "...": 0.0 },
  "Stock Splits": { "...": 0.0 }
}
```

**Compute the 52-week price range from JSON output**
```bash
yf history TSLA --period 1y --interval 1wk --output json | python3 -c "
import json, sys
data = json.load(sys.stdin)
highs = list(data['High'].values())
lows  = list(data['Low'].values())
print(f'52-week High: {max(highs):.2f}')
print(f'52-week Low:  {min(lows):.2f}')
"
```

---

## 3. Compare Annual Revenue and Net Income for MSFT

**Command**
```bash
yf financials MSFT --output json
```

**Extract and compare the two most recent fiscal years**
```bash
yf financials MSFT --output json | python3 -c "
import json, sys
data = json.load(sys.stdin)
for period in list(data.keys())[:2]:
    rev = data[period].get('TotalRevenue', 0)
    ni  = data[period].get('NetIncome', 0)
    margin = round(ni / rev * 100, 1) if rev else None
    print(f'{period}: Revenue \${rev/1e9:.1f}B  Net Income \${ni/1e9:.1f}B  Margin {margin}%')
"
```

**Output**
```
2025-06-30: Revenue $281.7B  Net Income $101.8B  Margin 36.1%
2024-06-30: Revenue $245.1B  Net Income $88.1B   Margin 36.0%
```

**Other statement types**
```bash
yf financials MSFT --type balance --freq quarterly
yf financials MSFT --type cashflow --freq ttm --output json
```

---

## 4. Retrieve Next Earnings Date for NVDA

**Command**
```bash
yf calendar NVDA
```

**Output**
```
╭──────────── NVDA — Earnings Calendar ────────────╮
│   Dividend Date                 2026-04-01       │
│   Ex-Dividend Date              2026-03-11       │
│   Earnings Date                 2026-05-21       │
│   Earnings High                 1.99             │
│   Earnings Low                  1.69             │
│   Earnings Average              1.7753           │
│   Revenue High                  85,512,000,000   │
│   Revenue Low                   77,896,000,000   │
│   Revenue Average               78,799,090,450   │
╰──────────────────────────────────────────────────╯
```

**As JSON for programmatic use**
```bash
yf calendar NVDA --output json
```

---

## 5. Screen for Large-Cap Value Stocks

**Command**
```bash
yf screen --preset undervalued-large-caps --limit 5
```

**Output**
```
Screener — undervalued-large-caps  (5 results)
┏━━━┳━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━┓
┃ # ┃ Symbol ┃ Name                       ┃  Price ┃  Change ┃  Chg % ┃    Volume ┃ Mkt Cap ┃
┡━━━╇━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━┩
│ 1 │ WF     │ Woori Financial Group Inc. │ 72.765 │ -0.4950 │ -0.68% │    46,993 │  17.73B │
│ 2 │ WES    │ Western Midstream Partners │  40.32 │ -0.3700 │ -0.91% │   277,935 │  16.45B │
│ 3 │ WBS    │ Webster Financial Corp     │  72.94 │ -0.1100 │ -0.15% │   747,342 │  11.76B │
│ 4 │ VIRT   │ Virtu Financial, Inc.      │  49.67 │ -0.8900 │ -1.76% │    90,578 │  10.67B │
│ 5 │ VG     │ Venture Global, Inc.       │ 11.625 │ +0.1750 │ +1.53% │ 3,567,776 │  28.86B │
└───┴────────┴────────────────────────────┴────────┴─────────┴────────┴───────────┴─────────┘
```

**List all available presets**
```bash
yf screen --list
```

---

## 6. Look Up an Unknown Ticker with `yf search`

Use this when the user knows a company name but not its ticker symbol.

**Command**
```bash
yf search "nvidia" --type quotes --limit 3
```

**Output**
```
                        Quotes — "nvidia"
┏━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━┓
┃ Symbol  ┃ Name                            ┃ Type   ┃ Exchange  ┃ Score ┃
┡━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━┩
│ NVDA    │ NVIDIA Corporation              │ EQUITY │ NASDAQ    │ 29944 │
│ NVD.DE  │ NVIDIA Corporation              │ EQUITY │ XETRA     │ 20011 │
│ 3NVD.AS │ Leverage Shares 3x NVIDIA ETP S │ EQUITY │ Amsterdam │ 20004 │
└─────────┴─────────────────────────────────┴────────┴───────────┴───────┘
```

Pick the result with the highest `Score` on the target exchange (NASDAQ/NYSE for US stocks).
Then use the resolved symbol in subsequent commands:

```bash
yf quote NVDA
yf analyst NVDA --type recommendations
```
