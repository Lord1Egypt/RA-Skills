---
name: subly-pay
description: Fetch a paywalled (HTTP 402) URL and pay for it automatically from the agent wallet's Kamino vault yield, without spending the principal. Also manages the Subly vault (deposit/withdraw) and the human owner's spending mandate (setup link, Face ID approvals). Use when a request returns 402, when the user asks to buy/access a paid API or resource, or mentions Subly / x402 / yield-funded payment.
version: 0.2.1
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
      - name: SUBLY_RELAYER_URL
        required: false
        description: Subly relayer API base URL. Defaults to https://api.demo.sublyfi.com.
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

This skill lets you fetch a paid HTTP resource and settle a standard x402
Solana USDC `exact` 402 challenge automatically. Payment comes from the agent
wallet's Kamino vault **yield** — the deposited principal is never spent, and
the Subly relayer refuses any payment the spendable yield cannot cover.

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
   sponsored.
4. Appoint the human owner and make the first deposit (one Face ID covers
   both). Agree the spending limits and the first deposit amount in chat,
   then create the setup link (minimum deposit is just over 1 USDC — the
   vault's share rounding refuses exactly 1.000000):
   `npx -y @subly_fi/pay setup-link --initial-deposit 1010000`
   Paste the printed `setupUrl` to the user VERBATIM — it expires in 10
   minutes and works once. The human opens it on their phone, reviews the
   limits, and confirms with Face ID (passkey) or a Solana wallet signature.
   After they say they finished, verify and deposit:
   `npx -y @subly_fi/pay setup-status <sessionId>` (the pasted setupUrl
   works as the argument too) → status "completed"
   `npx -y @subly_fi/pay deposit 1010000` (the pre-approved first deposit
   is picked up automatically; deposit also self-registers the wallet).
5. Yield accrues over time; a payment needs the price plus a fixed overhead
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
  - `payment_outcome_unknown` → a previous external x402 attempt may already
    have settled. Do not blindly re-pay; report the message and ask the user
    before using `SUBLY_PAY_FORCE_NEW_PAYMENT=1`.
  - `approval_required` → the price exceeds the owner's approval threshold;
    NOTHING was paid. The output carries an `approveUrl`, an `approvalId`,
    and a ready-made `retry` command: paste the approveUrl to the user, and
    once they approved (Face ID / wallet sign), run the `retry` command
    exactly as printed. It repeats the SAME cap — approval-needing prices
    exceed the default cap, so dropping it would refuse with
    `amount_exceeds_client_cap`:
    `npx -y @subly_fi/pay fetch "<url>" <sameMaxAmountRawUsdc> apr_<approvalId>`
  - `state_persist_failed` → the local pending-payment marker could not be
    stored. Do not retry until the state path/disk issue is fixed.

## Deposits and withdrawals

- `npx -y @subly_fi/pay deposit <amountRawUsdc> [apr_<approvalId>]`
- `npx -y @subly_fi/pay withdraw <amountRawUsdc> [apr_<approvalId>]`

Deposits move principal into DeFi risk, so they require the human owner's
approval. If the output contains `"approvalRequired": true`, paste the
`approveUrl` to the user and retry with the printed `apr_...` id once they
approved. If it contains `"setupRequired": true`, run the owner onboarding
(setup-link) from the wallet-setup section first — its initial deposit is
pre-approved by the same single Face ID. Withdrawals are normally automatic
(they exit risk back to the agent wallet); the same approvalRequired flow
applies only when the owner's mandate opts into withdrawal approval.

## Guardrails

- Never read, print, or transmit the contents of the keypair file in
  `SUBLY_DEMO_AGENT_KEYPAIR_PATH`. Only the public receipt is shared.
- Do not raise the payment cap on your own initiative.
- Paste setup/approve links exactly as printed; never alter the values the
  human is asked to confirm, and never claim an approval happened — always
  verify via setup-status or by retrying with the approval id.
