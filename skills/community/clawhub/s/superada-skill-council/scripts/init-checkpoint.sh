#!/usr/bin/env bash
set -euo pipefail

LABEL="${1:?Usage: init-checkpoint.sh <label> [domain] [mode]}"
DOMAIN="${2:-mixed}"
MODE="${3:-quick}"
FILE="/tmp/self-heal-council-${LABEL}.json"

cat > "$FILE" <<EOF
{
  "task": "council-${LABEL}",
  "label": "${LABEL}",
  "domain": "${DOMAIN}",
  "mode": "${MODE}",
  "round": 0,
  "personas": [],
  "completed": [],
  "models_tried": [],
  "last_error": null,
  "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
}
EOF

echo "$FILE"
