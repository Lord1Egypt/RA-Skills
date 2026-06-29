#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_SCRIPT="${TOKEN_COST_GUARD_SKILL_SCRIPT:-}"
if [ -z "$SKILL_SCRIPT" ]; then
  if [ -f "$SCRIPT_DIR/token_cost_guard.py" ]; then
    SKILL_SCRIPT="$SCRIPT_DIR/token_cost_guard.py"
  else
    SKILL_SCRIPT="$HOME/.hermes/skills/autonomous-ai-agents/token-cost-guard/scripts/token_cost_guard.py"
  fi
fi

THRESHOLD_CNY="${TOKEN_COST_GUARD_HOURLY_THRESHOLD_CNY:-10}"

exec python3 "$SKILL_SCRIPT" \
  --source hermes \
  --period previous-hour \
  --alert-mode total \
  --threshold-cny "$THRESHOLD_CNY" \
  --quiet-ok \
  --alert-exit-zero \
  "$@"
