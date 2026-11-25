# BYOB Workspace Bridge — Reference Runtime

**Pinned to** `docs/spec/BYOB-WORKSPACE-BRIDGE.md` rev 4 LOCKED 2026-05-30.

The OpenClaw side of the Phase 4 bridge. Lets Mission Control read, edit, and
sync the actual MD files in your agent's working directory — securely, atomically,
and with the same sync semantics OpenClaw uses for its own state.

## What this is (and what it is not)

This is **the production-grade reference runtime** an external openclaw
operator deploys to expose their agent's workspace to Mission Control. It is
not a demo. It is the runtime an MIT distributed-systems engineer would
write if asked to ship this on Monday morning:

- single file, stdlib only, ~430 lines
- atomic writes (`os.replace` after `tempfile.mkstemp`)
- strict spec compliance (every clause in code: NFC, lowercase `%2f`, sha256
  constant for GET, ±10min skew, 5MB cap, ETag = sha256[:32], filename
  echo-back, …)
- defence-in-depth path-safety (NFC normalise + `'/'`/`'..'` reject + resolved
  path must stay under root + `.history` reserved)
- in-process selftest (`workspace_bridge.py selftest`)
- end-to-end test (`test_workspace_bridge_e2e.py` — 11/11 PASS) that spawns
  the real HTTP server on a free port and exercises every endpoint without
  mocks

## Threat model

The runtime trusts the **working tree completely** and the **network not at
all**. Specifically:

| Assumption | Why it holds |
|---|---|
| TLS terminated upstream | Nginx / cloudflared / your tunnel — runtime never reads cleartext credentials from a connection that isn't TLS-terminated. |
| `beak_key` is long-lived but rotatable | If exposed, rotate via Mission Control + restart the runtime with the new key. Old chain signatures stop verifying — that's by design (Lane A signing trust boundary per spec finding CC). |
| HMAC protects against replay within ±10 min | Window pinned by spec finding R for NTP-pessimistic hosts. Optional: BYOB-side nonce tracking (`recent_timestamps` set, evict at 10min) hardens against in-window replay. Not required by spec. |
| Mission Control proxy validates SSRF before it reaches us | Spec finding CC blocks private IPs at the platform proxy. We can still bind to a private interface for additional defence-in-depth — see "Deployment". |
| Local filesystem is the source of truth | We never trust the request's etag if the file changed under us; `if_match` is enforced with the *current* file hash, not a cached value. |

**Out of scope for v1:**
- Mid-flight content scanning (CSP/XSS) — MC renders as plaintext; runtime
  serves bytes verbatim. If you have policy needs, layer an inspecting proxy.
- Auditing the *content* of writes (we audit metadata: timestamp + sender +
  etag transitions). Use `.history/` for content audit.
- Multi-tenant isolation — one runtime serves one workspace. Run N processes
  for N agents.

## Discovery — "as if it was syncing of its own UI"

The runtime locates the agent workspace via this precedence chain. The
**Gateway-token path** is the one Josh asked for — it mirrors how the existing
openclaw skill discovers its own state, so the bridge feels native:

1. `--workspace <path>` flag — explicit override (highest priority)
2. `$SPACEDUCK_WORKSPACE_DIR` env
3. **Gateway lookup**: `~/.openclaw/credentials/clawhub-gateway.json` → `spaceduck.workspace_dir`
4. Conventional `~/.openclaw/agents/<first>/`
5. Current working directory if it contains `AGENTS.md`

Run `python3 workspace_bridge.py introspect` to see which path was taken on
your host.

## Quick start

```bash
# 1. Get the agent's beak_key from Mission Control (Hatch panel)

# 2. Selftest the runtime
python3 workspace_bridge.py selftest

# 3. Run it
SPACEDUCK_BEAK_KEY=bk_LIVE_... \
python3 workspace_bridge.py run \
  --bind 0.0.0.0:8086 \
  --workspace ~/.openclaw/agents/wayne

# 4. Expose with a tunnel (laptop dev)
cloudflared tunnel --url http://localhost:8086
#   → https://random-tunnel.trycloudflare.com

# 5. Point Mission Control at it
curl -X POST https://beak.spaceduckling.com/beak/me/duck/$SD_ID/workspace-url \
  -H "Authorization: Bearer $JWT" -H 'Content-Type: application/json' \
  -d '{"url":"https://random-tunnel.trycloudflare.com"}'

# 6. Open Mission Control → Files. Banner flips to green ("LIVE from
#    agent workspace"); the file list now comes from your local disk.
```

