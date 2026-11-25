#!/usr/bin/env bash
# Edit a generated Google Vids clip with a prompt (recolour, add an object, restyle) and print the job id.
# Usage: edit.sh <video mediaId> "<the change>" [key=value ...]
#   duration=3..15 (default: the clip's length, at most 15; no longer than the clip)
#   aspectRatio=landscape|portrait  resolution=720p|1080p   (default: the source clip's)
# An edit returns at most 15 seconds (the first 15 of a longer clip) and costs at most the seconds it edits
# (a 15-second edit used 10 in our tests). A 15-second edit takes about 2 minutes or more.
# Google refuses edits of uploaded videos (422, nothing charged): edit clips the API generated.
# Docs: https://useapi.net/docs/api-google-vids-v1/post-google-vids-videos-edit
# This spends Google Vids seconds and is never retried automatically.
source "$(dirname "$0")/_common.sh"
MEDIA="${1:?Usage: edit.sh <video mediaId> \"<the change>\" [key=value ...]}"
PROMPT="${2:?Usage: edit.sh <video mediaId> \"<the change>\" [key=value ...]}"
shift 2

BODY=$(jq -n --arg m "$MEDIA" --arg p "$PROMPT" '{video: $m, prompt: $p}')
for KV in "$@"; do BODY=$(add_kv "$BODY" "$KV"); done
start_job videos/edit "$BODY"
