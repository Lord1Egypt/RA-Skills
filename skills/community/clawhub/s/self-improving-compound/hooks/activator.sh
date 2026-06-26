#!/usr/bin/env bash
# activator.sh — Surface relevant Pattern-Keys from SQLite at session start.
# No fallbacks to legacy markdown files — SQLite is the only source of truth.
set -euo pipefail

WORKSPACE_ROOT="${OPENCLAW_WORKSPACE:-$(pwd)}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
LEARNINGS_CLI="$SCRIPT_DIR/scripts/learnings.py"

CONTEXT="${1:-}"

# Exit quietly if the CLI doesn't exist
if [ ! -f "$LEARNINGS_CLI" ]; then
    exit 0
fi

STATUS_JSON="$(python3 "$LEARNINGS_CLI" --root "$WORKSPACE_ROOT" status --format json 2>/dev/null || true)"
if [ -z "$STATUS_JSON" ]; then
    exit 0
fi

MATCHES="$(printf '%s' "$STATUS_JSON" | python3 -c '
import json, sys
try:
    data = json.load(sys.stdin)
except Exception:
    sys.exit(0)
for item in data.get("hot_entities", [])[:5]:
    entity = item.get("entity_id", "")
    if entity.startswith("pattern-key:"):
        print("{:.2f} {}".format(float(item.get("score", 0)), entity.split(":", 1)[1]))
' 2>/dev/null || true)"

if [ -n "$MATCHES" ]; then
    echo ""
    echo "[activator] Active Pattern-Keys:"
    echo "$MATCHES" | while read -r SCORE KEY; do
        printf "  - %s (score: %s)\n" "$KEY" "$SCORE"
    done
    echo ""
fi
