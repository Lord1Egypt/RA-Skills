#!/usr/bin/env bash
# Generate one image in Google Vids, download it, and print its mediaId.
# Usage: image.sh "<prompt>" [key=value ...]
#   aspectRatio=16:9 (default, 1376x768) | 1:1 (1024x1024) | 9:16 (768x1376)
#   style=none (default) | photography | sketch | background | watercolor | vector-art | cyberpunk
# Costs 1 image of the account's monthly Google Vids images. The JPEG is saved to OUT_DIR (default: the current
# folder) and its path logged on stderr. Use the mediaId within a few hours as an avatar picture
# (avatar.sh image=<mediaId>), startImage or referenceImage_N.
# Docs: https://useapi.net/docs/api-google-vids-v1/post-google-vids-images
DIR="$(dirname "$0")"
source "$DIR/_common.sh"
PROMPT="${1:?Usage: image.sh \"<prompt>\" [key=value ...]}"
shift

BODY=$(jq -n --arg p "$PROMPT" '{prompt: $p}')
if [ -n "${USEAPI_EMAIL:-}" ]; then BODY=$(jq --arg e "$USEAPI_EMAIL" '.email = $e' <<< "$BODY"); fi
for KV in "$@"; do BODY=$(add_kv "$BODY" "$KV"); done
JOBID=$(start_job images "$BODY")
JOB=$(bash "$DIR/wait-job.sh" "$JOBID") || exit 1
if FILE=$(bash "$DIR/download.sh" - "${OUT_DIR:-.}" <<< "$JOB"); then log "saved $FILE"; else log "download failed; the mediaId still works for a few hours"; fi
jq -r .result.mediaId <<< "$JOB"
