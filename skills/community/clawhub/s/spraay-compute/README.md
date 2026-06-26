# Spraay Compute & Futures — OpenClaw Skill 💧

GPU compute, AI model inference, and prepaid **compute futures** for AI agents — paid in USDC over x402, no API keys and no accounts.

Compatible with OpenClaw, Claude Code, Cursor, GitHub Copilot, Codex, Gemini CLI, and 18+ other agents via the Vercel Skills CLI.

## Install

OpenClaw / ClawHub:
```
npx clawhub install spraay-compute
```

Vercel Skills CLI (Claude Code, Cursor, Codex, Gemini CLI, etc.):
```
npx skills add plagtech/spraay-compute
```

Or paste this repo's URL into your OpenClaw agent and it will install the skill automatically.

## What it does

Two capabilities at equal billing, both settled in USDC over x402 V2 on **Base mainnet** and **Solana mainnet**:

### Compute rental (pay per call)
- **GPU run** — any Replicate model (image, video, LLM, audio, utility) — `$0.06`
- **Text inference** — LLM chat/completion, 11 models 3B–405B via Chutes AI (Bittensor SN64) + OpenRouter — `$0.03`
- **Image generation** — FLUX Schnell/Dev/Pro, SDXL — `$0.03`
- **Video generation** — MiniMax Video 01, Wan 2.1 (async) — `$0.50`
- **Text-to-speech** — `$0.03` · **Speech-to-text** — Whisper Large V3, 100+ languages — `$0.02`
- **Embeddings** — for RAG and semantic search — `$0.005`
- **Batch** — up to 50 mixed jobs in one payment, 10% discount — `$0.05`
- **Estimate / model list** — free

### Compute futures (prepay and draw down)
- **Deposit** USDC into a credit account — `$0.01`. Tier discounts: $10+ (5%), $50+ (10%), $200+ (15%)
- **Execute** jobs against the balance with no per-call x402 — only `$0.001` settlement, discount applied
- **Balance / history / pricing** — check what's left and what you've spent
- **Refund** unused balance back to the depositor anytime — `$0.01`

## Why an agent wants this

- **No accounts, no API keys** — a funded wallet is the only credential.
- **Pay only for what you use** — per-call micropayments, or prepay for a discount.
- **Predictable spend** — open a futures account, run a workload, refund the rest.
- **Discovery-native** — the gateway exposes a machine-readable catalog at `/.well-known/x402.json`.

## Endpoints

Base URL: `https://gateway.spraay.app`

Full request/response schemas and model lists are in [`references/endpoints.md`](references/endpoints.md). Runnable examples — per-call and the full futures lifecycle — are in [`examples/quickstart.md`](examples/quickstart.md).

## Payment

x402 V2. The gateway answers protected routes with `402 Payment Required`; your x402 client signs a USDC authorization (EIP-3009 on Base, SPL on Solana) and retries. Works with `@x402/fetch`, `x402-axios`, the Spraay MCP server, or any OpenClaw payment skill.

- USDC on Base mainnet: `0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913`
- USDC mint on Solana mainnet: `EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v`

## Links

- Gateway: https://gateway.spraay.app
- Discovery: https://gateway.spraay.app/.well-known/x402.json
- Spraay: https://spraay.app

## Tags

`compute` `gpu` `inference` `compute-futures` `escrow` `x402` `defi` `agent-skills` `openclaw` `claude-code` `codex-cli` `skill-md`

## License

MIT
