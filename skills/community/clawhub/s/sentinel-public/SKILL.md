---
name: sentinel-transaction-safety
version: 1.1.0
description: >
  Pre-execution transaction safety check for autonomous AI agents — one capability of the
  SENTINEL trust oracle (sentinel-agent.dev). Before signing an on-chain transaction on Base,
  an agent calls SENTINEL and receives a SAFE / UNSAFE / UNKNOWN verdict, a SENTINEL Score
  (0-100, grade AAA-D), and an ed25519-signed receipt. Checks contract security (GoPlus token
  security) and execution simulation (Alchemy eth_call). Pay-per-call via x402 on Base —
  pricing is tiered by transaction value (from $0.005 USDC for small txs, scaling up for
  higher-value ones). No accounts, no API keys, no SDK required. No free trial. SENTINEL also
  exposes a separate counterparty-trust capability (behavioral 0-100 scoring); see "SENTINEL is
  one oracle with two capabilities" below.
license: MIT
compatibility: >
  Requires internet access to reach the SENTINEL API. No local dependencies. Compatible with any
  agent that can make HTTP POST requests and hold a Base-compatible wallet capable of signing an
  EIP-3009 USDC authorization. There is no no-wallet preview endpoint for /v1/guard.
metadata:
  author: teodorofodocrispin-cmyk
  version: 1.1.0
  oracle_onchain: "0x6841496c3e7eDF9eEB02bE64ab98CF5D5c5aF813 (Base)"
  endpoint: https://sentinel-agent.dev/v1/guard
  health: https://sentinel-agent.dev/health
  pricing: https://sentinel-agent.dev/pricing
  payment: "Base USDC via x402 (tiered by tx value, from $0.005; EIP-3009, facilitator-free local verification)"
  usdc_asset: "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913 (USDC on Base)"
  pay_to: "0xCf1d31020A7915421f6d66B9835Dcb6f422337E7"
  trial: "none — every /v1/guard call requires a valid x402 payment"
  requires_env: none
  receipt_signature: "ed25519 — signer public key published at /health for independent verification"
  infrastructure: "FastAPI + Supabase + Render"
  data_sources: "GoPlus token security + Alchemy eth_call simulation, reviewed by an LLM council"
  mcp_server: https://sentinel-agent.dev/mcp
  homepage: https://github.com/teodorofodocrispin-cmyk/sentinel-public
  docs_llm: https://sentinel-agent.dev/llms.txt
---

> ⚠️ **Data Handling Notice:** SENTINEL sends the unsigned transaction payload (chain, sender, tx data) to a remote API (`sentinel-agent.dev`) for evaluation. The payload is processed to produce a verdict and is not required to be a signed or broadcastable transaction. Review the transparency notice below before sending any transaction containing sensitive calldata.

> ℹ️ **Name notice:** This is `sentinel-agent.dev` (on-chain oracle `0x6841496c3e7eDF9eEB02bE64ab98CF5D5c5aF813`), distinct from unrelated projects sharing the SENTINEL name.

# SENTINEL — Agent Transaction Safety Oracle v1.1.0

A pre-execution safety oracle for autonomous AI agents. Before an agent signs a blockchain transaction, it calls SENTINEL and gets back a **SAFE / UNSAFE / UNKNOWN** verdict, a **SENTINEL Score (0-100, grade AAA-D)**, and an ed25519-signed receipt — all before a single unit of value moves. Pure M2M, pay-per-call via x402, no accounts.

Running on FastAPI + Supabase + Render — the same production stack as the rest of this M2M model family (VeraData, Intelica, TrustBoost).

---

## SENTINEL is one oracle with two capabilities

SENTINEL answers "is it safe to proceed?" in **two dimensions**. This skill documents the first; the second is available on the same service.

1. **Transaction safety (this skill) — `POST /v1/guard`.** Is *this specific on-chain transaction* safe to sign? A contract-level risk check before execution, returning SAFE / UNSAFE / UNKNOWN with a 0-100 score.
2. **Counterparty trust — `GET /v1/attestation`.** Is *this payment counterparty* trustworthy? A behavioral 0-100 score of x402 buyers and sellers on Base, backed by an append-only Default Registry of verified incidents, with ES256-signed attestations verifiable offline. Free cached tier; paid fresh tier (`/v1/attestation/deep`, $0.03 USDC). See `https://sentinel-agent.dev/llms.txt` for the full capability map.

Both capabilities are part of the same SENTINEL oracle (`sentinel-agent.dev`). This skill focuses on `/v1/guard` so an agent can consume it directly; if you need counterparty scoring instead, use `/v1/attestation`.

