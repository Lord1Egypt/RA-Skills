#!/usr/bin/env bash
# AI-Поддержка PRO — smoke-test
# Проверяет что коробка установлена корректно:
# структура + YAML-валидность + триггеры + режимы поддержки + proof-кейсы + ClawHub-совместимость.
# Версия коробки определяется ДИНАМИЧЕСКИ из SKILL.md YAML (без хардкода).
# Время выполнения: ~3-10 секунд. Без внешних вызовов API. set -uo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BOX_DIR="$(cd "$SCRIPT_DIR/.." && pwd)" PASS=0
FAIL=0
NOTES= check { local name="$1" local result="$2" local note="${3:-}" if [[ "$result" == "ok" ]]; then echo " [OK] $name" PASS=$((PASS + 1)) else echo " [FAIL] $name ${note:+— $note}" FAIL=$((FAIL + 1)) [[ -n "$note" ]] && NOTES+=("$name: $note") fi
} BOX_VERSION="$(grep '^version:' "$BOX_DIR/SKILL.md" 2>/dev/null | head -1 | sed -E 's/version: *//' | tr -d ' ')"
BOX_NAME="$(grep '^name:' "$BOX_DIR/SKILL.md" 2>/dev/null | head -1 | sed -E 's/name: *//' | tr -d ' ')" echo ""
echo "========================================================"
echo " AI-Поддержка PRO — smoke-test"
echo " Имя: ${BOX_NAME:-?} Версия: ${BOX_VERSION:-?}"
echo "========================================================"
echo ""
echo "Директория коробки: $BOX_DIR"
echo ""
echo "── 1. СТРУКТУРА (обязательные файлы) ──" REQUIRED_FILES=( SKILL.md README.md config.yaml .env.example install.sh test/smoke-test.sh examples/quick-start.md examples/full-library.md docs/onboarding.md docs/anti-fail.md docs/roi.md
)
for f in "${REQUIRED_FILES[@]}"; do if [[ -e "$BOX_DIR/$f" ]]; then check "exists: $f" "ok" else check "exists: $f" "fail" "не найден" fi
done echo ""
echo "── 2. Proof-кейсы (5 обязательных) ──"
for n in 01 02 03 04 05; do case_file=$(find "$BOX_DIR/proof" -maxdepth 1 -name "case-${n}*.md" 2>/dev/null | head -1) if [[ -n "$case_file" ]]; then check "proof case-$n" "ok" else check "proof case-$n" "fail" "не найден" fi
done echo ""
echo "── 3. SKILL.md — ClawHub-совместимость ──" if [[ "$BOX_NAME" == "ai-support-pro" ]]; then check "manifest name: $BOX_NAME" "ok"
else check "manifest name" "fail" "ожидается ai-support-pro, получено: $BOX_NAME"
fi if [[ -n "$BOX_VERSION" ]] && [[ "$BOX_VERSION" =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then check "version semver: $BOX_VERSION" "ok"
else check "version semver" "fail" "ожидается X.Y.Z"
fi if grep -q "^metadata:" "$BOX_DIR/SKILL.md" && grep -q "openclaw:" "$BOX_DIR/SKILL.md"; then check "metadata.openclaw блок" "ok"
else check "metadata.openclaw блок" "fail" "нужен для ClawHub"
fi if grep -q "^tags:" "$BOX_DIR/SKILL.md"; then check "tags: блок" "ok"
else check "tags: блок" "fail"
fi if grep -qE "^price: *[0-9]+" "$BOX_DIR/SKILL.md"; then check "price: явная цена" "ok"
else check "price:" "fail" "не найдено числовое значение"
fi # Версия должна быть 3.5.x
if [[ "$BOX_VERSION" =~ ^3\.5\. ]]; then check "version is 3.5.x" "ok"
else check "version is 3.5.x" "fail" "текущая: $BOX_VERSION"
fi echo ""
echo "── 4. SKILL.md — RU триггеры поддержки ──" RU_TRIGGERS=( "настрой поддержку" "обработай обращение" "SLA отчёт" "эскалация клиента" "карточка клиента" "клиент злится" "возврат денег" "NPS отчёт" "онбординг оператора" "автоответ" "FAQ бот" "тикет" "поддержка клиентов"
)
for trg in "${RU_TRIGGERS[@]}"; do if grep -Fq "$trg" "$BOX_DIR/SKILL.md" 2>/dev/null; then check "RU trigger: $trg" "ok" else check "RU trigger: $trg" "fail" fi
done echo ""
echo "── 5. SKILL.md — EN триггеры (ClawHub search) ──" EN_TRIGGERS=( "customer support" "helpdesk" "ticket routing" "24/7 bot"
)
for trg in "${EN_TRIGGERS[@]}"; do if grep -Fq "$trg" "$BOX_DIR/SKILL.md" 2>/dev/null; then check "EN trigger: $trg" "ok" else check "EN trigger: $trg" "fail" fi
done echo ""
echo "── 6. SKILL.md — режимы поддержки ──" MODES=( "категоризация|Категоризация" "SLA" "скалац" "Sentiment|sentiment" "автоответ|Автоответ" "CRM|crm" "NPS" "нбординг"
)
for mode in "${MODES[@]}"; do if grep -qiE "$mode" "$BOX_DIR/SKILL.md" 2>/dev/null; then check "режим: $mode" "ok" else check "режим: $mode" "fail" fi
done echo ""
echo "── 7. config.yaml — базовая валидность ──" if [[ -f "$BOX_DIR/config.yaml" ]]; then if grep -qE "^leader:" "$BOX_DIR/config.yaml"; then check "config: leader: блок" "ok" else check "config: leader: блок" "fail" fi if grep -qE "^company:" "$BOX_DIR/config.yaml"; then check "config: company: блок" "ok" else check "config: company: блок" "fail" fi if grep -qE "^sla:" "$BOX_DIR/config.yaml"; then check "config: sla: блок" "ok" else check "config: sla: блок" "fail" fi if grep -qE "^escalation:" "$BOX_DIR/config.yaml"; then check "config: escalation: блок" "ok" else check "config: escalation: блок" "fail" fi if grep -qE "^crm:|^integrations:" "$BOX_DIR/config.yaml"; then check "config: crm/integrations блок" "ok" else check "config: crm/integrations блок" "fail" fi
else check "config.yaml" "fail" "не найден"
fi echo ""
echo "── 8. .env.example — обязательные ключи ──" if [[ -f "$BOX_DIR/.env.example" ]]; then if grep -q "ANTHROPIC_API_KEY" "$BOX_DIR/.env.example"; then check ".env: ANTHROPIC_API_KEY" "ok" else check ".env: ANTHROPIC_API_KEY" "fail" fi if grep -q "OPENAI_API_KEY" "$BOX_DIR/.env.example"; then check ".env: OPENAI_API_KEY" "ok" else check ".env: OPENAI_API_KEY" "fail" fi if grep -q "TELEGRAM_BOT_TOKEN" "$BOX_DIR/.env.example"; then check ".env: TELEGRAM_BOT_TOKEN" "ok" else check ".env: TELEGRAM_BOT_TOKEN" "fail" fi if grep -qiE "BITRIX24|AMOCRM" "$BOX_DIR/.env.example"; then check ".env: CRM интеграция (Bitrix24/amoCRM)" "ok" else check ".env: CRM интеграция (Bitrix24/amoCRM)" "fail" fi
else check ".env.example" "fail" "не найден"
fi echo ""
echo "── 9. README.md — Quick Start в первых 30 строках ──" HEAD_30=$(head -30 "$BOX_DIR/README.md" 2>/dev/null)
if echo "$HEAD_30" | grep -qiE "quick start|быстрый старт|установка|15 минут|минут"; then check "Quick Start в начале README" "ok"
else check "Quick Start в начале README" "fail"
fi echo ""
echo "── 10. Маркетинг и конкуренты ──" if [[ -d "$BOX_DIR/marketing" ]] && [[ $(ls -A "$BOX_DIR/marketing" 2>/dev/null | wc -l) -ge 1 ]]; then check "marketing/ директория" "ok"
else check "marketing/ директория" "fail" "пустая или отсутствует"
fi if [[ -f "$BOX_DIR/marketing/onepager.md" ]]; then check "marketing/onepager.md" "ok"
else check "marketing/onepager.md" "fail"
fi if [[ -f "$BOX_DIR/competitors/competitors-comparison.md" ]]; then check "competitors/competitors-comparison.md" "ok"
else check "competitors/competitors-comparison.md" "fail"
fi echo ""
echo "──────────────────────────────────────────"
TOTAL=$((PASS + FAIL))
echo " ИТОГО: [OK] $PASS / $TOTAL [FAIL] $FAIL"
echo "──────────────────────────────────────────"
echo "" if [[ $FAIL -eq 0 ]]; then echo "PASS — коробка $BOX_NAME v$BOX_VERSION установлена корректно." echo "" echo "Следующий шаг: заполните OBLIGATORY поля в config.yaml и напишите боту триггер:" echo " 'настрой поддержку для [название компании]'" exit 0
else echo "FAIL — есть $FAIL проблем:" for note in "${NOTES[@]}"; do echo " * $note"; done echo "" echo "Решение: см. docs/anti-fail.md." exit 1
fi
