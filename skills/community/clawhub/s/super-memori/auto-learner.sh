#!/bin/bash
# auto-learner.sh — Auto-discover learning candidates from command logs
# Usage: ./auto-learner.sh
# Runs during weekly review, finds repeated failures not yet in memory.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
LOG_FILE="$HOME/.openclaw/logs/commands.log"
PENDING_DIR="$HOME/.openclaw/data/super_memori_pending"
THRESHOLD="0.85"
EXCLUDE_REGEX='^(grep|find|sed|awk|test|\[|ls|cd|echo|cat|head|tail|wc|sort|uniq|date|whoami|hostname|pwd)'

mkdir -p "$PENDING_DIR"

# Check if commands.log exists
if [ ! -f "$LOG_FILE" ]; then
    echo "⚠️  commands.log not found. Auto-learner inactive."
    echo "   Configure PROMPT_COMMAND in ~/.bashrc to enable."
    exit 0
fi

# Parse similarity score from query-memory.sh human-readable output
check_sim() {
    local text="$1"
    local sim
    sim=$("$SCRIPT_DIR/query-memory.sh" "$text" 2>/dev/null | \
        grep -oE '(score|similarity):? ?[0-9.]+' | head -1 | grep -oE '[0-9.]+' || echo "0")
    echo "${sim:-0}"
}

# Create pending JSON for a candidate
create_pending() {
    local cmd="$1" code="$2" ts="$3"
    local id="auto_$(date +%Y%m%d_%H%M%S)_$$"
    local title="${cmd:0:60} failed with exit $code"
    # Extract likely tags from command
    local tags="auto-discovered"
    
    cat > "$PENDING_DIR/$id.json" << JSONEOF
{
  "id": "$id",
  "type": "error",
  "auto_discovered": true,
  "reviewed": false,
  "created_at": "$(date -Iseconds)",
  "source_command": "$cmd",
  "exit_code": $code,
  "timestamp": "$ts",
  "suggested_title": "$title",
  "suggested_tags": ["$tags"]
}
JSONEOF
    echo "  → Pending: $title"
}

# Main loop: parse commands.log
seven_days_ago=$(date -d '7 days ago' +%s 2>/dev/null || date -v-7d +%s 2>/dev/null || echo "0")
new_count=0
skip_count=0

while IFS= read -r line; do
    # Expected format: 2026-04-05T14:23:10+08:00 | exit:2 | cmd:systemctl restart postgresql
    if [[ "$line" =~ ([0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}[^\ ]*)\ \|\ exit:([0-9]+)\ \|\ cmd:(.*) ]]; then
        ts="${BASH_REMATCH[1]}"
        code="${BASH_REMATCH[2]}"
        cmd="${BASH_REMATCH[3]}"
        
        # Skip exit 0 and 1 (grep no-match, etc.)
        [ "$code" -eq 0 ] && continue
        [ "$code" -eq 1 ] && continue
        
        # Skip trivial commands
        [[ "$cmd" =~ $EXCLUDE_REGEX ]] && continue
        
        # Check time window (7 days)
        ts_epoch=$(date -d "$ts" +%s 2>/dev/null || echo "0")
        [ "$ts_epoch" -lt "$seven_days_ago" ] && continue
        
        # Check if similar knowledge already exists
        sim=$(check_sim "$cmd")
        if (( $(echo "$sim >= $THRESHOLD" | bc -l 2>/dev/null || echo "0") )); then
            skip_count=$((skip_count + 1))
            continue
        fi
        
        create_pending "$cmd" "$code" "$ts"
        new_count=$((new_count + 1))
    fi
done < "$LOG_FILE"

echo "=== Auto-learner done: $new_count new, $skip_count already known. Pending: $(find "$PENDING_DIR" -name '*.json' 2>/dev/null | wc -l) files ==="
