#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
CONFIG_FILE="$SKILL_DIR/config.json"
FORCE="${ROC_FORCE_REREGISTER:-0}"

get_existing_agent_name() {
  if [ ! -f "$CONFIG_FILE" ]; then
    return 0
  fi
  if command -v jq >/dev/null 2>&1; then
    jq -r '.agent_name // empty' "$CONFIG_FILE" 2>/dev/null || true
    return 0
  fi
  sed -n 's/.*"agent_name"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p' "$CONFIG_FILE" | head -n 1
}

EXISTING_NAME="$(get_existing_agent_name || true)"
if [ "$FORCE" != "1" ] && [ -n "${EXISTING_NAME:-}" ]; then
  echo "ranking-of-claws: already registered as \"$EXISTING_NAME\" (config.json kept)."
  echo "To re-register: ROC_FORCE_REREGISTER=1 bash scripts/install.sh"
  bash "$SCRIPT_DIR/setup-cron.sh"
  exit 0
fi

DEFAULT_NAME="${RANKING_AGENT_NAME:-$(hostname)}"
AGENT_NAME=""

if [ -t 0 ]; then
  read -r -p "Agent name? " AGENT_NAME
fi

AGENT_NAME="${AGENT_NAME:-$DEFAULT_NAME}"
COUNTRY="${RANKING_COUNTRY:-XX}"
RAW_ID="$(hostname)-${HOME:-}-openclaw"
GATEWAY_ID="$(printf '%s' "$RAW_ID" | sha256sum | awk '{print $1}' | cut -c1-16)"
REGISTERED_AT="$(date -u +"%Y-%m-%dT%H:%M:%SZ")"

cat > "$CONFIG_FILE" <<EOF
{
  "agent_name": "$AGENT_NAME",
  "country": "$COUNTRY",
  "gateway_id": "$GATEWAY_ID",
  "registered_at": "$REGISTERED_AT"
}
EOF

echo "ranking-of-claws: registered \"$AGENT_NAME\" -> $CONFIG_FILE"
bash "$SCRIPT_DIR/setup-cron.sh"
