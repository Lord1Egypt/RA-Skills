#!/usr/bin/env bash
# Watch openclaw-uninstall publish pipeline. Polls GitHub Actions until complete.
# Usage: ./scripts/watch-publish-pipeline.sh [--repo OWNER/REPO]
# Notifies via macOS osascript when done. Run in background: ./scripts/watch-publish-pipeline.sh &

set -e

REPO="${1:-ERerGB/openclaw-uninstall}"
[[ "$1" == "--repo" ]] && { REPO="$2"; shift 2; }
LOG="/tmp/openclaw-uninstall-publish-watch.log"
POLL_INTERVAL=20
TIMEOUT=600  # 10 min

log() { echo "[$(date '+%H:%M:%S')] $*" | tee -a "$LOG"; }

notify() {
  local title="$1"
  local body="$2"
  if [[ "$(uname -s)" == "Darwin" ]]; then
    osascript -e "display notification \"$body\" with title \"$title\"" 2>/dev/null || true
  fi
  log "NOTIFY: $title - $body"
}

log "=== Watching publish pipeline: $REPO ==="

# Get latest run ID for "Publish Skills" workflow
RUN_ID=""
for i in $(seq 1 30); do
  RUN_ID=$(gh run list -R "$REPO" -w "Publish Skills" -L 1 --json databaseId -q '.[0].databaseId' 2>/dev/null) || true
  [[ -n "$RUN_ID" ]] && break
  log "Waiting for workflow to appear... ($i/30)"
  sleep 5
done

if [[ -z "$RUN_ID" ]]; then
  log "ERROR: Could not find Publish Skills run"
  notify "Publish Pipeline" "Failed to find workflow run"
  exit 1
fi

log "Watching run $RUN_ID (gh run watch $RUN_ID -R $REPO)"

ELAPSED=0
while (( ELAPSED < TIMEOUT )); do
  STATUS=$(gh run view "$RUN_ID" -R "$REPO" --json status,conclusion -q '.status + " " + (.conclusion // "null")' 2>/dev/null) || true
  log "Status: $STATUS"

  if [[ "$STATUS" == completed* ]]; then
    CONCLUSION=$(gh run view "$RUN_ID" -R "$REPO" --json conclusion -q '.conclusion' 2>/dev/null)
    if [[ "$CONCLUSION" == "success" ]]; then
      notify "Publish Pipeline" "All jobs completed successfully"
      log "SUCCESS"
      exit 0
    else
      notify "Publish Pipeline" "Failed: $CONCLUSION"
      log "FAILED: $CONCLUSION"
      gh run view "$RUN_ID" -R "$REPO" --log-failed 2>/dev/null | tail -50 >> "$LOG" || true
      exit 1
    fi
  fi

  sleep "$POLL_INTERVAL"
  ELAPSED=$((ELAPSED + POLL_INTERVAL))
done

log "TIMEOUT after ${TIMEOUT}s"
notify "Publish Pipeline" "Timeout - check $LOG"
exit 1
