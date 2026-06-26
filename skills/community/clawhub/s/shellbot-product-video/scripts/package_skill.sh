#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
SKILL_NAME="$(basename "$SKILL_DIR")"
OUT_DIR="$SKILL_DIR/dist"
STAMP="$(date +%Y%m%d-%H%M%S)"
TAR_ARCHIVE="$OUT_DIR/${SKILL_NAME}-${STAMP}.tar.gz"
ZIP_ARCHIVE="$OUT_DIR/${SKILL_NAME}-${STAMP}.zip"

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
TAR_ARCHIVE="$OUT_DIR/${SKILL_NAME}-${STAMP}.tar.gz"
ZIP_ARCHIVE="$OUT_DIR/${SKILL_NAME}-${STAMP}.zip"

tar -czf "$TAR_ARCHIVE" \
  --exclude="${SKILL_NAME}/dist" \
  --exclude="${SKILL_NAME}/scripts/__pycache__" \
  --exclude="${SKILL_NAME}/.DS_Store" \
  --exclude="${SKILL_NAME}/node_modules" \
  -C "$(dirname "$SKILL_DIR")" \
  "$SKILL_NAME"

if ! command -v zip >/dev/null 2>&1; then
  echo "zip command not found; cannot build ${ZIP_ARCHIVE}" >&2
  exit 1
fi

(
  cd "$(dirname "$SKILL_DIR")"
  zip -rq "$ZIP_ARCHIVE" "$SKILL_NAME" \
    -x "${SKILL_NAME}/dist/*" \
    -x "${SKILL_NAME}/scripts/__pycache__/*" \
    -x "${SKILL_NAME}/.DS_Store" \
    -x "${SKILL_NAME}/node_modules/*" \
    -x "${SKILL_NAME}/**/.DS_Store"
)

echo "$TAR_ARCHIVE"
echo "$ZIP_ARCHIVE"
