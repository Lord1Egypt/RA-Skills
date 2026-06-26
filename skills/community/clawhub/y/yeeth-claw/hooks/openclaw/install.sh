#!/usr/bin/env bash
# OpenClaw install script
# Copies the hook to ~/.claude/hooks/openclaw and merges settings into
# ~/.claude/settings.json (or ~/.claude/settings.local.json).

set -euo pipefail

HOOK_DIR="$HOME/.claude/hooks/openclaw"
SETTINGS="$HOME/.claude/settings.json"

echo "Installing OpenClaw to $HOOK_DIR..."
mkdir -p "$HOOK_DIR/lib"
cp hook.py "$HOOK_DIR/hook.py"
cp lib/registry.py "$HOOK_DIR/lib/registry.py"
cp lib/typosquat.py "$HOOK_DIR/lib/typosquat.py"
cp lib/argus.py "$HOOK_DIR/lib/argus.py"
cp lib/__init__.py "$HOOK_DIR/lib/__init__.py"
chmod +x "$HOOK_DIR/hook.py"

echo ""
echo "Hook installed. Add the following to $SETTINGS under \"hooks\":"
echo ""
cat settings.json
echo ""

# Optional: if jq is available, attempt to merge automatically
if command -v jq &>/dev/null && [ -f "$SETTINGS" ]; then
  echo "Detected jq — merging settings automatically..."
  TMP=$(mktemp)
  jq --slurpfile hook settings.json \
    '.hooks.PreToolUse = ((.hooks.PreToolUse // []) + $hook[0].hooks.PreToolUse)' \
    "$SETTINGS" > "$TMP" && mv "$TMP" "$SETTINGS"
  echo "Done. Restart Claude Code for the hook to take effect."
else
  echo "Merge settings.json into $SETTINGS manually, then restart Claude Code."
fi

echo ""
echo "Optional: set environment variables to enable Argus escalation:"
echo "  export OPENCLAW_ARGUS_URL=https://app.yeethsecurity.com"
echo "  export OPENCLAW_ARGUS_KEY=<your-api-key>"
