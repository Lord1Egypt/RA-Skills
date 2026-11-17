# x402Compute API Reference

Base URL: `https://compute.x402layer.cc`

Paid endpoints support both protocols:

- **x402**: server returns JSON `accepts[]`; client retries with `X-Payment`.
- **MPP**: server returns `WWW-Authenticate: Payment`; client retries with `Authorization: Payment ...`; success includes `Payment-Receipt`.

Compute plans can be backed by multiple providers:

- `provider: "vultr"` uses existing Vultr plan IDs, regions, OS images, and password fallback support.
- `provider: "digitalocean"` uses DigitalOcean Droplet sizes prefixed as `do:<size_slug>`.
- DigitalOcean instances require SSH key access because the DigitalOcean API does not expose initial root passwords.

## Endpoints

### Authentication (Required for management endpoints)

All **instance management** endpoints require authentication. Provision/extend accept x402 payment without compute auth headers. Choose one for management:

- **Signature Auth (wallet signing)**  
  Required headers:
  - `X-Auth-Address`: wallet address
  - `X-Auth-Chain`: `base`, `megaeth`, `robinhood`, or `solana`
  - `X-Auth-Signature`: signature over the request
  - `X-Auth-Timestamp`: epoch millis
  - `X-Auth-Nonce`: unique nonce
  - `X-Auth-Sig-Encoding`: `hex` (EVM: base/megaeth/robinhood) or `base64` (Solana)

- **API Key Auth (agent access)**
  Required header:
  - `X-API-Key`: compute API key (create via `POST /compute/api-keys`)

### Agent Pods

Agent Pod endpoints use the same compute auth (`X-API-Key`, signed session, or wallet
signature). A pod is a compute order, so the returned `pod.id` is also the instance id for
extend/destroy.

| Endpoint | Purpose |
|----------|---------|
| `GET /pods/catalog` | Public catalog: agents, tiers, channels, templates, pricing |
| `POST /pods` | Deploy a managed or BYOK Agent Pod |
| `GET /pods` | List owned pods |
| `GET /pods/{id}` | Pod details, heartbeat, masked credentials, customization |
| `PATCH /pods/{id}/settings` | Model/provider/settings/customization update |
| `POST /pods/{id}/actions` | Queue lifecycle action: restart, redeploy, update, diagnose, logs, cron |
| `POST /pods/{id}/api-keys` | Mint a pod-scoped `sk-sglpod-int-*` key for the OpenAI adapter |
| `POST /pods/{id}/v1/chat/completions` | OpenAI-compatible chat with the pod via `Authorization: Bearer sk-sglpod-int-*` |

`POST /pods` and `PATCH /pods/{id}/settings` accept the platform customization layer:

| Field | Max | Notes |
|-------|-----|-------|
| `agent_identity` | 8000 chars | Owner/platform identity text rendered into managed `AGENTS.md` and `IDENTITY.md`. |
| `agent_instructions` | 8000 chars | Owner/platform instructions rendered into managed `AGENTS.md`. |
| `heartbeat_prompt` | 4000 chars | Custom quiet self-check prompt. Empty or `null` on PATCH restores the default. |
| `agent_heartbeat_minutes` | server bounded | `0` disables self-checks; otherwise 15-1440 minutes. |

Raw `AGENTS.md` replacement is intentionally not exposed. The managed base keeps wallet
survival, x402 spend controls, security boundaries, and tool permissions intact; custom text is
layered into a bounded owner/platform section. Full pod details are in
`references/agent-pods.md`; the platform API-key surface is in `references/agent-pods-api.md`.

### GET /compute/plans

List available compute plans with pricing.

**Query Parameters:**
- `type` (optional): Filter by plan type — `vps`, `vhp`, `vdc`, `vcg` (GPU)

