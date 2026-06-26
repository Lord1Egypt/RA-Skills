# TTC Box REST API

Base URL: `https://ttc.box`

## Authentication

All requests to `/api/v1/` require two headers:

```
ttc-auth-token: <your-auth-token>
ttc-public-key: <your-public-key>
```

Obtain these by calling `POST /api/auth/login` or `POST /api/auth/register`.

---

## Auth Endpoints

### POST /api/auth/register

Create a new account. Client generates wallets and hashes the passkey before sending.

**Body:**
```json
{
  "email": "user@example.com",
  "hashedPasskey": "<sha256(passkey)>",
  "clientGeneratedWallets": {
    "solanaPublicKey": "<base58-pubkey>",
    "solanaPrivateKey": "<aes-encrypted-hex-keypair>",
    "evmAddress": "<0x-address>",
    "evmPrivateKey": "<aes-encrypted-hex-private-key>"
  }
}
```

**Response:**
```json
{
  "success": true,
  "authToken": "<token>",
  "publicKey": "<base58-pubkey>"
}
```

---

### POST /api/auth/login

Login with email and passkey. Send plain passkey — server SHA-256s it internally.

**Body:**
```json
{
  "email": "user@example.com",
  "passKey": "<plain-passkey>"
}
```

**Response:**
```json
{
  "success": true,
  "authToken": "<token>",
  "user": {
    "publicKey": "<base58-pubkey>"
  }
}
```

---

## Exchange Endpoints

### POST /api/v1/exchanges

Central dispatch for all exchange operations.

**Headers:** `ttc-auth-token`, `ttc-public-key`, `Content-Type: application/json`

**Body shape:**
```json
{
  "exchangeName": "<SupportedExchange>",
  "method": "<ExchangeMethod>",
  "params": {},
  "credentials": {
    "apiKey": "...",
    "apiSecret": "...",
    "passphrase": "...",
    "walletAddress": "..."
  }
}
```

> `getTickers` is the only method that does not require `credentials`.

> For `orderly` with **email-registered** accounts: set `ORDERLY_MAIN_WALLET_ADDRESS` in `.env` — the CLI sends it as `walletAddress` in credentials so the server routes requests to your real trading wallet. Web3 users do not need this; their `TTC_PUBLIC_KEY` is already their Orderly wallet address.

---

### Available Methods

```typescript
type ExchangeMethod =
  | "setHedgeMode"
  | "setLeverage"
  | "getPositions"
  | "getBalance"
  | "placeLimitOrder"
  | "placeMarketOrder"
  | "placeStopOrder"
  | "closeAllPositions"
  | "createWithdrawal"
  | "getDepositAddress"
  | "getOrders"
  | "cancelAllOrders"
  | "cancelOrder"
  | "getTickers"
  | "getBestBidAsk"
  | "getUserTradeHistory"
```

> **Note:** `getOpenOrders` is NOT a valid method — use `getOrders`.

| Method | Description | Creds Required |
|---|---|---|
| `getTickers` | Get ticker info for all/one trading pair | No |
| `getBestBidAsk` | Best bid and ask for a symbol | Yes |
| `getBalance` | Account balance | Yes |
| `getPositions` | Open positions | Yes |
| `getOrders` | Open or historical orders | Yes |
| `getUserTradeHistory` | Historical trade records | Yes |
| `placeLimitOrder` | Place a limit order | Yes |
| `placeMarketOrder` | Place a market order | Yes |
| `placeStopOrder` | Place a stop/trigger order | Yes |
| `cancelOrder` | Cancel a specific order | Yes |
| `cancelAllOrders` | Cancel all open orders | Yes |
| `closeAllPositions` | Close all open positions | Yes |
| `setLeverage` | Set leverage for a symbol | Yes |
| `setHedgeMode` | Enable/disable hedge mode | Yes |
| `getDepositAddress` | Get deposit address for an asset | Yes |
| `createWithdrawal` | Initiate a withdrawal | Yes |

---

### Method Params

#### getTickers
```json
{ "symbol": "BTCUSDT" }
```
Omit `symbol` to get all tickers.

#### getBestBidAsk
```json
"BTCUSDT"
```
Send the symbol as a plain string (not an object).

