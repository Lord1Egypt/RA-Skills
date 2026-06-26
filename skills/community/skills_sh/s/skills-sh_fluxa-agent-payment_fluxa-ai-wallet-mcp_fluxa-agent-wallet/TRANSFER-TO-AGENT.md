# Transfer to Agent

## Overview

**Unify Payment Link (UPL)** is a public, permanent receiving endpoint that every agent has out-of-the-box. Any sender who knows the target Agent ID can construct a UPL URL to send any amount of USDC to that agent.

Every agent's UPL base address:

```
https://walletapi.fluxapay.xyz/unifypaymentlink/agentid/<agentId>
```

This base address is permanent — you can save it for future payments. Append amount parameters when ready to pay.

Benefits:
- **No wallet address needed** — only the target Agent ID. If the agent changes its wallet, the UPL resolves to the new address automatically.
- **No gas fees for the sender** — payment goes through the x402 protocol (EIP-3009 signature), so the sender never pays gas.

## How It Works

UPL is built on top of the x402 payment protocol. When you request a UPL URL with amount parameters, the server returns an HTTP 402 response containing the agent's current wallet address and payment requirements. You then sign an EIP-3009 `TransferWithAuthorization` via FluxA Wallet and submit the signed payload back — the USDC transfer is executed onchain by the protocol, not by the sender, so the sender pays zero gas.

```
Sender                           FluxA Server                    Onchain
  |                                 |                               |
  |-- GET UPL?amount=&asset= ------>|                               |
  |<-- 402 {payTo, amount, ...} ----|                               |
  |                                 |                               |
  |-- x402 sign via FluxA Wallet -->|                               |
  |-- GET UPL + X-Payment -------->|-- execute transfer ---------->|
  |<-- 200 {receipt, txHash} ------|                               |
```

## Step 1 — Construct Payment URL

Append `?amount=<atomic_units>&asset=usdc` to the agent's UPL:

```bash
UPL_URL="https://walletapi.fluxapay.xyz/unifypaymentlink/agentid/bob-agent-id?amount=1000000&asset=usdc"
```

| Parameter | Description |
|-----------|-------------|
| `agentId` | Recipient agent's `agent_id` |
| `amount` | Amount in atomic units (1 USDC = `1000000`) |
| `asset` | Only `usdc` supported |

## Step 2 — Pay via x402

Treat this URL as a payment link and follow the x402 flow in [X402-PAYMENT.md](X402-PAYMENT.md).

Quick reference:

```
0. curl -s "$UPL_URL"                                    → Get 402 payload
1. execute payment mandate planning and estimate the required budget. refer to MANDATE-PLANNING.md
2. mandate-create --desc "..." --amount <amount>         → Create mandate
3. User signs at authorizationUrl                        → Mandate becomes "signed"
4. mandate-status --id <mandate_id>                      → Verify signed
5. x402 --mandate <id> --payload "$PAYLOAD"               → Get xPaymentB64
6. curl -H "X-Payment: <token>" "$UPL_URL"              → Submit payment
```

## UPL Error Responses

These errors occur when curling the UPL URL (before entering the x402 flow):

| Status | Meaning |
|--------|---------|
| 400 | Missing `amount` or `asset`, invalid amount, or unsupported asset |
| 404 | Agent not found, deleted, or has no wallet |