**Response:**
```json
{
  "plans": [
    {
      "id": "vcg-a100-1c-2g-6gb",
      "vcpu_count": 12,
      "ram": 120832,
      "disk": 1600,
      "bandwidth": 10240,
      "monthly_cost": 90,
      "type": "GPU",
      "gpu_vram_gb": 80,
      "gpu_type": "NVIDIA A100",
      "locations": ["lax", "ewr", "ord"]
    }
  ],
  "count": 1
}
```

Prices include the platform markup and are in USD. Plans now include `our_daily` pricing (hourly × 24). The x402 payment amount is calculated from the hourly rate times `prepaid_hours`, converted to stablecoin atomic units (6 decimals — USDC on Base/Solana, USDm on MegaETH, USDG on Robinhood Chain).

---

### GET /compute/regions

List available deployment regions.

**Response:**
```json
{
  "regions": [
    {
      "id": "lax",
      "city": "Los Angeles",
      "country": "US",
      "continent": "North America"
    }
  ]
}
```

---

### GET /compute/os

List available operating system images.

**Response:**
```json
{
  "os_options": [
    {
      "id": 2284,
      "name": "Ubuntu 24.04 LTS x64",
      "arch": "x64",
      "family": "ubuntu"
    }
  ]
}
```

---

### GET /compute/credits/balance

Get credit balance for the authenticated wallet.

**Headers:**
- Auth headers (see Authentication above)

**Response (200):**
```json
{
  "wallet": "0x...",
  "balance": "150.00",
  "total_deposited": "200.00",
  "total_spent": "50.00"
}
```

If no credits have been deposited, returns `{ "balance": 0, "total_deposited": 0, "total_spent": 0 }`.

---

### POST /compute/credits/topup

Top up credits via x402 payment. Returns `402 Payment Required` if no `X-Payment` header.

**Request Body:**
```json
{
  "amount": 50,
  "network": "base"
}
```

- `amount`: USD to deposit (minimum $1 — **$5 on Arc**, because Arc gas is paid in USDC and comes off the sale)
- `network`: `base`, `solana`, `megaeth`, `robinhood`, or `arc` (base/solana/arc = USDC, megaeth = USDm, robinhood = USDG). Arc is EIP-3009 `transferWithAuthorization` like Base/Robinhood — same signing flow, domain name `"USDC"` version `"2"` chainId `5042`; explorer: explorer.arc.io. **Machines, AI Machines and extensions also accept `network: "arc"` directly** — direct Arc payments carry the same $5 minimum; smaller prepayments go through credits.

**Headers:**
- Auth headers (see Authentication above)
- `X-Payment`: Base64-encoded x402 payment payload (after 402 challenge)

**Success Response (200):**
```json
{
  "success": true,
  "deposited": 50,
  "new_balance": "150.00",
  "tx_hash": "0x..."
}
```

---

### POST /compute/provision

Provision a new compute instance. Returns `402 Payment Required` with x402 and, when configured, MPP payment challenges — unless `use_credits` is `true`.

**Request Body:**
```json
{
  "plan": "vc2-1c-1gb",
  "region": "ewr",
  "os_id": 2284,
  "label": "my-daily-instance",
  "prepaid_hours": 24,
  "ssh_public_key": "ssh-ed25519 AAAA... user@host",
  "provider": "vultr",
  "network": "base",
  "use_credits": false
}
```

