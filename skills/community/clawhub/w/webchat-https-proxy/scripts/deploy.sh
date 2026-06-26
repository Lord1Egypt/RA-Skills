#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(cd -- "$SCRIPT_DIR/.." && pwd)"
WORKSPACE="${WORKSPACE:-$HOME/.openclaw/workspace}"
VOICE_DIR="$WORKSPACE/voice-input"
CFG="${OPENCLAW_CONFIG_PATH:-$HOME/.openclaw/openclaw.json}"
VOICE_HTTPS_PORT="${VOICE_HTTPS_PORT:-8443}"
VOICE_HOST="${VOICE_HOST:-}"

# --- Input validation ---
if ! [[ "$VOICE_HTTPS_PORT" =~ ^[0-9]+$ ]] || (( VOICE_HTTPS_PORT < 1 || VOICE_HTTPS_PORT > 65535 )); then
  echo "ERROR: VOICE_HTTPS_PORT must be a valid port (1-65535), got: $VOICE_HTTPS_PORT" >&2
  exit 1
fi

if [[ -z "$VOICE_HOST" ]]; then
  EXISTING_UNIT="$HOME/.config/systemd/user/openclaw-voice-https.service"
  if [[ -f "$EXISTING_UNIT" ]]; then
    EXISTING_HOST="$(grep -E '^Environment=VOICE_BIND_HOST=' "$EXISTING_UNIT" | tail -n1 | sed 's/^Environment=VOICE_BIND_HOST=//')"
    if [[ -n "$EXISTING_HOST" ]]; then
      VOICE_HOST="$EXISTING_HOST"
    fi
  fi
fi

if [[ -z "$VOICE_HOST" ]]; then
  VOICE_HOST="127.0.0.1"
fi

if ! [[ "$VOICE_HOST" =~ ^[a-zA-Z0-9._-]+$ ]]; then
  echo "ERROR: VOICE_HOST contains invalid characters: $VOICE_HOST" >&2
  exit 1
fi

ALLOWED_ORIGIN="https://${VOICE_HOST}:${VOICE_HTTPS_PORT}"

mkdir -p "$VOICE_DIR"

# 1) Copy https-server.py to workspace runtime dir
cp -f "$SKILL_DIR/assets/https-server.py" "$VOICE_DIR/https-server.py"

# 2) Ensure gateway allowedOrigins contains computed origin
python3 - "$CFG" "$ALLOWED_ORIGIN" << 'PY'
import json, sys
p, origin = sys.argv[1], sys.argv[2]
with open(p, 'r', encoding='utf-8') as f:
    c = json.load(f)
g = c.setdefault('gateway', {})
cu = g.setdefault('controlUi', {})
orig = cu.setdefault('allowedOrigins', [])
if origin not in orig:
    orig.append(origin)
    with open(p, 'w', encoding='utf-8') as f:
        json.dump(c, f, indent=2, ensure_ascii=False)
        f.write('\n')
    print(f'allowedOrigin ensured: {origin}')
PY

# 3) Find python with aiohttp
PYTHON_BIN=""
if [[ -x "${WORKSPACE}/.venv-faster-whisper/bin/python" ]]; then
  PYTHON_BIN="${WORKSPACE}/.venv-faster-whisper/bin/python"
elif python3 -c "import aiohttp" 2>/dev/null; then
  PYTHON_BIN="$(command -v python3)"
else
  echo "ERROR: No python with aiohttp found. Install aiohttp: pip3 install 'aiohttp>=3.9.0'" >&2
  exit 1
fi

# Verify minimum aiohttp version (>=3.9.0)
AIOHTTP_VERSION=$("$PYTHON_BIN" -c "import aiohttp; print(aiohttp.__version__)" 2>/dev/null || echo "0.0.0")
AIOHTTP_MAJOR=$(echo "$AIOHTTP_VERSION" | cut -d. -f1)
AIOHTTP_MINOR=$(echo "$AIOHTTP_VERSION" | cut -d. -f2)
if (( AIOHTTP_MAJOR < 3 )) || (( AIOHTTP_MAJOR == 3 && AIOHTTP_MINOR < 9 )); then
  echo "ERROR: aiohttp >= 3.9.0 required, found $AIOHTTP_VERSION. Upgrade: pip3 install 'aiohttp>=3.9.0'" >&2
  exit 1
fi

# 4) Install/refresh HTTPS proxy systemd service
mkdir -p "$HOME/.config/systemd/user"
cat > "$HOME/.config/systemd/user/openclaw-voice-https.service" <<UNIT
[Unit]
Description=OpenClaw HTTPS Proxy (Control UI + WS + Transcribe)
After=network.target

[Service]
Type=simple
ExecStart="${PYTHON_BIN}" "${VOICE_DIR}/https-server.py"
Restart=always
RestartSec=2
Environment=WORKSPACE=${WORKSPACE}
Environment=VOICE_HTTPS_PORT=${VOICE_HTTPS_PORT}
Environment=VOICE_ALLOWED_ORIGIN=${ALLOWED_ORIGIN}
Environment=VOICE_BIND_HOST=${VOICE_HOST}

[Install]
WantedBy=default.target
UNIT

systemctl --user daemon-reload
systemctl --user enable --now openclaw-voice-https.service
systemctl --user restart openclaw-voice-https.service

# 5) Restart gateway so allowedOrigins applies
openclaw gateway restart >/dev/null 2>&1 || true

echo "deploy:ok host=${VOICE_HOST} port=${VOICE_HTTPS_PORT} origin=${ALLOWED_ORIGIN}"
