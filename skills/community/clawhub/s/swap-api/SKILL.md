---
name: kycrip-swap
description: Exchange cryptocurrencies via kyc.rip aggregator API. Use when swapping, converting, or exchanging crypto assets. Supports 700+ coins, no KYC, best rates across 10+ providers.
license: MIT
metadata:
  author: kyc-rip
  version: "1.0"
---

# kyc.rip Swap API

No-KYC cryptocurrency exchange aggregator. Compares rates across 10+ providers (Houdini, Trocador, SimpleSwap, ChangeNOW, FixedFloat, StealthEX, LetsExchange, Exolix, Godex, SideShift, and more) and returns the best deal.

**Base URL:** `https://api.kyc.rip`

No authentication required. All endpoints are public.

---

## Endpoints

### 1. Get Swap Estimate

Compare rates across all providers for a given trading pair.

```
GET /v2/exchange/estimate
```

**Query Parameters:**

| Param      | Type   | Default    | Description |
|------------|--------|------------|-------------|
| `from`     | string | `btc`      | Source currency ticker (lowercase) |
| `from_net` | string | `Mainnet`  | Source network |
| `to`       | string | `xmr`      | Destination currency ticker (lowercase) |
| `to_net`   | string | `Mainnet`  | Destination network |
| `amount`   | number | (required) | Amount to send (must be > 0) |
| `kyc`      | string | `D`        | Max KYC level filter: `A` (none), `B` (light), `C` (moderate), `D` (any) |
| `log`      | string | `C`        | Max logging policy filter: `A` (no logs), `B` (minimal), `C` (any) |
| `type`     | string | —          | Set to `to` for fixed-output mode (specify desired receive amount) |
| `fund_risk`| string | —          | Fund risk tolerance filter |
| `no_cache` | string | —          | Set to `1` to bypass cache |

**Example — Get best rate for 0.1 BTC to XMR, privacy-only providers:**

```
GET /v2/exchange/estimate?from=btc&to=xmr&amount=0.1&kyc=A&log=A
```

**Response:**

```json
{
  "amount_to": 8.42,
  "routes": [
    {
      "provider": "Houdini_Privacy",
      "engine": "houdini",
      "amount_to": 8.42,
      "amount_from": 0.1,
      "kyc": "A",
      "log_policy": "A",
      "eta": 15,
      "fixed": false,
      "spread": 0.012,
      "providerLogo": "https://..."
    },
    {
      "provider": "SageSwap",
      "engine": "sageswap",
      "amount_to": 8.38,
      "amount_from": 0.1,
      "kyc": "A",
      "log_policy": "A",
      "eta": 20,
      "fixed": false,
      "spread": 0.015
    }
  ]
}
```

Routes are sorted by best rate. The top-level `amount_to` reflects the best route.

---

### 2. Create a Swap Trade

Execute a swap through a specific provider/engine.

```
POST /v2/exchange/create
Content-Type: application/json
```

**Request Body:**

| Field           | Type    | Required | Description |
|-----------------|---------|----------|-------------|
| `engine`        | string  | No       | Engine name (default: `trocador`). Use the `engine` value from the estimate route. |
| `provider`      | string  | Yes      | Provider name from the estimate route |
| `from_currency` | string  | Yes      | Source ticker (e.g. `btc`) |
| `from_network`  | string  | No       | Source network (default: `Mainnet`) |
| `to_currency`   | string  | Yes      | Destination ticker (e.g. `xmr`) |
| `to_network`    | string  | No       | Destination network (default: `Mainnet`) |
| `amount_from`   | number  | Yes*     | Amount to send (*required when `fixed_rate` is false) |
| `amount_to`     | number  | Yes*     | Amount to receive (*required when `fixed_rate` is true) |
| `address_to`    | string  | Yes      | Destination wallet address |
| `address_memo`  | string  | No       | Memo/tag for destination (XRP, XLM, etc.) |
| `fixed_rate`    | boolean | No       | Lock the exchange rate (default: false) |
| `ref`           | string  | No       | Referral code |

**Example — Swap 0.1 BTC to XMR:**

```json
{
  "engine": "houdini",
  "provider": "Houdini_Privacy",
  "from_currency": "btc",
  "from_network": "Mainnet",
  "to_currency": "xmr",
  "to_network": "Mainnet",
  "amount_from": 0.1,
  "address_to": "48vKMSzWMF9b..."
}
```

