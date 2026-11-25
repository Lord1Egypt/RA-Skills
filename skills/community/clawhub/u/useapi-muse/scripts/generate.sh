#!/usr/bin/env bash
# Start one Muse image or video job and print its job id. It does not wait: use wait-job.sh.
# Usage: generate.sh image|video "<prompt>" [key=value ...]
#   image_1..image_9=<assetId>                                  (image and video jobs)
#   video_1..video_3=<assetId>  audio_1..audio_3=<assetId>      (video jobs only)
#   replyUrl=<https webhook URL>  replyRef=<your reference>
# An assetId comes from upload.sh or from an earlier job's result.assets[] (no download or upload needed).
# The prompt (at most 5000 characters) names the inputs (image_1, video_1 ...), says the aspect ratio
# ("in exactly 16:9 aspect ratio") and puts any spoken lines in quotes. There are no model, ratio, resolution
# or duration parameters.
# Every option: https://useapi.net/docs/api-muse-v1/post-muse-jobs-video
# This uses the weekly Muse allowance. It never retries by itself: a retry after an unclear failure could use it twice.
source "$(dirname "$0")/_common.sh"
USAGE='Usage: generate.sh image|video "<prompt>" [key=value ...]'
TYPE="${1:?$USAGE}"
case "$TYPE" in image|video) ;; *) echo "$USAGE" >&2; exit 1 ;; esac
PROMPT="${2:?$USAGE}"
shift 2

BODY=$(jq -n --arg p "$PROMPT" '{prompt: $p}')
if [ -n "${USEAPI_EMAIL:-}" ]; then BODY=$(jq --arg e "$USEAPI_EMAIL" '.email = $e' <<< "$BODY"); fi
for KV in "$@"; do BODY=$(add_kv "$BODY" "$KV"); done
start_job "$TYPE" "$BODY"
