#!/usr/bin/env bash
# AI-офис PRO — smoke-test
# Проверяет что коробка установлена корректно (структура + YAML-валидность + триггеры + ClawHub-совместимость).
# Версия коробки определяется ДИНАМИЧЕСКИ из SKILL.md YAML (без хардкода).
# Время выполнения: ~3-10 секунд. Без внешних вызовов API. set -uo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BOX_DIR="$(cd "$SCRIPT_DIR/.." && pwd)" PASS=0
FAIL=0
NOTES= check { local name="$1" local result="$2" local note="${3:-}" if [[ "$result" == "ok" ]]; then echo " [✓] $name" PASS=$((PASS + 1)) else echo " [✗] $name ${note:+— $note}" FAIL=$((FAIL + 1)) [[ -n "$note" ]] && NOTES+=("$name: $note") fi
} BOX_VERSION="$(grep '^version:' "$BOX_DIR/SKILL.md" 2>/dev/null | head -1 | sed -E 's/version: *//' | tr -d ' ')"
BOX_NAME="$(grep '^name:' "$BOX_DIR/SKILL.md" 2>/dev/null | head -1 | sed -E 's/name: *//' | tr -d ' ')" echo ""
echo "╔══════════════════════════════════════════════════╗"
echo "║ AI-офис PRO — smoke-test ║"
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
echo "── 3. SKILL.md — ClawHub-совместимость ──" if [[ "$BOX_NAME" == "raai-ai-office" ]] || [[ "$BOX_NAME" == "ai-office-pro" ]]; then check "manifest name: $BOX_NAME" "ok"
else check "manifest name" "fail" "ожидается raai-ai-office или ai-office-pro"
fi if [[ -n "$BOX_VERSION" ]] && [[ "$BOX_VERSION" =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then check "version semver: $BOX_VERSION" "ok"
else check "version semver" "fail" "ожидается X.Y.Z"
fi if grep -q "^metadata:" "$BOX_DIR/SKILL.md" && grep -q "openclaw:" "$BOX_DIR/SKILL.md"; then check "metadata.openclaw блок" "ok"
else check "metadata.openclaw блок" "fail" "нужен для ClawHub"
fi if grep -q "^tags:" "$BOX_DIR/SKILL.md"; then check "tags: блок" "ok"
else check "tags: блок" "fail"
fi if grep -qE "^price: *[0-9]+" "$BOX_DIR/SKILL.md"; then check "price: явная цена" "ok"
else check "price:" "fail"
fi echo ""
echo "── 4. SKILL.md — ключевые RU и EN триггеры ──" RU_TRIGGERS=("брифинг CEO" "OKR" "weekly review" "decision log" "матрица эйзенхауэра" "делегирование" "отчёт для инвестора")
for trg in "${RU_TRIGGERS[@]}"; do if grep -Fq "$trg" "$BOX_DIR/SKILL.md" 2>/dev/null; then check "RU trigger: $trg" "ok" else check "RU trigger: $trg" "fail" fi
done EN_TRIGGERS=("CEO briefing" "OKR tracking" "investor update")
for trg in "${EN_TRIGGERS[@]}"; do if grep -Fq "$trg" "$BOX_DIR/SKILL.md" 2>/dev/null; then check "EN trigger: $trg" "ok" else check "EN trigger: $trg" "fail" fi
done echo ""
echo "── 5. config.yaml — базовая валидность ──" if [[ -f "$BOX_DIR/config.yaml" ]]; then if grep -qE "^leader:" "$BOX_DIR/config.yaml"; then check "config: leader: block" "ok" else check "config: leader: block" "fail" fi if grep -qE "^company:" "$BOX_DIR/config.yaml"; then check "config: company: block" "ok" else check "config: company: block" "fail" fi if grep -qi "OBLIGATORY\|обязат\|первом запуске\|5 полей" "$BOX_DIR/config.yaml"; then check "config: маркировка обязательных полей" "ok" else check "config: маркировка обязательных полей" "fail" fi
else check "config.yaml" "fail" "не найден"
fi echo ""
echo "── 6. README.md — Quick Start в первых 30 строках ──" HEAD_30=$(head -30 "$BOX_DIR/README.md" 2>/dev/null)
if echo "$HEAD_30" | grep -qi "quick start\|быстрый старт\|установка\|15 минут"; then check "Quick Start в начале README" "ok"
else check "Quick Start в начале README" "fail"
fi echo ""
echo "── 7. Dogfooding + конкуренты (премиум-бонус) ──" if [[ -f "$BOX_DIR/proof/dogfooding-RAAI.md" ]]; then check "proof/dogfooding-RAAI.md" "ok"
else check "proof/dogfooding-RAAI.md" "fail"
fi if [[ -f "$BOX_DIR/docs/competitors-comparison.md" ]]; then check "docs/competitors-comparison.md" "ok"
else check "docs/competitors-comparison.md" "fail"
fi if [[ -d "$BOX_DIR/competitors" ]] && [[ $(ls -A "$BOX_DIR/competitors" 2>/dev/null | wc -l) -ge 3 ]]; then check "competitors/ с архивом ≥3 SKILL.md" "ok"
else check "competitors/ архив" "fail" "ожидается ≥3 файла"
fi echo ""
echo "──────────────────────────────────────────"
TOTAL=$((PASS + FAIL))
echo " ИТОГО: [✓] $PASS / $TOTAL [✗] $FAIL"
echo "──────────────────────────────────────────"
echo "" if [[ $FAIL -eq 0 ]]; then echo "🟢 PASS — коробка $BOX_NAME v$BOX_VERSION установлена корректно." echo "" echo "Следующий шаг: заполните OBLIGATORY поля в config.yaml и напишите боту триггер 'брифинг'." exit 0
else echo "🔴 FAIL — есть $FAIL проблем:" for note in "${NOTES[@]}"; do echo " • $note"; done echo "" echo "Решение: см. docs/anti-fail.md." exit 1
fi
