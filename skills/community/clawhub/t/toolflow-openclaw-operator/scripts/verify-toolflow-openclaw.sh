#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
PLUGIN_PATH="$SKILL_DIR/toolflow-bundle/plugin"
RUNTIME_MAIN="$PLUGIN_PATH/dist/runtime-cli.js"
WORKFLOW="$PLUGIN_PATH/examples/workflows/safe-profile-mvp.json"

node "$RUNTIME_MAIN" doctor
node "$RUNTIME_MAIN" validate "$WORKFLOW"

echo "ToolFlow bundle verification complete."
