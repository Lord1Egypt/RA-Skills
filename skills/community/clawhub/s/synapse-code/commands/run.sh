#!/bin/bash
# synapse-code run — 运行 Pipeline 并自动触发 auto-log

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
project_name="$1"
shift

if [ -z "$project_name" ]; then
    echo "Usage: synapse-code run <project_name> [input text]"
    echo "Example: synapse-code run my-project '实现登录功能'"
    exit 1
fi

python3 "$SCRIPT_DIR/../scripts/run_pipeline.py" "$project_name" "$@"
