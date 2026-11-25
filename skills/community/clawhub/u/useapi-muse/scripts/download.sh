#!/usr/bin/env bash
# Download the file of a finished job (or any assetId) and print the saved path.
# Usage: download.sh <job.json | - | assetId> [OUT_DIR] [NAME]
# GET /assets streams the file from the account's Muse Library. It stays there until it is deleted at muse.ai,
# so it can be downloaded again later. Default name: muse_<image|video>_<the job's timestamp>.<webp|mp4>.
# When a job lists two files (the agent finished Muse's clip with its own tools), the finished one is first and is the one saved.
source "$(dirname "$0")/_common.sh"
SRC="${1:--}"
OUT="${2:-.}"
NAME="${3:-}"
mkdir -p "$OUT"

case "$SRC" in
  user:*) ASSET="$SRC"; LABEL="" ;;
  *)
    JOB=$(cat "$SRC")
    ASSET=$(jq -r '.result.assets[0].assetId // empty' <<< "$JOB")
    [ -n "$ASSET" ] || { echo "The job has no result to download: $(jq -c '{status, error}' <<< "$JOB")" >&2; exit 1; }
    LABEL=$(jq -r '[(.type // "file"), ((.jobid // "") | capture("^j(?<t>[0-9]+)").t // empty)] | join("_")' <<< "$JOB") ;;
esac
EXT="${ASSET##*.}"
case "$EXT" in webp|jpg|jpeg|png|mp4|mov|webm|mp3|wav|m4a|ogg) ;; *) EXT=bin ;; esac
if [ -z "$NAME" ]; then
  [ -n "$LABEL" ] || LABEL=$(printf '%s' "$ASSET" | cksum | cut -d' ' -f1)
  NAME="muse_$LABEL"
fi
FILE="$OUT/$NAME.$EXT"

# Reading a file is free, so a network error or a 502/503 is retried (3 tries, 10 s apart)
for TRY in 1 2 3; do
  CODE=$(acurl -sS --max-time 600 -o "$FILE.part" -w '%{http_code}' "$API/assets/$(enc "$ASSET")") || true
  CODE="${CODE:-000}"
  if [ "${CODE:0:1}" = 2 ]; then
    mv "$FILE.part" "$FILE"
    echo "$FILE"
    exit 0
  fi
  case "$CODE" in
    000|502|503) if [ "$TRY" -lt 3 ]; then log "GET /assets -> HTTP $CODE, retry $TRY of 2 in 10 s"; sleep 10; continue; fi ;;
  esac
  break
done
echo "GET /assets -> HTTP $CODE: $(cat "$FILE.part" 2>/dev/null)" >&2
hint "$CODE" "$FILE.part"
rm -f "$FILE.part"
exit 1
