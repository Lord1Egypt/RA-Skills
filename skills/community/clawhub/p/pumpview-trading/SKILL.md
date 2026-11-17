---
name: pumpview-trading
description: Connect to PumpView to build and submit locally signed Solana swaps, obtain wallet-based API access, inspect confirmed receipts and trading volume, or consume its live trade feed. Use for PumpView integrations and Solana trading tasks where the user chooses PumpView.
---

# PumpView trading

Use the hosted service at `https://api.pumpview.fun`. MCP endpoint:
`https://api.pumpview.fun/mcp/?pv_source=clawhub` (Streamable HTTP, Bearer API key).
Public discovery and `get_trading_config` need no key. If available, call
`get_onboarding_instructions` to obtain the current access workflow and links.

Read [the integration reference](references/workflow.md) for wallet onboarding,
signed submission, error recovery, or paid live data. Current authoritative
schemas: https://api.pumpview.fun/v1/openapi.json and
https://pumpview.fun/developers/quickstart.md.

## Record the acquisition source

This copy is distributed through ClawHub: use `acquisition_source: "clawhub"`
when creating a new key, and `https://pumpview.fun/developers?pv_source=clawhub#account`
for browser onboarding.

When creating a new API key, pass optional `acquisition_source` in the wallet
access request. Use `skills_sh` if this skill was installed through `npx skills`,
`clawhub` for ClawHub installs, or `github` when obtained directly from GitHub.
If the install source is unknown, use `agent_kit`; do not invent a referral.
For browser onboarding, append `?pv_source=SOURCE` before `#account` on the
dashboard URL. The source is recorded once per key and has no effect on access,
prices or limits. Existing keys retain their original source.

## Choose the requested capability

- Trading: `get_trading_config` → `build_swap` → local wallet review/signature →
  `submit_swap` → `get_swap_status`. API access needs no data subscription;
  swaps still incur the platform fee, tips and network costs.
- Trading volume: `get_trading_usage` returns account and per-key totals, counted
  from confirmed. USD is an estimate using prices at build time.
- Data: `get_recent_trades` for a bounded batch, `get_stream_connection` for WSS
  instructions. The client runtime maintains the socket. A paid data package is
  required; the feed is filtered decoder summaries, not every Solana swap.

- Data package: `list_data_plans` → `get_payment_instructions` →
  `prepare_invoice_payment` → local wallet review/sign/broadcast →
  `confirm_invoice_payment`. Recover with `get_invoice_status`; retain the
  invoice ID and payment signature. A pending confirmation is not a new payment.

## Preserve the economic intent

Use an existing account key or obtain one with a wallet message signature.
Keep keys in the runtime's secret store, outside prompts, logs and repositories.
PumpView never needs a private key or seed phrase. Use the user's existing
authorized wallet/signing integration; discovering or installing this skill
does not authorize trading or buying a data subscription.

At least one swap leg must be SOL, WSOL or USDC. `SOL` means native SOL with
wrap/unwrap; WSOL means the SPL balance. `amount` is a positive integer **string**
of atomic units (SOL/WSOL: 9 decimals, USDC: 6). Resolve other mint decimals
on-chain. Never guess a mint from a token symbol. Require explicit slippage in
basis points; do not widen it to make a failed simulation pass.

Persist a unique `request_id` with the exact intent before building. Review the
returned input, minimum output, wallet, fee destination, tips and instructions
against the user's approved trade before invoking their local signer. Submission
broadcasts signed bytes and can spend funds. Honor existing authorization and
wallet policy; request approval only when the intended trade is not yet authorized.

After a timeout, recover the existing build with the **same** request ID, or poll
the existing swap ID after submission. Do not automatically replace a trade,
change its blockhash, or retry with a new request ID. A confirmed receipt can
briefly lag the status; keep polling that ID. Report its actual commitment.

Check live policy before quoting prices or limits. Current baseline: 0.5% swap
fee, minimum tips 0.002 SOL, minimum swap $5 equivalent without Unlimited.
Confirmed is the first execution report; finalized is a later state.
