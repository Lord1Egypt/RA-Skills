# SGL Grid — Provide Compute (Run a Node)

Become a **grid node operator**: serve confidential, OpenAI-compatible inference from your own
TEE-capable machine and earn **USDC + SGL** on every settled job. This is the *provider* side of
the grid (the consumer side — calling inference — is in the main SKILL under "SGL Grid — Inference").

Everything here is agent-runnable: the installer and the `sgl` CLI are plain shell commands. The
only step that needs an on-chain wallet transaction is **staking** (see Step 1), which is itself
agentic via the staking API / the `x402-layer` skill.

Node software (open source): `https://github.com/Singularity-Layer/sgl-network-node`

---

## Requirements (check before starting)

- **A TEE-capable machine.** A supported Trusted Execution Environment is mandatory — it's what lets
  the node serve prompts it cannot read. Examples: Apple Secure Enclave (`apple_se`), Intel TDX/SGX,
  AMD SEV-SNP, AWS Nitro.
- **Compute for the model** you'll serve — CPU/RAM (+ GPU/Metal where available). 3B-class models run
  on modest hardware; larger models need more.
- **≥ 50,000 $SGL staked** to your operator wallet (the minimum to register a compute node; the live
  figure is shown in the staking app). Non-custodial, withdrawable after a cooldown.
- **A Solana wallet** holding the stake — the node is bound to it.
- **Local inference runtime** `llama.cpp` (`brew install llama.cpp`) and a **GGUF model file** for
  chat models, or the Singularity Node app v1.7.4+ for Laya/System One. The release-gated
  transcription candidate uses its own pinned whisper.cpp worker and model; it is not a llama.cpp
  or Laya mode.
- Reliable power + network (uptime = job matching; honest downtime is never penalized).

---

## Step 1 — Stake $SGL (bond the operator wallet)

Stake at least the minimum (**50,000 SGL**) to the wallet you'll run the node under. Staking is
non-custodial and **only slashable for proven tampering — never for honest downtime**.

Agentic options:
- Use the **`x402-layer` skill** (staking module) or the **Staking Engine API**
  (`docs.x402layer.cc/staking` · API reference under "Staking Engine") to stake programmatically.
- Or stake in the app: `https://staking.x402layer.cc`.

Token: `$SGL` mint `5c4HyD2rSShqnTsf5z3SaoD2H3GE452u2CUuYjviBAGS` (Solana). Full model (tiers,
cooldowns, rewards, slashing) → `https://docs.x402layer.cc/staking/introduction`.

---

## Step 2 — Install the node CLI + runtime

```bash
# 1. Install the sgl node CLI (Singularity-Layer/sgl-network-node release)
curl -sSf https://grid.x402compute.cc/install.sh | sh

# 2. Local inference runtime
brew install llama.cpp            # macOS; see repo README for Linux

# 3. A GGUF model to serve, e.g.
#    ~/models/Llama-3.2-3B-Instruct-Q4_K_M.gguf

sgl --help                        # verify install
```

---

## Step 3 — Register the node (bind to the staked wallet)

Agentic / headless (no browser) — recommended for agents:

```bash
sgl init --wallet <STAKED_WALLET> --tee-type apple_se --models llama-3.2-3b
```

Interactive (browser approval) alternative:

```bash
sgl login --tee-type apple_se --models llama-3.2-3b
```

- `--wallet` — the Solana wallet holding your stake (required for `init`).
- `--tee-type` — TEE on this machine (default `apple_se`).
- `--models` — comma-separated model names you'll advertise.

---

## Step 4 — Attest the enclave

Only **attestation-verified** nodes receive jobs. Re-run after any binary update.

```bash
sgl attest
```

---

## Step 5 — Serve

Production (background service — survives reboots, logout, crashes, idle sleep):

```bash
sgl service install \
  --model-path ~/models/Llama-3.2-3B-Instruct-Q4_K_M.gguf \
  --model-name llama-3.2-3b \
  --resource-percent 50
```

Foreground test first (optional):

```bash
sgl start --model-path ~/models/Llama-3.2-3B-Instruct-Q4_K_M.gguf --model-name llama-3.2-3b
```

Verify it's live:

```bash
sgl status            # node + hardware + orchestrator connection
sgl service status    # background-service state
curl https://grid.x402compute.cc/grid/capacity   # your node should raise active_nodes / models
```

The node now registers, advertises its model(s), heartbeats, and starts receiving jobs.

### Serve Laya / System One

For node operators, the preferred path is the desktop app:

1. Install or update to Singularity Node app v1.7.4 or newer.
2. Open Models → System One → Laya.
3. Connect. The app starts the local Laya sidecar on `127.0.0.1:8765`, then starts the normal SGL
   node service with `--systemone-sidecar-url`.

CLI fallback:

