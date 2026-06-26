#!/usr/bin/env bash
# AI-Продажник PRO — автоустановщик
# Копирует коробку в ~/.openclaw/skills/ и создаёт дефолтные файлы.
#
# Usage:
# bash install.sh [--target ~/.openclaw/skills/sales-pro]
#
# Поддержка: Linux / macOS / WSL. Windows — см. README Quick Start вариант ручной установки. set -euo pipefail SKILL_NAME="sales-pro"
DEFAULT_TARGET="${HOME}/.openclaw/skills/${SKILL_NAME}"
TARGET="${1:-$DEFAULT_TARGET}"
SRC_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)" echo ""
echo "╔══════════════════════════════════════════════════╗"
echo "║ AI-Продажник PRO — установка ║"
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
fi if [[ "$OPENCLAW_OK" == "no" && "$CLAUDE_OK" == "no" ]]; then echo "[!] Не найден ни openclaw, ни claude. Коробку всё равно установим." echo " OpenClaw: https://openclaw.ai/install" echo " Claude Code: https://claude.ai/download" echo ""
fi # 2. Создать target и скопировать файлы
mkdir -p "$TARGET"
cp "$SRC_DIR/SKILL.md" "$SRC_DIR/config.yaml" "$SRC_DIR/README.md" "$SRC_DIR/install.sh" "$SRC_DIR/.env.example" "$TARGET/"
cp -r "$SRC_DIR/docs" "$SRC_DIR/examples" "$SRC_DIR/proof" "$SRC_DIR/test" "$TARGET/"
chmod +x "$TARGET/install.sh" "$TARGET/test/smoke-test.sh" 2>/dev/null || true # Опциональные папки (marketing, competitors)
for sub in marketing competitors; do if [[ -d "$SRC_DIR/$sub" ]]; then cp -r "$SRC_DIR/$sub" "$TARGET/$sub" fi
done echo "[✓] Файлы скопированы в $TARGET" # 3. Создать .env из шаблона если нет
if [[ ! -f "$TARGET/.env" ]]; then cp "$SRC_DIR/.env.example" "$TARGET/.env" echo "[✓] Создан $TARGET/.env (заполнять только если нужны интеграции)"
else echo "[i] $TARGET/.env уже существует — не перезаписываю"
fi # 4. Напомнить про OBLIGATORY-поля
echo ""
echo "══════ СЛЕДУЮЩИЕ ШАГИ (15 минут) ══════"
echo ""
echo "1. Откройте config.yaml:"
echo " $TARGET/config.yaml"
echo ""
echo "2. Заполните [OBLIGATORY] поля:"
echo " • leader.role — РОП / Собственник / CEO"
echo " • company.industry — ваша ниша"
echo " • business.product — ваш продукт/услуга"
echo " • business.niche — B2B / B2C"
echo " • sales_metrics.monthly_leads — лидов в месяц"
echo ""
echo "3. Smoke-тест:"
echo " bash $TARGET/test/smoke-test.sh"
echo ""
echo "4. Первый запуск: напишите боту/агенту любой триггер"
echo " Например: скрипт звонка: [ваш продукт]"
echo " Или: квалифицируй: [описание лида]"
echo ""
echo "Готово. Полная документация — см. README.md Quick Start."
echo ""
