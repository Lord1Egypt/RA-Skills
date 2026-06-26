#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
SKILL_NAME="$(basename "$SKILL_DIR")"
OUT_DIR="$SKILL_DIR/dist"
STAMP="$(date +%Y%m%d-%H%M%S)"
ARCHIVE="$OUT_DIR/${SKILL_NAME}-${STAMP}.tar.gz"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --out-dir)
      OUT_DIR="$2"
      shift 2
      ;;
    *)
      echo "Unknown argument: $1" >&2
      echo "Usage: $0 [--out-dir <path>]" >&2
      exit 1
      ;;
  esac
done

mkdir -p "$OUT_DIR"
ARCHIVE="$OUT_DIR/${SKILL_NAME}-${STAMP}.tar.gz"

# Package the entire skill folder while excluding transient files.
tar -czf "$ARCHIVE" \
  --exclude="${SKILL_NAME}/dist" \
  --exclude="${SKILL_NAME}/scripts/__pycache__" \
  --exclude="${SKILL_NAME}/.DS_Store" \
  -C "$(dirname "$SKILL_DIR")" \
  "$SKILL_NAME"

echo "$ARCHIVE"
