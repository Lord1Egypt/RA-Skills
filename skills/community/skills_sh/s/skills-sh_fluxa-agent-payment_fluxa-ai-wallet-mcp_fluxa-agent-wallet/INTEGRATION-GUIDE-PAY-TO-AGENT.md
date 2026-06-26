# Integration Guide — Pay to Agent

## Overview

When your service needs to send USDC to an AI agent (rewards, refunds, settlements, etc.), use the agent's **Unify Payment Link (UPL)**.

**UPL** is a public, permanent receiving endpoint that every agent has out-of-the-box. It acts as the agent's stable payment address — you only need to know the Agent ID, not the wallet address. If the agent changes their wallet, the UPL automatically resolves to the new address.

## How It Works

When you request a UPL with amount parameters, FluxA Server returns an HTTP 402 response containing the agent's current wallet address and payment requirements. You then sign an EIP-3009 `TransferWithAuthorization` via FluxA Wallet and submit the signed payload back. The USDC transfer is executed onchain by the protocol, not by the sender — so the sender pays zero gas.

```
Your Service                     FluxA Server                    Onchain
  |                                 |                               |
  |-- GET UPL?amount=&asset= ------>|                               |
  |<-- 402 {payTo, amount, ...} ----|                               |
  |                                 |                               |
  |-- x402 sign via FluxA Wallet -->|                               |
  |-- GET UPL + X-Payment -------->|-- execute transfer ---------->|
  |<-- 200 {receipt, txHash} ------|                               |
```

## Usage

### Step 1 — Save the Agent's UPL

When an agent registers with your service, save their UPL base address:

```
https://walletapi.fluxapay.xyz/unifypaymentlink/agentid/<agentId>
```

This is a permanent URL — save it once, use it for all future payments to this agent.

### Step 2 — Pay When Needed

When you need to pay the agent, append `?amount=<atomic_units>&asset=usdc` to the saved UPL and follow the x402 payment flow:

```bash
UPL_URL="https://walletapi.fluxapay.xyz/unifypaymentlink/agentid/agent-abc123?amount=5000000&asset=usdc"
```

For the complete x402 payment steps, see [TRANSFER-TO-AGENT.md](TRANSFER-TO-AGENT.md).
