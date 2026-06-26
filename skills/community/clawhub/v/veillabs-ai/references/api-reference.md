# OpenClaw Skill — Veillabs API

This document is a complete reference for creating an **OpenClaw Skill** that integrates the entire Veillabs API. It includes a ready-to-use SKILL.md template, full endpoint documentation, and example workflows.

---

## 1. SKILL.md Format (Ready-to-Use Template)

Create a `SKILL.md` file in your OpenClaw skill directory:

```markdown
---
name: veillabs
description: >
  Interact with Veillabs privacy-focused DEX API for cross-chain swaps,
  private seed distributions, and transaction tracking.
metadata:
  openclaw:
    version: "1.0.0"
    emoji: "🔒"
    homepage: "https://trade.veillabs.app"
    user-invocable: true
    requires:
      env:
        - VEILLABS_BASE_URL
      config:
        - veillabs.enabled
---

# Veillabs Privacy DEX Skill

You are a Veillabs API integration assistant. Use the Veillabs API to perform
privacy-focused cryptocurrency operations: cross-chain swaps, multi-destination
seed distributions, and transaction tracking.

## Context

Veillabs is a privacy-focused decentralized exchange (DEX) platform. It provides:
- **Private Swap**: One-to-one cross-chain token swap
- **Private Seed**: Multi-destination distribution (split funds to multiple wallets)
- **Tracking**: Real-time transaction status monitoring

Base URL is read from `VEILLABS_BASE_URL` environment variable.
All requests and responses use `application/json`.
No authentication required (privacy-first platform).

## Instructions

### Checking Supported Tokens
1. Call `GET /api/currencies` to list all supported tokens
2. Call `GET /api/pairs/{ticker}/{network}` to check valid swap pairs
3. Call `GET /api/ranges?...` to get min/max limits for a swap pair
4. Call `GET /api/estimates?...` to get the estimated output amount

### Creating a Swap
1. Validate the pair using `/api/pairs` and `/api/ranges`
2. Get an estimate via `/api/estimates`
3. Create the swap via `POST /api/exchanges`
4. Track progress via `GET /api/tracking/{id}`

### Creating a Private Seed Distribution
1. Validate all destination splits meet minimum amounts
2. Create via `POST /api/seed/create`
3. Track intake via `GET /api/tracking/{id}`
4. Track distribution via `GET /api/seed/status/{id}`

### Getting Platform Stats
1. Call `GET /api/volume` for real-time volume data

## Error Handling
- 400: Bad Request (missing fields, below minimum amount)
- 404: Transaction/order not found
- 500: Internal server error (RPC, DB, Redis issues)

Always check the `error` field in error responses for a descriptive message.

## Rules
- ALWAYS validate swap pairs and minimum amounts before creating swaps or seeds.
- ALWAYS use the Veillabs Tracking ID (`V31L...` format) for status polling.
- Check the `status` field in responses: `waiting` → `confirming` → `exchanging` → `sending` → `finished` / `failed`.
```

---

## 2. Comprehensive API Documentation

### Environment Variable

| Variable | Description | Example |
|----------|-------------|---------|
| `VEILLABS_BASE_URL` | Base API URL | `https://trade.veillabs.app/api` or `http://localhost:3000/api` |

---

### 2.1 Market & Token Data

#### `GET /api/currencies`

Fetches the complete list of supported tokens and networks.

**Request:**
```
GET {BASE_URL}/api/currencies
```

**Response** `200 OK`:
```json
[
  {
    "ticker": "btc",
    "network": "btc",
    "name": "Bitcoin",
    "image": "https://...",
    "hasExtraId": false,
    "extraId": null,
    "addressValidationRegex": "...",
    "isFiat": false,
    "supportsFixedRate": true
  }
]
```

---

#### `GET /api/pairs/{ticker}/{network}`

Fetches the list of valid destination tokens based on the source token.

**Request:**
```
GET {BASE_URL}/api/pairs/eth/eth?fixed=false
```

| Path Parameter | Type | Description |
|----------------|------|-------------|
| `ticker` | string | Source token symbol (e.g., `eth`, `btc`) |
| `network` | string | Source token network (e.g., `eth`, `bsc`) |

| Query Parameter | Type | Default | Description |
|-----------------|------|---------|-------------|
| `fixed` | boolean | `false` | If `true`, only returns fixed-rate pairs |

**Response** `200 OK`:
```json
["btc:btc", "usdt:eth", "bnb-bsc:bsc", "usdt:trc20"]
```

---

#### `GET /api/estimates`

Calculates the estimated amount received based on input.