#### getBalance
```json
{}
```

#### getPositions
```json
{ "symbol": "BTCUSDT" }
```
Omit `symbol` for all positions.

#### getOrders
```json
{ "symbol": "BTCUSDT" }
```

#### placeLimitOrder
```json
{
  "symbol": "BTCUSDT",
  "side": "buy",
  "quantity": 0.001,
  "price": 60000,
  "positionSide": "long",
  "timeInForce": "GoodTillCancel",
  "reduceOnly": false,
  "clientOrderId": "my-order-1"
}
```

#### placeMarketOrder
```json
{
  "symbol": "BTCUSDT",
  "side": "buy",
  "quantity": 0.001,
  "positionSide": "long",
  "reduceOnly": false
}
```

#### placeStopOrder
```json
{
  "symbol": "BTCUSDT",
  "side": "sell",
  "quantity": 0.001,
  "stopPrice": 58000,
  "triggerType": "ByLastPrice",
  "positionSide": "long"
}
```

#### cancelOrder
```json
{
  "symbol": "BTCUSDT",
  "orderId": "12345"
}
```

#### cancelAllOrders
```json
{ "symbol": "BTCUSDT" }
```

#### setLeverage
```json
{
  "symbol": "BTCUSDT",
  "leverage": 10
}
```

#### setHedgeMode
```json
{ "hedgeMode": true }
```

#### getUserTradeHistory
```json
{ "limit": 1000 }
```

---

### GET /api/v1/exchanges

#### Health check
```
GET /api/v1/exchanges
```
Returns list of supported exchanges and API status.

#### List all methods
```
GET /api/v1/exchanges?list-methods=true
```

#### Get trade history (GET variant)
```
GET /api/v1/exchanges?method=getUserTradeHistory&exchange=bybit&apiKey=...&apiSecret=...
```

---

### GET /api/v1/exchanges/latency

Returns latency measurements for exchanges.

---

## Supported Exchanges

```typescript
type SupportedExchange =
  | "asterdex" | "apex"    | "ascendex" | "aevo"
  | "binance"  | "bingx"   | "bitget"   | "bitmex"
  | "blofin"   | "bybit"   | "deso"     | "dydx"
  | "extended" | "flash"   | "grvt"     | "hyperliquid"
  | "kucoin"   | "lighter" | "mexc"     | "okx"
  | "orderly"  | "pacifica"| "paradex"  | "phemex"
  | "propr"    | "reya"    | "variational" | "vest"
  | "woox"
```

---

## Market Endpoints

All market endpoints are `GET` requests. All require `ttc-auth-token` + `ttc-public-key` headers.

| Endpoint | Description |
|---|---|
| `GET /api/v1/markets/funding-rates` | Funding rates across exchanges |
| `GET /api/v1/markets/open-interest` | Open interest data |
| `GET /api/v1/markets/hybrid-tickers` | Aggregated tickers across exchanges |
| `GET /api/v1/markets/ttc-scanner` | TTC market scanner |
| `GET /api/v1/markets/volume-snapshot` | Volume snapshot |
| `GET /api/v1/markets/swap-volume` | Swap volume data |
| `GET /api/v1/markets/listings` | New token listings |
| `GET /api/v1/markets/news` | Market news |
| `GET /api/v1/markets/insights` | Market insights |
| `GET /api/v1/markets/calendar` | Economic calendar |
| `GET /api/v1/markets/quakes` | Market quake events |

---

## MPP Endpoints

| Endpoint | Description |
|---|---|
| `GET /api/v1/mpp` | MPP data |
| `GET /api/v1/mpp/solana` | Solana-specific MPP data |

---

## Known Quirks

- `getBestBidAsk` `params` must be a plain string (the symbol), not `{ symbol: "..." }` — the server wraps it internally as `{ symbol: params }`.
- `getOrders` is the correct method name. `getOpenOrders` returns 403.
- `getTickers` is the only public method — all others require exchange API credentials.
- For `orderly` with email-registered accounts, `walletAddress` must be sent explicitly in credentials. Set `ORDERLY_MAIN_WALLET_ADDRESS` in `.env` — the CLI handles this automatically. The server resolves the account as: `credentials.walletAddress || userWalletAddress`.
