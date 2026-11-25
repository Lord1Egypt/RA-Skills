#!/usr/bin/env bash
# Start one video generation and print its job id. It does not wait: use wait-job.sh.
# Usage: generate.sh "<prompt>" [key=value ...]
#   model=seedance-2.5 (this script's default) | seedance-2.5-draft | seedance-2.5-flash (CA) |
#         seedance-2.0 | seedance-2.0-fast | seedance-2.0-mini
#   ratio=16:9 (default) | 9:16 | 1:1 | 4:3 | 3:4 | 21:9   (not with firstFrameRef: the image's ratio is used)
#   duration=<seconds> (default 5. 4 to 30 on Seedance 2.5, 31 to 180 is long video on seedance-2.5, 4 to 15 on 2.0)
#   resolution=480p (Seedance 2.5 default) | 720p | 1080p | 4k (seedance-2.5 on CA accounts only)
#   firstFrameRef=<assetRef>  endFrameRef=<assetRef>  omni_1..N_imageRef / _videoRef / _audioRef=<assetRef>
#   unlimited=true   account=<REGION:email>
# Every option: https://useapi.net/docs/api-dreamina-v1/post-dreamina-videos
# This spends Dreamina credits. It never retries by itself: a retry after an unclear failure could pay twice.
source "$(dirname "$0")/_common.sh"
PROMPT="${1:?Usage: generate.sh \"<prompt>\" [key=value ...]}"
shift

BODY=$(jq -n --arg p "$PROMPT" '{prompt: $p, model: "seedance-2.5"}')
for KV in "$@"; do
  case "$KV" in *=*) ;; *) echo "Expected key=value, got: $KV" >&2; exit 1 ;; esac
  K="${KV%%=*}"
  V="${KV#*=}"
  case "$K" in
    duration|maxJobs) BODY=$(jq --arg k "$K" --argjson v "$V" '.[$k] = $v' <<< "$BODY") ;;
    unlimited) BODY=$(jq --argjson v "$V" '.unlimited = $v' <<< "$BODY") ;;
    *) BODY=$(jq --arg k "$K" --arg v "$V" '.[$k] = $v' <<< "$BODY") ;;
  esac
done
if [ -n "${USEAPI_EMAIL:-}" ] && [ "$(jq -r '.account // empty' <<< "$BODY")" = "" ]; then
  ACCOUNT=$(account_id)
  BODY=$(jq --arg a "$ACCOUNT" '.account = $a' <<< "$BODY")
fi

JOB=$(api POST videos "$BODY")
ID=$(jq -r '.jobid // empty' <<< "$JOB")
[ -n "$ID" ] || { echo "No job id in the answer: $JOB" >&2; exit 1; }
log "job $ID"
echo "$ID"
