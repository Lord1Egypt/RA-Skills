---
name: veradata-latam-compliance
description: Verified Latin American compliance data for autonomous AI agents. Use when an agent needs OFAC/UN/EU/UK sanctions screening, KYB entity verification (Colombia, Mexico, Brazil, Chile, Peru), LATAM central bank rates (TRM, TIIE, Selic, UF, dólar blue), business registry lookup (RUES/CNPJ/RFC), or AI-powered market intelligence for LATAM markets. Payment via x402 v2 micropayments in USDC on Base or Solana — no API key, no subscription, no account required. Single POST request per call. Use this skill whenever a task involves sanctions compliance, KYC/KYB, LATAM financial data, corporate registry, or regulatory screening for Latin American jurisdictions.
license: MIT
compatibility: Requires internet access to reach the VeraData API. No local dependencies. Compatible with any agent that can make HTTP POST requests with PAYMENT-SIGNATURE header (x402 v2). Also supports X-TRIAL header for 3–5 free calls per endpoint per IP per day.
metadata:
  author: teodorofodocrispin-cmyk
  version: "2.3.2"
  base_url: https://api.veradata.dev
  health: https://api.veradata.dev/health
  x402_discovery: https://api.veradata.dev/.well-known/x402
  llms_txt: https://api.veradata.dev/llms.txt
  openapi: https://api.veradata.dev/openapi.json
  mcp: https://api.veradata.dev/mcp
  payment_networks:
    base: "eip155:8453 — USDC 0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913"
    solana: "solana:5eykt4UsFv8P8NJdTREpY1vzqKqZKvdp — USDC EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"
  wallet_base: "0xCf1d31020A7915421f6d66B9835Dcb6f422337E7"
  wallet_solana: "giu4VciTkfWJNG1oeP6SzHEJwmabikJSMB91GaFNWE4"
  trial: "Add X-TRIAL: true header — 3 to 5 free calls per endpoint per IP per 24h"
  infrastructure: FastAPI + Supabase + Render (Starter)
  compliance: EU_AI_ACT_ART12, EU_AI_ACT_ART13, GDPR_ART25, LGPD_ART46, SARLAFT_2024, FATF_R16
  erc8299: "sanctions_screening artifact_type registered — issue x402-foundation/x402#2749"
  sanctions_coverage: "59,454 entries — OFAC SDN + UN Consolidated + EU Consolidated + UK HM Treasury"
  homepage: https://github.com/teodorofodocrispin-cmyk/veradata-public
---

# VeraData — LATAM Compliance API v2.3

Verified Latin American compliance data delivered as x402 v2 micropayments. No API key, no SDK, no subscription — one POST request, one USDC micropayment, one verified response with full audit trail.

Built on FastAPI + Supabase + Render. Every paid response generates an immutable audit record compliant with EU AI Act Art.12/13 and FATF R16.

---

## ⚠️ Transparency Notice (Read Before Installing)

### 1. Data Transmission

Requests are transmitted to Render infrastructure (AWS us-east) via FastAPI.

**What VeraData stores:** Endpoint, country, network, payer wallet, ip_hash, audit_hash, timestamp — never raw query content beyond entity names for sanctions lookup.

**Storage:** Supabase PostgreSQL (private audit ledger, `vera_audit` table).

**Sanctions data:** Pre-seeded from official sources (OFAC SDN, UN, EU, UK HMT) via cron — no external calls during your request.

### 2. Payment Model — x402 v2

VeraData uses the x402 v2 protocol for autonomous micropayments. The standard flow:

1. Agent makes request without payment header → receives HTTP 402 with `PAYMENT-REQUIRED` header (base64 JSON)
2. Agent decodes the header to get payment parameters
3. Agent signs EIP-3009 `TransferWithAuthorization` with its own USDC wallet
4. Agent encodes signature as base64 JSON → this is the `PAYMENT-SIGNATURE` value
5. Agent retries the same request with `PAYMENT-SIGNATURE: <value>` header
6. VeraData verifies via CDP/PayAI facilitator → returns 200 with data