**Request:**
```
GET {BASE_URL}/api/estimates?tickerFrom=eth&networkFrom=eth&tickerTo=btc&networkTo=btc&amount=1.5
```

| Query Parameter | Type | Required | Description |
|-----------------|------|----------|-------------|
| `tickerFrom` | string | ✅ | Source token symbol |
| `networkFrom` | string | ✅ | Source token network |
| `tickerTo` | string | ✅ | Destination token symbol |
| `networkTo` | string | ✅ | Destination token network |
| `amount` | string | ✅ | Amount to swap |

**Response** `200 OK`:
```json
{
  "amountTo": "0.05234",
  "traceId": "abc123..."
}
```

**Response** `400 Bad Request`:
```json
{
  "error": "Amount is below minimum"
}
```

---

#### `GET /api/ranges`

Fetches the minimum and maximum limits for a swap pair.

**Request:**
```
GET {BASE_URL}/api/ranges?tickerFrom=eth&networkFrom=eth&tickerTo=btc&networkTo=btc
```

| Query Parameter | Type | Required | Description |
|-----------------|------|----------|-------------|
| `tickerFrom` | string | ✅ | Source token symbol |
| `networkFrom` | string | ✅ | Source token network |
| `tickerTo` | string | ✅ | Destination token symbol |
| `networkTo` | string | ✅ | Destination token network |

**Response** `200 OK`:
```json
{
  "min": "0.001",
  "max": "50",
  "traceId": "abc123..."
}
```

---

### 2.2 Private Swap

#### `POST /api/exchanges`

Creates a new token swap (one-to-one).

**Request:**
```
POST {BASE_URL}/api/exchanges
Content-Type: application/json
```

