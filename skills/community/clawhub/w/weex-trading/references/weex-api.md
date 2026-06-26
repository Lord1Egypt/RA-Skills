# Weex V3 API Reference

Base URL: `https://api-spot.weex.com`

Weex uses a Binance-compatible REST API. Auth uses HMAC-SHA256 signatures.

## Authentication

All authenticated requests require these headers:

| Header | Description |
|--------|-------------|
| `ACCESS-KEY` | Your API key |
| `ACCESS-SIGN` | HMAC-SHA256 signature (base64) |
| `ACCESS-TIMESTAMP` | Current time in milliseconds |
| `ACCESS-PASSPHRASE` | Your passphrase (if set) |
| `Content-Type` | `application/json` |

### Signature Construction

```
prehash = timestamp + METHOD + path [+ "?" + queryString] + body
signature = base64(HMAC-SHA256(apiSecret, prehash))
```

- Timestamp is milliseconds (not seconds)
- Include `?` before queryString only when queryString is non-empty
- Body is empty string for GET/DELETE requests

## Public Endpoints (No Auth)

### GET /api/v3/ping
Test connectivity. Returns `{}`.

### GET /api/v3/time
Server time. Returns `{ "serverTime": 1234567890123 }`.

### GET /api/v3/market/ticker/price
Get latest price for a symbol or all symbols.
- `?symbol=BTCUSDT` — single symbol
- No params — all symbols

Returns: `{ "symbol": "BTCUSDT", "price": "68920.50" }`

### GET /api/v3/market/ticker/24hr
24-hour ticker stats.
- `?symbol=BTCUSDT`

Returns: `{ "symbol", "lastPrice", "highPrice", "lowPrice", "quoteVolume", "priceChangePercent", ... }`

### GET /api/v3/market/depth
Order book.
- `?symbol=BTCUSDT&limit=5` (limit: 5, 10, 20, 50, 100, 500, 1000)

### GET /api/v3/market/trades
Recent trades.
- `?symbol=BTCUSDT&limit=100`

### GET /api/v3/market/klines
Candlestick data.
- `?symbol=BTCUSDT&interval=1h&limit=100`
- Intervals: `1min`, `5min`, `15min`, `30min`, `1h`, `4h`, `12h`, `1day`, `1week`

### GET /api/v3/exchangeInfo
All symbols and trading rules.

### GET /api/v3/currencies
All supported currencies.

## Authenticated Endpoints

### GET /api/v3/account
Full account info including all balances.

Returns: `{ "balances": [{ "asset": "BTC", "free": "0.5", "locked": "0.1" }, ...] }`

### POST /api/v3/order
Place a new order.

Body:
```json
{
  "symbol": "BTCUSDT",
  "side": "BUY",
  "type": "MARKET",
  "quantity": "0.001"
}
```

For limit orders, add `price` and `timeInForce: "GTC"`.

### GET /api/v3/order
Get specific order. `?symbol=BTCUSDT&orderId=123`

### DELETE /api/v3/order
Cancel order. `?symbol=BTCUSDT&orderId=123`

### GET /api/v3/openOrders
Get open orders. Optional: `?symbol=BTCUSDT`

### DELETE /api/v3/openOrders
Cancel all open orders for a symbol. `?symbol=BTCUSDT`

### GET /api/v3/allOrders
Order history. `?symbol=BTCUSDT&limit=50`

### GET /api/v3/myTrades
Trade fills. `?symbol=BTCUSDT&limit=50`

## Response Format

Responses may come in two formats:

1. **Direct:** `{ "symbol": "BTCUSDT", "price": "68920" }`
2. **Wrapped:** `{ "code": "00000", "msg": "success", "data": { ... } }`

Success code is `"00000"`. Any other code indicates an error.

## Rate Limits

Standard exchange rate limits apply. HTTP 429 = rate limited.

## Symbol Format

V3 uses plain symbols: `BTCUSDT`, `ETHUSDT`, `SOLUSDT` (no `_SPBL` suffix from V1).

To convert a coin name to a symbol: append `USDT` if not already present.
- `BTC` → `BTCUSDT`
- `ETHUSDT` → `ETHUSDT` (unchanged)
