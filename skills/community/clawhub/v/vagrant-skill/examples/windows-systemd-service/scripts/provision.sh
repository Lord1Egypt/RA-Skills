#!/usr/bin/env bash
# provision.sh — deploy a Python HTTP server as a systemd service
#
# WHY THIS NEEDS A VM (on Windows/WSL2):
#   WSL2 does not run real systemd. Even with the systemd=true setting in
#   /etc/wsl.conf, it is a compatibility shim — unit file loading, socket
#   activation, and journald behave differently from a real Linux init system.
#   This VM gives you a genuine Ubuntu 24.04 systemd (PID 1) so you can write
#   and test unit files before shipping them to production servers.
#
# What this does:
#   1. Installs Python 3 (system package — no pip needed)
#   2. Creates a 'demo' system user (no login shell, no home dir)
#   3. Creates /srv/demo with sample HTML content
#   4. Writes /etc/systemd/system/demo-http.service
#   5. Enables and starts the service
#   6. Confirms the service is active and serving HTTP
set -euo pipefail

GREEN='\033[0;32m'; YELLOW='\033[1;33m'; NC='\033[0m'
info() { echo -e "${GREEN}[provision]${NC} $*"; }
warn() { echo -e "${YELLOW}[provision]${NC} $*"; }

# ── 1. Install Python 3 ───────────────────────────────────────────────────────
info "Installing Python 3..."
export DEBIAN_FRONTEND=noninteractive
apt-get update -qq
apt-get install -y -qq python3

# ── 2. Create dedicated service user (idempotent) ────────────────────────────
if ! id -u demo > /dev/null 2>&1; then
  info "Creating 'demo' system user..."
  useradd --system --no-create-home --shell /usr/sbin/nologin demo
else
  info "User 'demo' already exists"
fi

# ── 3. Create serve directory and content ────────────────────────────────────
info "Creating /srv/demo..."
mkdir -p /srv/demo
chown demo:demo /srv/demo
chmod 755 /srv/demo

# Quoted heredoc: shellcheck does not parse the HTML body as shell
cat > /srv/demo/index.html << 'HTMLEOF'
<!DOCTYPE html>
<html>
<head><title>demo-http</title></head>
<body>
  <h1>demo-http is running under systemd</h1>
  <p>This page is served by Python http.server, managed as a systemd unit.</p>
  <p>Check status: <code>systemctl status demo-http</code></p>
  <p>View logs: <code>journalctl -u demo-http --no-pager</code></p>
</body>
</html>
HTMLEOF

chown demo:demo /srv/demo/index.html

# ── 4. Write the systemd unit file ────────────────────────────────────────────
# Design notes:
#   ExecStart: full path /usr/bin/python3 — systemd does not source login PATH
#   WorkingDirectory: /srv/demo — http.server serves the CWD; without this,
#     systemd defaults to / and http.server would serve the root filesystem
#   User/Group: run as 'demo', not root — port 8000 needs no CAP_NET_BIND_SERVICE
#   RestartSec=2s: short enough for the bats test (sleep 4) to catch the restart
#   ProtectSystem=strict + ReadWritePaths: minimal write surface for the service
#
# Quoted heredoc: shellcheck does not parse ini-style content as shell
info "Writing /etc/systemd/system/demo-http.service..."
cat > /etc/systemd/system/demo-http.service << 'UNITEOF'
[Unit]
Description=Demo Python HTTP Server
After=network.target
Wants=network.target

[Service]
Type=simple
User=demo
Group=demo
WorkingDirectory=/srv/demo
ExecStart=/usr/bin/python3 -m http.server 8000
Restart=on-failure
RestartSec=2s
StandardOutput=journal
StandardError=journal
SyslogIdentifier=demo-http
NoNewPrivileges=yes
PrivateTmp=yes
ProtectSystem=strict
ReadWritePaths=/srv/demo

[Install]
WantedBy=multi-user.target
UNITEOF

# ── 5. Enable and start the service ──────────────────────────────────────────
info "Enabling and starting demo-http..."
systemctl daemon-reload
systemctl enable demo-http
systemctl start demo-http

# ── 6. Wait for service to be ready (up to 10s) ───────────────────────────────
info "Waiting for demo-http to be ready..."
i=0
while [ "$i" -lt 10 ]; do
  i=$((i + 1))
  if curl -sf http://localhost:8000 > /dev/null 2>&1; then
    info "demo-http is serving"
    break
  fi
  if [ "$i" -eq 10 ]; then
    warn "Timeout — check: journalctl -u demo-http --no-pager"
    exit 1
  fi
  sleep 1
done

# ── 7. Confirm ────────────────────────────────────────────────────────────────
info "Service status:"
systemctl is-active demo-http

info "Listening port:"
ss -tlnp | grep ':8000' || true

info "Done. Try:"
info "  vagrant ssh -c 'systemctl status demo-http'"
info "  vagrant ssh -c 'curl http://localhost:8000'"
info "  vagrant ssh -c 'journalctl -u demo-http --no-pager'"
