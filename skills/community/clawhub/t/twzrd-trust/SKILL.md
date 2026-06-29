---
name: twzrd-trust
description: |
  Check any Solana wallet or x402 seller BEFORE paying it. Free preflight returns a
  ReadinessCard (allow / warn / block + trust score + caveats) from a 50k+-payer /
  400k+-event observed Solana x402 payment corpus. Composes with any x402 payer skill
  (agentcash, bazaar pay, ClawRouter wallets): run the preflight first, abort on
  decision=block.

  WHAT YOU GET FREE: pre-spend ReadinessCard, wallet trust scores, x402 leaderboard,
  counterparty + facilitator footprint, wash/sybil-fleet detection, batch + compare,
  signed-receipt verification.
  PAID (x402, USDC on Solana): full renormalized trust model + portable Ed25519-signed
  V5 receipt at GET /v1/intel/trust/{pubkey} (0.05 USDC).
  TRIGGERS: should I pay this, is this wallet safe, check seller, x402 preflight, scam
  check, counterparty risk, wallet reputation, trust score, verify receipt, before
  paying, solana wallet check, agent trust, readiness card
homepage: https://intel.twzrd.xyz
metadata:
  version: "1.2"
---

# TWZRD Trust - check the counterparty before the money moves

TWZRD is the independent scorer on the real Solana x402 payer graph. It observes
cross-facilitator x402 payment behavior and scores it. Use it as the preflight gate in
front of ANY skill or tool that spends USDC: if the ReadinessCard says block, do not pay.

No API key. No signup. Free tier needs nothing but curl.

## Install

```bash
npx clawhub install twzrd-trust
```

After install: restart your OpenClaw session (skills load at session start), then
run the curl below to confirm it's working.

Note: the page may show `openclaw skills install twzrd-trust` — that command does not
exist. The correct install is `clawhub install` or `npx clawhub install` above.

## Try it now (no wallet, no keys)

Run this as-is — no substitution needed:

```bash
curl -s -X POST https://intel.twzrd.xyz/v1/intel/preflight \
  -H 'content-type: application/json' \
  -d '{"seller_wallet": "6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P", "agent_intent": "test"}'
```

You'll get back a `ReadinessCard` with `decision` (allow / warn / block), `trust_score`
(0-100), and `caveats[]` (human-readable risk factors). Replace the wallet with any
Solana seller address you want to vet before paying.

## The one rule

Before signing or sending any x402 payment to a seller you have not paid before, run
the preflight with the actual seller wallet from the 402 response:

```bash
curl -s -X POST https://intel.twzrd.xyz/v1/intel/preflight \
  -H 'content-type: application/json' \
  -d '{"resource_name": "my service name",
       "seller_wallet": "SELLER_PUBKEY_FROM_402_RESPONSE",
       "price_usdc": 0.05,
       "agent_intent": "swap quote"}'
```

Read `readiness_card.decision`:
- `block` -> abort. Do not sign or send the payment.
- `warn`  -> proceed with caution (low corpus signal, not confirmed bad).
- `allow` -> proceed normally.

Also returned: `trust_score` (0-100), `caveats[]` (human-readable risk factors), and
`proof` (whether a paid V5-receipt path exists for this seller). The response also
carries a `can_spend` flag - treat it as deliberately conservative: the free tier
defaults to warn / can_spend=false for any wallet without strong corpus signal (most
wallets, including well-known ones). Gate on `decision=block`, not on `can_spend`.
Fail open on preflight unavailability (timeout / non-2xx): the seller is not penalised
for TWZRD downtime, but say so in your output.

## Free discovery tools (HTTP, no auth)

| Call | What it answers |
|------|-----------------|
| `GET /v1/intel/score_wallet_for_intel?wallet=<pubkey>` | 0-100 intel score for one wallet |
| `GET /v1/intel/get_top_intel_agents?limit=10&min_paid_calls=2&max_days_since_last=14` | who is actively paying on Solana x402 (denoised leaderboard) |
| `GET /v1/intel/get_counterparties?wallet=<pubkey>&limit=10` | top merchants a wallet pays |
| `GET /v1/intel/get_facilitator_footprint?wallet=<pubkey>` | which x402 facilitators a payer settled through |
| `GET /v1/intel/compare_wallets?wallet_a=...&wallet_b=...` | side-by-side intel for two wallets |
| `POST /v1/intel/score_wallets_batch` body `{"wallets":[...]}` | score up to 25 wallets in one call |
| seller-side reputation | returned as the `provider_reputation` block inside the preflight response above (also the MCP tool `get_provider_reputation`) - there is no standalone HTTP GET route |

Base URL for everything: `https://intel.twzrd.xyz`

## Paid trust call (x402, 0.05 USDC on Solana mainnet)

```
GET https://intel.twzrd.xyz/v1/intel/trust/{pubkey}?seller_wallet=<seller you are about to pay>
```

Standard x402 flow: first request returns 402 with payment requirements; sign and retry
with the payment header (any x402 payer skill or `@wzrd_sol/sdk` handles this). Response
includes the renormalized trust model AND a portable Ed25519-signed V5 receipt anchored
to the settlement transaction.

Pass the seller counterparty on every paid call (`?seller_wallet=` here, `?merchant=` on
the market intel routes). It arms TWZRD's settle-time trust gate: if that seller scores
below threshold the server refuses to settle (402, charged:false, no on-chain tx) before
your payment broadcasts. The scored `{pubkey}` subject itself is never gated.

## Verify any V5 receipt offline (trusts no TWZRD code)

```bash
npx twzrd-receipt-verifier receipt.json --pubkey <published signing key>
# or: pip install twzrd-receipt-verifier
```

The signing key is published at `https://intel.twzrd.xyz/.well-known/x402` and inside
`/openapi.json`. A receipt that fails signature verification is not a TWZRD receipt.

## Optional: native MCP (streamable HTTP)

The same intel is exposed as an MCP server - 17 tools, MCP 2025-03-26 over streamable
HTTP, no local install. The install fact is the URL:

```
https://intel.twzrd.xyz/mcp   (transport: streamable-http)
```

Add it through your MCP client's server config. OpenClaw builds that expose an `mcp`
command can use:

```bash
openclaw mcp add twzrd --url https://intel.twzrd.xyz/mcp --transport streamable-http
```

If your build has no `mcp` command, use the HTTP calls above directly, or bridge via
mcporter.

## Honest framing (read before quoting numbers)

Corpus totals are ECOSYSTEM payment behaviors TWZRD observes and scores - not calls or
revenue to TWZRD. Raw payer counts include a 2026-04 onboarding-faucet wave; the durable
graph is the `corpus_slices` view (pre-spike base + multi-merchant payers) returned by
`get_top_intel_agents`. Free-tier scores are heuristic teasers; the corpus-grade
renormalized model and signed receipt live behind the paid trust call.

External-traction claims use the verified 9iXAtu $0.05 framing only - no overclaims.
Paid surface is 0.05 USDC x402 (Solana mainnet).

## More

- Machine-readable service descriptor: `https://intel.twzrd.xyz/.well-known/x402`
- Full agent orientation: `https://intel.twzrd.xyz/llms.txt`
- OpenAPI 3.1 with x402 annotations: `https://intel.twzrd.xyz/openapi.json`
