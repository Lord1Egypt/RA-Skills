#!/usr/bin/env bash
# Download the video of a finished job and print the saved path.
# Usage: download.sh <job.json|-> [OUT_DIR]
# videoUrl is the clean master when Dreamina has one. The links are signed and expire about 7 days after generation.
source "$(dirname "$0")/_common.sh"
JOB=$(cat "${1:--}")
DIR="${2:-.}"
mkdir -p "$DIR"

SHORT=$(jq -r '(.jobid // "") | (capture("^j(?<id>[0-9]+)").id // "")' <<< "$JOB")
FILE="$DIR/seedance${SHORT:+_$SHORT}.mp4"
for URL in $(jq -r '.response | (.videoUrl, .videoUrlBackup, .videoUrlWatermarked) // empty' <<< "$JOB"); do
  if curl -sS --fail --max-time 600 -o "$FILE" "$URL"; then
    echo "$FILE"
    exit 0
  fi
  rm -f "$FILE"
  log "download failed, trying the next link"
done
echo "Could not download the video: $(jq -c '{status, error}' <<< "$JOB")" >&2
exit 1