---

## ⚠️ Transparency Notice (Read Before Installing)

### 1. Data Transmission

The transaction payload you send (`chain`, `from`, `tx`) is transmitted to Render infrastructure for processing via FastAPI.

**What SENTINEL evaluates:** contract security (GoPlus token security — honeypot, owner abuse, taxes, mintable, proxy) and execution simulation (Alchemy `eth_call` — reverts), aggregated by rule-based checks plus an LLM council server-side, to produce a SAFE / UNSAFE / UNKNOWN verdict with a 0-100 score.

**What SENTINEL stores:** verdict, payer address, chain, and price paid, logged to Supabase for usage tracking. It does not require or store your wallet's private key at any point.

**For strict no-transmission requirements** (air-gapped systems, or transactions containing sensitive calldata that must never leave the local machine): this service is not suitable.

### 2. Payment Model and Autonomous Safety

SENTINEL uses **x402 with local EIP-3009 verification** — the payment is verified either through a facilitator (CDP/PayAI, which also indexes the service on the agentic.market Bazaar) or, as a fallback, by recovering the EIP-3009 signature locally with no facilitator dependency. No human confirmation needed.

**Pricing is tiered by transaction value.** The price for a `/v1/guard` call scales with the value of the transaction being checked: from **$0.005 USDC** for small transactions, stepping up for higher-value ones. The exact price for a given request is always returned in the 402 challenge (`maxAmountRequired`), so an agent never has to guess — it reads the required amount from the response and pays exactly that.

**How autonomous payment works safely:**

1. Agent calls `POST /v1/guard` without payment → receives HTTP 402 with the `PAYMENT-REQUIRED` header and a body listing `accepts` / `paymentRequirements` (network `base`, the tier-appropriate USDC amount, `payTo`).
2. Agent signs an EIP-3009 `TransferWithAuthorization` for the exact amount, using its own wallet's private key — **that signature never leaves the agent's own environment**.
3. Agent retries the request with the signed authorization in the `X-PAYMENT` header.
4. SENTINEL verifies the payment (facilitator first, local EIP-3009 signature recovery as fallback) and settles.
5. Verdict + signed receipt are returned only after verification succeeds.

**Why this is safe for autonomous agents:**

- The agent's private key never touches SENTINEL infrastructure — only the resulting signed authorization does.
- Local verification is deterministic cryptographic signature recovery.
- SENTINEL cannot initiate a charge — the agent must construct and sign the authorization itself, for the exact amount quoted in the 402.

**No trial mode.** Unlike the counterparty-trust capability (which has a free cached tier), `/v1/guard` has no free preview endpoint. Every call requires a valid payment.

### 3. Receipt Signature (independently verifiable)

Every `/v1/guard` verdict is returned with an **ed25519 signature**. The signer's public key is published at `https://sentinel-agent.dev/health` (field `signer`), so an agent can verify a receipt's authenticity offline, without trusting the transport. (Note: the counterparty-trust capability uses ES256/JWS with its key at `/.well-known/jwks.json` — two schemes for two capabilities, by design.)

### 4. Audit Trail

Every call is logged to Supabase with: verdict, payer address, chain, and price. Aggregate, unfiltered statistics are public at `/stats` — any agent can inspect SENTINEL's track record (verdict distribution, unique contracts seen, outcomes reported back) before depending on it.

### 5. Operator Verification

- **GitHub:** <https://github.com/teodorofodocrispin-cmyk>
- **Repository:** <https://github.com/teodorofodocrispin-cmyk/sentinel-public>
- **Health endpoint (with signer public key):** <https://sentinel-agent.dev/health>
- **Pricing:** <https://sentinel-agent.dev/pricing>
- **On-chain oracle (Base):** `0x6841496c3e7eDF9eEB02bE64ab98CF5D5c5aF813`

---

## When to use this skill

Activate this skill when:

- An agent is about to sign an on-chain transaction on Base and wants a pre-flight safety check (malicious contract, honeypot, owner abuse, simulation revert).
- The agent needs a signed, independently verifiable SAFE/UNSAFE/UNKNOWN verdict before spending funds.
- The agent's wallet has budget for per-call payment (from $0.005 USDC, tiered by tx value) — there is no free fallback for `/v1/guard`.

## When NOT to use this skill