**Notes:**
- `prepaid_hours` minimum is **24** (1 day). Use `24` for daily, `72` for 3 days, `168` for 1 week, `720` for 1 month, etc.
- Provide `ssh_public_key` to enable SSH access. Passwords are not returned by the API.
- If you do not provide an SSH key, use one-time fallback endpoint `POST /compute/instances/:id/password`.
- For DigitalOcean plans, `ssh_public_key` or existing `ssh_key_id(s)` is required. Password fallback is Vultr-only.
- DigitalOcean plan IDs are prefixed, for example `do:s-1vcpu-1gb`.
- Set `use_credits: true` to deduct from pre-loaded credit balance instead of requiring x402/MPP payment. Auth is required for the credit path. If balance is insufficient, returns `402` with the shortfall.
- `network` also accepts `"arc"` (USDC on Arc, EIP-3009 chainId 5042). **Direct Arc payments carry a $5 minimum** — Arc gas is USDC and comes off the sale — so a 24-hour micro-instance is refused with a pointer to credits; `use_credits: true` with an Arc-funded balance has no floor. Same for `/compute/instances/:id/extend`.
- **AI Machine:** add a **nested** object to deploy a GPU that comes up running an LLM. The two are mutually exclusive:
  - `"ai_machine": { "model_id": "<id>", "mode": "private" }` — a dedicated **OpenAI-compatible** endpoint (`mode` must be `"private"`). The success order carries `order.ai = { model_id, api_key, endpoint, ... }`. `endpoint` is the HTTPS OpenAI-compatible base URL, already ending in `/v1` (`https://ai.x402compute.cc/<order-id-or-slug>/v1` for VM providers), serving `/chat/completions` and `/models` with `Authorization: Bearer <api_key>`. Always use it; never call the box's raw IP/port (unencrypted). Pay with x402 or with credits (`use_credits: true`); deploying a trained model requires credits.
  - `"deploy_node": { "model_id": "<id>" }` — joins the grid to serve inference and earn USDC + SGL (requires ≥ 50,000 $SGL staked to the paying wallet; x402 Solana payment).
  - `os_id` is the provider GPU image id from the catalog (varies by provider). AI Machines are the **Standard** tier (not confidential/TEE). Full detail in `references/ai-machines.md`.

**Headers:**
- Auth headers (see Authentication above)
- `X-Payment`: Base64-encoded x402 payment payload (after 402 challenge)
- `Authorization: Payment ...`: MPP credential (after MPP challenge)

**402 Challenge Response:**
```json
{
  "x402Version": 1,
  "accepts": [
    {
      "scheme": "exact",
      "network": "base",
      "maxAmountRequired": "90000000",
      "resource": "https://compute.x402layer.cc/compute/provision",
      "payTo": "0x...",
      "extra": { "name": "USD Coin", "version": "2" }
    }
  ]
}
```

For Solana challenges, `network` may be `solana` (or facilitator-style `solana:*`) and may include `extra.feePayer`.

**MPP Example:**
```bash
npx mppx https://compute.x402layer.cc/compute/provision \
  -X POST \
  -J '{"plan":"vc2-1c-1gb","region":"ewr","os_id":2284,"label":"mpp-vps","prepaid_hours":24,"ssh_public_key":"ssh-ed25519 AAAA... agent"}'
```

If MPP provisioning is paid without wallet/API-key auth, the success response includes a one-time `management_api_key`. Store it and use it for `GET /compute/instances`, `POST /compute/instances/:id/resize`, `POST /compute/instances/:id/extend`, password retrieval, and destroy.

**Success Response (200):**
```json
{
  "success": true,
  "order": {
    "id": "uuid",
    "vultr_instance_id": "...",
    "plan": "vcg-a100-1c-2g-6gb",
    "region": "lax",
    "status": "active",
    "ip_address": "1.2.3.4",
    "expires_at": "2026-03-17T00:00:00Z"
  },
  "tx_hash": "0x..."
}
```

**Additional MPP-only fields when no wallet/API-key auth was supplied:**
```json
{
  "management_api_key": "x402c_...",
  "management_api_key_id": "uuid",
  "management_api_key_last4": "abcd",
  "management_note": "Store this API key securely. It is shown once..."
}
```

---

### GET /compute/instances

List your active instances.

**Headers:**
- Auth headers (see Authentication above)

---

### GET /compute/instances/:id

Get details for a specific instance.

**Headers:**
- Auth headers (see Authentication above)

---

### DELETE /compute/instances/:id

Destroy an instance immediately.

**Headers:**
- Auth headers (see Authentication above)

---

### POST /compute/instances/:id/password

Retrieve one-time root password fallback (only if SSH key was not used).

