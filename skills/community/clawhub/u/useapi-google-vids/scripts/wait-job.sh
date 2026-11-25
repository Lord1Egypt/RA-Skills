#!/usr/bin/env bash
# Poll a job every 10 seconds until it is completed or failed, then print the final job record (JSON).
# Usage: wait-job.sh <jobid> > job.json
# A video usually takes 20 seconds to about 2 minutes (an extend or an edit the longest), a talking avatar
# video 1 to 2.5 minutes, an image about 10 seconds. Reading a job is free: a network error, 429 or 5xx answer
# is retried. Safe to re-run on the same job id to resume. Job records are kept for 7 days.
# Exits 1 if the job failed, with a hint that says whether it was charged and whether resubmitting is safe.
source "$(dirname "$0")/_common.sh"
JOBID="${1:?Usage: wait-job.sh <jobid>}"

START=$(date +%s)
while true; do
  JOB=$(api_poll GET "jobs/$(enc "$JOBID")")
  STATUS=$(jq -r .status <<< "$JOB")
  if [ "$STATUS" = completed ] || [ "$STATUS" = failed ]; then break; fi
  log "job $STATUS ($(( $(date +%s) - START )) s)"
  sleep 10
done
echo "$JOB"
if [ "$STATUS" = completed ]; then
  log "job completed after $(( $(date +%s) - START )) s: $(jq -r '.result | [
      (if .duration then "\(.duration) s at \(.resolution) \(.width)x\(.height)" else "\(.width)x\(.height)" end),
      (if .quota.video then "\(.quota.video.left) s of video left this month"
       elif .quota.image then "\(.quota.image.left) images left this month"
       elif .quota.avatarVideo then "\(.quota.avatarVideo.left) AI avatar videos left this month"
       else empty end)
    ] | join(", ")' <<< "$JOB")"
  exit 0
fi
ERRCODE=$(jq -r '.error.code // 0' <<< "$JOB")
echo "Job failed ($ERRCODE): $(jq -r '.error.message // .error' <<< "$JOB")" >&2
TMP=$(mktemp)
jq -r '.error.message // ""' <<< "$JOB" > "$TMP"
hint "$ERRCODE" "$TMP"
rm -f "$TMP"
exit 1
