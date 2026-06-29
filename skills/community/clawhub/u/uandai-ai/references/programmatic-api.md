# Uandai Programmatic API Guide

**Docs-Version:** 2026.06.25 (spec v1.10)  
**OpenAPI:** `{API_ORIGIN}/openapi.json`  
**Related:** [Agent packaging guide](./agent-packaging.md) — create the upload zip first.  
**Subscribers (OpenClaw gateway):** [OpenClaw integration guide](./openclaw-integration.md).

---

## Base URL

| Environment | Base URL |
|-------------|----------|
| Production | `https://api.uandai.ai/api` |
| Local dev | `http://127.0.0.1:8000/api` |

Paths below are relative to `/api` (e.g. upload URL is `{BASE}/v1/agents/upload`). Legacy `{BASE}/agents/upload` remains supported.

---

## Authentication

### Create an API key (human / browser only)

Create keys in **uandai.ai app → Settings → API Keys** (JWT login required). The full secret is shown **once**.

Management endpoints (`/v1/me/api-keys`) accept **password JWT only** — not raw API keys, not JWT from key exchange.

### Session exchange (required for automation)

Exchange the raw key **once** for JWT access + refresh. Raw `uand_live_…` is **not** accepted on upload, invoke, or other business endpoints.

```http
POST /v1/auth/token
Authorization: Bearer uand_live_<secret>
```

Alternative on exchange only:

```http
X-Uandai-Api-Key: uand_live_<secret>
```

Or JSON body: `{ "api_key": "uand_live_<secret>" }`

Response: `{ "access_token", "refresh_token", "user" }` — **no cookie**.

Access tokens include a `sid` (session id) claim. If the API key or bound session is revoked, access tokens fail **immediately** — not after expiry.

### Token lifecycle

1. **Exchange** — `POST /v1/auth/token` with raw key → store `access_token` + `refresh_token`
2. **Call APIs** — `Authorization: Bearer <access_token>` on all programmatic endpoints
3. **Refresh** — when access expires (~15 min): `POST /v1/auth/refresh` with `refresh_token`
4. **Re-exchange** — if refresh fails (key revoked, TTL expired): exchange again with raw key if still active, else create a new key in Settings

### Environment variables (OpenClaw / scripts)

```bash
export UANDAI_API_ORIGIN="https://api.uandai.ai"
export APP_SITE_URL="https://app.uandai.ai"   # web app — manage agents UI
export UANDAI_API_KEY="uand_live_..."         # bootstrap only — exchange before API calls
# API base URL is always derived: ${UANDAI_API_ORIGIN}/api
```

Never paste keys into chat logs. Cache `access_token` / `refresh_token` in process memory, not in env.

---

## Typical trainer workflow

**Minimal ZIP upload (recommended — metadata in app):**

