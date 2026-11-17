---
name: topical-openclaw-setup
description: Wire Topical into OpenClaw — MCP server, inbound hook transform, and outbound webhook registration. Use when the user asks to connect Topical, set up Topical webhooks, or install the Topical OpenClaw integration.
homepage: https://usetopical.com
metadata: { "openclaw": { "requires": { "bins": ["openclaw"] } } }
---

# Install Topical for OpenClaw

You are inside an OpenClaw agent. The user wants Topical connected end-to-end:

1. **Pull** — MCP tools (`list_topics`, `get_topic_update`, …) via hosted Topical MCP.
2. **Push** — Topical POSTs `topic_briefing` and `topic_breaking_news` to the user's OpenClaw gateway hook.

The contract: print each command before running it, **merge** OpenClaw config (never overwrite unrelated keys), verify with `openclaw mcp list` / `openclaw mcp probe topical`, and tell the user what to paste into the Topical portal if they have not already.

Pair with [@daveangelcode/topical](https://clawhub.ai/daveangelcode/skills/topical) for day-to-day intelligence workflows after setup.

ClawHub: [topical-openclaw-setup](https://clawhub.ai/daveangelcode/skills/topical-openclaw-setup) · companion [topical](https://clawhub.ai/daveangelcode/skills/topical)

---

## Before you start

| Prerequisite | Where |
| --- | --- |
| Topical account + Agent API key | Portal → **Connect OpenClaw** (`https://app.usetopical.com/portal/openclaw/`) or **Settings → Agent API keys** |
| OpenClaw gateway running | `openclaw gateway status` |
| Public HTTPS URL to gateway hooks | **Topical portal only** — user registers where Topical should POST; OpenClaw does not need this in its config |

If the user has no API key yet, stop and send them to the Connect OpenClaw wizard in the Topical portal. They must copy the Bearer token once.

**Do not ask which Topical domain to use.** Topical MCP is always `https://app.usetopical.com/api/mcp`.

### Agent API key format

Keys from the Topical portal look like:

`agt_live_<uuid>_<secret>` (production) or `agt_test_<uuid>_<secret>` (non-production)

- Prefix: `agt_live_` or `agt_test_`
- Middle: UUID with dashes (36 characters), e.g. `827ce959-523e-49fe-a666-bb2ec41066ae`
- Suffix: 43-character base64url secret after the final `_`

Total length is ~89 characters. **The embedded UUID is normal** — accept keys copied from the portal; do not reject them as placeholders because of dashes or underscores.

---

## Step 1 — Discovery

Run these checks and report results as facts:

```bash
which openclaw
openclaw --version 2>/dev/null || true
test -f ~/.openclaw/openclaw.json && echo "openclaw.json: yes" || echo "openclaw.json: missing"
openclaw mcp list 2>&1 | grep -i topical || echo "topical MCP: not configured"
test -f ~/.openclaw/hooks/transforms/topical-inbound.mjs && echo "transform: installed" || echo "transform: missing"
```

Branch:

- **topical MCP already listed** → skip Step 2, go to Step 3.
- **No openclaw.json** → ask once where config lives; default `~/.openclaw/openclaw.json`.
- **Not OpenClaw** → stop; this skill is OpenClaw-only.

---

## Step 2 — Wire MCP (hosted HTTP)

Ask the user for their Topical **Agent API key** only if it was not already provided in the portal prompt. Accept keys matching `agt_live_<uuid>_<secret>` (~89 chars) — the UUID in the middle is expected, not a placeholder. Use **agentId**, **delivery channel**, and **topical.config.json** from the prompt exactly — do not re-ask. The hosted MCP URL is always:

`https://app.usetopical.com/api/mcp`

```bash
openclaw mcp set topical '{"url":"https://app.usetopical.com/api/mcp","transport":"streamable-http","headers":{"Authorization":"Bearer <AGENT_API_KEY>"}}'
openclaw mcp probe topical
```

Verify:

```bash
openclaw mcp list 2>&1 | grep -i topical
```

Install the usage skill if missing:

```bash
openclaw skills install @daveangelcode/topical --global
```

---

## Step 3 — Install hook transform

OpenClaw only loads transform modules from `~/.openclaw/hooks/transforms/` (not from skill directories).

From the topical skill bundle (ClawHub install path or `{baseDir}/../topical` in this monorepo):

```bash
bash "{baseDir}/scripts/copy-transforms.sh"
```

Or manually:

```bash
mkdir -p ~/.openclaw/hooks/transforms
cp <topical-skill>/assets/topical-inbound.mjs ~/.openclaw/hooks/transforms/
cp <topical-skill>/assets/topical.config.example.json ~/.openclaw/hooks/transforms/topical.config.json
```

Edit `~/.openclaw/hooks/transforms/topical.config.json`:

```json
{
  "agentId": "main",
  "deliver": true,
  "channel": "telegram",
  "to": "<CHAT_ID_IF_TELEGRAM>",
  "accountId": "default"
}
```

Use `"channel": "last"` when replies should go to the user's last active channel (omit `to`).

---

## Step 4 — Enable hooks mapping

Generate a **new** `hooks.token` (distinct from `gateway.auth.token`). Merge into `~/.openclaw/openclaw.json`. OpenClaw only needs the local hook path (`/hooks/topical-inbound`) — **do not ask for the public gateway URL**; the user registers that in the Topical portal.

```json5
{
  hooks: {
    enabled: true,
    token: "<RANDOM_HOOKS_TOKEN>",
    path: "/hooks",
    transformsDir: "~/.openclaw/hooks/transforms",
    mappings: [
      {
        match: { path: "topical-inbound" },
        action: "agent",
        transform: { module: "topical-inbound.mjs", export: "topicalInbound" },
      },
    ],
  },
}
```

Merge programmatically (preserve existing keys):

```bash
python3 <<'PY'
import json, secrets
from pathlib import Path
p = Path.home() / ".openclaw" / "openclaw.json"
cfg = json.loads(p.read_text()) if p.exists() else {}
hooks = cfg.setdefault("hooks", {})
if not hooks.get("token"):
    hooks["token"] = secrets.token_hex(24)
hooks["enabled"] = True
hooks.setdefault("path", "/hooks")
hooks.setdefault("transformsDir", "~/.openclaw/hooks/transforms")
mappings = hooks.setdefault("mappings", [])
if not any(m.get("match", {}).get("path") == "topical-inbound" for m in mappings):
    mappings.append({
        "match": {"path": "topical-inbound"},
        "action": "agent",
        "transform": {"module": "topical-inbound.mjs", "export": "topicalInbound"},
    })
p.parent.mkdir(parents=True, exist_ok=True)
p.write_text(json.dumps(cfg, indent=2))
print("hooks.token:", hooks["token"])
print("Local inbound path: /hooks/topical-inbound")
print("Register in Topical portal: <public-https-url>/hooks/topical-inbound with this hooks.token")
PY
```

Tell the user to copy **`hooks.token`** into the Topical portal (**Connect OpenClaw** wizard → register webhook). They enter their own public gateway URL there — OpenClaw does not store it.

---

## Step 5 — Register Topical outbound webhook (portal)

**Prefer the Topical portal** over `manage_agent_webhook` unless the user explicitly asks the agent to register it.

In the portal, the user saves:

- **URL:** `https://<their-public-gateway>/hooks/topical-inbound`
- **Bearer token:** the `hooks.token` from Step 4

Save the returned **signing secret** — Topical sends `X-Topical-Signature` on each POST.

Optional — register via MCP only if the user provides their public URL and asks you to call the tool:

```json
{
  "action": "set",
  "url": "https://<PUBLIC_GATEWAY_HOST>/hooks/topical-inbound",
  "bearerToken": "<hooks.token>",
  "breakingNewsAlertsEnabled": true,
  "briefingEnabled": true
}
```

---

## Step 6 — Restart and verify

```bash
openclaw gateway restart
bash "{baseDir}/scripts/verify-migration.sh"
```

Optional live probe (requires public URL):

```bash
curl -sS -X POST "https://<PUBLIC_GATEWAY_HOST>/hooks/topical-inbound" \
  -H "Authorization: Bearer <hooks.token>" \
  -H "Content-Type: application/json" \
  -d '{"type":"topic_breaking_news","topicId":"test","breakingNewsId":"probe","title":"Setup probe","summary":"Ignore","relevanceScore":0,"sources":[],"deliveredAt":"2026-01-01T00:00:00.000Z"}'
```

---

## Security notes

- Never commit or log the Agent API key or `hooks.token`.
- `hooks.token` must differ from `gateway.auth.token` — run `openclaw security audit` if unsure.
- Transform modules run with gateway trust — only install from `@daveangelcode/topical` or this repo.

---

## Done message template

Tell the user:

1. MCP: `openclaw mcp probe topical` succeeds.
2. Push URL registered in Topical portal (user's public URL + `hooks.token` from Step 4).
3. Digests arrive after the next scheduled topic run; event alerts fire on high-relevance matches.
4. For briefings on demand, use `@daveangelcode/topical` workflows (`get_topic_update` with `sinceLastRun: true`).
