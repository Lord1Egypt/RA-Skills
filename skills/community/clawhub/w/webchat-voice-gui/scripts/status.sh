#!/usr/bin/env bash
set -euo pipefail

if [[ -n "${OPENCLAW_UI_DIR:-}" ]]; then
  UI_DIR="$OPENCLAW_UI_DIR"
else
  UI_DIR="$(npm -g root 2>/dev/null || echo '')/openclaw/dist/control-ui"
fi

systemctl --user is-active openclaw-transcribe.service || echo 'transcribe:inactive'
grep -q 'voice-input.js' "$UI_DIR/index.html" && echo 'inject:ok' || echo 'inject:missing'
echo 'status:done'
