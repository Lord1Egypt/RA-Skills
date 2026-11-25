#!/usr/bin/env bash
# Extend a Google Vids clip by 3 to 10 seconds and print the job id. The result is the WHOLE clip (source + new seconds).
# Usage: extend.sh <video mediaId> "<prompt for the new seconds>" [key=value ...]
#   duration=3..10 (default 8, the seconds added: only these are charged). Up to 10 per call, even though a
#   new clip can be 15: Google adds only 10 and charges a longer request in full, so the API refuses it.
#   aspectRatio=landscape|portrait  resolution=720p|1080p   (default: the source clip's)
# The extend gets the clip, not the avatars: name people by what they wear ("the woman in the cream hoodie").
# Google Vids extends clips of up to 24 seconds (a longer source answers 400), so a chain tops out at about
# 34 seconds. Stay at 720p and upscale once at the end (clips of up to 20 s).
# An extend takes about 1.5 to 2 minutes.
# Docs: https://useapi.net/docs/api-google-vids-v1/post-google-vids-videos-extend
# This spends Google Vids seconds and is never retried automatically.
source "$(dirname "$0")/_common.sh"
MEDIA="${1:?Usage: extend.sh <video mediaId> \"<prompt>\" [key=value ...]}"
PROMPT="${2:?Usage: extend.sh <video mediaId> \"<prompt>\" [key=value ...]}"
shift 2

BODY=$(jq -n --arg m "$MEDIA" --arg p "$PROMPT" '{mediaId: $m, prompt: $p}')
for KV in "$@"; do BODY=$(add_kv "$BODY" "$KV"); done
start_job videos/extend "$BODY"
