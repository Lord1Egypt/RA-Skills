#!/usr/bin/env bash
# Uninstall webchat-voice-input: removes hook, UI injection, workspace files
set -euo pipefail

WORKSPACE="${WORKSPACE:-$HOME/.openclaw/workspace}"
VOICE_DIR="$WORKSPACE/voice-input"
if [[ -n "${OPENCLAW_UI_DIR:-}" ]]; then
  UI_DIR="$OPENCLAW_UI_DIR"
else
  UI_DIR="$(npm -g root 2>/dev/null || echo '')/openclaw/dist/control-ui"
fi
INDEX="$UI_DIR/index.html"
ASSET_DIR="$UI_DIR/assets"
HOOK_DIR="$HOME/.openclaw/hooks/voice-input-inject"

echo "=== Uninstalling webchat-voice-input ==="

# 1) Remove gateway startup hook
echo "[1/3] Removing gateway hook..."
if [[ -d "$HOOK_DIR" ]]; then
  rm -rf "$HOOK_DIR"
  echo "      removed: $HOOK_DIR"
else
  echo "      not found (skipped)."
fi

# 2) Remove voice-input.js from Control UI and undo index.html injection
echo "[2/3] Reverting Control UI..."
if [[ -f "$ASSET_DIR/voice-input.js" ]]; then
  rm -f "$ASSET_DIR/voice-input.js"
  echo "      removed: voice-input.js asset"
fi

if [[ -f "$INDEX" ]] && grep -q 'voice-input.js' "$INDEX"; then
  sed -i '/voice-input\.js/d' "$INDEX"
  echo "      removed script tag from index.html"
else
  echo "      index.html clean (skipped)."
fi

# 3) Remove workspace runtime files (voice-input.js, i18n.json)
echo "[3/3] Removing workspace runtime files..."
rm -f "$VOICE_DIR/voice-input.js" "$VOICE_DIR/i18n.json"
rmdir "$VOICE_DIR" 2>/dev/null && echo "      removed: $VOICE_DIR" || true

# Restart gateway
openclaw gateway restart >/dev/null 2>&1 || true

echo ""
echo "=== Uninstall complete ==="
echo ""
echo "The HTTPS proxy and faster-whisper backend were NOT touched."
echo "Uninstall those separately via their own skills."
