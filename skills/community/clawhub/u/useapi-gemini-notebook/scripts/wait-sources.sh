#!/usr/bin/env bash
# Wait until Google has processed every source in the notebook (each one `ready` or `error`).
# Usage: wait-sources.sh <notebook>
# Prints one line per source (kind, status, title). Exits 1 if no source ended up ready,
# or if sources are still processing after 10 minutes. A network error or HTTP 5xx is retried up to 3 times.
source "$(dirname "$0")/_common.sh"
NOTEBOOK="${1:?Usage: wait-sources.sh <notebook>}"

POLLS=0
while true; do
  NB=$(api_poll GET "notebooks/$(enc "$NOTEBOOK")")
  if jq -e '[.sources[].status] | all(. == "ready" or . == "error")' <<< "$NB" > /dev/null; then break; fi
  POLLS=$((POLLS + 1))
  if [ "$POLLS" -ge 60 ]; then
    echo "Sources still processing after 10 minutes: $(jq -r '[.sources[].status] | join(", ")' <<< "$NB"). Run wait-sources.sh again later, or remove the stuck source." >&2
    exit 1
  fi
  log "sources: $(jq -r '[.sources[].status] | join(", ")' <<< "$NB")"
  sleep 10
done
jq -r '.sources[] | "\(.kind)\t\(.status)\t\(.title)"' <<< "$NB"
jq -e '[.sources[] | select(.status == "ready")] | length > 0' <<< "$NB" > /dev/null || { echo "No source is ready" >&2; exit 1; }
