# x402 Protocol

HTTP-native payment protocol that enables API monetization via blockchain.

## How It Works

The x402 protocol extends HTTP with a two-phase payment flow using status code `402 Payment Required`:

```
Phase 1: Discovery
  Client  ──GET /resource──>  Server
  Client  <──HTTP 402──      Server (with payment requirements)

Phase 2: Payment
  Client  ──GET /resource──>  Server
           + PAYMENT-SIGNATURE header (signed payment)
  Client  <──HTTP 200──      Server (with resource + PAYMENT-RESPONSE header)
```

## Payment Requirements (402 Response)

When a server returns 402, the response body contains an `accepts` array:

```json
{
  "accepts": [
    {
      "scheme": "exact",
      "namespace": "evm",
      "networkId": "eip155:56",
      "asset": "USDT",
      "tokenAddress": "0x55d398326f99059fF775485246999027B3197955",
      "tokenDecimals": 18,
      "amountRequired": "5000000000000000000",
      "payToAddress": "0xRecipient...",
      "resource": "https://api.example.com/callback"
    }
  ],
  "x402Version": 2
}
```

## Payment Signature Header

The client signs an EIP-712 typed data structure and sends it as a Base64-encoded header:

| Protocol Version | Header Name |
|-----------------|-------------|
| v2 (current) | `PAYMENT-SIGNATURE` |
| v1 (legacy) | `X-PAYMENT` |

The signed payload includes:
- `from`: Payer wallet address
- `to`: Recipient address
- `value`: Exact payment amount (unique per order for matching)
- `validAfter` / `validBefore`: Time window for payment validity
- `nonce`: Random value for replay protection

## Payment Response Header

On success, the server returns a `PAYMENT-RESPONSE` header (Base64-encoded):

```json
{
  "txHash": "0xabc...def",
  "networkId": "eip155:56"
}
```

## Key Concepts

### Unique Amount Matching
The server generates a slightly adjusted unique amount for each order (e.g., $5.000001 instead of $5.00). This allows the server to match incoming payments to specific orders via Redis cache lookup, without requiring an order ID in the payment header.

### Facilitator
An intermediary service that:
1. Verifies the signed payment is valid
2. Submits the transaction on-chain
3. Confirms settlement
4. Returns the transaction hash

### Supported Networks

| Network | Chain ID | Token |
|---------|----------|-------|
| BSC Mainnet | eip155:56 | USDT (BEP-20) |

## Client Libraries

- `@x402/axios` — Axios interceptor, auto-handles 402 responses
- `@x402/fetch` — Fetch API wrapper
- `@x402/evm` — EVM signing utilities (EIP-712)