- Strict zero-transmission environments (air-gapped, on-premise) — the transaction payload leaves the local machine.
- Any agent without an x402-capable wallet able to sign EIP-3009 authorizations on Base. There is no no-wallet preview to fall back to for `/v1/guard`.
- Transactions containing calldata that must never be transmitted to a third party.
- You need to assess a *counterparty's* trustworthiness rather than a *transaction's* safety — use `/v1/attestation` instead.

---

## How it works

1. Agent `POST`s `{chain, from, tx}` to `sentinel-agent.dev/v1/guard`.
2. SENTINEL runs contract security (GoPlus) and execution simulation (Alchemy `eth_call`).
3. An LLM council reviews the aggregated signals server-side.
4. SENTINEL returns a JSON verdict (`SAFE` / `UNSAFE` / `UNKNOWN`), a 0-100 score with AAA-D grade, the contributing risk signals, a transaction digest (`sha256:...`), and an ed25519-signed receipt.

The `txDigest` in every response links the verdict to the exact transaction evaluated. An agent can later report what actually happened via the free `POST /v1/outcome` endpoint (referencing that digest), which feeds SENTINEL's public track record at `/stats`.

---

## Try it — check pricing and health first (free, no wallet needed)

```
curl https://sentinel-agent.dev/health
curl https://sentinel-agent.dev/pricing
```

These two endpoints are free and require no payment. `POST /v1/guard` itself always requires payment — there is no free equivalent. (`/health` also returns the ed25519 `signer` public key you can use to verify receipts.)

---

## API Request

**Endpoint:** `POST https://sentinel-agent.dev/v1/guard`
**Headers:** `Content-Type: application/json`, `X-PAYMENT: <x402 signed authorization>`

```
{
  "chain": "base",
  "from": "0xYourAgentWallet",
  "tx": { "to": "0xTargetContract", "data": "0x...", "value": "0x0" },
  "value_usd": 25.0
}
```

`value_usd` is optional. If provided, SENTINEL uses it to pick the price tier (covering ERC-20 transfers where the ETH `value` is 0); otherwise it derives the tier from the transaction's ETH `value`.

## API Response (no payment, 402)

The `maxAmountRequired` reflects the tier for this specific transaction.

```
{
  "x402Version": 2,
  "accepts": [
    {
      "scheme": "exact",
      "network": "eip155:8453",
      "maxAmountRequired": "5000",
      "payTo": "0xCf1d31020A7915421f6d66B9835Dcb6f422337E7",
      "asset": "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913"
    }
  ]
}
```

## API Response (success, 200)

```
{
  "verdict": "SAFE",
  "sentinelScore": 94,
  "grade": "AAA",
  "risks": [],
  "reasons": [],
  "txDigest": "sha256:...",
  "signature": "..."
}
```

## SENTINEL Score grading

| Grade    | Score range | Meaning                                                                     |
| -------- | ----------- | --------------------------------------------------------------------------- |
| AAA      | 90-100      | No material risk signals detected                                           |
| AA/A     | 70-89       | Minor advisory signals, no hard risks                                       |
| BBB/BB/B | 40-69       | Moderate risk signals present                                               |
| CCC/CC/C | 15-39       | Significant risk signals                                                    |
| D        | 0-14        | Hard risk detected (honeypot, owner abuse, simulation failure)              |

---

## Known Limitations

- **No free trial or no-wallet preview endpoint exists for `/v1/guard`.** Every call requires payment. (The separate counterparty-trust capability does have a free cached tier at `/v1/attestation`.)
- Verdicts reflect the checks currently implemented (GoPlus contract security, Alchemy simulation, LLM council review); they are not a guarantee against novel or unseen attack patterns.
- **No certified audit:** the SENTINEL Score is produced by rule-based checks plus an LLM council, not by a certified security firm.
- Settlement is validated end-to-end on Base; other networks may appear in the 402 for discoverability but Base is the validated settlement chain.

## Resources

- GitHub: <https://github.com/teodorofodocrispin-cmyk/sentinel-public>
- Health check (with signer public key): <https://sentinel-agent.dev/health>
- Pricing: <https://sentinel-agent.dev/pricing>
- Track record (public stats): <https://sentinel-agent.dev/stats>
- Agent card (A2A): <https://sentinel-agent.dev/.well-known/agent.json>
- Docs (LLM-readable, full capability map): <https://sentinel-agent.dev/llms.txt>
- Counterparty trust capability: <https://sentinel-agent.dev/v1/attestation>
- Methodology (public v1.0.0): <https://sentinel-agent.dev/methodology>
- MCP server: <https://sentinel-agent.dev/mcp>
- Infrastructure: FastAPI + Supabase + Render
