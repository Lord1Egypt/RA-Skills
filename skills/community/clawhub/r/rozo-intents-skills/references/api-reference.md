# Rozo API Reference

Base URL: `https://intentapiv4.rozo.ai/functions/v1/payment-api`

**Authentication:** None required. All endpoints are public and rate-limited.

## Create Payment

**POST** `/payment-api/`

### Request Body

```json
{
  "appId": "rozoAgent",
  "orderId": "optional-unique-id",
  "type": "exactOut",
  "display": {
    "title": "Payment",
    "description": "optional description",
    "currency": "USD"
  },
  "source": {
    "chainId": 8453,
    "tokenSymbol": "USDC",
    "tokenAddress": "0x833589fcd6edb6e08f4c7c32d4f71b54bda02913",
    "amount": "10.00"
  },
  "destination": {
    "chainId": 1500,
    "receiverAddress": "GC56BX...",
    "receiverMemo": "optional-for-stellar",
    "tokenSymbol": "USDC",
    "tokenAddress": "USDC:GA5ZSEJYB37JRC5AVCIA5MOP4RHTM335X2KGX3IHOJAPP5RE34K4KZVN",
    "amount": "10.00"
  },
  "webhookUrl": "optional-callback-url",
  "metadata": {}
}
```

### Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| appId | string | Yes | Always `rozoAgent` |
| orderId | string | No | Unique order reference for idempotency |
| type | enum | No | `exactIn` (fee from input) or `exactOut` (fee added to input, default) |
| display.title | string | Yes | Payment title |
| display.description | string | No | Payment description |
| display.currency | string | Yes | Display currency, use `USD` |
| source.chainId | integer | Yes | Source chain ID |
| source.tokenSymbol | enum | Yes | `USDC` or `USDT` |
| source.tokenAddress | string | No | Token contract address |
| source.amount | string | No | Required for `exactIn` type |
| destination.chainId | integer | Yes | Destination chain ID |
| destination.receiverAddress | string | Yes | Recipient wallet address |
| destination.receiverMemo | string | No | Required for Stellar memo-based payments |
| destination.tokenSymbol | enum | Yes | `USDC` or `USDT` |
| destination.tokenAddress | string | No | Token contract address |
| destination.amount | string | No | Required for `exactOut` type |

### Payment Types

- **exactOut** (default): Recipient receives the exact amount. Fee is added to the source amount.
- **exactIn**: Source sends exact amount. Fee is deducted, recipient gets less.

### Response (201 Created)

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "appId": "rozoAgent",
  "status": "payment_unpaid",
  "type": "exactOut",
  "createdAt": "2024-01-01T00:00:00Z",
  "expiresAt": "2024-01-01T01:00:00Z",
  "source": {
    "chainId": 8453,
    "tokenSymbol": "USDC",
    "amount": "10.50",
    "receiverAddress": "0x_DEPOSIT_ADDRESS_HERE",
    "fee": "0.50"
  },
  "destination": {
    "chainId": 1500,
    "receiverAddress": "GC56BX...",
    "tokenSymbol": "USDC",
    "amount": "10.00"
  }
}
```

Key response fields:
- `source.receiverAddress` — the deposit address where the user sends funds
- `source.receiverMemo` — memo if required (Stellar)
- `source.fee` — the fee amount
- `expiresAt` — payment must be funded before this time

### Errors

- **400** — Invalid request (bad parameters)
- **409** — Duplicate orderId conflict

## Get Payment

**GET** `/payments/{paymentId}`

### Path Parameters

| Parameter | Type | Required |
|-----------|------|----------|
| paymentId | string (UUID) | Yes |

### Response (200)

Same schema as Create Payment response.

### Payment Statuses

| Status | Description |
|--------|-------------|
| payment_unpaid | Created, awaiting funding |
| payment_started | Funding detected, processing |
| payment_payin_completed | Source funds received |
| payment_payout_completed | Destination funds sent |
| payment_completed | Fully complete |
| payment_bounced | Payout failed |
| payment_expired | Not funded in time |
| payment_refunded | Funds returned to sender |

## Check Payment by Source

**GET** `/payments/check`

Lookup a payment by source transaction hash or deposit address+memo instead of payment ID. Searches the last 7 days and returns the most recent match.

### Query Parameters

Provide **either** `txHash` **or** both `receiverAddress` + `receiverMemo`:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| txHash | string | Either this... | Source chain transaction hash (Stellar, EVM, Solana) |
| receiverAddress | string | ...or both of these | Deposit address |
| receiverMemo | string | | Memo associated with the deposit address |

### Response (200)

Same schema as Get Payment response.

### Errors

- **400** — Missing required params (need `txHash` or both `receiverAddress` + `receiverMemo`)
- **404** — No matching payment in last 7 days

## Stellar Contract Payments

For Stellar C-wallet destinations, the API uses `stellar_payin_contracts` intent:

1. Create payment as normal with C-wallet as destination
2. Response includes `receiverAddressContract` and `receiverMemoContract`
3. User invokes the Soroban contract's `pay()` function with amount and memo
4. System monitors the contract for payment
5. Cross-chain payout triggers once payment is detected
