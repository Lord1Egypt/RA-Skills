---
name: x402-compute
version: 1.36.0
description: |
  This skill should be used when the user asks to "provision GPU instance",
  "integrate agent pods over an API", "create pods for my customers",
  "pod webhooks", "pod events",
  "spin up a cloud server", "list compute plans", "browse GPU pricing",
  "deploy AI machine", "one-click GPU running an LLM", "deploy a private LLM endpoint",
  "OpenRouter-ready endpoint", "agent deploy GPU", "spin up my own OpenAI-compatible endpoint",
  "extend compute instance", "resize compute instance", "destroy server instance", "check instance status",
  "list my instances", "top up compute credits", "check credit balance",
  "run inference on the grid", "decentralized inference", "OpenAI-compatible API",
  "Anthropic-compatible API", "use Claude Code with the grid", "ANTHROPIC_BASE_URL",
  "/v1/messages on open models",
  "multimodal embeddings", "EmbeddingGemma 2", "embed image", "embed audio",
  "embed video", "mixed media vectors", "local embeddings",
  "speech to text", "transcribe audio", "Grid transcription", "Whisper STT",
  "dictation", "local dictation", "voice engine",
  "text to speech", "TTS", "read aloud", "voiceover", "Grid speech", "audio tags",
  "Chatterbox", "Kokoro", "local speech API",
  "confidential / TEE inference", "list grid models", "check grid capacity",
  "Laya", "System One", "Jev-compatible decisions", "typed decision model",
  "private Laya", "serve Laya from the node app",
  "run a node", "provide compute", "become a grid node", "node operator", "join the grid",
  "stake to run a node", "serve a model on the grid", "earn from compute",
  "deploy an always-on AI agent", "deploy a hosted OpenClaw agent", "spin up a ClawPod",
  "agent pod", "hosted agent with its own wallet", "free agent trial",
  "Pi pod", "HermPod", "run a command in my pod", "pod sandbox", "read or write files in my pod",
  "expose a port from my pod", "clone my pod", "pod with my own AI key and fallbacks",
  "deploy a processor", "sell my code per call", "monetize an endpoint",
  "publish a paid API", "connect a processor as an MCP tool",
  "fine-tune a model", "train a model on my data", "Training Lab", "train a model over x402",
  "start a training run", "fine-tune with a wallet", "training API",
  "back up my agent", "agent backup", "restore my agent", "migrate my agent",
  "agent vault", "snapshot my agent's memory", "move my agent to a new machine",
  or manage Singularity Cloud Network compute. Seven jobs: SGL Machines
  (GPU/VPS provisioning), AI Machines (one-click GPU
  running an LLM — deploy a private OpenAI-compatible endpoint, or join the grid & earn),
  SGL Grid (decentralized confidential inference, multimodal embeddings, release-gated
  client-sealed speech-to-text and text-to-speech, plus Laya/System One typed decisions —
  consume it),
  Provide Compute (run a TEE node on the grid to serve inference and earn USDC + SGL), and
  Agent Pods (deploy an always-on hosted OpenClaw agent with its own crypto wallet, memory,
  preinstalled x402 skills, and owner/platform customization for identity, instructions,
  and self-check heartbeat prompts — managed or BYOK, tiers, free 24h trial), and
  Processors (publish your own code as a paid endpoint — buyers pay you directly in USDC via
  x402, you pay only for runtime; every processor is also a connectable MCP server, so agents,
  harnesses and LangGraph nodes can call it with just a URL), and Agent Vault
  (zero-knowledge encrypted backup, restore & migration for OpenClaw/Hermes agents —
  snapshot an agent's memory and soul, store it encrypted, restore or migrate it to any
  machine or pod). Pay with
  USDC on Base, Solana or Arc, USDm on MegaETH, USDG on Robinhood Chain via x402, optional MPP/Mppx, or
  pre-loaded USD credits. Arc: accepted for credit top-ups AND direct machine/AI-machine provision
  and extension payments (direct Arc payments floor at $5 — Arc gas is USDC; smaller prepayments go
  through Arc-funded credits). Includes optional OWS-backed auth and management flows.
homepage: https://docs.x402layer.cc/agentic-access/x402-compute
metadata:
  clawdbot:
    emoji: "🖥️"
    homepage: https://cloud.x402compute.cc
    os:
      - linux
      - darwin
    requires:
      bins:
        - python3
      env:
        - name: PRIVATE_KEY
          description: EVM private key for Base/MegaETH/Robinhood payment signing (use a dedicated low-balance wallet)
          sensitive: true
          optional: true
        - name: WALLET_ADDRESS
          description: EVM wallet address corresponding to PRIVATE_KEY
          optional: true
        - name: SOLANA_SECRET_KEY
          description: Solana signer key for Solana payment signing (use a dedicated low-balance wallet)
          sensitive: true
          optional: true
        - name: SOLANA_WALLET_ADDRESS
          description: Solana wallet address
          optional: true
        - name: COMPUTE_API_KEY
          description: Reusable API key for management endpoints (created via POST /compute/api-keys)
          sensitive: true
          optional: true
        - name: COMPUTE_AUTH_CHAIN
          description: Auth chain override — base, megaeth, robinhood, or solana
          optional: true
        - name: OWS_BIN
          description: Explicit path to a locally installed OWS binary (avoids runtime npx downloads)
          optional: true
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - WebFetch
---


# Singularity Cloud Network — Compute & Grid

Products share one credit balance and one set of wallet/API-key auth:

