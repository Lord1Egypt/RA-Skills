#!/usr/bin/env bash
# Poll a job every 10 seconds until it is completed or failed, then print the final job record (JSON).
# Usage: wait-job.sh <jobid> > job.json
# A song usually takes 40 to 150 seconds. Exits 1 if the job failed (for example a content refusal).
# A network error or HTTP 5xx is retried up to 3 times. Safe to re-run on the same job id to resume.
# The API marks a job failed with error.code "timeout" when its result has not arrived 20 minutes after it started.
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
log "job $STATUS after $(( $(date +%s) - START )) s"
[ "$STATUS" = completed ] || { echo "Job failed: $(jq -c .error <<< "$JOB")" >&2; exit 1; }
