#!/bin/bash
# text-case-converter: Convert text in a file to upper, lower, or title case
# Arguments: FILE_PATH (required), CASE (optional: upper|lower|title, default: upper)
# Usage: bash run.sh <FILE_PATH> [CASE]
# Output: Converted text with status indicator

set -euo pipefail

if [ $# -lt 1 ] || [ $# -gt 2 ]; then
  echo "ERROR: Expected 1-2 arguments: <FILE_PATH> [CASE]"
  echo "Usage: bash run.sh <FILE_PATH> [upper|lower|title]"
  exit 1
fi

FILE_PATH="$1"
CASE="${2:-upper}"

if [ ! -f "$FILE_PATH" ]; then
  echo "ERROR: File not found: $FILE_PATH"
  exit 1
fi

case "$CASE" in
  upper|lower|title) ;;
  *)
    echo "ERROR: CASE must be 'upper', 'lower', or 'title', got: $CASE"
    exit 1
    ;;
esac

echo "FILE: $FILE_PATH"
echo "CASE: $CASE"
echo "---"

if [ "$CASE" = "upper" ]; then
  tr '[:lower:]' '[:upper:]' < "$FILE_PATH"
elif [ "$CASE" = "lower" ]; then
  tr '[:upper:]' '[:lower:]' < "$FILE_PATH"
elif [ "$CASE" = "title" ]; then
  awk '{for(i=1;i<=NF;i++){$i=toupper(substr($i,1,1)) tolower(substr($i,2))}}1' "$FILE_PATH"
fi

echo "---"
echo "STATUS: OK"
