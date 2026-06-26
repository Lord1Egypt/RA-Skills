#!/bin/bash
# Poll Squad Control for pending/review/stuck tasks
# Called by the agent's cron job
# Requires: SC_API_URL and SC_API_KEY environment variables

set -euo pipefail

SC_API_URL="${SC_API_URL:?SC_API_URL not set}"
SC_API_KEY="${SC_API_KEY:?SC_API_KEY not set}"

# Concurrency guard: prevent overlapping poll runs.
LOCK_DIR="${TMPDIR:-/tmp}/squad-control-poll.lock"
LOCK_TTL_SEC="${SC_POLL_LOCK_TTL_SEC:-240}" # 4 min default, below 5m cron interval

cleanup_lock() {
  rm -rf "$LOCK_DIR" 2>/dev/null || true
}

acquire_lock() {
  local now epoch lock_ts age
  epoch=$(date +%s)

  if mkdir "$LOCK_DIR" 2>/dev/null; then
    echo "$epoch" > "$LOCK_DIR/ts"
    trap cleanup_lock EXIT
    return 0
  fi

  lock_ts=$(cat "$LOCK_DIR/ts" 2>/dev/null || echo 0)
  age=$(( epoch - lock_ts ))

  # Clear stale lock, then retry once.
  if [ "$age" -gt "$LOCK_TTL_SEC" ]; then
    rm -rf "$LOCK_DIR" 2>/dev/null || true
    if mkdir "$LOCK_DIR" 2>/dev/null; then
      echo "$epoch" > "$LOCK_DIR/ts"
      trap cleanup_lock EXIT
      return 0
    fi
  fi

  # Another run is active. Quietly ack.
  echo "HEARTBEAT_OK"
  exit 0
}

acquire_lock

CURL_CONNECT_TIMEOUT="${SC_POLL_CONNECT_TIMEOUT_SEC:-5}"
CURL_MAX_TIME="${SC_POLL_MAX_TIME_SEC:-20}"
CURL_RETRIES="${SC_POLL_RETRIES:-3}"
CURL_RETRY_DELAY="${SC_POLL_RETRY_DELAY_SEC:-1}"

fetch_json() {
  local endpoint="$1"
  curl -sSL \
    --connect-timeout "$CURL_CONNECT_TIMEOUT" \
    --max-time "$CURL_MAX_TIME" \
    --retry "$CURL_RETRIES" \
    --retry-delay "$CURL_RETRY_DELAY" \
    --retry-all-errors \
    --retry-connrefused \
    --fail \
    "${SC_API_URL}${endpoint}" \
    -H "x-api-key: ${SC_API_KEY}" 2>/dev/null
}

poll_started_ms=$(date +%s%3N)

pending_response=$(fetch_json "/api/tasks/pending") || {
  echo "ERROR: Failed to reach Squad Control API at ${SC_API_URL}"
  exit 1
}

review_response=$(fetch_json "/api/tasks/list?status=review") || {
  echo "WARN: review fetch failed, continuing with empty review set" >&2
  review_response='{"tasks":[]}'
}
working_response=$(fetch_json "/api/tasks/list?status=working") || {
  echo "WARN: working fetch failed, continuing with empty working set" >&2
  working_response='{"tasks":[]}'
}

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
parser_out=$(python3 "$SCRIPT_DIR/poll-parser.py" <<JSON
{"pending": ${pending_response}, "review": ${review_response}, "working": ${working_response}}
JSON
)

# Optional metrics line for operators/debuggers.
poll_finished_ms=$(date +%s%3N)
elapsed_ms=$((poll_finished_ms - poll_started_ms))
echo "POLL_METRICS: {\"elapsedMs\": ${elapsed_ms}, \"connectTimeoutSec\": ${CURL_CONNECT_TIMEOUT}, \"maxTimeSec\": ${CURL_MAX_TIME}, \"retries\": ${CURL_RETRIES}}" >&2

echo "$parser_out"
