#!/usr/bin/env bash
# AI-Аналитик бизнеса PRO — smoke-test
# Проверяет что коробка установлена корректно.
# Версия коробки определяется ДИНАМИЧЕСКИ из SKILL.md YAML (без хардкода).
# Время выполнения: ~3-10 секунд. Без внешних вызовов API. set -uo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BOX_DIR="$(cd "$SCRIPT_DIR/.." && pwd)" PASS=0
FAIL=0
NOTES= check { local name="$1" local result="$2" local note="${3:-}" if [[ "$result" == "ok" ]]; then echo " [✓] $name" PASS=$((PASS + 1)) else echo " [✗] $name ${note:+— $note}" FAIL=$((FAIL + 1)) [[ -n "$note" ]] && NOTES+=("$name: $note") fi
} BOX_VERSION="$(grep '^version:' "$BOX_DIR/SKILL.md" 2>/dev/null | head -1 | sed -E 's/version: *//' | tr -d ' ')"
BOX_NAME="$(grep '^name:' "$BOX_DIR/SKILL.md" 2>/dev/null | head -1 | sed -E 's/name: *//' | tr -d ' ')" echo ""
echo "╔══════════════════════════════════════════════════╗"
echo "║ AI-Аналитик бизнеса PRO — smoke-test ║"
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
echo "── 3. SKILL.md — ClawHub-совместимость ──" if [[ "$BOX_NAME" == "business-analyst-pro" ]] || [[ "$BOX_NAME" == "raai-business-analyst" ]]; then check "manifest name: $BOX_NAME" "ok"
else check "manifest name" "fail" "ожидается business-analyst-pro"
fi if [[ -n "$BOX_VERSION" ]] && [[ "$BOX_VERSION" =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then check "version semver: $BOX_VERSION" "ok"
else check "version semver" "fail" "ожидается X.Y.Z (например 3.5.0)"
fi if grep -q "^metadata:" "$BOX_DIR/SKILL.md" && grep -q "openclaw:" "$BOX_DIR/SKILL.md"; then check "metadata.openclaw блок" "ok"
else check "metadata.openclaw блок" "fail" "нужен для ClawHub"
fi if grep -q "^tags:" "$BOX_DIR/SKILL.md"; then check "tags: блок" "ok"
else check "tags: блок" "fail"
fi if grep -q "^price:" "$BOX_DIR/SKILL.md"; then check "price: поле" "ok"
else check "price: поле" "fail" "нужно для маркетплейса"
fi echo ""
echo "── 4. Проверка 12 режимов в SKILL.md ──" MODES=( "Дашборд" "KPI" "unit экономика" "воронка" "план факт" "прогноз" "финмодель" "точка безубыточности" "когорты" "сравни" "маржа продуктов" "investor report"
)
for mode in "${MODES[@]}"; do if grep -qi "$mode" "$BOX_DIR/SKILL.md" 2>/dev/null; then check "режим: $mode" "ok" else check "режим: $mode" "fail" "не найден в SKILL.md" fi
done echo ""
echo "── 5. SKILL.md — ключевые RU и EN триггеры ──" RU_TRIGGERS=("дашборд" "покажи KPI" "unit экономика" "LTV" "CAC" "когорты" "investor report" "финмодель" "план факт")
for trg in "${RU_TRIGGERS[@]}"; do if grep -Fq "$trg" "$BOX_DIR/SKILL.md" 2>/dev/null; then check "RU trigger: $trg" "ok" else check "RU trigger: $trg" "fail" fi
done EN_TRIGGERS=("financial dashboard" "unit economics" "cohort analysis" "P&L" "investor report")
for trg in "${EN_TRIGGERS[@]}"; do if grep -Fq "$trg" "$BOX_DIR/SKILL.md" 2>/dev/null; then check "EN trigger: $trg" "ok" else check "EN trigger: $trg" "fail" fi
done echo ""
echo "── 6. config.yaml — базовая валидность ──" if [[ -f "$BOX_DIR/config.yaml" ]]; then if grep -qE "^leader:" "$BOX_DIR/config.yaml"; then check "config: leader: блок" "ok" else check "config: leader: блок" "fail" fi if grep -qE "^company:" "$BOX_DIR/config.yaml"; then check "config: company: блок" "ok" else check "config: company: блок" "fail" fi if grep -qE "^finance:" "$BOX_DIR/config.yaml"; then check "config: finance: блок" "ok" else check "config: finance: блок" "fail" fi if grep -qE "^business_metrics:" "$BOX_DIR/config.yaml"; then check "config: business_metrics: блок (KPI-пороги)" "ok" else check "config: business_metrics: блок (KPI-пороги)" "fail" fi if grep -qi "OBLIGATORY\|обязат\|первом запуске\|5 полей" "$BOX_DIR/config.yaml"; then check "config: маркировка обязательных полей" "ok" else check "config: маркировка обязательных полей" "fail" fi if grep -q "kpi_thresholds:" "$BOX_DIR/config.yaml"; then check "config: kpi_thresholds (светофор)" "ok" else check "config: kpi_thresholds (светофор)" "fail" fi if grep -q "ltv_cac_ratio" "$BOX_DIR/config.yaml"; then check "config: LTV/CAC порог" "ok" else check "config: LTV/CAC порог" "fail" fi
else check "config.yaml" "fail" "не найден"
fi echo ""
echo "── 7. README.md — Quick Start ──" HEAD_30=$(head -30 "$BOX_DIR/README.md" 2>/dev/null)
if echo "$HEAD_30" | grep -qi "quick start\|быстрый старт\|установка\|15 минут"; then check "Quick Start в начале README" "ok"
else check "Quick Start в начале README" "fail"
fi echo ""
echo "── 8. Маркетинг и конкуренты (премиум-блоки) ──" if [[ -d "$BOX_DIR/marketing" ]]; then check "marketing/ директория" "ok"
else check "marketing/ директория" "fail"
fi if [[ -f "$BOX_DIR/marketing/onepager.md" ]]; then check "marketing/onepager.md" "ok"
else check "marketing/onepager.md" "fail"
fi if [[ -d "$BOX_DIR/competitors" ]]; then check "competitors/ директория" "ok"
else check "competitors/ директория" "fail"
fi if [[ -f "$BOX_DIR/competitors/competitors-comparison.md" ]]; then check "competitors/competitors-comparison.md" "ok"
else check "competitors/competitors-comparison.md" "fail"
fi echo ""
echo "──────────────────────────────────────────"
TOTAL=$((PASS + FAIL))
echo " ИТОГО: [✓] $PASS / $TOTAL [✗] $FAIL"
echo "──────────────────────────────────────────"
echo "" if [[ $FAIL -eq 0 ]]; then echo "PASS — коробка $BOX_NAME v$BOX_VERSION установлена корректно." echo "" echo "Следующий шаг: заполните OBLIGATORY поля в config.yaml и напишите боту триггер 'дашборд'." exit 0
else echo "FAIL — есть $FAIL проблем:" for note in "${NOTES[@]}"; do echo " • $note"; done echo "" echo "Решение: см. docs/anti-fail.md." exit 1
fi
