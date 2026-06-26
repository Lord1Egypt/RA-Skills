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
  - `X-Auth-Chain`: `base` or `solana`
  - `X-Auth-Signature`: signature over the request
  - `X-Auth-Timestamp`: epoch millis
  - `X-Auth-Nonce`: unique nonce
  - `X-Auth-Sig-Encoding`: `hex` (Base) or `base64` (Solana)

- **API Key Auth (agent access)**
  Required header:
  - `X-API-Key`: compute API key (create via `POST /compute/api-keys`)

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

Prices include the platform markup and are in USD. Plans now include `our_daily` pricing (hourly × 24). The x402 payment amount is calculated from the hourly rate times `prepaid_hours`, converted to USDC atomic units (6 decimals).

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

- `amount`: USD to deposit (minimum $1)
- `network`: `base`, `solana`, or `megaeth`

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

Decentralized, confidential, **OpenAI-compatible** inference. Auth with your API key as **either** `Authorization: Bearer x402c_…` (standard OpenAI style — works with the OpenAI SDK, Cursor, opencode, LibreChat, etc.) **or** `X-API-Key: x402c_…` (billed to prepaid credits — same key/credits as Machines), or per-request x402 via `X-Payment`. Pay-per-token in USDC.

### GET /v1/models

List models currently served by active attested nodes.

```bash
curl https://grid.x402compute.cc/v1/models -H "X-API-Key: x402c_..."
```

### POST /v1/chat/completions

OpenAI-compatible chat completion. Set `"stream": true` for token streaming (SSE; each chunk is end-to-end encrypted). Body matches the OpenAI schema (`model`, `messages`, optional `temperature`, `max_tokens`, `stream`). Works with any OpenAI SDK via `base_url=https://grid.x402compute.cc/v1`.

```bash
curl -X POST https://grid.x402compute.cc/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "X-API-Key: x402c_..." \
  -d '{"model":"llama-3.2-3b","messages":[{"role":"user","content":"Hello"}]}'
```

Errors: `401` invalid/revoked API key · `402` payment required (resend with `X-Payment`) or insufficient credits (top up in Settings → Credits).

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
