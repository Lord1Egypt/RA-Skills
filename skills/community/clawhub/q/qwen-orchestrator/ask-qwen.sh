#!/usr/bin/env bash
set -Eeuo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
TODAY=$(date '+%Y-%m-%d %H:%M %Z')

SEARCH_MODE=false
THINK_MODE=false
SESSION_NAME=""
USE_DAEMON=false
DRY_RUN=false
VISIBLE=false
WAIT_FOR_AUTH=false
CLOSE_BROWSER=false
DEBUG_MODE=false
VERBOSE_MODE=false
FORCE_STDIN=false
START_NEW_CHAT=false
END_SESSION=false
QUESTION=""
STDIN_TEXT=""

SESSION_ARGS=()
PUPPETEER_ARGS=()

while [[ $# -gt 0 ]]; do
  case "$1" in
    --search) SEARCH_MODE=true; shift ;;
    --session)
      SESSION_NAME="$2"
      SESSION_ARGS=(--session "$2")
      shift 2
      ;;
    --new-chat) START_NEW_CHAT=true; shift ;;
    --end-session) END_SESSION=true; shift ;;
    --daemon) USE_DAEMON=true; shift ;;
    --visible) VISIBLE=true; shift ;;
    --wait) WAIT_FOR_AUTH=true; shift ;;
    --dry-run) DRY_RUN=true; shift ;;
    --close) CLOSE_BROWSER=true; shift ;;
    --debug) DEBUG_MODE=true; shift ;;
    --verbose) VERBOSE_MODE=true; shift ;;
    --stdin) FORCE_STDIN=true; shift ;;
    --help|-h)
      cat <<'EOF'
ask-qwen.sh — Qwen Chat (chat.qwen.ai) via Puppeteer

USAGE (English):
  ask-qwen.sh "question"                  # single request
  ask-qwen.sh --session work "question"   # keep context in a named session
  ask-qwen.sh --search "query"            # enable Qwen web search
  ask-qwen.sh --daemon                     # use running daemon (faster)
  ask-qwen.sh --session work --new-chat "question"
  ask-qwen.sh --session work --end-session
  cat file.txt | ask-qwen.sh "analyze this"
  ask-qwen.sh --stdin < file.txt

FLAGS (English):
  --session NAME  Session name; preserves chat context between calls
  --search        Enable Qwen web search before sending the prompt
  --new-chat      Start a new Qwen chat inside the named session namespace
  --end-session   Delete saved session state
  --daemon        Use background Chrome daemon (~35ms startup)
  --visible       Open visible browser (auth / CAPTCHA repair)
  --wait          Wait for manual auth completion (with --visible)
  --dry-run       Check auth + composer without sending a prompt
  --stdin         Read prompt body from stdin
  --close         Close browser after answer
  --debug         Debug logs
  --verbose       More detailed logs
  -h, --help      Show this help

---

Использование:
  ask-qwen.sh "вопрос"                    — одиночный
  ask-qwen.sh --session work "вопрос"     — сессия
  ask-qwen.sh --search "запрос"           — с веб-поиском
  ask-qwen.sh --daemon                    — через демон (быстрее)
  ask-qwen.sh --session work --new-chat "вопрос"
  ask-qwen.sh --session work --end-session
  cat file.txt | ask-qwen.sh "проанализируй"
  ask-qwen.sh --stdin < file.txt

Флаги:
  --session NAME  Имя сессии (контекст сохраняется)
  --search        Включить веб-поиск Qwen
  --new-chat      Новый чат в сессии
  --end-session   Завершить сессию
  --daemon        Использовать фоновый Chrome (~35ms startup)
  --visible       Открыть видимый браузер (для авторизации)
  --wait          Ждать ручную авторизацию (с --visible)
  --dry-run       Проверить auth + composer без отправки
  --stdin         Читать промпт из stdin
  --close         Закрыть браузер после ответа
  --debug         Отладка
  --verbose       Подробный лог
  -h, --help      Справка

Демон:
  Запуск:   cd ~/.openclaw/workspace/skills/qwen-orchestrator
            bash scripts/setup-daemon.sh
  Останов:  pm2 stop qwen-daemon
EOF
      exit 0
      ;;
    --)
      shift
      while [[ $# -gt 0 ]]; do
        QUESTION="${QUESTION:+$QUESTION }$1"
        shift
      done
      ;;
    -*)
      echo "Неизвестный флаг: $1. Запусти --help"
      exit 1
      ;;
    *)
      QUESTION="${QUESTION:+$QUESTION }$1"
      shift
      ;;
  esac
done

# Read stdin
if [[ "$FORCE_STDIN" = true ]]; then
  if [[ -t 0 ]]; then
    echo "Ошибка: --stdin указан, но stdin не передан" >&2
    exit 1
  fi
  STDIN_TEXT=$(cat)
