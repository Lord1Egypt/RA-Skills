#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -lt 3 ]; then
  echo "Usage: $0 <channel> <target> <archive-path> [message]" >&2
  exit 2
fi

CHANNEL="$1"
TARGET="$2"
SRC="$3"
MSG="${4:-Report archive}"

ls -lh "$SRC" >&2
file "$SRC" >&2

openclaw message send \
  --channel "$CHANNEL" \
  --target "$TARGET" \
  --message "$MSG" \
  --media "$SRC" \
  --force-document
