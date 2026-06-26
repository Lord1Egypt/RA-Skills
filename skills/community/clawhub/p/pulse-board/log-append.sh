#!/usr/bin/env bash
# Pulse Board — log-append.sh
# Called by skill cron wrappers to record a one-line outcome.
# This is the only way skills should write to pending.log.
# No sudo. No root.

set -euo pipefail

PULSE_HOME="${PULSE_HOME:-$HOME/.pulse-board}"
PENDING_LOG="$PULSE_HOME/logs/pending.log"

usage() {
  echo "Usage: log-append.sh --skill <n> --status <OK|WARN|SKIP|ERROR> --message <msg>"
  exit 1
}

SKILL="" STATUS="" MESSAGE=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --skill)   SKILL="$2";   shift 2 ;;
    --status)  STATUS="$2";  shift 2 ;;
    --message) MESSAGE="$2"; shift 2 ;;
    --help|-h) usage ;;
    *) echo "Unknown argument: $1" >&2; usage ;;
  esac
done

[[ -z "$SKILL"   ]] && { echo "Error: --skill is required."   >&2; usage; }
[[ -z "$STATUS"  ]] && { echo "Error: --status is required."  >&2; usage; }
[[ -z "$MESSAGE" ]] && { echo "Error: --message is required." >&2; usage; }

STATUS="$(echo "$STATUS" | tr '[:lower:]' '[:upper:]')"
case "$STATUS" in
  OK|WARN|SKIP|ERROR) ;;
  *) echo "Error: --status must be OK, WARN, SKIP, or ERROR." >&2; exit 1 ;;
esac

mkdir -p "$(dirname "$PENDING_LOG")"

printf "[%s] [%-14s] [%-5s] %s\n" \
  "$(date +'%Y-%m-%d %H:%M %Z')" \
  "$SKILL" \
  "$STATUS" \
  "$MESSAGE" \
  >> "$PENDING_LOG"
