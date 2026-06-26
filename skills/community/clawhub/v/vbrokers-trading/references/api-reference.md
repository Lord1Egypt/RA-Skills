# VBrokers OpenAPI Reference

> Source: https://quant-open.hstong.com/api-docs
> Gateway: http://127.0.0.1:11111
> All requests: POST, Content-Type: application/json
> All request bodies: `{"timeout_sec": 10, "params": {...}}`

## Table of Contents
1. [Authentication](#authentication)
2. [Account & Funds](#account--funds)
3. [Positions](#positions)
4. [Orders](#orders)
5. [Quotes (HTTP)](#quotes-http)
6. [K-Lines](#k-lines)
7. [Error Codes](#error-codes)

---

## Authentication

### Trade Login
```
POST /trade/TradeLogin
params: {"password": "<AES-ECB-base64-encrypted-password>"}
```
**Must call after Gateway restart.** Password encrypted with AES-ECB/PKCS5, key is base64-decoded 24-byte key.

### Trade Logout
```
POST /trade/TradeLogout
params: {}
```

---

## Account & Funds

### Query Margin Fund Info
```
POST /trade/TradeQueryMarginFundInfo
params: {"exchangeType": "P"}  // P=US, K=HK, v=深股通, t=沪股通
```
Key response fields:
- `assetBalance` — total assets
- `marketValue` — position market value
- `buyPower` — buying power (margin)
- `enableBalance` — available cash (can be negative if using margin)
- `accountStatus` — account status

---

## Positions

### Query Holdings
```
POST /trade/TradeQueryHoldsList
params: {"exchangeType": "P"}
```
⚠️ `exchangeType` is required — omitting causes error 2001.

Key response fields per position:
- `stockCode`, `stockName`
- `currentAmount` — total shares held
- `enableAmount` — shares available to sell
- `costPrice` — average cost
- `keepCostPrice` — maintained cost
- `lastPrice` — last price (may be stale outside trading hours)
- `incomeBalance` — unrealized P&L
- `marketValue` — position market value

---

## Orders

### Place Order
```
POST /trade/TradeEntrust
params:
  exchangeType: "P" | "K"
  stockCode: "AAPL"
  entrustAmount: "1"        // string, not integer
  entrustPrice: "180.00"    // string; use "0" for market orders
  entrustBs: "1"            // "1"=buy, "2"=sell
  entrustType: "3"          // "3"=limit, "5"=market (US only)
  sessionType: "1"          // "0"=regular, "1"=extended (pre/post market)
```
Returns: `entrustId` (order ID for cancellation)

### Cancel Order
```
POST /trade/TradeCancelEntrust
params:
  exchangeType: "P"
  stockCode: "AAPL"
  entrustId: "<order-id>"
  entrustAmount: "1"    // optional
  entrustPrice: "180.00"  // optional
```

### Cancel All Orders
```
POST /trade/TradeBatchCancelEntrust
params: {"exchangeType": "P"}
```

### Query Today's Orders
```
POST /trade/TradeQueryRealEntrustList
params:
  exchangeType: "P"
  queryCount: 20
  queryParamStr: "0"   // required, use "0"
```

### Query Today's Fills
```
POST /trade/TradeQueryRealDeliverList
params:
  exchangeType: "P"
  queryCount: 20
  queryParamStr: "0"
```

---

## Quotes (HTTP)

### Real-Time Quote (BasicQot)
```
POST /hq/BasicQot
params:
  security: [{"dataType": 20000, "code": "AAPL"}]
  needDelayFlag: "0"
  mktTmType: -1   // optional: -1=pre, 1=regular, -2=after, -3=night
```

dataType values:
- `20000` — US stocks
- `10000` — HK stocks
- `30000` — A shares

⚠️ Without `mktTmType`, returns last close price (not real-time).

Key response fields per quote:
- `lastPrice` — last traded price
- `lastClosePrice` — previous close
- `openPrice`, `highPrice`, `lowPrice`
- `volume`, `turnover`
- `tradeTime` — timestamp of last trade (format: YYYYMMDDHHMMSS)
- `mktTmType` — actual session returned

### Overnight Tradeable List (US)
```
POST /hq/UsOverNightTradeCodes
params: {}
```
Returns list of US stocks available for overnight/extended trading.

---

## K-Lines

### Historical / Real-Time K-Lines
```
POST /hq/KL
params:
  security: {"dataType": 20000, "code": "AAPL"}
  startDate: 20260101    // YYYYMMDD integer
  direction: 0           // 0=left (historical), 1=right (forward)
  exRightFlag: 0         // 0=no adjustment, 1=forward adjust
  cycType: 2             // see below
  limit: 20              // for daily: number of bars; for intraday: number of days
```

cycType values:
- `2` — Daily (日线)
- `5` — 1-minute
- `6` — 5-minute
- `7` — 15-minute
- `8` — 30-minute
- `9` — 60-minute

Key response fields per bar:
- `time`, `openPrice`, `highPrice`, `lowPrice`, `closePrice`
- `volume`, `turnover`

---

## Error Codes

| Code | Meaning |
|------|---------|
| `0000` | Success |
| `2001` | Missing required parameter |
| `2002` | Invalid parameter value |
| `3001` | Not logged in / session expired |
| `3002` | Insufficient buying power |
| `4001` | Market closed |
| `4002` | Order rejected by exchange |

---

## Notes & Gotchas

1. **All numeric params must be strings** in `entrustAmount`, `entrustPrice`, etc.
2. **Market orders** (`entrustType="5"`) only supported for US stocks during extended hours with `sessionType="1"` and `entrustPrice="0"`.
3. **HK stocks** do not support extended session (`sessionType="0"` only).
4. **Login expires** when Gateway restarts — always call `TradeLogin` before trading operations.
5. **`lastPrice` in positions** may be stale outside market hours — use `BasicQot` with explicit `mktTmType` for real-time prices.