1. Package workspace → zip ([packaging guide](./agent-packaging.md)); exclude `uandai-ai/` (platform skill)
2. `POST /v1/auth/token` → obtain access JWT
3. Collect **`agent_name`** and **`description`** from user (only required form fields besides the zip)
4. `POST /v1/agents/upload` with **`bundle`** + name + description (access JWT)
5. Optional gallery: `POST /agents/{id}/media` … (after upload — see [Gallery media](#gallery-media-screenshots--video)); submit via `PATCH` only (not on upload)
6. Complete price, model, provider URL (when required), invocation settings via **uandai.ai app** or `POST /agents/{id}/proposals` — **do not** ask for provider API keys (`{PROVIDER}_KEY`); subscribers supply those at subscribe/invoke
7. `PATCH /agents/{id}/proposals/{proposal_id}` with `status=submitted` when ready for review (Step 4 in create wizard, or manage **For Approval** tab)
8. After admin approval, subscribers can invoke
9. Optional: `DELETE /agents/{agent_id}` when the trainer wants to remove an agent they own (see [Delete agent](#delete-agent-trainer))

**Full ZIP upload (all metadata at POST):**

1. Same packaging and exchange as above
2. Collect name, description, price, model, provider URL test value (when required), and custom/skill test rows from user — **not** `{PROVIDER}_KEY`
3. `POST /v1/agents/upload` with `bundle` + full marketplace fields
4. After admin approval, subscribers can invoke

**OpenClaw import (`openclaw_root` / `files`) — server/advanced:**

Requires subscription price, model, and provider URL / custom test rows at POST (not `{PROVIDER}_KEY`). Trainers should use **ZIP** instead of multipart `files`.

### Typical subscriber workflow

1. `POST /v1/auth/token` → obtain access JWT
2. `GET /v1/me/subscriptions`
3. `GET /v1/me/activations?invokable_only=true`
4. `POST /v1/executions`
5. `GET /v1/executions/{run_id}` until terminal status

### Subscriber OpenClaw access

Subscribers with an active agent subscription use Hydra’s `/openclaw` reverse proxy (not `/api/v1/*` business routes).

See **[OpenClaw integration guide](./openclaw-integration.md)** for session keys, allowable HTTP/WebSocket endpoints, readiness, browser Control UI, and blocked surfaces.

---

## Endpoints

All business endpoints below require `Authorization: Bearer <access_token>` (from exchange or password login).

### Upload agent (create)

```http
POST /v1/agents/upload
Authorization: Bearer <access_token>
Content-Type: multipart/form-data
```

Legacy alias: `POST /agents/upload` (same multipart contract).

#### Upload modes

Exactly **one** mode per request: `bundle` (ZIP) **or** `openclaw_root` (server path) **or** repeated `files` (multipart OpenClaw tree).

| Mode | When to use | Required at POST |
|------|-------------|------------------|
| **ZIP** (`bundle`) | Packaged archive from [agent-packaging.md](./agent-packaging.md) — **trainer default** | **`bundle`**, **`agent_name`**, **`description`** (minimal); or full metadata (see below) |
| **OpenClaw import** (`openclaw_root` / `files`) | Server path or advanced multipart tree | Tree + full marketplace metadata (price, model, provider URL / custom test rows) |

---

#### Prerequisites — minimal ZIP upload (`bundle`)

**Default trainer path.** Collect only name, description, and the packaged zip before POST.

| Field | Required at POST | Notes |
|-------|------------------|-------|
| `bundle` | **Yes** | `.zip` from [agent-packaging.md](./agent-packaging.md), max 50MB |
| `agent_name` | **Yes** | Non-empty display name — **ask user** |
| `description` | **Yes** | Non-empty marketplace description — **ask user** |
| `subscription_price` | No | Defaults to lowest configured tier when omitted |
| `default_model_identifier` | No | Complete later; proposal starts as `pending` |
| `config_data_type_json` / `test_values_json` | No | Required before submit-for-approval (see below) |
| `photo_url`, invocation env fields | No | Optional; set via app or proposal update |

**Minimal ZIP pre-call checklist:**

- [ ] JWT exchanged (`access_token` in session — not raw `uand_live_…`)
- [ ] Zip packaged and validated per agent-packaging.md
- [ ] User provided `agent_name` and `description`
- [ ] Do **not** block upload waiting for price/model — user can finish in the uandai.ai app

**After minimal upload:** return `agent.id`, `revision_no`, and latest proposal `review_status` (`pending` when no model). Share manage link `{APP_SITE_URL}/training-center/agents/manage/{agent.id}` for price, duration, provider LLM, and model. User can also complete via proposal API before submitting for approval.

---

#### Prerequisites — full ZIP upload (`bundle`)

Use when the user already has price, model, provider URL (when required), and custom/skill test rows at upload time.

| Field | Required | Notes |
|-------|----------|-------|
| `bundle` | **Yes** | `.zip` file, max 50MB |
| `agent_name` | **Yes** | Non-empty display name |
| `description` | **Yes** | Non-empty marketplace description |
| `subscription_price` | **Yes** | Decimal string (`0`–`1000000`), must match a configured tier |
| `default_model_identifier` | **Yes** | OpenClaw model ref, e.g. `ollama/qwen3:8b` |
| `config_data_type_json` | **Yes** (with model) | JSON map of env key → data type; platform reconciles provider `{PROVIDER}_KEY` / `{PROVIDER}_URL` from the model (see below) |
| `test_values_json` | **Yes** (with model) | JSON **array** of `{ "key", "data_type", "value" }` trainer test rows for custom/skill vars and provider **URL** when required — **never** `{PROVIDER}_KEY`; attach `file_<KEY>` parts for file types |
| `required_env_vars` | When invokable | Comma-separated subscriber invocation keys (in addition to provider keys) |
| `config_skill_data_type_json` | When skill envs | JSON map for `required_skill_envs` |
| `skill_description_env_json` | When skill envs | JSON defaults for skill env keys |
| `is_invokable` | Optional | `true` / `false` — when `true`, also send duration tier + `prompt_template` and invocation env fields |
| `agent_duration_pricing_id` | When invokable (preferred) | Duration pricing tier id from `GET /agents/duration-pricing` |
| `invokable_duration_seconds` | When invokable (fallback) | Max run duration (seconds) — resolved to a tier when `agent_duration_pricing_id` is omitted |
| `prompt_template` | When invokable | Prompt template for pay-per-use runs |
| `photo_url` | Optional | Marketplace image URL |

---

#### Prerequisites — OpenClaw import (`openclaw_root` / `files`)

Server-side or advanced path. **Not** the trainer minimal flow — use ZIP instead.

| Field | Required at POST | Notes |
|-------|------------------|-------|
| `agent_name` | **Yes** | Non-empty display name |
| `description` | **Yes** | Non-empty marketplace description |
| `openclaw_root` **or** `files` | **Yes** (one mode) | Server path or multipart tree (`openclaw.json`, `workspace/…`) |
| `subscription_price` | **Yes** | Decimal string matching a configured tier |
| `default_model_identifier` | **Yes** | OpenClaw model ref |
| `config_data_type_json` / `test_values_json` | **Yes** (with model) | Provider URL (when required) and custom/skill trainer test rows — not `{PROVIDER}_KEY` |

---

#### Complete metadata later (minimal ZIP upload)

Owner-only. Same multipart fields as upload, but bundle/tree is optional on update.

```http
POST /agents/{agent_id}/proposals
Authorization: Bearer <access_token>
Content-Type: multipart/form-data
```

Send at least: `agent_name`, `description`, `subscription_price`, `default_model_identifier`, `config_data_type_json`, `test_values_json`, `revision_no` (from latest proposal). Include provider **URL** test rows when required (e.g. `OLLAMA_URL` for Ollama) and custom/skill test rows — **omit** `{PROVIDER}_KEY`.

Submit for admin review when complete:

```http
PATCH /agents/{agent_id}/proposals/{proposal_id}
Authorization: Bearer <access_token>
Content-Type: application/json

{ "revision_no": <current>, "status": "submitted" }
```

**Submit is rejected (`400`) until:** valid `subscription_price` tier, `default_model_identifier`, provider URL test value (when the catalog has no default base URL), custom/skill test rows as needed, and (if `is_invokable`) a duration tier (`agent_duration_pricing_id` or `invokable_duration_seconds`) + `prompt_template`. Sending `{PROVIDER}_KEY` in `test_values_json` is also rejected (`400`).

---

#### Duration pricing tiers (invokable agents)

List platform duration fee tiers (no auth required):

```http
GET /agents/duration-pricing
```

**Response `200`:**

```json
{
  "items": [
    { "id": 1, "min_seconds": 0, "max_seconds": 60, "fee_amount": "0.10", "currency": "USD" }
  ]
}
```

When `is_invokable=true` on upload or proposal, prefer **`agent_duration_pricing_id`** from this list. If omitted, the platform resolves a tier from **`invokable_duration_seconds`** (1–7200). An unknown `agent_duration_pricing_id` returns `400`.

---

#### Provider credentials (when `default_model_identifier` is set)

The platform reconciles provider storage keys from the model’s provider (same as the uandai.ai app trainer UI). `{PROVIDER}_KEY` is added to `config_data_type_json` / `required_env_vars` for **subscribers** — trainers must **not** send it in `test_values_json` (request rejected with `400`).

| Field | Trainer upload / proposal | Subscriber subscribe / invoke |
|-------|-------------------------|-----------------------------|
| `{PROVIDER}_KEY` in schema | Reconciled automatically | Required — subscriber supplies API key |
| `{PROVIDER}_KEY` in `test_values_json` | **Forbidden** | N/A |
| `{PROVIDER}_URL` in `test_values_json` | Required when catalog has no default `base_url` (e.g. Ollama) | Subscriber may override URL |
| Live HTTP probe | Skipped on trainer path | Runs when subscriber saves credentials |

For `ollama/qwen3:8b`, reconciled `config_data_type_json` includes both keys; trainer `test_values_json` includes **URL only**:

```json
{"OLLAMA_KEY":"string","OLLAMA_URL":"string"}
```

```json
[{"key":"OLLAMA_URL","data_type":"string","value":"http://127.0.0.1:11434"}]
```

Cloud providers with a catalog default base URL (e.g. OpenAI, DeepSeek) need no provider URL test row. Custom invocation and skill env test rows are unchanged.

Full ZIP form example: `postman/collections/Hydra MVP/API Upload Agent ZIP (JSON).request.yaml` (internal collection name)

OpenClaw import layout rules: same dress/skills/personality extraction as path/multipart modes (see API OpenAPI description). ZIP layout rules: [agent-packaging.md](./agent-packaging.md).

**Response `201`:** `{ "agent": { "id", "revision_no", "name", … } }`

**Response `400` (bundle layout):** structured `detail.code` — e.g. `openclaw_bundle_platform_skill` when `uandai-ai/` is present in the zip. See [packaging guide](./agent-packaging.md).

### Upload agent version (proposal)

```http
POST /agents/{agent_id}/proposals
Authorization: Bearer <access_token>
Content-Type: multipart/form-data
```

Owner only. Updates marketplace metadata and optionally replaces bundle/tree. Required for completing a minimal ZIP upload before submit.

### Submit proposal for approval

```http
PATCH /agents/{agent_id}/proposals/{proposal_id}
Authorization: Bearer <access_token>
Content-Type: application/json

{ "revision_no": 0, "status": "submitted" }
```

Withdraw submission: same endpoint with `"status": "pending"` (only when current status is `submitted`).

### List created agents (trainer)

Dashboard-style list of agents owned by the current trainer (metrics per agent).

```http
GET /agents/created
Authorization: Bearer <access_token>
```

**Response `200`:** `{ "agents": [ { "id", "name_agent", "revision_no", "subscription_price", "total_invocations", "success_rate", "can_delete", "delete_blockers", … } ] }`

Each agent includes **`can_delete`** (boolean) and **`delete_blockers`** — an array of `{ "code", "message", "destroys_at"?, "entitled_count"? }` for delete preflight (same shape as `GET /agents/{agent_id}/delete-eligibility`).

Use before delete or manage flows when the user knows the agent name but not the numeric `agent_id`.

### List agents (trainer)

Full trainer agent records (marketplace metadata, invocation settings, last run).

```http
GET /agents
Authorization: Bearer <access_token>
```

**Response `200`:** `{ "agents": [ … ] }` — richer than `/agents/created`; includes `revision_no`, `is_published`, `last_run`, provider/model fields.

### List agent proposals (trainer)

```http
GET /agents/{agent_id}/proposals?limit=20&sort=
Authorization: Bearer <access_token>
```

Owner only. Returns proposal history with `review_status` (`pending`, `submitted`, `approved`, `rejected`).

### Check delete eligibility (trainer)

Preflight whether `DELETE` will succeed — use before attempting delete.

```http
GET /agents/{agent_id}/delete-eligibility
Authorization: Bearer <access_token>
```

**Response `200`:**

```json
{
  "agent_id": 42,
  "can_delete": false,
  "blockers": [
    {
      "code": "agent_delete_entitled_subscribers",
      "message": "…",
      "destroys_at": "2026-07-01T00:00:00+00:00",
      "entitled_count": 2
    }
  ]
}
```

When `can_delete` is `false`, explain blockers to the user (include `destroys_at` for entitled subscribers) — do **not** call `DELETE` until resolved.

### Delete agent (trainer)

Permanently remove a trainer-owned agent when it has no active operational dependencies.

```http
DELETE /agents/{agent_id}
Authorization: Bearer <access_token>
```

Legacy path: `DELETE /api/agents/{agent_id}` (same contract).

#### Prerequisites — collect before DELETE

| Requirement | Notes |
|-------------|-------|
| Trainer role | Subscriber JWT returns `403` |
| Agent owner | Non-owner trainer returns `403` |
| `agent_id` | Confirm with user; optional `GET /agents/created` or `GET /agents/{agent_id}/delete-eligibility` first |

No request body. Rate limit: **5 requests/minute** per user. Prefer preflight (`delete-eligibility` or `can_delete` on `/agents/created`) before `DELETE`.

#### Allowed when

All of the following are true:

- No **entitled** subscribers (`destroys_at` still in the future blocks delete; after the grace window expires, delete is allowed)
- No **active deployment** to a user pod (`undeployed_at` is null)
- No **pending subscription checkout** for the agent
- No **in-flight runs** with status `queued`, `dispatching`, or `running`
- No runs in **`pending_payment`**
- No **worker lease** executing a run for the agent

#### Response

**`200 OK`:**

```json
{ "agent_id": 42, "deleted": true }
```

**`404`:** agent not found  
**`403`:** not trainer (`detail`), or not agent owner (`agent_delete_forbidden`)  
**`409`:** delete blocked — structured `code` in body (see `message`):

| Code | Meaning |
|------|---------|
| `agent_delete_entitled_subscribers` | Active subscribers within grace (`destroys_at` in params) |
| `agent_delete_active_deployment` | Agent deployed to a user pod |
| `agent_delete_pending_subscription_checkout` | In-flight subscription checkout for this agent |
| `agent_delete_run_in_progress` | Run `queued`, `dispatching`, `running`, or `pending_payment` |
| `agent_delete_worker_executing` | Worker lease active for this agent |

#### What delete does

- **Removes:** the `agents` row, proposals, trainer-owned invocation defaults, and on-disk bundle/extract artifacts (best effort)
- **Retains (historical):** terminal `agent_runs`, usage/payment rows, subscriber `agent_invocation_defaults`, `user_agents`, `agent_subscriptions`, `subscription_request_lines`, and `agent_deployments` — `agent_id` is nulled and `agent_name` is snapshotted where needed
- **Subscribers:** past activations remain visible with `agent_removed: true`; invoke and OpenClaw readiness for the deleted agent stop working

Re-uploading after delete creates a **new** `agent_id` (ids are not reused).

### Gallery media (screenshots + video)

Gallery assets are **separate REST** — not bundled in proposal multipart. Icon/banner is optional external **`photo_url` (HTTPS)** on upload/proposal; **never** derived from `media[0]`.

| Limit | Value |
|-------|-------|
| Screenshots | Max **10** (png/jpg/webp, ≤5 MB each) |
| Preview video | Max **1** (mp4/webm/mov, ≤50 MB, ≤**30s**) |
| Required at publish (v1) | **Optional** |
| Captions (trainer UI v1) | **None** — API `caption` field exists for v2/programmatic use |

**Create flow (app parity):** Step 3 `POST /agents/upload` only (proposal stays `pending`) → Step 4 optional gallery CRUD → `PATCH` submit. Refresh mid–Step 4: continue on manage **For Approval** tab (`?tab=approval`).

#### Owner CRUD (editable proposal / `scope=draft` only)

```http
POST   /agents/{agent_id}/media
POST   /agents/{agent_id}/media/upload-session
POST   /agents/{agent_id}/media/{media_id}/complete
GET    /agents/{agent_id}/media
PATCH  /agents/{agent_id}/media/{media_id}
PUT    /agents/{agent_id}/media/reorder
DELETE /agents/{agent_id}/media/{media_id}
Authorization: Bearer <access_token>
```

##### Proxy upload (multipart — default for automation)

- `POST /agents/{agent_id}/media` — multipart field `file` (screenshot or video). Returns updated proposal draft list (`media[]` with `trainer_proposal` URLs).
- **OpenClaw / API-key automation:** use this path. Works when `HYDRA_AGENT_MEDIA_DIRECT_UPLOAD` is off or on (app falls back here on `404`).

##### Direct upload (browser → S3/MinIO)

When `HYDRA_AGENT_MEDIA_DIRECT_UPLOAD=true` **and** `HYDRA_STORAGE_AGENT_MEDIA_MODE=object`, the trainer web app uploads large blobs without proxying through the API. **Programmatic clients may use the same flow** if they can `PUT` to the presigned URL (bucket CORS required for browsers).

| Step | Method | Path / target |
|------|--------|----------------|
| 0 | `GET` | `/agents/{agent_id}/media` — read `direct_upload_enabled` |
| 1 | `POST` | `/agents/{agent_id}/media/upload-session` — JSON `{ "filename", "content_type", "content_length", "caption"? }` |
| 2 | `PUT` | Presigned `upload_url` from step 1 (not Hydra; send `required_headers` as-is) |
| 3 | `POST` | `/agents/{agent_id}/media/{media_id}/complete` — JSON `{ "caption"? }` |

**Session response:** `{ "media_id", "upload_method": "PUT", "upload_url", "required_headers", "expires_at" }` (Unix seconds; max TTL 900s).

**Complete** validates the object (`HEAD`), enforces size/type/duration (video), inserts the draft `agent_media` row, and deletes the upload session. Same limits as proxy upload apply.

**Flag off or object mode unavailable:** `upload-session` / `complete` return `404` with `direct_upload_disabled` or `direct_upload_requires_object_storage`; use proxy `POST /media`.

**Ops:** prod needs S3 CORS on the gallery bucket before enabling the flag — see `hydra_mvp/k8s/docs/agent-media-direct-upload-rollout.md` and `hydra_mvp/docs/api-testing.md` § Direct gallery upload.

##### Other owner routes

- `GET /agents/{agent_id}/media` — draft list; includes `direct_upload_enabled: bool`.
- `PUT …/reorder` — body `{ "media_ids": ["uuid-3", "uuid-1", …] }` (every id must belong to current editable proposal).
- `409` when proposal is already `submitted` (gallery edits blocked until reject or new proposal fork).

#### Serve routes (per audience — no merged owner resolver)

| Route | Auth | Scope |
|-------|------|-------|
| `GET /listings/{agent_id}/media/{media_id}` | None | **Published live** only |
| `GET /agents/{agent_id}/media/{media_id}` | Owner JWT | **Live published** only |
| `GET /agents/{agent_id}/proposals/{proposal_id}/media/{media_id}` | Owner JWT | **Proposal draft** row |

JSON `media[].url` is a display URL only — **`storage_ref_json` never appears in JSON**.

#### Listing detail shape

`GET /listings/{agent_id}` includes `media[]` and explicit top-level `preview_video` when a video exists:

```json
"preview_video": {
  "media_id": "…",
  "url": "https://api.example.com/api/v1/listings/42/media/…",
  "duration_sec": 28
}
```

`null` when no video in the published set.

#### Approve semantics

On admin approve: **copy/replace** — new `scope=published` rows with **new** `media_id`s; **reuse** `storage_ref_json` verbatim (pointer copy); delete superseded published blobs only when refcount → 0. Draft proposal rows remain for admin diff.

#### Postman

Folders: `postman/collections/Hydra MVP/agent-media/` (`01` proxy upload; `01c`–`01e` direct session → PUT → complete) and `listings-public/` (see `hydra_mvp/docs/api-testing.md`).

### List subscriptions

```http
GET /v1/me/subscriptions?agent_id={id}&limit=20
Authorization: Bearer <access_token>
```

Optional query: `agent_id` (filter), `limit` (max 100).

**Renew toggle** (subscriber): `PATCH /v1/me/subscriptions/{subscription_id}` with JSON `{ "is_renew_enabled": true|false }`.

Subscription checkout (`POST /v1/me/subscription-requests`) and Stripe flows remain **browser/app only** — not API-key automation.

### List subscription request lines (subscriber)

Read-only observability for checkout/refill state (does not create subscriptions).

```http
GET /v1/me/subscription-line-requests?status=pending&agent_id={id}&limit=20
Authorization: Bearer <access_token>
```

| Query | Notes |
|-------|-------|
| `status` | Optional: `pending`, `completed`, `aborted` |
| `agent_id` | Optional filter |
| `limit` | Max 100 |

**Response `200`:** `{ "items": [ { "agent_id", "type", "status" } ] }`

### List activations (subscriber)

```http
GET /v1/me/activations?invokable_only=false
Authorization: Bearer <access_token>
```

| Query | Default | Notes |
|-------|---------|-------|
| `invokable_only` | `false` | When `true`, only agents the subscriber can invoke right now |

Each item includes:

| Field | Notes |
|-------|-------|
| `user_agent_id` | Stable activation row id — use for history after trainer delete |
| `id` | Live marketplace `agent_id`; **`null` when archived** |
| `agent_removed` | `true` when the trainer deleted the agent |
| `is_invokable` | `false` when archived, expired, or not entitled |
| `revision_no` | Current revision when live; needed for invoke |

**Archived activations:** After trainer `DELETE /agents/{agent_id}`, past subscriptions stay listed with `agent_removed: true` and `is_invokable: false`. Invoke, config PATCH, and OpenClaw readiness for that agent stop working; run history remains queryable via executions.

### Activation detail (subscriber)

```http
GET /v1/me/activations/{id}
Authorization: Bearer <access_token>
```

`{id}` accepts **`user_agent_id`** or live **`agent_id`**. Archived rows return read-only detail (no live listing fields).

### Activation metrics (subscriber)

```http
GET /v1/me/activations/metrics
Authorization: Bearer <access_token>
```

Dashboard totals (`total_agents` counts live agents only; run totals include archived history).

### Activation configs (subscriber)

```http
GET /v1/me/activations/{id}/configs
Authorization: Bearer <access_token>
```

Returns config template items and saved values. **`410`** when the activation is archived (`agent_removed`). Path `{id}` accepts `user_agent_id` or live `agent_id` (live `agent_id` wins when both could match).

Save a config value:

```http
PATCH /v1/me/activations/{id}/configs/{config_id}
Authorization: Bearer <access_token>
Content-Type: application/json

{ "value": "…" }
```

Requires a live activation row (`404` when missing; `410` when archived).

**Config file policy** (limits for invoke file uploads): `GET /v1/me/activations/config-file-policy`

### Create execution (invoke)

```http
POST /v1/executions
Authorization: Bearer <access_token>
Content-Type: multipart/form-data
```

#### Prerequisites — collect before POST (OpenClaw)

**STOP** until you have every required field below. Do not invoke with guessed `configs` or stale revision numbers.

| Field | Source | If missing |
|-------|--------|------------|
| `agent_id` | `GET /v1/me/activations?invokable_only=true` **or** user-provided id confirmed against activations | List activations or ask user to choose |
| `revision_no` | Activation record for chosen agent | Re-fetch activations; do not guess |
| `configs` | **Ask user** — required keys per agent `required_env_vars` / prompt template | Do not invoke |
| `config_files` | User attachment when agent expects file inputs | Ask user for file + matching `config_file_keys` |

**Pre-call checklist:**

- [ ] JWT exchanged (`access_token` in session)
- [ ] Target agent appears in activations (or user explicitly confirmed id)
- [ ] `revision_no` matches current activation
- [ ] `configs` JSON collected from user for all required keys

| Field | Required | Notes |
|-------|----------|-------|
| `agent_id` | Yes | Target agent |
| `revision_no` | Yes | Must match current revision |
| `configs` | Yes | JSON string of runtime variables |
| `config_file_keys` | If files | Keys for uploaded files |
| `config_files` | Optional | File parts |

**Response `200`:** `{ "id": <run_id>, "status": "queued" | "pending_payment" }`

- `queued` — run enqueued normally
- `pending_payment` — credits insufficient; auto-refill may be in progress (poll until terminal or user tops up)

### Poll execution

```http
GET /v1/executions/{run_id}
Authorization: Bearer <access_token>
```

### List executions

```http
GET /v1/executions?agent_id={id}&user_agent_id={id}&limit=20
Authorization: Bearer <access_token>
```

| Query | Notes |
|-------|-------|
| `agent_id` | Filter by live marketplace agent id |
| `user_agent_id` | Filter by activation row — use for **archived** history after trainer delete |
| `limit` | Optional cap |

List items may include `agent_removed: true` and nullable `agent_id` when the trainer deleted the agent.

### Download artifact

```http
GET /v1/executions/{run_id}/artifacts/{file_name}
Authorization: Bearer <access_token>
```

### Current user

```http
GET /v1/auth/me
Authorization: Bearer <access_token>
```

---

## Example: exchange, upload, invoke

```bash
UANDAI_API_BASE_URL="${UANDAI_API_ORIGIN}/api"

# 1. Exchange (bootstrap)
RESP=$(curl -sS -X POST "$UANDAI_API_BASE_URL/v1/auth/token" \
  -H "Authorization: Bearer $UANDAI_API_KEY")
ACCESS=$(echo "$RESP" | jq -r .access_token)
REFRESH=$(echo "$RESP" | jq -r .refresh_token)

# 2a. Upload (trainer) — minimal ZIP (bundle + name + description only)
curl -sS -X POST "$UANDAI_API_BASE_URL/v1/agents/upload" \
  -H "Authorization: Bearer $ACCESS" \
  -F "bundle=@output/my-agent-workspace.zip" \
  -F "agent_name=My Agent" \
  -F "description=My agent marketplace description"
# Complete price/model later via POST /agents/{id}/proposals, then PATCH submit.

# 2b. Upload (trainer) — full ZIP example
curl -sS -X POST "$UANDAI_API_BASE_URL/v1/agents/upload" \
  -H "Authorization: Bearer $ACCESS" \
  -F "bundle=@output/my-agent-workspace.zip" \
  -F "agent_name=My Agent" \
  -F "description=My agent marketplace description" \
  -F "subscription_price=19.99" \
  -F "default_model_identifier=ollama/qwen3:8b" \
  -F 'config_data_type_json={"OLLAMA_KEY":"string","OLLAMA_URL":"string"}' \
  -F 'test_values_json=[{"key":"OLLAMA_URL","data_type":"string","value":"http://127.0.0.1:11434"}]'

# 3. List invocable (subscriber)
curl -sS "$UANDAI_API_BASE_URL/v1/me/activations?invokable_only=true" \
  -H "Authorization: Bearer $ACCESS"

# 4. Invoke (agent_id and revision_no are integers from activations)
curl -sS -X POST "$UANDAI_API_BASE_URL/v1/executions" \
  -H "Authorization: Bearer $ACCESS" \
  -F "agent_id=42" \
  -F "revision_no=1" \
  -F 'configs={"PROMPT":"hello"}'
# Response: {"id":123,"status":"queued"}

# 5. Delete agent (trainer) — only when no entitled subscribers, deployments, checkout, or in-flight runs
curl -sS -X DELETE "$UANDAI_API_BASE_URL/agents/42" \
  -H "Authorization: Bearer $ACCESS"

# 6. Refresh when access expires
NEW=$(curl -sS -X POST "$UANDAI_API_BASE_URL/v1/auth/refresh" \
  -H "Content-Type: application/json" \
  -d "{\"refresh_token\":\"$REFRESH\"}")
ACCESS=$(echo "$NEW" | jq -r .access_token)
REFRESH=$(echo "$NEW" | jq -r .refresh_token)
```

---

## Errors

| Code | Meaning |
|------|---------|
| `401` | Missing, invalid, or revoked token; raw API key on business route (exchange first) |
| `403` | Wrong owner or key used on management endpoint |
| `402` | Insufficient credits |
| `404` | Agent, run, activation, or key not found |
| `410` | Activation archived (`agent_removed`) — configs read/PATCH not available |
| `409` | Revision mismatch; or delete blocked — structured `code` (see [Delete agent](#delete-agent-trainer)) |
| `422` | Validation error (see response body) |
| `429` | Rate limit |

---

## Out of scope for API keys

- Stripe checkout, credit top-up, subscription purchase
- Creating or listing API keys via API key auth
- Sending raw `uand_live_…` on business routes (exchange → JWT first)

**OpenClaw gateway (`/openclaw`):** see [OpenClaw integration guide](./openclaw-integration.md).

---

## OpenClaw

Install the full skill folder (`SKILL.md` + `references/`) from `docs/openclaw-skills/uandai-ai/` or ClawHub (`openclaw skills install uandai-ai --global`). See `GET /docs/openclaw-skills`.

- **`uandai-ai`** — configure access, package zip, exchange, upload, delete agent, subscriptions, invoke

When packaging for upload, **exclude `uandai-ai/`** from the zip (trainer-only platform skill). See [packaging guide](./agent-packaging.md) or bundled `references/agent-packaging.md` in the installed skill.

Read bundled `references/programmatic-api.md`, `references/agent-packaging.md`, and (for subscribers) `references/openclaw-integration.md` in the skill directory before acting. Live `{API_ORIGIN}/docs/*` URLs are for humans only unless the user pastes them in chat.
