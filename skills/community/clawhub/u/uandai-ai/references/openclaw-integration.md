# Uandai OpenClaw Integration Guide

**Docs-Version:** 2026.06.19 (spec v1.1)  
**Related:** [Programmatic API guide](./programmatic-api.md) — Hydra `/api/v1/*` auth, subscriptions, and executions.

---

## Overview

Subscribers with an **active agent subscription** reach the trainer’s OpenClaw gateway through Hydra’s reverse proxy at `{APP_SITE_URL}/openclaw`. Use **JWT from API key exchange** — raw `uand_live_…` keys are rejected on `/openclaw`.

| Surface | Base URL |
|---------|----------|
| Hydra API (exchange, readiness) | `{API_ORIGIN}/api` |
| OpenClaw gateway (proxied) | `{APP_SITE_URL}/openclaw` |

**Session key (subscriber main chat):** `agent:hydra-subscribed-agent-{agent_id}:main`

Copy chat URL, gateway base, and session key from **uandai.ai → Workspace → agent → Integration**, or build them from the table above.

---

## Prerequisites

1. Create an API key in **uandai.ai app → Settings → API Keys** (shown once).
2. Exchange for JWT:

```http
POST {API_ORIGIN}/api/v1/auth/token
Content-Type: application/json

{ "api_key": "uand_live_…" }
```

3. Poll readiness until `status=ready`:

```http
GET {API_ORIGIN}/api/v1/me/openclaw/readiness?agent_id={agent_id}
Authorization: Bearer {access_token}
```

4. Call `/openclaw` with `Authorization: Bearer {access_token}` (refresh with `POST /api/v1/auth/refresh` before ~15 min expiry).

**Entitlement:** active subscription for `{agent_id}` and a ready user pod. Hydra returns `403` when not entitled or when a path/method is blocked for subscribers.

