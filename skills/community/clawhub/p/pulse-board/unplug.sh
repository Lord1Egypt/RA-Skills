#!/usr/bin/env bash
# Pulse Board — unplug.sh
# Remove a skill from Pulse Board and clean up its cron entry.
# No sudo. No root.

set -euo pipefail

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PULSE_HOME="${PULSE_HOME:-$HOME/.pulse-board}"

# ── UI helpers ────────────────────────────────────────────────────────────────
bold()   { printf "\033[1m%s\033[0m"      "$*"; }
green()  { printf "\033[0;32m%s\033[0m\n" "$*"; }
yellow() { printf "\033[0;33m%s\033[0m\n" "$*"; }
red()    { printf "\033[0;31m%s\033[0m\n" "$*"; }
dim()    { printf "\033[2m%s\033[0m\n"    "$*"; }

usage() {
  echo ""
  echo "  Usage: unplug.sh --skill <n>"
  echo ""
  exit 1
}

SKILL=""
while [[ $# -gt 0 ]]; do
  case "$1" in
    --skill) SKILL="$2"; shift 2 ;;
    --help|-h) usage ;;
    *) red "Unknown argument: $1"; usage ;;
  esac
done

[[ -z "$SKILL" ]] && { red "  Error: --skill is required."; usage; }

SKILL_SAFE="$(echo "$SKILL" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9-]/-/g')"
CONF_FILE="$PULSE_HOME/registry/${SKILL_SAFE}.conf"

echo ""

# ── Remove registry entry ─────────────────────────────────────────────────────
if [[ -f "$CONF_FILE" ]]; then
  rm "$CONF_FILE"
  green "  ✓ Registry entry removed"
else
  yellow "  · No registry entry found for: $SKILL_SAFE"
fi

# ── Remove cron entry ─────────────────────────────────────────────────────────
EXISTING_CRON="$(crontab -l 2>/dev/null || true)"

if echo "$EXISTING_CRON" | grep -q "pulse-board:$SKILL_SAFE"; then
  echo "$EXISTING_CRON" | grep -v "pulse-board:$SKILL_SAFE" | crontab -
  green "  ✓ Cron entry removed"
else
  yellow "  · No cron entry found for: $SKILL_SAFE"
fi

echo ""
green "  $(bold "$SKILL_SAFE") unplugged."
dim "  Detail logs preserved at: $PULSE_HOME/logs/detail/$SKILL_SAFE/"
echo ""
