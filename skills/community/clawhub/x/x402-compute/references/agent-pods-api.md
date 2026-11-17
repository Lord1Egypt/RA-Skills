# Agent Pods API — `/pods/v1` (API-key surface)

The endpoints in `agent-pods.md` are the **dashboard's** surface: they expect a wallet
signature or a compute session, which is right for a human at a browser and awkward for a
program. `/pods/v1` is the same product behind **one API key**, meant for building on top of
pods rather than clicking them.

Use this reference when the caller holds an `x402c_…` key and no wallet. Use `agent-pods.md`
when signing with OWS.

- **Base:** `https://compute.x402layer.cc/pods/v1`
- **Auth:** `X-API-Key: x402c_…` on every route
- **Mint a key:** dashboard → Settings → API Keys

---

## Two rules that will cost you if you skip them

**Create is idempotent and the header is required.** `POST /pods` refuses without
`Idempotency-Key`, because the call provisions a machine and charges for it. Replaying the
same key returns the original response byte for byte instead of making a second pod; the same
key with a *different* body is a `409` with `details.code = idempotency_mismatch`, since that
is a bug in the caller and swallowing it would hide it.

Use an id you already have — an order number, a job id. A generated UUID protects a retry
inside one process; only a stable id protects a retry after that process dies.

**Delete is not instant.**

| Response | Meaning |
|---|---|
| `200` `destroyed` | the machine is confirmed gone |
| `202` `destroying` | accepted, provider would not delete yet, **may bill a few minutes more** |

A provider refuses to remove a machine that is still installing. Treating `202` as done is how
a pod keeps billing after you thought you deleted it. Poll `GET /pods/{id}` until `destroyed`.

---

## Create, then talk to it

```bash
POD=$(curl -s -X POST https://compute.x402layer.cc/pods/v1/pods \
  -H "X-API-Key: $SGL_API_KEY" \
  -H "Idempotency-Key: order-4471" \
  -H 'content-type: application/json' \
  -d '{
    "tier": "starter",
    "name": "support agent",
    "external_ref": "customer-42",
    "agent_identity": "You are Atlas, Acme Cloud support.",
    "agent_instructions": "Answer as Acme support. Be concise and cite the current integration step.",
    "heartbeat_prompt": "Check open escalations and renew yourself if runway is low. Stay silent if clear.",
    "agent_heartbeat_minutes": 30
  }' | jq -r .pod.id)

# Booting takes a few minutes. status goes provisioning -> online.
curl -s "https://compute.x402layer.cc/pods/v1/pods/$POD" -H "X-API-Key: $SGL_API_KEY" | jq -r .pod.status
```

`external_ref` is **your** id. It comes back on every read and filters `GET /pods`, so you can
find a pod again from your own database without storing ours.

### Engines

`engine` picks the agent. Leave it out and you get ClawPod.

| `engine` | Product | What it is |
|---|---|---|
| `clawpod` | ClawPod (OpenClaw) | Always-on agent: chat, shell, browser, wallet, Telegram and Discord |
| `hermpod` | HermPod (Hermes) | Self-improving agent that writes its own skills and keeps long-term memory |
| `pipod` | Pi pod | Lightweight coding agent, extended with skills and MCP tools |

Any other value is a `400` listing the valid names. Check `available` per engine in
`GET https://compute.x402layer.cc/pods/catalog` before you build on one.

### Bring your own AI key (BYOK), with fallbacks

Managed pods run Singularity Layer models from your credits. A BYOK pod runs on your key:

```json
{
  "engine": "clawpod",
  "tier": "starter",
  "ai": {
    "mode": "byok",
    "preset": "venice",
    "api_key": "<YOUR_PROVIDER_KEY>",
    "name": "Venice",
    "fallbacks": [
      { "preset": "openrouter", "api_key": "<YOUR_OPENROUTER_KEY>", "model": "meta-llama/llama-3.3-70b-instruct" },
      { "preset": "singularity", "model": "z-ai/glm-5.3" }
    ],
    "managed_models": true
  },
  "model": "<model id at your provider>"
}
```

- `preset`: `openrouter`, `openai`, `venice`, `0g` or `custom`. A preset fixes the URL, so you
  send only the key and model. `custom` needs `base_url` (https) and optionally `api`
  (`openai-completions`, `openai-responses`, `anthropic-messages`, `google-generative`).