**Response:**

```json
{
  "id": "abc123-def456",
  "status": "WAITING",
  "engine": "houdini",
  "provider": "Houdini_Privacy",
  "depositAddress": "bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh",
  "depositAmount": 0.1,
  "depositMemo": null,
  "fromTicker": "BTC",
  "fromNetwork": "Mainnet",
  "fromAmount": 0.1,
  "toTicker": "XMR",
  "toNetwork": "Mainnet",
  "toAmount": 8.42,
  "address_user": "48vKMSzWMF9b...",
  "createdAt": "2026-03-15T10:00:00Z",
  "eta": 15
}
```

After creating the trade, send the exact `depositAmount` to `depositAddress`. If `depositMemo` is present, include it in the transaction.

---

### 3. Check Trade Status

Poll the status of an existing trade.

```
GET /v2/exchange/status/:id
```

**Query Parameters:**

| Param    | Type   | Description |
|----------|--------|-------------|
| `engine` | string | (Optional) Specify the engine directly. If omitted, the API auto-detects. |

**Example:**

```
GET /v2/exchange/status/abc123-def456?engine=houdini
```

**Response:**

```json
{
  "id": "abc123-def456",
  "status": "EXCHANGING",
  "engine": "houdini",
  "provider": "Houdini_Privacy",
  "fromTicker": "BTC",
  "fromAmount": 0.1,
  "toTicker": "XMR",
  "toAmount": 8.42,
  "depositAddress": "bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh",
  "depositAmount": 0.1,
  "address_user": "48vKMSzWMF9b...",
  "txIn": "a1b2c3d4e5f6...",
  "txOut": null,
  "confirmations": 2,
  "createdAt": "2026-03-15T10:00:00Z",
  "timing": {
    "detectedAt": "2026-03-15T10:05:00Z",
    "confirmedAt": "2026-03-15T10:15:00Z",
    "sendingAt": null,
    "finishedAt": null
  }
}
```

**Trade Statuses:**

| Status        | Description |
|---------------|-------------|
| `WAITING`     | Awaiting deposit from user |
| `CONFIRMING`  | Deposit detected, waiting for blockchain confirmations |
| `EXCHANGING`  | Deposit confirmed, exchange in progress |
| `SENDING`     | Exchange complete, sending funds to destination |
| `FINISHED`    | Swap completed successfully |
| `FAILED`      | Swap failed (contact support) |
| `REFUNDED`    | Funds returned to sender |
| `EXPIRED`     | Deposit window expired |

---

### 4. List Supported Currencies

Get all currencies available for swapping.

```
GET /v2/exchange/currencies
```

**Query Parameters:**

| Param   | Type   | Description |
|---------|--------|-------------|
| `force` | string | Set to `true` to bypass cache and refresh from all engines |

**Example:**

```
GET /v2/exchange/currencies
```

**Response (array):**

```json
[
  {
    "id": "btc-Mainnet",
    "ticker": "btc",
    "network": "Mainnet",
    "name": "Bitcoin",
    "image": "https://...",
    "minimum": 0.0001,
    "maximum": 10,
    "memo": false,
    "engine": "trocador",
    "engines": ["trocador", "houdini", "sageswap"]
  },
  {
    "id": "usdt-TRC20",
    "ticker": "usdt",
    "network": "TRC20",
    "name": "Tether",
    "image": "https://...",
    "minimum": 1,
    "maximum": 100000,
    "memo": false,
    "engine": "trocador",
    "engines": ["trocador", "houdini"]
  }
]
```

---

### 5. Validate Crypto Address

Check if a wallet address is valid for a given currency and network.

```
GET /v2/exchange/validate
```

**Query Parameters:**

| Param     | Type   | Required | Description |
|-----------|--------|----------|-------------|
| `ticker`  | string | Yes      | Currency ticker (e.g. `btc`) |
| `network` | string | Yes      | Network name (e.g. `Mainnet`) |
| `address` | string | Yes      | Wallet address to validate |

**Example:**

```
GET /v2/exchange/validate?ticker=btc&network=Mainnet&address=bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh
```

**Response:**

```json
{
  "valid": true,
  "ticker": "btc",
  "network": "Mainnet"
}
```

---

### 6. Ghost Protocol (Privacy Bridge)

Two-hop privacy swaps that route through an intermediary (typically XMR) to break the on-chain link between source and destination.

#### 6a. Bridge Estimate

