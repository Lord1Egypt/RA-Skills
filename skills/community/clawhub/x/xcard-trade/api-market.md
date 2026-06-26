# Module: Market Data

**When to load this file:** User asks about prices, order book depth, candlesticks, funding rates, or open interest.

Trigger phrases: "price", "quote", "orderbook", "candle", "funding", "open interest", "index price", "mark price", "价格", "行情", "报价", "K线", "资金费率"

---

## GET /market/symbols

Returns the full list of tradable perpetual contracts.

**Request**
```
GET /market/symbols
X-API-KEY: {XCARD_TRADE_API_KEY}
```

**Query params**

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| status | string | No | Filter by `active` / `suspended`. Default: `active` |

**Response**
```json
{
  "symbols": [
    {
      "symbol": "BTC/USDT",
      "base_currency": "BTC",
      "quote_currency": "USDT",
      "index_price": 68185.00,
      "mark_price": 68200.00,
      "last_price": 68250.00,
      "funding_rate": 0.0001,
      "next_funding_time": "2025-03-25T16:00:00Z",
      "max_leverage": 125,
      "status": "active"
    }
  ]
}
```

---

## GET /market/{symbol}/quote

Returns the latest price quote for a specific perpetual contract.

**Request**
```
GET /market/BTC-USDT/quote
X-API-KEY: {XCARD_TRADE_API_KEY}
```

> Note: symbol uses hyphen `BTC-USDT` in URL paths.

**Response**
```json
{
  "symbol": "BTC/USDT",
  "last_price": 68250.00,
  "mark_price": 68200.00,
  "index_price": 68185.00,
  "bid": 68248.00,
  "ask": 68252.00,
  "bid_iv": null,
  "ask_iv": null,
  "funding_rate": 0.0001,
  "next_funding_time": "2025-03-25T16:00:00Z",
  "open_interest": 1250000000.00,
  "volume_24h": 8500000000.00,
  "timestamp": "2025-03-25T10:30:00Z"
}
```

> Always display `timestamp` so the user knows how fresh the data is.
> Show `funding_rate` as a percentage (multiply by 100 for display).

---

## GET /market/{symbol}/orderbook

Returns the current bid/ask order book for a perpetual contract.

**Request**
```
GET /market/BTC-USDT/orderbook
X-API-KEY: {XCARD_TRADE_API_KEY}
```

**Query params**

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| depth | integer | No | Number of price levels per side. Default: `10`, max: `50` |

**Response**
```json
{
  "symbol": "BTC/USDT",
  "bids": [
    { "price": 68248.00, "size": 12.5 },
    { "price": 68245.00, "size": 8.2 }
  ],
  "asks": [
    { "price": 68252.00, "size": 15.3 },
    { "price": 68255.00, "size": 6.7 }
  ],
  "timestamp": "2025-03-25T10:30:00Z"
}
```

---

## GET /market/{symbol}/candles

Returns OHLCV candlestick data for charting or trend analysis.

**Request**
```
GET /market/BTC-USDT/candles
X-API-KEY: {XCARD_TRADE_API_KEY}
```

**Query params**

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| interval | string | Yes | `1m`, `5m`, `15m`, `1h`, `4h`, `1d`, `1w` |
| limit | integer | No | Number of candles. Default: `100`, max: `1000` |

**Response**
```json
{
  "symbol": "BTC/USDT",
  "interval": "1h",
  "candles": [
    {
      "time": "2025-03-25T09:00:00Z",
      "open": 67800.00,
      "high": 68500.00,
      "low": 67650.00,
      "close": 68250.00,
      "volume": 125680.5
    }
  ]
}
```

---

## GET /market/funding-rates

Returns current funding rates for all or filtered symbols.

**Request**
```
GET /market/funding-rates
X-API-KEY: {XCARD_TRADE_API_KEY}
```

**Query params**

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| symbol | string | No | Filter by symbol, e.g. `BTC/USDT` |

**Response**
```json
{
  "funding_rates": [
    {
      "symbol": "BTC/USDT",
      "funding_rate": 0.0001,
      "funding_rate_pct": 0.01,
      "next_funding_time": "2025-03-25T16:00:00Z",
      "mark_price": 68200.00
    }
  ]
}
```

> Display `funding_rate_pct` (e.g. `0.01%`) rather than the raw decimal.
> Funding is settled every 8 hours at `next_funding_time`. Remind users of this for swing trades.
