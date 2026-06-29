#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -lt 3 ]; then
  echo "Usage: $0 <channel> <target> <html-report-path> [message]" >&2
  exit 2
fi

CHANNEL="$1"
TARGET="$2"
SRC="$3"
MSG="${4:-HTML report}"
TMP="/tmp/openclaw"
OUT="$TMP/$(basename "$SRC")"

ls -lh "$SRC" >&2
file "$SRC" >&2
mkdir -p "$TMP"
chmod 700 "$TMP" || true
cp "$SRC" "$OUT"
chmod 600 "$OUT"

openclaw message send \
  --channel "$CHANNEL" \
  --target "$TARGET" \
  --message "$MSG" \
  --media "$OUT" \
  --force-document
