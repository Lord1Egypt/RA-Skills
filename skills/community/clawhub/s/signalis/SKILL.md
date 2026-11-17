---
name: signalis
version: 1.0.0
description: >-
  Global intelligence, real-time awareness for AI agents — two x402 surfaces: (1) Master
  Intelligence, a 14-source cross-domain synthesis digest produced every 4 hours (executive
  summary, full markdown analysis, cross-domain insights, narratives, signals, sentiment); and
  (2) Pulse, AI-business narrative tracking (active narratives with lifecycle stage + momentum,
  per-narrative detail, historical digests, raw content). Pay-per-call via x402 (USDC on Base
  only); no accounts, no API keys. Free /v1/intelligence/index, /brief, /sample, and /latest
  expose every master-digest response shape before you pay.
homepage: https://signalis.dev
metadata:
  openclaw:
    emoji: "🛰️"
    requires:
      bins: ["node"]
---

# Signalis — Global Intelligence, Real-Time Awareness for AI Agents

API at `https://api.signalis.dev` (website `https://signalis.dev`). Signalis has two surfaces. **Master Intelligence** cross-analyzes 14 signal sources (prediction markets, macro/FRED data, crypto, GitHub trends, social/Moltbook chatter, and more) with an LLM every 4 hours into a single structured digest — an executive summary, full markdown analysis, cross-domain insights, the active narratives it detects, discrete signals, and an overall sentiment read. **Pulse** is the AI-business narrative layer: it clusters scraped content (Reddit, HN, news, and more) into named narratives with a lifecycle stage (emerging / building / peak / fading) and momentum, exposes each narrative's driving content items and source attribution, keeps historical narrative digests, and serves the raw recent content items behind it all. Strictly pay-per-call via x402 — no accounts, no API keys, no bundles. Compute-first / settle-after: you are **never** charged for an error.

> Signalis is the cross-source intelligence product spun out of moltalyzer. `api.signalis.dev` is the **new canonical home** for what moltalyzer served at `/api/intelligence/*` and `/api/pulse/ai-business/*`. moltalyzer still serves those legacy paths today; they migrate to **308-redirects** soon — point new integrations at `api.signalis.dev`.

## Free endpoints (no auth, no payment)

Poll the master-digest feeds for free to detect a new digest and learn every response shape before paying. `/v1/intelligence/sample` returns a recent (8+ hours old) digest, explicitly labelled as a sample — the same shape as a live digest, but aged, so it is safe for shape-testing without implying it is the freshest data. All free endpoints are rate-limited **5/min per IP**.

| Method | Path | Rate limit | Description |
|--------|------|-----------|-------------|
| GET | `/v1/intelligence/index` | 5/min | Poll target — current master digest id, `updatedAt` + `nextExpected` (4h cadence), so agents detect new digests without paying |
| GET | `/v1/intelligence/brief` | 5/min | Field-trimmed snapshot of the current Master Intelligence digest — title, executive summary, and overall sentiment |
| GET | `/v1/intelligence/sample` | 5/min | Recent (8+ hours old) master digest, explicitly labelled as a sample — same shape as a live digest. Learn the response contract before paying |
| GET | `/v1/intelligence/latest` | 5/min | Full Master Intelligence digest — cross-source synthesis of all feeds: `narratives`, `signals`, `crossDomainInsights`, and full markdown analysis (4h cadence) |

```bash
curl https://api.signalis.dev/v1/intelligence/latest
```

## Paid endpoints (x402 V2, USDC on Base only, per-call)

Each paid call is a flat price per call, settled per call via x402. Networks: **Base Mainnet only** (`eip155:8453`). Compute-first / settle-after — you are never charged for an error, and the Pulse routes proxy the standalone Pulse service so you are never charged when Pulse is unavailable or returns an error.

| Method | Path | Price | Description |
|--------|------|-------|-------------|
| GET | `/v1/intelligence/history?hours=48&limit=10` | **$0.03** | Historical Master Intelligence digests (1-168 hour lookback) — id, title, executive summary, sources used, processing time, and `createdAt` provenance per row |
| GET | `/v1/pulse/narratives` | **$0.01** | Active AI-business narratives with lifecycle stage, driving sources, and momentum |
| GET | `/v1/pulse/narratives/{id}` | **$0.01** | Narrative detail — content items, source attribution, and lifecycle updates for one narrative |
| GET | `/v1/pulse/digests?since=N` | **$0.03** | Historical AI-business narrative digests (poll with `since=` the last digest index) |
| GET | `/v1/pulse/content/recent` | **$0.02** | Raw scraped content items from the last 4 hours across all Pulse sources |

