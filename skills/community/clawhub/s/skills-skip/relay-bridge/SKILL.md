---
name: relay-bridge
description: |
  Cross-chain bridge using Relay API. Bridge tokens between 20+ blockchains instantly.
  
  Features:
  - Instant bridging between EVM chains
  - Support for 20+ chains (ETH, ARB, OPT, BASE, AVAX, POL, etc.)
  - Quote fetching before execution
  - Status tracking
  
  Use when: user wants to bridge tokens across chains.
metadata:
  openclaw:
    emoji: 🌉
    requires:
      bins: ["python3", "curl"]
      env: 
        - RELAY_API_KEY
    startup:
      type: "manual"
---

# Relay Bridge 🌉

Cross-chain bridging skill using Relay API.

## Setup

### Get API Key

1. Go to https://relay.link/bridge
2. Sign up / Connect wallet
3. Get API key from dashboard

### Environment

```bash
RELAY_API_KEY=your_relay_api_key
```

## Supported Chains

| Chain ID | Chain Name |
|----------|------------|
| 1 | Ethereum |
| 42161 | Arbitrum |
| 10 | Optimism |
| 8453 | Base |
| 43114 | Avalanche |
| 137 | Polygon |
| 56 | BNB Chain |
| 250 | Fantom |
| 100 | Gnosis |
| 11155111 | Sepolia (testnet) |

## Usage

### Get Quote

```bash
# Bridge ETH from Ethereum to Arbitrum
relay_quote --from 1 --to 42161 --amount 0.1 --token ETH
```

### Execute Bridge

```bash
# Execute bridge
relay_bridge --from 1 --to 42161 --amount 0.1 --token ETH --recipient 0x...
```

## API Reference

### Get Quote (v2)

```bash
curl -X POST "https://api.relay.link/quote/v2" \
  -H "Content-Type: application/json" \
  -H "x-relay-api-key: YOUR_API_KEY" \
  -d '{
    "user": "0x...",
    "recipient": "0x...",
    "originChainId": 1,
    "destinationChainId": 42161,
    "originCurrency": "0x0000000000000000000000000000000000000000",
    "destinationCurrency": "0x0000000000000000000000000000000000000000",
    "amount": "100000000000000000",
    "tradeType": "EXACT_INPUT"
  }'
```

### Execute

```bash
curl -X POST "https://api.relay.link/execute" \
  -H "Content-Type: application/json" \
  -H "x-relay-api-key: YOUR_API_KEY" \
  -d '{"quote": {...}, "user": "0x...", "recipient": "0x..."}'
```

## Functions

### get_quote(from_chain, to_chain, token, amount, from_address)

Returns bridge quote with:
- Estimated arrival time
- Gas fees
- Bridge fees
- Route details

### execute_bridge(quote_id, to_address)

Executes bridge transaction.

### get_status(transaction_hash)

Returns bridge transaction status.

## Example Response

```json
{
  "quoteId": "quote_123...",
  "fromChainId": 1,
  "toChainId": 42161,
  "fromToken": "ETH",
  "toToken": "ETH",
  "amountIn": "0.1",
  "amountOut": "0.0995",
  "estimatedArrival": 180,
  "fees": {
    "bridgeFee": "0.001",
    "gasEstimate": "0.002"
  }
}
```

## Safety

⚠️ Always verify quote before executing. Bridge times vary by chain congestion.
