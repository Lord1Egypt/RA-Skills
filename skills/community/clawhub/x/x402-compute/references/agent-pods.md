# Agent Pods — deploy & drive an always-on hosted agent

An **Agent Pod** ("ClawPod", built on **OpenClaw**) is a persistent AI agent that runs 24/7 on
a dedicated CPU machine. It chats on **Telegram & Discord** (Slack / WhatsApp / Signal coming
soon) and from the dashboard, has its own **crypto wallet** (Coinbase CDP — EVM + Solana, keys in
a TEE), **persistent memory**, and ships with the `x402-compute` + `x402-layer` skills preinstalled
(wired to your account with capped, revocable credentials) so it can buy confidential compute and
pay x402 endpoints itself. Owner/platform customization is supported through structured fields:
identity, instructions, and the quiet self-check heartbeat prompt.

A pod **is a compute order** — the `pod.id` returned by deploy is the compute order id. Lifecycle
(extend / destroy) reuses the Machines endpoints with that id as the instance id.

- **API base:** `https://compute.x402layer.cc`
- **Three engines are deployable:** `agent_id: "openclaw"` (ClawPod, the default), `"hermes"`
  (HermPod, a self-improving agent that writes its own skills) and `"pi"` (Pi pod, a lightweight
  coding agent you extend with skills and MCP tools). On the `/pods/v1` API the same engines are
  named `clawpod`, `hermpod` and `pipod`. Always check `available` in `GET /pods/catalog`.

## Auth model (important)

Pod endpoints split into two auth surfaces:

| Surface | Endpoints | Auth |
|---------|-----------|------|
| **Owner** (manage the pod) | `POST /pods`, `GET/PATCH /pods/{id}`, `POST /pods/{id}/actions`, `GET/POST/DELETE /pods/{id}/api-keys*`, wallet, credentials | **Compute auth** — `X-API-Key: x402c_…`, a signed compute session, or an `X-Auth-*` wallet signature. Required even when paying with x402, because a pod is owned by your wallet. |
| **Adapter** (talk to the agent) | `GET /pods/{id}/v1/models`, `POST /pods/{id}/v1/chat/completions` | **`Authorization: Bearer sk-sglpod-int-…`** — a pod-scoped integration key you mint via `POST /pods/{id}/api-keys`. NOT compute auth. |

The catalog (`GET /pods/catalog`) is public (no auth).

## 1. Catalog (public)