elif [[ ! -t 0 ]]; then
  STDIN_TEXT=$(cat)
fi

if [[ -n "$STDIN_TEXT" ]]; then
  if [[ -n "$QUESTION" ]]; then
    QUESTION="${QUESTION}"$'\n\n'"${STDIN_TEXT}"
  else
    QUESTION="$STDIN_TEXT"
  fi
fi

# End session
if [[ "$END_SESSION" = true ]]; then
  if [[ -n "$SESSION_NAME" ]]; then
    node "$SCRIPT_DIR/ask-puppeteer.js" "${SESSION_ARGS[@]}" --end-session >/dev/null 2>&1 || true
    rm -f "$SCRIPT_DIR/.sessions/${SESSION_NAME}.json"
    echo "Сессия '$SESSION_NAME' завершена"
  else
    echo "Ошибка: --end-session требует --session NAME" >&2
    exit 1
  fi
  exit 0
fi

# Need question (unless dry-run)
if [[ -z "$QUESTION" ]]; then
  if [[ "$DRY_RUN" = true ]]; then
    QUESTION="dry-run"
  else
    echo "Ошибка: нужен вопрос. ask-qwen.sh \"вопрос\"" >&2
    exit 1
  fi
fi

# Build full prompt
FULL_PROMPT="[Дата: ${TODAY}]"
[[ "$SEARCH_MODE" = true ]] && FULL_PROMPT="$FULL_PROMPT [РЕЖИМ: ПОИСК]"
FULL_PROMPT="$FULL_PROMPT $QUESTION"

# Pass flags
[[ "$SEARCH_MODE" = true ]] && PUPPETEER_ARGS+=(--search)
[[ -n "$SESSION_NAME" ]] && PUPPETEER_ARGS+=("${SESSION_ARGS[@]}")
[[ "$START_NEW_CHAT" = true ]] && PUPPETEER_ARGS+=(--new-chat)
[[ "$USE_DAEMON" = true ]] && PUPPETEER_ARGS+=(--daemon)
[[ "$VISIBLE" = true ]] && PUPPETEER_ARGS+=(--visible)
[[ "$WAIT_FOR_AUTH" = true ]] && PUPPETEER_ARGS+=(--wait)
[[ "$DRY_RUN" = true ]] && PUPPETEER_ARGS+=(--dry-run)
[[ "$CLOSE_BROWSER" = true ]] && PUPPETEER_ARGS+=(--close)
[[ "$DEBUG_MODE" = true ]] && PUPPETEER_ARGS+=(--debug)
[[ "$VERBOSE_MODE" = true ]] && PUPPETEER_ARGS+=(--verbose)

PROMPT_FILE="$(mktemp)"
cleanup_prompt_file() {
  rm -f "$PROMPT_FILE"
}
trap cleanup_prompt_file EXIT
printf '%s' "$FULL_PROMPT" > "$PROMPT_FILE"

echo "📅 $TODAY"
[[ -n "$SESSION_NAME" ]] && echo "🔄 Сессия: $SESSION_NAME"
[[ "$SEARCH_MODE" = true ]] && echo "🔍 Поиск"
[[ "$USE_DAEMON" = true ]] && echo "⚡ Режим демона"
echo ""

# Check daemon
if [[ "$USE_DAEMON" = true ]]; then
  if [[ ! -f "$SCRIPT_DIR/.daemon-ws-endpoint" ]]; then
    # Fallback from daemon.json
    if [[ -f "$SCRIPT_DIR/.sessions/daemon.json" ]]; then
      daemon_ws=$(node -e 'try{const fs=require("fs");const j=JSON.parse(fs.readFileSync(process.argv[1],"utf8"));if(j&&j.browserWSEndpoint)process.stdout.write(j.browserWSEndpoint)}catch(e){}' "$SCRIPT_DIR/.sessions/daemon.json")
      if [[ -n "$daemon_ws" ]]; then
        printf '%s' "$daemon_ws" > "$SCRIPT_DIR/.daemon-ws-endpoint"
      fi
    fi
  fi
  if [[ ! -f "$SCRIPT_DIR/.daemon-ws-endpoint" ]]; then
    echo "❌ Демон не запущен. Запусти: cd \"$SCRIPT_DIR\" && bash scripts/setup-daemon.sh"
    exit 1
  fi
fi

# Execute
if [[ "$USE_DAEMON" = true ]]; then
  node "$SCRIPT_DIR/ask-puppeteer.js" --file "$PROMPT_FILE" "${PUPPETEER_ARGS[@]}" 2>&1
else
  node "$SCRIPT_DIR/ask-puppeteer.js" --file "$PROMPT_FILE" "${PUPPETEER_ARGS[@]}" --close 2>&1
fi
exit $?
