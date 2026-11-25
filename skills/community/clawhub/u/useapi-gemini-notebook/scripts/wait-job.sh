#!/usr/bin/env bash
# Poll a job every 15 seconds until it is completed or failed, then print the final job record (JSON).
# Usage: wait-job.sh <jobid> > job.json
# An Audio Overview usually takes 3 to 10 minutes, a slide deck about 7, a Video Overview 10 or more. Exits 1 if the job failed.
# A network error or HTTP 5xx is retried up to 3 times. Safe to re-run on the same job id to resume.
source "$(dirname "$0")/_common.sh"
JOBID="${1:?Usage: wait-job.sh <jobid>}"

START=$(date +%s)
while true; do
  JOB=$(api_poll GET "jobs/$(enc "$JOBID")")
  STATUS=$(jq -r .status <<< "$JOB")
  if [ "$STATUS" = completed ] || [ "$STATUS" = failed ]; then break; fi
  log "job $STATUS ($(( $(date +%s) - START )) s)"
  sleep 15
done
echo "$JOB"
log "job $STATUS after $(( $(date +%s) - START )) s"
[ "$STATUS" = completed ] || { echo "Job failed: $(jq -c .error <<< "$JOB")" >&2; exit 1; }
