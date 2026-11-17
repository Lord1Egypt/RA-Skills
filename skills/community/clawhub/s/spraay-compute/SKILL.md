---
name: spraay-compute
description: "Pay-per-call GPU rental and AI inference (LLM, image, video, TTS, STT, embeddings) via Spraay x402 gateway. USDC micropayments on Base/Solana. Prepaid compute-futures with bulk discounts up to 15%. Keyless, agent-native — no API keys, no signup."
version: 1.1.0
metadata:
  openclaw:
    requires:
      bins:
        - bash
        - curl
---

# Spraay Compute & Futures 💧

Two capabilities, equal billing:

1. **Compute rental** — pay-per-call GPU and model inference (LLM, image, video, TTS, STT, embeddings) via the Spraay x402 gateway. One HTTP request, one USDC payment, the result comes back. No keys, no signup.
2. **Compute futures** — prepay USDC into a credit balance and draw it down per job at a tier discount (up to 15%). Settle once, run many jobs with no per-call payment, refund whatever is left.

Everything settles in **USDC over x402 V2** on **Base mainnet** and **Solana mainnet**. The gateway returns a standard HTTP `402 Payment Required` with payment requirements; the agent pays via its x402 client and retries. Base address `0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913` (USDC); Solana mint `EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v`.

Base URL: `https://gateway.spraay.app`

## ⚠️ Before you install — real money warning

> **Every paid call in this skill spends real USDC from a funded on-chain wallet.** This is not a testnet, sandbox, or simulated environment.
>
> - **Wallet charges:** Each compute call debits USDC from your agent's wallet via the x402 payment protocol. Costs range from $0.001 to $0.50 per call.
> - **Compute futures deposits:** The `deposit` endpoint locks real USDC (minimum $10) into a prepaid credit balance. This is an on-chain transaction that commits funds.
> - **Irreversible payments:** x402 payments are on-chain USDC transfers. Once settled, they cannot be reversed. Compute futures refunds return unused balance but cannot recover funds already spent on jobs.
> - **Autonomous spending risk:** If this skill is installed on an agent with a funded wallet, it may trigger paid calls based on user requests. Always require explicit human approval before any paid operation, especially deposits.
>
> **Recommendations:**
> - Use a dedicated wallet with limited funds
> - Always call the **free** `compute/estimate` or `compute/models` endpoint first to check cost
> - Set a per-session spending cap if your agent framework supports it
> - Require human confirmation before `compute-futures/deposit` (locks funds)

## When to use this skill

Use this skill when the user explicitly requests GPU compute, model inference, or Spraay-specific operations:

- **Explicit Spraay/x402 references** — "run this through Spraay", "use x402 compute", "call the Spraay gateway"
- **GPU rental** — "rent a GPU to run this model", "run this Replicate model"
- **Compute futures** — "prepay compute credits", "check my compute balance", "deposit into compute futures"
- **Specific inference via this gateway** — "generate an image via Spraay", "transcribe this audio through the x402 gateway"

> **Note:** Generic phrases like "generate an image" or "run inference" do not necessarily mean this skill should handle them — the user may prefer a local model, a free provider, or a different service. Only activate this skill when the user has indicated they want to use the Spraay x402 gateway or when this is the only available compute provider.

## When to use which billing mode

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

Prices below are the **x402 gate price per call** (what the agent pays at the 402). Free endpoints need no payment — **use free endpoints first** to plan before spending.

**GPU / Compute rental**

| Endpoint                 | Method | Price  | Purpose                                                     |
| ------------------------ | ------ | ------ | ----------------------------------------------------------- |
| `/api/v1/gpu/run`        | POST   | $0.06  | Run any Replicate model (image, video, LLM, audio, utility) |
| `/api/v1/gpu/status/:id` | GET    | $0.005 | Poll an async GPU prediction                                |
| `/api/v1/gpu/models`     | GET    | free   | List GPU model shortcuts                                    |

**Model inference**

