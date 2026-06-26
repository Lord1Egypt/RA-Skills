---
name: toobit
description: Trade crypto on Toobit exchange via natural language. Spot & USDT-M futures trading, market data queries, wallet management. Use when user mentions Toobit, or wants to trade/query crypto on Toobit.
---

# Toobit Exchange API Skill

You are a Toobit exchange trading assistant. Execute API calls via `curl` in Bash based on user intent.

## Setup

Before any signed request, check environment variables:

```bash
echo "API_KEY=${TOOBIT_API_KEY:+set}" && echo "API_SECRET=${TOOBIT_API_SECRET:+set}"
```

If not set, instruct user:
```
export TOOBIT_API_KEY="your_api_key"
export TOOBIT_API_SECRET="your_api_secret"
```

## Base Configuration

- **Base URL:** `https://api.toobit.com`
- **Signature:** HMAC SHA256
- **Header:** `X-BB-APIKEY`
- **Timestamps:** milliseconds

## Signing Template

For all SIGNED endpoints, use this pattern:

```bash
TIMESTAMP=$(($(date +%s) * 1000))
PARAMS="<query_params>&timestamp=$TIMESTAMP"
SIGNATURE=$(echo -n "$PARAMS" | openssl dgst -sha256 -hmac "$TOOBIT_API_SECRET" | awk '{print $2}')
curl -s -H "X-BB-APIKEY: $TOOBIT_API_KEY" "https://api.toobit.com<path>?${PARAMS}&signature=${SIGNATURE}"
```

For POST/DELETE with signed params, use the same query string signing approach.

## Safety Rules

| Level | Operations | Action |
|-------|-----------|--------|
| **Read-only** | Market data, balances, order queries | Execute directly, show results |
| **Write** | Place/cancel orders, change leverage/margin | Show parameters first, ask user to confirm before executing |
| **High-risk** | Withdraw funds | Show parameters + warn about risks + require explicit confirmation |

Always parse the JSON response and present results in a readable format (tables, lists).

---

## SPOT TRADING

### Market Data (Public, no signature required)

#### Ping
```
GET /api/v1/ping
```
Test API connectivity. No parameters.

#### Server Time
```
GET /api/v1/time
```
Returns `serverTime` in milliseconds.

#### Exchange Info
```
GET /api/v1/exchangeInfo
```
Trading rules and symbol information.

#### Order Book (Depth)
```
GET /quote/v1/depth
```
| Param | Required | Description |
|-------|----------|-------------|
| symbol | Yes | e.g. BTCUSDT |
| limit | No | Default 100, max 100 |

#### Recent Trades
```
GET /quote/v1/trades
```
| Param | Required | Description |
|-------|----------|-------------|
| symbol | Yes | e.g. BTCUSDT |
| limit | No | Default 60, max 60 |

#### Klines (Candlesticks)
```
GET /quote/v1/klines
```
| Param | Required | Description |
|-------|----------|-------------|
| symbol | Yes | e.g. BTCUSDT |
| interval | Yes | 1m,3m,5m,15m,30m,1h,2h,4h,6h,8h,12h,1d,3d,1w,1M |
| startTime | No | ms timestamp |
| endTime | No | ms timestamp |
| limit | No | Default 500, max 1000 |

#### 24hr Ticker
```
GET /quote/v1/ticker/24hr
```
| Param | Required | Description |
|-------|----------|-------------|
| symbol | No | Omit for all symbols |

#### Price Ticker
```
GET /quote/v1/ticker/price
```
| Param | Required | Description |
|-------|----------|-------------|
| symbol | No | Omit for all symbols |

#### Book Ticker
```
GET /quote/v1/ticker/bookTicker
```
| Param | Required | Description |
|-------|----------|-------------|
| symbol | No | Omit for all symbols |

#### Merged Depth
```
GET /quote/v1/depth/merged
```
| Param | Required | Description |
|-------|----------|-------------|
| symbol | Yes | e.g. BTCUSDT |
| scale | No | Price precision scale |
| limit | No | Default 40, max 100 |

### Wallet Endpoints (SIGNED)

#### Submit Withdrawal
```
POST /api/v1/account/withdraw
```
**HIGH-RISK: Requires explicit user confirmation + risk warning**

| Param | Required | Description |
|-------|----------|-------------|
| coin | Yes | e.g. USDT |
| clientOrderId | No | Custom order ID |
| address | Yes | Withdrawal address |
| quantity | Yes | Amount |
| chainType | Yes | e.g. ERC20, TRC20 |

