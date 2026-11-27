#!/usr/bin/env bash
# Start one video generation and print its video id. It does not wait: use wait-job.sh.
# Usage: generate.sh "<prompt>" [key=value ...]
#   model=v6 (this script's default; works on every paid PixVerse plan) | v5.6 | pixverse-c1 |
#         seedance-2.5 | seedance-2.5-flash | seedance-2.0 | seedance-2.0-fast | seedance-2.0-mini |
#         kling-4.0 | kling-o3 | kling-v3 | grok-imagine | grok-imagine-1.5 (image to video only) |
#         veo-3.1-lite | veo-3.1-fast | veo-3.1-standard | minimax-h3 | minimax-h3-max | wan-3.0 |
#         happyhorse-1.0 | gemini-omni-flash | flux-3.0
#         (third-party models need a PixVerse Pro plan or higher)
#   duration=<seconds>  quality=<resolution>  aspect_ratio=16:9|9:16|1:1|... (not with first_frame_path)
#   first_frame_path=<upload path from upload.sh>  audio=true|false  email=<PixVerse account>
# duration and quality are required by the API on every model except v6, v5.6, v5.5, v5 and v5-fast.
# When they are missing this script fills in the cheapest sensible value: duration 5 (veo: 4), and quality 720p
# (seedance: 480p, grok-imagine: 480p, minimax-h3 and minimax-h3-max: 768p). Pass them to choose.
# Every option: https://useapi.net/docs/api-pixverse-v2/post-pixverse-videos-create-v4
# Limits per model: https://useapi.net/docs/api-pixverse-v2/model-capabilities
# This spends PixVerse credits. It never retries by itself: a retry after an unclear failure could pay twice.
source "$(dirname "$0")/_common.sh"
PROMPT="${1:?Usage: generate.sh \"<prompt>\" [key=value ...]}"
shift

BODY=$(jq -n --arg p "$PROMPT" '{prompt: $p, model: "v6"}')
for KV in "$@"; do
  case "$KV" in *=*) ;; *) echo "Expected key=value, got: $KV" >&2; exit 1 ;; esac
  K="${KV%%=*}"
  V="${KV#*=}"
  case "$K" in
    duration|maxJobs|seed|template_id) BODY=$(jq --arg k "$K" --argjson v "$V" '.[$k] = $v' <<< "$BODY") ;;
    audio|auto_sound|multi_shot|relax_mode|preview_mode|off_peak_mode) BODY=$(jq --arg k "$K" --argjson v "$V" '.[$k] = $v' <<< "$BODY") ;;
    *) BODY=$(jq --arg k "$K" --arg v "$V" '.[$k] = $v' <<< "$BODY") ;;
  esac
done

MODEL=$(jq -r .model <<< "$BODY")
case "$MODEL" in
  v6|v5.6|v5.5|v5|v5-fast) ;;
  *)
    if [ "$(jq -r '.duration // empty' <<< "$BODY")" = "" ]; then
      case "$MODEL" in veo-*) D=4 ;; *) D=5 ;; esac
      BODY=$(jq --argjson d "$D" '.duration = $d' <<< "$BODY")
    fi
    if [ "$(jq -r '.quality // empty' <<< "$BODY")" = "" ]; then
      case "$MODEL" in
        seedance-*|grok-imagine*) Q=480p ;;
        minimax-h3*) Q=768p ;;
        *) Q=720p ;;
      esac
      BODY=$(jq --arg q "$Q" '.quality = $q' <<< "$BODY")
    fi ;;
esac
if [ -n "${USEAPI_EMAIL:-}" ] && [ "$(jq -r '.email // empty' <<< "$BODY")" = "" ]; then
  BODY=$(jq --arg e "$USEAPI_EMAIL" '.email = $e' <<< "$BODY")
fi

JOB=$(api POST videos/create "$BODY")
ID=$(jq -r '.video_id // empty' <<< "$JOB")
[ -n "$ID" ] || { echo "No video id in the answer: $JOB" >&2; exit 1; }
log "video $ID"
echo "$ID"
