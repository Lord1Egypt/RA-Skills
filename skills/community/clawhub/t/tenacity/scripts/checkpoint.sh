#!/bin/bash
# checkpoint.sh — Tenacity checkpoint manager
# Usage: checkpoint.sh <milestone_id> [state_json]
#        checkpoint.sh --resume

CHECKPOINT_DIR="${CHECKPOINT_DIR:-/tmp/tenacity-checkpoints}"
mkdir -p "$CHECKPOINT_DIR"

RESUME_FLAG="$1"

if [ "$RESUME_FLAG" = "--resume" ]; then
    # Find most recent incomplete checkpoint
    LATEST=$(ls -t "$CHECKPOINT_DIR"/checkpoint-*.json 2>/dev/null | head -1)
    if [ -z "$LATEST" ]; then
        echo "NO_CHECKPOINT"
        exit 1
    fi
    cat "$LATEST"
    exit 0
fi

MILESTONE="$1"
STATE_JSON="${2:-{}}"
TIMESTAMP=$(date -Iseconds)
CHECKPOINT_FILE="$CHECKPOINT_DIR/checkpoint-${MILESTONE}.json"

cat > "$CHECKPOINT_FILE" << EOF
{
  "milestone": "$MILESTONE",
  "state": $STATE_JSON,
  "timestamp": "$TIMESTAMP",
  "status": "IN_PROGRESS"
}
EOF

echo "CHECKPOINT_SAVED: $MILESTONE"
echo "State: $STATE_JSON"