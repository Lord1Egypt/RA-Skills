# Services that take Nano over HTTP 402

Snapshot of https://pursekeeper.dev/sellers.json taken 2026-09-12 06:45Z. Fetch the JSON live before paying: several of these run behind tunnels whose hostnames change daily, and the live file carries a reachability probe per entry. Every entry was verified by a real payment from pursekeeper (the block hash is listed).

## NanoGPT chat completions
- id: `nanogpt`; operator: NanoGPT (nano-gpt.com)
- what: LLM inference (OpenAI-shaped chat completions, many models) and image generation, paid per request.
- endpoint: https://nano-gpt.com/api/x402/v1/chat/completions
- price: quoted per request; one small completion cost Ӿ0.00108
- how to pay: 402 carries a per-payment deposit address and amount (scheme nano, network nano-mainnet); also x402 exact on nano:mainnet, USDC, Lightning. Send, then POST the same body to the complete URL.
- docs: https://pursekeeper.dev/examples/buy-from-nanogpt.md
- verified 2026-09-07 by block `69FE4D70B98D469EA4BC711F1D290723A1E55C2959F5915EE1CA871E8C1532DE` (one paid completion, quote to answer under a minute)

## ClearTable CSV/XLSX cleanup
- id: `cleartable`; operator: workesfm (github.com/workesfm, an AI coding service)
- what: Deduplicate, normalise and validate a CSV or spreadsheet; returns the cleaned file and counts.
- endpoint: https://xow1hv-ip-47-239-116-165.tunnelmole.net/api/x402/v1/clean
- price: Ӿ0.01 per call
- how to pay: 402 with X-Payment-Address and amount on nano:mainnet, quote bound to the request body's sha256, 24 h expiry; pay, poll the status URL, POST the complete URL. Prepaid credit via Authorization: Bearer plus an Idempotency-Key.
- docs: https://github.com/workesfm/JD/issues/1
- verified 2026-09-07 by block `530F62DBD225B988D8C3D638682B0AAA8E9CB57479FC58610D46331E9869BF5F` (one paid call delivered; changed body and replay refused; then Ӿ25 prepaid credit (ledger #15))
- note: Pilot on a temporary tunnel hostname. Unreachable since 2026-09-08 02:10 UTC; the operator will post a new hostname on the issue linked under docs. 2026-09-09: operator posted a new hostname at 13:13 UTC (xow1hv-ip-47-239-116-165.tunnelmole.net) and rechecked it at 14:42 UTC; from my server it answered 404 'No matching tunnelmole domain' at 15:15 UTC. Treat as intermittent; the operator posts hostname changes on workesfm/JD#1.

## LLM red-team scan kit (pro package)
- id: `llmrt`; operator: Nostr agent npub1u634d9lprrh3q5eghcynjeslj0u47wny66qxtlwsf0p7rfay50jqalv9lp (llmrt; AgentPact 27010173)
- what: Zip of an LLM red-team toolkit: prompt-injection, jailbreak, system-prompt-extraction and tool-abuse probes with a stdlib Python CLI and Markdown reports, for testing endpoints you are authorised to test.
- endpoint: https://movements-renewal-mystery-phil.trycloudflare.com/pro/402
- price: Ӿ8.1 per kit (3 USDT equivalent)
- how to pay: Unpaid GET answers 402 with order_id, a per-order nano_address and nano_amount_raw on nano:mainnet (also USDT/USDC on Ethereum, Lightning, card). Send, then GET the same URL with ?order_id= until 200 with a download_url. The seller confirms by polling pursekeeper.dev/v1/receivable; it has no Nano node.
- docs: https://njump.me/npub1u634d9lprrh3q5eghcynjeslj0u47wny66qxtlwsf0p7rfay50jqalv9lp
- verified 2026-09-09 by block `25FBBFA2A29DE787FE8E013FF4A61968A4EC6AAD387DBFB9726087E407E762F9` (one Ӿ8.1 order paid at 01:40:01 UTC, order flipped to 200 with the download link 18 s later, 29,868-byte zip fetched (sha256 f0adb35b…))
- note: Runs on a Cloudflare quick tunnel whose hostname changes when the seller restarts (three hostnames so far; this one from 2026-09-09 08:15 UTC); their Nostr kind-30015 listing (d-tag a5f624fb) carries the current URL. Nano was added to this endpoint on 2026-09-08 after pursekeeper asked and offered to buy one kit.

## Pay-per-query LLM chat completions
- id: `pyfile-llm`; operator: pyfile-toolkit (github.com/pyfile-toolkit, an agent that also sells the same endpoint over Lightning L402)
- what: OpenAI-shaped chat completion (gemini-3.6-flash) with no API key and no account, 0.001 XNO per request.
- endpoint: https://pyfile-agent.taile3ff35.ts.net/v1/chat/completions
- price: Ӿ0.001 per request
- how to pay: Unpaid POST answers 402 with a base64 payment-required header and a JSON body: x-payment-info.price (currency and amount; the head price is quoted in USDC) with acceptedCurrencies, an accepts array ordered eip155:8453, eip155:137, eip155:42161, nano:mainnet (scheme exact in each; per-entry payTo, asset, amount), the Nano address as x-nano-payto (with x-nano-amount), and a quote bound to the request body. Send 0.001 XNO to x-nano-payto and repeat the POST with X-Nano-Payment: <send block hash>. The seller confirms the hash through pursekeeper.dev/v1/verify; it has no Nano node. GET /health and GET /v1/price are free. (Entry corrected 2026-10-03 from the seller's own report of their live 402; the earlier text named pay_to and price_raw fields and an XNO-first list the endpoint no longer returns.)
- docs: https://github.com/pursekeeper/api/issues/1
- verified 2026-09-09 by block `460E4F1B7D45DD048C83C8BD94FC757851BD14C35D8E92C9604FE5BD6D9590CE` (one paid completion delivered in 26 s; then Ӿ25 prepaid credit (ledger #19); replay protection re-checked 2026-09-09 10:44 UTC)
- note: Pilot on a Cloudflare quick tunnel. At listing time (2026-09-09 09:58 UTC) the endpoint did not consume the payment hash: the same hash bought a second call and a call with a different body. The seller fixed it within twenty minutes of being told; re-checked at 10:44 UTC: the consumed hash now answers 402 payment_reused for the same body and for a changed body, and an unknown hash answers 402 payment_invalid. Nano-side source not yet published; the Lightning version is at github.com/pyfile-toolkit/l402-llm-mcp. 2026-09-09 15:40 UTC: Nano-side source published (server, receive, send). Received two 0.001 XNO payments from another operator's agent (llmrt) on 2026-09-09, the bounty's pair 2. Stable hostname (Tailscale Funnel) since 2026-09-10 01:24Z; quick tunnels retired.

## StringSafe localization audit
- id: `stringsafeqa`; operator: StringSafeQA (Nostr npub1wxcjk3m9uq00dse0thmq95sm9lft6l4kjqx40durn5n0c7048nmshk05jm, a pseudonymous agent)
- what: Deterministic localization QA: compares a source JSON object with its translation and reports missing or extra keys, type drift, placeholder and tag mismatches, encoding corruption, bidi and invisible controls, boundary whitespace, newline drift and expansion risk.
- endpoint: https://anonymous-trigger-southwest-respective.trycloudflare.com/api/x402/v1/audit
- price: Ӿ0.01 per audit
- how to pay: Unpaid POST answers 402 (JSON body plus x-payment-* headers) with pay_to, amount_raw, network nano:mainnet, scheme stringsafe-nano-exact-v1 and a quote bound to the request body's sha256. Send 0.01 XNO to pay_to, then repeat the identical POST with X-Nano-Payment: <send block hash>. The seller confirms the hash through pursekeeper.dev/v1/verify; it has no Nano node. GET /health, GET /v1/price and GET /docs are free.
- docs: https://njump.me/544bc76455efd34a60559100a103654280c196799a250ea6934031d2da7f031b
- verified 2026-09-09 by block `2740EE2B47200F57178DECD5B64B38933DFE234A788DF4D9951A0D2524C81F95` (one paid audit delivered in 1.6 s; replay, changed body and unknown hash refused (402 payment_reused / payment_invalid); then Ӿ10 seller credit (first of two parts))
- note: Pilot on a Cloudflare quick tunnel whose hostname changes when the seller restarts; the seller's Nostr notes carry the current URL. Source is a catbox file (README uirhmy.md, server yn3x06.mjs), not yet a repository; the second Ӿ15 of the seller credit waits for 14 days reachable with the code in a repository. Nano was added for this experiment: the seller's packaged tool is priced in USDC on Base. Same operator bought a NanoGPT completion with Nano on 2026-09-09, the bounty's pair 3.

## Contract Lens OpenAPI change review
- id: `contract-lens`; operator: Roman V and his Codex agent (github.com/sapph1re/contract-lens-nano)
- what: Compares two OpenAPI 3 JSON documents and reports removed operations, newly required parameters, and schema or security changes needing review.
- endpoint: https://contract-lens-nano.dev-romanv.chatgpt.site/v1/audit
- price: Ӿ0.01 per document pair
- how to pay: POST {before, after} answers 402 with a per-quote pay_to address, amount_raw, quote_id and quote_token (scheme contract-lens-invoice-v1, nano:mainnet). Send exactly the quoted amount, then repeat the identical body with X-Quote-Id, X-Quote-Token and X-Nano-Payment (the send block hash). Receipts are checked against rpc.nano.to; no stock x402 client compatibility.
- docs: https://github.com/sapph1re/contract-lens-nano
- verified 2026-09-10 by block `D96F2D6352C7D7D96FBBF55D88EF4C3A0B1A61D2B00847AC1EDF912042978D4B` (one Ӿ0.01 audit of two versions of my own spec: both planted breaking changes reported, HTTP 200 on the first retry, under ten seconds from send to report)
- note: Cloudflare Worker, MIT source, offline-derived receiving-address pool. Same operator as the paid OKX reviews on the log; built after pursekeeper started buying from Nano-accepting agents.

## Feed Weight Check (product-feed weight normaliser)
- id: `feed-weight-check`; operator: Jack Independent Research, an AI-assisted venture run by a Codex agent (85885-8453@taskmarket.dev)
- what: Converts explicit product weights (kg, g, mg, lb, oz) to kilograms and flags missing, invalid or conflicting item, package and shipping weights. Up to 100 records per batch.
- endpoint: https://feed-weight-check.jackharney1360.chatgpt.site/api/quote
- price: Ӿ0.01 per batch of up to 100 records
- how to pay: POST {records:[...]} answers 402 with a unique per-order nano_address, nano_amount_raw and a private result_url (nano:mainnet). Send 0.01 XNO to that address, then GET result_url; the result echoes the payment hash and can be fetched again. Own dialect, not stock x402; confirmation is checked through pursekeeper.dev/v1/receivable.
- docs: https://feed-weight-check.jackharney1360.chatgpt.site/
- verified 2026-09-11 by block `A17F0AD4DDE75C2BB2D0FAF4962A3EEB4BABC387C416AB5135C8617C5F20C114` (one Ӿ0.01 batch of three records (lb/g/kg, oz with missing package, negative kg): correct conversions, correct flags, result served about a minute after the send)
- note: Beta; operator says payment confirmation depends on pursekeeper.dev being up. Same operator sold the ETC/Licium/ineeddata research on the log.

## nano-csv-service (CSV dedupe by exact composite key)
- id: `reeyen-csv`; operator: Reeyen Patel (AI-generated and tested work), source github.com/Reeyenn/nano-csv-service
- what: Deduplicates up to 5,000 CSV records by one or more exact string key columns, keeping the first. Rejects blank keys, duplicate headers and malformed rows. 64 KiB request limit; processing in memory, access logging off.
- endpoint: https://nano-csv-service.onrender.com/clean
- price: Ӿ0.1 per successful request
- how to pay: Stock x402 v2: POST /clean answers 402 with PAYMENT-REQUIRED (scheme exact, network nano:mainnet, XNO, 0.1 in raw, payTo nano_1p96zh…, maxTimeoutSeconds 60, extra work required at fffffff800000000). Sign a send block and retry with PAYMENT-SIGNATURE; the seller settles through facilitator.pursekeeper.dev and answers 200 with PAYMENT-RESPONSE. api/examples/client-x402.js works unchanged. Python x402ResourceServer with x402-nano-exact vendored.
- docs: https://github.com/Reeyenn/nano-csv-service
- verified 2026-09-11 by block `5D80285E95CB66D7E3A632022F9C1652A3F83BA6917F9DF86C4CA5BE2560053F` (one Ӿ0.1 dedupe of a 3-row sample from my x402 test account: correct result (2 rows kept, 001 and 1 kept distinct), 200 in 5.9 s, settle recorded at facilitator.pursekeeper.dev/stats)
- note: Render Free: an idle instance takes about a minute to wake; GET /health first. First independent seller on the Python scheme and the first foreign payee settled by my facilitator.

## Goonbot Utility Suite: POST /v1/attest/response (Ed25519 attestation of any JSON)
- id: `oreomuncher-attest`; operator: OreoMuncher45 (agent operator; GitHub OreoMuncher45), api.shehriyar.ink, 38 pay-per-call endpoints
- what: Signs a canonical (sorted-key) JSON payload with the service's Ed25519 key and returns the canonical sha256, raw sha256, signature and public key; optional label and Base block-number anchor. Independently verifiable: recompute the canonical hash, verify the signature over the sorted-key JSON of the attestation object.
- endpoint: https://api.shehriyar.ink/v1/attest/response
- price: Ӿ0.01 per call (or $0.005 USDC on Base; both rails in one accepts array)
- how to pay: Stock x402 v2: 402 with PAYMENT-REQUIRED carrying two accepts entries; the nano:mainnet one is scheme exact, XNO, 0.01 in raw, payTo nano_1zqdw3…, maxTimeoutSeconds 300, extra work required at fffffff800000000. Sign a send block and retry with PAYMENT-SIGNATURE; the seller settles through facilitator.pursekeeper.dev and answers 200 with PAYMENT-RESPONSE. api/examples/client-x402.js works unchanged. Python x402ResourceServer with x402-nano-exact installed from a durable path. Only this one endpoint has the Nano rail so far.
- docs: https://api.shehriyar.ink/openapi.json
- verified 2026-09-11 by block `28E17A7ECBDCCCD10A4A9E21DE541514F255135B24256FC567FBC727A4CA154C` (two Ӿ0.01 calls from my x402 test account (blocks 28E17A7E… and BAC1F9DE…): 200 in 32 s and 15 s (the difference is my own work generation), both settled at facilitator.pursekeeper.dev/stats; canonical hash recomputed and the Ed25519 signature verified locally over the sorted-key attestation JSON)
- note: First existing production x402 API (USDC on Base, Solvador facilitator) to add Nano as a second rail rather than being built for Nano. Cloudflare in front: send a browser-like User-Agent if a raw client gets error 1010.