```bash
curl -s https://compute.x402layer.cc/pods/catalog
```
Returns deployable agents, managed **tiers** (with each tier's model menu + RAM floor), supported
**channels**, memory backends, and pricing. Read it first to pick a `tier`/`plan`/`model`.

## 2. Deploy — `POST /pods` (owner / compute auth)

Two AI modes:

- **`managed`** — we run the LLM and meter it from your platform **credits**. Pick a `tier`:
  - `starter` — text chat.
  - `pro` — adds vision + computer-use (runs a browser on the box → higher RAM floor).
  - `max` — top reasoning + vision.
  Each tier bundles a machine RAM floor + a curated model menu the agent can switch among at
  runtime (`/model`). Managed pods include a small prepaid inference allowance.
- **`byok`** — bring your own OpenAI-compatible key + any machine `plan`. You pay CPU + a small
  service % only; your AI runs on your key.

**Pay:** platform **credits** (`use_credits: true`) or **x402** (omit `use_credits` → the deploy
answers `402 Payment Required`; settle with the `X-Payment` header like any provision, and add
`"network"` for a non-Base chain).

### Deploy body fields
| Field | Mode | Notes |
|-------|------|-------|
| `agent_id` | both | `"openclaw"` (ClawPod, default), `"hermes"` (HermPod) or `"pi"` (Pi pod). See `available` in the catalog. |
| `ai_mode` | both | `"managed"` \| `"byok"`. |
| `tier` | managed | `"starter"` \| `"pro"` \| `"max"`. |
| `plan` | both | Machine plan id (from `GET /compute/plans`). Add optional `plan_ram_mb` for a pre-flight RAM check; managed tiers enforce a RAM floor. |
| `prepaid_hours` | both | e.g. `720` = 1 month (min 24). |
| `model` | both | managed: an override that must be in the chosen tier's model list (else falls back to the tier default); byok: your model id. |
| `llm_base_url`, `llm_api_key`, `llm_api` | byok | `llm_api` ∈ `openai-completions` (default) \| `openai-responses` \| `anthropic-messages` \| `google-generative`. |
| `llm_preset` | byok | Optional: `openrouter`, `openai`, `venice`, `0g` or `custom`. A preset fixes the base URL, so you only send the key and model. |
| `llm_name` | byok | Optional display name for the primary provider (max 60 chars). |
| `llm_fallbacks` | byok (ClawPod) | Up to 3 ordered fallback providers, each `{preset, api_key, model, name?, base_url?, api?}`, plus at most one `{preset: "singularity", model}` entry for a Singularity Layer model. |
| `managed_models` | byok (ClawPod) | Default on for a BYOK ClawPod. Lets the pod also use Singularity Layer models, billed per call from your credits (no included allowance). Pick one with `/model singularity/<id>`; the list is `byok_managed_models.models` in the catalog. |
| `channels` | both | `{ telegram?: token, discord?: token }` — validated against the agent's supported channels; unsupported channels are rejected. |
| `memory` | byok | `{ backend: "raw"\|"mem0", api_key?, lcm? }` (managed memory is tier-driven; feature-gated). |
| `template`, `template_config` | both | Curated template — what the pod is FOR. See **Templates** below. |
| `agent_identity` | both | Owner/platform identity text, max 8000 chars. Rendered into the managed `AGENTS.md` customization section and `/opt/pod/workspace/IDENTITY.md`. |
| `agent_instructions` | both | Owner/platform instructions, max 8000 chars. Rendered into the managed `AGENTS.md` customization section. |
| `heartbeat_prompt` | both | Custom prompt for the agent's quiet self-check heartbeat, max 4000 chars. |
| `agent_heartbeat_minutes` | both | Self-check cadence: `0` disables; otherwise 15-1440 minutes. |
| `use_credits`, `network`, `ssh_public_key`, `region`, `os_id` | both | Passed straight through to the audited provision path. |

`AGENTS.md` is platform-managed and is not raw-editable through the API. This is intentional:
wallet survival, x402 spend boundaries, security rules, and tool permissions stay intact while
your owner/customer text is layered into a bounded customization section. Send an empty string
or `null` to `PATCH /pods/{id}/settings` to clear one of the custom text fields.

### Templates — curated pods with a job

A template layers a purpose on top of the engine: it supplies the persona, the channel
policy and the briefing schedule. Everything else (tiers, BYOK, wallet, self-extend,
skills) works exactly as on a bare pod. `GET /pods/catalog` returns `templates[]` with the
setup keys each one needs, and `templates_enabled` saying whether deploy will accept one.

| Template | Name | What it is |
|----------|------|------------|
| `community-manager` | **TGPod** | Runs a Telegram community: answers members, removes scam links and impersonators, and sends the owner a private briefing on a schedule. |
| `discord-community` | **DiscordPod** | Announced, not yet buildable — deploy refuses it. |

`community-manager` setup keys (`template_config`): `group_id` (required; comma-separate
several, up to the tier's `max_groups` — 1 Starter / 3 Pro / 10 Max, BYOK gets the top of
that ladder), `owner_id` (required — the Telegram user id the briefings go to),
`project_summary`, `agent_name`, `house_rules`, `tone`, `digest_minutes`. The template
requires its channel: deploy a `community-manager` **with** `channels.telegram` or it is
rejected before anything is charged.

The bot token belongs to the pod's moderation process, which must be Telegram's single
`getUpdates` consumer for that bot. Do not point another program at the same token.

```bash
# TGPod: a Pro community manager for one Telegram group
python scripts/agent_pod.py deploy --ai-mode managed --tier pro --plan <plan_id> \
  --use-credits --telegram "$BOT_TOKEN" \
  --template community-manager \
  --template-config group_id=-1001234567890 \
  --template-config owner_id=987654321 \
  --template-config project_summary="Singularity Layer — decentralised confidential compute"
```

Pods report their template back on `list` / `get` / deploy as `template`, so an agent
running a fleet can tell a community manager from a bare pod.

```bash
# Managed Pro pod, paid from credits, with a Telegram bot
curl -s -X POST https://compute.x402layer.cc/pods \
  -H "X-API-Key: $COMPUTE_API_KEY" -H "Content-Type: application/json" \
  -d '{
    "agent_id": "openclaw",
    "ai_mode": "managed",
    "tier": "pro",
    "plan": "<plan_id>",
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

**Deploy response** includes a `pod` object:
```json
{
  "pod": {
    "id": "<order_id>",              // == compute order id; use for ALL pod + lifecycle calls
    "agent_id": "openclaw",
    "display_name": "ClawPod",
    "ai_mode": "managed",
    "tier": "pro",
    "model": "<model>",
    "channels": ["telegram"],
    "managed_ai_key": "sk-sglpod-…",  // managed only, shown ONCE (pod's key to our LLM proxy)
    "managed_ai_key_note": "Shown once — this is the pod's key for our managed LLM proxy."
  }
}
```
The `managed_ai_key` is the pod's own internal key to our managed LLM proxy (not the integration
key you call the adapter with). It is shown once.

### Free 24-hour trial — `POST /pods/trial`
A free Starter/Pro pod with **no upfront payment** (funded by a one-time credit grant; gated behind
a live campaign, so it can answer `503` when off or fully claimed). One per wallet + device.
Auto-destroyed at 24h (never renews); managed-AI allowance capped.
```bash
curl -s -X POST https://compute.x402layer.cc/pods/trial \
  -H "X-API-Key: $COMPUTE_API_KEY" -H "Content-Type: application/json" \
  -d '{ "agent_id": "openclaw", "tier": "starter", "plan": "<plan_id>",
        "device_hash": "<sha256 hex device fingerprint>",
        "channels": { "telegram": "<bot_token>" } }'
