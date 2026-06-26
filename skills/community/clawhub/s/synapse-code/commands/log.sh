#!/bin/bash
# synapse-code log — 手动触发 Synapse auto-log

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
project_path="${1:-.}"

python3 "$SCRIPT_DIR/../scripts/auto_log_trigger.py" "$project_path"
