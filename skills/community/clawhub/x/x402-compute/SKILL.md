---
name: x402-compute
version: 1.8.1
description: |
  This skill should be used when the user asks to "provision GPU instance",
  "spin up a cloud server", "list compute plans", "browse GPU pricing",
  "extend compute instance", "resize compute instance", "destroy server instance", "check instance status",
  "list my instances", "top up compute credits", "check credit balance",
  "run inference on the grid", "decentralized inference", "OpenAI-compatible API",
  "confidential / TEE inference", "list grid models", "check grid capacity",
  "run a node", "provide compute", "become a grid node", "node operator", "join the grid",
  "stake to run a node", "serve a model on the grid", "earn from compute",
  or manage Singularity Cloud Network compute. Three jobs: SGL Machines
  (GPU/VPS provisioning across Vultr & DigitalOcean), SGL Grid (decentralized,
  confidential, OpenAI-compatible inference — consume it), and Provide Compute
  (run a TEE node on the grid to serve inference and earn USDC + SGL). Pay with
  USDC on Base or Solana, USDm on MegaETH via x402, optional MPP/Mppx, or
  pre-loaded USD credits. Includes optional OWS-backed auth and management flows.
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
          description: EVM private key for Base/MegaETH payment signing (use a dedicated low-balance wallet)
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
          description: Auth chain override — base, megaeth, or solana
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

Two products, one credit balance, one set of wallet/API-key auth:

- **SGL Machines** — provision, manage, resize, and extend GPU/VPS instances on Vultr or DigitalOcean. **API base:** `https://compute.x402layer.cc`
- **SGL Grid** — decentralized, confidential (TEE), **OpenAI-compatible** inference across attested nodes; token streaming + end-to-end encryption. **API base:** `https://grid.x402compute.cc` (see [SGL Grid — Inference](#sgl-grid--inference) below)
- **Provide Compute (run a node)** — turn a TEE-capable machine into a grid node: stake $SGL, register, attest, serve a model, earn USDC + SGL. Agentic via the `sgl` CLI. Operators can set a **custom per-token price** within a band (`sgl price set`, suggested × 0.5–× 5); callers compare nodes via `GET /v1/providers`. See [Provide Compute](#provide-compute-run-a-node) below and `references/node-operator.md`.
- **SGL Processors** — serverless TEE functions. *Coming soon.*

Pay with x402, MPP, or pre-loaded credits — the same `x402c_…` API key and prepaid credit balance work across Machines and Grid.

**x402 Networks:** Base (EVM) • Solana • MegaETH
**x402 Currency:** USDC (Base/Solana) • USDm (MegaETH)
**MPP Methods:** Tempo • Stripe/card when enabled by the service
**Credits:** Pre-load USD via x402 topup, then provision/extend (`use_credits: true`) or call the Grid with `X-API-Key`
**Protocol:** HTTP 402 Payment Required (`X-Payment` for x402, `Authorization: Payment` for MPP)
**$SGL:** native token, live on Solana — mint `5c4HyD2rSShqnTsf5z3SaoD2H3GE452u2CUuYjviBAGS` (staking secures the grid; see [staking.x402layer.cc](https://staking.x402layer.cc))

This section below (Machines) covers provisioning. Jump to **[SGL Grid — Inference](#sgl-grid--inference)** for the OpenAI-compatible inference API.

**Access Note:** Preferred access is SSH public key. If no SSH key is provided, a one-time password fallback can be fetched once via API.
**DigitalOcean Note:** DigitalOcean instances require SSH key access because one-time root passwords are not exposed through the DigitalOcean API.

---

## Quick Start

### 1. Install Dependencies
```bash
pip install -r {baseDir}/requirements.txt
```

### 2. Choose Wallet Mode

#### Option A: Direct signing keys (Base, MegaETH, or Solana)

> **Use a dedicated low-balance wallet.** Never use your primary custody wallet.

```bash
# Base (EVM) — same keys work for MegaETH
export PRIVATE_KEY=<your-evm-private-key>
export WALLET_ADDRESS=<your-evm-wallet-address>

# MegaETH (uses same EVM keys as Base)
export PRIVATE_KEY=<your-evm-private-key>
export WALLET_ADDRESS=<your-evm-wallet-address>
export COMPUTE_AUTH_CHAIN="megaeth"

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
| `provision.py` | Provision a new instance (x402 payment, `--months` or `--days`) |
| `create_api_key.py` | Create an API key for agent access (optional) |
| `list_instances.py` | List your active instances |
| `instance_details.py` | Get details for a specific instance |
| `get_one_time_password.py` | Retrieve one-time root password fallback |
| `extend_instance.py` | Extend instance lifetime (x402 payment) |
| `resize_instance.py` | Resize an instance in place (compute auth only) |
| `destroy_instance.py` | Destroy an instance |
| `ows_cli.py` | Run OpenWallet / OWS wallet, sign-message, and key commands |
| `solana_signing.py` | Internal helper for Solana x402 payment signing |

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

# DigitalOcean plans are prefixed with do:
# They require SSH key access.
python {baseDir}/scripts/provision.py do:s-1vcpu-1gb nyc3 --days 1 --label "do-test" --ssh-key-file ~/.ssh/x402_compute.pub

# Provision a daily instance (cheaper, use-and-throw)
python {baseDir}/scripts/provision.py vc2-1c-1gb ewr --days 1 --label "test-daily" --ssh-key-file ~/.ssh/x402_compute.pub

# Provision for 3 days
python {baseDir}/scripts/provision.py vc2-1c-1gb ewr --days 3 --label "short-task" --ssh-key-file ~/.ssh/x402_compute.pub

# Provision on Solana
python {baseDir}/scripts/provision.py vc2-1c-1gb ewr --months 1 --label "my-sol-vps" --network solana --ssh-key-file ~/.ssh/x402_compute.pub

# Provision on MegaETH (pays with USDm)
python {baseDir}/scripts/provision.py vc2-1c-1gb ewr --months 1 --label "my-mega-vps" --network megaeth --ssh-key-file ~/.ssh/x402_compute.pub

# Provision via MPP / mppx (Tempo by default; Stripe/card if your mppx config supports it)
npx mppx https://compute.x402layer.cc/compute/provision \
  -X POST \
  -J '{"plan":"vc2-1c-1gb","region":"ewr","os_id":2284,"label":"mpp-vps","prepaid_hours":24,"ssh_public_key":"ssh-ed25519 AAAA... agent"}'

# If the response includes management_api_key, store it for later instance management:
export COMPUTE_API_KEY="x402c_..."

# ⚠️ After provisioning, wait 2-3 minutes for Vultr to complete setup
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

# DigitalOcean disk growth is irreversible and must be confirmed explicitly
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
   - Solana: signed SPL transfer transaction payload
3. Script resends request with `X-Payment` header containing signed payload
4. Server verifies payment, settles on-chain, provisions/extends instance

MegaETH uses an embedded facilitator (no external CDP dependency). The user signs an off-chain ERC-2612 permit, and the facilitator calls `permit()` + `transferFrom()` on MegaETH (~10ms blocks, near-zero gas).

For Solana, transient facilitator failures can happen. Retry once or twice if you get a temporary 5xx verify error.

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

## SGL Grid — Inference

Decentralized, confidential inference across attested TEE nodes — **OpenAI-compatible**, so any OpenAI SDK works by pointing `base_url` at the grid. Requests are end-to-end encrypted and can stream token-by-token.

**API base:** `https://grid.x402compute.cc`
**Auth:** `X-API-Key: x402c_…` (billed to your prepaid credits — same key/credits as Machines) **or** per-request x402 via `X-Payment`.
**Billing:** pay-per-token in USDC (credits or x402). No subscription.

| Method | Path | Purpose |
|--------|------|---------|
| `GET`  | `/v1/models` | List models currently served by active attested nodes |
| `POST` | `/v1/chat/completions` | OpenAI-compatible chat (set `"stream": true` to stream) |
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

---

## Provide Compute (run a node)

The other side of the grid: turn a **TEE-capable machine** into a node that serves confidential,
OpenAI-compatible inference and **earns USDC + SGL** per settled job. Fully agentic — the installer
and the `sgl` CLI are shell commands. Full runbook (requirements, flags, maintenance, slashing,
earnings) → **`references/node-operator.md`**.

**Prerequisites:** a supported TEE (e.g. Apple Secure Enclave `apple_se`, Intel TDX/SGX, AMD SEV-SNP,
AWS Nitro), `llama.cpp` + a GGUF model, and **≥ 50,000 $SGL staked** to your operator (Solana) wallet.

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

**Maintenance:** `sgl off-grid` (stop new jobs cleanly for planned downtime — no penalty) / `sgl on-grid`
(resume). Honest downtime is never slashed; only proven tampering is. Re-run `sgl attest` after binary
updates. Docs: `https://docs.x402layer.cc/cloud/provide/node-setup`.

---

## Plan Types

| Type | Plan Prefix | Description |
|------|-------------|-------------|
| GPU | `vcg-*` | GPU-accelerated (A100, H100, etc.) |
| VPS | `vc2-*` | Standard cloud compute |
| High-Perf | `vhp-*` | High-performance dedicated |
| Dedicated | `vdc-*` | Dedicated bare-metal |
| DigitalOcean | `do:*` | DigitalOcean Droplets (provider-prefixed size slugs) |

---

## Environment Reference

| Variable | Required For | Description |
|----------|--------------|-------------|
| `PRIVATE_KEY` | Base/MegaETH payment signing | EVM private key (0x...) |
| `WALLET_ADDRESS` | Base/MegaETH direct-signing mode | EVM wallet address (0x...) |
| `SOLANA_SECRET_KEY` | Solana direct-signing mode | Solana signer key (base58 or JSON byte array) |
| `SOLANA_WALLET_ADDRESS` | Solana direct-signing mode | Solana wallet address (optional if derivable from secret) |
| `COMPUTE_AUTH_CHAIN` | Chain auth override | `base`, `megaeth`, or `solana` |
| `COMPUTE_API_KEY` | Optional | Reusable API key for compute management endpoints |
| `COMPUTE_AUTH_MODE` | Optional | `auto`, `private-key`, or `ows` |
| `OWS_WALLET` | OWS auth mode | OWS wallet name or ID |
| `OWS_BIN` | OWS auth mode | Optional explicit path to the `ows` executable |
| `COMPUTE_API_KEY` | MPP/no-wallet management | API key returned once after an MPP provision without wallet auth |

---

## API Reference

For full endpoint details, see:
- [references/api-reference.md](references/api-reference.md)
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
- keep direct Base, MegaETH, or Solana signing keys for the paid provision and extend flows
- resize, list, details, password fallback, and destroy work with normal compute auth / API keys