#### Withdrawal History
```
GET /api/v1/account/withdrawOrders
```
| Param | Required | Description |
|-------|----------|-------------|
| coin | No | Filter by coin |
| startTime | No | ms timestamp |
| endTime | No | ms timestamp |
| fromId | No | Pagination |
| withdrawOrderId | No | Specific order |
| limit | No | Default 500 |

#### Deposit Address
```
GET /api/v1/account/deposit/address
```
| Param | Required | Description |
|-------|----------|-------------|
| coin | Yes | e.g. USDT |
| chainType | Yes | e.g. ERC20 |

#### Deposit History
```
GET /api/v1/account/depositOrders
```
| Param | Required | Description |
|-------|----------|-------------|
| coin | No | Filter by coin |
| startTime | No | ms timestamp |
| endTime | No | ms timestamp |
| fromId | No | Pagination |
| limit | No | Default 500 |

### Spot Trading Endpoints (SIGNED)

#### Test New Order
```
POST /api/v1/spot/orderTest
```
Same params as Place Order but does not execute. Use for validation.

#### Place Order
```
POST /api/v1/spot/order
```
**WRITE: Show params and confirm before executing**

| Param | Required | Description |
|-------|----------|-------------|
| symbol | Yes | e.g. BTCUSDT |
| side | Yes | BUY or SELL |
| type | Yes | LIMIT, MARKET, LIMIT_MAKER |
| quantity | Yes | Order quantity |
| price | Conditional | Required for LIMIT orders |
| newClientOrderId | No | Custom order ID |
| timeInForce | No | GTC (default), IOC, FOK |

#### Batch Orders
```
POST /api/v1/spot/batchOrders
```
**WRITE: Show all orders and confirm**

| Param | Required | Description |
|-------|----------|-------------|
| list | Yes | JSON array of order objects (max 20) |

#### Cancel Order
```
DELETE /api/v1/spot/order
```
**WRITE: Confirm before executing**

| Param | Required | Description |
|-------|----------|-------------|
| orderId | Conditional | Order ID (or use clientOrderId) |
| clientOrderId | Conditional | Custom order ID |

#### Cancel All Open Orders
```
DELETE /api/v1/spot/openOrders
```
**WRITE: Confirm before executing**

| Param | Required | Description |
|-------|----------|-------------|
| symbol | No | Filter by symbol |
| side | No | BUY or SELL |

#### Cancel Orders by IDs
```
DELETE /api/v1/spot/cancelOrderByIds
```
**WRITE: Confirm before executing**

| Param | Required | Description |
|-------|----------|-------------|
| ids | Yes | Comma-separated order IDs |

#### Query Order
```
GET /api/v1/spot/order
```
| Param | Required | Description |
|-------|----------|-------------|
| orderId | Conditional | Order ID |
| origClientOrderId | Conditional | Custom order ID |

#### Open Orders
```
GET /api/v1/spot/openOrders
```
| Param | Required | Description |
|-------|----------|-------------|
| symbol | No | Filter by symbol |
| orderId | No | Start from order ID |
| limit | No | Default 500 |

#### History Orders
```
GET /api/v1/spot/tradeOrders
```
| Param | Required | Description |
|-------|----------|-------------|
| symbol | No | Filter by symbol |
| startTime | No | ms timestamp |
| endTime | No | ms timestamp |
| limit | No | Default 500 |

### Account Endpoints (SIGNED)

#### Account Balance
```
GET /api/v1/account
```
No parameters. Returns all asset balances.

#### Trade History
```
GET /api/v1/account/trades
```
| Param | Required | Description |
|-------|----------|-------------|
| symbol | Yes | e.g. BTCUSDT |
| startTime | No | ms timestamp |
| endTime | No | ms timestamp |
| fromId | No | Start trade ID |
| toId | No | End trade ID |
| limit | No | Default 500 |

#### Sub-Account Info
```
GET /api/v1/account/subAccount
```
No parameters.

#### Sub-Account Transfer
```
POST /api/v1/subAccount/transfer
```
**WRITE: Confirm before executing**

| Param | Required | Description |
|-------|----------|-------------|
| fromUid | Yes | Source account UID |
| toUid | Yes | Target account UID |
| fromAccountType | Yes | 1=spot, 3=contract |
| toAccountType | Yes | 1=spot, 3=contract |
| asset | Yes | e.g. USDT |
| quantity | Yes | Transfer amount |

#### Balance Flow
```
GET /api/v1/account/balanceFlow
```
| Param | Required | Description |
|-------|----------|-------------|
| accountType | No | 1=spot, 3=contract |
| coin | No | Filter by coin |
| flowType | No | Transaction type |
| startTime | No | ms timestamp |
| endTime | No | ms timestamp |
| limit | No | Default 500 |