**Headers:**
- Auth headers (see Authentication above)

**Response (200):**
```json
{
  "success": true,
  "access": {
    "method": "one_time_password",
    "username": "root",
    "ip_address": "1.2.3.4",
    "password": "example-password"
  }
}
```

Subsequent calls return `409`.

---

### POST /compute/instances/:id/extend

Extend an instance's lifetime. Returns `402 Payment Required` with x402 and, when configured, MPP payment challenges — unless `use_credits` is `true`.

**Request Body:**
```json
{
  "extend_hours": 720,
  "network": "base",
  "use_credits": false
}
```

**Headers:**
- Auth headers (see Authentication above)
- `X-Payment`: Base64-encoded x402 payment payload (after 402 challenge)
- `Authorization: Payment ...`: MPP credential (after MPP challenge)

MPP extension requires compute auth because MPP card/Stripe payments do not always identify a wallet owner. Use the `management_api_key` returned from MPP provisioning:

```bash
npx mppx https://compute.x402layer.cc/compute/instances/<instance_id>/extend \
  -X POST \
  -H "X-API-Key: $COMPUTE_API_KEY" \
  -J '{"extend_hours":720}'
```

Set `use_credits: true` to extend using pre-loaded credits instead of x402/MPP payment. Auth is required, and the wallet must own the instance.

---

### POST /compute/instances/:id/resize

Resize an active instance in place on its current provider.

**Request Body:**
```json
{
  "plan": "vc2-2c-4gb"
}
```

**Optional confirmation for irreversible disk growth:**
```json
{
  "plan": "do:s-2vcpu-4gb",
  "confirm_disk_resize": true
}
```

**Headers:**
- Auth headers (see Authentication above)

**Behavior:**
- Resize is a management action only. It does **not** create a new x402 or MPP payment challenge.
- The API preserves remaining prepaid dollar credit and recalculates `expires_at` for the target hourly rate.
- Resize stays on the current provider and region.
- Vultr is upgrade-only.
- DigitalOcean disk increases are irreversible and require `confirm_disk_resize: true`.

**Example:**
```bash
curl -X POST https://compute.x402layer.cc/compute/instances/<instance_id>/resize \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $COMPUTE_API_KEY" \
  -d '{"plan":"vc2-2c-4gb"}'
```

---

### POST /compute/api-keys

Create an API key for agent access (signature auth required).

**Request Body:**
```json
{
  "label": "my-agent"
}
```

**Response (201):**
```json
{
  "api_key": "x402c_...",
  "id": "uuid",
  "label": "my-agent",
  "created_at": "2026-02-18T00:00:00Z"
}
```

---

### GET /compute/api-keys

List API keys for your wallet.

**Response:**
```json
{
  "api_keys": [
    {
      "id": "uuid",
      "label": "my-agent",
      "key_last4": "abcd",
      "created_at": "2026-02-18T00:00:00Z",
      "revoked_at": null
    }
  ]
}
```

---

### DELETE /compute/api-keys/:id

Revoke an API key (signature auth required).

---

## SGL Grid — Inference (base: `https://grid.x402compute.cc`)

Decentralized confidential inference. Chat and embeddings expose their documented
OpenAI-compatible shapes. System One and transcription use separate contracts. Auth with your API
key as **either** `Authorization: Bearer x402c_…` or `X-API-Key: x402c_…` (billed to prepaid
credits — same key/credits as Machines), or per-request x402 via `X-Payment`. Billing units depend
on the workload; transcription uses exact sample-derived audio duration with the charge rounded up to micro-USDC.

### GET /v1/models

List models currently served by active nodes that satisfy the requested tier and model capability.

```bash
curl https://grid.x402compute.cc/v1/models -H "X-API-Key: x402c_..."
curl "https://grid.x402compute.cc/v1/models?type=embedding" -H "X-API-Key: x402c_..."
curl "https://grid.x402compute.cc/v1/models?type=systemone" -H "X-API-Key: x402c_..."
curl "https://grid.x402compute.cc/v1/models?type=transcription" -H "X-API-Key: x402c_..."
```