```bash
python3 -m venv ~/.sgl-laya
~/.sgl-laya/bin/pip install "laya[serve]"
LAYA_DEVICE=cpu LAYA_PRELOAD=1 ~/.sgl-laya/bin/laya-serve --host 127.0.0.1 --port 8765

sgl login --models convaiinnovations/laya
sgl attest
sgl service install \
  --model-name convaiinnovations/laya \
  --systemone-sidecar-url http://127.0.0.1:8765 \
  --max-jobs 1
```

Keep the sidecar bound to loopback. The grid node service remains the only public serving lane.

### Speech-to-text candidate

Grid transcription is default off and is not an operator setup option until a released node package,
private canary, and public discovery gates pass. Do not adapt the chat or Laya commands above.

The pinned candidate is `whisper-1` using a dedicated pinned whisper.cpp v1.9.5 runtime and
Whisper Small model. A provider advertises transcription capacity only after exact model/runtime
verification and a real known-audio startup smoke. A crash, stale heartbeat, failed smoke, revision
mismatch, or changed encryption-key binding removes eligibility immediately.

Read [transcription.md](transcription.md) for the immutable candidate pins and release gates. Wait
for the published node artifact and official operator command; do not download a mutable model URL,
modify another managed service, or install the staged fixed-label service beside Laya or
EmbeddingGemma.

---

## Maintenance & lifecycle

```bash
sgl off-grid          # planned downtime: stop NEW jobs cleanly (in-flight finish, no penalty)
sgl on-grid           # resume receiving jobs
```

- After updating the binary, re-run `sgl attest`.
- **Slashing is narrow:** only proven tampering with confidential-compute results is slashable.
  Honest downtime/maintenance is never slashed — it just means no new jobs while offline.

---

## CLI quick reference

| Command | Purpose |
|---|---|
| `sgl init --wallet <W>` | Register headless under a staked wallet (agentic) |
| `sgl login` | Register via browser approval |
| `sgl attest` | Submit hardware attestation (required before jobs; re-run after updates) |
| `sgl start` | Run in foreground (test) |
| `sgl service install` | Run as managed OS service (production) |
| `sgl service stop` / `service status` | Manage the background service |
| `sgl status` | Node + hardware + orchestrator status |
| `sgl off-grid` / `on-grid` | Maintenance mode toggle |
| `sgl price show` | Show your per-model price, the suggested rate, and the allowed band |
| `sgl price set --model <M> --input <USD/1M> --output <USD/1M>` | Set a custom per-token price (within the band) |
| `sgl price reset --model <M>` | Revert a model to the platform suggested price |

`sgl start` / `sgl service install` flags: `--model-path`, `--model-name`, `--resource-percent`
(1–100 preset), `--threads`, `--gpu-layers`, `--context-size`, `--max-jobs`, `--inference-port`
(default 8081), `--heartbeat-interval` (default 5s). `sgl service install --sandbox` (macOS)
runs the node under a Seatbelt sandbox that walls off SSH keys / wallets / keychains / browser
data from the inference process; on Linux equivalent systemd hardening is always applied.

---

## Pricing (set your own per-token price)

By default your node bills the platform **suggested rate** (~OpenRouter ÷ 10) and you keep 80%.
You may optionally set your **own** per-token price within an allowed band around that suggested
rate: **floor = suggested × 0.5**, **ceiling = suggested × 5**. Prices are USD per 1M tokens,
split into input (prompt) and output (completion). You always earn 80% of whatever you charge.

```bash
sgl price show
# llama-3.2-3b   in $0.005000 / out $0.005000  [suggested]   (band: in $0.0025–$0.025 ...)

sgl price set --model llama-3.2-3b --input 0.004 --output 0.004   # undercut to win more jobs
sgl price reset --model llama-3.2-3b                              # back to suggested
```

Notes:
- The server enforces the band and that the model is one you actually advertise; out-of-band
  prices are rejected. There's a short anti-flap cooldown between changes to the same model.
- A model with no custom price simply bills at the suggested rate — nothing changes for you.
- You can also set prices from the operator dashboard (`cloud.x402compute.cc` → Provide → your node)
  or via the API (`POST /grid/nodes/:id/prices`); callers can compare providers at
  `GET /v1/providers?model=<M>`.

## Earnings

Operators earn a share of every settled job in **USDC + SGL**. Payout/claim details:
`https://docs.x402layer.cc/cloud/provide/earnings`. Reward split is 80/5/10/5 (node/stakers/team/burn);
see the staking rewards docs.

## Docs

- Setup: `https://docs.x402layer.cc/cloud/provide/node-setup`
- Requirements: `https://docs.x402layer.cc/cloud/provide/requirements`
- CLI reference: `https://docs.x402layer.cc/cloud/provide/cli`
- Staking to operate: `https://docs.x402layer.cc/cloud/provide/staking`
- Node repo: `https://github.com/Singularity-Layer/sgl-network-node`