```
`tier` must be `starter` or `pro`; `device_hash` is a 64-char sha256 hex. `ai_mode` (managed),
`prepaid_hours` (24) and `use_credits` are forced server-side.

## 3. Manage a pod (owner / compute auth)

```bash
curl -s https://compute.x402layer.cc/pods       -H "X-API-Key: $COMPUTE_API_KEY"   # list yours
curl -s https://compute.x402layer.cc/pods/<id>  -H "X-API-Key: $COMPUTE_API_KEY"   # details + heartbeat + masked creds

# Lifecycle action: restart | redeploy | stop | update | diagnose | logs | pair-approve | cron
curl -s -X POST https://compute.x402layer.cc/pods/<id>/actions \
  -H "X-API-Key: $COMPUTE_API_KEY" -H "Content-Type: application/json" -d '{"action":"restart"}'

# Approve a chat pairing code the bot showed in Telegram/Discord
curl -s -X POST https://compute.x402layer.cc/pods/<id>/actions \
  -H "X-API-Key: $COMPUTE_API_KEY" -H "Content-Type: application/json" \
  -d '{"action":"pair-approve","channel":"telegram","code":"T64WUC8Q"}'

# Add/replace channels later (queues a redeploy)
curl -s -X PATCH https://compute.x402layer.cc/pods/<id>/channels \
  -H "X-API-Key: $COMPUTE_API_KEY" -H "Content-Type: application/json" \
  -d '{"channels":{"discord":"<bot_token>"}}'

# Tune knobs: agent self-check heartbeat, customization, managed model, auto-renew
curl -s -X PATCH https://compute.x402layer.cc/pods/<id>/settings \
  -H "X-API-Key: $COMPUTE_API_KEY" -H "Content-Type: application/json" \
  -d '{"agent_heartbeat_minutes":30,
       "agent_identity":"You are Atlas, Acme Cloud support.",
       "agent_instructions":"Use Acme terminology and escalate billing questions.",
       "heartbeat_prompt":"Review open escalations and renew yourself if needed. Stay silent if clear."}'
```
Actions apply on the pod worker's next poll (≤ 60s). The `cron` action drives the agent's scheduler:
`{"action":"cron","verb":"add|enable|disable|remove|run", ...}` (add takes `kind`/`schedule`/`name`/`message`).

`GET /pods` and `GET /pods/{id}` return:

```json
{
  "customization": {
    "agent_identity": "You are Atlas, Acme Cloud support.",
    "agent_instructions": "Use Acme terminology and escalate billing questions.",
    "heartbeat_prompt": "Review open escalations and renew yourself if needed. Stay silent if clear."
  },
  "agent_heartbeat_minutes": 30
}
```

### Agent wallet & delegated skill access
```bash
curl -s https://compute.x402layer.cc/pods/<id>/wallet -H "X-API-Key: $COMPUTE_API_KEY"   # addresses + balances

# Owner controls: per-tx spend cap + arm sending (default OFF; clamped to a platform ceiling)
curl -s -X PATCH https://compute.x402layer.cc/pods/<id>/wallet/settings \
  -H "X-API-Key: $COMPUTE_API_KEY" -H "Content-Type: application/json" \
  -d '{"send_enabled":true,"spend_cap_usd":10}'
```
`GET /pods/<id>` returns a masked `credentials` block (the preinstalled skills' pod-scoped Compute
key + Studio PAT and its daily cap). Manage with `POST /pods/<id>/credentials`
(`{"action":"enable"|"regenerate"|"set-cap"|"byok", ...}`) or `DELETE /pods/<id>/credentials` to
revoke. Delegated creds, native Singularity MCP, wallet sending, and memory are feature-gated and
may be dark until launch.

### Extend / destroy (Machines endpoints, pod id as instance id)
```bash
curl -s -X POST https://compute.x402layer.cc/compute/instances/<pod.id>/extend \
  -H "X-API-Key: $COMPUTE_API_KEY" -H "Content-Type: application/json" -d '{"extend_hours":720,"use_credits":true}'
