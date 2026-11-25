#!/usr/bin/env bash
# Download every file of a finished job (.m4a for audio, .mp4 for video, .pdf and .pptx for slides) and print the saved paths.
# Usage: download.sh <job.json|-> [OUT_DIR]
# Files are named after the episode title (letters and digits in any script) plus a short job id.
# The download links need the same API token, so they cannot be opened in a browser as they are.
source "$(dirname "$0")/_common.sh"
JOB=$(cat "${1:--}")
OUT="${2:-.}"
mkdir -p "$OUT"

NAME=$(jq -r '(.result.title // "") | gsub("[^\\p{L}\\p{M}\\p{N}_-]+"; "_") | .[:60] | sub("^_+"; "") | sub("_+$"; "")' <<< "$JOB")
NAME="${NAME#_}"
NAME="${NAME:-gemini-notebook}"
SHORT=$(jq -r '(.jobid // "") | (capture("job:(?<id>[0-9a-f]{8})").id // "")' <<< "$JOB")
if [ -n "$SHORT" ]; then NAME="${NAME}_$SHORT"; fi
jq -r '.result.files[] | "\(.format)\t\(.url)"' <<< "$JOB" | while IFS=$'\t' read -r FORMAT URL; do
  FILE="$OUT/$NAME.$FORMAT"
  acurl -sS --fail --max-time 600 -o "$FILE" "$URL"
  echo "$FILE"
done