**VeraData never has access to agent private keys.** Payment signing happens entirely client-side.

### 3. Audit Trail

Every paid call generates an `audit_hash` (SHA-256 chain) stored in `vera_audit`. The hash chain is: `query_hash → event_hash → chain_hash`. Audit records are never deleted — they are the compliance proof.

### 4. Trial Mode

Add `X-TRIAL: true` to any POST request for 3–5 free calls per endpoint per IP per 24 hours. No wallet required for trial.

### 5. Operator Verification

- **GitHub:** https://github.com/teodorofodocrispin-cmyk
- **Health:** https://api.veradata.dev/health
- **x402 discovery:** https://api.veradata.dev/.well-known/x402
- **Contact:** teodorofodocrispin@gmail.com
- **ERC-8299 conformance:** https://github.com/babyblueviper1/preaction-governance-conformance

---

## Endpoints & Pricing

| Endpoint | Method | Price | Description |
|----------|--------|-------|-------------|
| `/sanctions/quick` | POST | $0.01 USDC | Quick OFAC-only screening — cheapest entry point |
| `/sanctions` | POST | $0.05 USDC | Full screening OFAC+UN+EU+UK (59,454 entries) |
| `/sanctions/zkp` | POST | $0.05 USDC | ZKP privacy screening — GDPR Art.25 compliant |
| `/entity` | POST | $0.03 USDC | Entity enrichment RUES/CNPJ/RFC |
| `/registry` | POST | $0.05 USDC | Business registry full record |
| `/context` | POST | $0.10 USDC | AI market intelligence (Claude Sonnet) |
| `/rates` | POST | $0.02 USDC | LATAM central bank rates (TRM/TIIE/Selic/UF/dólar blue) |
| `/rates/stream` | GET | $0.02 USDC/event | SSE streaming rates — use `/rates/stream/token` first |
| `/solutions/kyb-complete-co` | POST | $0.15 USDC | Full KYB bundle Colombia |
| `/solutions/kyb-complete-mx` | POST | $0.15 USDC | Full KYB bundle México |
| `/solutions/kyb-complete-br` | POST | $0.15 USDC | Full KYB bundle Brasil |
| `/solutions/kyb-complete-cl` | POST | $0.15 USDC | Full KYB bundle Chile |
| `/solutions/kyb-complete-pe` | POST | $0.15 USDC | Full KYB bundle Perú |
| `/solutions/screening-global` | POST | $0.08 USDC | Global screening: GCC, Africa, India, SEA |

---

## Quick Start — Trial (No Payment)

```bash
curl -X POST https://api.veradata.dev/sanctions/quick \
  -H "Content-Type: application/json" \
  -H "X-TRIAL: true" \
  -d '{"name": "Nicolás Maduro"}'
```

```bash
curl -X POST https://api.veradata.dev/sanctions \
  -H "Content-Type: application/json" \
  -H "X-TRIAL: true" \
  -d '{"name": "PDVSA", "country": "VE"}'
```

```bash
curl -X POST https://api.veradata.dev/rates \
  -H "Content-Type: application/json" \
  -H "X-TRIAL: true" \
  -d '{"country": "CO"}'
```

---

## x402 Payment Flow (Python)