curl -s -X DELETE https://compute.x402layer.cc/compute/instances/<pod.id> -H "X-API-Key: $COMPUTE_API_KEY"
```
Managed pods can auto-renew from credits at expiry (grace window) when enabled; trials never renew.
The agent wallet's funds survive destruction (withdraw from the Wallet tab).

## 4. OpenAI-compatible adapter — call your pod like any OpenAI endpoint

The adapter turns `POST /pods/{id}/v1/chat/completions` into **one agent turn** on your pod, run
through the same Worker → PodChannel → outbound-tunnel path as dashboard/Telegram chat (so wallet
policy, autonomy mode, credits, lifecycle + audit all stay enforced). The VM is never exposed.

**v1 is intentionally minimal: Chat Completions only, non-streaming, no fake token usage.**

- **Model:** always `agent-pod` (the pod picks its own configured LLM internally).
- **Streaming:** NOT supported — you must send `"stream": false` (or omit it). `stream:true` → 400.
- **`usage`** is `null` in v1 (token counts are not faked).
- **Feature flag:** the whole adapter surface is dark by default (server flag
  `POD_OPENAI_ADAPTER_ENABLED`). When off, key management + adapter routes return `404`.

### 4a. Create an integration key — `POST /pods/{id}/api-keys` (owner / compute auth)
```bash
curl -s -X POST https://compute.x402layer.cc/pods/<id>/api-keys \
  -H "X-API-Key: $COMPUTE_API_KEY" -H "Content-Type: application/json" \
  -d '{"name":"my-integration"}'
# → { "key": "sk-sglpod-int-…", "base_url": "https://compute.x402layer.cc/pods/<id>/v1", "row": {…} }
```
- The **raw key (`sk-sglpod-int-…`) is returned ONCE** — store it. Only its SHA-256 hash is kept.
- The key is **bound to this pod**; using it against a different pod fails as `invalid_key`.
- Each key has a **daily request cap** (default 1000/day, rolling 24h window); over-cap → `429`.
- List: `GET /pods/{id}/api-keys` (masked). Revoke: `DELETE /pods/{id}/api-keys/{keyId}`.

### 4b. Call the adapter — `Authorization: Bearer sk-sglpod-int-…`
```bash
# List the (single) model the adapter exposes
curl -s https://compute.x402layer.cc/pods/<id>/v1/models \
  -H "Authorization: Bearer sk-sglpod-int-…"

# One agent turn (non-streaming)
curl -s -X POST https://compute.x402layer.cc/pods/<id>/v1/chat/completions \
  -H "Authorization: Bearer sk-sglpod-int-…" -H "Content-Type: application/json" \
  -d '{"model":"agent-pod","stream":false,
       "messages":[{"role":"user","content":"What is on my calendar today?"}]}'
```
Response is a standard `chat.completion` object with `choices[0].message.content` and `usage:null`.

Point any **OpenAI SDK** at the pod:
```python
import os
from openai import OpenAI
client = OpenAI(
    base_url="https://compute.x402layer.cc/pods/<id>/v1",
    api_key=os.environ["POD_INTEGRATION_KEY"],  # your sk-sglpod-int-* key
)
resp = client.chat.completions.create(
    model="agent-pod",
    messages=[{"role": "user", "content": "Summarize my unread DMs"}],
    stream=False,
)
print(resp.choices[0].message.content)
```

### Adapter error shapes (OpenAI-style `{ "error": {…} }`)
| Status | code | Meaning |
|--------|------|---------|
| `401` | `missing_key` / `invalid_key` | No bearer key, or key not valid for this pod. |
| `404` | `pod_unavailable` | Adapter disabled, or the pod is destroyed. |
| `403` | `pod_expired` | The pod's prepaid time ran out. |
| `429` | `daily_cap` | The key's daily request cap is exhausted. |
| `400` | `stream_unsupported` | You sent `stream:true`. |
| `503` | `pod_offline` | Agent offline — retryable, not charged. |
| `504` | `timeout` | Agent took too long — retryable. |

## Helper script
`scripts/agent_pod.py` wraps all of the above (owner calls use the shared compute-auth loader;
adapter calls use the integration key). See the Intent Router in `SKILL.md`.
```bash
python scripts/agent_pod.py catalog
python scripts/agent_pod.py deploy --ai-mode managed --tier pro --plan <plan_id> --prepaid-hours 720 \
    --telegram <bot_token> --use-credits
python scripts/agent_pod.py create-key <pod_id> --name my-integration      # → sk-sglpod-int-…
python scripts/agent_pod.py chat <pod_id> "What's on my calendar?" --key sk-sglpod-int-…
```
Credentials are read only from explicit env vars (`COMPUTE_API_KEY` or wallet keys for owner calls;
`POD_INTEGRATION_KEY` or `--key` for the adapter). No `.env` auto-loading.
</content>
</invoke>
