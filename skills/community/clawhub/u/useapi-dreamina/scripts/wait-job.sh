#!/usr/bin/env bash
# Poll a video job every 15 seconds until it is completed or failed, then print the final job record (JSON).
# Usage: wait-job.sh <jobid> > job.json
# A clip usually takes 1 to 3 minutes. Long videos (31 to 180 s) took 13 to 17 minutes in useapi.net's tests.
# Exits 1 if the job failed (failed jobs are not charged). A network error or HTTP 5xx is retried up to 3 times.
# Safe to re-run on the same job id to resume.
# Docs: https://useapi.net/docs/api-dreamina-v1/get-dreamina-videos-jobid
source "$(dirname "$0")/_common.sh"
JOBID="${1:?Usage: wait-job.sh <jobid>}"

START=$(date +%s)
while true; do
  JOB=$(api_poll GET "videos/$JOBID")
  STATUS=$(jq -r .status <<< "$JOB")
  if [ "$STATUS" = completed ] || [ "$STATUS" = failed ]; then break; fi
  log "job $STATUS ($(( $(date +%s) - START )) s)"
  sleep 15
done
echo "$JOB"
log "job $STATUS after $(( $(date +%s) - START )) s"
if [ "$STATUS" != completed ]; then
  echo "Job failed: $(jq -c '{error, errorDetails, failMsg, code}' <<< "$JOB")" >&2
  case "$(jq -r '.code // ""' <<< "$JOB")" in
    2053) echo "Hint: Dreamina judged the finished video to show recognisable third-party content (a costumed character, a trademarked place, a celebrity look-alike). Describe something original." >&2 ;;
    2038|2050) echo "Hint: Dreamina refused the prompt. Rephrase it, without brand or character names." >&2 ;;
    2039|2048|18000) echo "Hint: Dreamina refused a reference image (content, protected content, or an aspect ratio too wide or narrow). Change or crop the image." >&2 ;;
    2043|2045|2052) echo "Hint: the generated video or its sound failed Dreamina's moderation. Rephrase the prompt and try again." >&2 ;;
    *) echo "Hint: failed jobs are not charged. Try again once, or change the prompt." >&2 ;;
  esac
  exit 1
fi
