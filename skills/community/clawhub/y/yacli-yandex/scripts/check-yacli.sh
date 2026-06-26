#!/usr/bin/env bash
set -euo pipefail

CONFIG_PATH="${1:-${MCPORTER_CONFIG:-./config/mcporter.json}}"

echo "== English =="
echo "Checking yacli skill prerequisites"
echo "mcporter config: $CONFIG_PATH"
echo
echo "== Русский =="
echo "Проверка предпосылок для skill yacli-yandex"
echo "Конфиг mcporter: $CONFIG_PATH"
echo

if ! command -v mcporter >/dev/null 2>&1; then
  echo "mcporter not found in PATH" >&2
  exit 1
fi

mcporter list yacli --schema --config "$CONFIG_PATH"
mcporter call --server yacli --tool yacli.account.list --args '{}' --config "$CONFIG_PATH"
mcporter call --server yacli --tool yacli.auth.status --args '{}' --config "$CONFIG_PATH"
