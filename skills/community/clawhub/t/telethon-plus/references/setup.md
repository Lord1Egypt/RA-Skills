# telethon-plus setup

Operator-side reference: installing, logging in, and configuring the container. The agent skill itself is **consumer-only**: it talks to an already-running, already-logged-in instance and never provisions or authenticates an account.

## Deployment guidance (read before exposing this anywhere)

- **Bind to localhost, or put TLS in front of it.** Don't expose `TELETHON_HTTP_LISTEN_ADDRESS` on `0.0.0.0` to an untrusted network without a reverse proxy terminating TLS (see "Public Access via Reverse Proxy" below).
- **Set `TELETHON_AUTH_KEY`.** Unset/empty = every route except `/healthz` and `/metrics` is wide open to anyone who can reach the port.
- **Never expose `/mcp/` or `/api/` to untrusted agents or networks.** Both surfaces grant full read/write/admin control of a real Telegram account. Treat them like you'd treat exposing a database or a cloud credential, not like a public API.

## Requirements

- Docker.
- A Telegram **API ID** and **API HASH** from <https://my.telegram.org/apps> (one-time, per Telegram account).
- A **string session** minted once via the interactive login flow (`make login`). This proves the human once (phone number, SMS code, optionally 2FA), then never again.
- Outbound network to Telegram's MTProto servers.

> **The session string is full account access.** Whoever holds it *is* the account. Never commit it, paste it in chat, or bake it into an image. `.env` is gitignored for this reason.

## First-time login (operator)

Login is interactive and happens **once**, outside the agent. It writes a `TELETHON_SESSION` string you then hand to the running container.

With the repo (writes the session straight into `.env`):

```bash
cp .env.example .env
$EDITOR .env            # set TELETHON_API_ID and TELETHON_API_HASH
make login              # interactive: phone → SMS code → optional 2FA
make run                # run locally on :8080
```

Without the repo:

```bash
docker run --rm -it \
  -e TELETHON_API_ID=123456 \
  -e TELETHON_API_HASH=your-api-hash \
  psyb0t/telethon-plus login
```

Copy the printed session string and set it as `TELETHON_SESSION` on the server container.

## Quick Install

`docker run`:

```bash
docker run -d --name telethon-plus \
  -p 8080:8080 \
  -e TELETHON_API_ID=123456 \
  -e TELETHON_API_HASH=your-api-hash \
  -e TELETHON_SESSION='1Aa...long-string-from-login...' \
  -v $HOME/telethon-cache:/cache \
  --restart unless-stopped \
  psyb0t/telethon-plus
```

`docker compose`:

```yaml
services:
  telethon-plus:
    image: psyb0t/telethon-plus
    ports:
      - "8080:8080"
    environment:
      TELETHON_API_ID: "123456"
      TELETHON_API_HASH: "your-api-hash"
      TELETHON_SESSION: "1Aa...long-string-from-login..."
      # TELETHON_AUTH_KEY: "a-strong-random-secret"
      # TELETHON_POST_TO_URL: "https://your-app.example/hook"
    volumes:
      - ./telethon-cache:/cache
    restart: unless-stopped
```

Mount `/cache` as a host volume so the persistent entity cache survives restarts (the container declares `VOLUME ["/cache"]` and runs as a non-root `telethon-plus` user, UID 1000).

**Verify:** `curl http://localhost:8080/healthz` returns `{"status": "ok", "authorized": true}`.

## Environment Variables

### Required

| Var | Notes |
|---|---|
| `TELETHON_API_ID` | API ID from my.telegram.org |
| `TELETHON_API_HASH` | API hash from my.telegram.org |
| `TELETHON_SESSION` | StringSession from the login flow |

### Auth + bind

| Var | Default | Notes |
|---|---|---|
| `TELETHON_AUTH_KEY` | `""` (no auth) | When set, `Authorization: Bearer <key>` required on every route except `/healthz` and `/metrics`; WS takes it as `?token=`. Empty = wide open: every route including `/mcp/` and `/api/` is reachable by anyone who can reach the port. Set this before exposing the container beyond a fully trusted, private network. |
| `TELETHON_HTTP_LISTEN_ADDRESS` | `0.0.0.0:8080` | `host:port` to bind inside the container. |

### Client identity + behavior

| Var | Default | Notes |
|---|---|---|
| `TELETHON_LOG_LEVEL` | `INFO` | `DEBUG` / `INFO` / `WARNING` / `ERROR` / `CRITICAL` |
| `TELETHON_LOG_JSON` | `false` | JSON-structured logs |
| `TELETHON_REQUEST_TIMEOUT` | `60` | Per-request timeout (seconds) |
| `TELETHON_FLOOD_SLEEP_THRESHOLD` | `60` | Auto-sleep through `FLOOD_WAIT` errors up to this many seconds; a longer one answers 429 |
| `TELETHON_DEVICE_MODEL` | `docker-telethon-plus` | Device string Telegram sees |
| `TELETHON_SYSTEM_VERSION` | `1.0` | OS string |
| `TELETHON_APP_VERSION` | `1.0` | App version string |
| `TELETHON_PROXY` | `""` | `socks5://`, `socks4://` or `http://` as `scheme://[user:password@]host:port`; an invalid value stops startup |
| `TELETHON_DOWNLOAD_DIR` | `/tmp/telethon-plus` | Scratch dir for `send_file` uploads |
| `TELETHON_METRICS_ENABLED` | `true` | Expose `GET /metrics` |

