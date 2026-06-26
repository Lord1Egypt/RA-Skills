#!/bin/bash
# synapse-code status — 检查项目 Synapse + Pipeline 状态

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
project_path="${1:-.}"

python3 "$SCRIPT_DIR/../scripts/check_status.py" "$project_path"
