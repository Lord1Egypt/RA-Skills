#!/bin/bash
# Cron-friendly performance check — alerts on degradation
# Usage: ./check_vector_search_performance.sh
#
# Security manifest:
#   Env vars: none (reads only local files and runs local Node.js)
#   External endpoints: none
#   Files read: vector search report logs under HISTORY_DIR
#   Files written: HISTORY_DIR/$DATE.json (performance snapshot)
set -euo pipefail

NODE="/usr/bin/node"
SCRIPT="/home/openclaw/.openclaw/skills/rag-memory/scripts/analyze_vector_search.js"
HISTORY_DIR="/home/openclaw/.openclaw/workspace/logs/vector_search_reports"
ALERT_HIT_RATE=0.70   # below 70% hit rate → alert
ALERT_MAX_SCORE=0.75  # average top score below this → alert
ALERT_DURATION=500    # average latency above ms → alert

# Get latest report
REPORT_JSON=$(node "$SCRIPT" 2>/dev/null)
if [ $? -ne 0 ]; then
  echo "ERROR: analyzer failed"
  exit 1
fi

# Save today's snapshot
DATE=$(date +%F)
echo "$REPORT_JSON" > "$HISTORY_DIR/$DATE.json"

# Parse values using jq (must be installed)
HIT_RATE=$(echo "$REPORT_JSON" | jq -r '.hit_rate // "null"')
MAX_SCORE=$(echo "$REPORT_JSON" | jq -r '.avg_max_score // "null"')
DURATION=$(echo "$REPORT_JSON" | jq -r '.avg_duration_ms // "null"')
QUERIES=$(echo "$REPORT_JSON" | jq -r '.entries_total // 0')

# Compare to previous 3-day average if available
# (skip for the first few days)
# For now, only threshold alerts without baseline diff

ALERT=""
if [ "$HIT_RATE" != "null" ] && python3 -c "import sys; sys.exit(0 if $HIT_RATE < $ALERT_HIT_RATE else 1)"; then
  ALERT="LOW_HIT_RATE(${HIT_RATE}) "
fi
if [ "$MAX_SCORE" != "null" ] && python3 -c "import sys; sys.exit(0 if $MAX_SCORE < $ALERT_MAX_SCORE else 1)"; then
  ALERT="${ALERT}LOW_MAX_SCORE(${MAX_SCORE}) "
fi
if [ "$DURATION" != "null" ] && python3 -c "import sys; sys.exit(0 if $DURATION > $ALERT_DURATION else 1)"; then
  ALERT="${ALERT}HIGH_LATENCY(${DURATION}ms) "
fi

if [ -n "$ALERT" ]; then
  echo "ALERT: $ALERT | Queries: $QUERIES | Hit: $HIT_RATE | Score: $MAX_SCORE | Dur: ${DURATION}ms"
  # Could send Telegram message here if message tool available in a session.
else
  echo "OK: Queries: $QUERIES | Hit: $HIT_RATE | Score: $MAX_SCORE | Dur: ${DURATION}ms"
fi