---
name: check-balance
description: >
  Check wallet USDC and USDT balances across all supported chains via the
  Rozo balance API. Supports EVM wallets (Ethereum, Arbitrum, Base, BSC,
  Polygon), Solana, and Stellar (G-wallet and C-wallet). Use when user
  says "check balance", "how much do I have", "show my balance", "wallet
  balance", or "what's my USDC balance". Auto-detects chain from address.
metadata:
  author: rozo
  version: 0.1.0
---

# Check Wallet Balance

## Instructions

Fetch all USDC and USDT balances for a wallet address using the Rozo balance API.

### Step 1: Get the wallet address

The user provides their wallet address. If not provided, ask:
> "What is your wallet address?"

### Step 2: Fetch balances

```bash
node scripts/dist/check-balance.js --address <wallet_address>
```

The API auto-detects chain type from the address format:
- `0x...` (42 chars) → EVM — returns balances across Ethereum, Arbitrum, Polygon, BSC, Base
- Base58 (32-44 chars) → Solana — returns USDC and USDT balances
- `G...` or `C...` (56 chars) → Stellar — returns USDC balance

### Step 3: Present results

Display balances in a clear table format:

```
Wallet: 0xa9E3...567dB (EVM)

| Chain    | USDC      | USDT     |
|----------|-----------|----------|
| Ethereum | 1,155.83  | 53.63    |
| Arbitrum | 9.86      | 6.45     |
| Polygon  | 37.75     | 0.00     |
| BSC      | 1.61      | 22.74    |
| Base     | 100.81    | —        |
```

## Examples

### Example 1: EVM wallet
User: "Check my balance for 0xa9E3Da13EF5eADFC6EcB2BB6BDddE95016B567dB"

1. Fetch → display all USDC/USDT across EVM chains

### Example 2: Solana wallet
User: "What's my balance?" (wallet known from context)

1. Fetch → display USDC and USDT on Solana

### Example 3: Stellar wallet
User: "Show balance for GC56BXCNEWL6JSGKHD3RJ5HJRNKFEJQ53D3YY3SMD6XK7YPDI75BQ7FD"

1. Fetch → display USDC on Stellar
