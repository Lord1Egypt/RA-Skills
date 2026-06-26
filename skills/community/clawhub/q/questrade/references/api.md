# Questrade API Reference

Official docs: https://www.questrade.com/api/documentation/getting-started

---

## Authentication — OAuth 2.0

Questrade uses OAuth 2.0 with **rotating refresh tokens**.

### Token endpoint

| Environment | URL |
|-------------|-----|
| Production  | `POST https://login.questrade.com/oauth2/token` |
| Practice    | `POST https://practicelogin.questrade.com/oauth2/token` |

**Request** (query string or form body):

```
grant_type=refresh_token&refresh_token=<your_refresh_token>
```

**Response:**

```json
{
  "access_token"  : "<access_token>",
  "token_type"    : "Bearer",
  "expires_in"    : 1800,
  "refresh_token" : "<new_refresh_token>",
  "api_server"    : "https://api01.iq.questrade.com"
}
```

> **Important:** `refresh_token` in the response is a **new** token.
> Always save it to avoid losing access.

All subsequent API calls must:

1. Use the `api_server` URL as the base (it can change between tokens)
2. Include `Authorization: Bearer <access_token>` in the request header

---

## Base URL

```
{api_server}/v1
```

Example: `https://api01.iq.questrade.com/v1`

---

## Account Calls

### GET /v1/time

Returns server time.

**Response:**
```json
{ "time": "2026-03-04T10:00:00.000000-05:00" }
```

---

### GET /v1/accounts

Returns all accounts linked to the token.

**Response:**
```json
{
  "accounts": [
    {
      "type"       : "Margin",
      "number"     : "12345678",
      "status"     : "Active",
      "isPrimary"  : true,
      "isBilling"  : true,
      "clientAccountType": "Individual"
    }
  ]
}
```

Account types: `Cash`, `Margin`, `TFSA`, `RRSP`, `SRRSP`, `LRSP`, `LIRA`, `LIF`, `RRIF`, `PRIF`, `RESP`, `FRESP`

---

### GET /v1/accounts/{id}/positions

Open positions in an account.

> **Note:** The response does not include a currency field per position.
> Currency can be inferred from the symbol suffix: `.TO` / `.VN` / `.CN` = CAD, no suffix = USD.

**Response:**
```json
{
  "positions": [
    {
      "symbol"            : "AAPL",
      "symbolId"          : 8049,
      "openQuantity"      : 10,
      "closedQuantity"    : 0,
      "currentMarketValue": 1950.00,
      "currentPrice"      : 195.00,
      "averageEntryPrice" : 180.00,
      "dayPnl"            : 5.00,
      "closedPnl"         : 0,
      "openPnl"           : 150.00,
      "totalCost"         : 1800.00,
      "isRealTime"        : true,
      "isUnderReorg"      : false
    }
  ]
}
```

---

### GET /v1/accounts/{id}/balances

Account balances in CAD and USD.

**Response:**
```json
{
  "perCurrencyBalances": [
    {
      "currency"        : "CAD",
      "cash"            : 5000.00,
      "marketValue"     : 12000.00,
      "totalEquity"     : 17000.00,
      "buyingPower"     : 5000.00,
      "maintenanceExcess": 5000.00,
      "isRealTime"      : false
    }
  ],
  "combinedBalances": [ ... ],
  "sodPerCurrencyBalances": [ ... ],
  "sodCombinedBalances": [ ... ]
}
```

---

### GET /v1/accounts/{id}/executions

Trade executions. Query params: `startTime`, `endTime` (ISO 8601 with offset).

**Response:**
```json
{
  "executions": [
    {
      "symbol"          : "AAPL",
      "symbolId"        : 8049,
      "quantity"        : 10,
      "side"            : "Buy",
      "price"           : 180.00,
      "id"              : 53817310,
      "orderId"         : 177106005,
      "orderChainId"    : 17710600,
      "exchangeExecId"  : "FQ1306241800030500",
      "timestamp"       : "2026-01-15T09:35:00.000000-05:00",
      "notes"           : "",
      "venue"           : "LAMP",
      "totalCost"       : 1800.00,
      "orderPlacementCommission": 0,
      "commission"      : 4.95,
      "executionFee"    : 0,
      "secFee"          : 0,
      "canadianExecutionFee": 0,
      "parentId"        : 0
    }
  ]
}
```