```python
import httpx, base64, json

BASE_URL = "https://api.veradata.dev"

async def call_veradata(endpoint: str, payload: dict, wallet_client) -> dict:
    """
    Full x402 v2 payment flow for any VeraData endpoint.
    wallet_client must implement sign_eip3009(amount, to, usdc_contract, valid_before, nonce) -> str
    """
    # Step 1: probe for 402
    r = await httpx.post(f"{BASE_URL}{endpoint}", json=payload)
    if r.status_code == 200:
        return r.json()

    if r.status_code != 402:
        raise Exception(f"Unexpected status: {r.status_code}")

    # Step 2: decode payment requirements
    header_b64 = r.headers.get("PAYMENT-REQUIRED")
    payment_req = json.loads(base64.b64decode(header_b64))

    # Step 3: sign EIP-3009
    accepts = payment_req["accepts"][0]  # pick Base or Solana
    signature = await wallet_client.sign_eip3009(
        amount=int(accepts["maxAmountRequired"]),
        to=accepts["paymentInfo"]["payTo"],
        usdc_contract=accepts["paymentInfo"]["extra"]["erc20Address"],
        valid_before=int(time.time()) + 300,
        nonce=secrets.token_hex(16),
    )

    # Step 4: encode and retry
    payment_header = base64.b64encode(json.dumps({
        "scheme": accepts["scheme"],
        "networkId": accepts["networkId"],
        "payload": signature,
    }).encode()).decode()

    r2 = await httpx.post(
        f"{BASE_URL}{endpoint}",
        json=payload,
        headers={"PAYMENT-SIGNATURE": payment_header},
    )
    return r2.json()
```

---

## SSE Streaming — `/rates/stream`

SSE requires a pre-paid token because streaming connections cannot carry payment headers mid-stream.

**Step 1 — Get a stream token (pays $0.02 USDC):**
```bash
# Without payment — receive 402 with PAYMENT-REQUIRED header
curl -X POST "https://api.veradata.dev/rates/stream/token?country=CO"

# With payment — receive stream_token valid 5 minutes
curl -X POST "https://api.veradata.dev/rates/stream/token?country=CO" \
  -H "PAYMENT-SIGNATURE: <base64-encoded-signature>"
```

**Response:**
```json
{
  "stream_token": "abc123...",
  "country": "CO",
  "expires_in": 300,
  "stream_url": "https://api.veradata.dev/rates/stream?country=CO&stream_token=abc123..."
}
```

**Step 2 — Connect to stream:**
```bash
curl -N "https://api.veradata.dev/rates/stream?country=CO&stream_token=abc123..."
```

**SSE Events:**
- `event: rates` — rate data payload
- `event: end` — stream complete, includes `trial_remaining_today`
- `event: limit` — trial exhausted, includes 7-step payment_flow instructions
- `event: error` — fetcher error

**Trial:** 3 free events per IP per 24h without stream_token. After trial is exhausted, the `event: limit` payload contains exact payment instructions.

---

## Sanctions Screening Response

```json
{
  "status": "ok",
  "matches": [],
  "total_screened": 59454,
  "lists_checked": ["OFAC_SDN", "UN_CONSOLIDATED", "EU_CONSOLIDATED", "UK_HM_TREASURY"],
  "screening_timestamp": "2026-07-02T18:00:00Z",
  "audit_hash": "sha256:abc123...",
  "decision_ref": "vd_2026...",
  "eu_ai_act": {"art12_logged": true, "art13_compliant": true},
  "network": "base",
  "payer": "0x..."
}
```

**`matches: []` means clean — no sanctions hits found.**

If `matches` is non-empty, each entry includes: `list_name`, `entry_name`, `match_score`, `programs`, `country`.

---

## KYB Bundles — `/solutions/kyb-complete-{country}`

Combines sanctions + entity enrichment + registry lookup in a single atomic call.

**Request:**
```json
{
  "company_name": "Bancolombia S.A.",
  "country": "CO",
  "registration_number": "890903938"
}
```

**Response includes:**
- `sanctions_result` — full screening across all 4 lists
- `entity_data` — enriched entity profile (RUES/CNPJ/RFC)
- `registry_record` — full business registry extract
- `risk_score` — composite risk 0.0–1.0
- `audit_hash` — chain hash for compliance audit trail
- `eu_ai_act` — Art.12/13 compliance flags

**Countries:** `co` (RUES), `mx` (RFC/SAT), `br` (CNPJ/Receita Federal), `cl` (RUT/SII), `pe` (RUC/SUNAT)