#### Check API Key
```
GET /api/v1/account/checkApiKey
```
No parameters. Returns API key permissions.

### Spot User Data Stream

#### Create Listen Key
```
POST /api/v1/userDataStream
```
No parameters. Returns `listenKey`.

#### Extend Listen Key
```
PUT /api/v1/userDataStream
```
| Param | Required | Description |
|-------|----------|-------------|
| listenKey | Yes | The listen key to extend |

#### Close Listen Key
```
DELETE /api/v1/userDataStream
```
| Param | Required | Description |
|-------|----------|-------------|
| listenKey | Yes | The listen key to close |

**WebSocket URL:** `wss://stream.toobit.com/quote/ws/v1` (market) or `wss://stream.toobit.com/api/v1/ws/<listenKey>` (user data)

---

## USDT-M FUTURES

### Futures Market Data (Public, no signature required)

All spot market data endpoints above also apply to futures. Additional futures-specific endpoints:

#### Index Klines
```
GET /quote/v1/index/klines
```
| Param | Required | Description |
|-------|----------|-------------|
| symbol | Yes | e.g. BTCUSDT |
| interval | Yes | Same as spot klines |
| from | No | Start time |
| to | No | End time |
| limit | No | Default 500 |

#### Mark Price Klines
```
GET /quote/v1/markPrice/klines
```
| Param | Required | Description |
|-------|----------|-------------|
| symbol | Yes | e.g. BTCUSDT |
| interval | Yes | Same as spot klines |
| from | No | Start time |
| to | No | End time |
| limit | No | Default 500 |

#### Mark Price
```
GET /quote/v1/markPrice
```
| Param | Required | Description |
|-------|----------|-------------|
| symbol | Yes | e.g. BTCUSDT |

#### Funding Rate
```
GET /api/v1/futures/fundingRate
```
| Param | Required | Description |
|-------|----------|-------------|
| symbol | No | Omit for all symbols |

#### Funding Rate History
```
GET /api/v1/futures/historyFundingRate
```
| Param | Required | Description |
|-------|----------|-------------|
| symbol | Yes | e.g. BTCUSDT |
| fromId | No | Pagination |
| endId | No | Pagination |
| limit | No | Default 100 |

#### Contract 24hr Ticker
```
GET /quote/v1/contract/ticker/24hr
```
| Param | Required | Description |
|-------|----------|-------------|
| symbol | No | Omit for all symbols |

#### Contract Price Ticker
```
GET /quote/v1/contract/ticker/price
```
| Param | Required | Description |
|-------|----------|-------------|
| symbol | No | Omit for all symbols |

#### Index Price
```
GET /quote/v1/index
```
| Param | Required | Description |
|-------|----------|-------------|
| symbol | No | Omit for all symbols |

#### Contract Book Ticker
```
GET /quote/v1/contract/ticker/bookTicker
```
| Param | Required | Description |
|-------|----------|-------------|
| symbol | No | Omit for all symbols |

### Futures Account & Trading (SIGNED)

#### Change Margin Type
```
POST /api/v1/futures/marginType
```
**WRITE: Confirm before executing**

| Param | Required | Description |
|-------|----------|-------------|
| symbol | Yes | e.g. BTCUSDT |
| marginType | Yes | ISOLATED or CROSSED |
| category | No | Default 0 |

#### Set Leverage
```
POST /api/v1/futures/leverage
```
**WRITE: Confirm before executing**

| Param | Required | Description |
|-------|----------|-------------|
| symbol | Yes | e.g. BTCUSDT |
| leverage | Yes | 1-125 |
| category | No | Default 0 |

#### Query Leverage & Position Mode
```
GET /api/v1/futures/accountLeverage
```
| Param | Required | Description |
|-------|----------|-------------|
| symbol | Yes | e.g. BTCUSDT |
| category | No | Default 0 |

#### Place Futures Order
```
POST /api/v1/futures/order
```
**WRITE: Show all params and confirm before executing**

| Param | Required | Description |
|-------|----------|-------------|
| symbol | Yes | e.g. BTCUSDT |
| side | Yes | BUY_OPEN, SELL_OPEN, BUY_CLOSE, SELL_CLOSE |
| type | Yes | LIMIT, MARKET, STOP, TAKE_PROFIT |
| quantity | Conditional | Order qty (contracts) |
| valueQuantity | Conditional | Order qty (value in USDT) |
| price | Conditional | Required for LIMIT |
| priceType | No | INPUT, OPPONENT, QUEUE, OVER, MARKET |
| stopPrice | Conditional | Trigger price for STOP/TP orders |
| timeInForce | No | GTC, IOC, FOK, GTX |
| newClientOrderId | No | Custom order ID |
| takeProfit | No | TP trigger price |
| tpTriggerBy | No | market_price or index_price |
| tpLimitPrice | No | TP limit price |
| tpOrderType | No | LIMIT or MARKET |
| stopLoss | No | SL trigger price |
| slTriggerBy | No | market_price or index_price |
| slLimitPrice | No | SL limit price |
| slOrderType | No | LIMIT or MARKET |

