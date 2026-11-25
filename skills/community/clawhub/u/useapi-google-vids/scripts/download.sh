#!/usr/bin/env bash
# Download the file of a finished job (or any video or image mediaId) and print the saved path.
# Usage: download.sh <job.json | - | mediaId> [OUT_DIR] [NAME]
# The file comes through api.useapi.net (GET /media), since Google's own links open only with the account's cookies.
# Files are temporary: videos last 24 hours and images a few hours, so download soon.
# Default name: vids_<mode>_<13 digits of the job id>.mp4 (or .jpg for an image).
source "$(dirname "$0")/_common.sh"
SRC="${1:--}"
OUT="${2:-.}"
NAME="${3:-}"
mkdir -p "$OUT"

case "$SRC" in
  user:*-video:*|user:*-image:*) MEDIA="$SRC"; LABEL="" ;;
  *)
    JOB=$(cat "$SRC")
    MEDIA=$(jq -r '.result.mediaId // empty' <<< "$JOB")
    [ -n "$MEDIA" ] || { echo "The job has no result to download: $(jq -c '{status, error}' <<< "$JOB")" >&2; exit 1; }
    LABEL=$(jq -r '[(.mode // .type // "video"), ((.jobid // "") | capture("^j(?<t>[0-9]{13})").t // empty)] | join("_")' <<< "$JOB") ;;
esac
case "$MEDIA" in *-image:*) EXT=jpg ;; *) EXT=mp4 ;; esac
if [ -z "$NAME" ]; then
  [ -n "$LABEL" ] || LABEL=$(printf '%s' "$MEDIA" | cksum | cut -d' ' -f1)
  NAME="vids_$LABEL"
fi
FILE="$OUT/$NAME.$EXT"

# Reading a file is free, so a network error or a 502/503 from Google is retried (3 tries, 10 s apart)
for TRY in 1 2 3; do
  CODE=$(acurl -sS --max-time 600 -o "$FILE.part" -w '%{http_code}' "$API/media/$(enc "$MEDIA")") || true
  CODE="${CODE:-000}"
  if [ "${CODE:0:1}" = 2 ]; then
    mv "$FILE.part" "$FILE"
    echo "$FILE"
    exit 0
  fi
  case "$CODE" in
    000|502|503) if [ "$TRY" -lt 3 ]; then log "GET /media -> HTTP $CODE, retry $TRY of 2 in 10 s"; sleep 10; continue; fi ;;
  esac
  break
done
echo "GET /media -> HTTP $CODE: $(cat "$FILE.part" 2>/dev/null)" >&2
hint "$CODE" "$FILE.part"
rm -f "$FILE.part"
exit 1
