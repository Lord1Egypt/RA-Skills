---
name: usdc-dance-evvm-payment
description: Pay with USDC Krump (USDC.k) via x402 on Story Aeneid EVVM. Supports EVVM Native adapter (no EIP-3009 on token) and legacy Bridge adapter. Requires PRIVY_APP_ID and PRIVY_APP_SECRET (or private key for legacy path); credentials are user-supplied, not stored by the skill.
version: 1.2.0
author: OpenClaw USDC Krump
tags: [payment, evvm, x402, usdc, layerzero, story-aeneid, openclaw, privy, bridge, usdc-krump]
requires: [privy]
---

# USDC Krump (USDC.k) EVVM Payment Skill

Enables OpenClaw agents to pay with **USDC Krump (USDC.k)** via the **x402 protocol** on **Story Aeneid EVVM**, using **Privy server wallets** or a private key.

## Scope

This skill provides **instructions and parameter reference** for USDC Krump (USDC.k) payments via x402 on Story Aeneid. Executable code, examples, and scripts (e.g. EVVM deposit, two-agent flows) live in the full [USDC Krump repository](https://github.com/arunnadarasa/usdckrump); use that repo to run scripts or integrate the payment logic. Only create wallets or initiate payments when the user has **explicitly requested** a payment and the required credentials are configured.

## Required credentials

The skill **does not store or provide** credentials. You must supply one of:

- **Privy (recommended):** Set `PRIVY_APP_ID` and `PRIVY_APP_SECRET` (e.g. in `~/.openclaw/openclaw.json` under `env.vars`, or as environment variables). Get these from [dashboard.privy.io](https://dashboard.privy.io).
- **Legacy / private key:** For the legacy `payViaEVVM` path, the payer private key must be supplied (e.g. `AGENT_PRIVATE_KEY`). Prefer Privy-managed wallets over raw private keys; do not store private keys in plain environment variables if avoidable.

## Features

- ✅ **Privy Integration**: Privy server wallets for autonomous agent transactions
- ✅ **x402 Protocol**: EIP-3009-style auth; **EVVM Native adapter** (Core internal balances) or legacy adapter (EIP-3009 on token)
- ✅ **EVVM Integration**: Payment routing through EVVM Core (ID 1140)
- ✅ **EVVM Deposit**: Script to deposit USDC.k into EVVM Treasury so payers have internal balance for Native adapter
- ✅ **Two-Agent Examples**: Direct x402, legacy adapter, and **native adapter** (`two-agents-x402-native.ts`)
- ✅ **Policy-Based Security**: Privy policies for spending limits and guardrails
- ✅ **Receipt Tracking**: `checkPaymentStatus(receiptId, adapterAddress, rpcUrl)`

## Prerequisites

1. **Privy account** (for Privy path): Get credentials from [dashboard.privy.io](https://dashboard.privy.io).
2. **Privy skill installed**: `clawhub install privy`
3. **OpenClaw config**: Add the required credentials (see **Required credentials** above). For Privy, add to `~/.openclaw/openclaw.json`:

```json
{
  "env": {
    "vars": {
      "PRIVY_APP_ID": "your-app-id",
      "PRIVY_APP_SECRET": "your-app-secret"
    }
  }
}
```

## Quick Start

### EVVM deposit before using Native adapter

EVVM Core moves **internal ledger balances**; it does not pull tokens from the wallet. For the **EVVM Native x402 adapter**, the payer must deposit USDC.k into EVVM first. **Run this in the full USDC Krump repo** (clone from [github.com/arunnadarasa/usdckrump](https://github.com/arunnadarasa/usdckrump)):

```bash
cd lz-bridge
PRIVATE_KEY=0x<payer_key> DEPOSIT_AMOUNT=1000000 npm run evvm:deposit-usdck
```

Then use `useNativeAdapter: true` and the Native adapter address below.

### Option 1: Using Privy Wallet (Recommended)

Code reference (implement in your environment or use the full repo’s `src/`):

```typescript
import { payViaEVVMWithPrivy } from './src/index';

// EVVM Native adapter (no EIP-3009 on token; payer must have deposited USDC.k via Treasury)
const receipt = await payViaEVVMWithPrivy({
  walletId: 'privy-wallet-id',
  to: recipientAddress,
  amount: '1000000', // 1 USDC.k (6 decimals)
  receiptId: 'payment_123',
  adapterAddress: '0xDf5eaED856c2f8f6930d5F3A5BCE5b5d7E4C73cc', // EVVM Native x402 adapter
  usdcDanceAddress: '0xd35890acdf3BFFd445C2c7fC57231bDE5cAFbde5', // USDC.k (BridgeUSDC)
  evvmCoreAddress: '0xa6a02E8e17b819328DDB16A0ad31dD83Dd14BA3b',
  evvmId: 1140,
  rpcUrl: 'https://aeneid.storyrpc.io',
  useNativeAdapter: true,
});
```

### Option 2: Using Private Key (Legacy)

Code reference (use the full repo’s `src/` when running):

```typescript
import { payViaEVVM } from './src/index';

const receipt = await payViaEVVM({
  from: agentAddress,
  to: recipientAddress,
  amount: '1000000',
  receiptId: 'payment_123',
  privateKey: agentPrivateKey,
  adapterAddress: '0xDf5eaED856c2f8f6930d5F3A5BCE5b5d7E4C73cc', // Native adapter
  usdcDanceAddress: '0xd35890acdf3BFFd445C2c7fC57231bDE5cAFbde5',
  evvmCoreAddress: '0xa6a02E8e17b819328DDB16A0ad31dD83Dd14BA3b',
  evvmId: 1140,
  rpcUrl: 'https://aeneid.storyrpc.io',
  useNativeAdapter: true,
});
```

### Two-agent native example

In the **full USDC Krump repo**, run:

```bash
AGENT_A_PRIVATE_KEY=0x... AGENT_B_ADDRESS=0x... npx tsx examples/two-agents-x402-native.ts
```

See the repo’s `examples/README-two-agents-x402.md` for direct x402 and legacy adapter flows.

## Configuration

### Required Addresses (Story Aeneid Testnet)

- **EVVM Core**: `0xa6a02E8e17b819328DDB16A0ad31dD83Dd14BA3b`
- **EVVM ID**: `1140`
- **USDC.k (BridgeUSDC)**: `0xd35890acdf3BFFd445C2c7fC57231bDE5cAFbde5`
- **EVVM Native x402 adapter**: `0xDf5eaED856c2f8f6930d5F3A5BCE5b5d7E4C73cc` — use with `useNativeAdapter: true` (payer must deposit USDC.k via Treasury first)
- **Bridge EVVM adapter (legacy)**: `0x00ed0E80E5EAE285d98eC50236aE97e2AF615314` — EIP-3009 on token

### Network Details

- **Chain**: Story Aeneid Testnet
- **Chain ID**: `1315`
- **Native Currency**: IP
- **RPC**: `https://aeneid.storyrpc.io`

## Privy Integration

This skill integrates with the [Privy OpenClaw skill](https://docs.privy.io/recipes/agent-integrations/openclaw-agentic-wallets) to enable:

- **Autonomous Wallet Management**: Agents have their own Privy server wallets
- **Policy-Based Security**: Use Privy policies to limit spending, restrict chains, or whitelist contracts
- **No Private Key Storage**: Privy handles key management securely
- **Transaction Signing**: Privy signs EIP-3009 and EIP-191 signatures via API

### Creating a Privy Wallet for Your Agent

Ask your OpenClaw agent:

> "Create an Ethereum wallet for yourself using Privy on Story Aeneid testnet"

The agent will create a Privy server wallet and return the wallet ID.

### Setting Up Policies

Create spending limits and restrictions:

> "Create a Privy policy that limits USDC Krump (USDC.k) payments to 10 USDC.k max per transaction"

> "Attach the spending limit policy to my Privy wallet"

## Functions

### `payViaEVVMWithPrivy(options)`

Process a payment through EVVM using x402 protocol with Privy wallet.

**Parameters:**
- `walletId`, `to`, `toIdentity`, `amount`, `receiptId`, `adapterAddress`, `usdcDanceAddress`, `evvmCoreAddress`, `evvmId`, `rpcUrl` (see Option 1 example)
- `useNativeAdapter`: Set `true` for EVVM Native x402 adapter (payer must have deposited USDC.k via Treasury first)
- `privyAppId`, `privyAppSecret`: Optional; use env vars if not provided

**Returns:** Transaction receipt

### `payViaEVVM(options)` (Legacy)

Process payment using private key directly (not recommended for production).

### `checkPaymentStatus(receiptId, adapterAddress, rpcUrl)`

Check if a payment was successfully processed.

## Examples

In the **full [USDC Krump repository](https://github.com/arunnadarasa/usdckrump)**, see the `examples/` directory:

- `two-agents-x402-native.ts` — Two agents with EVVM Native adapter (recommended)
- `two-agents-x402-simulation.ts` — Two agents with legacy Bridge adapter
- `two-agents-x402-direct.ts` — Direct x402 transfer (no EVVM)
- `agent-payment-privy-example.ts` — Privy wallets
- `agent-payment-example.ts` — Private keys (legacy)

See the repo’s `examples/README-two-agents-x402.md` for the EVVM deposit step and all flows.

## Security Considerations

Credentials are **user-supplied only**; this skill does not store or transmit secrets. Only create wallets or initiate payments when the user has **explicitly requested** a payment and you have configured the required credentials (see **Required credentials**).

⚠️ **When using Privy wallets:**

1. **Set policies**: Always configure spending limits and restrictions (e.g. max per transaction, whitelisted chains/contracts).
2. **Test first**: Use testnet and minimal amounts before any mainnet or real funds.
3. **Monitor activity**: Regularly check wallet activity in the Privy dashboard.
4. **Rotate credentials**: If compromised, rotate Privy App Secret immediately.
5. **Prefer Privy over raw keys**: Prefer Privy-managed wallets over supplying a private key; avoid storing private keys in plain environment variables.

## Requirements

- Node.js 18+, ethers.js v6 (when running code from the full repo)
- Privy skill installed: `clawhub install privy`
- Access to Story Aeneid RPC endpoint
- Required credentials: `PRIVY_APP_ID` and `PRIVY_APP_SECRET` (Privy path), or payer private key (legacy path)

## License

MIT