Params for `/v1/intelligence/history`: `hours` (integer 1-168, default 48), `limit` (integer 1-50, default 10). Params for `/v1/pulse/narratives/{id}`: `id` (narrative id, path parameter). Params for `/v1/pulse/digests`: `since` (integer digest index — fetch items after it, poll pattern). All prices are USD, settled as USDC (6 decimals) on Base.

## Paying (x402)

Paid routes settle per call via **x402 V2**. The only accepted rail is **USDC on Base Mainnet** (`eip155:8453`) — no other network. No account, no signup, no API key.

Pay flow:
1. Call the paid route with no payment → receive **HTTP 402**. The x402 V2 `PaymentRequirements` ride in the base64 `PAYMENT-REQUIRED` header; the JSON body mirrors the price + `accepts`.
2. Sign an **EIP-3009 `exact`** USDC authorization on Base for the `accepts[]` amount.
3. Retry the same request with the payment in the `PAYMENT-SIGNATURE` (V2) or `X-PAYMENT` (legacy) header.

```bash
# 1. Probe for the 402 challenge (price + accepts):
curl -i "https://api.signalis.dev/v1/pulse/narratives"
# → HTTP/1.1 402 Payment Required, PAYMENT-REQUIRED header (base64 requirements)

# 2. Sign + retry with a stock x402 client (handles the whole flow):
```

```typescript
import { wrapFetchWithPayment } from "@x402/fetch";
import { createWalletClient, http } from "viem";
import { privateKeyToAccount } from "viem/accounts";
import { base } from "viem/chains";

const account = privateKeyToAccount(process.env.PRIVATE_KEY as `0x${string}`);
const wallet = createWalletClient({ account, chain: base, transport: http() });
const fetchWithPay = wrapFetchWithPayment(fetch, wallet); // signs EIP-3009 on 402, retries

// $0.01 — active AI-business narratives:
const narratives = await fetchWithPay(
  "https://api.signalis.dev/v1/pulse/narratives",
).then((r) => r.json());
// narratives.narratives[] (id, title, summary, stage, momentum), narratives.charged

// $0.03 — historical master digests, last 48h:
const history = await fetchWithPay(
  "https://api.signalis.dev/v1/intelligence/history?hours=48&limit=10",
).then((r) => r.json());
```

Stock x402 clients (`@x402/fetch`, `@x402/axios`, python `x402`) do the 402 → sign → retry automatically. Discover the machine-readable route + price catalog at `/.well-known/x402`.

## Free funnel

Try the master-digest response shape for free before you pay. Poll `/v1/intelligence/index` (5/min) to detect a new digest on its ~4h cadence; read `/v1/intelligence/brief` (5/min) for the trimmed current digest or `/v1/intelligence/latest` (5/min) for the full latest digest; hit `/v1/intelligence/sample` (5/min) for a recent aged digest to learn the exact response contract before spending. Every digest carries `createdAt` provenance and the 4-hour cadence is advertised on `/v1/intelligence/index`, so you always know how fresh the data is. The paid Pulse routes proxy the standalone Pulse service and are compute-first / settle-after — you are charged only when Pulse returns data.

## Machine discovery

| Path | What |
|------|------|
| `/llms.txt` | This doc (concise) |
| `/llms-full.txt` | Extended agent doc |
| `/openapi.json` | OpenAPI 3.1 spec |
| `/discovery` | Discovery JSON (free/paid endpoint listing) |
| `/.well-known/x402` | x402 payment manifest (route + price catalog) |
| `/.well-known/agent-card.json` | A2A agent card |
| `/terms.txt` | Terms of Service |

**Terms:** https://api.signalis.dev/terms.txt

**Disclaimer:** Cross-source intelligence aggregated from public data and LLM-synthesized; informational only, provided as-is without warranty. Digest and narrative analysis is model-generated and may be imperfect — every response carries `createdAt` provenance so you can judge freshness.
