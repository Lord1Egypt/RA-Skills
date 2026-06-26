#!/usr/bin/env bash
set -euo pipefail

WORKSPACE="${OPENCLAW_WORKSPACE:-$HOME/.openclaw/workspace}"
MEMORY_DIR="$WORKSPACE/memory"
STATE_FILE="$MEMORY_DIR/it-events-sent.json"

INTERESTS="${1:-}"

if [[ -z "$INTERESTS" ]]; then
  echo "Помилка: передай IT-напрями одним аргументом."
  echo 'Приклад: bash scripts/search-events.sh "Python, AI, Data Science"'
  exit 1
fi

if ! command -v openclaw >/dev/null 2>&1; then
  echo "Помилка: команда openclaw не знайдена в PATH."
  exit 1
fi

mkdir -p "$MEMORY_DIR"

if [[ ! -f "$STATE_FILE" ]]; then
  cat > "$STATE_FILE" <<'EOF'
{
  "sent": []
}
EOF
  echo "Створив state file: $STATE_FILE"
fi

PROMPT="Use the it_events skill. Find new future IT events in Ukraine for these interests: $INTERESTS. Exclude events already listed in memory/it-events-sent.json. Return the answer in Ukrainian. After producing the result, update memory/it-events-sent.json."

openclaw agent --message "$PROMPT"
