#!/bin/bash

# Generic Twitter/X Automated Posting Template
# Customize the content functions below for your account/brand.
#
# Usage:
#   1. Set X_API_KEY, X_API_SECRET, X_ACCESS_TOKEN, X_ACCESS_TOKEN_SECRET
#   2. Edit get_content() with your own tweet templates
#   3. Run: ./generic-post.sh
#
# Controls:
#   MAX_POSTS_PER_DAY  — max tweets per day (default: 3)
#   COOLDOWN_HOURS     — minimum hours between posts (default: 3)

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
STATE_DIR="${OPENCLAW_STATE_DIR:-$HOME/.openclaw/x-poster}"
LOG_FILE="$STATE_DIR/post.log"
STATE_FILE="$STATE_DIR/state.json"

MAX_POSTS_PER_DAY="${MAX_POSTS_PER_DAY:-3}"
COOLDOWN_HOURS="${COOLDOWN_HOURS:-3}"

mkdir -p "$STATE_DIR"

# Initialize state if missing
if [ ! -f "$STATE_FILE" ]; then
  echo '{"lastPost": null, "postsToday": 0, "lastReset": null}' > "$STATE_FILE"
fi

log() {
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

post_tweet() {
  local text="$1"
  log "Posting tweet: $text"
  node "$SCRIPT_DIR/bin/x.js" post "$text" 2>&1 | tee -a "$LOG_FILE"
}

# ─── CUSTOMIZE THIS FUNCTION ───────────────────────────────────────
# Return a tweet string. Use $hour for time-based content.
# Replace these examples with your own content.
get_content() {
  local hour=$(date +%H)

  if [ "$hour" -ge 6 ] && [ "$hour" -lt 12 ]; then
    echo "Good morning! Here's your daily update. #YourHashtag"
  elif [ "$hour" -ge 12 ] && [ "$hour" -lt 18 ]; then
    echo "Afternoon thought: customize this template with your own content!"
  else
    echo "Evening check-in. What did you build today? #YourHashtag"
  fi
}
# ────────────────────────────────────────────────────────────────────

main() {
  log "=== Automated Post Script Started ==="

  local today=$(date +%Y-%m-%d)
  local last_reset=$(jq -r '.lastReset' "$STATE_FILE" 2>/dev/null || echo "null")

  # Reset counter on new day
  if [ "$last_reset" != "$today" ]; then
    log "New day — resetting post counter."
    jq --arg today "$today" '.postsToday = 0 | .lastReset = $today' "$STATE_FILE" > "${STATE_FILE}.tmp" && mv "${STATE_FILE}.tmp" "$STATE_FILE"
  fi

  local posts_today=$(jq -r '.postsToday' "$STATE_FILE")
  local last_post=$(jq -r '.lastPost' "$STATE_FILE")

  # Check daily limit
  if [ "$posts_today" -ge "$MAX_POSTS_PER_DAY" ]; then
    log "Daily limit ($MAX_POSTS_PER_DAY) reached. Skipping."
    exit 0
  fi

  # Check cooldown
  if [ "$last_post" != "null" ]; then
    local last_ts=$(date -j -f "%Y-%m-%dT%H:%M:%S" "$last_post" +%s 2>/dev/null || echo "0")
    local now=$(date +%s)
    local hours_since=$(( (now - last_ts) / 3600 ))
    if [ "$hours_since" -lt "$COOLDOWN_HOURS" ]; then
      log "Cooldown: ${hours_since}h since last post (need ${COOLDOWN_HOURS}h). Skipping."
      exit 0
    fi
  fi

  local content=$(get_content)
  if [ -n "$content" ]; then
    post_tweet "$content"
    local timestamp=$(date +%Y-%m-%dT%H:%M:%S)
    jq --arg ts "$timestamp" '.lastPost = $ts | .postsToday += 1' "$STATE_FILE" > "${STATE_FILE}.tmp" && mv "${STATE_FILE}.tmp" "$STATE_FILE"
    log "✅ Tweet posted successfully"
  else
    log "❌ No content generated"
    exit 1
  fi
}

main
