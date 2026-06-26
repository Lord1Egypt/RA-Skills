#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
DEFAULT_ENV_FILE="$HOME/.openclaw/workspace/.env/webtop-galim.env"
LEGACY_ENV_FILE="$HOME/.openclaw/workspace/.env/galim.env"
ENV_FILE="${WEBTOP_GALIM_ENV:-$DEFAULT_ENV_FILE}"

choose_env_file() {
  if [ -n "${WEBTOP_GALIM_ENV:-}" ]; then
    ENV_FILE="$WEBTOP_GALIM_ENV"
    return
  fi

  if [ -f "$DEFAULT_ENV_FILE" ] && grep -qE '^(GALIM_USERNAME_CHILD1|OFEK_USERNAME_CHILD1)=' "$DEFAULT_ENV_FILE"; then
    if grep -qE '^(GALIM_USERNAME_CHILD1|OFEK_USERNAME_CHILD1)=[^[:space:]]' "$DEFAULT_ENV_FILE"; then
      ENV_FILE="$DEFAULT_ENV_FILE"
      return
    fi
  fi

  if [ -f "$LEGACY_ENV_FILE" ]; then
    ENV_FILE="$LEGACY_ENV_FILE"
    return
  fi

  ENV_FILE="$DEFAULT_ENV_FILE"
}

load_env() {
  if [ -f "$ENV_FILE" ]; then
    set -a
    . "$ENV_FILE"
    set +a
  else
    echo "Missing env file: $ENV_FILE" >&2
    echo "Run: bash $ROOT_DIR/scripts/install.sh" >&2
    exit 1
  fi
}

map_legacy_env() {
  : "${GALIM_NAME_CHILD1:=${GALIM_NAME_YUVAL:-}}"
  : "${GALIM_USERNAME_CHILD1:=${GALIM_USERNAME_YUVAL:-}}"
  : "${GALIM_PASSWORD_CHILD1:=${GALIM_PASSWORD_YUVAL:-}}"
  : "${GALIM_NAME_CHILD2:=${GALIM_NAME_SHIRA:-}}"
  : "${GALIM_USERNAME_CHILD2:=${GALIM_USERNAME_SHIRA:-}}"
  : "${GALIM_PASSWORD_CHILD2:=${GALIM_PASSWORD_SHIRA:-}}"

  : "${OFEK_NAME_CHILD1:=${OFEK_NAME_YUVAL:-}}"
  : "${OFEK_USERNAME_CHILD1:=${OFEK_USERNAME_YUVAL:-}}"
  : "${OFEK_PASSWORD_CHILD1:=${OFEK_PASSWORD_YUVAL:-}}"
  : "${OFEK_NAME_CHILD2:=${OFEK_NAME_SHIRA:-}}"
  : "${OFEK_USERNAME_CHILD2:=${OFEK_USERNAME_SHIRA:-}}"
  : "${OFEK_PASSWORD_CHILD2:=${OFEK_PASSWORD_SHIRA:-}}"

  export GALIM_NAME_CHILD1 GALIM_USERNAME_CHILD1 GALIM_PASSWORD_CHILD1
  export GALIM_NAME_CHILD2 GALIM_USERNAME_CHILD2 GALIM_PASSWORD_CHILD2
  export OFEK_NAME_CHILD1 OFEK_USERNAME_CHILD1 OFEK_PASSWORD_CHILD1
  export OFEK_NAME_CHILD2 OFEK_USERNAME_CHILD2 OFEK_PASSWORD_CHILD2
}

build_ofek_kids_json() {
  if [ -n "${OFEK_KIDS_JSON:-}" ]; then
    export OFEK_KIDS_JSON
    return
  fi

  if [ -n "${OFEK_USERNAME_CHILD1:-}" ] && [ -n "${OFEK_PASSWORD_CHILD1:-}" ] && \
     [ -n "${OFEK_USERNAME_CHILD2:-}" ] && [ -n "${OFEK_PASSWORD_CHILD2:-}" ]; then
    export OFEK_KIDS_JSON="[$(
      python3 - <<'PY'
import json, os
kids = [
    {
        "name": os.getenv("OFEK_NAME_CHILD1", "Child 1"),
        "username": os.getenv("OFEK_USERNAME_CHILD1", ""),
        "password": os.getenv("OFEK_PASSWORD_CHILD1", ""),
    },
    {
        "name": os.getenv("OFEK_NAME_CHILD2", "Child 2"),
        "username": os.getenv("OFEK_USERNAME_CHILD2", ""),
        "password": os.getenv("OFEK_PASSWORD_CHILD2", ""),
    },
]
print(",".join(json.dumps(k, ensure_ascii=False) for k in kids), end="")
PY
    )]"
  fi
}

usage() {
  cat <<EOF
Usage:
  bash scripts/claude-code-wrapper.sh <command> [args...]

Commands:
  webtop      Run Webtop summary
  galim       Run Galim task fetcher
  ofek        Run Ofek task fetcher
  report      Run unified report
  expanded    Run expanded report
  sync        Sync Galim tasks to calendar
  env-check   Validate that env file exists and key vars are loaded
EOF
}

main() {
  local cmd="${1:-}"
  shift || true

  if [ -z "$cmd" ]; then
    usage
    exit 1
  fi

  choose_env_file
  load_env
  map_legacy_env
  build_ofek_kids_json

  case "$cmd" in
    webtop)
      exec python3 "$ROOT_DIR/scripts/webtop_fetch_summary.py" "$@"
      ;;
    galim)
      exec python3 "$ROOT_DIR/scripts/galim_fetch_tasks.py" "$@"
      ;;
    ofek)
      exec python3 "$ROOT_DIR/scripts/fetch_tasks.py" "$@"
      ;;
    report)
      exec python3 "$ROOT_DIR/scripts/unified_report.py" "$@"
      ;;
    expanded)
      exec python3 "$ROOT_DIR/scripts/expanded_report.py" "$@"
      ;;
    sync)
      exec python3 "$ROOT_DIR/scripts/sync_galim_calendar.py" "$@"
      ;;
    env-check)
      echo "Env file: $ENV_FILE"
      echo "GALIM child1 user: ${GALIM_USERNAME_CHILD1:+set}"
      echo "GALIM child2 user: ${GALIM_USERNAME_CHILD2:+set}"
      echo "OFEK child1 user: ${OFEK_USERNAME_CHILD1:+set}"
      echo "OFEK child2 user: ${OFEK_USERNAME_CHILD2:+set}"
      echo "OFEK_KIDS_JSON: ${OFEK_KIDS_JSON:+set}"
      echo "Calendar ID: ${OFEK_GALIM_CALENDAR_ID:-unset}"
      ;;
    -h|--help|help)
      usage
      ;;
    *)
      echo "Unknown command: $cmd" >&2
      usage >&2
      exit 1
      ;;
  esac
}

main "$@"
