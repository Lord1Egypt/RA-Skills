#!/usr/bin/env bash
# Everything in one command: upload local files, generate, wait, download. Prints the saved .mp4 path.
# Usage: video.sh "<prompt>" [key=value ...]
#   Any value that is an existing local file (for firstFrameRef, endFrameRef or omni_N_imageRef /
#   omni_N_videoRef / omni_N_audioRef) is uploaded first and replaced by its assetRef. All uploads go to
#   one account: USEAPI_EMAIL, else the first connected account (a Canada one for 4k or seedance-2.5-flash).
#   Other options as in generate.sh. The default model is seedance-2.5.
# Example: video.sh "@image1 walks into a sunlit cafe and waves at the camera" omni_1_imageRef=./me.jpg ratio=9:16 duration=8
# OUT_DIR sets the folder (default: the current one). If the run is interrupted after the job id was
# logged, resume with: wait-job.sh <jobid> > job.json && download.sh job.json
DIR="$(dirname "$0")"
source "$DIR/_common.sh"
PROMPT="${1:?Usage: video.sh \"<prompt>\" [key=value ...]}"
shift

REGION=""
ACCOUNT=""
for KV in "$@"; do
  case "$KV" in
    resolution=4k|model=seedance-2.5-flash) REGION=CA ;;
    account=*) ACCOUNT="${KV#account=}" ;;
  esac
done

ARGS=()
UPLOADED=""
for KV in "$@"; do
  K="${KV%%=*}"
  V="${KV#*=}"
  if [ "$K" != "$KV" ] && [ -f "$V" ]; then
    if [ -z "$ACCOUNT" ]; then ACCOUNT=$(account_id "$REGION"); fi
    V=$("$DIR/upload.sh" "$V" "$ACCOUNT")
    KV="$K=$V"
    UPLOADED=1
  fi
  ARGS+=("$KV")
done
# References only work on the account that holds them, so the job runs there
case " ${ARGS[*]-} " in
  *" account="*) ;;
  *) if [ -n "$UPLOADED" ]; then ARGS+=("account=$ACCOUNT"); fi ;;
esac

JOBID=$("$DIR/generate.sh" "$PROMPT" ${ARGS[@]+"${ARGS[@]}"})
JOB=$("$DIR/wait-job.sh" "$JOBID")
"$DIR/download.sh" - "${OUT_DIR:-.}" <<< "$JOB"