### POST /v1/embeddings

OpenAI-compatible input-only embeddings. Existing text models accept a string or string array.
The release-gated `embeddinggemma-2` model adds ordered text, image, audio, video, and mixed
items at 768/512/256/128 dimensions. It is callable only while listed by
`GET /v1/models?type=embedding`.

Multimodal media is inline canonical base64 with its lowercase SHA-256. Audio/video also require
verified `duration_seconds`. The 24 MiB encoded body, media, batch, and 8,192 processed-token
limits are enforced before payment and again at the runtime boundary. See the complete contract,
stable error table, and Local app path in `references/multimodal-embeddings.md`.

Omitted EmbeddingGemma 2 `input_type` defaults to `query`; send `unspecified` only to opt out
of retrieval prefixing. Legacy omission retains each model's existing behavior. The sealed input
envelope becomes purge-eligible 30 minutes after terminal status and the encrypted result after
one hour. Because cleanup runs hourly, practical upper bounds are about 90 minutes and two hours.
Plaintext node failure details are never persisted.

```bash
python {baseDir}/scripts/grid_embeddings.py embed \
  --text "A searchable document" --input-type document --dimensions 256
```

### POST /v1/audio/transcriptions/reserve + /v1/audio/transcriptions

Default-off client-sealed speech-to-text. The reserve call sends metadata/sample count only and
returns a verified node identity, short-lived token, immutable model pins, and quote. The client
then seals one raw mono 16 kHz signed 16-bit PCM utterance to that node and submits the reservation
token plus JSON `enc` object. The Worker never receives plaintext audio. This is not multipart,
streaming, or OpenAI wire compatibility.

Use the official SDK helper or `scripts/grid_transcription.py`; never hand-roll a plaintext
fallback. The exact 60-second/1,920,000-byte bound, $0.0001/exact-audio-second price (4.2 seconds = $0.000420; $0.0001 minimum), privacy and
retention rules, result validation, and release gates are in `references/transcription.md`.

```bash
python {baseDir}/scripts/grid_transcription.py models
python {baseDir}/scripts/grid_transcription.py transcribe ./utterance.pcm --dry-run
```

Do not call either endpoint unless the type-filtered model list returns `whisper-1`.

### POST /v1/chat/completions

OpenAI-compatible chat completion. Set `"stream": true` for token streaming (SSE; each chunk is end-to-end encrypted). Body matches the OpenAI schema (`model`, `messages`, optional `temperature`, `max_tokens`, `stream`). Works with any OpenAI SDK via `base_url=https://grid.x402compute.cc/v1`.

```bash
curl -X POST https://grid.x402compute.cc/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "X-API-Key: x402c_..." \
  -d '{"model":"llama-3.2-3b","messages":[{"role":"user","content":"Hello"}]}'
```

Errors: `401` invalid/revoked API key · `402` payment required (resend with `X-Payment`) or insufficient credits (top up in Settings → Credits).

### POST /v1/messages (Anthropic-compatible)

The Anthropic Messages API on Grid models, streaming and non-streaming, with tools and (on
vision models) base64 images. Auth is `x-api-key: x402c_...` or `Authorization: Bearer x402c_...`,
or x402 via `X-Payment`. Base URL for Anthropic SDKs and Claude Code is
`https://grid.x402compute.cc` (no `/v1`). Model ids are Grid ids.

```bash
curl -s https://grid.x402compute.cc/v1/messages \
  -H "x-api-key: x402c_..." -H "anthropic-version: 2023-06-01" -H "content-type: application/json" \
  -d '{"model":"qwen-2.5-32b","max_tokens":512,"messages":[{"role":"user","content":"Hello"}]}'
```

