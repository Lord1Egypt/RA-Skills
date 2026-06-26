#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(cd -- "$SCRIPT_DIR/.." && pwd)"
SRC="${QQBOT_SRC_DIR:-$HOME/.openclaw/extensions/qqbot}"
OUT_DIR="${QQBOT_EXPORT_DIR:-$SKILL_DIR/dist}"
TS="$(date +%Y%m%d-%H%M%S)"
NAME="qqbot-plugin-${TS}.tar.gz"
OUT="$OUT_DIR/$NAME"

mkdir -p "$OUT_DIR"

if [ ! -d "$SRC" ]; then
  echo "qqbot source dir not found: $SRC" >&2
  exit 1
fi

tar \
  --exclude='node_modules' \
  --exclude='.git' \
  --exclude='dist/*.map' \
  -czf "$OUT" \
  -C "$(dirname "$SRC")" \
  "$(basename "$SRC")"

echo "$OUT"
