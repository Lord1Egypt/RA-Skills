#!/usr/bin/env bash
# Everything in one command: upload a local first frame, generate, wait, download. Prints the saved .mp4 path.
# Usage: video.sh "<prompt>" [key=value ...]
#   A first_frame_path value that is an existing local image file is uploaded first and replaced by its upload path.
#   Other options as in generate.sh. The default model is v6.
# Example: video.sh "A red panda eats bamboo in a misty forest" model=kling-4.0 quality=720p duration=5 aspect_ratio=9:16
# OUT_DIR sets the folder (default: the current one). If the run is interrupted after the video id was
# logged, resume with: wait-job.sh <video_id> > job.json && download.sh job.json
DIR="$(dirname "$0")"
source "$DIR/_common.sh"
PROMPT="${1:?Usage: video.sh \"<prompt>\" [key=value ...]}"
shift

ARGS=()
for KV in "$@"; do
  K="${KV%%=*}"
  V="${KV#*=}"
  if [ "$K" = first_frame_path ] && [ -f "$V" ]; then
    V=$("$DIR/upload.sh" "$V")
    KV="$K=$V"
  fi
  ARGS+=("$KV")
done

VID=$("$DIR/generate.sh" "$PROMPT" ${ARGS[@]+"${ARGS[@]}"})
JOB=$("$DIR/wait-job.sh" "$VID")
"$DIR/download.sh" - "${OUT_DIR:-.}" <<< "$JOB"