**Body:**
```json
{
  "tickerFrom": "eth",
  "networkFrom": "eth",
  "tickerTo": "btc",
  "networkTo": "btc",
  "amount": "0.1",
  "addressTo": "bc1q...",
  "fixed": false
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `tickerFrom` | string | ✅ | Source token symbol |
| `networkFrom` | string | ✅ | Source token network |
| `tickerTo` | string | ✅ | Destination token symbol |
| `networkTo` | string | ✅ | Destination token network |
| `amount` | string | ✅ | Amount sent |
| `addressTo` | string | ✅ | Destination wallet address |
| `fixed` | boolean | ❌ | Fixed (`true`) or floating (`false`) rate |

**Response** `200 OK`:
```json
{
  "id": "V31L-XXXX-XXXX",
  "orderId": "provider-uuid",
  "veilId": "V31L-XXXX-XXXX",
  "status": "waiting",
  "tickerFrom": "eth",
  "networkFrom": "eth",
  "amountFrom": "0.1",
  "addressFrom": "0x_DEPOSIT_ADDRESS",
  "tickerTo": "btc",
  "networkTo": "btc",
  "amountTo": "0.00523",
  "addressTo": "bc1q...",
  "traceId": "abc123..."
}
```

> **Note**: `id` / `veilId` = Veillabs Tracking ID. `orderId` = Provider ID. The user must send funds to `addressFrom`.

---

#### `GET /api/exchanges/{id}`

Fetches swap status directly from the external provider.

**Request:**
```
GET {BASE_URL}/api/exchanges/V31L-XXXX-XXXX
```

| Path Parameter | Type | Description |
|----------------|------|-------------|
| `id` | string | Veillabs ID (`V31L...`) or Provider ID |

**Response** `200 OK`:
```json
{
  "id": "V31L-XXXX-XXXX",
  "orderId": "provider-uuid",
  "status": "exchanging",
  "tickerFrom": "eth",
  "networkFrom": "eth",
  "amountFrom": "0.1",
  "amountTo": "0.00523",
  "addressFrom": "0x...",
  "addressTo": "bc1q...",
  "txFrom": "0x_HASH_INPUT",
  "txTo": "TX_HASH_OUTPUT",
  "traceId": "abc123..."
}
```

---

### 2.3 Private Seed Distribution

#### `POST /api/seed/create`

Creates a multi-destination distribution. Funds are first converted to a pool asset (BNB/BSC or ETH/Base), then distributed to each destination.

**Request:**
```
POST {BASE_URL}/api/seed/create
Content-Type: application/json
```

**Body:**
```json
{
  "tickerFrom": "eth",
  "networkFrom": "eth",
  "tickerTo": "bnb-bsc",
  "networkTo": "bsc",
  "amount": "1.5",
  "destinations": [
    {
      "address": "0xABC...",
      "percentage": 50,
      "ticker": "usdt",
      "network": "bsc"
    },
    {
      "address": "0xDEF...",
      "percentage": 50,
      "ticker": "bnb-bsc",
      "network": "bsc"
    }
  ]
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `tickerFrom` | string | ✅ | Source token symbol |
| `networkFrom` | string | ✅ | Source token network |
| `tickerTo` | string | ✅ | Destination pool token |
| `networkTo` | string | ✅ | Destination pool network |
| `amount` | string | ✅ | Total amount sent |
| `destinations` | array | ✅ | Array of distribution destinations |
| `destinations[].address` | string | ✅ | Destination wallet address |
| `destinations[].percentage` | number | ✅ | Percentage of total (0-100) |
| `destinations[].ticker` | string | ❌ | Final destination token (default: `tickerTo`) |
| `destinations[].network` | string | ❌ | Final destination network (default: `networkTo`) |

**Pool Network Logic:**
- If `networkFrom` is **not** BSC → pool = `bnb-bsc` / `bsc`
- If `networkFrom` **is** BSC → pool = `eth` / `base` (bypass via Base network)

**Response** `200 OK`:
```json
{
  "id": "V31L-XXXX-XXXX",
  "orderId": "provider-uuid",
  "addressFrom": "0x_DEPOSIT_ADDRESS",
  "status": "waiting",
  "amountFrom": "1.5",
  "tickerFrom": "eth",
  "networkFrom": "eth",
  "amountTo": "0.85",
  "tickerTo": "bnb-bsc",
  "networkTo": "bsc",
  "destinations": [
    { "address": "0xABC...", "percentage": 50, "ticker": "usdt", "network": "bsc" },
    { "address": "0xDEF...", "percentage": 50, "ticker": "bnb-bsc", "network": "bsc" }
  ]
}
```

**Response** `400 Bad Request` — Split too small:
```json
{
  "error": "Split too small for USDT (BSC). Estimated: 0.001 BNB-BSC. Required min: 0.01 BNB-BSC. Please increase your total amount or adjust percentages.",
  "destMax": "0.01",
  "failedAddress": "0xABC..."
}
```

**Response** `400 Bad Request` — Below minimum:
```json
{
  "error": "Amount is below minimum. Required: 0.01 ETH",
  "min": "0.01"
}
```

---

#### `GET /api/seed/status/{id}`

Fetches the complete status of a seed distribution, including the status of each destination.

**Request:**
```
GET {BASE_URL}/api/seed/status/V31L-XXXX-XXXX
```

**Response** `200 OK`:
```json
{
  "id": "V31L-XXXX-XXXX",
  "status": "finished",
  "addressFrom": "0x_DEPOSIT_ADDRESS",
  "tickerFrom": "eth",
  "networkFrom": "eth",
  "amountFrom": "1.5",
  "amountTo": "0.85",
  "tickerTo": "bnb-bsc",
  "networkTo": "bsc",
  "txFrom": "0x_INPUT_HASH",
  "txTo": "0x_POOL_HASH",
  "createdAt": "2026-03-24T10:00:00.000Z",
  "destinations": [
    {
      "address": "0xABC...",
      "percentage": 50,
      "status": "finished",
      "amount": "0.425",
      "txFrom": "0x_HASH_1",
      "txTo": "0x_HASH_2"
    },
    {
      "address": "0xDEF...",
      "percentage": 50,
      "status": "processing",
      "amount": "0.425",
      "txFrom": null,
      "txTo": null
    }
  ]
}
```

**Response** `404 Not Found`:
```json
{ "error": "Transaction not found" }
```

---

### 2.5 Universal Tracking

#### `GET /api/tracking/{id}`

Universal tracking for standard swaps and seed distributions (intake side).

**Request:**
```
GET {BASE_URL}/api/tracking/V31L-XXXX-XXXX
```

| Path Parameter | Type | Description |
|----------------|------|-------------|
| `id` | string | Veillabs Tracking ID (`V31L...`) or External Order ID |

**Response** `200 OK`:
```json
{
  "id": "V31L-XXXX-XXXX",
  "orderId": "provider-uuid",
  "status": "exchanging",
  "type": "SWAP",
  "tickerFrom": "eth",
  "networkFrom": "eth",
  "amountFrom": "0.1",
  "tickerTo": "btc",
  "networkTo": "btc",
  "amountTo": "0.00523",
  "addressFrom": "0x_DEPOSIT_ADDRESS",
  "addressTo": "bc1q...",
  "txFrom": "0x_HASH",
  "txTo": null,
  "createdAt": "2026-03-24T10:00:00.000Z",
  "updatedAt": "2026-03-24T10:05:00.000Z",
  "isPrivateSeed": false,
  "destinations": []
}
```

**Response for SEED type:**
```json
{
  "id": "V31L-XXXX-XXXX",
  "orderId": "provider-uuid",
  "status": "finished",
  "type": "SEED",
  "tickerFrom": "eth",
  "networkFrom": "eth",
  "amountFrom": "1.5",
  "tickerTo": "bnb-bsc",
  "networkTo": "bsc",
  "amountTo": "0.85",
  "addressFrom": "0x_DEPOSIT_ADDRESS",
  "addressTo": null,
  "isPrivateSeed": true,
  "destinations": [
    {
      "address": "0xABC...",
      "percentage": 50,
      "status": "finished",
      "ticker": "usdt",
      "network": "bsc",
      "amount": "0.425",
      "txFrom": "0x_HASH_1",
      "txTo": "0x_HASH_2"
    }
  ]
}
```

> **Note**: For `SEED` type, the `addressTo` field is always `null` (pool wallet is hidden from response).

**Response** `404 Not Found`:
```json
{ "error": "Order not found" }
```

---

### 2.6 Platform Stats

#### `GET /api/volume`

Fetches trading platform volume data normalized to USD.

**Request:**
```
GET {BASE_URL}/api/volume
```

**Response** `200 OK`:
```json
{
  "data": {
    "total_volume": 125000.50,
    "total_volume_24h": 5000.00,
    "total_volume_7d": 35000.00,
    "total_volume_30d": 80000.00,
    "total_volume_90d": 120000.00
  }
}
```

> All values are in USD, calculated based on real-time market prices.

---

## 3. Status Lifecycle

### Swap & Seed Intake Status Flow

```
waiting → confirming → exchanging → sending → finished
                                              ↘ failed
```

| Status | Description |
|--------|-------------|
| `waiting` | Waiting for user deposit |
| `confirming` | Deposit detected, waiting for blockchain confirmation |
| `exchanging` | Conversion/swap process is running |
| `sending` | Assets are being sent to destination |
| `finished` | Transaction finished |
| `failed` | Transaction failed |

### Seed Distribution Destination Status

```
waiting → processing → finished
                     ↘ failed
```

## 4. Background Workers (BullMQ)

| Queue | Worker | Description |
|-------|--------|-------------|
| `tracking-status` | Track Worker | Monitors pending order status. When `SEED` is finished, automatically forwards to `seed-distribution` |
| `seed-distribution` | Seed Worker | Handles distribution to each destination (direct transfer or hybrid swap) |


---

## 5. HTTP Status Code

| Code | Description |
|------|-------------|
| `200` | Success |
| `400` | Bad Request — missing fields, below minimum amount, total amount mismatch |
| `404` | Tracking ID / Order ID not found |
| `500` | Server error — database, Redis, or blockchain RPC issues |

---

## 6. Example Workflows for OpenClaw Skill

### Workflow A: Full Private Swap

```
Step 1: GET /api/currencies → Fetch token list
Step 2: GET /api/pairs/eth/eth → Check valid destination tokens
Step 3: GET /api/ranges?tickerFrom=eth&networkFrom=eth&tickerTo=btc&networkTo=btc → Check min/max
Step 4: GET /api/estimates?tickerFrom=eth&networkFrom=eth&tickerTo=btc&networkTo=btc&amount=0.1 → Estimate
Step 5: POST /api/exchanges → Create swap (user must deposit to addressFrom)
Step 6: GET /api/tracking/{id} → Poll status (every 3-5 seconds)
```

### Workflow B: Private Seed Distribution

```
Step 1: GET /api/currencies → Fetch token list
Step 2: GET /api/ranges → Validate minimum amount
Step 3: POST /api/seed/create → Create distribution (user deposits to addressFrom)
Step 4: GET /api/tracking/{id} → Poll intake status
Step 5: GET /api/seed/status/{id} → Poll per-destination distribution (after intake finishes)
```

## 7. Skill Directory Structure (Recommended)

```
veillabs-skill/
├── SKILL.md              # Main file (template in Section 1)
├── scripts/
│   └── veillabs-client.sh  # Helper script for API calls
├── examples/
│   ├── swap-example.json     # Swap request body example
│   └── seed-example.json     # Seed request body example
└── references/
    └── api-reference.md     # Copy of this documentation
```

---

## 8. Implementation Tips

1. **Rate Limiting**: No explicit rate limits, but use `debounce` for status polling (3-5 second intervals).
2. **Polling Pattern**: Use `GET /api/tracking/{id}` to poll. Stop when `status` = `finished` or `failed`.
3. **Error Recovery**: If you receive a `500` status code, retry from scratch.
4. **Seed Validation**: Always validate the minimum amount per split before creating a seed (the API validates it, but a pre-check is better).
