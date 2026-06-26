#!/bin/bash
# file-tree: Show directory tree structure
# Arguments: [DIRECTORY] [DEPTH] (both optional; 2 args max)
# Usage: bash run.sh [DIRECTORY] [DEPTH]

set -euo pipefail

if [ $# -gt 2 ]; then
  echo "ERROR: Expected at most 2 arguments: [DIRECTORY] [DEPTH]"
  echo "Usage: bash run.sh [DIRECTORY] [DEPTH]"
  exit 1
fi

DIR_PATH="${1:-.}"
DEPTH="${2:-3}"

if [ ! -d "$DIR_PATH" ]; then
  echo "ERROR: Directory not found: $DIR_PATH"
  exit 1
fi

if ! echo "$DEPTH" | grep -qE '^[0-9]+$'; then
  echo "ERROR: DEPTH must be a positive integer, got: $DEPTH"
  exit 1
fi

find "$DIR_PATH" -maxdepth "$DEPTH" | sort | sed 's|[^/]*/|  |g'
