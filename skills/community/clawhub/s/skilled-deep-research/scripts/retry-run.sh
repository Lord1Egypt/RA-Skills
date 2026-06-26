#!/usr/bin/env bash
# retry-run.sh — Spawn a worker to re-attempt failed URL fetches from the retry queue.
# Usage: retry-run.sh <slug> [--output /path/to/final-report.md]
#
# Reads retry-queue.md, spawns a focused retry worker via Ada's session,
# and prints the sessions_spawn call to stdout for Ada to execute.
# (Ada must run the actual spawn — this script just prepares the task.)

set -euo pipefail

SLUG="${1:?Usage: retry-run.sh <slug>}"
OUTPUT="${2:-}"
WORKSPACE="${OPENCLAW_WORKSPACE:-$HOME/.openclaw/workspace}"
DATA_DIR="$WORKSPACE/skills-data/skilled-deep-research/$SLUG"
RETRY_FILE="$DATA_DIR/workers/retry-queue.md"

if [[ ! -f "$RETRY_FILE" ]]; then
  echo "No retry queue found at: $RETRY_FILE"
  exit 0
fi

RETRY_COUNT=$(grep -c '^- ' "$RETRY_FILE" 2>/dev/null || echo 0)

if [[ "$RETRY_COUNT" -eq 0 ]]; then
  echo "Retry queue is empty — nothing to retry."
  exit 0
fi

echo "Retry queue: $RETRY_COUNT URLs pending"
echo ""
echo "URLs to retry:"
grep '^- ' "$RETRY_FILE" | head -20
echo ""
echo "---"
echo "Spawn this retry worker via Ada:"
echo ""
cat <<EOF
sessions_spawn(
  task: "You are a retry worker for research run: $SLUG
Topic: $(python3 -c "import json; d=json.load(open('$DATA_DIR/meta.json')); print(d.get('topic','unknown'))" 2>/dev/null || echo 'unknown')
Data dir: $DATA_DIR

Your job: re-attempt every URL listed in $RETRY_FILE
For each URL:
1. Try the fetch script first:
   /home/sean/.openclaw/workspace/lab/skills/ddg-search/scripts/fetch <url>
2. If that fails (403/bot-block), try Playwright:
   mcporter call playwright.browser_navigate url=<url>
   mcporter call playwright.browser_snapshot
3. If still fails, note as permanently failed in results.md

Use the same results.md format as defined in SKILL.md.
Append to: $DATA_DIR/workers/retry-results.md
Update heartbeat: $DATA_DIR/workers/retry-progress.json

When done, run:
  python3 ~/.openclaw/workspace/skills/skilled-deep-research/scripts/merge-reports.py $SLUG${OUTPUT:+ --output $OUTPUT}",
  label: "research-$SLUG-retry",
  model: "google/gemini-2.5-flash",
  runTimeoutSeconds: 1800
)
EOF