- `fallbacks`: up to 3 providers tried in order when the primary fails, each
  `{preset, api_key, model, name?, base_url?, api?}`. One extra entry may be
  `{preset: "singularity", model}` for a Singularity Layer model.
- `managed_models`: on by default for a BYOK ClawPod. The pod may also use Singularity Layer
  models, billed per call from your credits (no included allowance). The list is
  `byok_managed_models.models` in the catalog; the agent switches with `/model singularity/<id>`.
- Fallbacks and Singularity Layer models on a BYOK pod are ClawPod only for now.
- To change providers later, `PATCH /pods/{id}` with `ai.providers` (the whole ordered list,
  primary first; leave out `api_key` to keep a stored key) and `ai.managed_models`.

### Customizing the agent

Platforms can customize a pod without taking over the managed runtime files:

| Field | Create | PATCH | Meaning |
|---|---:|---:|---|
| `agent_identity` | yes | yes | Owner/platform identity text, max 8000 chars. Rendered into managed `AGENTS.md` and `IDENTITY.md`. |
| `agent_instructions` | yes | yes | Owner/platform operating instructions, max 8000 chars. Rendered into managed `AGENTS.md`. |
| `heartbeat_prompt` | yes | yes | Prompt for the quiet self-check heartbeat, max 4000 chars. |
| `agent_heartbeat_minutes` | yes | yes | Heartbeat cadence: `0` disables; otherwise 15-1440 minutes. |

`AGENTS.md` itself is **not** raw-editable through the API. The platform-managed base keeps
wallet survival, spend caps, x402 payment safety, and tool boundaries intact. Your text is
rendered into a bounded owner/platform section; send `""` or `null` on PATCH to clear a
custom text field and restore the default heartbeat prompt.

`GET /pods/{id}` returns:

```json
{
  "pod": {
    "id": "pod_...",
    "customization": {
      "agent_identity": "You are Atlas, Acme Cloud support.",
      "agent_instructions": "Answer as Acme support.",
      "heartbeat_prompt": "Check open escalations. Stay silent if clear."
    },
    "agent_heartbeat_minutes": 30
  }
}
```

Once `online`, mint a pod key and use any OpenAI client. The model id is **`agent-pod`**:

```bash
KEY=$(curl -s -X POST "https://compute.x402layer.cc/pods/v1/pods/$POD/keys" \
  -H "X-API-Key: $SGL_API_KEY" -H 'content-type: application/json' -d '{}' | jq -r .key.secret)

curl -s -X POST "https://compute.x402layer.cc/pods/$POD/v1/chat/completions" \
  -H "Authorization: Bearer $KEY" -H 'content-type: application/json' \
  -d '{"model":"agent-pod","messages":[{"role":"user","content":"summarise today"}]}'
```

Streaming works (`"stream": true`, SSE). The pod key is returned **once**; it is not the same
thing as the account key and cannot manage pods.

---

## Routes

