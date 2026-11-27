#!/usr/bin/env bash
# Download the video of a finished job and print the saved path.
# Usage: download.sh <job.json|-> [OUT_DIR]
source "$(dirname "$0")/_common.sh"
JOB=$(cat "${1:--}")
DIR="${2:-.}"
mkdir -p "$DIR"

SHORT=$(jq -r '(.video_id // "") | (capture("video:(?<id>[0-9]+)$").id // "")' <<< "$JOB")
MODEL=$(jq -r '(.model // "") | gsub("[^A-Za-z0-9._-]"; "")' <<< "$JOB")
FILE="$DIR/pixverse${MODEL:+_$MODEL}${SHORT:+_$SHORT}.mp4"
URL=$(jq -r '.url // empty' <<< "$JOB")
if [ -n "$URL" ] && curl -sS --fail --max-time 600 -o "$FILE" "$URL"; then
  echo "$FILE"
  exit 0
fi
rm -f "$FILE"
echo "Could not download the video: $(jq -c '{video_status_name, url}' <<< "$JOB")" >&2
exit 1