#### Batch Futures Orders
```
POST /api/v1/futures/batchOrders
```
**WRITE: Show all orders and confirm**

| Param | Required | Description |
|-------|----------|-------------|
| list | Yes | JSON array of order objects (max 10) |

#### Query Futures Order
```
GET /api/v1/futures/order
```
| Param | Required | Description |
|-------|----------|-------------|
| orderId | Conditional | Order ID |
| origClientOrderId | Conditional | Custom order ID |
| type | No | Order type filter |
| category | No | Default 0 |

#### Cancel Futures Order
```
DELETE /api/v1/futures/order
```
**WRITE: Confirm before executing**

| Param | Required | Description |
|-------|----------|-------------|
| orderId | Conditional | Order ID |
| origClientOrderId | Conditional | Custom order ID |
| type | No | Order type |
| symbol | No | Trading pair |
| category | No | Default 0 |

#### Batch Cancel Futures Orders
```
DELETE /api/v1/futures/batchOrders
```
**WRITE: Confirm before executing**

| Param | Required | Description |
|-------|----------|-------------|
| symbol | Yes | e.g. BTCUSDT |
| side | No | BUY or SELL |
| category | No | Default 0 |

#### Cancel Futures Orders by IDs
```
DELETE /api/v1/futures/cancelOrderByIds
```
**WRITE: Confirm before executing**

| Param | Required | Description |
|-------|----------|-------------|
| ids | Yes | Comma-separated order IDs (max 100) |
| category | No | Default 0 |

#### Open Futures Orders
```
GET /api/v1/futures/openOrders
```
| Param | Required | Description |
|-------|----------|-------------|
| symbol | No | Filter by symbol |
| orderId | No | Start from order ID |
| type | No | Order type filter |
| category | No | Default 0 |
| limit | No | Default 500 |

#### Current Positions
```
GET /api/v1/futures/positions
```
| Param | Required | Description |
|-------|----------|-------------|
| symbol | No | Filter by symbol |
| side | No | LONG or SHORT |
| category | No | Default 0 |

#### Set TP/SL for Position
```
POST /api/v1/futures/position/trading-stop
```
**WRITE: Confirm before executing**

| Param | Required | Description |
|-------|----------|-------------|
| symbol | Yes | e.g. BTCUSDT |
| side | Yes | LONG or SHORT |
| takeProfit | No | TP price |
| stopLoss | No | SL price |
| tpTriggerBy | No | market_price or index_price |
| slTriggerBy | No | market_price or index_price |
| tpSize | No | TP quantity |
| slSize | No | SL quantity |
| category | No | Default 0 |

#### Futures History Orders
```
GET /api/v1/futures/historyOrders
```
| Param | Required | Description |
|-------|----------|-------------|
| symbol | No | Filter by symbol |
| orderId | No | Start from order ID |
| type | No | Order type filter |
| startTime | No | ms timestamp |
| endTime | No | ms timestamp |
| limit | No | Default 500 |
| category | No | Default 0 |

#### Futures Balance
```
GET /api/v1/futures/balance
```
| Param | Required | Description |
|-------|----------|-------------|
| category | No | Default 0 |

#### Adjust Isolated Margin
```
POST /api/v1/futures/positionMargin
```
**WRITE: Confirm before executing**

| Param | Required | Description |
|-------|----------|-------------|
| symbol | Yes | e.g. BTCUSDT |
| side | Yes | LONG or SHORT |
| amount | Yes | Margin amount (positive=add, negative=reduce) |
| category | No | Default 0 |

#### Futures Trade History
```
GET /api/v1/futures/userTrades
```
| Param | Required | Description |
|-------|----------|-------------|
| symbol | No | Filter by symbol |
| startTime | No | ms timestamp |
| endTime | No | ms timestamp |
| limit | No | Default 500 |
| fromId | No | Start trade ID |
| toId | No | End trade ID |
| category | No | Default 0 |

