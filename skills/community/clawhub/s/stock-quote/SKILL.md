---
name: stock-quote
description: "Fetch real-time stock prices and fundamental data. Use when: (1) User asks for current stock price or quote, (2) Need to update portfolio holdings with latest prices, (3) Check PE ratios, 52-week ranges, or market caps, (4) Daily portfolio valuation updates, (5) Pre-trade price verification. Supports bulk queries for multiple symbols. Default: Stooq (free, no API key)."
---

# Stock Quote Skill

Real-time stock price and fundamental data retrieval skill.

## Quick Start

```bash
# Single stock (uses Stooq - free, no key)
python ~/.openclaw/skills/stock-quote/scripts/quote.py NVDA

# Multiple stocks
python ~/.openclaw/skills/stock-quote/scripts/quote.py NVDA TSLA BABA ORCL

# JSON output (for programmatic use)
python ~/.openclaw/skills/stock-quote/scripts/quote.py NVDA TSLA --json

# Force specific data source
python ~/.openclaw/skills/stock-quote/scripts/quote.py NVDA --source yfinance
python ~/.openclaw/skills/stock-quote/scripts/quote.py NVDA --source stooq
python ~/.openclaw/skills/stock-quote/scripts/quote.py NVDA --source fmp
```

## Output Fields

| Field | Description |
|-------|-------------|
| price | Current market price |
| change | Price change from previous close |
| change_percent | Percentage change |
| previous_close | Previous trading day's close |
| day_high / day_low | Today's trading range |
| volume | Trading volume |
| market_cap | Market capitalization |
| pe_ratio | Trailing P/E ratio |
| week_52_high / week_52_low | 52-week range |
| dividend_yield | Dividend yield (if applicable) |

## Data Sources

| Source | Priority | API Key | Coverage | Notes |
|--------|----------|---------|----------|-------|
| **Stooq** | 1st (auto) | ❌ No | US stocks | Free, delayed EOD prices |
| **yfinance** | 2nd | ❌ No | Global | Rate limited (~2000/day) |
| **FMP** | 3rd | ⚠️ Demo | Global | Limited demo data |
| **Web** | 4th | ❌ No | Yahoo only | HTML scraping |

**Auto mode** (default): Stooq → yfinance → FMP → Web scrape

## Integration Examples

### Update Portfolio Holdings

```python
from skills.stock_quote.scripts.quote import fetch_yfinance_data

# Fetch current prices for all holdings
holdings = ['NVDA', 'TSLA', 'BABA', 'ORCL', 'UNH', 'AAL', 'AMZN']
quotes = fetch_yfinance_data(holdings)

# Calculate current portfolio value
total_value = sum(quote['price'] * shares for symbol, quote in quotes.items() 
                  if 'price' in quote and quote['price'])
```

### Check Trading Rules Compliance

```python
# Check PE ratio rule (PE > 35 blocked)
quote = fetch_yfinance_data(['NVDA'])['NVDA']
if quote.get('pe_ratio', 0) > 35:
    print("⚠️ PE ratio exceeds 35 - rule violation")

# Check 52-week percentile (above 70% blocked)
if quote.get('price') and quote.get('week_52_high') and quote.get('week_52_low'):
    percentile = (quote['price'] - quote['week_52_low']) / \
                 (quote['week_52_high'] - quote['week_52_low'])
    if percentile > 0.70:
        print("⚠️ Price above 70th percentile of 52-week range")
```

### Daily Heartbeat Update

Add to `HEARTBEAT.md`:
```
- Fetch current prices for all holdings (NVDA, TSLA, BABA, ORCL, UNH, AAL, AMZN)
- Update MEMORY.md position table with latest market values
- Check if any position within 5% of stop loss
- Alert if TSLA approaches $385.90 stop loss
```

## Error Handling

- Network failures → Returns error field with message
- Invalid symbol → Returns error: "No data found"
- Market closed → Returns last traded price with timestamp

Always check for 'error' field in results before using price data.

## Dependencies

```bash
# Primary (recommended)
pip install yfinance

# Fallback (if yfinance unavailable)
pip install requests
```

## Usage with Other Skills

- **stock-advisor**: Provides price data for analysis
- **trading-supervisor**: Validates prices against trading rules
- **elite-memory**: Updates portfolio valuations in MEMORY.md

## Example Output

```
📈 NVDA: $176.46 +2.34 (+1.35%)
   市值：$4.32T
   PE: 68.45
   52 周：$108.13 - $185.50 (当前位置：73.2%)

📉 TSLA: $398.68 -5.12 (-1.27%)
   市值：$1.28T
   PE: 95.23
   52 周：$206.50 - $479.86 (当前位置：41.5%)
```
