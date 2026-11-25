#!/usr/bin/env bash
# Poll a Zooop task until it reaches a terminal state, then print the final
# JSON. Terminal states: succeeded, failed, cancelled.
#
# Usage:  poll.sh <taskId>           # poll every 3s, give up after 20 min
#         poll.sh <taskId> 5 60      # poll every 5s, max 60 attempts (= 5 min)
set -euo pipefail

: "${ZOOOP_API_KEY:?ZOOOP_API_KEY must be set}"
HOST="${ZOOOP_API_HOST:-https://api.zooop.ai}"

if [[ $# -lt 1 ]]; then
  echo "usage: $0 <taskId> [intervalSeconds] [maxAttempts]" >&2
  exit 64
fi

TASK_ID="$1"
INTERVAL="${2:-3}"
MAX_ATTEMPTS="${3:-400}"  # 400 × 3s ≈ 20 min

for ((i = 0; i < MAX_ATTEMPTS; i++)); do
  RESPONSE=$(curl -fsS "$HOST/v1/tasks/$TASK_ID" \
    -H "Authorization: Bearer $ZOOOP_API_KEY")

  # Cheap status extract — avoids a jq dependency. The substring match is
  # only used for the terminal-state break; full JSON is what we print.
  STATUS=$(printf '%s' "$RESPONSE" | grep -oE '"status":"[a-z_]+"' | head -1 | cut -d'"' -f4)

  case "$STATUS" in
    succeeded|failed|cancelled)
      printf '%s\n' "$RESPONSE"
      [[ "$STATUS" == "succeeded" ]] && exit 0 || exit 1
      ;;
    queued|running|"")
      sleep "$INTERVAL"
      ;;
    *)
      echo "unexpected status: $STATUS" >&2
      printf '%s\n' "$RESPONSE"
      exit 2
      ;;
  esac
done

echo "timed out after ${MAX_ATTEMPTS} attempts" >&2
exit 124