**Trainer delete:** when the trainer deletes an agent, readiness returns non-ready / entitlement fails and archived activations show `agent_removed: true` in `GET /v1/me/activations` — see [programmatic API — activations](./programmatic-api.md#list-activations-subscriber).

---

## HTTP API (allowed)

All paths below are relative to `{APP_SITE_URL}/openclaw/`. Use the subscriber session key in query, body, or `x-openclaw-session-key` header as required by OpenClaw.

| Method | Path | Purpose |
|--------|------|---------|
| `GET` | `v1/models` | List models |
| `GET` | `v1/models/{model_id}` | Model metadata |
| `POST` | `v1/chat/completions` | OpenAI-compatible chat (set `?session=` or header for multi-turn) |
| `POST` | `v1/embeddings` | Embeddings |
| `GET` | `sessions/{sessionKey}/history` | Transcript history (`sessionKey` URL-encoded) |
| `GET` | `api/chat/media/outgoing/{sessionKey}/…` | Outgoing chat media |
| `GET` | `chat` (+ static Control UI assets) | Browser chat (`?session=…`) |

### Chat completions example

```http
POST {APP_SITE_URL}/openclaw/v1/chat/completions?session=agent:hydra-subscribed-agent-{agent_id}:main
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "model": "openclaw/hydra-subscribed-agent-{agent_id}",
  "messages": [{ "role": "user", "content": "Hello" }],
  "stream": false
}
```

**Multi-turn:** reuse the same `session` query param or send `x-openclaw-session-key: agent:hydra-subscribed-agent-{agent_id}:main` on subsequent `POST v1/chat/completions` calls.

### Session history example

```http
GET {APP_SITE_URL}/openclaw/sessions/{url_encoded_session_key}/history?limit=20
Authorization: Bearer {access_token}
```

---

## WebSocket API (allowed RPC methods)

Connect to `wss://{APP_HOST}/openclaw/` with the same Bearer JWT (browser Control UI and programmatic clients).

Hydra enforces a **default-deny allowlist** on gateway RPC methods. Allowed groups:

| Group | Methods |
|-------|---------|
| Connect | `connect`, `poll`, `health`, `status`, `gateway.identity.get`, `plugins.uiDescriptors`, `commands.list` |
| Chat / agent runs | `chat.send`, `chat.history`, `chat.abort`, `agent`, `agent.wait`, `agent.identity.get`, `assistant.media.get` |
| Sessions | `sessions.list`, `sessions.preview`, `sessions.describe`, `sessions.resolve`, `sessions.get`, `sessions.create`, `sessions.send`, `sessions.abort`, `sessions.steer`, `sessions.patch`, `sessions.subscribe`, `sessions.unsubscribe`, `sessions.messages.subscribe`, `sessions.messages.unsubscribe`, `sessions.compaction.list`, `sessions.compaction.get`, `sessions.compaction.branch` |
| Artifacts | `artifacts.list`, `artifacts.get`, `artifacts.download` |
| Models / tools (read) | `models.list`, `models.authStatus`, `tools.catalog`, `tools.effective` |
| Tasks | `tasks.list`, `tasks.get`, `tasks.cancel` |
| Agents (metadata) | `agents.list` |
| Config (limited UI) | `config.get`, `config.schema.lookup`, `config.patch` |
| Talk / TTS | `talk.catalog`, `talk.config`, `talk.client.create`, `talk.client.toolCall`, `talk.session.*`, `talk.speak`, `talk.mode`, `tts.status`, `tts.providers`, `tts.personas`, `tts.enable`, `tts.disable`, `tts.convert`, `tts.setProvider`, `tts.setPersona` |

Blocked examples (return Hydra `INVALID_REQUEST` or HTTP `403`): `tools.invoke`, `agents.files.*`, `skills.*`, `config.set`, admin/channel hooks.

---

## Browser Control UI

| URL | Notes |
|-----|-------|
| `{APP_SITE_URL}/openclaw/chat?session=agent:hydra-subscribed-agent-{id}:main` | Chat while signed in (cookie JWT) or with Bearer |
| `{APP_SITE_URL}/openclaw/ai-agents` | Limited settings (provider/model); other agent admin routes hidden |

---

## HTTP paths blocked for subscribers

| Path / pattern | Reason |
|----------------|--------|
| `POST tools/invoke` | Arbitrary tool execution |
| `hooks/*` | Operator hooks |
| `api/v1/admin/*` | Admin RPC |
| `api/channels/*` | Channel management |
| `POST sessions/{sessionKey}/kill` | Session kill |

---

## Errors

| Code | Meaning on `/openclaw` |
|------|-------------------------|
| `401` | Missing/invalid JWT; raw API key |
| `403` | Not subscribed, not ready, agent removed by trainer, or path/method blocked for subscribers |
| `404` | Session or resource not found |

---

## Related Hydra API (not `/openclaw`)

Classic subscriber **invoke** flow (executions without OpenClaw gateway) remains on `/api/v1/*` — see [programmatic-api.md](./programmatic-api.md) § Typical subscriber workflow.

---

## Proof / examples

Hydra MVP Postman collection: `openclaw-gateway/` (token exchange → readiness → models → chat → history; `08` expects `403` on `tools/invoke`).

---

## FAQ (subscribers)

Plain-language answers live on the uandai.ai app **FAQ** page (`/faq`) — search **openclaw** or **integration**. Topics include:

- Who can use integration (active subscription)
- Browser chat vs programmatic API
- Chat URL, gateway base, and session key (also on Workspace → agent → **Integration**)
- Readiness states (provisioning / failed)
- JWT vs raw API key on `/openclaw`
- What is blocked for subscribers

Read bundled `references/openclaw-integration.md` in the `uandai-ai` skill folder before acting. Live `{API_ORIGIN}/docs/openclaw-integration` is for humans unless pasted in chat.

**Postman (Hydra API):** trainer gallery folders `agent-media/` (`01` proxy; `01c`–`01e` direct upload) and public `listings-public/` under `hydra_mvp/postman/collections/Hydra MVP/` — see `hydra_mvp/docs/api-testing.md`.
