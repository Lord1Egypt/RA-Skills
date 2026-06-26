#!/usr/bin/env bash
set -euo pipefail

WORKSPACE="${WORKSPACE:-$HOME/.openclaw/workspace}"
SKILLS_DIR="${SKILLS_DIR:-$WORKSPACE/skills}"

BACKEND_STATUS="$SKILLS_DIR/faster-whisper-local-service/scripts/status.sh"
PROXY_STATUS="$SKILLS_DIR/webchat-https-proxy/scripts/status.sh"
GUI_STATUS="$SKILLS_DIR/webchat-voice-gui/scripts/status.sh"

echo "=== [full-stack] Backend status ==="
if [[ -f "$BACKEND_STATUS" ]]; then
  bash "$BACKEND_STATUS"
else
  echo "  faster-whisper-local-service not installed."
fi

echo ""
echo "=== [full-stack] HTTPS Proxy status ==="
if [[ -f "$PROXY_STATUS" ]]; then
  bash "$PROXY_STATUS"
else
  echo "  webchat-https-proxy not installed."
fi

echo ""
echo "=== [full-stack] Voice GUI status ==="
if [[ -f "$GUI_STATUS" ]]; then
  bash "$GUI_STATUS"
else
  echo "  webchat-voice-gui not installed."
fi

echo ""
echo "=== [full-stack] status:done ==="
