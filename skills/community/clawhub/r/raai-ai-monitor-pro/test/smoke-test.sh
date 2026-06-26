#!/usr/bin/env bash
# AI-Монитор PRO — smoke-test
# Проверяет что коробка установлена корректно:
# структура + YAML-валидность + триггеры + ClawHub-совместимость + маркетинг
# Версия коробки определяется ДИНАМИЧЕСКИ из SKILL.md YAML.
# Время выполнения: ~3-10 секунд. Без внешних вызовов API. set -uo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BOX_DIR="$(cd "$SCRIPT_DIR/.." && pwd)" PASS=0
FAIL=0
NOTES= check { local name="$1" local result="$2" local note="${3:-}" if [[ "$result" == "ok" ]]; then echo " [✓] $name" PASS=$((PASS + 1)) else echo " [✗] $name ${note:+— $note}" FAIL=$((FAIL + 1)) [[ -n "$note" ]] && NOTES+=("$name: $note") fi
} BOX_VERSION="$(grep '^version:' "$BOX_DIR/SKILL.md" 2>/dev/null | head -1 | sed -E 's/version: *//' | tr -d ' \"')"
BOX_NAME="$(grep '^name:' "$BOX_DIR/SKILL.md" 2>/dev/null | head -1 | sed -E 's/name: *//' | tr -d ' ')" echo ""
echo "╔══════════════════════════════════════════════════╗"
echo "║ AI-Монитор PRO — smoke-test ║"
echo "║ Имя: ${BOX_NAME:-?} Версия: ${BOX_VERSION:-?}"
echo "╚══════════════════════════════════════════════════╝"
echo ""
echo "Директория коробки: $BOX_DIR"
echo "" # ── 1. СТРУКТУРА (обязательные файлы) ──
echo "── 1. СТРУКТУРА (обязательные файлы) ──" REQUIRED_FILES=( SKILL.md README.md config.yaml .env.example install.sh test/smoke-test.sh examples/quick-start.md examples/full-library.md docs/onboarding.md docs/anti-fail.md docs/roi.md
)
for f in "${REQUIRED_FILES[@]}"; do if [[ -e "$BOX_DIR/$f" ]]; then check "exists: $f" "ok" else check "exists: $f" "fail" "не найден" fi
done # ── 2. Proof-кейсы (5 обязательных) ──
echo ""
echo "── 2. Proof-кейсы (5 обязательных) ──"
for n in 01 02 03 04 05; do case_file=$(find "$BOX_DIR/proof" -maxdepth 1 -name "case-${n}*.md" 2>/dev/null | head -1) if [[ -n "$case_file" ]]; then check "proof case-$n" "ok" else check "proof case-$n" "fail" fi
done # ── 3. SKILL.md — ClawHub-совместимость ──
echo ""
echo "── 3. SKILL.md — ClawHub-совместимость ──" if [[ "$BOX_NAME" == "ai-monitor-pro" ]]; then check "manifest name: $BOX_NAME" "ok"
else check "manifest name" "fail" "ожидается ai-monitor-pro, получено: $BOX_NAME"
fi if [[ -n "$BOX_VERSION" ]] && [[ "$BOX_VERSION" =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then check "version semver: $BOX_VERSION" "ok"
else check "version semver" "fail" "ожидается X.Y.Z, получено: ${BOX_VERSION:-пусто}"
fi if grep -q "^metadata:" "$BOX_DIR/SKILL.md" && grep -q "openclaw:" "$BOX_DIR/SKILL.md"; then check "metadata.openclaw блок" "ok"
else check "metadata.openclaw блок" "fail" "нужен для ClawHub"
fi if grep -q "^tags:" "$BOX_DIR/SKILL.md"; then check "tags: блок" "ok"
else check "tags: блок" "fail"
fi if grep -qE "^price: *[0-9]+" "$BOX_DIR/SKILL.md"; then check "price: явная цена" "ok"
else check "price:" "fail"
fi # Проверка что always: false в metadata.openclaw
if grep -q "always:" "$BOX_DIR/SKILL.md"; then check "metadata.openclaw always: false" "ok"
else check "metadata.openclaw always:" "fail" "нужен always: false"
fi # ── 4. SKILL.md — ключевые RU триггеры (строй-ниша) ──
echo ""
echo "── 4. SKILL.md — ключевые RU триггеры (строй-ниша) ──" check_trigger { local label="$1" local pattern="$2" # LC_ALL=C для стабильного grep на Windows с кириллицей if LC_ALL=C grep -qi "$pattern" "$BOX_DIR/SKILL.md" 2>/dev/null; then check "trigger: $label" "ok" else check "trigger: $label" "fail" fi
} check_trigger "мониторинг стройки" "мониторинг стройки"
check_trigger "фото-отчёт" "фото-отчёт"
check_trigger "контроль качества" "контроль качества"
check_trigger "нарушение сроков" "нарушение сроков"
check_trigger "дашборд" "дашборд"
check_trigger "алерт" "алерт"
check_trigger "инцидент" "инцидент"
check_trigger "post-mortem" "post-mortem"
check_trigger "SLA" "SLA" # ── 5. SKILL.md — EN триггеры ──
echo ""
echo "── 5. SKILL.md — EN триггеры ──" check_trigger "construction monitoring" "construction monitoring"
check_trigger "site inspection" "site inspection"
check_trigger "quality control" "quality control"
check_trigger "incident (EN)" "incident" # ── 6. config.yaml — базовая валидность ──
echo ""
echo "── 6. config.yaml — базовая валидность ──" if [[ -f "$BOX_DIR/config.yaml" ]]; then if grep -qE "^leader:" "$BOX_DIR/config.yaml"; then check "config: leader: block" "ok" else check "config: leader: block" "fail" fi if grep -qE "^company:" "$BOX_DIR/config.yaml"; then check "config: company: block" "ok" else check "config: company: block" "fail" fi if grep -qi "OBLIGATORY\|обязат\|обязательн" "$BOX_DIR/config.yaml"; then check "config: маркировка обязательных полей" "ok" else check "config: маркировка обязательных полей" "fail" fi
else check "config.yaml" "fail" "не найден"
fi # ── 7. README.md — Quick Start в первых 30 строках ──
echo ""
echo "── 7. README.md — Quick Start в первых 30 строках ──" HEAD_30=$(head -30 "$BOX_DIR/README.md" 2>/dev/null)
if echo "$HEAD_30" | grep -qi "quick start\|быстрый старт\|установка\|15 минут"; then check "Quick Start в начале README" "ok"
else check "Quick Start в начале README" "fail"
fi # ── 8. Маркетинг-упаковка ──
echo ""
echo "── 8. Маркетинг-упаковка ──" if [[ -f "$BOX_DIR/marketing/onepager.md" ]]; then check "marketing/onepager.md" "ok"
else check "marketing/onepager.md" "fail"
fi if [[ -f "$BOX_DIR/marketing/comparison.md" ]]; then check "marketing/comparison.md" "ok"
else check "marketing/comparison.md" "fail"
fi if [[ -f "$BOX_DIR/marketing/testimonial-template.md" ]]; then check "marketing/testimonial-template.md" "ok"
else check "marketing/testimonial-template.md" "fail"
fi # ── 9. Конкуренты ──
echo ""
echo "── 9. Конкуренты (исследование) ──" if [[ -f "$BOX_DIR/competitors/competitors-comparison.md" ]]; then check "competitors/competitors-comparison.md" "ok"
else check "competitors/competitors-comparison.md" "fail"
fi # ── 10. SKILL.md — дифференциаторы в теле ──
echo ""
echo "── 10. SKILL.md — дифференциаторы ──" if grep -qi "надзор-инженер\|40-60%\|надзора" "$BOX_DIR/SKILL.md" 2>/dev/null; then check "SKILL.md: заменяет надзор-инженера" "ok"
else check "SKILL.md: заменяет надзор-инженера" "fail"
fi if grep -qi "строй\|стройк\|прораб\|объект" "$BOX_DIR/SKILL.md" 2>/dev/null; then check "SKILL.md: строй-ниша упомянута" "ok"
else check "SKILL.md: строй-ниша упомянута" "fail"
fi # ── Итог ──
echo ""
echo "──────────────────────────────────────────"
TOTAL=$((PASS + FAIL))
echo " ИТОГО: [✓] $PASS / $TOTAL [✗] $FAIL"
echo "──────────────────────────────────────────"
echo "" if [[ $FAIL -eq 0 ]]; then echo "PASS — коробка $BOX_NAME v$BOX_VERSION установлена корректно." echo "" echo "Следующий шаг: заполните OBLIGATORY поля в config.yaml и напишите боту триггер 'мониторинг стройки'." exit 0
else echo "FAIL — есть $FAIL проблем:" for note in "${NOTES[@]}"; do echo " • $note"; done echo "" echo "Решение: см. docs/anti-fail.md." exit 1
fi
