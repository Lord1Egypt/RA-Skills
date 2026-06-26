#!/usr/bin/env bash
# AI-Продажник PRO — smoke-test
# Проверяет структуру, YAML-совместимость, триггеры, ClawHub-совместимость.
# Версия коробки определяется динамически из SKILL.md.
# Время выполнения: ~3-10 сек. Без внешних API-вызовов. set -uo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BOX_DIR="$(cd "$SCRIPT_DIR/.." && pwd)" PASS=0
FAIL=0
NOTES= check { local name="$1" local result="$2" local note="${3:-}" if [[ "$result" == "ok" ]]; then echo " [✓] $name" PASS=$((PASS + 1)) else echo " [✗] $name ${note:+— $note}" FAIL=$((FAIL + 1)) [[ -n "$note" ]] && NOTES+=("$name: $note") fi
} BOX_VERSION="$(grep '^version:' "$BOX_DIR/SKILL.md" 2>/dev/null | head -1 | sed -E 's/version: *//' | tr -d ' ')"
BOX_NAME="$(grep '^name:' "$BOX_DIR/SKILL.md" 2>/dev/null | head -1 | sed -E 's/name: *//' | tr -d ' ')" echo ""
echo "╔══════════════════════════════════════════════════╗"
echo "║ AI-Продажник PRO — smoke-test ║"
echo "║ Имя: ${BOX_NAME:-?} Версия: ${BOX_VERSION:-?}"
echo "╚══════════════════════════════════════════════════╝"
echo ""
echo "Директория коробки: $BOX_DIR"
echo ""
echo "── 1. СТРУКТУРА (обязательные файлы) ──" REQUIRED_FILES=( SKILL.md README.md config.yaml .env.example install.sh test/smoke-test.sh examples/quick-start.md examples/full-library.md docs/onboarding.md docs/anti-fail.md docs/roi.md
)
for f in "${REQUIRED_FILES[@]}"; do if [[ -e "$BOX_DIR/$f" ]]; then check "exists: $f" "ok" else check "exists: $f" "fail" "не найден" fi
done echo ""
echo "── 2. Proof-кейсы (5 обязательных) ──"
for n in 01 02 03 04 05; do case_file=$(find "$BOX_DIR/proof" -maxdepth 1 -name "case-${n}*.md" 2>/dev/null | head -1) if [[ -n "$case_file" ]]; then check "proof case-$n" "ok" else check "proof case-$n" "fail" fi
done echo ""
echo "── 3. SKILL.md — YAML-заголовок и версия ──" if [[ "$BOX_NAME" == "sales-pro" ]]; then check "manifest name: $BOX_NAME" "ok"
else check "manifest name" "fail" "ожидается sales-pro, найдено: $BOX_NAME"
fi if [[ -n "$BOX_VERSION" ]] && [[ "$BOX_VERSION" =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then check "version semver: $BOX_VERSION" "ok"
else check "version semver" "fail" "ожидается X.Y.Z"
fi if grep -q "^metadata:" "$BOX_DIR/SKILL.md" && grep -q "openclaw:" "$BOX_DIR/SKILL.md"; then check "metadata.openclaw блок" "ok"
else check "metadata.openclaw блок" "fail" "нужен для ClawHub"
fi if grep -q "^tags:" "$BOX_DIR/SKILL.md"; then check "tags: блок" "ok"
else check "tags: блок" "fail"
fi if grep -qE "^price: *[0-9]+" "$BOX_DIR/SKILL.md"; then check "price: явная цена" "ok"
else check "price:" "fail"
fi if grep -q "triggers:" "$BOX_DIR/SKILL.md"; then check "triggers: блок" "ok"
else check "triggers: блок" "fail"
fi echo ""
echo "── 4. SKILL.md — ключевые RU триггеры ──" RU_TRIGGERS=("скрипт продаж" "квалификация лида" "работа с возражениями" "дожим" "follow up" "холодный звонок" "BANT" "pipeline" "win loss" "РОП отчёт")
for trg in "${RU_TRIGGERS[@]}"; do if grep -Fq "$trg" "$BOX_DIR/SKILL.md" 2>/dev/null; then check "RU trigger: $trg" "ok" else check "RU trigger: $trg" "fail" fi
done echo ""
echo "── 5. SKILL.md — ключевые EN триггеры ──" EN_TRIGGERS=("sales script" "lead qualification" "objection handling" "SPIN selling" "Challenger Sale" "pipeline report")
for trg in "${EN_TRIGGERS[@]}"; do if grep -Fq "$trg" "$BOX_DIR/SKILL.md" 2>/dev/null; then check "EN trigger: $trg" "ok" else check "EN trigger: $trg" "fail" fi
done echo ""
echo "── 6. config.yaml — базовая валидность ──" if [[ -f "$BOX_DIR/config.yaml" ]]; then if grep -qE "^leader:" "$BOX_DIR/config.yaml"; then check "config: leader: block" "ok" else check "config: leader: block" "fail" fi if grep -qE "^company:|^business:" "$BOX_DIR/config.yaml"; then check "config: company/business: block" "ok" else check "config: company/business: block" "fail" fi if grep -qi "OBLIGATORY\|обязат\|первом запуске" "$BOX_DIR/config.yaml"; then check "config: маркировка обязательных полей" "ok" else check "config: маркировка обязательных полей" "fail" fi if grep -qE "^funnel_stages:|^qualification:" "$BOX_DIR/config.yaml"; then check "config: воронка/квалификация" "ok" else check "config: воронка/квалификация" "fail" fi
else check "config.yaml" "fail" "не найден"
fi echo ""
echo "── 7. README.md — Quick Start в первых 30 строках ──" HEAD_30=$(head -30 "$BOX_DIR/README.md" 2>/dev/null)
if echo "$HEAD_30" | grep -qi "quick start\|быстрый старт\|установка\|15 минут"; then check "Quick Start в начале README" "ok"
else check "Quick Start в начале README" "fail"
fi echo ""
echo "── 8. .env.example — обязательные секции ──" if [[ -f "$BOX_DIR/.env.example" ]]; then if grep -q "LLM_API_KEY\|ANTHROPIC_API_KEY" "$BOX_DIR/.env.example"; then check ".env.example: LLM API" "ok" else check ".env.example: LLM API" "fail" fi if grep -q "TELEGRAM_BOT_TOKEN" "$BOX_DIR/.env.example"; then check ".env.example: Telegram" "ok" else check ".env.example: Telegram" "fail" fi if grep -q "GOOGLE_SHEETS\|AMOCRM\|BITRIX24" "$BOX_DIR/.env.example"; then check ".env.example: CRM-интеграции" "ok" else check ".env.example: CRM-интеграции" "fail" fi
else check ".env.example" "fail" "не найден"
fi echo ""
echo "── 9. Маркетинг-пакет ──" if [[ -f "$BOX_DIR/marketing/onepager.md" ]]; then check "marketing/onepager.md" "ok"
else check "marketing/onepager.md" "fail"
fi if [[ -f "$BOX_DIR/marketing/comparison.md" ]]; then check "marketing/comparison.md" "ok"
else check "marketing/comparison.md" "fail"
fi if [[ -f "$BOX_DIR/marketing/testimonial-template.md" ]]; then check "marketing/testimonial-template.md" "ok"
else check "marketing/testimonial-template.md" "fail"
fi echo ""
echo "── 10. Конкурентный анализ ──" if [[ -f "$BOX_DIR/competitors/competitors-comparison.md" ]]; then check "competitors/competitors-comparison.md" "ok"
else check "competitors/competitors-comparison.md" "fail"
fi echo ""
echo "── 11. SKILL.md — дифференциаторы и 3 уровня ──" if grep -q "дифференциатор\|Дифференциатор" "$BOX_DIR/SKILL.md" 2>/dev/null; then check "5 дифференциаторов в SKILL.md" "ok"
else check "5 дифференциаторов в SKILL.md" "fail"
fi if grep -q "3 уровня\|уровень 3\|Уровень" "$BOX_DIR/SKILL.md" 2>/dev/null; then check "3 уровня продукта в SKILL.md" "ok"
else check "3 уровня продукта в SKILL.md" "fail"
fi echo ""
echo "──────────────────────────────────────────"
TOTAL=$((PASS + FAIL))
PCTVAL=$(( PASS * 100 / TOTAL ))
echo " ИТОГО: [✓] $PASS / $TOTAL [✗] $FAIL ($PCTVAL%)"
echo "──────────────────────────────────────────"
echo "" if [[ $FAIL -eq 0 ]]; then echo "PASS — коробка $BOX_NAME v$BOX_VERSION установлена корректно." echo "" echo "Следующий шаг: заполните OBLIGATORY поля в config.yaml и напишите триггер 'скрипт звонка: [ваш продукт]'." exit 0
else echo "FAIL — есть $FAIL проблем:" for note in "${NOTES[@]}"; do echo " • $note"; done echo "" echo "Решение: см. docs/anti-fail.md." exit 1
fi
