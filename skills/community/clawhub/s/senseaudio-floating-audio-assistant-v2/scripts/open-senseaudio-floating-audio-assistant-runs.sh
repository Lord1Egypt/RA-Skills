#!/bin/bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=common.sh
source "$SCRIPT_DIR/common.sh"
RUNS_DIR="$WORKSPACE_DIR/state/realtime_interpreter/runs"

mkdir -p "$RUNS_DIR"
open "$RUNS_DIR"
echo "Opened SenseAudio floating audio assistant runs: $RUNS_DIR"