---

### GET /v1/accounts/{id}/orders

Orders list. Query params: `stateFilter` (Open / Closed / All), `startTime`, `endTime`, `orderId`.

**Response:**
```json
{
  "orders": [
    {
      "id"              : 177106005,
      "symbol"          : "AAPL",
      "symbolId"        : 8049,
      "totalQuantity"   : 10,
      "openQuantity"    : 10,
      "filledQuantity"  : 0,
      "canceledQuantity": 0,
      "side"            : "Buy",
      "orderType"       : "Limit",
      "limitPrice"      : 145.50,
      "stopPrice"       : null,
      "isAllOrNone"     : false,
      "isAnonymous"     : false,
      "icebergQuantity" : null,
      "minQuantity"     : null,
      "avgExecPrice"    : null,
      "lastExecPrice"   : null,
      "source"          : "TradingAPI",
      "timeInForce"     : "Day",
      "gtdDate"         : null,
      "state"           : "Queued",
      "rejectionReason" : "",
      "chainId"         : 17710600,
      "creationTime"    : "2026-03-04T09:00:00.000000-05:00",
      "updateTime"      : "2026-03-04T09:00:00.000000-05:00",
      "notes"           : "",
      "primaryRoute"    : "AUTO",
      "secondaryRoute"  : "",
      "orderRoute"      : "LAMP",
      "venueHoldingOrder": "",
      "comissionCharged": 0,
      "exchangeOrderId" : "Unknown",
      "isSignificantShareHolder": false,
      "isInsider"       : false,
      "isLimitOffsetInDollar": false,
      "userId"          : 3000124,
      "placementCommission": null,
      "legs"            : [],
      "strategyType"    : "SingleLeg",
      "triggerStopPrice": null,
      "orderGroupId"    : 0,
      "orderClass"      : null
    }
  ]
}
```

Order states: `Pending`, `Active`, `Binance`, `Cancelled`, `Executed`, `FilledPartially`, `Expired`,
`Queued`, `Triggered`, `Activated`, `PendingRiskReview`, `ContingentOrder`, `PendingActivation`

> **Note:** `Binance` appears in Questrade's official enumeration list and may refer to
> an internal routing state — treat it as an informational/unknown state if encountered.

---

### GET /v1/accounts/{id}/orders/{orderId}

Single order by ID. Also accepts `?ids=orderId1,orderId2,...` as a query param
for fetching multiple specific orders. Returns same structure as above.

---

### POST /v1/accounts/{id}/orders *(partner access)*

Place a new order.

**Request body:**
```json
{
  "accountNumber"  : "12345678",
  "symbolId"       : 8049,
  "quantity"       : 10,
  "icebergQuantity": 10,
  "limitPrice"     : 145.50,
  "stopPrice"      : null,
  "isAllOrNone"    : false,
  "isAnonymous"    : false,
  "orderType"      : "Limit",
  "timeInForce"    : "Day",
  "action"         : "Buy",
  "primaryRoute"   : "AUTO",
  "secondaryRoute" : "AUTO"
}
```

Order types: `Market`, `Limit`, `Stop`, `StopLimit`, `TrailingStopInPercentage`,
`TrailingStopInDollar`, `TrailingStopLimitInPercentage`, `TrailingStopLimitInDollar`,
`LimitOnOpen`, `LimitOnClose`

Time-in-force values: `Day`, `GoodTillCanceled`, `ImmediateOrCancel`, `FillOrKill`,
`GoodTillExtendedDay`, `WeekToDate`, `MonthToDate`, `Expiry`, `GoodTillDate`

---

### DELETE /v1/accounts/{id}/orders/{orderId} *(partner access)*

Cancel an order. Returns updated order detail.

---

### GET /v1/accounts/{id}/activities

Account activities (deposits, dividends, commissions, trades, etc.).
Query params: `startTime`, `endTime`.