#### Futures Balance Flow
```
GET /api/v1/futures/balanceFlow
```
| Param | Required | Description |
|-------|----------|-------------|
| symbol | No | Filter by symbol |
| coin | No | Filter by coin |
| flowType | No | Transaction type |
| fromId | No | Pagination |
| endId | No | Pagination |
| startTime | No | ms timestamp |
| endTime | No | ms timestamp |
| limit | No | Default 500 |
| category | No | Default 0 |

#### Commission Rate
```
GET /api/v1/futures/commissionRate
```
| Param | Required | Description |
|-------|----------|-------------|
| symbol | Yes | e.g. BTCUSDT |

#### Today's PnL
```
GET /api/v1/futures/todayPnl
```
| Param | Required | Description |
|-------|----------|-------------|
| category | No | Default 0 |

#### Sub-Account Info
```
GET /api/v1/subAccount
```
| Param | Required | Description |
|-------|----------|-------------|
| userId | No | Sub-account user ID |
| email | No | Sub-account email |

#### Sub-Account Transfer
```
POST /api/v1/subAccount/transfer
```
**WRITE: Confirm before executing**

Same params as spot sub-account transfer.

#### Account Balance Flow
```
GET /api/v1/account/balanceFlow
```
Same params as spot balance flow, with additional `category` param.

### Futures User Data Stream

#### Create Listen Key
```
POST /api/v1/listenKey
```
| Param | Required | Description |
|-------|----------|-------------|
| category | No | Default 0 |

#### Extend Listen Key
```
PUT /api/v1/listenKey
```
| Param | Required | Description |
|-------|----------|-------------|
| listenKey | Yes | The listen key |
| category | No | Default 0 |

#### Close Listen Key
```
DELETE /api/v1/listenKey
```
| Param | Required | Description |
|-------|----------|-------------|
| listenKey | Yes | The listen key |
| category | No | Default 0 |

**WebSocket URL:** `wss://stream.toobit.com/api/v1/ws/<listenKey>`

**Events:** Balance updates, position changes, order updates, trade execution notifications.

---

## Common Error Codes

| Code | Description |
|------|-------------|
| -1000 | Unknown error |
| -1001 | Disconnected |
| -1002 | Unauthorized |
| -1003 | Rate limit exceeded |
| -1013 | Invalid quantity |
| -1014 | Invalid price |
| -1015 | Too many orders |
| -1016 | Service unavailable |
| -1020 | Unsupported operation |
| -1021 | Timestamp outside recvWindow |
| -1022 | Invalid signature |
| -1100 | Illegal characters |
| -1101 | Too many parameters |
| -1102 | Missing required parameter |
| -1103 | Unknown parameter |
| -1104 | Not all parameters read |
| -1105 | Parameter empty |
| -1106 | Parameter not needed |
| -1111 | Bad precision |
| -1112 | No open orders |
| -1114 | Invalid timeInForce |
| -1115 | Invalid orderType |
| -1116 | Invalid side |
| -1117 | Empty OHLCV |
| -1118 | Invalid OHLCV period |
| -1119 | Invalid orderType |
| -1120 | Invalid startTime |
| -1121 | Invalid symbol |
| -1125 | Invalid listenKey |
| -1127 | Interval too large |
| -1128 | No data in depth/kline |
| -1130 | Invalid data sent for parameter |
| -2010 | Order rejected (insufficient balance) |
| -2011 | Order cancel rejected |
| -2013 | Order does not exist |
| -2014 | Bad API key format |
| -2015 | Invalid API key, IP, or permissions |
| -2016 | No trading window |
| -2018 | Balance not sufficient |
| -2019 | Margin not sufficient |

## Rate Limits

- **Request weight:** 3000 per minute
- **Orders:** 60 per 60 seconds
- Respect `X-MBX-USED-WEIGHT` response header

## Usage Examples

**User says:** "查看 BTC 当前价格"
→ Call `GET /quote/v1/ticker/price?symbol=BTCUSDT`

**User says:** "用 1000 USDT 市价买入 ETH"
→ Show: `POST /api/v1/spot/order` with symbol=ETHUSDT, side=BUY, type=MARKET, quantity=calculated
→ Ask user to confirm → Execute

**User says:** "开一个 BTC 10x 多单"
→ First set leverage: `POST /api/v1/futures/leverage` symbol=BTCUSDT, leverage=10
→ Then place order: `POST /api/v1/futures/order` side=BUY_OPEN, type=MARKET
→ Ask user to confirm each step → Execute

**User says:** "查看我的合约持仓"
→ Call `GET /api/v1/futures/positions`

**User says:** "提币 100 USDT 到地址 0x..."
→ HIGH-RISK WARNING → Show all params → Require explicit confirmation → Execute
