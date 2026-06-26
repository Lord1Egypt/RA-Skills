#!/bin/bash

# Xiaohongshu CDP publisher wrapper
# Usage:
# run_xhs_publish.sh "title" "content"

TITLE="$1"
BODY="$2"

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

if [ -z "$TITLE" ] || [ -z "$BODY" ]; then
  echo "Usage: run_xhs_publish.sh \"title\" \"content\""
  exit 1
fi

python3 "$SCRIPT_DIR/cdp_xhs_publish.py" "$TITLE" "$BODY"
