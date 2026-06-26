#!/bin/bash
# text-search: Search for text pattern in files within a directory
# Arguments: PATTERN [DIRECTORY] (1 required, 1 optional; 2 args max)
# Usage: bash run.sh <PATTERN> [DIRECTORY]

set -euo pipefail

if [ $# -lt 1 ] || [ $# -gt 2 ]; then
  echo "ERROR: Expected 1-2 arguments: <PATTERN> [DIRECTORY]"
  echo "Usage: bash run.sh <PATTERN> [DIRECTORY]"
  exit 1
fi

PATTERN="$1"
DIR_PATH="${2:-.}"

if [ ! -d "$DIR_PATH" ]; then
  echo "ERROR: Directory not found: $DIR_PATH"
  exit 1
fi

echo "Searching for '$PATTERN' in $DIR_PATH:"
echo "---"
grep -rn "$PATTERN" "$DIR_PATH" 2>/dev/null || echo "No matches found."
