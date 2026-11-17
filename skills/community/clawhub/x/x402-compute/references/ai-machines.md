# AI Machines — One-Click GPU Running an LLM

**AI Machines** are the fastest path from "I want an LLM" to a running model: provision a GPU
instance that comes up **already running an LLM**, with the serving mode chosen at deploy time. It's
the same x402-native lifecycle as any SGL Machine (provision / manage / resize / extend / destroy),
just with one extra **nested** deploy object — `ai_machine` (private) or `deploy_node` (grid).

- **API base:** `https://compute.x402layer.cc`
- **Tier:** **Standard** (not confidential / not TEE). For confidential inference, use the SGL Grid
  (see the main SKILL "SGL Grid — Inference") or run a TEE node (`references/node-operator.md`).
- **Fully managed:** the box is kept alive, auto-updates are applied (allowlist-gated), and SSH stays
  available for you.
- **Agent-friendly:** an agent with a funded wallet can deploy, extend, and destroy an AI Machine
  entirely over x402 — no dashboard needed.

---

## The two modes (chosen at deploy)

Each mode is a **nested object** on the provision body. They are **mutually exclusive** (the server
rejects a request that includes both):

- **Private** → `"ai_machine": { "model_id": "<id>", "mode": "private" }` (`mode` must be `"private"`).
- **Grid** → `"deploy_node": { "model_id": "<id>" }`.

### 1. `ai_machine` (private) — your own OpenAI-compatible endpoint

Deploys a GPU running `llama-server`, which exposes an **OpenAI-compatible** API on port `8080`:

- `POST /v1/chat/completions`
- `GET /v1/models`

The provision response returns `order.ai = { model_id, api_key, endpoint, ... }`. `endpoint` is the
machine's **HTTPS** OpenAI-compatible base URL, already ending in `/v1`:
`https://ai.x402compute.cc/<order-id-or-slug>/v1` (VM providers) or the provider's HTTPS proxy
(RunPod). Always use it: it is TLS-encrypted and accepts your managed keys. Do not call the box's raw
IP or port directly; that path is unencrypted and would expose your key and conversations.
Authenticate with `Authorization: Bearer <api_key>`. Point any OpenAI-compatible client, agent
framework, or router at it (base URL = `endpoint`, API key = the returned key). Until the machine
finishes booting the endpoint answers "warming up"; poll `GET /compute/instances/:id`.

> **OpenRouter-ready:** because it speaks the OpenAI schema, it works with any OpenAI-compatible
> client out of the box. Listing it *as a provider on OpenRouter itself* is a separate OpenRouter
> approval process and is **roadmap**, not something this deploy does for you.

### 2. `deploy_node` (grid) — join the grid & earn

Deploys the machine as a **grid node** that serves inference to the SGL Grid and earns **USDC + SGL**
per settled job. Requires **≥ 50,000 $SGL staked** to the wallet (the same requirement as any node —
see `references/node-operator.md`). This is the "provide compute / earn" side rather than "I want a
private endpoint" side.

| Mode | Deploy object | You get | Requires |
|------|---------------|---------|----------|
| private | `ai_machine: { model_id, mode:"private" }` | Your own OpenAI-compatible endpoint (URL + API key) | funded wallet for the **x402 deploy** (credits not accepted) |
| grid | `deploy_node: { model_id }` | Node that serves the grid and earns USDC + SGL | funded wallet **+ 50,000 SGL staked** |

---

## Deploy (x402)

Add the nested `ai_machine` (private) or `deploy_node` (grid) object to deploy an AI Machine.
Everything else is the normal provision request (`plan`, `region`, `os_id`, duration). `os_id` is the
provider GPU image id from the machine catalog (it varies by provider — do not hardcode it).

### Via the bundled script

```bash
# Private OpenAI-compatible endpoint, 1 day
python scripts/provision.py vcg-a100-1c-2g-6gb lax --days 1 --label "my-llm" \
    --model-id llama-3.2-3b --mode private

# Join the grid & earn (wallet must have 50k SGL staked), 1 month
python scripts/provision.py vcg-a100-1c-2g-6gb lax --months 1 --label "grid-node" \
    --model-id llama-3.2-3b --mode grid

# Pay on Solana instead of Base
python scripts/provision.py vcg-a100-1c-2g-6gb lax --days 1 --label "my-llm" \
    --model-id llama-3.2-3b --mode private --network solana
```

On success in `private` mode the script prints the OpenAI-compatible **endpoint** and the **API key**
(shown once — store it).

### Raw x402 (what the script does)

`POST /compute/provision` with the nested `ai_machine` object, then the standard 402 → sign → resend
flow:

```json
{
  "plan": "vcg-a100-1c-2g-6gb",
  "region": "lax",
  "os_id": "<provider-gpu-image-id>",
  "label": "my-llm",
  "prepaid_hours": 720,
  "network": "base",
  "ai_machine": { "model_id": "llama-3.2-3b", "mode": "private" }
}
```

Grid deploy uses `"deploy_node": { "model_id": "llama-3.2-3b" }` instead (mutually exclusive with
`ai_machine`).

1. Server returns `402` with `accepts[]` (Base USDC / Solana / MegaETH USDm / Robinhood USDG).
2. Sign the payment locally (USDC `TransferWithAuthorization` on Base, USDG `TransferWithAuthorization` on Robinhood Chain, SPL transfer on Solana).
3. Resend with the `X-Payment` header.
4. Server settles on-chain and provisions the GPU with the model running.

