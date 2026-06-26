#!/bin/bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
WORKSPACE_ROOT="${OPENCLAW_WORKSPACE:-$(cd "$SKILL_DIR/../.." && pwd)}"
DATA_DIR="${TWITTER_WATCH_REPLY_DATA_DIR:-$WORKSPACE_ROOT/data/twitter-watch-reply}"
INTERVAL="${TWITTER_WATCH_REPLY_INTERVAL_SECONDS:-30}"
mkdir -p "$DATA_DIR"
LOG="$DATA_DIR/watch-loop.log"
cd "$WORKSPACE_ROOT"
while true; do
  {
    echo "===== $(date '+%Y-%m-%d %H:%M:%S %Z') interval=${INTERVAL}s ====="
    python3 "$SKILL_DIR/scripts/fetch_latest_tweets.py"
    python3 "$SKILL_DIR/scripts/pick_pending_tweet.py"
    echo
  } >> "$LOG" 2>&1 || true
  sleep "$INTERVAL"
done
