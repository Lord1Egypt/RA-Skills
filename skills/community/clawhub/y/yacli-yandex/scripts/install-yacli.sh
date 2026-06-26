#!/usr/bin/env bash
set -euo pipefail

echo "== English =="
echo "yacli-yandex public installer"
echo
echo "This script does not install yacli automatically because host packaging varies."
echo "It validates the expected host-side pieces and prints the next steps."
echo

need_bin() {
  local name="$1"
  if ! command -v "$name" >/dev/null 2>&1; then
    echo "Missing required binary: $name" >&2
    return 1
  fi
}

need_bin mcporter

if command -v yacli >/dev/null 2>&1; then
  echo "Found yacli: $(command -v yacli)"
else
  echo "yacli not found in PATH"
fi

if command -v yacli-mcp-server >/dev/null 2>&1; then
  echo "Found yacli-mcp-server: $(command -v yacli-mcp-server)"
else
  echo "yacli-mcp-server not found in PATH"
fi

echo
echo "Next steps:"
echo "1. Install yacli from the upstream project: https://github.com/NextStat/yacli"
echo "2. Make sure yacli-mcp-server is callable on this host"
echo "3. Add the example MCP entry from assets/mcporter.yacli.example.json to your mcporter.json"
echo "4. Authenticate at least one Yandex account"
echo "5. Run scripts/check-yacli.sh"
echo
echo "== Русский =="
echo "Публичный installer для skill yacli-yandex"
echo
echo "Скрипт не ставит yacli автоматически, потому что упаковка на разных хостах различается."
echo "Он только проверяет базовые предпосылки и подсказывает следующие шаги."
echo
if ! command -v yacli >/dev/null 2>&1; then
  echo "yacli не найден в PATH"
fi
if ! command -v yacli-mcp-server >/dev/null 2>&1; then
  echo "yacli-mcp-server не найден в PATH"
fi
echo
echo "Следующие шаги:"
echo "1. Установить yacli из upstream-проекта: https://github.com/NextStat/yacli"
echo "2. Убедиться, что yacli-mcp-server запускается на этом хосте"
echo "3. Добавить пример MCP entry из assets/mcporter.yacli.example.json в mcporter.json"
echo "4. Авторизовать хотя бы один Яндекс-аккаунт"
echo "5. Запустить scripts/check-yacli.sh"
