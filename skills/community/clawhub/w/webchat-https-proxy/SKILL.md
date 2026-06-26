---
name: webchat-https-proxy
description: >
  HTTPS/WSS reverse proxy for OpenClaw WebChat Control UI. Serves the Control UI
  over HTTPS with TLS cert management, proxies WebSocket connections to the
  gateway, and forwards /transcribe requests to the local faster-whisper endpoint.
  Runs as a user systemd service. Pure infrastructure — no voice-specific UI logic.
  Keywords: HTTPS proxy, WSS, TLS, reverse proxy, Control UI, systemd service,
  self-signed certificate, WebSocket proxy.
requires:
  config_paths:
    - ~/.openclaw/openclaw.json (appends allowedOrigins entry)
  modified_paths:
    - ~/.config/systemd/user/openclaw-voice-https.service (creates unit)
    - ~/.openclaw/workspace/voice-input/https-server.py (copies runtime file)
    - ~/.openclaw/workspace/voice-input/certs/ (generates self-signed TLS cert)
  env:
    - VOICE_HTTPS_PORT (optional, default: 8443)
    - VOICE_HOST (optional, default: 127.0.0.1 — set to a LAN IP to expose externally)
    - VOICE_ALLOWED_ORIGIN (optional, default: https://<VOICE_HOST>:<VOICE_HTTPS_PORT>)
  persistence:
    - "User systemd service: openclaw-voice-https.service (HTTPS/WSS proxy)"
  privileges: user-level only, no root/sudo required
  dependencies:
    - python3 with aiohttp >= 3.9.0 (pip)
    - openssl (for self-signed cert generation)
---

# WebChat HTTPS Proxy

Standalone HTTPS/WSS reverse proxy for OpenClaw WebChat Control UI:
- Serves the Control UI over HTTPS (default port 8443)
- WebSocket passthrough to gateway (`ws://127.0.0.1:18789`)
- `/transcribe` proxy endpoint to local faster-whisper service (same-origin browser auth; optional Bearer fallback)
- Self-signed TLS certificate management
- SPA fallback for Control UI routing
- Path traversal protection for static file serving

## Deploy

```bash
bash scripts/deploy.sh
```

Or expose on LAN:
```bash
VOICE_HOST=10.0.0.42 VOICE_HTTPS_PORT=8443 bash scripts/deploy.sh
```

This script is idempotent.

## Quick verify

```bash
bash scripts/status.sh
```

## Security Notes

### Network isolation
- **Localhost by default**: Binds to `127.0.0.1` only. Not reachable from other devices unless `VOICE_HOST` is explicitly set.
- **LAN access opt-in**: Setting `VOICE_HOST=<LAN-IP>` enables trusted LAN access. Re-deploys preserve the existing configured bind host unless you explicitly override `VOICE_HOST`.
- **CORS**: Single allowed origin only (`VOICE_ALLOWED_ORIGIN`). Validated at startup — wildcards (`*`) and malformed origins are rejected.

### TLS
- **TLS 1.2+ enforced**: Minimum protocol version set to TLS 1.2. Legacy SSL/TLS 1.0/1.1 rejected.
- **Self-signed TLS**: Auto-generated certificate. Browser certificate warning on first access.
- **Private key permissions**: `chmod 600` on TLS key file.

### Authentication
- **Bearer token auth**: `/transcribe` endpoint validates Bearer token against gateway auth token using constant-time comparison (`hmac.compare_digest`).
- When no gateway token is configured, auth is skipped (safe for localhost-only).

### Input validation
- **Upload size limit**: 50 MB hard limit on `/transcribe` proxy requests (HTTP 413).
- **Empty body rejection**: HTTP 400 for empty requests.
- **Response size limit**: 10 MB cap on upstream response to prevent memory exhaustion.
- **Path traversal protection**: Static file serving resolves symlinks (`os.path.realpath`) and validates the resolved path stays within the Control UI directory.

### Error handling
- **No exception leaking**: Error responses return generic messages, not internal exception details.
- **Upstream timeout**: 120s timeout on transcription backend requests.

### SSRF protection
- Upstream URLs (`VOICE_TRANSCRIBE_URL`, `VOICE_GATEWAY_WS`) are validated to point to localhost only. Non-localhost targets are rejected at startup.

### No data exfiltration
- No outbound network calls. Proxy only connects to localhost services.
- No telemetry, analytics, or phone-home behavior.

### Persistence
- User systemd service starts on boot. Use `uninstall.sh` to fully revert.

## What this skill modifies

| What | Path | Action |
|---|---|---|
| Gateway config | `~/.openclaw/openclaw.json` | Adds HTTPS origin to `gateway.controlUi.allowedOrigins` |
| Systemd service | `~/.config/systemd/user/openclaw-voice-https.service` | Creates + enables persistent HTTPS proxy |
| Runtime file | `~/.openclaw/workspace/voice-input/https-server.py` | Copies proxy server |
| TLS certs | `~/.openclaw/workspace/voice-input/certs/` | Auto-generated self-signed cert on first run |

## Uninstall

```bash
bash scripts/uninstall.sh
```

## Common fixes

- `404 /chat?...` → SPA fallback missing in HTTPS proxy.
- `origin not allowed` → ensure deploy used correct `VOICE_HOST` and added matching HTTPS origin to `gateway.controlUi.allowedOrigins`.
- `token missing` → open URL with `?token=...` once.
- `pairing required` → approve pending device via `openclaw devices approve <requestId> --token <gateway-token>`.

ces approve <requestId> --token <gateway-token>`.

