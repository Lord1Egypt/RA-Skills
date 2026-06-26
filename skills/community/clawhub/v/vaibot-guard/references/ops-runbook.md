# VAIBot Guard — Ops Runbook

This runbook describes how to run `vaibot-guard-service.mjs` as a service.

CLI usage note: do not assume an executable shim exists. Use:

```bash
node scripts/vaibot-guard.mjs <command> ...
```

Two options are provided:
- **Local workstation mode (recommended):** user service (`systemctl --user`)
- **VPS / production mode:** system service (`sudo systemctl`) — **templates are not shipped in the ClawHub skill artifact**; generate/copy your own unit file (see notes below).

## Shared environment variables

Retention:
- `VAIBOT_LOG_RETENTION_DAYS` (default 14): remove guard log/state files in `VAIBOT_GUARD_LOG_DIR` older than this many days.

Common env vars (see `SKILL.md` for full list):
- `VAIBOT_GUARD_HOST` (default `127.0.0.1`)
- `VAIBOT_GUARD_PORT` (default `39111`)
- `VAIBOT_GUARD_TOKEN` (recommended)
- `VAIBOT_POLICY_PATH` (default `references/policy.default.json`)
- `VAIBOT_GUARD_LOG_DIR` (default `${VAIBOT_WORKSPACE}/.vaibot-guard`)
- `VAIBOT_API_URL`, `VAIBOT_API_KEY`, `VAIBOT_PROVE_MODE`

## Option A — User service (recommended)

### Install

Recommended: generate the user unit + env file via the built-in helper (does not rely on shipping any `.service` files in the skill artifact):

```bash
node scripts/vaibot-guard.mjs install-local
```

Then enable/start (if you didn’t choose that in the installer):

```bash
systemctl --user daemon-reload
systemctl --user enable --now vaibot-guard
systemctl --user status vaibot-guard
```

Notes:
- The installer writes:
  - `~/.config/systemd/user/vaibot-guard.service`
  - `~/.config/vaibot-guard/vaibot-guard.env` (recommended `chmod 600`)
- Systemd templates are provided under `references/systemd/` for reference; do not assume `.service` files ship in the ClawHub artifact.

### Logs

```bash
journalctl --user -u vaibot-guard -f
```

### Run at boot (optional)

If you want the user service to run when you are not logged in:

```bash
loginctl enable-linger $USER
```

## Option B — System service (VPS/production)

We intentionally **do not ship** `systemd/system/*` unit files in the ClawHub skill artifact (scanner/persistence concerns).

If you need a system-wide service on a VPS/production host, use this as a starting point:

1) Create a dedicated user:

```bash
sudo useradd --system --create-home --home-dir /var/lib/vaibot-guard --shell /usr/sbin/nologin vaibot-guard
```

2) Create `/etc/vaibot-guard/vaibot-guard.env` and set required env vars (at minimum `VAIBOT_GUARD_TOKEN`, `VAIBOT_POLICY_PATH`, `VAIBOT_GUARD_LOG_DIR`).

3) Create a unit file (example skeleton):

```ini
[Unit]
Description=VAIBot Guard policy service
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=vaibot-guard
WorkingDirectory=/var/lib/vaibot-guard
EnvironmentFile=/etc/vaibot-guard/vaibot-guard.env
ExecStart=/usr/bin/env node /path/to/vaibot-guard/scripts/vaibot-guard-service.mjs
Restart=on-failure
RestartSec=2

[Install]
WantedBy=multi-user.target
```

4) Enable + start:

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now vaibot-guard
sudo systemctl status vaibot-guard
```

Logs:

```bash
sudo journalctl -u vaibot-guard -f
```
