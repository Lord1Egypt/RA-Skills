#!/bin/bash
# session_state.sh — Per-agent session state persistence
# v1.1.0
# Usage: session_state.sh <agent_id> <get|inc|reset|trigger|complete|should>

set -euo pipefail

AGENT_ID="${1:-main}"
LEARNINGS_DIR="${LEARNINGS_DIR:-$HOME/.openclaw/workspace/agents/$AGENT_ID/.learnings}"
STATE_FILE="$LEARNINGS_DIR/.session_state.json"
MAX_MESSAGES=10   # threshold: N messages before self-review

mkdir -p "$LEARNINGS_DIR"

init_state() {
    if [ ! -f "$STATE_FILE" ]; then
        cat > "$STATE_FILE" << 'EOF'
{
  "agent_id": "__AGENT_ID__",
  "message_count": 0,
  "review_triggered": false,
  "review_completed": false,
  "session_started_at": "__TS__"
}
EOF
        sed -i "s/__AGENT_ID__/$AGENT_ID/g" "$STATE_FILE"
        sed -i "s/__TS__/$(date +%s)/g" "$STATE_FILE"
    fi
}

read_state() {
    init_state
    cat "$STATE_FILE"
}

inc_message_count() {
    init_state
    local count
    count=$(node -e "
const fs = require('fs');
let d = JSON.parse(fs.readFileSync('$STATE_FILE', 'utf8'));
d.message_count++;
fs.writeFileSync('$STATE_FILE', JSON.stringify(d, null, 2));
console.log(d.message_count);
")
    echo "$count"
}

trigger_review() {
    init_state
    node -e "
const fs = require('fs');
let d = JSON.parse(fs.readFileSync('$STATE_FILE', 'utf8'));
d.review_triggered = true;
d.message_count++;
fs.writeFileSync('$STATE_FILE', JSON.stringify(d, null, 2));
"
}

complete_review() {
    init_state
    node -e "
const fs = require('fs');
let d = JSON.parse(fs.readFileSync('$STATE_FILE', 'utf8'));
d.review_completed = true;
d.review_triggered = false;  // allow re-trigger for next task in same session
fs.writeFileSync('$STATE_FILE', JSON.stringify(d, null, 2));
"
}

reset_session() {
    rm -f "$STATE_FILE"
}

should_trigger() {
    init_state
    local count threshold triggered
    count=$(node -e "console.log(JSON.parse(require('fs').readFileSync('$STATE_FILE')).message_count)" 2>/dev/null || echo 0)
    threshold=$MAX_MESSAGES
    triggered=$(node -e "console.log(JSON.parse(require('fs').readFileSync('$STATE_FILE')).review_triggered)" 2>/dev/null || echo false)
    # Trigger if: count >= threshold AND no review is currently in progress
    # After complete_review() resets triggered=false, next threshold crossing re-triggers
    [ "$count" -ge "$threshold" ] && [ "$triggered" = "false" ] && echo "yes" || echo "no"
}

case "${2:-get}" in
    get)        read_state ;;
    inc)        inc_message_count ;;
    reset)      reset_session ;;
    trigger)    trigger_review ;;
    complete)   complete_review ;;
    should)     should_trigger ;;
    *)          echo "Usage: session_state.sh <agent_id> <get|inc|reset|trigger|complete|should>" ;;
esac