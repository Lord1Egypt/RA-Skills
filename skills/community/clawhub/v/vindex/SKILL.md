---
name: vindex
version: 1.4.0
description: >-
  Vehicle intelligence for AI agents — decode any 17-char VIN with a factory-warranty-terms
  block, MERGED US (NHTSA) + Canada (Transport Canada) recalls, LLM-clustered known issues with
  ODI citations plus a reliability-aggregates block, and itemized used-car drive-away costs for
  all 50 US states + DC and all 13 Canadian jurisdictions. Pay-per-call via x402 (USDC on Base);
  no accounts, no keys. Free /v1/sample/* endpoints return every response shape before you pay.
homepage: https://vindexapi.dev
metadata:
  openclaw:
    emoji: "🚗"
    requires:
      bins: ["node"]
---

# Vindex — Vehicle Intelligence for AI Agents

API at `https://api.vindexapi.dev`. Vindex aggregates free, public-domain vehicle-safety data and sells thin intelligence layers on top, priced per call. It is the only API that merges US (NHTSA) and Canada (Transport Canada) recalls in one response. Strictly pay-per-call via x402 — no accounts, no API keys, no bundles. Compute-first / settle-after: you are **never** charged for an error or a below-threshold (insufficient-data) answer.

VINs are used only as cache keys (up to 90 days), never linked to a person. Vindex is **NOT** a vehicle-history report — it makes no liens/accidents/odometer claims.

## Free endpoints (no auth, no payment)

Every `/v1/sample/*` endpoint always serves the SAME fixed sample vehicle (**2013 Ford F-150, VIN `1FTFW1ET5DFC10312`**), computed live through the normal pipeline — identical response shape to its paid per-VIN twin, plus top-level `sample: true`. Use them to learn every shape before paying.

| Method | Path | Description |
|--------|------|-------------|
| GET | `/health` | Liveness + configured payment mode (`live`\|`mock`) |
| GET | `/v1/sample/decode` | FREE sample VIN decode (same shape as paid `/v1/decode`) |
| GET | `/v1/sample/recalls` | FREE sample merged US + Canada recalls + full decode (same shape as `/v1/recalls`) |
| GET | `/v1/sample/known-issues` | FREE sample known-issues + reliability block + full decode (same shape as `/v1/known-issues`; served as-is, never 503) |
| GET | `/v1/sample/purchase-costs` | FREE sample closing costs for BOTH countries — `ca` (Ontario $25,000 private) + `us` (California $25,000 private) |
| GET | `/terms.txt` · `/terms.json` | Terms of Service (also sets `X-Terms-URL`) |

```bash
curl https://api.vindexapi.dev/v1/sample/known-issues
```

## Paid endpoints (x402 V2, USDC on Base, per-call)

Each paid call is a flat price per call, paid via x402. Every JSON response also carries a `disclaimer` string.

| Method | Path | Price | Description |
|--------|------|-------|-------------|
| GET | `/v1/decode?vin=VIN` | **$0.01** | NHTSA vPIC normalized decode (make/model/year/engine/…) + a `warranty` block of ORIGINAL factory new-vehicle terms (basic/powertrain/corrosion/roadside/EV-battery) keyed off make/model-year — not warranty-remaining, excludes extended-warranty campaigns/recalls/emissions warranties. 90-day cache |
| GET | `/v1/recalls?vin=VIN` | **$0.01** | MERGED NHTSA (US) + Transport Canada (CA) recalls + counts + FULL decoded vehicle. OGL–Canada attribution. 24h cache |
| GET | `/v1/known-issues?vin=VIN` | **$0.05** | LLM-clustered named failure modes from NHTSA complaints; EVERY issue cites verified ODI complaint numbers (validated against the source set — hallucination-gated). ALSO returns a `reliability` aggregates block (top components; severity: crashes/fires/injuries; US & Canada recall counts incl. Canadian units affected) + the full decoded `vehicle` + `complaintsAnalyzed` (sample size) vs `complaintCount` (total). Refuses (uncharged, but still returns decode + reliability) below 15 complaints. 90-day cache |
| GET | `/v1/purchase-costs?country=CA&province=BC&price=25000&sale_type=private\|dealer` | **$0.02** | Itemized Canadian used-vehicle closing costs for any of the 10 provinces + 3 territories (BC/AB/SK/MB/ON/QC/NB/NS/PE/NL/YT/NT/NU): provincial tax (PST/RST/QST/HST or GST-only) + transfer/registration/plate fees + inspection, per-line `sourceUrl` + confidence |
| GET | `/v1/purchase-costs?country=US&state=CA&price=25000&sale_type=private\|dealer` | **$0.02** | Itemized US used-vehicle closing costs for any of the 50 states + DC (sales/use/excise tax, title, first-year registration, inspection, dealer doc fee), per-line `sourceUrl` + confidence |
| GET | `/v1/prepurchase?vin=VIN&country=CA\|US` | **$0.25** | Whole-job pre-purchase bundle: normalized decode + safety recalls + known-issue/reliability summary + a jurisdiction-level CA/US ownership-cost estimate for the decoded vehicle, in ONE call (equivalent to 4 separate paid calls, composed in-process). Decode computed first — invalid VIN/decode failure is UNCHARGED; settles only if decode succeeds AND ≥2 of the 3 secondary sections are available (else UNCHARGED `insufficient_sections`). Cost section is an estimate — call `/v1/purchase-costs` for an exact itemized figure. Each section carries its own fetch provenance. 90-day-strictest composite cache |

Purchase-costs is ONE endpoint selected by `country=CA|US`: CA requires `province`, US requires `state` (same $0.02 price). Required params: `vin` (17 chars, no I/O/Q) on the VIN routes; `country` + `province`/`state` + `price` + `sale_type` on the purchase-cost route. There is NO separate reliability endpoint — its aggregates ship inside every `/v1/known-issues` response.

Optional CA purchase-costs params: `&buyer_has_plates=true` (selects plate-dependent fee lines, e.g. Ontario permit $32 vs permit + plate $59), `&family_gift=true` (jurisdiction's family/related-individual gift exemption, $0 tax, private sales only). AB + YT/NT/NU have no private-sale tax.

Optional US purchase-costs params: `&trade_in=5000` (deducted from tax base only where the state grants a FULL dealer trade-in credit), `&local_rate=1.5` (exact county/city surtax %; omitted → sales-tax line carries a range up to the state max). Special regimes are handled automatically (DC tiered title EXCISE; IL RUT-50 private-party flat fee; SC 5% IMF capped $500; AK/AZ/HI/MT/NV/NH/OR levy no state sales tax on private-party sales).

Prices are USD, settled as USDC (6 decimals) on Base.

## Paying (x402)

Paid endpoints are a flat price per call — decode $0.01, recalls $0.01, known-issues $0.05,
purchase-costs $0.02, prepurchase $0.25 — via x402 (USDC on Base). Server flow is
compute-first / settle-after: you are **never** charged for an error or a below-threshold
(insufficient-data) answer. Try every response shape for free first via `/v1/sample/*`. Agents
can use the `vindex-mcp` npm package (an MCP server) which handles payment, or read the full
flow at [api.vindexapi.dev/llms.txt](https://api.vindexapi.dev/llms.txt).

## Machine discovery

| Path | What |
|------|------|
| `/llms.txt` | This doc (concise) |
| `/llms-full.txt` | Extended agent doc |
| `/openapi.json` | OpenAPI 3.1 spec |
| `/discovery` | Discovery JSON (free/paid endpoint listing) |
| `/.well-known/x402` | x402 payment manifest |
| `/.well-known/agent-card.json` | A2A agent card |

## Errors & caveats

- **400** — invalid VIN (must be 17 chars, no I/O/Q) or bad params (missing `province`/`state`/`price`/`sale_type`).
- **402** — payment required / verification or settlement failed (you were **NOT** charged).
- **422** — vPIC could not resolve make/model/year for this VIN (`vpicErrorText` explains).
- **502** — an upstream public-data source was unavailable (served stale where possible).
- **Insufficient data** — known-issues below 15 complaints → **200** `{ "status": "insufficient_data", … }`, uncharged (not an error).

**Data sources & attribution:** NHTSA vPIC + api.nhtsa.gov (US federal, public domain) for decode, recalls, and complaints; Transport Canada vehicle-recall-database for Canadian recalls — *Contains information licensed under the Open Government Licence – Canada.*

**Disclaimer:** Informational vehicle data aggregated from public sources; not professional, legal, or purchasing advice; provided as-is without warranty. NOT a vehicle-history report (no liens/accidents/odometer). Recall/complaint data reflects the source databases at fetch time. Terms: https://api.vindexapi.dev/terms.txt