---

## Rates Response

```json
{
  "country": "CO",
  "currency": "COP",
  "rates": {
    "TRM": {"value": 4185.23, "unit": "COP/USD", "source": "Banco de la República"},
    "DTF": {"value": 12.45, "unit": "%", "source": "Banco de la República"}
  },
  "timestamp": "2026-07-02T18:00:00Z",
  "data_freshness": "live",
  "cache_age_seconds": 180
}
```

**Countries:** CO (TRM, DTF), MX (TIIE, tipo de cambio), BR (Selic, PTAX), CL (UF, TPM), PE (referencia BCRP), AR (dólar blue, oficial, MEP)

---

## MCP Integration

VeraData exposes a full MCP server at `https://api.veradata.dev/mcp`.

```python
# In your MCP client config:
{
  "mcpServers": {
    "veradata": {
      "url": "https://api.veradata.dev/mcp",
      "transport": "http"
    }
  }
}
```

Available MCP tools: `sanctions_screen`, `entity_lookup`, `registry_search`, `get_rates`, `kyb_complete`.

---

## Error Responses

**402 — Payment Required (no payment sent):**
```json
{
  "error": "Payment required",
  "payment_flow": ["1. Decode base64 PAYMENT-REQUIRED header", "..."],
  "trial": "Add X-TRIAL: true header for 3–5 free calls per IP per 24h"
}
```
Header `PAYMENT-REQUIRED: <base64>` is always present on 402 responses.

**402 — Verification Failed:**
```json
{"error": "Payment verification failed — sign a FRESH EIP-3009 (new nonce) and retry"}
```
Header `X-402-Reason: verification_failed` helps agents distinguish this from "no payment".

**429 — Trial Exhausted:**
```json
{"error": "Trial limit reached", "trial_limit": "3 calls per endpoint per IP per 24h"}
```

---

## Compliance Coverage

| Standard | Coverage |
|----------|----------|
| EU AI Act Art.12 | Every paid call logged with audit_hash |
| EU AI Act Art.13 | Transparency metadata in every response |
| GDPR Art.25 | ZKP endpoint available — `/sanctions/zkp` |
| LGPD Art.46 | Brazilian entity data handled with appropriate safeguards |
| FATF R16 | Wire transfer screening via OFAC+UN lists |
| SARLAFT 2024 | Colombian AML screening patterns |
| ERC-8299 | `sanctions_screening` artifact_type registered |

---

## Known Limitations

- **Render Starter cold starts:** First request after 15min inactivity may take 2–5s. Subsequent requests are fast.
- **Sanctions data freshness:** Lists are updated via cron, not real-time. OFAC SDN typically updates within 24h of official publication.
- **Entity data availability:** RUES/RFC/CNPJ data depends on official registry APIs — occasionally unavailable during source maintenance windows.
- **SSE stream_token:** Single-use, 5-minute TTL. If the stream disconnects, purchase a new token.
- **x402 facilitator dependency:** Payment verification uses CDP/PayAI. Circuit breaker activates after 3 failures (60s cooldown).

---

## Resources

- Health check: https://api.veradata.dev/health
- x402 discovery: https://api.veradata.dev/.well-known/x402
- OpenAPI: https://api.veradata.dev/openapi.json
- llms.txt: https://api.veradata.dev/llms.txt
- A2A manifest: https://api.veradata.dev/.well-known/a2a-agent.json
- GitHub (public): https://github.com/teodorofodocrispin-cmyk/veradata-public
- Python example: https://github.com/teodorofodocrispin-cmyk/veradata-public/blob/main/docs/examples/python_agent.py
- TypeScript example: https://github.com/teodorofodocrispin-cmyk/veradata-public/blob/main/docs/examples/typescript_agent.ts
- ERC-8299 conformance: https://github.com/babyblueviper1/preaction-governance-conformance/examples/veradata/check_chain.py
