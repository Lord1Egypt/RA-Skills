#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 1 ]]; then
  echo "Usage: $0 <url> [outdir]" >&2
  exit 2
fi

URL="$1"
OUTDIR="${2:-$(pwd)/tmp/social-video-distill-media}"
SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
YT_DLP="$SKILL_DIR/.runtime/ytvenv/bin/yt-dlp"

if [[ ! -x "$YT_DLP" ]]; then
  echo "INSTALL_RUNTIME_REQUIRED" >&2
  echo "Run: bash $SKILL_DIR/scripts/install_runtime.sh" >&2
  exit 1
fi

mkdir -p "$OUTDIR"
"$YT_DLP" -o "$OUTDIR/%(id)s.%(ext)s" "$URL"
find "$OUTDIR" -maxdepth 1 -type f | sort