> Private **AI Machines** require an **x402 wallet payment** — `"use_credits": true` is rejected for
> `ai_machine`. Prepaid credits work for bare and grid machines (authenticate with `X-API-Key`; see
> the main SKILL "Credits" workflow).

---

## Using a private endpoint

Once `private` mode returns the endpoint + API key, it is a drop-in OpenAI endpoint (`<ENDPOINT>` = `order.ai.endpoint`, HTTPS, already ends in `/v1`):

```bash
# List the model(s) the box serves
curl <ENDPOINT>/models -H "Authorization: Bearer <RETURNED_API_KEY>"

# Chat completion
curl -X POST <ENDPOINT>/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <RETURNED_API_KEY>" \
  -d '{"model":"llama-3.2-3b","messages":[{"role":"user","content":"Hello"}]}'
```

Any OpenAI SDK / agent framework / router (Cursor, opencode, LibreChat, LangChain, etc.) works by
setting the client's base URL to `<ENDPOINT>` and its API key to the key returned when you provisioned.

> This is your **own dedicated box**, distinct from the shared, confidential SGL Grid at
> `https://grid.x402compute.cc`. Pick AI Machines when you want a private, dedicated LLM endpoint;
> pick the Grid when you want confidential, pay-per-token, multi-node inference.

---

## Full control API (same lifecycle as any Machine)

All management endpoints use compute auth (`X-API-Key: x402c_…` or wallet-signature headers).

| Method | Path | Purpose |
|--------|------|---------|
| `POST`   | `/compute/provision` | Deploy. For an AI machine add the nested `ai_machine` (private) or `deploy_node` (grid) object. Required base fields: `plan`, `region`, `os_id`. Provision uses `prepaid_hours`. |
| `GET`    | `/compute/instances` | List your instances |
| `GET`    | `/compute/instances/:id` | Instance details (IP, status, expiry) |
| `POST`   | `/compute/instances/:id/extend` | **Extend runtime** (x402/MPP/credits) — the most-used action; extend before expiry |
| `POST`   | `/compute/instances/:id/resize` | Resize in place (compute auth only; no new payment — preserves prepaid value via new expiry) |
| `POST`   | `/compute/instances/:id/password` | One-time SSH root password fallback (Vultr; used once, then `409`) |
| `DELETE` | `/compute/instances/:id` | Destroy |
| `POST`   | `/compute/credits/topup` | Top up prepaid USD credits via x402 |

Extend is the one to remember: AI Machines expire after their prepaid duration, so keep them alive by
extending before `expires_at`.

```bash
# Extend an AI machine by a month
python scripts/extend_instance.py <instance_id> --hours 720

# Or raw (credits):
curl -X POST https://compute.x402layer.cc/compute/instances/<id>/extend \
  -H "Content-Type: application/json" -H "X-API-Key: $COMPUTE_API_KEY" \
  -d '{"extend_hours":720,"use_credits":true}'
```

---

## Agent deploys an AI Machine (end-to-end, x402)

A funded-wallet agent can run the whole lifecycle with no human in the loop. This reuses the skill's
existing x402 payment path (`scripts/wallet_signing.py` / `scripts/solana_signing.py`) — no new
payment scheme.

```bash
# 0. One dedicated low-balance wallet for the agent. Set PRIVATE_KEY (EVM: Base by default; the
#    same key works for MegaETH and Robinhood via COMPUTE_AUTH_CHAIN) or, for Solana,
#    SOLANA_SECRET_KEY + COMPUTE_AUTH_CHAIN=solana. See SKILL.md "Choose Wallet Mode".
export WALLET_ADDRESS=<evm-wallet-address>

# 1. Deploy a private LLM endpoint, non-interactive (-y skips the confirm prompt)
python scripts/provision.py vcg-a100-1c-2g-6gb lax --days 1 --label "agent-llm" \
    --model-id llama-3.2-3b --mode private -y
#   → prints Endpoint + API Key (capture from stdout / the returned JSON)

# 2. Use it — it's an OpenAI-compatible endpoint (see "Using a private endpoint" above)

# 3. Keep it alive if the task runs long
python scripts/extend_instance.py <instance_id> --hours 24 -y

# 4. Tear it down when done
python scripts/destroy_instance.py <instance_id>
```

Spend guard: `provision.py` / `extend_instance.py` refuse to pay above `COMPUTE_MAX_SPEND_USD`
(default $500) unless overridden with `--max-spend`. Keep the agent wallet low-balance.

---

## Managed & SSH notes

- **Kept alive + auto-updated:** the platform maintains the box and applies allowlisted updates. You
  don't babysit the process.
- **SSH:** provide `ssh_public_key` at provision for key access (recommended). On Vultr, if you skip
  the key you can fetch a one-time root password once via `POST /compute/instances/:id/password`.
  DigitalOcean plans require an SSH key (no password fallback).
- **Standard tier:** AI Machines are not confidential. Don't send data you need cryptographically
  shielded from the host — for that, use the confidential SGL Grid or a TEE node.

---

## Roadmap (not shipped)

- Listing a private AI Machine **as a provider on OpenRouter** (their approval flow). Today the box is
  OpenRouter-*ready* (OpenAI-compatible), not an approved OpenRouter provider.
