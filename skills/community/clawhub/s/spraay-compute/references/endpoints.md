# Spraay Compute & Futures — Endpoint Reference 💧

Base URL: `https://gateway.spraay.app`
Protocol: x402 V2. Settlement: USDC on Base mainnet (`eip155:8453`) and Solana mainnet.
Prices shown are the **x402 gate price per call** (the amount quoted in the `402` response). "free" endpoints require no payment.

## Contents
- [GPU / Compute rental](#gpu--compute-rental)
- [Model inference (Compute Services)](#model-inference-compute-services)
- [Compute Futures (prepaid credits)](#compute-futures-prepaid-credits)
- [Free / discovery endpoints](#free--discovery-endpoints)
- [Payment mechanics](#payment-mechanics)

---

## GPU / Compute rental

### POST /api/v1/gpu/run — $0.06
Run AI model inference via Replicate (image, video, LLM, audio, utility).
- Body: `{ model, input, version?, webhook? }`
- Required: `model`, `input`
- Example in: `{ "model": "flux-pro", "input": { "prompt": "a serene mountain lake at sunset" } }`
- Example out: `{ "id": "abc123", "status": "succeeded", "model": "black-forest-labs/flux-1.1-pro", "output": ["https://replicate.delivery/..."] }`

### GET /api/v1/gpu/status/:id — $0.005
Check prediction status for async jobs.
- Out schema: `{ id, status, output }`

### GET /api/v1/gpu/models — free
List GPU model shortcuts.

---

## Model inference (Compute Services)

### POST /api/v1/compute/text-inference — $0.03
LLM chat completion and text generation. 11 models from 3B to 405B parameters. Providers: Chutes AI (Bittensor SN64), OpenRouter. Pick a model or use `auto`.
- Body: `{ messages, model?, max_tokens?, temperature? }`
- Required: `messages`
- Example in: `{ "messages": [{ "role": "user", "content": "Classify this wallet address" }], "model": "auto" }`
- Example out: `{ "provider": "chutes", "model": "meta-llama/Llama-3.3-70B-Instruct", "choices": [{ "message": { "content": "..." } }], "usage": { "total_tokens": 150 }, "price_usdc": "0.030" }`

### POST /api/v1/compute/image-generation — $0.03
Text-to-image. FLUX Schnell, FLUX Dev, FLUX Pro, Stable Diffusion XL via Replicate.
- Body: `{ prompt, model?, width?, height?, num_outputs? }`
- Required: `prompt`
- Example out: `{ "provider": "replicate", "model": "black-forest-labs/flux-schnell", "images": [{ "url": "https://...", "width": 1024, "height": 1024 }], "price_usdc": "0.030" }`

### POST /api/v1/compute/video-generation — $0.50
Text-to-video. MiniMax Video 01, Wan 2.1 via Replicate. **Async** — poll `/compute/status/:jobId` for the result.
- Body: `{ prompt, model?, duration_seconds? }`
- Required: `prompt`
- Example out: `{ "status": "processing", "prediction_id": "abc123", "poll_url": "/api/v1/compute/status/abc123", "price_usdc": "0.500" }`

### POST /api/v1/compute/text-to-speech — $0.03
TTS / voice synthesis.
- Body: `{ text, model?, language? }`
- Required: `text`
- Example out: `{ "status": "completed", "audio_url": "https://...", "price_usdc": "0.030" }`

### POST /api/v1/compute/speech-to-text — $0.02
Whisper Large V3 transcription / speech recognition. 100+ languages.
- Body: `{ audio_url | audio, model?, language? }`
- Required: audio source

### POST /api/v1/compute/embeddings — $0.005
Text/vector embeddings for RAG and semantic search (Chutes).
- Body: `{ input, model? }`
- Required: `input`
- Example out: `{ "data": [{ "embedding": [0.0023], "index": 0 }], "usage": { "total_tokens": 5 }, "price_usdc": "0.005" }`

### POST /api/v1/compute/batch — $0.05
Submit up to 50 jobs in a single x402 payment with a 10% batch discount. Mix any compute types (text-inference, image-generation, TTS, STT, embeddings, video).
- Body: `{ jobs }`
- Required: `jobs`
- Example in: `{ "jobs": [{ "type": "text-inference", "messages": [{ "role": "user", "content": "Classify 0x..." }] }, { "type": "image-generation", "prompt": "Company logo" }] }`
- Example out: `{ "batch_id": "batch_abc123", "jobs_submitted": 2, "total_cost_usdc": "0.054", "results": [] }`

### GET /api/v1/compute/status/:jobId — $0.001
Poll async compute job status (video generation, in-flight batch items).

### GET /api/v1/compute/models — free
List all available compute models with pricing.

### POST /api/v1/compute/estimate — free
Price estimation before committing to a job.

---

## Compute Futures (prepaid credits)

Category 22. Prepay USDC into a credit account, draw it down per job at a tier discount, refund what's left. `execute` charges only a `$0.001` settlement instead of the full per-call gate price, and applies the tier discount to the underlying model cost.

Tier discounts by deposit size: **$10+ → 5%**, **$50+ → 10%**, **$200+ → 15%**.

### POST /api/v1/compute-futures/deposit — $0.01
Deposit USDC to create a prepaid compute credit account.
- Body: `{ depositor, amount, expiresInDays? }`
- Required: `depositor`, `amount`
- Example out: `{ "status": "active", "computeFuture": { "id": "CFE-ABC12345", "tier": "scale", "discount": "10% discount", "balanceRemaining": "50 USDC" } }`

### GET /api/v1/compute-futures/balance — $0.001
Check remaining balance, tier, discount, and usage stats.
- Query: `{ futuresId }`

### POST /api/v1/compute-futures/execute — $0.001
Execute a compute job and deduct the cost from the prepaid balance. No per-call x402 for the compute itself; the tier discount is applied automatically.
- Body: `{ futuresId, type, model?, messages?, prompt? }`
- Required: `futuresId`, `type`
- `type` is one of: `text-inference`, `image-generation`, `video-generation`, `text-to-speech`, `speech-to-text`, `embeddings`
- Example out: `{ "status": "completed", "billing": { "charged": "$0.027", "balanceRemaining": "$42.473 USDC" }, "compute": { "type": "text-inference", "model": "Llama 3.3 70B" } }`

### GET /api/v1/compute-futures/history — $0.002
Full usage ledger — every job, model, price, and balance change.
- Query: `{ futuresId }`

### POST /api/v1/compute-futures/refund — $0.01
Refund unused balance back to the depositor. Depositor-only.
- Body: `{ futuresId, caller }`
- Required: `futuresId`, `caller` (must equal the original depositor)
- Example out: `{ "status": "refunded", "refund": { "refundAmount": "42.50 USDC", "jobsExecuted": 15 } }`

### GET /api/v1/compute-futures/pricing — $0.001
Tier discounts, per-model costs, and bulk-discount info.

---

## Free / discovery endpoints

| Endpoint | Method | Purpose |
| --- | --- | --- |
| `/` | GET | Gateway info |
| `/health` | GET | Health check |
| `/stats` | GET | Usage stats |
| `/.well-known/x402.json` | GET | Machine-readable discovery catalog (endpoints, prices, schemas) |
| `/api/v1/tokens` | GET | Supported tokens |
| `/api/v1/gpu/models` | GET | GPU model shortcuts |
| `/api/v1/compute/models` | GET | Compute models + pricing |
| `/api/v1/compute/estimate` | POST | Cost estimate before committing |

---

## Payment mechanics

1. Send the request to a protected endpoint.
2. Receive `402 Payment Required` with `accepts: [{ scheme: "exact", price, network, payTo }, ...]` for Base and Solana.
3. Sign a USDC authorization for the quoted price:
   - **Base**: EIP-3009 `transferWithAuthorization`, sent in the `X-PAYMENT` header. Use a `validBefore` at least 5 minutes out and a fresh 32-byte nonce per request.
   - **Solana**: SPL transfer, sent in the `X-Solana-Tx` header.
4. Retry the request with the payment header attached.
5. The gateway verifies/settles via the facilitator and returns the result.

USDC contracts:
- Base mainnet: `0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913`
- Solana mainnet mint: `EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v`

Any x402-aware client (`@x402/fetch`, `x402-axios`, the Spraay MCP server, or an OpenClaw payment skill) performs steps 2–4 automatically; the agent only needs a funded wallet.
