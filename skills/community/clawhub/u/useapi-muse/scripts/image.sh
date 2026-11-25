#!/usr/bin/env bash
# Everything in one command: upload local input images, start a Muse image job, wait for it, download the .webp.
# Prints the saved path.
# Usage: image.sh "<prompt>" [image_1..image_9=<assetId or local file>] [replyUrl= replyRef=]
# Example: image.sh "In exactly 4:5 aspect ratio, the person from image_1 wearing the jacket from image_2." \
#            image_1=./me.jpg image_2=./jacket.png
# OUT_DIR sets the folder (default: the current one). The final job record is saved next to it as .json,
# with the new file's assetId in .result.assets[0].assetId for the next job.
# If the run is interrupted after "job ..." was logged, do NOT run it again (that uses the allowance twice). Resume with:
#   wait-job.sh <jobid> > job.json && download.sh job.json
DIR="$(dirname "$0")"
source "$DIR/_common.sh"
PROMPT="${1:?Usage: image.sh \"<prompt>\" [key=value ...]}"
shift

resolve_inputs ${1+"$@"}
JOBID=$("$DIR/generate.sh" image "$PROMPT" ${ARGS[@]+"${ARGS[@]}"})
JOB=$("$DIR/wait-job.sh" "$JOBID") || { echo "Not resubmitted. Job id: $JOBID" >&2; exit 1; }
FILE=$("$DIR/download.sh" - "${OUT_DIR:-.}" <<< "$JOB") || { echo "Resume the download with: download.sh <job.json> (job id $JOBID)" >&2; exit 1; }
echo "$JOB" > "${FILE%.*}.json"
log "assetId $(jq -r '.result.assets[0].assetId' <<< "$JOB")"
echo "$FILE"
