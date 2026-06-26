---
name: spraay-compute
description: Rent GPU compute, run AI model inference (LLM chat, image, video, speech-to-text, text-to-speech, embeddings), and buy prepaid compute-futures credits — all paid in USDC over x402, no API keys and no accounts. Use this skill whenever an agent needs to rent GPU time, run or batch model inference, generate images/video/audio, create text embeddings for RAG, estimate compute cost before spending, or lock in discounted compute by prepaying into a compute-futures credit balance. Trigger it for any phrasing like "rent GPU", "run inference", "generate an image/video", "transcribe audio", "text to speech", "get embeddings", "prepay compute", "compute credits", or "compute futures", even when x402 or Spraay is not named.
---

# Spraay Compute & Futures 💧

Two capabilities, equal billing:

1. **Compute rental** — pay-per-call GPU and model inference (LLM, image, video, TTS, STT, embeddings) via the Spraay x402 gateway. One HTTP request, one USDC payment, the result comes back. No keys, no signup.
2. **Compute futures** — prepay USDC into a credit balance and draw it down per job at a tier discount (up to 15%). Settle once, run many jobs with no per-call payment, refund whatever is left.

Everything settles in **USDC over x402 V2** on **Base mainnet** and **Solana mainnet**. The gateway returns a standard HTTP `402 Payment Required` with payment requirements; the agent pays via its x402 client and retries. Base address `0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913` (USDC); Solana mint `EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v`.

Base URL: `https://gateway.spraay.app`

## When to use which

- **One-off or low-volume job** → call the relevant compute endpoint directly and pay per call.
- **Repeated jobs / known budget / cost-sensitive agent** → open a compute-futures account once, then `execute` against the balance. Cheaper (tier discount), and each job costs only a `$0.001` settlement instead of the full per-call gate price.
- **Unsure of cost** → hit `POST /api/v1/compute/estimate` (free) first, or `GET /api/v1/compute-futures/pricing` (`$0.001`) for tier and per-model costs.

## The x402 flow (how every paid call works)

1. Agent sends the request (e.g. `POST /api/v1/compute/text-inference`).
2. Gateway responds `402 Payment Required` with `accepts` (price, network, payTo).
3. Agent's x402 client signs an EIP-3009 (Base) or SPL (Solana) USDC authorization for the quoted amount.
4. Agent retries with the `X-PAYMENT` header (Base) / `X-Solana-Tx` header (Solana).
5. Gateway verifies/settles via the facilitator and returns the result.

Any x402-aware client handles this automatically (`@x402/fetch`, `x402-axios`, the Spraay MCP server, or an OpenClaw payment skill such as ClawPay/Vault-0). The agent only needs a funded wallet.

## Quick endpoint reference

Prices below are the **x402 gate price per call** (what the agent pays at the 402). Free endpoints need no payment.

**GPU / Compute rental**
| Endpoint | Method | Price | Purpose |
| --- | --- | --- | --- |
| `/api/v1/gpu/run` | POST | $0.06 | Run any Replicate model (image, video, LLM, audio, utility) |
| `/api/v1/gpu/status/:id` | GET | $0.005 | Poll an async GPU prediction |
| `/api/v1/gpu/models` | GET | free | List GPU model shortcuts |

**Model inference**
| Endpoint | Method | Price | Purpose |
| --- | --- | --- | --- |
| `/api/v1/compute/text-inference` | POST | $0.03 | LLM chat/completion — 11 models 3B–405B (Chutes AI / Bittensor SN64, OpenRouter) |
| `/api/v1/compute/image-generation` | POST | $0.03 | Text-to-image — FLUX Schnell/Dev/Pro, SDXL |
| `/api/v1/compute/video-generation` | POST | $0.50 | Text-to-video — MiniMax Video 01, Wan 2.1 (async) |
| `/api/v1/compute/text-to-speech` | POST | $0.03 | TTS / voice synthesis |
| `/api/v1/compute/speech-to-text` | POST | $0.02 | Whisper Large V3 transcription, 100+ languages |
| `/api/v1/compute/embeddings` | POST | $0.005 | Text/vector embeddings for RAG and semantic search |
| `/api/v1/compute/batch` | POST | $0.05 | Up to 50 mixed jobs in one payment, 10% batch discount |
| `/api/v1/compute/status/:jobId` | GET | $0.001 | Poll an async compute job (video, batch items) |
| `/api/v1/compute/models` | GET | free | List all compute models with pricing |
| `/api/v1/compute/estimate` | POST | free | Estimate cost before committing |

