---
name: z-zero-payments
description: Pay for things safely from your agent — gasless USDC on Base plus JIT single-use virtual cards via the Z-Zero MCP server. Card data never enters the model context, and no payment executes without explicit human approval.
homepage: https://z-zero.xyz
user-invocable: true
metadata:
  {
    "openclaw":
      {
        "requires": { "bins": ["npx"], "env": ["Z_ZERO_API_KEY"] },
        "primaryEnv": "Z_ZERO_API_KEY",
        "emoji": "💳",
      },
  }
---

# Z-Zero Payments

Give this agent the ability to buy things — SaaS subscriptions, API credits, physical goods — without ever seeing a card number.

Z-Zero is a payment MCP server with two rails behind one interface:

- **Gasless USDC on Base** for crypto-native checkouts (sponsored by Coinbase Paymaster — the wallet holds only USDC, no ETH, no gas UX).
- **JIT single-use virtual cards** for the 99% of the web that only takes cards: issued for one amount, one merchant, 1-hour TTL, burned after a single use.

## The security model (read this first)

This skill is deliberately boring about money. Three properties are structural, not policy:

1. **The model never sees card data.** No PAN, no CVV, no expiry ever enters your context. You only ever handle single-use *tokens*; the real card details are injected into the merchant's checkout form by a local Playwright process and wiped from RAM. If you ever think you need a card number, you are off the rails — stop.
2. **Humans approve money movement.** Before any payment executes, call `request_human_approval` with the exact final total and wait for confirmation. A purchase your operator didn't approve is a failed purchase, even if the checkout would have succeeded.
3. **Blast radius is capped by design.** Tokens are amount-locked and merchant-locked. A prompt-injected or hallucinating agent holding a Z-Zero token can lose at most that token's amount — not a wallet, not a card limit.
4. **Keys rotate on connect (v1.5.0+).** Any Passport Key that was pasted into a conversation is treated as burned: on first connect the server swaps it for a fresh key stored only in `~/.z-zero/credentials` (0600) — the live key never exists in any LLM context. One key = one machine; all agents on the machine share it, and a connect from a different machine disconnects this one (built-in intrusion alarm).

## One-time setup

1. Your operator gets a Passport Key (starts with `zk_live_`) at **[z-zero.xyz/dashboard/agents](https://z-zero.xyz/dashboard/agents)** and funds the wallet by sending USDC on Base to the deposit address shown there.
2. Export it as `Z_ZERO_API_KEY` in the agent environment. (This is only a bootstrap: on first connect the key auto-rotates and the live key moves to `~/.z-zero/credentials` — the exported value goes stale by design.)
3. Register the MCP server (OpenClaw runs MCP via mcporter). Add to `~/.openclaw/openclaw.json`:

```json
{
  "mcpServers": {
    "z-zero": {
      "command": "npx",
      "args": ["-y", "z-zero-mcp-server@latest"],
      "env": { "Z_ZERO_API_KEY": "${Z_ZERO_API_KEY}" }
    }
  }
}
```

4. Verify: list the server's tools (e.g. `mcporter list`). You should see 12 tools including `list_cards`, `auto_pay_checkout`, and `request_human_approval`, plus the `safe_checkout` prompt.

## Hard rules (non-negotiable)

- **Always read the SOP resource first** (`mcp://resources/sop`) before your first payment in a session. It is the authoritative flow; this skill is the summary.
- **Never call the REST endpoint `/api/tokens/resolve`.** It exists for the server-side injection process only. An agent calling it defeats the entire security model.
- **Never proceed past a missing approval.** No `request_human_approval` confirmation → no payment. Do not interpret silence as consent.
- **Respect the budget.** If the operator set a cap and the final total (including shipping) exceeds it, abort and report — do not negotiate with yourself.
- **Report honestly.** "Filled the form" is not "paid". Read the result `status` and relay it verbatim, including failures.
- **Prove, don't claim.** A confirmed payment returns a signed receipt with a public `verify_url`. Give it to the operator instead of asserting from memory that the order went through.

## Buying something (the flow)

1. Read `mcp://resources/sop` (once per session).
2. `get_merchant_hints` for the target platform (Shopify, Etsy, WooCommerce…) and follow its `pre_steps`.
3. Navigate the checkout until the **final total including shipping** is visible.
4. **Compare the page with what was actually asked for** — same items, quantity, variant, destination. If anything differs, stop here: no token has been issued, so a mismatch caught now costs nothing.
5. `request_human_approval` with item, merchant, and exact total. Wait.
6. On approval: `auto_pay_checkout` (it auto-detects crypto vs card checkout and routes — an EIP-681 crypto checkout settles as a gasless USDC transfer on Base; a card checkout uses a JIT single-use virtual card). For the manual path, pass `cart` and `ship_to` to `request_payment_token` so the card is bound to a **signed intent** — proof of what it was authorized to buy, not just how much it could spend.
7. Relay the result status and the receipt: `signed_receipt.diff` shows what the merchant actually did versus what was authorized (charged more, swapped an item). `verify_receipt(receipt_id)` re-checks it any time.
8. If a checkout failed for a *technical* reason, call `report_checkout_fail(url, failure_class, step, error_message)`. `failure_class` is a fixed enum — `card_declined_issuer`, `card_declined_bin_block`, `avs_mismatch`, `3ds_required`, `bot_detected`, `form_changed`, `price_changed`, `out_of_stock`, `shipping_unsupported`, `login_required`, `timeout`, `outcome_unconfirmed`, `intent_mismatch`, `unknown` — so each failure becomes evidence the next agent can use, not a log line.

## Wallet operations (read-only, no approval needed)

- `list_cards` — card aliases and balances
- `check_balance` — spendable USD for an alias
- `get_deposit_addresses` — the Base USDC deposit address for top-ups

## Troubleshooting

- `Z_ZERO_API_KEY is missing` → key not exported or agent not restarted after config change.
- `401 Invalid API Key` → key truncated on copy; re-copy the full `zk_live_…` value.
- Cloudflare-protected merchants may block the headless browser → tell the operator instead of retrying blindly.

## Links

- Source: [github.com/Dempty-glitch/Z-Zero-mcp](https://github.com/Dempty-glitch/Z-Zero-mcp) (MIT)
- npm: [`z-zero-mcp-server`](https://www.npmjs.com/package/z-zero-mcp-server)
- Official MCP Registry: `io.github.Dempty-glitch/z-zero-mcp`
- Proof of a real gasless USDC transfer on Base mainnet: [`0xdfd1f2f8…5d7a`](https://basescan.org/tx/0xdfd1f2f824e1232c3e03c52485332570ff01fbb0340c5571f699ed1218735d7a)
