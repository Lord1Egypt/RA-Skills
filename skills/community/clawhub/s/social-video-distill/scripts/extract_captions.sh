#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 1 ]]; then
  echo "Usage: $0 <url> [outdir]" >&2
  exit 2
fi

URL="$1"
OUTDIR="${2:-$(pwd)/tmp/social-video-distill-captions}"
SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
YT_DLP="$SKILL_DIR/.runtime/ytvenv/bin/yt-dlp"

if [[ ! -x "$YT_DLP" ]]; then
  echo "INSTALL_RUNTIME_REQUIRED" >&2
  echo "Run: bash $SKILL_DIR/scripts/install_runtime.sh" >&2
  exit 1
fi

mkdir -p "$OUTDIR"
BEFORE_COUNT="$(find "$OUTDIR" -maxdepth 1 -type f | wc -l)"

"$YT_DLP" \
  --skip-download \
  --write-subs \
  --write-auto-subs \
  --sub-langs 'all,-live_chat' \
  --convert-subs srt \
  -o "$OUTDIR/%(id)s.%(ext)s" \
  "$URL"

AFTER_COUNT="$(find "$OUTDIR" -maxdepth 1 -type f | wc -l)"
if [[ "$AFTER_COUNT" -le "$BEFORE_COUNT" ]]; then
  echo "NO_CAPTIONS"
  exit 0
fi

find "$OUTDIR" -maxdepth 1 -type f | sort