```
GET /v2/exchange/bridge/estimate
```

**Query Parameters:**

| Param         | Type   | Default   | Description |
|---------------|--------|-----------|-------------|
| `from`        | string | `btc`     | Source ticker |
| `to`          | string | `btc`     | Destination ticker |
| `amount`      | number | (required)| Amount to send (must be > 0) |
| `network_from`| string | `Mainnet` | Source network |
| `network_to`  | string | `Mainnet` | Destination network |
| `no_cache`    | string | —         | Set to `1` to bypass cache |

**Example — Bridge 1 ETH to BTC via privacy tunnel:**

```
GET /v2/exchange/bridge/estimate?from=eth&to=btc&amount=1&network_from=Mainnet&network_to=Mainnet
```

**Response:**

```json
{
  "amount_to": 0.038,
  "eta": 20,
  "routes": [
    {
      "engine": "houdini",
      "provider": "HOUDINI_Tunnel",
      "amount_to": 0.038,
      "eta": 15,
      "kyc": "A",
      "type": "TUNNEL",
      "ingressProvider": "Houdini",
      "egressProvider": "Houdini",
      "ingressKyc": "A",
      "egressKyc": "A",
      "requiresRefund": false,
      "bridgeLabel": "MONERO_TUNNEL",
      "bridgeBadge": "FASTEST",
      "bridgeHighlight": "SPEED_OPTIMIZED"
    },
    {
      "engine": "custom",
      "provider": "Custom_Privacy_Bridge",
      "amount_to": 0.0375,
      "eta": 30,
      "kyc": "A",
      "type": "DOUBLE_HOP",
      "hops": [
        { "name": "SimpleSwap" },
        { "name": "SageSwap" }
      ],
      "ingressProvider": "SimpleSwap",
      "egressProvider": "SageSwap",
      "ingressKyc": "C",
      "egressKyc": "A",
      "requiresRefund": true,
      "bridgeLabel": "CUSTOM_PRIVACY_BRIDGE",
      "bridgeBadge": "OPTIMAL",
      "bridgeHighlight": "BEST_OF_BOTH"
    }
  ]
}
```

Routes are sorted by a composite score: privacy (40%) + rate (40%) + speed (20%).

#### 6b. Bridge Create

```
POST /v2/exchange/bridge/create
Content-Type: application/json
```

**Request Body:**

| Field            | Type   | Required | Description |
|------------------|--------|----------|-------------|
| `engine`         | string | No       | Engine name (default: `trocador`). Use `engine` from bridge estimate route. |
| `from_currency`  | string | Yes      | Source ticker |
| `from_network`   | string | No       | Source network (default: `Mainnet`) |
| `to_currency`    | string | Yes      | Destination ticker |
| `to_network`     | string | No       | Destination network (default: `Mainnet`) |
| `amount_from`    | number | Yes      | Amount to send |
| `address_to`     | string | Yes      | Final destination address |
| `refund_address` | string | Varies   | Refund address. **Required** for engines where `requiresRefund` is true. |
| `address_memo`   | string | No       | Memo/tag for destination address |
| `refund_memo`    | string | No       | Memo/tag for refund address |
| `ref`            | string | No       | Referral code |

**Example:**

```json
{
  "engine": "houdini",
  "from_currency": "eth",
  "from_network": "Mainnet",
  "to_currency": "btc",
  "to_network": "Mainnet",
  "amount_from": 1,
  "address_to": "bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh"
}
```

**Response (array of trade legs):**

```json
[
  {
    "id": "leg1-id",
    "status": "WAITING",
    "engine": "houdini",
    "fromTicker": "ETH",
    "toTicker": "XMR",
    "depositAddress": "0xabc...",
    "depositAmount": 1,
    "toAmount": 6.5,
    "createdAt": "2026-03-15T10:00:00Z"
  },
  {
    "id": "leg2-id",
    "status": "WAITING",
    "engine": "houdini",
    "fromTicker": "XMR",
    "toTicker": "BTC",
    "depositAddress": "48vKMSzWMF9b...",
    "depositAmount": 6.5,
    "toAmount": 0.038,
    "createdAt": "2026-03-15T10:00:00Z"
  }
]
```

Only the first leg requires your deposit. The second leg is automatically triggered when the first completes.

---

## Network Names

Use these normalized network names in all API calls:

