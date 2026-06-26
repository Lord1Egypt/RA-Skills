#!/bin/bash
# Weibo CDP 运营封装
CONTENT="$1"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
if [ -z "$CONTENT" ]; then
  echo "Usage: run_weibo_ops.sh \"content\""
  exit 1
fi
python3 "$SCRIPT_DIR/cdp_weibo_ops.py" "$CONTENT"
