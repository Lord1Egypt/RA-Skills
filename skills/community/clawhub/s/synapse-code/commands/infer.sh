#!/bin/bash
# synapse-code infer — 推断 task_type

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
input_text="$*"

if [ -z "$input_text" ]; then
    # Read from stdin
    python3 "$SCRIPT_DIR/../scripts/infer_task_type.py"
else
    python3 "$SCRIPT_DIR/../scripts/infer_task_type.py" "$input_text"
fi
