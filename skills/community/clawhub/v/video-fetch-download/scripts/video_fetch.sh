#!/usr/bin/env bash
# video-fetch: download video/torrent and upload to rclone remote
# Usage: video_fetch.sh <url|magnet|.torrent> [remote:path]
# Env: VIDEOFETCH_REMOTE (default: webdav:videos), VIDEOFETCH_TMPDIR (default: /tmp/video-fetch)

set -euo pipefail

INPUT="${1:-}"
REMOTE="${2:-${VIDEOFETCH_REMOTE:-115drive:云下载}}"
TMPDIR="${VIDEOFETCH_TMPDIR:-/tmp/video-fetch}"

if [[ -z "$INPUT" ]]; then
  echo "Usage: video_fetch.sh <url|magnet|.torrent> [remote:path]" >&2
  exit 1
fi

mkdir -p "$TMPDIR"

# ── Detect input type ──────────────────────────────────────────────
is_torrent() {
  [[ "$INPUT" == magnet:* ]] || [[ "$INPUT" == *.torrent ]] || \
  [[ -f "$INPUT" && "$INPUT" == *.torrent ]]
}

if is_torrent; then
  # ── Torrent / Magnet download via aria2c ───────────────────────
  echo "[video-fetch] Torrent mode: $INPUT"
  aria2c \
    --dir="$TMPDIR" \
    --seed-time=0 \
    --max-connection-per-server=4 \
    --split=4 \
    --bt-stop-timeout=300 \
    --console-log-level=notice \
    "$INPUT"
else
  # ── Direct URL download via yt-dlp ────────────────────────────
  echo "[video-fetch] URL mode: $INPUT"
  yt-dlp \
    --format "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best" \
    --merge-output-format mp4 \
    --output "$TMPDIR/%(title)s.%(ext)s" \
    --no-playlist \
    --write-info-json \
    "$INPUT"
fi

# ── Find downloaded files ──────────────────────────────────────────
FILES=$(find "$TMPDIR" -maxdepth 2 \
  \( -name '*.mp4' -o -name '*.mkv' -o -name '*.webm' \
     -o -name '*.avi' -o -name '*.mov' -o -name '*.flv' \
     -o -name '*.ts'  -o -name '*.rmvb' \) \
  ! -name '*.part' 2>/dev/null)

if [[ -z "$FILES" ]]; then
  echo "[video-fetch] ERROR: no video file found after download" >&2
  exit 1
fi

# ── Upload via rclone ──────────────────────────────────────────────
echo "[video-fetch] Uploading to $REMOTE ..."
while IFS= read -r FILE; do
  echo "  -> $(basename "$FILE")"
  rclone copy "$FILE" "$REMOTE" --progress
done <<< "$FILES"

# ── Cleanup ────────────────────────────────────────────────────────
echo "[video-fetch] Cleaning up ..."
find "$TMPDIR" -maxdepth 2 \
  \( -name '*.mp4' -o -name '*.mkv' -o -name '*.webm' \
     -o -name '*.avi' -o -name '*.mov' -o -name '*.flv' \
     -o -name '*.ts'  -o -name '*.rmvb' -o -name '*.json' \
     -o -name '*.torrent' \) -delete

echo "[video-fetch] Done. Files uploaded to $REMOTE"