| Method | Path | Notes |
|---|---|---|
| `POST` | `/pods` | `Idempotency-Key` required. `201`, `status: provisioning` |
| `GET` | `/pods` | Newest first. `?external_ref=`, `?cursor=`, `?limit=` |
| `GET` `PATCH` `DELETE` | `/pods/{id}` | PATCH: `name`, `model`, `slug`, `auto_renew`, `agent_identity`, `agent_instructions`, `heartbeat_prompt`, `agent_heartbeat_minutes` |
| `POST` `GET` | `/pods/{id}/keys` | Pod endpoint keys; secret shown once |
| `DELETE` | `/pods/{id}/keys/{keyId}` | Takes effect immediately |
| `GET` | `/pods/{id}/usage` | AI spend and token counts |
| `POST` `GET` | `/pods/{id}/actions` | `restart`, `stop`, `redeploy`, `update`, `diagnose`, `logs` |
| `GET` `POST` | `/pods/{id}/tasks` | Scheduled tasks |
| `PATCH` `DELETE` | `/pods/{id}/tasks/{jobId}` | |
| `GET` `PATCH` | `/pods/{id}/wallet` | Cap field is `per_tx_cap_usd` |
| `GET` `PATCH` | `/pods/{id}/updates` | Who decides when this pod takes our updates |
| `POST` | `/pods/{id}/wallet/send` | Move funds. Needs `pods:wallet:write` |
| `POST` | `/pods/{id}/wallet/x402/pay` | Pay an x402 endpoint from the pod wallet |
| `GET` `POST` `DELETE` | `/pods/{id}/connectors` | MCP connectors |
| `GET` `PATCH` | `/pods/{id}/backups` | |
| `POST` | `/pods/{id}/exec` | Sandbox: run a shell command. Needs `pods:control:write` |
| `GET` `PUT` | `/pods/{id}/files` | Sandbox: list, read (`?path=`), write files. Needs `pods:control:write` |
| `POST` `GET` | `/pods/{id}/ports` | Sandbox: open a public URL to a port, list open ports |
| `DELETE` | `/pods/{id}/ports/{port}` | Close a port |
| `POST` `GET` | `/pods/{id}/clone` | POST: new pod restored from this pod's Vault backup. GET (on the new pod): restore status |
| `POST` | `/pods/{id}/chat-ticket` | Ticket for the streaming socket |
| `POST` `GET` | `/pods/{id}/channels/telegram/join-code` | POST mints, GET polls |
| `POST` | `/pods/{id}/channels/telegram/connect` | Attaches the group that claimed the code |
| `POST` | `/pods/{id}/channels/{channel}/pair` | Approves someone to DM the agent |
| `GET` | `/events` | Account event log, paged by `seq` |
| `POST` `GET` | `/webhooks` · `PATCH` `DELETE` `/webhooks/{id}` | |

### Actions are queued, not immediate

`POST /actions` returns **202**. The pod applies it on its next check-in, usually within a
minute. `diagnose` and `logs` write their output back through the heartbeat — read it from
`GET /actions` as `last_result`, and expect a minute or two, not a second.

Same for `tasks` and `connectors`: a `202` means the pod has been told, not that it is done.
`GET /tasks` reports what the pod itself says it has, so it lags the write by a heartbeat.

### Pairing: who may DM the agent

A stranger who finds the bot's username can DM it, and unlike a group that conversation is
private. So the agent refuses unknown people, shows them a short code, and waits. `POST
.../channels/{channel}/pair` with that `code` approves them.

The code must come from the agent, so this approves a pairing somebody already started — it
cannot add a person who never asked.

### Deciding when a pod takes an update

We ship updates to the pod's scripts, and by default a pod applies ours within six hours,
restarting its gateway for about forty seconds. That is fine for a pod you run for yourself.
It is not fine if you run pods for customers, because their agents all blink offline at a
moment you did not choose.

`PATCH /pods/{id}/updates` with `{"mode":"manual"}` and we keep answering that pod's version
poll with the version it already has, so it never updates itself. You apply the update when it
suits you:

```bash
curl -X POST ".../pods/v1/pods/$POD/actions" -H "X-API-Key: $KEY" \
  -H 'content-type: application/json' -d '{"action":"update"}'
```

`GET /pods/{id}/updates` tells you whether one is waiting, and `pod.update_available` fires in
the event log when a release arrives that a held pod has not taken.

**The hold expires after 30 days.** Security fixes ride these bundles, so a pod pinned
indefinitely stops being your scheduling choice and becomes an unpatched machine. The response
always names the date, and `hold_expired: true` says plainly when the window has passed.


---

## Sandbox: exec, files, ports, clone

Run commands and edit files inside a pod you own, publish a port, or clone a pod. Allowed for
the owner signed in, or an account key with **`pods:control:write`**. A pod's own key can never
use these routes (an agent must not get a shell on itself through the platform).

The pod must be `online`. For about a minute after it first reports `online` these routes can
answer `409 conflict` "The pod is offline"; retry.

### Run a command

```bash
curl -s -X POST "https://compute.x402layer.cc/pods/v1/pods/$POD/exec" \
  -H "X-API-Key: $SGL_API_KEY" -H 'content-type: application/json' \
  -d '{"command":"ls -la && python3 --version","timeout_seconds":60}'
# { "exec": { "exit_code": 0, "timed_out": false, "duration_ms": 41, "stdout": "...",
#             "stderr": "", "truncated": false, "cwd": "/opt/pod/workspace" } }
```

