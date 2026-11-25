#!/usr/bin/env bash
# Everything in one command: upload local images, generate a Google Vids clip, wait, download. Prints the saved .mp4 path.
# Usage: video.sh "<prompt>" [key=value ...]     (options as in generate.sh)
#   Values of startImage and referenceImage_N that are existing local files are uploaded first.
# Example: video.sh "@avatar_1 holds up @referenceImage_1, smiles and says: \"Best coffee all year.\" Handheld phone camera." \
#            avatar_1=<avatarId> referenceImage_1=./mug.png aspectRatio=portrait duration=6
# OUT_DIR sets the folder (default: the current one); the final job record is saved next to the video as .json.
# If the run is interrupted after "job ..." was logged, do NOT run it again (that pays twice). Resume with:
#   wait-job.sh <jobid> > job.json && download.sh job.json
DIR="$(dirname "$0")"
source "$DIR/_common.sh"
PROMPT="${1:?Usage: video.sh \"<prompt>\" [key=value ...]}"
shift

# An avatar pins the account it lives on, so uploads go there too
for KV in "$@"; do
  case "$KV" in
    avatar_[123]=*) if [ -z "${USEAPI_EMAIL:-}" ]; then USEAPI_EMAIL=$(id_email "${KV#*=}"); export USEAPI_EMAIL; fi ;;
  esac
done
ARGS=()
for KV in "$@"; do
  case "$KV" in
    startImage=*|referenceImage_[123]=*) file_or_id "${KV#*=}"; KV="${KV%%=*}=$FID" ;;
  esac
  ARGS+=("$KV")
done
[ -n "${USEAPI_EMAIL:-}" ] || unset USEAPI_EMAIL

JOBID=$(bash "$DIR/generate.sh" "$PROMPT" ${ARGS[@]+"${ARGS[@]}"})
JOB=$(bash "$DIR/wait-job.sh" "$JOBID") || { echo "Not resubmitted. Job id: $JOBID" >&2; exit 1; }
FILE=$(bash "$DIR/download.sh" - "${OUT_DIR:-.}" <<< "$JOB") || { echo "Resume the download with: download.sh <job.json> (job id $JOBID)" >&2; exit 1; }
echo "$JOB" > "${FILE%.*}.json"
echo "$FILE"
