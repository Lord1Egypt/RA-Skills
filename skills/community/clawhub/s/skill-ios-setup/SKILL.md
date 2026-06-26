# skill-ios-setup

Set up the OpenClaw iOS app on any OpenClaw installation. Deploys the stats server, configures access, and outputs connection details for the user.

## When to use
- User says "set me up for the iOS app", "I want to use the iOS app", "help me connect the app"
- After a fresh OpenClaw install
- Stats server is down or iOS can't connect

## What this skill does NOT do
- Blog pipeline setup
- Outreach pipeline setup
- Any business-specific crons or pipelines
- Those are optional — the app works without them

---

## Step 1 — Detect environment

Find this skill's own directory first:
```bash
openclaw skills list --json 2>/dev/null | python3 -c "
import json,sys
skills = json.load(sys.stdin)
for s in skills:
    if s.get('id','').startswith('skill-ios-setup'):
        print(s.get('path',''))
        break
"
```

Then run the environment check script from that path:
```bash
python3 <skill-dir>/scripts/detect_env.py
```

This outputs JSON with:
- `install_type`: `docker` | `direct`
- `workspace`: path to agent workspace (e.g. `~/.openclaw/workspace/main`)
- `gateway_token`: from openclaw config
- `gateway_port`: default 18789
- `stats_running`: bool
- `stats_port`: 8765
- `public_ip`: detected public IP if any
- `tailscale_ip`: Tailscale IP if tailscale is installed
- `nginx_available`: bool
- `os`: linux | macos | other

> The `workspace` field is the source of truth for all subsequent paths — never hardcode `orchestrator` or any agent name.

---

## Step 2 — Deploy stats server

Check `stats_running`. If false, deploy it:

```bash
python3 <skill-dir>/scripts/deploy_stats.py
```

This will:
1. Locate `stats_server.py` under the workspace path from Step 1
2. Install Python deps (requests, etc.) if missing
3. Start the stats server

If stats server is already running, skip this step.

### Auto-restart on reboot

After starting, set up auto-restart appropriate to the install type:

**Docker install** — tell the user to add `restart: unless-stopped` to their `docker-compose.yml` for the OpenClaw service. Docker will restart the container (and the stats server with it) automatically on reboot or crash.

**Direct install** — use the `workspace` value from Step 1 to build the correct path:
```bash
# workspace = value from detect_env.py output, e.g. /home/user/.openclaw/workspace/main
ENSURE_SCRIPT="<workspace>/scripts/dashboard/ensure_stats_server.sh"

# Tell user to run:
crontab -e
# Add this line (substituting the actual path):
@reboot bash <workspace>/scripts/dashboard/ensure_stats_server.sh
```

Always show the user the fully resolved path — never show a placeholder like `/path/to/`.

Do NOT set up an agent watchdog cron for open source users — it wastes tokens on every install.

---

## Step 3 — Determine connectivity method

Ask the user (or detect from env output):

> "How do you want to expose OpenClaw to your iPhone?
> 1. I have a domain + nginx/reverse proxy
> 2. I use Tailscale
> 3. Direct IP on local network (home/office only)
> 4. I'll set it up myself — just give me the details"

Use their answer to proceed to the relevant step below.

---

## Step 4a — Domain + nginx

Tell the user:

```
Add this to your nginx config (replace YOUR_DOMAIN):

server {
    listen 443 ssl;
    server_name YOUR_DOMAIN;

    # SSL config here (certbot/Let's Encrypt recommended)

    # Gateway (WebSocket + API)
    location / {
        proxy_pass http://127.0.0.1:18789;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_read_timeout 86400;
    }

    # Stats server
    location /stats/ {
        proxy_pass http://127.0.0.1:8765;
        proxy_set_header Host $host;
    }
    location /tools/ {
        proxy_pass http://127.0.0.1:8765;
        proxy_set_header Host $host;
    }
}
```

Then run: `sudo nginx -t && sudo systemctl reload nginx`

**Connection details for iOS app:**
- Gateway URL: `https://YOUR_DOMAIN`
- Token: (from config)

---

## Step 4b — Tailscale

Check if Tailscale is installed (`tailscale_ip` in env output).

If installed, tell the user to run:
```bash
tailscale serve --bg http://127.0.0.1:18789
tailscale serve --bg --set-path /stats http://127.0.0.1:8765
```

Then get their Tailscale hostname:
```bash
tailscale status --json | python3 -c "import json,sys; d=json.load(sys.stdin); print(d['Self']['DNSName'].rstrip('.'))"
```

**Connection details for iOS app:**
- Gateway URL: `https://<tailscale-hostname>`
- Token: (from config)

If Tailscale is NOT installed, suggest it:
> "Tailscale is the easiest way to access OpenClaw remotely with no port forwarding. Install from tailscale.com, then come back and run this skill again."

---

## Step 4c — Local network (LAN only)

Use `lan_ip` from the detect_env.py output directly.

Tell the user:
- Gateway URL: `http://<lan_ip>:18789`
- This only works when your iPhone is on the same WiFi network
- Not recommended for production use

---

## Step 4d — Manual / self-managed

Output the raw details:
- Gateway port: 18789 (WebSocket + HTTP API)
- Stats server port: 8765 (internal, proxy to /stats/* and /tools/*)
- Token: (from config)

Tell them to expose these however they prefer and enter the URL + token in the app.

---

## Step 5 — Output connection summary

Always end with a clean summary block:

```
✅ OpenClaw iOS Setup Complete

Gateway URL:  https://your-domain-or-ip
Token:        your-token-here

In the iOS app:
1. Open the app
2. Enter the URL and token when prompted
3. Tap Connect

Stats server: running on port 8765 ✓
```

If anything failed, clearly say what failed and what the user needs to do manually.

---

## Notes
- **Never hardcode agent names** (`orchestrator`, `main`, etc.) — always use the `workspace` path from `detect_env.py`
- The gateway token comes from: `openclaw config get gateway.auth.token` or from `~/.openclaw/openclaw.json`
- Docker installs: scripts run inside the container, nginx typically lives on the host
- For Docker + nginx: the nginx block is on the HOST, proxying into the container's exposed ports

## Stats server survival across restarts

**Gateway soft restart (SIGUSR1):** stats server survives — it is a separate process, unaffected.

**Docker container restart or machine reboot:** stats server dies. Recovery is handled by the OS-level mechanism set up in Step 2 (Docker `restart: unless-stopped` or system `@reboot` crontab) — no agent watchdog needed.

Tell the user: "If your iOS app loses connection after a server restart, the stats server may have stopped. Message the agent 'restart stats server' and it will bring it back up."
