#!/usr/bin/env bash
# Batch-transcribe every audio/video file in a folder with transcribe-so.
# Usage: ./batch-transcribe.sh <folder> [max-usd-per-file]
# Requires: transcribe-so on PATH, TRANSCRIBE_API_KEY exported, jq.
# Sequential on purpose: at the concurrency cap, upload-sourced jobs are
# rejected (fair-use) rather than queued, so we run one job at a time.

set -euo pipefail

FOLDER="${1:?usage: batch-transcribe.sh <folder> [max-usd-per-file]}"
MAX_USD="${2:-5}"
OUT_DIR="$FOLDER/transcripts"
mkdir -p "$OUT_DIR"

for file in "$FOLDER"/*.{mp3,m4a,wav,flac,ogg,mp4,mov,webm,avi}; do
  [ -e "$file" ] || continue
  base=$(basename "$file")
  out="$OUT_DIR/${base%.*}.json"
  if [ -s "$out" ]; then
    echo "skip (already done): $base" >&2
    continue
  fi

  echo "uploading: $base" >&2
  up=$(transcribe-so upload "$file")
  upload_id=$(echo "$up" | jq -r .upload_id)
  duration=$(echo "$up" | jq -r .duration_seconds)

  echo "transcribing: $base (${duration}s, budget \$$MAX_USD)" >&2
  if transcribe-so run --source upload \
      --upload-id "$upload_id" \
      --duration "$duration" \
      --max-usd "$MAX_USD" > "$out"; then
    echo "done: $out" >&2
  else
    code=$?
    rm -f "$out"
    # 6 = local budget refusal (raise MAX_USD), 4 = wallet/spend cap,
    # 5 = transient (retry later). Stop on payment problems, keep going otherwise.
    echo "failed ($code): $base" >&2
    if [ "$code" -eq 4 ]; then
      echo "wallet/spend-cap problem; stopping" >&2
      exit 4
    fi
  fi
done
