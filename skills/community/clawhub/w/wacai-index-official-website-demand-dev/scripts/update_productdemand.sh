#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="${1:-}"
INPUT_FILE="${2:-}"
DEMAND_FILE_NAME="${3:-productdemand.md}"

if [[ -z "$PROJECT_DIR" || -z "$INPUT_FILE" ]]; then
  echo "Usage: $0 <project-dir> <input-markdown-file> [demand-file-name]" >&2
  exit 2
fi

if [[ ! -f "$INPUT_FILE" ]]; then
  echo "Input file not found: $INPUT_FILE" >&2
  exit 2
fi

TARGET_FILE="$PROJECT_DIR/$DEMAND_FILE_NAME"
TIMESTAMP_HOUR="$(date '+%Y-%m-%d-%H')"
BACKUP_FILE="$PROJECT_DIR/productdemand.backup.${TIMESTAMP_HOUR}.md"

mkdir -p "$PROJECT_DIR"

if [[ -f "$TARGET_FILE" ]]; then
  cp "$TARGET_FILE" "$BACKUP_FILE"
  echo "BACKUP_FILE=$BACKUP_FILE"
else
  echo "BACKUP_FILE="
fi

cp "$INPUT_FILE" "$TARGET_FILE"
echo "PROJECT_DIR=$PROJECT_DIR"
echo "TARGET_FILE=$TARGET_FILE"
