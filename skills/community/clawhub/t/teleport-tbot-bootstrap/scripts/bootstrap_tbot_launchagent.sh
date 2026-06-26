#!/usr/bin/env bash
set -euo pipefail

# Bootstrap persistent tbot identity refresh via macOS LaunchAgent.
# Usage:
#   bootstrap_tbot_launchagent.sh --proxy teleport.example.com:443 --token <token> [--join-method bound_keypair] [--bot-name openclaw-bot] [--out-dir ~/.openclaw/workspace/tbot]

JOIN_METHOD="bound_keypair"
OUT_DIR="${HOME}/.openclaw/workspace/tbot"
BOT_NAME="openclaw-bot"
PROXY=""
TOKEN=""
REGISTRATION_SECRET=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --proxy) PROXY="$2"; shift 2;;
    --token) TOKEN="$2"; shift 2;;
    --registration-secret) REGISTRATION_SECRET="$2"; shift 2;;
    --join-method) JOIN_METHOD="$2"; shift 2;;
    --bot-name) BOT_NAME="$2"; shift 2;;
    --out-dir) OUT_DIR="$2"; shift 2;;
    *) echo "Unknown arg: $1" >&2; exit 1;;
  esac
done

command -v tbot >/dev/null || { echo "tbot not found" >&2; exit 1; }
command -v tsh >/dev/null || { echo "tsh not found" >&2; exit 1; }

if [[ -z "$PROXY" ]]; then
  echo "--proxy is required" >&2
  exit 1
fi

if [[ -z "$TOKEN" && -z "$REGISTRATION_SECRET" ]]; then
  echo "Provide either --token or --registration-secret" >&2
  exit 1
fi

STATE_DIR="${OUT_DIR}/state"
CONF_PATH="${OUT_DIR}/tbot.yaml"
IDENTITY_PATH="${OUT_DIR}/identity"
PLIST_PATH="${HOME}/Library/LaunchAgents/com.openclaw.tbot.plist"
LABEL="com.openclaw.tbot"

mkdir -p "$OUT_DIR" "$STATE_DIR" "${HOME}/Library/LaunchAgents"

CFG=(
  tbot configure identity
  --output "$CONF_PATH"
  --destination "file://${OUT_DIR}"
  --storage "file://${STATE_DIR}"
  --proxy-server "$PROXY"
  --join-method "$JOIN_METHOD"
)

if [[ -n "$TOKEN" ]]; then
  CFG+=(--token "$TOKEN")
fi
if [[ -n "$REGISTRATION_SECRET" ]]; then
  CFG+=(--registration-secret "$REGISTRATION_SECRET")
fi

"${CFG[@]}"

cat > "$PLIST_PATH" <<PLIST
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key><string>${LABEL}</string>
  <key>ProgramArguments</key>
  <array>
    <string>$(command -v tbot)</string>
    <string>start</string>
    <string>-c</string>
    <string>${CONF_PATH}</string>
  </array>
  <key>RunAtLoad</key><true/>
  <key>KeepAlive</key><true/>
  <key>StandardOutPath</key><string>${OUT_DIR}/tbot.stdout.log</string>
  <key>StandardErrorPath</key><string>${OUT_DIR}/tbot.stderr.log</string>
  <key>WorkingDirectory</key><string>${OUT_DIR}</string>
</dict>
</plist>
PLIST

launchctl bootout "gui/$(id -u)/${LABEL}" >/dev/null 2>&1 || true
launchctl bootstrap "gui/$(id -u)" "$PLIST_PATH"
launchctl kickstart -k "gui/$(id -u)/${LABEL}"

sleep 2

if [[ ! -s "$IDENTITY_PATH" ]]; then
  echo "Identity file not created yet at: $IDENTITY_PATH" >&2
  exit 2
fi

# quick smoke test (can fail if RBAC has no node access; still useful signal)
set +e
tsh -i "$IDENTITY_PATH" --proxy="$PROXY" ls >/tmp/tbot-smoke.out 2>/tmp/tbot-smoke.err
RC=$?
set -e

echo "Configured: $CONF_PATH"
echo "LaunchAgent: $PLIST_PATH"
echo "Identity: $IDENTITY_PATH"
echo "Smoke test exit: $RC"
if [[ $RC -ne 0 ]]; then
  echo "Smoke stderr:"
  sed -n '1,60p' /tmp/tbot-smoke.err
fi
