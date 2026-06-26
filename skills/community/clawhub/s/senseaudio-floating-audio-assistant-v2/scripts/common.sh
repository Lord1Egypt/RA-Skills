#!/bin/bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
WORKSPACE_DIR="$(cd "$SKILL_DIR/../.." && pwd)"
BUNDLED_TOOL_DIR="$SKILL_DIR/runtime/realtime_interpreter"
EXTERNAL_TOOL_DIR="$WORKSPACE_DIR/tools/realtime_interpreter"
if [ -d "$BUNDLED_TOOL_DIR" ]; then
  TOOL_DIR="$BUNDLED_TOOL_DIR"
else
  TOOL_DIR="$EXTERNAL_TOOL_DIR"
fi
STATE_DIR="$WORKSPACE_DIR/state/realtime_interpreter"
