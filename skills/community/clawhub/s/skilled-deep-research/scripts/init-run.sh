#!/usr/bin/env bash
# init-run.sh — Initialize a new research run data directory
# Usage: init-run.sh <slug> <topic> [output_dir]
#
# Creates the data directory structure for a new research run and
# writes meta.json. Safe to call multiple times (idempotent).

set -euo pipefail

SLUG="${1:?Usage: init-run.sh <slug> <topic> [output_dir]}"
TOPIC="${2:?Usage: init-run.sh <slug> <topic> [output_dir]}"
OUTPUT_DIR="${3:-}"

WORKSPACE="${OPENCLAW_WORKSPACE:-$HOME/.openclaw/workspace}"
DATA_DIR="$WORKSPACE/skills-data/skilled-deep-research/$SLUG"

mkdir -p "$DATA_DIR/workers"
touch "$DATA_DIR/known-urls.txt"

# Write meta.json
cat > "$DATA_DIR/meta.json" <<EOF
{
  "slug": "$SLUG",
  "topic": "$TOPIC",
  "output_dir": "$OUTPUT_DIR",
  "started": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "status": "running",
  "workers": []
}
EOF

echo "Initialized: $DATA_DIR"
echo "DATA_DIR=$DATA_DIR"
