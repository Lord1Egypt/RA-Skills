#!/usr/bin/env bash
# Poll a job every 10 seconds until it is completed or failed, then print the final job record (JSON).
# Usage: wait-job.sh <jobid> > job.json
# An image usually takes 20 to 60 seconds, a video 60 to 140 (swapping a person in a video takes the longest).
# Reading a job is free: a network error, 429 or 5xx answer is retried. Safe to re-run on the same job id to resume.
# Exits 1 if the job failed, with a hint that says whether running it again is safe.
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
  log "job completed after $(( $(date +%s) - START )) s: $(jq -r '[(.result.assets[0] | "\(.type) \(.mime), \(.bytes) bytes"), (.result.text // empty | "Muse: \(.)")] | join(". ")' <<< "$JOB")"
  exit 0
fi
ERRCODE=$(jq -r '.error.code // 0' <<< "$JOB")
echo "Job failed ($ERRCODE): $(jq -r '(.error.message // .error | tostring) + (if .error.retryAt? then " (retryAt \(.error.retryAt))" else "" end)' <<< "$JOB")" >&2
TMP=$(mktemp)
jq -r '.error.message // ""' <<< "$JOB" > "$TMP"
hint "$ERRCODE" "$TMP"
rm -f "$TMP"
exit 1