| Network          | Value       | Used For |
|------------------|-------------|----------|
| Native chains    | `Mainnet`   | BTC, XMR, ETH (native), LTC, DOGE, XRP, BCH, ADA, XLM, SOL, BNB, TRX |
| Ethereum ERC-20  | `Ethereum`  | USDT, USDC, DAI on Ethereum |
| Tron TRC-20      | `TRC20`     | USDT, USDC on Tron |
| BNB Smart Chain  | `BSC`       | BEP-20 tokens |
| Solana SPL       | `Solana`    | SPL tokens |
| Polygon          | `Polygon`   | Polygon tokens |
| Arbitrum         | `Arbitrum`  | Arbitrum tokens |
| Base             | `Base`      | Base tokens |
| Optimism         | `Optimism`  | Optimism tokens |
| Avalanche C-Chain| `Avalanche` | Avalanche tokens |

---

## KYC & Logging Ratings

Providers are rated on two axes. Use these to filter for your privacy needs:

**KYC Rating** (`kyc` param): How much identity verification is required.

| Grade | Meaning |
|-------|---------|
| `A`   | No KYC at all |
| `B`   | Light KYC (email or IP-based limits) |
| `C`   | Moderate KYC (may require ID for larger amounts) |
| `D`   | Any (no filter) |

**Logging Policy** (`log` param): How much transaction data the provider retains.

| Grade | Meaning |
|-------|---------|
| `A`   | No logs / fully private |
| `B`   | Minimal logs |
| `C`   | Any (no filter) |

For maximum privacy, use `kyc=A&log=A`.

---

## Common Workflows

### Standard Swap (Estimate, Create, Poll)

```
Step 1: Get quotes
  GET /v2/exchange/estimate?from=btc&to=xmr&amount=0.5

Step 2: Pick the best route and create the trade
  POST /v2/exchange/create
  {
    "engine": "<route.engine>",
    "provider": "<route.provider>",
    "from_currency": "btc",
    "to_currency": "xmr",
    "amount_from": 0.5,
    "address_to": "<user_xmr_address>"
  }

Step 3: Send crypto to the depositAddress from the response

Step 4: Poll status until FINISHED
  GET /v2/exchange/status/<trade_id>?engine=<engine>
```

### Privacy Bridge (Ghost Protocol)

```
Step 1: Get bridge quotes
  GET /v2/exchange/bridge/estimate?from=eth&to=btc&amount=2

Step 2: Create the bridge (picks a route)
  POST /v2/exchange/bridge/create
  {
    "engine": "<route.engine>",
    "from_currency": "eth",
    "to_currency": "btc",
    "amount_from": 2,
    "address_to": "<user_btc_address>",
    "refund_address": "<user_eth_address>"
  }

Step 3: Send crypto to the first leg's depositAddress

Step 4: Poll both trade legs
  GET /v2/exchange/status/<leg1_id>?engine=<engine>
  GET /v2/exchange/status/<leg2_id>?engine=<engine>
```

### Rate Comparison

```
# Compare all providers for 1000 USDT (TRC20) -> BTC
GET /v2/exchange/estimate?from=usdt&from_net=TRC20&to=btc&to_net=Mainnet&amount=1000

# Compare only no-KYC providers
GET /v2/exchange/estimate?from=usdt&from_net=TRC20&to=btc&to_net=Mainnet&amount=1000&kyc=A&log=A
```

---

## Error Handling

All errors return JSON with an `error` field:

```json
{ "error": "Invalid amount" }
```

| HTTP Code | Meaning |
|-----------|---------|
| 400       | Bad request (missing/invalid params) |
| 404       | Trade or resource not found |
| 500       | Provider or server error |

When the estimate endpoint has no available routes, it returns:

```json
{ "routes": [], "amount_to": 0 }
```

---

## Tips for AI Agents

- **Always estimate first.** Do not hardcode provider names; they change. Use the estimate response to get the current best `engine` and `provider`.
- **Respect minimums.** Check `minimum` from the currencies endpoint before attempting a swap.
- **Poll with backoff.** When checking status, poll every 15-30 seconds. Most swaps complete in 5-30 minutes.
- **Handle memo coins.** XRP, XLM, and some others require a `depositMemo`. Always check the create response for `depositMemo` and include it in the deposit transaction.
- **Validate addresses before creating trades.** Use the `/v2/exchange/validate` endpoint to avoid failed trades.
- **Use the `engine` param on status checks** for faster lookups when you know which engine handled the trade.
