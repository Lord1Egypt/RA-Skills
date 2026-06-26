#!/bin/bash
# view-failed-logs.sh — View failed logs for Publish Skills workflow
# Usage: ./scripts/view-failed-logs.sh [RUN_ID]
#   With RUN_ID: view that run's failed logs
#   Without: show latest run and prompt to view if failed

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$REPO_ROOT"

RUN_ID="${1:-}"

if [ -n "$RUN_ID" ]; then
  echo "📋 Failed logs for run $RUN_ID"
  gh run view "$RUN_ID" --log-failed
  exit 0
fi

# No run ID: show latest runs and suggest
echo "📋 Latest Publish Skills runs:"
gh run list --workflow=publish.yml --limit 5

echo ""
echo "💡 To view failed logs: ./scripts/view-failed-logs.sh <RUN_ID>"
echo "   Or: gh run view <RUN_ID> --log-failed"
echo "   Run ID is in the notification (e.g. #12345) or from the list above."
