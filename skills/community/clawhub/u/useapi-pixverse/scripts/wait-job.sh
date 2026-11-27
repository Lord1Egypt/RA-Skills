#!/usr/bin/env bash
# Poll a video every 10 seconds until it is completed, failed or moderated, then print the final video record (JSON).
# Usage: wait-job.sh <video_id> [max seconds, default 1800] > job.json
# The API answers 404 while a video is still processing, so 404 means keep waiting (until the time limit).
# Exits 1 if the video failed or was moderated, or the limit passed. Safe to re-run on the same id to resume.
# A network error or HTTP 5xx is retried up to 3 times.
# Docs: https://useapi.net/docs/api-pixverse-v2/get-pixverse-videos-video_id
source "$(dirname "$0")/_common.sh"
VID="${1:?Usage: wait-job.sh <video_id> [max seconds]}"
MAX="${2:-1800}"
P="videos/$(enc "$VID")"

START=$(date +%s)
TRIES=0
JOB=""
while true; do
  _call GET "$P"
  case "$CODE" in
    2??)
      JOB=$(cat "$OUT"); rm -f "$OUT"
      STATUS=$(jq -r '.video_status_name // "UNKNOWN"' <<< "$JOB")
      FINAL=$(jq -r '.video_status_final // false' <<< "$JOB")
      if [ "$FINAL" = true ]; then break; fi
      log "video $STATUS ($(( $(date +%s) - START )) s)" ;;
    404)
      rm -f "$OUT"
      log "video processing ($(( $(date +%s) - START )) s)" ;;
    000|5??)
      rm -f "$OUT"
      TRIES=$((TRIES + 1))
      if [ "$TRIES" -gt 3 ]; then echo "GET /$P -> HTTP $CODE, giving up after 3 retries" >&2; hint "$CODE" /dev/null; exit 1; fi
      log "GET /$P -> HTTP $CODE, retry $TRIES of 3" ;;
    *)
      _finish GET "$P" ;;
  esac
  if [ $(( $(date +%s) - START )) -ge "$MAX" ]; then
    echo "Still not finished after $MAX s. Do not start a new video: wait again with wait-job.sh \"$VID\"" >&2
    exit 1
  fi
  sleep 10
done
echo "$JOB"
log "video $STATUS after $(( $(date +%s) - START )) s"
if [ "$STATUS" != COMPLETED ]; then
  echo "Video not made: $(jq -c '{video_status_name, error, prompt}' <<< "$JOB")" >&2
  case "$STATUS" in
    MODERATED) echo "Hint: PixVerse moderation stopped this video. Rephrase the prompt, without brand or character names, or use another image. Repeated moderation can get a PixVerse account suspended, so do not retry it unchanged." >&2 ;;
    *) echo "Hint: try again once, or change the prompt. See https://useapi.net/docs/api-pixverse-v2/get-pixverse-videos" >&2 ;;
  esac
  exit 1
fi