| Endpoint                           | Method | Price  | Purpose                                                                          |
| ---------------------------------- | ------ | ------ | -------------------------------------------------------------------------------- |
| `/api/v1/compute/text-inference`   | POST   | $0.03  | LLM chat/completion — 11 models 3B–405B (Chutes AI / Bittensor SN64, OpenRouter) |
| `/api/v1/compute/image-generation` | POST   | $0.03  | Text-to-image — FLUX Schnell/Dev/Pro, SDXL                                       |
| `/api/v1/compute/video-generation` | POST   | $0.50  | Text-to-video — MiniMax Video 01, Wan 2.1 (async)                                |
| `/api/v1/compute/text-to-speech`   | POST   | $0.03  | TTS / voice synthesis                                                            |
| `/api/v1/compute/speech-to-text`   | POST   | $0.02  | Whisper Large V3 transcription, 100+ languages                                   |
| `/api/v1/compute/embeddings`       | POST   | $0.005 | Text/vector embeddings for RAG and semantic search                               |
| `/api/v1/compute/batch`            | POST   | $0.05  | Up to 50 mixed jobs in one payment, 10% batch discount                           |
| `/api/v1/compute/status/:jobId`    | GET    | $0.001 | Poll an async compute job (video, batch items)                                   |
| `/api/v1/compute/models`           | GET    | free   | List all compute models with pricing                                             |
| `/api/v1/compute/estimate`         | POST   | free   | Estimate cost before committing                                                  |

**Compute futures (prepaid credits) — ⚠️ deposits lock real USDC**

| Endpoint                          | Method | Price  | Purpose                                                                  |
| --------------------------------- | ------ | ------ | ------------------------------------------------------------------------ |
| `/api/v1/compute-futures/deposit` | POST   | $0.01  | Open a prepaid credit account. Tiers: $10+ (5%), $50+ (10%), $200+ (15%) |
| `/api/v1/compute-futures/balance` | GET    | $0.001 | Balance, tier, discount, usage stats                                     |
| `/api/v1/compute-futures/execute` | POST   | $0.001 | Run a job, deduct from balance (no per-call x402, discount applied)      |
| `/api/v1/compute-futures/history` | GET    | $0.002 | Full usage ledger                                                        |
| `/api/v1/compute-futures/refund`  | POST   | $0.01  | Refund unused balance to the depositor                                   |
| `/api/v1/compute-futures/pricing` | GET    | $0.001 | Tier discounts, per-model costs, bulk-discount info                      |

For exact request/response schemas, required fields, and model lists, read `references/endpoints.md`. For runnable end-to-end examples (per-call and the full futures lifecycle), read `examples/quickstart.md`.

## Headline workflows

**Rent compute (per-call), e.g. LLM inference**

> ⚠️ This example costs $0.03 USDC when executed.

```text
POST /api/v1/compute/text-inference
{ "messages": [{ "role": "user", "content": "Summarize this contract: ..." }], "model": "auto" }
→ 402 → pay $0.03 USDC → retry → { provider, model, choices: [...], usage, price_usdc }
```

**Run a GPU model on Replicate**

> ⚠️ This example costs $0.06 USDC when executed.

```text
POST /api/v1/gpu/run
{ "model": "flux-pro", "input": { "prompt": "a serene mountain lake at sunset" } }
→ 402 → pay $0.06 USDC → retry → { id, status, model, output: ["https://replicate.delivery/..."] }
```

**Compute futures lifecycle (prepay → draw down → refund)**

> ⚠️ The deposit step below locks $50 real USDC on-chain. Do not run this example without confirming the amount with the user.

```text
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
- **Human approval required** for `compute-futures/deposit` (locks funds) and any operation the user has not explicitly requested.

## Changelog

### v1.1.0

- **Added YAML frontmatter permissions** — declared `bins: [bash, curl]` under `metadata.openclaw.requires` to match actual runtime dependencies. Fixes "MCP Least Privilege" audit finding.
- **Added real-money USDC warning** — prominent disclosure that all paid calls spend real USDC from a funded wallet, including privacy and billing risk notes. Fixes 3 "Missing User Warnings" findings.
- **Narrowed trigger guidance** — replaced broad activation phrases with specific criteria requiring explicit Spraay/x402 references. Fixes "Vague Triggers" audit finding.
- **Added cost warnings to examples** — every quickstart and inline example now shows the USDC cost before the code block so agents don't auto-fire paid calls without disclosure.
- **Added human approval rules** — `compute-futures/deposit` and any unprompted paid operation now require explicit user confirmation.
- **Updated description** — tighter, keyword-rich, accurate capability disclosure within 300-char limit.

### v1.0.0

- Initial release with 20 endpoints across GPU rental, model inference, and compute futures.

## Related terms

GPU rental, serverless inference, pay-per-call AI, USDC compute payments,
x402 micropayments, agent compute provider, Replicate GPU proxy,
prepaid inference credits, bulk compute discount, keyless model access,
Base chain, Solana, autonomous agent payments, machine-payable API

## Provenance

This skill wraps the Spraay x402 Gateway compute surface (GPU/Compute, Compute Services, and Compute Futures / Category 22). Prices reflect the live gateway gate prices in USDC. If the gateway updates pricing or adds models, regenerate `references/endpoints.md` from `/.well-known/x402.json`.
