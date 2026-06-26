#!/usr/bin/env bash
# AI-офис PRO v3.4 — автоустановщик
# Копирует коробку в ~/.openclaw/skills/ и создаёт дефолтные файлы.
#
# Usage:
# bash install.sh [--claude-home ~/.openclaw/skills/ai-office-pro]
#
# Поддержка: Linux / macOS / WSL. Windows — см. README Quick Start вариант ручной установки. set -euo pipefail SKILL_NAME="ai-office-pro"
DEFAULT_TARGET="${HOME}/.openclaw/skills/${SKILL_NAME}"
TARGET="${1:-$DEFAULT_TARGET}"
SRC_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)" echo ""
echo "╔══════════════════════════════════════════════════╗"
echo "║ AI-офис PRO v3.4 — установка ║"
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
cp "$SRC_DIR/SKILL.md" "$SRC_DIR/config.yaml" "$SRC_DIR/README.md" "$SRC_DIR/install.sh" "$SRC_DIR/.env.example" "$TARGET/"
cp -r "$SRC_DIR/docs" "$SRC_DIR/examples" "$SRC_DIR/proof" "$SRC_DIR/test" "$TARGET/"
chmod +x "$TARGET/install.sh" "$TARGET/test/smoke-test.sh" 2>/dev/null || true
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
echo "2. Заполните 5 [OBLIGATORY] полей:"
echo " • leader.name — Имя Отчество"
echo " • leader.role — CEO / Собственник / Управляющий"
echo " • company.name — название компании"
echo " • company.goal_monthly_revenue — цель выручки/мес"
echo " • team.size — размер команды"
echo " • channels.primary — главный канал"
echo ""
echo "3. Smoke-тест:"
echo " bash $TARGET/test/smoke-test.sh"
echo ""
echo "4. Первый запуск: напишите боту/агенту любой триггер"
echo " (брифинг / OKR / итоги недели / зафиксировать решение / приоритеты)"
echo ""
echo "Готово. Полная установка — см. README.md Quick Start."
echo ""