- `command`: 1 to 20000 characters, run with bash.
- `timeout_seconds`: 1 to 300, default 60. A timeout returns `timed_out: true`.
- Runs as the unprivileged `pod` user in the workspace, with a clean environment. Each of stdout
  and stderr is capped at 1 MB (`truncated: true` when cut).
- Rate limit: 120 per minute.

### Files

```bash
# List the workspace
curl -s "https://compute.x402layer.cc/pods/v1/pods/$POD/files" -H "X-API-Key: $SGL_API_KEY"
# -> { "files": [...], "root": "/opt/pod/workspace" }

# Read one file
curl -s "https://compute.x402layer.cc/pods/v1/pods/$POD/files?path=notes.txt" -H "X-API-Key: $SGL_API_KEY"
# -> { "file": { "path", "content", "modified", "managed" } }

# Write (create or replace) a text file
curl -s -X PUT "https://compute.x402layer.cc/pods/v1/pods/$POD/files" \
  -H "X-API-Key: $SGL_API_KEY" -H 'content-type: application/json' \
  -d '{"path":"notes.txt","content":"hello"}'
# -> { "file": { "path", "size", "modified" } }
```

Rate limit 240 per minute. Bodies are capped at 128 KB like the rest of the API.

### Ports: a public URL for something the pod serves

```bash
curl -s -X POST "https://compute.x402layer.cc/pods/v1/pods/$POD/ports" \
  -H "X-API-Key: $SGL_API_KEY" -H 'content-type: application/json' \
  -d '{"port":8080,"visibility":"private"}'
# 201 { "port": { "port": 8080, "url": "https://.../pods/port/<id>/", "token": "...",
#                 "token_header": "x-pod-port-token", "note": "..." }, "rotated": false }
```

- The URL (and the token for a `private` port) is shown **once**. Opening the same port again
  rotates them (`200`, `rotated: true`). `public` (default) needs no token; `private` needs the
  token in the `x-pod-port-token` header.
- Ports 1024 to 65535 only. Ports the platform uses on the pod (8642, 8787, 18780 to 18799) are
  refused.
- At most 5 open ports per pod. `GET /ports` lists them (never the URLs).
  `DELETE /ports/{port}` closes one.
- Proxied requests: HTTP only, 5 MB per body, 30 second timeout, 600 requests per minute per pod.

### Clone a pod from its Vault backup

Makes a **new pod**, billed exactly like `POST /pods` (same rails, caps and `Idempotency-Key`
rule), and restores the source pod's latest completed Agent Vault backup onto it once it is
online (usually 5 to 10 minutes).

```bash
curl -s -X POST "https://compute.x402layer.cc/pods/v1/pods/$POD/clone" \
  -H "X-API-Key: $SGL_API_KEY" -H "Idempotency-Key: clone-4471" -H 'content-type: application/json' \
  -d '{"passphrase":"<YOUR_VAULT_PASSPHRASE>","name":"support agent 2"}'
# 201 { "pod": {...}, "clone": { "source_pod_id", "backup_id", "restore": { "status": "pending" } } }

# Then, on the NEW pod id:
curl -s "https://compute.x402layer.cc/pods/v1/pods/$NEW_POD/clone" -H "X-API-Key: $SGL_API_KEY"
```

- Body: `passphrase` (your Vault backup passphrase, required), and optional `backup_id`, `name`,
  `term_hours`, `region`, `max_total_usd`, `channels`, `ai`.
- Copied: engine, tier, managed model, template, customization, heartbeat, capabilities.
  Not copied: channel tokens (pass `channels`), a BYOK key (pass `ai` for a BYOK source), the
  vanity slug, wallet, keys, webhooks, ports.
- `409` with `details.code = no_backup` means the source has no completed backup yet. Turn
  backups on with `PATCH /pods/{id}/backups`; backups run automatically.

---

## Scopes

Ordinary work needs `compute:read` / `compute:write`. Two powers are deliberately separate, so
a general key cannot use them:

| Scope | Grants |
|---|---|
| `pods:wallet:write` | Send from a pod wallet, pay x402 endpoints with it, raise its caps, set a backup passphrase |
| `pods:control:write` | Add/remove connectors, the Sandbox API (exec, files, ports), and a full-power control socket (pod files, skills, backups) |

