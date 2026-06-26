#!/bin/bash
# word-count: Count words, lines, and characters in a file
# Arguments: FILE_PATH (required, exactly 1 argument)
# Usage: bash run.sh <FILE_PATH>
# Output: Labeled line/word/character counts, deterministic format

set -euo pipefail

if [ $# -ne 1 ]; then
  echo "ERROR: Expected exactly 1 argument: <FILE_PATH>"
  echo "Usage: bash run.sh <FILE_PATH>"
  exit 1
fi

FILE_PATH="$1"

if [ ! -f "$FILE_PATH" ]; then
  echo "ERROR: File not found: $FILE_PATH"
  exit 1
fi

LINES=$(wc -l < "$FILE_PATH")
WORDS=$(wc -w < "$FILE_PATH")
CHARS=$(wc -c < "$FILE_PATH")

echo "FILE: $FILE_PATH"
echo "LINES: $LINES"
echo "WORDS: $WORDS"
echo "BYTES: $CHARS"
echo "STATUS: OK"
