#!/usr/bin/env bash
# Uninstall webchat-https-proxy: removes service, gateway origin, certs, runtime files
set -euo pipefail

WORKSPACE="${WORKSPACE:-$HOME/.openclaw/workspace}"
VOICE_DIR="$WORKSPACE/voice-input"
CFG="${OPENCLAW_CONFIG_PATH:-$HOME/.openclaw/openclaw.json}"
VOICE_HTTPS_PORT="${VOICE_HTTPS_PORT:-8443}"

# Input validation
if ! [[ "$VOICE_HTTPS_PORT" =~ ^[0-9]+$ ]] || (( VOICE_HTTPS_PORT < 1 || VOICE_HTTPS_PORT > 65535 )); then
  echo "ERROR: VOICE_HTTPS_PORT must be a valid port (1-65535), got: $VOICE_HTTPS_PORT" >&2
  exit 1
fi

echo "=== Uninstalling webchat-https-proxy ==="

# 1) Stop and remove systemd service
echo "[1/4] Stopping and removing openclaw-voice-https.service..."
systemctl --user stop openclaw-voice-https.service 2>/dev/null || true
systemctl --user disable openclaw-voice-https.service 2>/dev/null || true
rm -f "$HOME/.config/systemd/user/openclaw-voice-https.service"
systemctl --user daemon-reload 2>/dev/null || true
echo "      done."

# 2) Remove HTTPS origin from gateway config
echo "[2/4] Cleaning gateway config (allowedOrigins)..."
if [[ -f "$CFG" ]]; then
  python3 - "$CFG" "$VOICE_HTTPS_PORT" << 'PY'
import json, sys
p, port = sys.argv[1], sys.argv[2]
with open(p, 'r', encoding='utf-8') as f:
    c = json.load(f)
g = c.get('gateway', {})
cu = g.get('controlUi', {})
orig = cu.get('allowedOrigins', [])
before = len(orig)
cu['allowedOrigins'] = [o for o in orig if f':{port}' not in o]
after = len(cu['allowedOrigins'])
with open(p, 'w', encoding='utf-8') as f:
    json.dump(c, f, indent=2, ensure_ascii=False)
    f.write('\n')
print(f'      removed {before - after} origin(s) from allowedOrigins')
PY
else
  echo "      config not found (skipped)."
fi

# 3) Restart gateway
echo "[3/4] Restarting gateway..."
openclaw gateway restart >/dev/null 2>&1 || true
echo "      done."

# 4) Remove TLS certs and runtime files
echo "[4/4] Removing TLS certificates and runtime files..."
CERT_DIR="$VOICE_DIR/certs"
if [[ -d "$CERT_DIR" ]]; then
  rm -rf "$CERT_DIR"
  echo "      removed: $CERT_DIR"
fi
rm -f "$VOICE_DIR/https-server.py"
rmdir "$VOICE_DIR" 2>/dev/null && echo "      removed: $VOICE_DIR" || true

echo ""
echo "=== Uninstall complete ==="