**Response:**
```json
{
  "activities": [
    {
      "tradeDate"         : "2026-01-15T00:00:00.000000-05:00",
      "transactionDate"   : "2026-01-17T00:00:00.000000-05:00",
      "settlementDate"    : "2026-01-17T00:00:00.000000-05:00",
      "action"            : "Buy",
      "symbol"            : "AAPL",
      "symbolId"          : 8049,
      "description"       : "APPLE INC.",
      "currency"          : "USD",
      "quantity"          : 10,
      "price"             : 180.00,
      "grossAmount"       : -1800.00,
      "commission"        : -4.95,
      "netAmount"         : -1804.95,
      "type"              : "Trades"
    }
  ]
}
```

Activity types: `Deposits`, `Dividends`, `Withdrawals`, `Trades`, `Transfers`,
`ForeignCurrencyExchanges`, `Fees`, `Interest`, `Rebates`, `OptionsPremiumsCredits`,
`RequestFromCurrencyConversion`, `Others`

---

## Market Data Calls

> **Key concept:** Most market-data endpoints accept integer **symbol IDs**,
> not ticker strings.  Use `GET /v1/symbols/search` to find the ID for a ticker.

---

### GET /v1/symbols/search

Search for symbols.

**Query params:** `prefix` (required), `offset` (optional, default 0)

**Response:**
```json
{
  "symbols": [
    {
      "symbol"          : "AAPL",
      "symbolId"        : 8049,
      "prevDayClosePrice": 193.89,
      "highPrice52"     : 199.62,
      "lowPrice52"      : 124.17,
      "averageVol3Months": 57598474,
      "averageVol20Days": 62044781,
      "outstandingShares": 15441088000,
      "eps"             : 6.16,
      "pe"              : 31.46,
      "dividend"        : 0.24,
      "yield"           : 0.0061,
      "exDate"          : "2026-02-07T00:00:00.000000-05:00",
      "marketCap"       : 2992729952320,
      "optionType"      : null,
      "optionDurationType": null,
      "optionRoot"      : "",
      "optionContractDeliverables": null,
      "optionExerciseType": null,
      "listingExchange" : "NASDAQ",
      "description"     : "APPLE INC",
      "securityType"    : "Stock",
      "optionExpiryDate": null,
      "dividendDate"    : null,
      "optionStrikePrice": null,
      "isTradable"      : true,
      "isQuotable"      : true,
      "hasOptions"      : true,
      "minTicks"        : [ ... ],
      "industrySector"  : "Technology",
      "industryGroup"   : "Technology Hardware, Storage & Peripherals",
      "industrySubgroup": "Technology Hardware, Storage & Peripherals",
      "currency"        : "USD"
    }
  ]
}
```

Security types: `Stock`, `Option`, `Bond`, `Right`, `Gold`, `MutualFund`, `Index`

---

### GET /v1/symbols/{id}

Get full details for a symbol by its integer ID.

---

### GET /v1/markets/quotes/{id}

Level 1 quote for a single symbol by path parameter.

### GET /v1/markets/quotes?ids={id1},{id2},...

Level 1 quotes for multiple symbols. Use the `ids` **query parameter** with a
comma-separated list — do not put multiple IDs in the path.

**Response:**
```json
{
  "quotes": [
    {
      "symbol"               : "AAPL",
      "symbolId"             : 8049,
      "tier"                 : "",
      "bidPrice"             : 194.20,
      "bidSize"              : 400,
      "askPrice"             : 194.25,
      "askSize"              : 200,
      "lastTradePriceTrHrs"  : 194.22,
      "lastTradePrice"       : 194.00,
      "lastTradeSize"        : 100,
      "lastTradeTick"        : "Up",
      "lastTradeTime"        : "2026-03-04T09:31:00.000000-05:00",
      "volume"               : 1200000,
      "openPrice"            : 193.50,
      "highPrice"            : 194.80,
      "lowPrice"             : 193.00,
      "delay"                : 0,
      "isHalted"             : false,
      "high52w"              : 199.62,
      "low52w"               : 124.17,
      "VWAP"                 : 194.10
    }
  ]
}
```

---

### GET /v1/markets/candles/{id}

Historical OHLCV candlestick data.

**Query params:**

