#!/usr/bin/env bash
# knowledge-base-pro — автоустановщик
# Копирует коробку в ~/.openclaw/skills/ и создаёт дефолтные файлы.
#
# Usage:
# bash install.sh [--target ~/.openclaw/skills/knowledge-base-pro]
#
# Поддержка: Linux / macOS / WSL. Windows — см. README Quick Start вариант ручной установки. set -euo pipefail SKILL_NAME="knowledge-base-pro"
DEFAULT_TARGET="${HOME}/.openclaw/skills/${SKILL_NAME}"
TARGET="${1:-$DEFAULT_TARGET}"
SRC_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)" echo ""
echo "╔══════════════════════════════════════════════════╗"
echo "║ AI-База знаний PRO.0 — установка ║"
echo "╚══════════════════════════════════════════════════╝"
echo ""
echo "Источник: $SRC_DIR"
echo "Назначение: $TARGET"
echo "" # 1. Проверка OpenClaw или Claude Code
OPENCLAW_OK="no"
CLAUDE_OK="no"
if command -v openclaw >/dev/null 2>&1; then OPENCLAW_OK="yes" echo "[✓] openclaw найден: $(openclaw --version 2>/dev/null | head -1 || echo 'version unknown')"
fi
if command -v claude >/dev/null 2>&1; then CLAUDE_OK="yes" echo "[✓] claude найден: $(claude --version 2>/dev/null | head -1 || echo 'version unknown')"
fi if [[ "$OPENCLAW_OK" == "no" && "$CLAUDE_OK" == "no" ]]; then echo "[!] Не найден ни openclaw, ни claude. Коробку всё равно установим, но запустить вы сможете только когда поставите один из движков." echo " OpenClaw: https://openclaw.ai/install" echo " Claude Code: https://claude.ai/download" echo ""
fi # 2. Создать target и скопировать файлы
mkdir -p "$TARGET"
cp "$SRC_DIR/SKILL.md" "$SRC_DIR/config.yaml" "$SRC_DIR/README.md" "$SRC_DIR/install.sh" "$SRC_DIR/.env.example" "$TARGET/" for subdir in docs examples proof test; do if [[ -d "$SRC_DIR/$subdir" ]]; then cp -r "$SRC_DIR/$subdir" "$TARGET/" fi
done chmod +x "$TARGET/install.sh" 2>/dev/null || true
if [[ -f "$TARGET/test/smoke-test.sh" ]]; then chmod +x "$TARGET/test/smoke-test.sh" 2>/dev/null || true
fi
echo "[✓] Файлы скопированы в $TARGET" # 3. Создать .env из шаблона если нет
if [[ ! -f "$TARGET/.env" ]]; then cp "$SRC_DIR/.env.example" "$TARGET/.env" echo "[✓] Создан $TARGET/.env (заполнять только если нужны интеграции)"
else echo "[i] $TARGET/.env уже существует — не перезаписываю"
fi # 4. Напомнить про OBLIGATORY-поля
echo ""
echo "══════ СЛЕДУЮЩИЕ ШАГИ (5 минут) ══════"
echo ""
echo "1. Откройте config.yaml:"
echo " $TARGET/config.yaml"
echo ""
echo "2. Заполните [OBLIGATORY] поля:"
echo " • company.name — название вашей компании"
echo " • company.language — rus (русский по умолчанию)"
echo " • team.size — количество сотрудников"
echo " • kb.storage_type — notion / confluence / google_drive / local"
echo ""
echo "3. Smoke-тест:"
echo " bash $TARGET/test/smoke-test.sh"
echo ""
echo "4. Первый запуск: напишите боту/агенту любой триггер:"
echo " (база знаний / FAQ / онбординг / найди: [вопрос] / добавь в базу)"
echo ""
echo "Готово. Полная установка — см. README.md Quick Start."
echo ""
