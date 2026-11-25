#!/usr/bin/env bash
# Start one Gemini Omni 1.2 Flash video in Google Vids and print its job id. It does not wait; use wait-job.sh.
# Usage: generate.sh "<prompt>" [key=value ...]
#   duration=3..15 (default 8, seconds; the clip uses that many seconds of the Google Vids allowance)
#   aspectRatio=landscape (default) | portrait      resolution=720p (default) | 1080p (same cost)
#   avatar_1..3=<avatarId>  referenceImage_1..3=<assetId or image mediaId>   (3 references in all)
#   startImage=<assetId or image mediaId>   (the clip opens on it; not with avatars or references)
# The prompt may name references with @avatar_1, @referenceImage_1 ... (each marker needs its parameter).
# Every option: https://useapi.net/docs/api-google-vids-v1/post-google-vids-videos
# This spends Google Vids seconds. It never retries by itself: a retry after an unclear failure could pay twice.
source "$(dirname "$0")/_common.sh"
PROMPT="${1:?Usage: generate.sh \"<prompt>\" [key=value ...]}"
shift

BODY=$(jq -n --arg p "$PROMPT" '{prompt: $p}')
if [ -n "${USEAPI_EMAIL:-}" ]; then BODY=$(jq --arg e "$USEAPI_EMAIL" '.email = $e' <<< "$BODY"); fi
for KV in "$@"; do BODY=$(add_kv "$BODY" "$KV"); done
start_job videos "$BODY"