| Param       | Required | Description |
|-------------|----------|-------------|
| `startTime` | Yes      | ISO 8601 datetime with offset (e.g. `2026-01-01T00:00:00-05:00`) |
| `endTime`   | Yes      | ISO 8601 datetime with offset |
| `interval`  | Yes      | Candle granularity (see below) |

**Interval values:**
`OneMinute`, `TwoMinutes`, `ThreeMinutes`, `FourMinutes`, `FiveMinutes`,
`TenMinutes`, `FifteenMinutes`, `TwentyMinutes`, `HalfHour`,
`OneHour`, `TwoHours`, `FourHours`,
`OneDay`, `OneWeek`, `OneMonth`, `OneYear`

**Response:**
```json
{
  "candles": [
    {
      "start" : "2026-01-15T09:30:00.000000-05:00",
      "end"   : "2026-01-15T09:31:00.000000-05:00",
      "low"   : 179.50,
      "high"  : 180.20,
      "open"  : 179.80,
      "close" : 180.05,
      "volume": 452310,
      "VWAP"  : 179.98
    }
  ]
}
```

---

### GET /v1/markets

List all markets and their session times.

**Response:**
```json
{
  "markets": [
    {
      "name"                : "TSX",
      "tradingVenues"       : [ "TSX", "ALPH", "CXC", "..." ],
      "defaultTradingVenue" : "AUTO",
      "primaryOrderRoutes"  : [ "AUTO" ],
      "secondaryOrderRoutes": [ "TSX", "AUTO", "..." ],
      "level1Feeds"         : [ "TSX" ],
      "level2Feeds"         : [ "TSX", "..." ],
      "extendedStartTime"   : "2026-03-04T07:00:00.000000-05:00",
      "startTime"           : "2026-03-04T09:30:00.000000-05:00",
      "endTime"             : "2026-03-04T16:00:00.000000-05:00",
      "extendedEndTime"     : "2026-03-04T20:00:00.000000-05:00",
      "snapQuotesLimit"     : 2147483647
    }
  ]
}
```

> **Note:** `startTime`/`endTime` are full ISO 8601 timestamps (not just time strings).
> The date portion reflects today's session. No `currency` or `defaultSymbolCurrency`
> field is present — currency is implied by the exchange (TSX/TSXV/CNSX = CAD, others = USD).

---

## Enumerations

### Order Side
`Buy`, `Sell`, `Short`, `Cov` (Cover)

### Order State
`Pending`, `Active`, `Binance`, `Cancelled`, `Executed`, `FilledPartially`,
`Expired`, `Queued`, `Triggered`, `Activated`, `PendingRiskReview`,
`ContingentOrder`, `PendingActivation`

### Security Type
`Stock`, `Option`, `Bond`, `Right`, `Gold`, `MutualFund`, `Index`

### Listing Exchanges
`TSX`, `TSXV`, `CNSX`, `MX`, `NASDAQ`, `NYSE`, `NYSEAM`, `ARCA`,
`OPRA`, `PinkSheets`, `OTCBB`

---

## Error Codes

| HTTP Code | Meaning |
|-----------|---------|
| 400       | Bad request / validation error |
| 401       | Unauthorized — token expired or invalid |
| 403       | Forbidden — personal token cannot place orders (partner access required) |
| 404       | Resource not found |
| 429       | Rate limit exceeded |
| 500       | Internal server error |

### 401 Recovery

Delete the token cache file and retry — the CLI will refresh automatically:

```bash
rm ~/.openclaw/data/questrade-token-cache.json
```

If the refresh token itself is expired (7-day window), generate a new one from
Questrade → App Hub → API Centre.

---

## Rate Limits

Questrade applies per-IP rate limits.  Typical safe usage is well within
limits for interactive queries.  Avoid tight polling loops on quote endpoints.

---

## Practice vs. Production

| Setting                  | Value |
|--------------------------|-------|
| Practice login URL       | `https://practicelogin.questrade.com/oauth2/token` |
| Production login URL     | `https://login.questrade.com/oauth2/token` |
| Env var to toggle        | `QUESTRADE_PRACTICE=true` or `false` |
| Credentials file field   | `"practice": true` or `false` |

Practice accounts use paper money and have identical API structure to live.

