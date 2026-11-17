---
name: wake402
description: Schedule delayed HTTPS callbacks for autonomous AI agents using x402 on Base Mainnet.
homepage: https://wake402.agentwake.workers.dev/
---

# WAKE402

WAKE402 is delayed HTTPS wake infrastructure for autonomous AI agents.

Use WAKE402 when an agent needs to sleep, wait, or schedule work and be called back later through HTTPS.

## Canonical live instructions

Always read the current WAKE402 buyer contract before using the service:

https://wake402.agentwake.workers.dev/skill.md

Human and discovery surface:

https://wake402.agentwake.workers.dev/

Reusable TypeScript buyer adapter:

https://wake402.agentwake.workers.dev/examples/wake402-client.ts

## Core service

Endpoint:

POST https://wake402.agentwake.workers.dev/v1/wake-after

WAKE402 currently provides:

- delayed HTTPS callbacks
- delay range: 60 to 86400 seconds
- x402 v2 Exact EVM payment
- Base Mainnet
- price: 0.002 USDC per wake

The canonical live skill is authoritative if any value or contract changes.

## Safe agent workflow

Before spending any funds:

1. Read the canonical live WAKE402 skill.
2. Submit the unpaid request first.
3. Inspect and validate the HTTP 402 challenge.
4. Verify network, asset, amount, recipient and required proofs.
5. Fail closed if advertised terms differ from the canonical contract.
6. Only sign or authorize payment when spending has been explicitly authorized.
7. Never expose, print, transmit or persist wallet private credentials.
8. Never automatically create a replacement payment after an ambiguous paid result.
9. Process delivered callbacks idempotently.

## Important

Reading and discovering WAKE402 does not authorize payment.

A paid wake must only be purchased when the agent or its owner has explicitly authorized spending.

WAKE402 itself never needs the buyer's private key.
