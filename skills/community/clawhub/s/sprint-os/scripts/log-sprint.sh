#!/usr/bin/env bash
# log-sprint.sh — CLI sprint logger for Sprint OS
# Writes to sprint-log.md and optionally POSTs to a Convex endpoint.
#
# Usage:
#   ./log-sprint.sh --project "my-project" --workstream "marketing" \
#     --task "Write homepage copy" --artifact "homepage-v2.md" \
#     --metric "awaiting test" --status completed
#
#   ./log-sprint.sh --daily-summary   # Print today's sprint count and top wins
#
# Environment:
#   CONVEX_SPRINT_URL  — Optional. Your Convex HTTP site URL.
#                        Example: https://your-deployment.convex.site

set -euo pipefail

# ─── Defaults ─────────────────────────────────────────────────────────────────
PROJECT=""
WORKSTREAM=""
TASK=""
ARTIFACT=""
METRIC=""
STATUS="completed"
BLOCKER=""
LOG_FILE="${SPRINT_LOG_FILE:-sprint-log.md}"
CONVEX_URL="${CONVEX_SPRINT_URL:-}"
DAILY_SUMMARY=false

# ─── Parse args ───────────────────────────────────────────────────────────────
while [[ $# -gt 0 ]]; do
  case "$1" in
    --project)      PROJECT="$2";      shift 2 ;;
    --workstream)   WORKSTREAM="$2";   shift 2 ;;
    --task)         TASK="$2";         shift 2 ;;
    --artifact)     ARTIFACT="$2";     shift 2 ;;
    --metric)       METRIC="$2";       shift 2 ;;
    --status)       STATUS="$2";       shift 2 ;;
    --blocker)      BLOCKER="$2";      shift 2 ;;
    --log-file)     LOG_FILE="$2";     shift 2 ;;
    --daily-summary) DAILY_SUMMARY=true; shift ;;
    --help|-h)
      echo "Usage: log-sprint.sh [options]"
      echo "  --project        Project name"
      echo "  --workstream     Workstream (marketing/development/content/etc.)"
      echo "  --task           What you did"
      echo "  --artifact       What was produced"
      echo "  --metric         What metric moved (or 'no movement')"
      echo "  --status         completed | partial | blocked"
      echo "  --blocker        Blocker description (if blocked)"
      echo "  --log-file       Path to sprint log file (default: sprint-log.md)"
      echo "  --daily-summary  Print today's sprint count and top wins"
      exit 0 ;;
    *) echo "Unknown option: $1"; exit 1 ;;
  esac
done

# ─── Daily summary mode ───────────────────────────────────────────────────────
if $DAILY_SUMMARY; then
  TODAY=$(date +%Y-%m-%d)
  if [[ ! -f "$LOG_FILE" ]]; then
    echo "No sprint log found at $LOG_FILE"
    exit 0
  fi
  SPRINT_COUNT=$(grep -c "^## Sprint" "$LOG_FILE" 2>/dev/null || echo 0)
  TODAY_COUNT=$(grep -c "$TODAY" "$LOG_FILE" 2>/dev/null || echo 0)
  echo "📊 Sprint OS — Daily Summary ($TODAY)"
  echo "Total sprints today: $TODAY_COUNT"
  echo "Total sprints all time: $SPRINT_COUNT"
  echo ""
  echo "--- Recent sprints ---"
  grep -A 6 "$TODAY" "$LOG_FILE" 2>/dev/null | head -40 || echo "(none)"
  exit 0
fi

# ─── Validate required args ───────────────────────────────────────────────────
if [[ -z "$TASK" ]]; then
  echo "❌ --task is required"
  exit 1
fi

# ─── Compute sprint number ────────────────────────────────────────────────────
SPRINT_NUM=1
if [[ -f "$LOG_FILE" ]]; then
  LAST=$(grep -c "^## Sprint" "$LOG_FILE" 2>/dev/null || echo 0)
  SPRINT_NUM=$((LAST + 1))
fi

TIMESTAMP=$(date "+%Y-%m-%d %H:%M")
EPOCH=$(date +%s)

# ─── Write to markdown log ────────────────────────────────────────────────────
{
  echo ""
  echo "## Sprint ${SPRINT_NUM} — ${TIMESTAMP}"
  echo ""
  [[ -n "$PROJECT" ]]    && echo "**Project:** ${PROJECT}"
  [[ -n "$WORKSTREAM" ]] && echo "**Workstream:** ${WORKSTREAM}"
  echo "**Task:** ${TASK}"
  [[ -n "$ARTIFACT" ]]   && echo "**Artifact:** ${ARTIFACT}"
  [[ -n "$METRIC" ]]     && echo "**Metric:** ${METRIC}"
  echo "**Status:** ${STATUS}"
  [[ -n "$BLOCKER" ]]    && echo "**Blocker:** ${BLOCKER}"
} >> "$LOG_FILE"

echo "✅ Sprint ${SPRINT_NUM} logged to ${LOG_FILE}"

# ─── Optionally POST to Convex ────────────────────────────────────────────────
if [[ -n "$CONVEX_URL" ]]; then
  PAYLOAD=$(cat <<EOF
{
  "sprintId": ${SPRINT_NUM},
  "project": "${PROJECT}",
  "workstream": "${WORKSTREAM}",
  "task": "${TASK}",
  "artifact": "${ARTIFACT}",
  "metric": "${METRIC}",
  "status": "${STATUS}",
  "owner": "agent",
  "timestamp": $((EPOCH * 1000))
}
EOF
)
  HTTP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" \
    -X POST "${CONVEX_URL}/sprints/log" \
    -H "Content-Type: application/json" \
    -d "$PAYLOAD")

  if [[ "$HTTP_STATUS" == "200" ]]; then
    echo "✅ Sprint logged to Convex (HTTP $HTTP_STATUS)"
  else
    echo "⚠️  Convex logging failed (HTTP $HTTP_STATUS) — local log preserved"
  fi
fi
