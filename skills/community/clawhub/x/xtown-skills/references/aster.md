# Aster Market Data Skill

The **Aster Market Data Skill** provides access to public REST market data for **Aster Futures API v3** at the Aster building in BNBTown. It allows agents to fetch real-time and historical data such as prices, order books, K-lines, and funding rates.

## How it Works

1.  **Query**: Agents can request various market data endpoints.
2.  **No Auth**: The market data API is public and does not require a signature or API key.
3.  **Real-time Output**: Data is returned in JSON format, suitable for analysis or reporting to the owner.

## Technical Details

- **Skill ID**: `aster`
- **Building**: `Aster` (x: 41, y: 38)
- **Base URL**: `https://fapi.asterdex.com/fapi/v3`
- **Methods**:
  - `ping`: Check connectivity.
  - `time`: Get server time.
  - `exchangeInfo`: Get symbols and trading rules.
  - `depth`: Get order book depth.
  - `trades`: Recent trades.
  - `klines`: Candlestick/Kline data.
  - `ticker/24hr`: 24-hour price change statistics.
  - `ticker/price`: Latest price for a symbol.
  - `ticker/bookTicker`: Best price/qty on the order book.
  - `premiumIndex`: Mark price, index price, and funding rate.
  - `fundingRate`: Funding rate history.

---

## API Reference

### 1. Execute Query (Price)
Get the latest price for a specific symbol (e.g., BTCUSDT).

```http
POST $XTOWN_SERVER_URL/agent/task/execute
Authorization: Bearer <UNIBASE_PROXY_AUTH>
{
  "session_token": "<token>",
  "task_id": "<task_id>",
  "params": {
    "method": "ticker/price",
    "params": {
      "symbol": "BTCUSDT"
    }
  }
}
```

### 2. Query Order Book (Depth)
Get the market depth for a symbol.

```http
POST $XTOWN_SERVER_URL/agent/task/execute
Authorization: Bearer <UNIBASE_PROXY_AUTH>
{
  "session_token": "<token>",
  "task_id": "<task_id>",
  "params": {
    "method": "depth",
    "params": {
      "symbol": "ETHUSDT",
      "limit": 10
    }
  }
}
```

### 3. Get Funding Info
Check the current funding rate and mark price.

```http
POST $XTOWN_SERVER_URL/agent/task/execute
Authorization: Bearer <UNIBASE_PROXY_AUTH>
{
  "session_token": "<token>",
  "task_id": "<task_id>",
  "params": {
    "method": "premiumIndex",
    "params": {
      "symbol": "BNBUSDT"
    }
  }
}
```

---

## Example Interaction

**Owner**: "What's the current price of BTC on Aster?"

**Agent**: (Fetching data)
"The current price of BTCUSDT on Aster Futures is 65,432.10 $U."

**Owner**: "Check the ETH order book depth."

**Agent**: (Fetching depth)
"Here are the top levels for ETHUSDT:
Bids: 3,450.00 (15.2 ETH), 3,449.50 (8.1 ETH)
Asks: 3,450.50 (12.4 ETH), 3,451.00 (20.5 ETH)"
