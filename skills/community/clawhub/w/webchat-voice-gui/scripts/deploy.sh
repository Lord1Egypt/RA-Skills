#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(cd -- "$SCRIPT_DIR/.." && pwd)"
WORKSPACE="${WORKSPACE:-$HOME/.openclaw/workspace}"
VOICE_DIR="$WORKSPACE/voice-input"
if [[ -n "${OPENCLAW_UI_DIR:-}" ]]; then
  UI_DIR="$OPENCLAW_UI_DIR"
else
  NPM_ROOT="$(npm -g root 2>/dev/null || true)"
  if [[ -z "$NPM_ROOT" ]] || [[ ! -d "$NPM_ROOT/openclaw/dist/control-ui" ]]; then
    echo "ERROR: Cannot find Control UI. Set OPENCLAW_UI_DIR or install openclaw globally." >&2
    exit 1
  fi
  UI_DIR="$NPM_ROOT/openclaw/dist/control-ui"
fi
INDEX="$UI_DIR/index.html"
ASSET_DIR="$UI_DIR/assets"

if [[ ! -f "$INDEX" ]]; then
  echo "ERROR: Control UI index.html not found at: $INDEX" >&2
  exit 1
fi

# --- Check HTTPS proxy is running ---
if ! systemctl --user is-active openclaw-voice-https.service >/dev/null 2>&1; then
  echo "WARNING: openclaw-voice-https.service is not running." >&2
  echo "         Deploy webchat-https-proxy first for HTTPS access." >&2
  echo "         Continuing anyway (voice input will work if proxy is started later)." >&2
fi

# --- Check transcription service ---
if ! systemctl --user is-active openclaw-transcribe.service >/dev/null 2>&1; then
  echo "WARNING: openclaw-transcribe.service is not running." >&2
  echo "         Deploy faster-whisper-local-service first for STT." >&2
fi

# 0) Language selection
VOICE_LANG="${VOICE_LANG:-}"
if [[ -z "$VOICE_LANG" ]] && [[ -t 0 ]]; then
  echo ""
  echo "Available UI languages: auto (browser default), en, de, zh"
  read -r -p "Choose UI language [auto]: " VOICE_LANG
fi
VOICE_LANG="${VOICE_LANG:-auto}"

if ! [[ "$VOICE_LANG" =~ ^([a-zA-Z]{2,5}(-[a-zA-Z]{2,5})?|auto)$ ]]; then
  echo "ERROR: VOICE_LANG must be a language code (en, de, en-US, zh) or 'auto', got: $VOICE_LANG" >&2
  exit 1
fi

mkdir -p "$VOICE_DIR"

# 1) Copy bundled assets from skill -> workspace runtime dir
cp -f "$SKILL_DIR/assets/voice-input.js" "$VOICE_DIR/voice-input.js"
cp -f "$SKILL_DIR/assets/i18n.json" "$VOICE_DIR/i18n.json" 2>/dev/null || true

# Patch default language into voice-input.js if not auto
if [[ "$VOICE_LANG" != "auto" && -n "$VOICE_LANG" ]]; then
  sed -i "/const LANG_KEY = 'oc-voice-lang';/a\\
  const DEFAULT_LANG = '${VOICE_LANG}';" "$VOICE_DIR/voice-input.js"
  sed -i "s|const nav = (navigator.language || 'en').slice(0, 2);|const nav = DEFAULT_LANG || (navigator.language || 'en').slice(0, 2);|" "$VOICE_DIR/voice-input.js"
  echo "UI language set to: ${VOICE_LANG}"
else
  echo "UI language: auto-detect (browser default)"
fi

# 2) Deploy voice-input asset + inject index (idempotent)
mkdir -p "$ASSET_DIR"
cp -f "$VOICE_DIR/voice-input.js" "$ASSET_DIR/voice-input.js"

if ! grep -q 'voice-input.js' "$INDEX"; then
  sed -i 's|</body>|    <script src="./assets/voice-input.js"></script>\n  </body>|' "$INDEX"
fi

# 3) Install gateway startup hook (survives openclaw update)
HOOK_DIR="$HOME/.openclaw/hooks/voice-input-inject"
mkdir -p "$HOOK_DIR"
cp -f "$SKILL_DIR/hooks/handler.ts" "$HOOK_DIR/handler.ts"
cp -f "$SKILL_DIR/hooks/inject.sh" "$HOOK_DIR/inject.sh"
cp -f "$SKILL_DIR/hooks/HOOK.md" "$HOOK_DIR/HOOK.md"
chmod +x "$HOOK_DIR/inject.sh"
echo "hook installed: $HOOK_DIR"

# 4) Restart gateway so injection hook applies cleanly
openclaw gateway restart >/dev/null 2>&1 || true

echo "deploy:ok"
