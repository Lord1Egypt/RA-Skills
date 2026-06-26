#!/usr/bin/env bash
set -euo pipefail

JOB_NAME="UA IT Events Weekly"
TIMEZONE="Europe/Kiev"
CRON_EXPR="0 9 * * 1"

WORKSPACE="${OPENCLAW_WORKSPACE:-$HOME/.openclaw/workspace}"
MEMORY_DIR="$WORKSPACE/memory"
STATE_FILE="$MEMORY_DIR/it-events-sent.json"

INTERESTS="${1:-}"

if [[ -z "$INTERESTS" ]]; then
  echo "Помилка: передай IT-напрями одним аргументом."
  echo 'Приклад: bash scripts/setup-cron.sh "JavaScript, Frontend, React"'
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

MESSAGE="Use the it_events skill. Find new future IT events in Ukraine that match these user interests: $INTERESTS. Exclude events already stored in memory/it-events-sent.json. Return the digest in Ukrainian. After sending the result, update memory/it-events-sent.json."

EXISTING_JOB_ID="$(openclaw cron list 2>/dev/null | awk -v name="$JOB_NAME" '
  BEGIN { FS="[[:space:]][[:space:]]+" }
  $0 ~ name { print $1; exit }
')"

if [[ -n "${EXISTING_JOB_ID:-}" ]]; then
  echo "Знайшов існуючий cron job: $EXISTING_JOB_ID"
  echo "Онови його вручну через UI або видали й створи заново."
  echo
  echo "Щоб видалити старий job, якщо треба:"
  echo "openclaw cron delete $EXISTING_JOB_ID"
  echo
fi

openclaw cron add \
  --name "$JOB_NAME" \
  --cron "$CRON_EXPR" \
  --tz "$TIMEZONE" \
  --session isolated \
  --message "$MESSAGE"

echo
echo "Готово."
echo "Cron job додано."
echo "Назва: $JOB_NAME"
echo "Розклад: $CRON_EXPR ($TIMEZONE)"
echo "Інтереси: $INTERESTS"
echo "State file: $STATE_FILE"
echo
echo "Перевірити:"
echo "openclaw cron list"
