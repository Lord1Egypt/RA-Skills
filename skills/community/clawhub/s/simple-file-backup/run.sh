#!/bin/bash
# file-backup: Create a timestamped backup copy of a file
# Arguments: FILE_PATH [BACKUP_DIR] (1 required, 1 optional; 2 args max)
# Usage: bash run.sh <FILE_PATH> [BACKUP_DIR]

set -euo pipefail

if [ $# -lt 1 ] || [ $# -gt 2 ]; then
  echo "ERROR: Expected 1-2 arguments: <FILE_PATH> [BACKUP_DIR]"
  echo "Usage: bash run.sh <FILE_PATH> [BACKUP_DIR]"
  exit 1
fi

FILE_PATH="$1"
BACKUP_DIR="${2:-$(dirname "$FILE_PATH")}"

if [ ! -f "$FILE_PATH" ]; then
  echo "ERROR: File not found: $FILE_PATH"
  exit 1
fi

if [ ! -d "$BACKUP_DIR" ]; then
  echo "ERROR: Backup directory not found: $BACKUP_DIR"
  exit 1
fi

BASENAME=$(basename "$FILE_PATH")
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="$BACKUP_DIR/${BASENAME}.backup_${TIMESTAMP}"

cp "$FILE_PATH" "$BACKUP_FILE"
echo "OK: Backup created at $BACKUP_FILE"