- **SGL Machines**: provision, manage, resize, and extend GPU/VPS instances on Singularity Cloud. **API base:** `https://compute.x402layer.cc`
- **AI Machines** — one-click deploy of a **GPU already running an LLM**, mode chosen at deploy: `private` (your own **OpenAI-compatible** endpoint — returns URL + API key) or `grid` (serve as a node & earn USDC + SGL, needs 50k SGL staked). Same x402 lifecycle as Machines; add `model_id` + `mode` to provision. **Standard tier (not confidential).** See [AI Machines](#ai-machines--one-click-llm-gpu) below and `references/ai-machines.md`.
- **SGL Grid** — decentralized confidential inference across capability-qualified nodes. Chat and embeddings use their documented OpenAI-compatible shapes; release-gated speech-to-text uses a two-step client-sealed JSON contract at `/v1/audio/transcriptions`, not multipart. It also serves **EmbeddingGemma 2 multimodal embeddings** and **Laya/System One** typed decisions. Always check the type-filtered model list before use. **API base:** `https://grid.x402compute.cc` (see [SGL Grid — Inference](#sgl-grid--inference), `references/transcription.md`, `references/multimodal-embeddings.md`, and `references/systemone-laya.md`)
- **Provide Compute (run a node)** — turn a capable machine into a grid node: stake $SGL, register, attest when supported, serve a model, earn USDC + SGL. Agentic via the `sgl` CLI. Operators can serve GGUF chat models, Laya/System One, or separately managed EmbeddingGemma 2 and release-gated Whisper transcription workers. Never reuse or modify one runtime for another workload. Operators can set a **custom per-token price** for supported token-billed models; transcription has its own per-audio-second price. See [Provide Compute](#provide-compute-run-a-node) below and `references/node-operator.md`.
- **Agent Pods**: deploy an **always-on hosted AI agent** on a dedicated CPU machine. Engines: ClawPod (OpenClaw, default), HermPod (Hermes) and Pi pod (a lightweight coding agent). Owners can also run commands, edit files, open ports and clone a pod through the Sandbox API (`references/agent-pods-api.md`). It chats on Telegram & Discord (more channels soon) + the dashboard, has its own crypto wallet + memory, and comes with the `x402-compute` + `x402-layer` skills preinstalled. Managed (we run the LLM, tiered) or BYOK; a **free 24h trial** is available. Platforms can customize the agent's layered identity/instructions and its quiet self-check heartbeat prompt without replacing the managed `AGENTS.md` safety base. **Curated templates** give a pod a job out of the box: `community-manager` (**TGPod**) runs a Telegram community; run `agent_pod.py templates` for the live list. Same x402 / API-key + credits lifecycle as Machines. **API base:** `https://compute.x402layer.cc` (see [Agent Pods](#agent-pods--always-on-hosted-agents) below).
- **SGL Processors** — deploy ONE function, get a paid HTTP endpoint **and a live MCP server**. Buyers pay the PUBLISHER directly via x402 (no platform cut); the publisher pays only for compute (~$0.0003/run, held then rebated to actual). Runs in isolated V8 sandboxes — **NOT a TEE**. Deny-by-default egress + server-side secret injection. **LIVE via the CLI** (`npm i -g @singularity-layer/cli`); the dashboard UI is still dark. Supports TypeScript + npm via local bundling, captured `console.log` per run, persistent `SGL.kv` / `SGL.files` state with signed download links, per-secret `mode: "env"`, publisher pause/resume, pricing computed from the buyer's input, **buyer payment on Solana, Base or Robinhood Chain** via a per-chain `payout` map, and **signed webhooks** (ping-to-activate, HMAC-signed `sale.completed`/`run.failed` deliveries with retries + auto-disable). See `references/processors.md`.
- **Datasets** — buy a validated **JSONL fine-tuning dataset** generated from one sentence plus 5-20 example conversations. Priced **per 100 examples** (fast $0.50 / balanced $0.75 / best $1.50 / decentralized grid $0.35), 50-2000 rows. Every row is **checked by a second model** against your house rules and rewritten if it breaks them (managed = frontier judge; **grid checks its own work on-network, so nothing leaves it even to be verified**). Fully agentic over x402: quote (402) → pay → **202 with a claim token in ~1s** → poll or signed webhook → presigned JSONL download. Generation takes minutes, so it NEVER blocks the request. Managed models or the confidential **encrypted grid**. Failed jobs refund. See `references/datasets.md`.
- **Training Lab** — fine-tune a small open model (Qwen 2.5 0.5B / 1.5B) on a dataset you own: pick a GPU block, pay once, get a LoRA adapter + score report back (plus a GGUF when `gguf_available`). **No account needed over x402**: quote (402, exact price) → pay from the wallet that owns the dataset → **202 with a claim token** → poll. Or use an API key with `training:write` and pay from credits. Runs that cannot start come back as credits. See `references/training.md` and `scripts/train_x402.py`.

Pay with x402, MPP, or pre-loaded credits — the same `x402c_…` API key and prepaid credit balance work across Machines and Grid.

**x402 Networks:** Base (EVM) • Solana • MegaETH • Robinhood Chain (EVM)
**PROCESSORS accept Solana, Base and Robinhood Chain — NOT MegaETH.** A publisher declares a `payout` address per chain (default: USDC on Solana at their deploying wallet), and the 402 carries ONE `accepts` ENTRY PER DECLARED CHAIN — read the array, do not assume one entry. `maxAmountRequired` is the same integer on every entry because all three assets are 6-decimal. **Robinhood is offered only on request** (`X-Accept-Networks: solana,base,robinhood`) because the reference x402 client rejects an entire `accepts` array containing a name it does not know. Owner/CLI auth is still a Solana signature. **A processor payment is FINAL — there are no refunds**; the recovery path for a failed paid run is re-sending the same `X-Payment` header, which returns the run already bought rather than charging again. See `references/processors.md`.
**x402 Currency:** USDC (Base/Solana) • USDm (MegaETH) • USDG (Robinhood Chain)
**MPP Methods:** Tempo • Stripe/card when enabled by the service
**Credits:** Pre-load USD via x402 topup, then provision/extend (`use_credits: true`) or call the Grid with `X-API-Key`
**Protocol:** HTTP 402 Payment Required (`X-Payment` for x402, `Authorization: Payment` for MPP)
**$SGL:** native token, live on Solana — mint `5c4HyD2rSShqnTsf5z3SaoD2H3GE452u2CUuYjviBAGS` (staking secures the grid; see [staking.x402layer.cc](https://staking.x402layer.cc))

This section below (Machines) covers provisioning. Jump to **[SGL Grid — Inference](#sgl-grid--inference)** for the OpenAI-compatible inference API.

**Access Note:** Preferred access is SSH public key. If no SSH key is provided, a one-time password fallback can be fetched once via API.
**`do:` plans:** plans whose id starts with `do:` require SSH key access (no one-time password fallback).

---

## Quick Start

### 1. Install Dependencies
```bash
pip install -r {baseDir}/requirements.txt
```

### 2. Choose Wallet Mode

#### Option A: Direct signing keys (Base, MegaETH, Robinhood, or Solana)

> **Use a dedicated low-balance wallet.** Never use your primary custody wallet.

> **Credentials must be exported.** These scripts read the process environment only — they do
> not load `.env` files. If your keys live in a `.env`, `source` it yourself first.

```bash
# Base (EVM) — same keys work for MegaETH and Robinhood Chain
export PRIVATE_KEY=<your-evm-private-key>
export WALLET_ADDRESS=<your-evm-wallet-address>

# MegaETH (uses same EVM keys as Base)
export PRIVATE_KEY=<your-evm-private-key>
export WALLET_ADDRESS=<your-evm-wallet-address>
export COMPUTE_AUTH_CHAIN="megaeth"

# Robinhood Chain (uses same EVM keys as Base; pays with USDG)
export PRIVATE_KEY=<your-evm-private-key>
export WALLET_ADDRESS=<your-evm-wallet-address>
export COMPUTE_AUTH_CHAIN="robinhood"

# Solana
export SOLANA_SECRET_KEY=<your-solana-secret-key>
export SOLANA_WALLET_ADDRESS=<your-solana-wallet-address>
export COMPUTE_AUTH_CHAIN="solana"
```

#### Option B: OpenWallet / OWS (optional-first)
```bash
npm install -g @open-wallet-standard/core@0.5.0
export OWS_WALLET="compute-wallet"
export COMPUTE_AUTH_MODE="ows"
```

Create `COMPUTE_API_KEY` (optional) for management endpoints:
```bash
python {baseDir}/scripts/create_api_key.py --label "my-agent"
```

OWS is best for compute auth and routine management flows. Direct x402 provision and extend still use local payment-signing paths. MPP provision/extend should use `mppx` or Tempo Wallet.

Resize is a management action, not a second payment flow. The API preserves remaining prepaid dollar credit by recalculating `expires_at` for the target hourly rate after the provider accepts the resize.

---

## ⚠️ Security Notice

> **IMPORTANT**: This skill handles private keys for signing blockchain transactions.
>
> - **Never use your primary custody wallet** - Create a dedicated wallet with limited funds
> - **Private keys are used locally only** - They sign transactions locally and are never transmitted
> - **For testing**: Use a throwaway wallet with minimal USDC/USDm

---

## Scripts Overview

| Script | Purpose |
|--------|---------|
| `browse_plans.py` | List available GPU/VPS plans with pricing |
| `browse_regions.py` | List deployment regions |
| `provision.py` | Provision a new instance (x402 payment, `--months` or `--days`). Add `--model-id` + `--mode private\|grid` to deploy an **AI Machine** (GPU running an LLM). |
| `create_api_key.py` | Create an API key for agent access (optional) |
| `list_instances.py` | List your active instances |
| `instance_details.py` | Get details for a specific instance |
| `get_one_time_password.py` | Retrieve one-time root password fallback |
| `extend_instance.py` | Extend instance lifetime (x402 payment) |
| `resize_instance.py` | Resize an instance in place (compute auth only) |
| `destroy_instance.py` | Destroy an instance |
| `ows_cli.py` | Run OpenWallet / OWS wallet, sign-message, and key commands |
| `pod_sandbox.py` | **Pod Sandbox** over `/pods/v1`: `exec` a command, `ls` / `cat` / `put` workspace files, `port-open` / `port-list` / `port-close`. Needs an API key with `pods:control:write` |
| `agent_pod.py` | Deploy an **Agent Pod** (`POST /pods`), create an `sk-sglpod-int-*` integration key, and call the pod's **OpenAI adapter** (`catalog`/`list`/`get`/`deploy`/`create-key`/`chat`) |
| `grid_embeddings.py` | Build and call text or ordered multimodal Grid embedding requests; hash/base64 media locally; supports `--dry-run` |
| `grid_transcription.py` | Validate bounded raw PCM locally, discover release-gated STT availability, or call the official SDK's client-sealed transcription helper |
| `train_x402.py` | **Training Lab over x402**: `catalog` / `run` (quote → pay the exact amount → 202 + claim token) / `status`. No account; the paying wallet must own an approved dataset |
| `solana_signing.py` | Internal helper for Solana x402 payment signing |

---

## Intent Router

Map the user's request to the script + reference to load (progressive disclosure — only open the
reference you need).

| User intent | Script | Reference |
|-------------|--------|-----------|
| "provision a GPU/VPS", "spin up a server", "extend/resize/destroy instance" | `provision.py` / `extend_instance.py` / `resize_instance.py` / `destroy_instance.py` | `references/api-reference.md` |
| "deploy a private LLM endpoint", "one-click GPU running an LLM", "OpenRouter-ready endpoint" | `provision.py --model-id … --mode private` | `references/ai-machines.md` |
| "join the grid & earn", "run a node", "provide compute" | `sgl` CLI or Singularity Node app (see below) | `references/node-operator.md` |
| **"use Claude Code with the grid"**, "Anthropic-compatible API", "Anthropic SDK on open models", "/v1/messages" | curl / Anthropic SDK / Claude Code → `grid.x402compute.cc` (`ANTHROPIC_BASE_URL`) | **`references/grid-anthropic-messages.md`** |
| "run inference on the grid", "confidential/TEE OpenAI-compatible inference" | curl / any OpenAI SDK → `grid.x402compute.cc` | `references/api-reference.md` |
| **"multimodal embeddings"**, "EmbeddingGemma 2", "embed image/audio/video", "mixed media vectors" | **`grid_embeddings.py`** → `POST /v1/embeddings` | **`references/multimodal-embeddings.md`** |
| **"local embeddings"**, "embed media on my Mac", "Node app embeddings" | Singularity Node app → Local → Embeddings | **`references/multimodal-embeddings.md`** |
| **"speech to text"**, "transcribe audio", "Whisper STT", "Grid transcription" | **`grid_transcription.py`** or official SDK → reserve + sealed `POST /v1/audio/transcriptions` | **`references/transcription.md`** |
| **"local dictation"**, "voice engine", "push to talk" | Singularity Node app → Dictation → Local | **`references/transcription.md`** |
| **"text to speech"**, "TTS", "voiceover", "Grid speech", "audio tags like [laugh]" | Official SDK `speak()` → reserve + sealed `POST /v1/audio/speech` | **`references/speech.md`** |
| **"read aloud on my Mac"**, "local TTS", "local speech API" | Singularity Node app → Voice Studio, or `http://127.0.0.1:8094/v1/audio/speech` | **`references/speech.md`** |
| "use Laya", "System One", "Jev-compatible typed decisions", "private Laya" | curl / private sealed System One → `grid.x402compute.cc` | `references/systemone-laya.md` |
| "serve Laya from my node", "node app Laya", "System One node operator" | Singularity Node app v1.7.4+ or `sgl` CLI with a local Laya sidecar | `references/systemone-laya.md` + `references/node-operator.md` |
| **"deploy an agent pod"**, "hosted OpenClaw/ClawPod", "always-on AI agent with its own wallet", "free 24h agent trial" | **`agent_pod.py deploy`** (or `catalog`/`list`/`get`) | **`references/agent-pods.md`** |
| **"call my pod via the OpenAI API"**, "give my pod an OpenAI-compatible endpoint", "get an API key for my agent pod" | **`agent_pod.py create-key` then `agent_pod.py chat`** | **`references/agent-pods.md`** |
| **"telegram community manager"**, "TGPod", "moderate my telegram group", "bot that answers members and removes scams", "discord community manager" (soon) | **`agent_pod.py templates`** then **`agent_pod.py deploy --template community-manager`** | **`references/agent-pods.md`** |
| **"run a command in my pod"**, "read/write files in my pod", "expose a port from my pod", "pod sandbox", "clone my pod" | **`pod_sandbox.py`** (exec/files/ports) or `POST /pods/v1/pods/{id}/clone` | **`references/agent-pods-api.md`** (Sandbox) |
| **"deploy a Pi pod"**, "HermPod", "pod with my own AI key and fallbacks", "Venice / 0G / OpenRouter key on a pod" | `agent_pod.py deploy` (`agent_id` `pi` / `hermes`) or `/pods/v1` (`engine` `pipod` / `hermpod`, `ai.fallbacks`) | **`references/agent-pods-api.md`** |
| **"integrate agent pods into my product"**, "pods over an API key", "create pods for my customers", "pod webhooks / events", "no wallet, just an API key" | `curl` / `PodsClient` (both SDKs) → `/pods/v1` | **`references/agent-pods-api.md`** |
| **"back up my agent"**, "restore/migrate my agent", "agent vault", "snapshot my agent's memory" | **`npx @singularity-layer/agentvault`** (`login`, `backup --all`, `restore`) | **`references/agent-vault.md`** |
| **"fine-tune a model"**, "train a model on my data", "Training Lab", "start a training run", "train over x402" | `scripts/train_x402.py run` (no account, x402) or `POST /training/runs` with an API key (`training:write`) | **`references/training.md`** |
| **"buy a training dataset"**, "generate fine-tuning data", "make me a JSONL dataset", "synthetic training data for my model" | `POST /datasets/x402/synth` (402 → pay → poll) or the MCP dataset tools | **`references/datasets.md`** |

Agent Pod quick path:
```bash
python {baseDir}/scripts/agent_pod.py catalog                              # pick tier/plan/model
python {baseDir}/scripts/agent_pod.py templates                            # curated pods with a job (TGPod …)
python {baseDir}/scripts/agent_pod.py deploy --ai-mode managed --tier pro \
    --plan <plan_id> --prepaid-hours 720 --telegram <bot_token> --use-credits
python {baseDir}/scripts/agent_pod.py create-key <pod_id> --name my-integration   # → sk-sglpod-int-…
python {baseDir}/scripts/agent_pod.py chat <pod_id> "What's on my calendar?" --key sk-sglpod-int-…
```

System One / Laya quick path:
```bash
curl "https://grid.x402compute.cc/v1/models?type=systemone" \
  -H "X-API-Key: $COMPUTE_API_KEY"

curl -X POST https://grid.x402compute.cc/v1/systemone \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $COMPUTE_API_KEY" \
  -d '{"model":"convaiinnovations/laya","state":{"text":"refund request from pro customer"},"questions":{"route":{"type":"choice","instructions":"Pick the best team.","criteria":{"billing":"Billing/refund issue","support":"Technical issue"}}}}'
```

Multimodal embeddings quick path:
```bash
python {baseDir}/scripts/grid_embeddings.py models
python {baseDir}/scripts/grid_embeddings.py embed --text "A searchable document" \
  --input-type document --dimensions 256
python {baseDir}/scripts/grid_embeddings.py embed --text "Product demo" \
  --image ./frame.png --audio ./narration.mp3 --audio-seconds 4.2 \
  --input-type document --dimensions 256
```

Speech-to-text candidate quick path (default off; availability check does not spend credits):
```bash
python {baseDir}/scripts/grid_transcription.py models
python {baseDir}/scripts/grid_transcription.py transcribe ./utterance.pcm --language auto --dry-run

# After the released Python SDK exposes the sealed helper and discovery lists whisper-1:
pip install singularity-grid
python {baseDir}/scripts/grid_transcription.py transcribe ./utterance.pcm
```

---

## Instance Lifecycle

```
Browse Plans → Choose Provider/Plan → Provision (x402/MPP/Credits) → Active → Extend / Destroy → Expired
```

Instances expire after their prepaid duration. Extend before expiry to keep them running.

---

## Workflows

### A. Browse and Provision

```bash
# List GPU plans
python {baseDir}/scripts/browse_plans.py

# Filter by type (gpu/vps/high-performance)
python {baseDir}/scripts/browse_plans.py --type vcg

# Check available regions
python {baseDir}/scripts/browse_regions.py

# Generate a dedicated SSH key once (recommended for agents)
ssh-keygen -t ed25519 -N "" -f ~/.ssh/x402_compute

# Provision an instance for 1 month (triggers x402 payment)
python {baseDir}/scripts/provision.py vcg-a100-1c-2g-6gb lax --months 1 --label "my-gpu" --ssh-key-file ~/.ssh/x402_compute.pub

# Plans whose id starts with do: require SSH key access.
python {baseDir}/scripts/provision.py do:s-1vcpu-1gb nyc3 --days 1 --label "ssh-only-test" --ssh-key-file ~/.ssh/x402_compute.pub

# Provision a daily instance (cheaper, use-and-throw)
python {baseDir}/scripts/provision.py vc2-1c-1gb ewr --days 1 --label "test-daily" --ssh-key-file ~/.ssh/x402_compute.pub

# Provision for 3 days
python {baseDir}/scripts/provision.py vc2-1c-1gb ewr --days 3 --label "short-task" --ssh-key-file ~/.ssh/x402_compute.pub

# Provision on Solana
python {baseDir}/scripts/provision.py vc2-1c-1gb ewr --months 1 --label "my-sol-vps" --network solana --ssh-key-file ~/.ssh/x402_compute.pub

# Provision on MegaETH (pays with USDm)
python {baseDir}/scripts/provision.py vc2-1c-1gb ewr --months 1 --label "my-mega-vps" --network megaeth --ssh-key-file ~/.ssh/x402_compute.pub

# Provision on Robinhood Chain (pays with USDG — same EVM keys as Base)
python {baseDir}/scripts/provision.py vc2-1c-1gb ewr --months 1 --label "my-usdg-vps" --network robinhood --ssh-key-file ~/.ssh/x402_compute.pub

# Provision via MPP / mppx (Tempo by default; Stripe/card if your mppx config supports it)
npx mppx https://compute.x402layer.cc/compute/provision \
  -X POST \
  -J '{"plan":"vc2-1c-1gb","region":"ewr","os_id":2284,"label":"mpp-vps","prepaid_hours":24,"ssh_public_key":"ssh-ed25519 AAAA... agent"}'

# If the response includes management_api_key, store it for later instance management:
export COMPUTE_API_KEY="x402c_..."

# ⚠️ After provisioning, wait 2-3 minutes for the machine to finish setup
# Then fetch your instance details (IP, status):
python {baseDir}/scripts/instance_details.py <instance_id>
```

### B. Manage Instances

```bash
# Optional: create a reusable API key (avoids message signing each request)
python {baseDir}/scripts/create_api_key.py --label "my-agent"

# List all your instances
python {baseDir}/scripts/list_instances.py

# Get details for one instance
python {baseDir}/scripts/instance_details.py <instance_id>

# Optional fallback if no SSH key was provided during provisioning
python {baseDir}/scripts/get_one_time_password.py <instance_id>

# Extend by 1 day
python {baseDir}/scripts/extend_instance.py <instance_id> --hours 24

# Extend by 1 month
python {baseDir}/scripts/extend_instance.py <instance_id> --hours 720

# Extend on Solana
python {baseDir}/scripts/extend_instance.py <instance_id> --hours 720 --network solana

# Extend on MegaETH (pays with USDm)
python {baseDir}/scripts/extend_instance.py <instance_id> --hours 720 --network megaeth

# Extend on Robinhood Chain (pays with USDG)
python {baseDir}/scripts/extend_instance.py <instance_id> --hours 720 --network robinhood

# Extend via MPP. MPP extension requires compute auth; use the management API key
# returned from MPP provisioning or normal wallet signature auth.
npx mppx https://compute.x402layer.cc/compute/instances/<instance_id>/extend \
  -X POST \
  -H "X-API-Key: $COMPUTE_API_KEY" \
  -J '{"extend_hours":720}'

# Resize via bundled helper script
python {baseDir}/scripts/resize_instance.py <instance_id> vc2-2c-4gb

# Resize in place with management auth only (no x402 or MPP payment)
curl -X POST https://compute.x402layer.cc/compute/instances/<instance_id>/resize \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $COMPUTE_API_KEY" \
  -d '{"plan":"vc2-2c-4gb"}'

# On do: plans, disk growth is irreversible and must be confirmed explicitly
curl -X POST https://compute.x402layer.cc/compute/instances/<instance_id>/resize \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $COMPUTE_API_KEY" \
  -d '{"plan":"do:s-2vcpu-4gb","confirm_disk_resize":true}'

# Destroy
python {baseDir}/scripts/destroy_instance.py <instance_id>
```

### C. OpenWallet / OWS

```bash
# List local OWS wallets
python {baseDir}/scripts/ows_cli.py wallet-list

# Sign a Base-compatible compute auth message
python {baseDir}/scripts/ows_cli.py sign-message --chain eip155:8453 --wallet compute-wallet --message "hello"

# Sign a MegaETH-compatible compute auth message
python {baseDir}/scripts/ows_cli.py sign-message --chain eip155:4326 --wallet compute-wallet --message "hello"

# Sign a Solana-compatible compute auth message
python {baseDir}/scripts/ows_cli.py sign-message --chain solana --wallet compute-wallet --message "hello"

# Create an OWS agent key
python {baseDir}/scripts/ows_cli.py key-create --name codex-compute --wallet compute-wallet
```

### D. Credits (payment-free provisioning)

```bash
# Top up credits via x402 payment (one-time)
# network: base | solana | megaeth | robinhood | arc  (Arc minimum $5 — gas is paid in USDC there)
curl -X POST https://compute.x402layer.cc/compute/credits/topup \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $COMPUTE_API_KEY" \
  -d '{"amount": 100, "network": "base"}'
# Returns 402 → pay → credits added to wallet balance

# Check credit balance
curl https://compute.x402layer.cc/compute/credits/balance \
  -H "X-API-Key: $COMPUTE_API_KEY"

# Provision using credits (no x402/MPP payment needed)
curl -X POST https://compute.x402layer.cc/compute/provision \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $COMPUTE_API_KEY" \
  -d '{
    "plan": "vc2-1c-1gb",
    "region": "ewr",
    "os_id": 2284,
    "label": "credit-vps",
    "prepaid_hours": 720,
    "ssh_public_key": "ssh-ed25519 AAAA... agent",
    "use_credits": true
  }'

# Extend using credits
curl -X POST https://compute.x402layer.cc/compute/instances/<instance_id>/extend \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $COMPUTE_API_KEY" \
  -d '{"extend_hours": 720, "use_credits": true}'
```

Credits are scoped per wallet. If the cloud provider rejects the instance after credits are deducted, the full amount is automatically refunded.

---

## x402 Payment Flow

1. Request provision/extend → server returns `HTTP 402` with payment requirements
2. Script signs payment locally:
   - Base: USDC `TransferWithAuthorization` (EIP-712)
   - MegaETH: USDm ERC-2612 `permit` (EIP-712) — gasless for the user, facilitator settles on-chain
   - Robinhood Chain: USDG `TransferWithAuthorization` (EIP-3009, EIP-712) — gasless for the user, facilitator settles on-chain in a single tx (domain `name="Global Dollar"`, `version="1"`, chainId `4663`)
   - Solana: signed SPL transfer transaction payload
3. Script resends request with `X-Payment` header containing signed payload
4. Server verifies payment, settles on-chain, provisions/extends instance

MegaETH uses an embedded facilitator (no external CDP dependency). The user signs an off-chain ERC-2612 permit, and the facilitator calls `permit()` + `transferFrom()` on MegaETH (~10ms blocks, near-zero gas).

Robinhood Chain also uses an embedded facilitator (no third party). The user signs an off-chain EIP-3009 `TransferWithAuthorization` for USDG (`0x5fc5360D0400a0Fd4f2af552ADD042D716F1d168`, 6 decimals), and the facilitator submits `transferWithAuthorization()` on Robinhood Chain (chainId 4663) in a single transaction — the contract self-verifies the signature, nonce, and balance on-chain.

For Solana, transient facilitator failures can happen. Retry once or twice if you get a temporary 5xx verify error.

**After you have paid, never pay again for the same request:**
- `HTTP 202` with `pending: true`: you paid and the machine exists, but its delivery is still being confirmed. The body is the full order (save any one-time keys in it). Poll `instance_details.py <order_id>` (or `agent_pod.py get <pod_id>`). Do not re-provision.
- `HTTP 409` with code `settlement_pending`: the payment outcome is not known yet and it may have moved. Do not pay again. The server checks the chain and either delivers or credits the amount to your balance automatically.

## MPP Payment Flow

MPP is available side-by-side with x402 on the same paid endpoints.

1. Request provision/extend -> server returns `HTTP 402` with `WWW-Authenticate: Payment`
2. `mppx` or Tempo Wallet creates an MPP credential
3. Client retries with `Authorization: Payment ...`
4. Server verifies the MPP payment, provisions/extends the instance, and returns `Payment-Receipt`

Notes:
- `POST /compute/provision` can be paid via MPP without wallet auth. In that case the response includes `management_api_key`; store it because it is shown once and is required for later management.
- `POST /compute/instances/:id/extend` via MPP requires compute auth, usually `X-API-Key: $COMPUTE_API_KEY`.
- `POST /compute/instances/:id/resize` uses compute auth only. It preserves remaining prepaid value by changing expiry instead of charging again.
- x402 remains fully supported through the Python scripts and `X-Payment` header flow.
- MPP methods are service-configured. Tempo is used by default by `mppx`; Stripe/card requires a Stripe-capable MPP client/config.

---

## AI Machines — One-Click LLM GPU

One-click deploy of a **GPU that comes up already running an LLM**. Same x402 lifecycle as any
Machine (provision / extend / resize / destroy) — you just add `model_id` + `mode` to provision.
Two modes, chosen at deploy:

- **`private`** — your own **OpenAI-compatible** endpoint. The box runs `llama-server` exposing
  `POST /v1/chat/completions` and `GET /v1/models`; the provision response returns the **endpoint URL
  + API key**. Works with any OpenAI-compatible client/agent/router → **OpenRouter-ready**. (Listing it
  *as an OpenRouter provider* is a separate OpenRouter approval — roadmap only.)
- **`grid`** — serve as a grid node and **earn USDC + SGL** (requires **≥ 50,000 $SGL staked**).

**Tier:** Standard (**not** confidential/TEE — for confidential inference use the Grid below or a TEE
node). **Managed:** kept alive, auto-updates (allowlist-gated), SSH available. An **agent with a
funded wallet can deploy + extend + destroy entirely via x402.**

```bash
# Deploy a PRIVATE OpenAI-compatible LLM endpoint (returns endpoint + API key)
python {baseDir}/scripts/provision.py vcg-a100-1c-2g-6gb lax --days 1 --label "my-llm" \
    --model-id llama-3.2-3b --mode private

# Deploy a GRID node (join the grid & earn; wallet needs 50k SGL staked)
python {baseDir}/scripts/provision.py vcg-a100-1c-2g-6gb lax --months 1 --label "grid-node" \
    --model-id llama-3.2-3b --mode grid

# Use a private endpoint (OpenAI-compatible). <ENDPOINT> = order.ai.endpoint: HTTPS, already ends in /v1
curl -X POST <ENDPOINT>/chat/completions \
  -H "Content-Type: application/json" -H "Authorization: Bearer <RETURNED_API_KEY>" \
  -d '{"model":"llama-3.2-3b","messages":[{"role":"user","content":"Hello"}]}'

# Extend runtime before it expires (most-used lifecycle action)
python {baseDir}/scripts/extend_instance.py <instance_id> --hours 720

# Destroy when done
python {baseDir}/scripts/destroy_instance.py <instance_id>
```

Control API: `POST /compute/provision` (add `model_id`+`mode`; base fields `plan`,`region`,`os_id`),
`GET /compute/instances`, `GET /compute/instances/:id`, `POST /compute/instances/:id/extend`,
`POST /compute/instances/:id/resize`, `POST /compute/instances/:id/password`,
`DELETE /compute/instances/:id`, `POST /compute/credits/topup`. Full detail + the end-to-end agent
deploy example → **`references/ai-machines.md`**.

---

## SGL Grid — Inference

Decentralized confidential inference across capability-qualified nodes. Chat and embeddings expose
their documented OpenAI-compatible shapes. Laya/System One and transcription use separate
contracts. Transcription is client-sealed JSON and non-streaming; do not send it through an OpenAI
multipart client.

**API base:** `https://grid.x402compute.cc`
**Auth:** `X-API-Key: x402c_…` (billed to your prepaid credits — same key/credits as Machines) **or** per-request x402 via `X-Payment`.
**Billing:** chat/embeddings use their documented token/input units; transcription uses exact sample-derived
audio duration, with the charge rounded up to micro-USDC. Pay in USDC through credits or x402. No subscription.

| Method | Path | Purpose |
|--------|------|---------|
| `GET`  | `/v1/models` | List models currently served by active attested nodes (Anthropic shape with an `anthropic-version` header) |
| `POST` | `/v1/chat/completions` | OpenAI-compatible chat (set `"stream": true` to stream) |
| `POST` | `/v1/messages` | Anthropic-compatible Messages API (streaming, tools, images on vision models) |
| `POST` | `/v1/messages/count_tokens` | Anthropic-compatible token count (estimate, free) |
| `POST` | `/v1/embeddings` | Text and release-gated EmbeddingGemma 2 text/image/audio/video/mixed vectors |
| `POST` | `/v1/audio/transcriptions/reserve` | Release-gated metadata-only STT reservation and quote |
| `POST` | `/v1/audio/transcriptions` | Release-gated client-sealed PCM transcription submit; JSON only |
| `POST` | `/v1/audio/speech/reserve` | Release-gated metadata-only TTS reservation and quote |
| `POST` | `/v1/audio/speech` | Release-gated client-sealed text-to-speech submit; JSON only, returns sealed m4a |
| `POST` | `/v1/systemone` | Laya/System One typed decisions (`convaiinnovations/laya`) |
| `GET`  | `/grid/capacity` | Live capacity: active nodes, TEE types, served models, `at_capacity` |

```bash
# 1) Reuse your compute API key (x402c_…) + prepaid credits, or create one:
python {baseDir}/scripts/create_api_key.py --label "my-agent"   # → x402c_...
# Top up credits in the dashboard: Settings → Credits (cloud.x402compute.cc).

# 2) Check what's being served + whether the grid has capacity
curl https://grid.x402compute.cc/v1/models -H "X-API-Key: $COMPUTE_API_KEY"
curl https://grid.x402compute.cc/grid/capacity            # active_nodes, models, at_capacity

# 3) OpenAI-compatible chat (billed to credits)
curl -X POST https://grid.x402compute.cc/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $COMPUTE_API_KEY" \
  -d '{"model":"llama-3.2-3b","messages":[{"role":"user","content":"Hello"}]}'

# Streaming: add "stream": true and read the SSE token chunks.
# Pay-per-request with x402 instead of credits: send the X-Payment header
# (same 402 → sign → resend flow as provision/extend) and omit X-API-Key.
```

Use any **OpenAI SDK** by setting `base_url=https://grid.x402compute.cc/v1` and `api_key=$COMPUTE_API_KEY`. Before a large batch, check `/grid/capacity` and back off / retry if `at_capacity` is true.

**Anthropic SDKs and Claude Code:** the Grid also speaks the Anthropic Messages API. Set the
base URL to `https://grid.x402compute.cc` (no `/v1`) and the API key to your compute key
(`x-api-key` or Bearer). Model ids are Grid ids. For Claude Code:

```bash
export ANTHROPIC_BASE_URL=https://grid.x402compute.cc
export ANTHROPIC_API_KEY=<YOUR_COMPUTE_API_KEY>
claude --model qwen-2.5-32b
```

Claude Code's own prompt is about 13k tokens, so pick a model whose `max_input_tokens` (from
`GET /v1/models` with an `anthropic-version` header) is well above that. Today `qwen-2.5-32b`
(32k) fits. Details, supported fields and refused features: `references/grid-anthropic-messages.md`.

**EmbeddingGemma 2:** call `POST /v1/embeddings`, not chat. It preserves string and string-array
input and adds ordered text/image/audio/video parts. Omitted `input_type` defaults to `query`;
`unspecified` is an explicit prefix opt-out. Only use it when
`GET /v1/models?type=embedding` lists `embeddinggemma-2`; absence means the default-off release
gate or exact node capability requirement is not satisfied. Build media requests with
`grid_embeddings.py` and read `references/multimodal-embeddings.md` for dimensions, limits,
stable errors, Local mode, sealed transport, and billing.

**Speech-to-text:** first call the metadata-only reserve endpoint, validate the returned node key
binding and quote, then seal raw mono 16 kHz signed 16-bit PCM locally and submit the reservation
token plus encrypted JSON envelope. Use `grid_transcription.py` with the released official SDK and
read `references/transcription.md`. v1 is one utterance, at most 60 seconds, and is not multipart or
streaming. It costs $0.0001 per exact audio second ($0.006/minute; $0.0001 minimum), rounded up to micro-USDC: 4.2 seconds costs $0.000420. Do not use
the route unless `GET /v1/models?type=transcription` lists `whisper-1`; all release gates default off.

**Text-to-speech:** same two-step sealed shape: reserve with metadata (model, voice, speed, exact
UTF-8 byte count), seal the text to that node, submit, verify the signed result, get m4a audio.
Models: `kokoro-82m` (10 voices, speed 0.5 to 2.0, $8 per 1M bytes) and `chatterbox-turbo`
(voice `aria`, performs `[laugh]`, `[chuckle]`, `[cough]` and more, $15 per 1M bytes). At most
1000 bytes per request. Use the official SDK `speak()` and read `references/speech.md`. Only use a
model that discovery lists; all release gates default off.

**Laya/System One:** call `POST /v1/systemone`, not `/v1/chat/completions`. Use
`GET /v1/models?type=systemone` to discover it. For end-to-end private Laya, use the reserve +
sealed-submit flow in `references/systemone-laya.md`.

---

## Provide Compute (run a node)

The other side of the grid: turn a **TEE-capable machine** into a node that serves confidential,
OpenAI-compatible inference and **earns USDC + SGL** per settled job. Fully agentic — the installer
and the `sgl` CLI are shell commands. Full runbook (requirements, flags, maintenance, slashing,
earnings) → **`references/node-operator.md`**.

**Prerequisites:** a supported TEE (e.g. Apple Secure Enclave `apple_se`, Intel TDX/SGX, AMD SEV-SNP,
AWS Nitro), `llama.cpp` + a GGUF model for chat or a local Laya sidecar for System One, and **≥ 50,000 $SGL staked** to your operator (Solana) wallet.

```bash
# 1. Stake ≥50,000 SGL to your operator wallet (agentic via the x402-layer skill / Staking Engine API,
#    or at https://staking.x402layer.cc). Non-custodial; slashable only for proven tampering.

# 2. Install the node CLI + runtime, get a model
curl -sSf https://grid.x402compute.cc/install.sh | sh     # installs `sgl` (Singularity-Layer/sgl-network-node)
brew install llama.cpp                                     # local inference runtime (macOS)
#   download a GGUF, e.g. ~/models/Llama-3.2-3B-Instruct-Q4_K_M.gguf

# 3. Register the node under the staked wallet (headless / agentic)
sgl init --wallet <STAKED_WALLET> --tee-type apple_se --models llama-3.2-3b
#   (interactive alternative: `sgl login`)

# 4. Attest the enclave (required before jobs; re-run after any binary update)
sgl attest

# 5. Serve as a background service (production)
sgl service install \
  --model-path ~/models/Llama-3.2-3B-Instruct-Q4_K_M.gguf \
  --model-name llama-3.2-3b \
  --resource-percent 50

# verify
sgl status
curl https://grid.x402compute.cc/grid/capacity            # your node raises active_nodes / models
```

For Laya, use the Singularity Node desktop app v1.7.4+ and select Models → System One → Laya. The app
starts the loopback sidecar and the normal node service. CLI fallback:
`sgl service install --model-name convaiinnovations/laya --systemone-sidecar-url http://127.0.0.1:8765 --max-jobs 1`.

**Maintenance:** `sgl off-grid` (stop new jobs cleanly for planned downtime — no penalty) / `sgl on-grid`
(resume). Honest downtime is never slashed; only proven tampering is. Re-run `sgl attest` after binary
updates. Docs: `https://docs.x402layer.cc/cloud/provide/node-setup`.

---

## Agent Pods — always-on hosted agents

Deploy a persistent AI agent ("ClawPod", built on OpenClaw) on a dedicated CPU machine. It stays online 24/7, chats on **Telegram & Discord** (Slack / WhatsApp / Signal are coming soon) **and** from the dashboard, has its own **crypto wallet** (Coinbase CDP — EVM + Solana, keys in a TEE) and **persistent memory**, and ships with the `x402-compute` + `x402-layer` skills preinstalled — wired to your account with capped, revocable credentials — so it can buy confidential compute and pay x402 endpoints itself. Platforms building on Agent Pods can layer owner identity, owner instructions, and a custom self-check heartbeat prompt over the managed base.

**API base:** `https://compute.x402layer.cc`
**Auth:** pod endpoints **always require compute auth** (`X-API-Key`, a signed compute session, or `X-Auth-*` wallet signature) — even when paying with x402, because a pod is owned by your wallet. (This differs from `POST /compute/provision`, which accepts anonymous x402.)
**Pay:** platform **credits** (`use_credits: true`) or **x402** (omit `use_credits` → the deploy answers `402 Payment Required`; settle with the `X-Payment` header like any provision, and add `"network"` for a non-Base chain).
**Engines:** `agent_id: "openclaw"` (ClawPod, default), `"hermes"` (HermPod) and `"pi"` (Pi pod, a lightweight coding agent). On `/pods/v1` they are `clawpod`, `hermpod` and `pipod`. Check `available` in `GET /pods/catalog` before deploying.

### Catalog (public, no auth)
```bash
# Agents, managed tiers (models per tier), channels, memory backends, pricing
curl -s https://compute.x402layer.cc/pods/catalog
```

### Deploy a pod — `POST /pods`
Two AI modes:
- **`managed`** — we run the LLM and meter it from your credits. Pick a `tier`: `starter` (text chat), `pro` (adds vision + computer-use), `max` (top reasoning + vision). Each tier bundles a machine RAM floor + a curated model menu the agent can switch among at runtime (`/model`). Managed pods include a small prepaid inference allowance.
- **`byok`** — bring your own OpenAI-compatible key + any machine `plan`. You pay CPU + a small service % only; your AI runs on your key.

```bash
# Managed Pro pod, paid from credits, with a Telegram bot
curl -s -X POST https://compute.x402layer.cc/pods \
  -H "X-API-Key: $COMPUTE_API_KEY" -H "Content-Type: application/json" \
  -d '{
    "agent_id": "openclaw",
    "ai_mode": "managed",
    "tier": "pro",
    "plan": "<plan_id from /compute/plans>",
    "prepaid_hours": 720,
    "channels": { "telegram": "<bot_token>" },
    "agent_identity": "You are Atlas, Acme Cloud's support agent.",
    "agent_instructions": "Answer as Acme support. Be concise and cite the current integration step.",
    "heartbeat_prompt": "Check open support escalations and renew yourself if runway is low. Stay silent if clear.",
    "agent_heartbeat_minutes": 30,
    "use_credits": true
  }'

# BYOK pod (your own model + key), paid from credits
curl -s -X POST https://compute.x402layer.cc/pods \
  -H "X-API-Key: $COMPUTE_API_KEY" -H "Content-Type: application/json" \
  -d '{
    "agent_id": "openclaw", "ai_mode": "byok",
    "plan": "<plan_id>", "prepaid_hours": 720,
    "llm_base_url": "https://openrouter.ai/api/v1",
    "llm_api_key": "<your_llm_key>", "llm_api": "openai-completions",
    "model": "openai/gpt-4o-mini",
    "use_credits": true
  }'
```
The response includes the new `pod.id` (this **is** the compute order id — use it for all pod + lifecycle calls) and, for managed pods, a one-time `managed_ai_key` (the pod's key to our managed LLM proxy — shown once).

**Deploy body fields:**
- `agent_id`: `"openclaw"` (default), `"hermes"` or `"pi"`.
- `ai_mode` — `"managed"` | `"byok"`.
- `tier` — managed only: `"starter"` | `"pro"` | `"max"`.
- `plan` (+ optional `plan_ram_mb` for a pre-flight RAM check) — the machine; managed tiers enforce a RAM floor (pro/max run a browser on the box).
- `prepaid_hours` — e.g. `720` = 1 month (min 24).
- `model` — managed: an override that must be in the chosen tier's model list (else it falls back to the tier default); byok: your model id.
- `llm_base_url`, `llm_api_key`, `llm_api` — byok only. `llm_api` ∈ `openai-completions` (default) | `openai-responses` | `anthropic-messages` | `google-generative`.
- `llm_preset` (`openrouter`, `openai`, `venice`, `0g`, `custom`), `llm_fallbacks` (up to 3 ordered backup providers, plus one optional `{preset: "singularity", model}`) and `managed_models` (default on for BYOK ClawPod: also use Singularity Layer models, billed per call from credits). BYOK only. See `references/agent-pods.md`.
- `channels` — `{ telegram?: token, discord?: token }` (validated against the agent's supported channels; unsupported channels are rejected).
- `memory` — byok only: `{ backend: "raw"|"mem0", api_key?, lcm? }` (managed memory is tier-driven). Applies only when the memory feature is enabled.
- `agent_identity` — optional owner/platform identity text (max 8000 chars), rendered into the managed `AGENTS.md` customization section and `/opt/pod/workspace/IDENTITY.md`.
- `agent_instructions` — optional owner/platform instructions (max 8000 chars), rendered into the managed `AGENTS.md` customization section.
- `heartbeat_prompt` — optional quiet self-check prompt (max 4000 chars), used by the agent heartbeat. It replaces the default survival/check-work prompt only for this pod.
- `agent_heartbeat_minutes` — optional self-check cadence (`0` disables; otherwise 15-1440 minutes).
- `use_credits`, `network`, `ssh_public_key`, `region`, `os_id` — passed straight through to the audited provision path.

`AGENTS.md` is not raw-editable over the API. Singularity Layer keeps the platform-managed base so wallet survival, spend caps, x402 safety, and tool boundaries remain intact; your text is appended in a bounded owner/platform section. Use `PATCH /pods/<id>/settings` with empty string or `null` to clear a custom field.

### Free 24-hour trial — `POST /pods/trial`
A free Starter/Pro pod with **no upfront payment** (funded by a one-time credit grant; gated behind a live campaign, so it can answer `503` when off or fully claimed). One per wallet + device. The pod is **auto-destroyed at 24h** (never renews) and its managed-AI allowance is capped.
```bash
curl -s -X POST https://compute.x402layer.cc/pods/trial \
  -H "X-API-Key: $COMPUTE_API_KEY" -H "Content-Type: application/json" \
  -d '{
    "agent_id": "openclaw",
    "tier": "starter",
    "plan": "<plan_id>",
    "device_hash": "<sha256 hex device fingerprint>",
    "channels": { "telegram": "<bot_token>" }
  }'
```
`tier` must be `starter` or `pro`; `device_hash` is a 64-char sha256 hex. `ai_mode` (managed), `prepaid_hours` (24) and `use_credits` are forced server-side — you supply the tier, plan, device_hash, and any channels.

### Manage a pod
```bash
curl -s https://compute.x402layer.cc/pods       -H "X-API-Key: $COMPUTE_API_KEY"   # list yours
curl -s https://compute.x402layer.cc/pods/<id>  -H "X-API-Key: $COMPUTE_API_KEY"   # details + live heartbeat + masked credential state

# Lifecycle action: restart | redeploy | stop | update | diagnose | logs | pair-approve | cron
curl -s -X POST https://compute.x402layer.cc/pods/<id>/actions \
  -H "X-API-Key: $COMPUTE_API_KEY" -H "Content-Type: application/json" -d '{"action":"restart"}'

# Link a chat: the bot shows a pairing code in Telegram/Discord; approve it
curl -s -X POST https://compute.x402layer.cc/pods/<id>/actions \
  -H "X-API-Key: $COMPUTE_API_KEY" -H "Content-Type: application/json" \
  -d '{"action":"pair-approve","channel":"telegram","code":"T64WUC8Q"}'

# Add/replace channels later (queues a redeploy)
curl -s -X PATCH https://compute.x402layer.cc/pods/<id>/channels \
  -H "X-API-Key: $COMPUTE_API_KEY" -H "Content-Type: application/json" \
  -d '{"channels":{"discord":"<bot_token>"}}'

# Tune the agent self-check heartbeat, identity, and instructions
curl -s -X PATCH https://compute.x402layer.cc/pods/<id>/settings \
  -H "X-API-Key: $COMPUTE_API_KEY" -H "Content-Type: application/json" \
  -d '{"agent_heartbeat_minutes":30,
       "agent_identity":"You are Atlas, Acme Cloud support.",
       "agent_instructions":"Use Acme terminology and escalate billing questions.",
       "heartbeat_prompt":"Review open escalations and renew yourself if needed. Stay silent if clear."}'
```
Actions apply on the pod worker's next poll (≤ 60s). The `cron` action drives the agent's scheduler: `{"action":"cron","verb":"add|enable|disable|remove|run", ...}` (add takes `kind`/`schedule`/`name`/`message`).

### Agent wallet & delegated skill access
```bash
# The pod's own wallet — addresses + balances (fund it so the agent can pay for things)
curl -s https://compute.x402layer.cc/pods/<id>/wallet -H "X-API-Key: $COMPUTE_API_KEY"

# Owner controls: per-tx spend cap + arm sending (default OFF; clamped to a platform ceiling)
curl -s -X PATCH https://compute.x402layer.cc/pods/<id>/wallet/settings \
  -H "X-API-Key: $COMPUTE_API_KEY" -H "Content-Type: application/json" \
  -d '{"send_enabled":true,"spend_cap_usd":10}'

# Send from / pay an x402 endpoint with the pod wallet (gated; owner is uncapped, the agent is cap-bound):
#   POST /pods/<id>/wallet/send      {chain, to, token, amount, idempotency_key}
#   POST /pods/<id>/wallet/x402/pay  {url, method?, headers?, body?, max_amount_usd?}
```
`GET /pods/<id>` returns a masked `credentials` block — the preinstalled skills' pod-scoped Compute key + Studio PAT (for the marketplace / MCP) and its daily cap. Manage it with `POST /pods/<id>/credentials` (`{"action":"enable"|"regenerate"|"set-cap"|"byok", ...}`) or `DELETE /pods/<id>/credentials` to revoke. Delegated creds, native Singularity MCP, wallet sending, and memory are **feature-gated** and may be dark until launch.

### Extend / destroy
A pod is a compute order, so use the **Machines endpoints with the pod id as the instance id**:
```bash
# Extend early (credits or x402, same as any Machine)
curl -s -X POST https://compute.x402layer.cc/compute/instances/<pod.id>/extend \
  -H "X-API-Key: $COMPUTE_API_KEY" -H "Content-Type: application/json" -d '{"extend_hours":720,"use_credits":true}'
# Destroy (revokes the pod's delegated creds, refunds remaining prepaid time)
curl -s -X DELETE https://compute.x402layer.cc/compute/instances/<pod.id> -H "X-API-Key: $COMPUTE_API_KEY"
```
Managed pods can also **auto-renew** from your credits at expiry (with a grace window) when that feature is enabled; trials never renew. The agent wallet's funds survive destruction (withdraw from the Wallet tab).

### OpenAI-compatible adapter (talk to your pod like any OpenAI endpoint)
Point any OpenAI SDK at a pod. **v1 is Chat Completions only, non-streaming, `usage:null`**; the model
is always `agent-pod` (the pod uses its own configured LLM). The adapter surface is **feature-flagged**
(dark by default) — it answers `404` until enabled.
```bash
# 1) Mint a pod-scoped integration key (owner / compute auth). Raw key shown ONCE.
curl -s -X POST https://compute.x402layer.cc/pods/<id>/api-keys \
  -H "X-API-Key: $COMPUTE_API_KEY" -H "Content-Type: application/json" -d '{"name":"my-integration"}'
# → { "key": "sk-sglpod-int-…", "base_url": "https://compute.x402layer.cc/pods/<id>/v1" }

# 2) Call it with Authorization: Bearer <key> (NOT compute auth)
curl -s -X POST https://compute.x402layer.cc/pods/<id>/v1/chat/completions \
  -H "Authorization: Bearer sk-sglpod-int-…" -H "Content-Type: application/json" \
  -d '{"model":"agent-pod","stream":false,"messages":[{"role":"user","content":"Hello"}]}'
```
Keys are bound to the pod, carry a daily request cap (default 1000/day → `429` over-cap), and are
revocable (`DELETE /pods/<id>/api-keys/<keyId>`). Full body fields, response shapes, and error codes
→ **`references/agent-pods.md`**. Scripted end-to-end: `scripts/agent_pod.py` (`deploy` → `create-key`
→ `chat`).

---

## Agent Vault — encrypted agent backup & migration

Zero-knowledge encrypted snapshots of an agent's entire state (memory, soul,
config, skills) for OpenClaw and Hermes — restorable on any machine or pod.
Encryption happens on the agent's own machine; the platform stores ciphertext
it cannot read, so **a lost passphrase is unrecoverable**. Plans: FREE = one
rolling snapshot (new replaces old), 1 GB. VAULT PRO = $3/month or $30/year —
10 GB, the last 10 snapshots of each agent. VAULT MAX = $5/month or $50/year —
50 GB, unlimited snapshots. Paid from credits — or directly with x402 (USDC on Base/Solana, USDG on
Robinhood, USDm on MegaETH) — via
`POST /backups/subscribe {"plan":"pro|max","interval":"month|year"}`, adding
`"pay":"x402","network":"base"` for the x402 rail, or dashboard → Upgrade.
The FREE tier needs no call at all.

```bash
npm i -g @singularity-layer/agentvault
agentvault login          # browser wallet approval (or --api-key)
agentvault backup --all   # encrypt + upload every detected agent
agentvault backup --path ~/my-agent --name "My Agent"   # ANY directory (universal)
agentvault restore        # bring an agent back, anywhere
```

Vault works for any login (wallet or account login). Pods back up one-click from their dashboard **Backups** tab, no install.
Cross-restoring a snapshot onto a different pod or machine IS migration.
Full flows, HTTP API, and agent safety rules: `references/agent-vault.md`.

## Plan Types

| Type | Plan Prefix | Description |
|------|-------------|-------------|
| GPU | `vcg-*` | GPU-accelerated (A100, H100, etc.) |
| VPS | `vc2-*` | Standard cloud compute |
| High-Perf | `vhp-*` | High-performance dedicated |
| Dedicated | `vdc-*` | Dedicated bare-metal |
| Standard (SSH key only) | `do:*` | Standard cloud compute; SSH key required, disk resize irreversible |

---

## Environment Reference

| Variable | Required For | Description |
|----------|--------------|-------------|
| `PRIVATE_KEY` | Base/MegaETH/Robinhood payment signing | EVM private key (0x...) |
| `WALLET_ADDRESS` | Base/MegaETH/Robinhood direct-signing mode | EVM wallet address (0x...) |
| `SOLANA_SECRET_KEY` | Solana direct-signing mode | Solana signer key (base58 or JSON byte array) |
| `SOLANA_WALLET_ADDRESS` | Solana direct-signing mode | Solana wallet address (optional if derivable from secret) |
| `COMPUTE_AUTH_CHAIN` | Chain auth override | `base`, `megaeth`, `robinhood`, or `solana` |
| `COMPUTE_API_KEY` | Optional | Reusable API key for compute management endpoints |
| `COMPUTE_AUTH_MODE` | Optional | `auto`, `private-key`, or `ows` |
| `OWS_WALLET` | OWS auth mode | OWS wallet name or ID |
| `OWS_BIN` | OWS auth mode | Optional explicit path to the `ows` executable |
| `COMPUTE_API_KEY` | MPP/no-wallet management | API key returned once after an MPP provision without wallet auth |

---

## API Reference

For full endpoint details, see:
- [references/api-reference.md](references/api-reference.md)
- [references/multimodal-embeddings.md](references/multimodal-embeddings.md) — EmbeddingGemma 2 ordered media contract, Local/Grid usage, limits, dimensions, billing, and exact public errors
- [references/transcription.md](references/transcription.md) — Local versus Grid STT, client-sealed JSON flow, PCM limits, privacy, pricing, release gates, and helper usage
- [references/speech.md](references/speech.md) — Local Voice Studio and Speech API versus Grid TTS, models, voices, audio tags, sealed flow, pricing, and serving a speech node
- [references/systemone-laya.md](references/systemone-laya.md) — Laya/System One typed decisions, private sealed flow, and node-app serving path
- [references/ai-machines.md](references/ai-machines.md) — AI Machines (one-click LLM GPU: modes, endpoint+key, control API, agent x402 deploy)
- [references/agent-pods.md](references/agent-pods.md) — Agent Pods (deploy `POST /pods`, manage, wallet, and the OpenAI-compatible adapter: `sk-sglpod-int-*` keys + `/v1/chat/completions`)
- [references/agent-pods-api.md](references/agent-pods-api.md): the **`/pods/v1` API-key surface** for building ON pods rather than clicking them: idempotent create, lifecycle actions, tasks, connectors, wallet, backups, an account **event log** and **signed webhooks**, plus engines (`clawpod`, `hermpod`, `pipod`), BYOK with fallbacks, and the **Sandbox** (exec, files, ports, clone). Use it when the caller holds an `x402c_…` key and no wallet; `agent-pods.md` remains the signature/OWS path.
- [references/grid-anthropic-messages.md](references/grid-anthropic-messages.md): Anthropic-compatible `/v1/messages`, `count_tokens`, Anthropic-shaped `/v1/models`, Claude Code setup
- [references/node-operator.md](references/node-operator.md) — run a grid node (provide compute, earn)
- [references/openwallet-ows.md](references/openwallet-ows.md)

---

## Resources

- 📖 **Documentation:** [docs.x402layer.cc/agentic-access/x402-compute](https://docs.x402layer.cc/agentic-access/x402-compute)
- 🖥️ **Cloud Network app:** [cloud.x402compute.cc](https://cloud.x402compute.cc) (Machines, Grid, API keys, credits)
- 🌐 **Singularity Compute:** [x402compute.cc](https://x402compute.cc)
- 🔑 **Staking:** [staking.x402layer.cc](https://staking.x402layer.cc) — stake $SGL (min 50,000) to run a node / validate; rewards in USDC + SGL
- **API bases:** Machines `https://compute.x402layer.cc` · Grid `https://grid.x402compute.cc`

---

## OWS scope note

OWS support is optional-first in this release:
- use it for compute auth and management/API-key flows
- keep direct Base, MegaETH, Robinhood, or Solana signing keys for the paid provision and extend flows
- resize, list, details, password fallback, and destroy work with normal compute auth / API keys
