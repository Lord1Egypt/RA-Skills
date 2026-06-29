---
name: subly-pay
description: Fetch a paywalled (HTTP 402) URL and pay for it automatically from the agent wallet's Kamino vault yield, without spending the principal. Use when a request returns 402, when the user asks to buy/access a paid API or resource, or mentions Subly / x402 / yield-funded payment.
version: 0.1.1
metadata:
  openclaw:
    requires:
      bins:
        - node
        - npm
    primaryEnv: SUBLY_DEMO_AGENT_KEYPAIR_PATH
    envVars:
      - name: SUBLY_DEMO_AGENT_KEYPAIR_PATH
        required: true
        description: Path to the agent wallet keypair JSON (create with solana-keygen). The private key never leaves this file.
      - name: SUBLY_FACILITATOR_URL
        required: false
        description: Subly facilitator base URL. Defaults to https://api.demo.sublyfi.com.
      - name: SOLANA_RPC_URL
        required: false
        description: Solana RPC endpoint. Defaults to the public mainnet RPC.
      - name: SUBLY_MCP_MAX_AMOUNT_RAW_USDC
        required: false
        description: Per-payment cap in raw USDC units (6 decimals). Defaults to 10000 (0.01 USDC).
    emoji: "💸"
    homepage: https://github.com/SublyFi/subly-payment-protocol
---

# Subly pay (yield-funded x402)

This skill lets you fetch a paid HTTP resource and settle its x402
(`subly-yield-exact`) 402 challenge automatically. Payment comes from the
agent wallet's Kamino vault **yield** — the deposited principal is never
spent, and the facilitator refuses any payment the spendable yield cannot
cover.

## When to use

- A request to a URL returns HTTP 402, or the user asks you to buy / access
  a paywalled API or resource served via Subly / x402.
- Only pay for URLs the user actually intends to purchase. Treat the
  per-payment cap as a hard limit.

## One-time wallet setup (if not done yet)

Subly does NOT create wallets — bring your own Solana keypair. If
`SUBLY_DEMO_AGENT_KEYPAIR_PATH` is not set or the wallet has no vault
balance, guide the user through this once:

1. Create a keypair (or export one from an existing wallet):
   `solana-keygen new --no-bip39-passphrase -o ~/.subly/agent.json`
   The printed public key is the agent wallet address. The private key
   stays in that file — never share or print it.
2. Point the skill at it: `export SUBLY_DEMO_AGENT_KEYPAIR_PATH=~/.subly/agent.json`
3. Send USDC (Solana mainnet) to that address. No SOL is needed — fees are
   sponsored. Then deposit into the vault (minimum 1 USDC):
   `npx -y @subly_fi/pay deposit 1000000` (deposit also self-registers the wallet).
4. Yield accrues over time; a payment needs the price plus a fixed overhead
   (~0.0024 USDC) of spendable yield.

## How to run

Run the one-shot pay command (no clone — uses the published package via npx)
with the resource URL:

```bash
npx -y @subly_fi/pay fetch "<url>"
```

To set a tighter per-call cap (raw USDC, 6 decimals — e.g. 100 = 0.0001 USDC):

```bash
npx -y @subly_fi/pay fetch "<url>" 100
```

The command prints a single JSON object on stdout. On success it contains
`"paid": true` plus a `payment` object with `amountUsdc`, `payTo`,
`paymentId`, and `solscanUrl` (the on-chain receipt). Report the delivered
body and the receipt to the user.

## Reading the result

- `paid: true` with a `payment` block → the resource was delivered and paid.
  Show the content and the Solscan link.
- `refused: true` with a `reason`:
  - `insufficient_yield` → not enough vault yield accrued yet. This is normal;
    tell the user to wait (yield accrues over time) — do NOT retry in a loop.
  - `amount_exceeds_client_cap` → the price exceeds the cap. Only re-run with a
    higher cap if the user confirms the price is expected.
  - `delivery_failed_payment_pending` → the payment was signed but delivery
    failed. Run the **exact same command again** — it retries the same payment
    and does NOT pay twice. Do not treat this as unpaid.
  - `payment_already_settled` / `payment_outcome_unknown` → a previous payment
    is unresolved. Do not blindly re-pay; report the `paymentId` to the user.

## Guardrails

- Never read, print, or transmit the contents of the keypair file in
  `SUBLY_DEMO_AGENT_KEYPAIR_PATH`. Only the public receipt is shared.
- Do not raise the payment cap on your own initiative.
