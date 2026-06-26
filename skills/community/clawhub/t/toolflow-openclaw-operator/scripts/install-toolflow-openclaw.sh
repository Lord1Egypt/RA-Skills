#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
PLUGIN_PATH="$SKILL_DIR/toolflow-bundle/plugin"

if ! command -v openclaw >/dev/null 2>&1; then
  echo "openclaw CLI not found in PATH." >&2
  exit 1
fi

if [[ ! -f "$PLUGIN_PATH/openclaw.plugin.json" ]]; then
  echo "Bundled ToolFlow plugin manifest not found at: $PLUGIN_PATH" >&2
  exit 1
fi

echo "Installing bundled ToolFlow plugin from: $PLUGIN_PATH"
openclaw plugins install --link "$PLUGIN_PATH"

echo
echo "Running ToolFlow doctor check..."
node "$PLUGIN_PATH/dist/runtime-cli.js" doctor

echo
echo "ToolFlow bundle installed."
