---
name: toll402
description: 2,600+ pay-per-call tools for AI agents — read pages/PDFs, extract JSON, verify emails, FX rates, provenance (human vs synthetic), trusted-source lookup, a 4.6M-business verified directory, 50+ national ID validators, forge new tools, and provider APIs (SEO keyword/backlink data, social profiles and posts, people/company enrichment, ads, stocks and crypto, image/video generation). Pay per call with USDC via x402 (no account) or prepaid card credits (API key). Charged only on success.
metadata:
  version: 1.3.0
  homepage: https://toll402.dev
  docs: https://toll402.dev/llms.txt
  repository: https://github.com/toll402/toll402
license: MIT
---

# Toll402 — one gateway, every capability, pay per call

## When to use
- You need clean Markdown of a web page or PDF for reasoning (`read_url`, `pdf_to_text`).
- You need structured JSON from a page/text matching YOUR schema (`extract_structured`).
- You must know whether content is human-written or AI-generated, with evidence (`provenance`).
- You need facts from trusted sources with citations (`trusted_lookup`: Wikipedia, Wikidata, arXiv, Crossref, World Bank).
- You need to find or verify a real business anywhere in the world, its hours, services and how to book (`business_search`, `business_verify`, `business_details`, `business_shortlist`).
- You need third-party data: SEO keyword volume, backlinks and rank (Semrush, DataForSEO, Moz, SerpApi), TikTok/Instagram/YouTube/LinkedIn/X/Reddit profiles and posts, people and company enrichment (Hunter, Apollo, Crunchbase…), ad libraries, stock and crypto prices, image/video generation: `POST /v1/p/<endpoint id>` (browse at https://toll402.dev/catalog or `GET /v1/find?need=…`).
- A tool you need doesn't exist: describe it and `forge_tool` builds, tests and publishes it.
- Not sure which tool: `POST /v1/do { need, input }` routes for you.

## Setup (one of the two)
- `TOLL402_API_KEY`: prepaid-credits key (`tk_…`) that the operator buys by card at https://toll402.dev/credits. Sent as the `x-toll402-key` header. No crypto needed.
- `TOLL402_WALLET_KEY`: 0x private key of a wallet holding a few USDC on **Base** (eip155:8453); pays per call via x402, no account. Never paste it in chat or logs.
- Optional `TOLL402_MAX_USD` (default 0.25): hard cap per single x402 payment.
- Every call is paid; there is no free tier. Discovery endpoints (`/v1/find`, `/v1/catalog`, `/v1/spec/…`) are free.

## How to call (any language)
1. Discover (free): `GET https://toll402.dev/v1/find?need=<what you need>` → ranked tools with `url`, `price`, `inputSchema`, `example`.
2. Call: `POST <url>` with a JSON body (send `x-toll402-key` if you use credits). Success → `{ ok: true, result: {...} }`; the headers `x-toll402-charged` / `x-toll402-balance` show the debit and what is left.
3. If the response is **402** without a key: pay with x402 and retry (the clients below do this automatically). With a key it means the balance is empty (`insufficient_credits`); ask the operator to top up. You are charged **only on 2xx**; errors are never settled. A `402 key_daily_cap` means this agent key hit the daily limit its operator set: stop and report, do not retry.
4. **Image and video generation** answer `202` with `result.job.id` (credits only). Poll `GET https://toll402.dev/v1/jobs/<id>` with the same key (images every ~10 s, video every 30-60 s) until `succeeded` (`result.urls`, download promptly) or `failed` (refunded).
5. **After you use an answer, rate it**: `POST https://toll402.dev/v1/calls/<x-toll402-call-id>/review {"useful": true|false, "reason": "one sentence"}`. It is free and moves tool ranking. Lost an answer you paid for? `GET /v1/calls/<id>` returns it for 24 h; `GET /v1/calls?days=1` lists your calls.

### JavaScript
```js
import { Toll402 } from "toll402-client";              // npm i toll402-client
const t = new Toll402({ apiKey: process.env.TOLL402_API_KEY });            // credits
// or: new Toll402({ walletKey: process.env.TOLL402_WALLET_KEY, maxUsdPerCall: 0.25 })   // x402
const page = await t.read("https://example.com");         // $0.002
const biz  = await t.business.search({ city: "Ciudad de México", category: "dentist", minLevel: "corroborated", limit: 5 });
const seo  = await t.call("moz.web.url.metrics", { targets: ["example.com"] });   // any provider endpoint by id
const any  = await t.do("convert 100 usd to mxn", { base: "USD", quote: "MXN", amount: 100 });
t.lastCharge;  // { usd, balanceUsd, callId } after a credits-paid call
await t.review(true, { reason: "accurate" });            // rate the last call
const img = await t.generate("p/replicate.image-gen.flux-schnell", { input: { prompt: "a red kite" } }); // waits for the task
```
### Python
```python
from toll402 import Toll402                                # pip install toll402  (add "[pay]" for x402)
t = Toll402(api_key=os.environ.get("TOLL402_API_KEY"))    # or Toll402(wallet_key=...)
t.read("https://example.com"); t.business.verify(website="https://example.com", name="Example")
t.call("tikhub.tiktok.user.profile", {"uniqueId": "tiktok"}); t.last_charge
```
### curl
```bash
curl -X POST https://toll402.dev/v1/read -H 'x-toll402-key: tk_…' -H 'content-type: application/json' -d '{"url":"https://example.com"}'
curl -i -X POST https://toll402.dev/v1/read -H 'content-type: application/json' -d '{"url":"https://example.com"}'   # no key → 402 with x402 requirements
```
### MCP (Claude Code / Cursor / OpenClaw MCP)
```json
{ "mcpServers": { "toll402": { "command": "npx", "args": ["-y", "toll402-mcp"], "env": { "TOLL402_API_KEY": "tk_..." } } } }
```
Remote, no install: `https://toll402.dev/mcp` (send `x-toll402-key` as a header, or `?key=tk_…` in the URL when headers are impossible). Operators manage balance and activity at https://toll402.dev/account.

## Tool groups and prices (USD per call)
| Group | Tools | Price |
|---|---|---|
| Reading | read_url $0.002 · pdf_to_text $0.005 | cheap, no LLM |
| Data | verify_email $0.001 · fx_rate $0.001 · community tools (hn_top, github_repo_stats, npm_package_info, crypto_price, url_status, rss_latest, json_schema_validate, text_stats, wikipedia_summary, ip_geolocate) $0.001–$0.005 | |
| Validators | RFC, CURP, CPF/CNPJ, CUIT, RUT, NIT, VAT, EIN, IBAN, SIRET and 40+ more national IDs | $0.001–$0.002 |
| Trust | provenance $0.01 (deep $0.04) · trusted_lookup $0.01 (synthesized $0.04) | evidence-based |
| Businesses | business_search $0.005 · business_verify $0.01 · business_details $0.08 · business_shortlist $0.25 | any city seeds on demand |
| LLM | extract_structured $0.06 · summarize $0.05 · judge_output $0.07 | hard token caps |
| Provider APIs | 2,400+ endpoints from 30+ vendors (SEO, social, enrichment, ads, market data, AI generation) at `/v1/p/<id>` | vendor rate + 25%, from $0.001 |
| Meta | do $0.02 (routes + runs tools ≤ maxPriceUsd) · forge_tool $0.25 (new tool, sandbox-tested, published) | |
| External | 2,800+ other x402 services listed at /v1/tools?kind=external (proxied, +15%) | |

## Safety rules
- Charged only on HTTP 2xx. 4xx/5xx are never settled or debited.
- Keep `TOLL402_MAX_USD` low (0.25 default). Prefer `find` (free) before paying.
- Business data: scores aggregate dated public evidence; `unverified` means unknown, not fake. Cite `verification.lastVerifiedAt`.
- Provenance is evidence + calibrated score, not a binary verdict; treat `uncertain` as unknown.
- Never log or echo the wallet key or the credits key. Report what you spent when asked: `GET /v1/account` (credits) lists every debit.