## Production deployment

### Behind nginx + systemd

```ini
# /etc/systemd/system/spaceduck-bridge.service
[Service]
EnvironmentFile=/etc/default/spaceduck-bridge   # SPACEDUCK_BEAK_KEY=…
ExecStart=/usr/bin/python3 /opt/space-duck/workspace_bridge.py run \
            --bind 127.0.0.1:8086 \
            --workspace /var/lib/openclaw/agents/wayne
Restart=always
User=openclaw
ProtectSystem=strict
ReadWritePaths=/var/lib/openclaw/agents/wayne
```

```nginx
# /etc/nginx/sites-enabled/spaceduck-bridge
server {
  listen 443 ssl http2;
  server_name wayne-bridge.example.com;
  ssl_certificate     /etc/letsencrypt/live/wayne-bridge/fullchain.pem;
  ssl_certificate_key /etc/letsencrypt/live/wayne-bridge/privkey.pem;
  client_max_body_size 6m;
  location /v1/ {
    proxy_pass http://127.0.0.1:8086;
    proxy_read_timeout 20s;
    proxy_set_header Host $host;
    proxy_set_header X-Forwarded-For $remote_addr;
  }
}
```

### AWS Fargate

Containerise (`python:3.11-slim` + the file) and run with:
- Health check: `GET /v1/files` with valid headers
- Bind: `0.0.0.0:8086` (ALB terminates TLS)
- IAM role: read/write on the EFS / EBS mount that holds the workspace

### Tailscale / WireGuard

Bind to `0.0.0.0:8086`. Set workspace URL to your tailnet hostname — no public
exposure, no nginx needed. The platform proxy must resolve to a reachable IP
that is **not** in the SSRF private-range list, so use a hostname that
resolves to a Tailscale 100.x address only if your platform proxy is on the
same tailnet. Otherwise expose via cloudflared.

## Observability

The handler logs nothing by default (HTTP servers that log every request leak
filenames into syslog). Uncomment `super().log_message(fmt, *args)` in
`BridgeHandler.log_message` for stdout-style access logs during dev.

For prod: layer access logging at nginx; metrics via promtail / Vector.
Mission Control already audits every read/write call platform-side
(`byob_workspace.*` events with 90d/365d split TTL per spec).

## Failure modes

| Scenario | Runtime behaviour | MC behaviour |
|---|---|---|
| Process crashes mid-write | `os.replace` is atomic — file is either old bytes or new bytes; no truncation | next read gets old or new etag; if 409 → MC prompts overwrite |
| Disk full during snapshot copy | `write_atomic` raises → 5xx to MC | MC shows retry banner; cache + .history untouched |
| Clock drift > 10 min | every signed request → 401 `stale_timestamp` | MC banner: "check the agent's clock — drift > 10 minutes" + NTP-fix link |
| `beak_key` rotated upstream but not here | every signed request → 401 `invalid_token` | MC banner: "rotate the beak key and update your runtime" |
| Path traversal attempt | resolved path doesn't start with workspace root → 404 `invalid_filename` | MC: standard 404 |
| `.history/` directly requested | rejected in `_safe()` | MC: 404 |
| Symlink pointing outside workspace | `Path.resolve()` follows the link; the prefix check then rejects | 404 |

## Testing

```bash
python3 workspace_bridge.py selftest               # in-proc HMAC + atomic write
python3 test_workspace_bridge_e2e.py                # end-to-end via real HTTP
```

Both must pass before deploying. Selftest covers HMAC canonical layer + atomic
write semantics. E2E covers the full wire protocol including auth failures.

## Versioning

This file SHIPS rev 4 of the spec. When the spec bumps, bump the version
banner in the source (`server_version = 'spaceduck-byob-bridge/1.0'`) and
regenerate the README's compatibility statement. Mission Control verifies
`server_version` is `spaceduck-byob-bridge/1.x` and surfaces a warning for
mismatches.

## Files

- `workspace_bridge.py` — the runtime (single file)
- `test_workspace_bridge_e2e.py` — end-to-end test (11/11 PASS)
- `byob_hmac.py` — Python HMAC reference (used by both runtime + tests)
- `../space-duck-html/static/byob-hmac.js` — browser HMAC reference
- `../../docs/spec/BYOB-WORKSPACE-BRIDGE.md` — protocol spec rev 4 LOCKED
