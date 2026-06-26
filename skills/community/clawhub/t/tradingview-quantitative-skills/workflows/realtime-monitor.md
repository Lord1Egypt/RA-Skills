---
description: Real-time Market Monitor Workflow - Get and monitor real-time market quotes
---

# Real-time Market Monitor Workflow

Get and monitor real-time market quotes, including price, bid/ask, volume, and other key data.

## Execution Steps

### Step 1: Determine Monitoring Symbols

Extract list of symbols to monitor from user input:
- Single symbol: Get detailed quote
- Multiple symbols: Batch get quotes (up to 10)

### Step 2: Select Trading Session

Select trading session based on user needs:
- regular: Regular trading hours (default)
- extended: Pre-market and after-hours
- premarket: Pre-market only
- postmarket: After-hours only

### Step 3: Get Real-time Quotes

**Single Symbol**: Call `tradingview_get_quote`

```
Parameter description:
- symbol: Symbol code (required, format EXCHANGE:SYMBOL)
- session: Trading session (optional, default regular)
- fields: Return fields (optional, default all)
```

**Multiple Symbols**: Call `tradingview_get_quote_batch`

```
Parameter description:
- symbols: Symbol array (required, 1-10)
- session: Trading session (optional, default regular)
- fields: Return fields (optional, default all)
```

### Step 4: Parse Quote Data

Extract key information:
- **Price data**: Current price, open, high, low, previous close
- **Change data**: Change %, change amount
- **Trading data**: Volume, turnover
- **Bid/Ask**: Bid price, ask price, bid/ask size
- **Market info**: Exchange, currency, trading status

### Step 5: Generate Quote Report

Output formatted quote report, including:
- Symbol basic information
- Real-time price and change status
- Trading activity analysis
- Bid/ask strength comparison
- Unusual volatility alerts

## Example Conversations

**User**: "Check Apple stock real-time quote"

**Execution**:
1. Call `tradingview_get_quote`, symbol="NASDAQ:AAPL"
2. Return current price, change %, volume, and other data
3. Analyze bid/ask strength, provide brief commentary

---

**User**: "Monitor AAPL, TSLA, NVDA quotes simultaneously"

**Execution**:
1. Call `tradingview_get_quote_batch`, symbols=["NASDAQ:AAPL", "NASDAQ:TSLA", "NASDAQ:NVDA"]
2. Return real-time quote comparison for three stocks
3. Highlight largest change and most active trading

---

**User**: "Check BTCUSDT pre-market quote"

**Execution**:
1. Call `tradingview_get_quote`, symbol="BINANCE:BTCUSDT", session="extended"
2. Return pre-market trading data (if applicable)
3. Compare with regular session price changes