Without `pods:control:write` a chat ticket is issued at **`chat`** scope: the socket accepts
conversation and nothing else. That is the intended default. Ask for the scope only when you
need the workspace, and expect a `403` naming it if you did not.

---

## Events and webhooks

**The log is the source of truth; webhooks are one way to read it.** A failed delivery is
gone, the log is not — so if you miss one, page `GET /events` and catch up.

Page by **`seq`**, never by timestamp. `seq` only goes up. Two events can share a millisecond,
and a timestamp cursor either skips one or repeats it forever.

```bash
curl -s "https://compute.x402layer.cc/pods/v1/events?after=41&limit=50" -H "X-API-Key: $SGL_API_KEY"
# { "events": [...], "next_after": 92, "has_more": true }
```

Types: `pod.created`, `pod.active`, `pod.destroyed`, `pod.destroy_failed`,
`pod.action.queued`, `pod.status.changed`, `pod.renewed`, `pod.renewal_failed`,
`pod.expiring`, `pod.backup.completed`, `pod.backup.failed`, `pod.update_available`.

### Verifying a delivery

HTTPS only. The signing secret is returned **once** at creation. Omit `event_types` for
everything; an empty array is refused, because subscribing to nothing is a webhook that
silently never fires.

```
x-sgl-signature: t=<unix>,v1=<hmac-sha256 of "<t>.<raw body>">
x-sgl-event-type: pod.status.changed
x-sgl-event-id: <uuid>
```

**Verify against the raw body.** Parsing and re-encoding JSON changes key order and spacing,
and the signature covers the bytes we sent — re-serialise and a genuine delivery will fail to
verify. Both SDKs ship a helper (`verifyPodWebhook`, `verify_pod_webhook`) that also enforces
the timestamp window; without that window, putting the timestamp inside the signature buys
nothing, because an old capture would still verify.

Failures back off (1, 5, 15, 60, 180, 360, 720 minutes) and then stop. When we give up,
`disabled_by_us_at` is set — deliberately distinct from `enabled: false`, which is you turning
it off. From the outside both look like silence.

---

## Errors and limits

```json
{ "error": { "code": "conflict", "message": "...", "details": { "code": "idempotency_mismatch" } } }
```

Branch on `code`, not the message: `invalid_request`, `unauthorized`, `forbidden`,
`not_found`, `conflict`, `limit_exceeded`, `capability_disabled`, `rate_limited`,
`not_implemented`, `internal`.

Every response carries **`x-request-id`**. Send your own and it is echoed; quote it in a
support message and it can be found in our logs.

| Limit | |
|---|---|
| Reads | 240/min per account |
| Writes | 60/min per account |
| **Creates** | **60/hour**, a separate bucket — this one provisions machines and charges |
| Body | 128 KB |
| Wallet moves | 30/hour, its own bucket |
| Webhooks | 10 per account |
| Event retention | 30 days |

---

## SDKs

Both published clients wrap this surface and are kept feature-equal:

```ts
import { PodsClient } from "@singularity-layer/grid";
const pods = new PodsClient({ apiKey: process.env.SGL_API_KEY! });
const pod = await pods.createPod({
  tier: "starter",
  idempotencyKey: `order-${id}`,
  agentIdentity: "You are Atlas, Acme Cloud support.",
  agentInstructions: "Answer as Acme support and cite the integration step.",
  heartbeatPrompt: "Check open escalations. Stay silent if clear.",
  agentHeartbeatMinutes: 30,
});
await pods.waitForOnline(pod.id);
```

```python
from singularity_grid import PodsClient
pods = PodsClient(api_key=os.environ["SGL_API_KEY"])
pod = pods.create_pod(
    tier="starter",
    idempotency_key=f"order-{id}",
    agent_identity="You are Atlas, Acme Cloud support.",
    agent_instructions="Answer as Acme support and cite the integration step.",
    heartbeat_prompt="Check open escalations. Stay silent if clear.",
    agent_heartbeat_minutes=30,
)
pods.wait_for_online(pod["id"])
```

`waitForDestroyed` / `wait_for_destroyed` exist for the same reason the `202` above does: they
hold until the machine is genuinely gone rather than until we accepted the request.
