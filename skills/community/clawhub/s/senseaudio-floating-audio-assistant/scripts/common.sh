#!/bin/bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
WORKSPACE_DIR="$(cd "$SKILL_DIR/../.." && pwd)"
TOOL_DIR="$WORKSPACE_DIR/tools/realtime_interpreter"
STATE_DIR="$WORKSPACE_DIR/state/realtime_interpreter"
