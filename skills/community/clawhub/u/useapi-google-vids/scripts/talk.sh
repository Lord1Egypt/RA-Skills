#!/usr/bin/env bash
# Talking avatar in one command: the avatar reads your script word for word, in its own voice, as a
# 1280x720 landscape talking-head MP4 of up to 30 seconds. Waits, downloads, prints the saved .mp4 path.
# Usage: talk.sh <avatarId> "<script>"
#   The script is 1 to 400 characters and must fit in 30 seconds when spoken (about 250 to 400 characters,
#   depending on the voice). Audio tags in square brackets, such as [whisper] or [short pause], are performed,
#   not read aloud.
# Uses 1 AI avatar video and 1 Gemini use of the account the avatar lives on, no video seconds. Google counts
# the video even when its safety check refuses the finished clip (422). Takes about 1 to 2.5 minutes.
# OUT_DIR sets the folder (default: the current one); the final job record is saved next to the video as .json.
# If the run is interrupted after "job ..." was logged, do NOT run it again. Resume with:
#   wait-job.sh <jobid> > job.json && download.sh job.json
# Docs: https://useapi.net/docs/api-google-vids-v1/post-google-vids-videos-avatar
DIR="$(dirname "$0")"
source "$DIR/_common.sh"
AVATAR="${1:?Usage: talk.sh <avatarId> \"<script>\"}"
SCRIPT="${2:?Usage: talk.sh <avatarId> \"<script>\"}"

JOBID=$(start_job videos/avatar "$(jq -n --arg a "$AVATAR" --arg s "$SCRIPT" '{avatar: $a, script: $s}')")
JOB=$(bash "$DIR/wait-job.sh" "$JOBID") || { echo "Not resubmitted. Job id: $JOBID" >&2; exit 1; }
FILE=$(bash "$DIR/download.sh" - "${OUT_DIR:-.}" <<< "$JOB") || { echo "Resume the download with: download.sh <job.json> (job id $JOBID)" >&2; exit 1; }
echo "$JOB" > "${FILE%.*}.json"
echo "$FILE"