- `POST /v1/messages/count_tokens` returns `{"input_tokens": N}` (estimate, free, no auth).
- `GET /v1/models` with an `anthropic-version` header returns the Anthropic model list shape,
  including `max_input_tokens`. `GET /v1/models/{model_id}` returns one model.
- Claude Code: `ANTHROPIC_BASE_URL=https://grid.x402compute.cc` plus `ANTHROPIC_API_KEY` set to a
  compute key. Use a model with well over 13k `max_input_tokens` (today `qwen-2.5-32b`, 32k).

Supported fields, ignored hints, refused features and billing notes: `references/grid-anthropic-messages.md`.

### POST /v1/systemone

Laya/System One typed decisions. Current model: `convaiinnovations/laya` (aliases: `laya`,
`laya-system-one`, `systemone-laya`). This is not OpenAI chat; sending Laya to
`/v1/chat/completions` returns `wrong_endpoint_for_model`.

```bash
curl -X POST https://grid.x402compute.cc/v1/systemone \
  -H "Content-Type: application/json" \
  -H "X-API-Key: x402c_..." \
  -d '{"model":"convaiinnovations/laya","state":{"ticket":"refund request"},"questions":{"route":{"type":"choice","instructions":"Pick the best team.","criteria":{"billing":"Billing or refund","support":"Technical support"}}}}'
```

Question types: `choice`, `score`, `noul`. Limits: 64 KiB state, 32 questions, 64 criteria per
question, 16,384 input tokens, 256 KiB request, 1 MiB response. Billing is input-only. For
end-to-end private Laya, first call `POST /v1/systemone/reserve`, encrypt locally to the returned
node key, then submit the sealed payload to `POST /v1/systemone`. See `references/systemone-laya.md`.

### GET /grid/capacity

Live grid capacity — active node count, TEE types, served models, and an `at_capacity` flag. No auth. Check before a large batch and back off if `at_capacity` is true.

```bash
curl https://grid.x402compute.cc/grid/capacity
```

### GET /v1/providers

Compare the nodes serving a model, with each node's effective per-token price (custom if the operator set one, else the suggested reference), sorted cheapest-first. No auth. Optional `cluster` filter. Pass a chosen `node` to `/v1/chat/completions` (or the `node=` arg in the SDKs) to pin that provider; omit it to let the grid route.

```bash
curl "https://grid.x402compute.cc/v1/providers?model=llama-3.2-3b"
# {"model":"llama-3.2-3b","count":2,"providers":[
#   {"node_id":"…","input_per_m":0.004,"output_per_m":0.004,"blended_per_1k":4e-06,"is_custom":true,"online":true}, …]}
```

**Price cap (`max_price`):** instead of picking a node, add `"max_price": <USD per 1M tokens, blended>` to your `/v1/chat/completions` (or `/v1/reserve`) request — the grid routes only to nodes at/under that rate and never bills above it. Returns `price_cap_unmet` if none qualify. Available as `max_price` (Python) / `maxPrice` (TS) in the SDKs.

### GET /grid/nodes/:id/prices

Public. A node's per-model prices: the `reference` (suggested) rate, the allowed `floor`/`ceiling` band, the operator's `custom` price (or `null`), and the `effective` price billed.

```bash
curl https://grid.x402compute.cc/grid/nodes/<NODE_ID>/prices
```

### POST /grid/nodes/:id/prices

Operator-only — set or reset a model's price. Auth with the node token (`X-Node-Auth`, used by `sgl price …`) **or** an owner wallet signature. Band-enforced (suggested × 0.5 … × 5), the model must be one the node advertises, and there's a short cooldown between changes. Body: `{ "model": "...", "input_per_m": 0.004, "output_per_m": 0.004 }` (or `{ "model": "...", "reset": true }`).

```bash
curl -X POST https://grid.x402compute.cc/grid/nodes/<NODE_ID>/prices \
  -H "X-Node-Auth: <node-token>" -H "Content-Type: application/json" \
  -d '{"model":"llama-3.2-3b","input_per_m":0.004,"output_per_m":0.004}'
```