**Compute futures (prepaid credits)**
| Endpoint | Method | Price | Purpose |
| --- | --- | --- | --- |
| `/api/v1/compute-futures/deposit` | POST | $0.01 | Open a prepaid credit account. Tiers: $10+ (5%), $50+ (10%), $200+ (15%) |
| `/api/v1/compute-futures/balance` | GET | $0.001 | Balance, tier, discount, usage stats |
| `/api/v1/compute-futures/execute` | POST | $0.001 | Run a job, deduct from balance (no per-call x402, discount applied) |
| `/api/v1/compute-futures/history` | GET | $0.002 | Full usage ledger |
| `/api/v1/compute-futures/refund` | POST | $0.01 | Refund unused balance to the depositor |
| `/api/v1/compute-futures/pricing` | GET | $0.001 | Tier discounts, per-model costs, bulk-discount info |

For exact request/response schemas, required fields, and model lists, read `references/endpoints.md`. For runnable end-to-end examples (per-call and the full futures lifecycle), read `examples/quickstart.md`.

## Headline workflows

**Rent compute (per-call), e.g. LLM inference**
```
POST /api/v1/compute/text-inference
{ "messages": [{ "role": "user", "content": "Summarize this contract: ..." }], "model": "auto" }
→ 402 → pay $0.03 USDC → retry → { provider, model, choices: [...], usage, price_usdc }
```

**Run a GPU model on Replicate**
```
POST /api/v1/gpu/run
{ "model": "flux-pro", "input": { "prompt": "a serene mountain lake at sunset" } }
→ 402 → pay $0.06 USDC → retry → { id, status, model, output: ["https://replicate.delivery/..."] }
```

**Compute futures lifecycle (prepay → draw down → refund)**
```
POST /api/v1/compute-futures/deposit   { "depositor": "0xYou", "amount": "50" }
  → pay $0.01 → { computeFuture: { id: "CFE-ABC12345", tier: "scale", discount: "10% discount", balanceRemaining: "50 USDC" } }
POST /api/v1/compute-futures/execute   { "futuresId": "CFE-ABC12345", "type": "text-inference", "messages": [...] }
  → pay $0.001 → { billing: { charged: "$0.027", balanceRemaining: "$42.473 USDC" }, compute: { model: "Llama 3.3 70B" } }
POST /api/v1/compute-futures/refund    { "futuresId": "CFE-ABC12345", "caller": "0xYou" }
  → pay $0.01 → { refund: { refundAmount: "42.50 USDC", jobsExecuted: 15 } }
```

## Rules and gotchas

- **Async endpoints** (`video-generation`, some `batch` items) return a `prediction_id` / `poll_url`. Poll `/compute/status/:jobId` until `status: "completed"`.
- **`execute` only deducts from a prepaid balance** — it does not run a per-call x402 payment for the compute itself; you only pay the `$0.001` settlement. Make sure the futures account has enough balance or the job is rejected.
- **Refunds are depositor-only.** `caller` must equal the original `depositor`.
- **Use `auto` for `model`** when you don't care which model serves the request; the gateway routes to a sensible default for that job type.
- **Free before paid.** `compute/estimate`, `compute/models`, `gpu/models`, and `/.well-known/x402.json` cost nothing — use them to plan a call before spending.
- **Discovery:** the gateway publishes a machine-readable catalog at `https://gateway.spraay.app/.well-known/x402.json`. Point a discovery-driven agent there to enumerate live endpoints and prices.

## Provenance

This skill wraps the Spraay x402 Gateway compute surface (GPU/Compute, Compute Services, and Compute Futures / Category 22). Prices reflect the live gateway gate prices in USDC. If the gateway updates pricing or adds models, regenerate `references/endpoints.md` from `/.well-known/x402.json`.
