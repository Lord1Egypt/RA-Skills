---
name: treat-rocks
description: Buy a novelty digital rock from treat.rocks over x402 (USDC on Base) — a signed, independently-verifiable certificate for your agent. Fixed price, no token, not an investment.
version: 1.0.0
metadata:
  openclaw:
    emoji: 🪨
    homepage: https://treat.rocks
    always: false
---

# treat-rocks

Buy a treat.rocks novelty digital rock for **$2 USDC on Base**, paid over the
[x402 protocol](https://www.x402.org/) with your own wallet. Treat.rocks
never touches your keys — your x402-capable client signs and sends the
payment; the server only ever sees the settled result. Base network gas is
separate from the $2 and paid by your own client, same as any other
on-chain transaction it sends — this skill doesn't add any fee of its own.

This is a novelty, priced and described as exactly that: **not an
investment**, no token, no resale market, no subscription, no refunds once a
rock is minted. One rock, $2, forever. See `no_token_pledge` and
`not_an_investment` in `/store.json` for the same claims machine-readable.

**Operator:** Sybl LLC, disclosed at `https://treat.rocks/SECURITY.md` and in
`/store.json`'s `operator` field. Contact for security reports or questions:
`contact@treat.rocks`.

**Source:** the treat.rocks server is closed-source. You don't need to trust
that — every rock independently re-derives from public data (see Verify,
below), the same check the operator's own claims are held to.

## How to buy

Two equivalent paths — pick whichever your client already speaks.

### Path A: MCP (recommended if your agent has an MCP client)

`POST https://treat.rocks/mcp` — JSON-RPC 2.0. Call `tools/list` to see the
full tool set (`browse_gallery`, `get_rock` are read-only, no purchase). Call
`buy_rock` (or `gift_rock` with a `recipient_address` to mint to a different
owner) to get the current payment instructions — price, network, and
endpoint, sourced live from the server, never hardcoded here. The full
signed x402 payment requirements (payTo, asset contract, scheme) come from
that endpoint's own `402` response, exactly as in Path B. Neither tool
spends your money: they hand back payment instructions, and your own
x402-capable client completes the payment against the direct endpoint below.

### Path B: direct x402 (fallback, no MCP needed)

`POST https://treat.rocks/api/rock` with no payment header first — the
server responds `402` with the exact payment requirements (scheme `exact`,
network `base`, asset USDC). Pay them with your x402 client, then retry the
same `POST` with the payment headers attached to receive your rock. Optional
query param `?gift_to=<0x address>` mints to a different owner while you
remain the recorded buyer.

Either path ends with a rock: a signed JSON certificate plus an image,
unique to your payment. The mint response includes the rock's `id` — run
Verify on it (below) before reporting the purchase complete.

## Verify before you trust it

Don't take this skill's word, or the server's, for what you bought:

- `GET https://treat.rocks/verify/<id>` does the re-derivation and the
  Ed25519 signature check itself and reports the result — you don't need
  your own crypto implementation, just this one GET request. It re-derives
  the rock's attributes from its public seed, re-derives that seed from
  (owner, tx), and checks the signature over the result.
- If you want to check the math yourself instead of trusting this endpoint's
  verdict, the certificate public key is published at
  `https://treat.rocks/.well-known/treatrocks-pubkey.json`. One scope note:
  for a purchased rock both re-derivation inputs (payer, settlement tx) are
  on-chain; a gifted rock's recipient owner is published on its certificate
  page rather than on-chain, so its re-derivation rests on that public
  record — the same caveat `/SECURITY.md` states.
- Full security posture, what the server can and can't do, and how to report
  a problem (including anything unexpected after a payment settles):
  `https://treat.rocks/SECURITY.md`, or email `contact@treat.rocks` directly.

## Machine-readable references

- `https://treat.rocks/store.json` — catalog/manifest (price, endpoints, operator, contact, security, terms)
- `https://treat.rocks/.well-known/x402.json` — x402 discovery manifest
- `https://treat.rocks/llms.txt` / `https://treat.rocks/llms-full.txt` — the same purchase/verify instructions as this skill, served live by the server (if this file and the live site ever disagree, the live site is current)
- `https://treat.rocks/terms` — plain-English terms: fixed price, no refunds, no token

## What this skill does NOT do

- It never asks for, stores, or handles your seed phrase or private key.
- It never spends on your behalf — every payment is a transaction your own
  client signs.
- It adds no server surface of its own; every endpoint above is the live
  treat.rocks production API, called directly.
