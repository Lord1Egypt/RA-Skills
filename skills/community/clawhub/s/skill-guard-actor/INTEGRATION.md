# SkillGuard Integration Guide

> This file is bundled with the `skill-guard` skill. If you installed via
> `clawhub install skill-guard`, it lives at `{baseDir}/INTEGRATION.md` in
> your skills folder.

This guide explains how to wire up your OpenClaw gateway to receive results
from the SkillGuard Apify actor via webhook.

> **Already configured?** If `OPENCLAW_WEBHOOK_URL` and `OPENCLAW_HOOKS_TOKEN`
> are already set in your environment or OpenClaw secrets, and your gateway's
> webhook endpoint is reachable, you can skip straight to Step 4.

## How It Works

SkillGuard runs asynchronously on Apify's cloud. When the scan finishes, Apify
calls back to your OpenClaw gateway's `/hooks/agent` endpoint with the results.
Your agent then processes the verdicts and responds to you.

```
You: "Install the instagram-search skill"
  ↓
Claude triggers numerous_hierarchy/skill-guard-actor (TMjFBNFqIIUfCBf6K) with ad-hoc webhook
  ↓
Actor scans SKILL.md via Lakera Guard (~10–30 seconds)
  ↓
Apify POSTs results to your OpenClaw /hooks/agent endpoint
  ↓
Claude reports verdict and installs (or blocks) the skill
```

---

## Step 1: Enable Webhooks in OpenClaw

Add the following to your `~/.openclaw/openclaw.json`:

```json
{
  "hooks": {
    "enabled": true,
    "token": "your-secret-token-here",
    "path": "/hooks"
  }
}
```

- `token` is required — this becomes your `OPENCLAW_HOOKS_TOKEN`
- `path` defaults to `/hooks` if omitted
- Restart your gateway after saving

Verify it's running:

```bash
curl -X POST http://localhost:18789/hooks/wake \
  -H 'Authorization: Bearer your-secret-token-here' \
  -H 'Content-Type: application/json' \
  -d '{"text":"webhook test"}'
# Should return 200
```

---

## Step 2: Make Your Gateway Reachable

Apify's cloud needs to reach your gateway to deliver the callback. Options:

**Tailscale (recommended)** — if your gateway is on a Tailscale network, use its
Tailscale IP or MagicDNS hostname:
```
http://my-machine.tail1234.ts.net:18789/hooks/agent
```

**Remote gateway** — if you're running OpenClaw on a VPS or cloud server, use its
public IP/domain:
```
https://your-server.com/hooks/agent
```

**Cloudflare Tunnel** — free, no open ports, works on any network:
```bash
cloudflared tunnel --url http://localhost:18789
# Use the https://*.trycloudflare.com URL it gives you
```
For a permanent tunnel, set up a named tunnel via the Cloudflare dashboard and point it at `localhost:18789`.

**ngrok (local dev)** — for testing locally:
```bash
ngrok http 18789
# Use the https:// URL ngrok gives you
```

> ⚠️ `localhost` or `127.0.0.1` will not work — Apify cannot reach your local machine.

---

## Step 3: Set Environment Variables

Add these to your OpenClaw secrets or environment:

```bash
APIFY_TOKEN=your_apify_api_token       # from console.apify.com
LAKERA_API_KEY=your_lakera_api_key     # from platform.lakera.ai
OPENCLAW_WEBHOOK_URL=https://your-gateway-url/hooks/agent
OPENCLAW_HOOKS_TOKEN=your-secret-token-here
```

To add secrets via OpenClaw CLI:
```bash
openclaw secrets set APIFY_TOKEN=apify_xxxx
openclaw secrets set LAKERA_API_KEY=lkr_xxxx
openclaw secrets set OPENCLAW_WEBHOOK_URL=https://your-gateway/hooks/agent
openclaw secrets set OPENCLAW_HOOKS_TOKEN=your-secret-token
```

---

## Step 4: Install SkillGuard

```bash
clawhub install skill-guard
```

Verify the skill loaded:
```bash
openclaw skills list
# Should show: 🛡️ skill-guard
```

---

## Testing the Integration

Ask your agent to scan a skill:

```
scan the instagram-search skill
```

Or run the bundled script directly:

```bash
bash ~/.openclaw/skills/skill-guard/scripts/scan.sh --slug instagram-search
```

You should see:
1. Claude triggers numerous_hierarchy/skill-guard-actor (TMjFBNFqIIUfCBf6K)
2. Within ~30 seconds, Claude reports back with a verdict
3. If safe, Claude proceeds with installation. If flagged, Claude blocks it.

---

## Troubleshooting

**Webhook never fires back**
- Confirm your gateway URL is publicly reachable (test with curl from another machine)
- Check Apify Console → the actor run's webhook log for delivery errors
- Make sure `hooks.enabled: true` is set and gateway was restarted

**401 Unauthorized from OpenClaw**
- Verify `OPENCLAW_HOOKS_TOKEN` matches the `hooks.token` in your config exactly

**Actor run starts but no response from Claude**
- Check gateway logs: `openclaw logs` or `~/.openclaw/gateway.log`
- The `/hooks/agent` endpoint returns `202` (async) — Claude processes it in the background

**Scan takes too long**
- SkillGuard uses `run-sync` with a 300-second timeout. If ClawHub or Lakera is slow, it may time out. Check the Apify run logs for where it stalled.