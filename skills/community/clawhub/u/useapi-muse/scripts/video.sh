#!/usr/bin/env bash
# Everything in one command: upload local inputs, start a Muse video job, wait for it, download the .mp4.
# Prints the saved path.
# Usage: video.sh "<prompt>" [key=value ...]
#   image_1..9, video_1..3, audio_1..3 = an assetId or a local file (uploaded first). replyUrl= replyRef= as in generate.sh.
# Example: video.sh "Animate image_1: she turns to the camera and says: \"Best seat in town.\" Keep her face exactly as in image_1." \
#            image_1=./photo.jpg
# OUT_DIR sets the folder (default: the current one). The final job record is saved next to it as .json,
# with the new file's assetId in .result.assets[0].assetId for the next job.
# If the run is interrupted after "job ..." was logged, do NOT run it again (that uses the allowance twice). Resume with:
#   wait-job.sh <jobid> > job.json && download.sh job.json
DIR="$(dirname "$0")"
source "$DIR/_common.sh"
PROMPT="${1:?Usage: video.sh \"<prompt>\" [key=value ...]}"
shift

resolve_inputs ${1+"$@"}
JOBID=$("$DIR/generate.sh" video "$PROMPT" ${ARGS[@]+"${ARGS[@]}"})
JOB=$("$DIR/wait-job.sh" "$JOBID") || { echo "Not resubmitted. Job id: $JOBID" >&2; exit 1; }
FILE=$("$DIR/download.sh" - "${OUT_DIR:-.}" <<< "$JOB") || { echo "Resume the download with: download.sh <job.json> (job id $JOBID)" >&2; exit 1; }
echo "$JOB" > "${FILE%.*}.json"
log "assetId $(jq -r '.result.assets[0].assetId' <<< "$JOB")"
echo "$FILE"