### Safety switches

| Var | Default | Notes |
|---|---|---|
| `TELETHON_READ_ONLY` | `false` | `true` → every write endpoint returns `403`; reads/status/metrics still work. Panic killswitch, or to keep a test deployment harmless. |
| `TELETHON_DRY_RUN` | `false` | `true` → writes are validated but not sent to Telegram; response echoes `{"dry_run": true, "would_...": {...}}`. |

### Throttling & entity cache (anti-flood, defaults are conservative)

| Var | Default | Notes |
|---|---|---|
| `TELETHON_THROTTLE_ENABLED` | `true` | Master switch for all rate-limiting below |
| `TELETHON_THROTTLE_GLOBAL_INTERVAL_MS` | `50` | Min gap between any two outgoing requests |
| `TELETHON_THROTTLE_JITTER_MS` | `200` | Random jitter of 0 up to this many ms on top (breaks metronome patterns) |
| `TELETHON_THROTTLE_PER_CHAT_INTERVAL_MS` | `1100` | Min gap between sends to the same chat |
| `TELETHON_THROTTLE_PER_CHAT_READ_INTERVAL_MS` | `250` | Min gap between reads from the same chat |
| `TELETHON_THROTTLE_ADAPTIVE` | `true` | Each `FLOOD_WAIT` in the last hour doubles the global and per-chat gaps (up to 64x); each one stops counting an hour after it happened |
| `TELETHON_BUCKET_RESOLVE_PER_MIN` | `5` | Cap on `resolveUsername`, the main thing that gets accounts banned |
| `TELETHON_BUCKET_GET_FULL_PER_MIN` | `10` | Cap on `getFullChannel` (linked-chat lookups) / `get_participants` |
| `TELETHON_BUCKET_JOIN_PER_HOUR` | `5` | Cap on channel/group joins |
| `TELETHON_BUCKET_CREATE_PER_HOUR` | `5` | Cap on channel/group creation |
| `TELETHON_BUCKET_SEND_PER_MIN` | `20` | Cap on sends across all chats |
| `TELETHON_BUCKET_READ_PER_MIN` | `600` | Cap on read ops (counted per server-side API call) |
| `TELETHON_CACHE_ENABLED` | `true` | Persist resolved entities to disk |
| `TELETHON_CACHE_PATH` | `/cache/entities.json` | Mount `/cache` to keep across rebuilds |
| `TELETHON_CACHE_TTL_SECONDS` | `604800` | 7 days; `0` = no expiry |

### Updates / webhook

| Var | Default | Notes |
|---|---|---|
| `TELETHON_UPDATES_ENABLED` | `true` | Register incoming-event handlers and expose `/ws/updates` |
| `TELETHON_UPDATES_BUFFER_SIZE` | `256` | Per-subscriber WS queue depth; a client that falls this far behind is closed with code 1013 and must reconnect and catch up with `GET /api/messages` |
| `TELETHON_POST_TO_URL` | `""` | Outbound webhook: every incoming event is `POST`ed here as JSON (in addition to WS). Empty = disabled. **Data exfiltration warning:** once set, EVERY incoming message's content, sender metadata, and account activity is forwarded to this URL, indefinitely, for as long as the container runs. Use only a trusted HTTPS endpoint you control, never a third party's URL. |
| `TELETHON_POST_TO_TIMEOUT` | `10` | Webhook POST timeout (seconds) |

## Ports

| Port | Service |
|---|---|
| 8080 | HTTP API + MCP (`/mcp/`) + WebSocket (`/ws/updates`), one port |

The container binds `0.0.0.0:8080` by default (override with `TELETHON_HTTP_LISTEN_ADDRESS`). Control host exposure with `-p` at `docker run` time:

- `-p 127.0.0.1:8080:8080`: loopback-only on the host.
- `-p 8080:8080`: all host interfaces.

## Management

```bash
docker logs -f telethon-plus            # tail logs
docker stop telethon-plus               # stop
docker rm telethon-plus                 # remove
docker pull psyb0t/telethon-plus        # update

curl -s http://localhost:8080/healthz | jq              # liveness + authorized state
curl -s http://localhost:8080/api/throttle/status | jq  # live rate-limit + cache state
```

If the container isn't responding on `/healthz`, the session is likely dead: an unauthorized `TELETHON_SESSION` makes the process exit at startup rather than serve a degraded `authorized: false`. Check `docker logs`, then re-run the login flow and update `TELETHON_SESSION`.

## Public Access via Reverse Proxy (optional)

The container binds inside the container only. For public exposure, terminate TLS at a reverse proxy (Caddy / Traefik / nginx) and **also** set `TELETHON_AUTH_KEY` on the container so the app still requires a bearer even if the proxy is misconfigured. Don't rely on the proxy alone.

```caddy
telethon.example.com {
    reverse_proxy localhost:8080
}
```

## OpenClaw / ClawHub Config

```bash
export TELETHON_PLUS_URL=http://localhost:8080
export TELETHON_AUTH_KEY=<key>   # only if the server requires it
```

Or via `~/.openclaw/openclaw.json`:

```json
{
  "skills": {
    "entries": {
      "telethon-plus": {
        "env": {
          "TELETHON_PLUS_URL": "http://localhost:8080",
          "TELETHON_AUTH_KEY": "<key>"
        }
      }
    }
  }
}
```
