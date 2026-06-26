#!/usr/bin/env bash
# AI-Прораб PRO — smoke-test
# Проверяет что коробка установлена корректно:
# структура + YAML-валидность + триггеры + ClawHub-совместимость.
# Версия коробки определяется ДИНАМИЧЕСКИ из SKILL.md YAML.
# Время выполнения: ~3-10 секунд. Без внешних вызовов API. set -uo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BOX_DIR="$(cd "$SCRIPT_DIR/.." && pwd)" PASS=0
FAIL=0
NOTES= check { local name="$1" local result="$2" local note="${3:-}" if [[ "$result" == "ok" ]]; then echo " [✓] $name" PASS=$((PASS + 1)) else echo " [✗] $name ${note:+— $note}" FAIL=$((FAIL + 1)) [[ -n "$note" ]] && NOTES+=("$name: $note") fi
} BOX_VERSION="$(grep '^version:' "$BOX_DIR/SKILL.md" 2>/dev/null | head -1 | sed -E 's/version: *//' | tr -d ' ')"
BOX_NAME="$(grep '^name:' "$BOX_DIR/SKILL.md" 2>/dev/null | head -1 | sed -E 's/name: *//' | tr -d ' ')" echo ""
echo "╔══════════════════════════════════════════════════╗"
echo "║ AI-Прораб PRO — smoke-test ║"
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
for n in 01 02 03 04 05; do case_file=$(find "$BOX_DIR/proof" -maxdepth 1 -name "case-${n}*.md" 2>/dev/null | head -1) if [[ -n "$case_file" ]]; then check "proof case-$n" "ok" else check "proof case-$n" "fail" "не найден" fi
done # ── 3. SKILL.md — ClawHub-совместимость ──
echo ""
echo "── 3. SKILL.md — ClawHub-совместимость ──" if [[ "$BOX_NAME" == "foreman-pro" ]]; then check "manifest name: $BOX_NAME" "ok"
else check "manifest name" "fail" "ожидается foreman-pro, получено: ${BOX_NAME:-пусто}"
fi if [[ -n "$BOX_VERSION" ]] && [[ "$BOX_VERSION" =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then check "version semver: $BOX_VERSION" "ok"
else check "version semver" "fail" "ожидается X.Y.Z"
fi if grep -q "^metadata:" "$BOX_DIR/SKILL.md" && grep -q "openclaw:" "$BOX_DIR/SKILL.md"; then check "metadata.openclaw блок" "ok"
else check "metadata.openclaw блок" "fail" "нужен для ClawHub"
fi if grep -q "emoji:" "$BOX_DIR/SKILL.md"; then check "metadata.openclaw.emoji" "ok"
else check "metadata.openclaw.emoji" "fail"
fi if grep -q "security_level:" "$BOX_DIR/SKILL.md"; then check "metadata.openclaw.security_level" "ok"
else check "metadata.openclaw.security_level" "fail"
fi if grep -q "^tags:" "$BOX_DIR/SKILL.md"; then check "tags: блок" "ok"
else check "tags: блок" "fail"
fi if grep -qE "^price: *[0-9]+" "$BOX_DIR/SKILL.md"; then check "price: явная цена" "ok"
else check "price:" "fail" "добавить поле price: в SKILL.md"
fi # ── 4. SKILL.md — ключевые RU и EN триггеры ──
echo ""
echo "── 4. SKILL.md — ключевые RU и EN триггеры (25+) ──" # RU: bash grep ненадёжен с кириллицей на Windows/Git Bash.
# Считаем строки в блоке triggers (- <слово>) как надёжный прокси.
TRIGGER_COUNT=$(grep -cE "^ - [a-zA-Z]" "$BOX_DIR/SKILL.md" 2>/dev/null || echo 0)
TRIGGER_TOTAL=$(grep -cE "^ - " "$BOX_DIR/SKILL.md" 2>/dev/null || echo 0)
if [[ "$TRIGGER_TOTAL" -ge 20 ]]; then check "RU+EN triggers блок (>=20 строк, найдено $TRIGGER_TOTAL)" "ok"
else check "RU+EN triggers блок" "fail" "найдено $TRIGGER_TOTAL строк, ожидается >=20"
fi # EN-триггеры — ASCII, надёжно через grep
EN_TRIGGERS=( "foreman" "work log" "construction schedule" "crew management" "site acceptance" "material write-off"
)
for trg in "${EN_TRIGGERS[@]}"; do if grep -Fq "$trg" "$BOX_DIR/SKILL.md" 2>/dev/null; then check "EN trigger: $trg" "ok" else check "EN trigger: $trg" "fail" fi
done # ── 5. config.yaml — базовая валидность ──
echo ""
echo "── 5. config.yaml — базовая валидность ──" if [[ -f "$BOX_DIR/config.yaml" ]]; then if grep -qE "^leader:" "$BOX_DIR/config.yaml"; then check "config: leader: блок" "ok" else check "config: leader: блок" "fail" fi if grep -qE "^company:" "$BOX_DIR/config.yaml"; then check "config: company: блок" "ok" else check "config: company: блок" "fail" fi if grep -qE "^object:" "$BOX_DIR/config.yaml"; then check "config: object: блок" "ok" else check "config: object: блок" "fail" fi if grep -qE "^team:" "$BOX_DIR/config.yaml"; then check "config: team: блок" "ok" else check "config: team: блок" "fail" fi
else check "config.yaml" "fail" "не найден"
fi # ── 6. README.md — Quick Start в первых 30 строках ──
echo ""
echo "── 6. README.md — Quick Start в первых 30 строках ──" HEAD_30=$(head -30 "$BOX_DIR/README.md" 2>/dev/null)
if echo "$HEAD_30" | grep -qi "quick start\|быстрый старт\|установка\|15 минут"; then check "Quick Start в начале README" "ok"
else check "Quick Start в начале README" "fail"
fi # ── 7. Дифференциаторы и маркетинг ──
echo ""
echo "── 7. Дифференциаторы и маркетинг ──" if grep -qi "40-50\|Replaces\|replaces" "$BOX_DIR/SKILL.md" 2>/dev/null; then check "SKILL.md: заявление о замене сотрудника (40-50%)" "ok"
else check "SKILL.md: заявление о замене сотрудника" "fail" "добавить 'заменяет X на Y%' или '40-50%'"
fi if grep -qE "[0-9]+(K|К|000)" "$BOX_DIR/SKILL.md" 2>/dev/null || grep -qi "RUB\|ruble\|70-120" "$BOX_DIR/SKILL.md" 2>/dev/null; then check "SKILL.md: ROI/экономия в рублях" "ok"
else check "SKILL.md: ROI/экономия в рублях" "fail"
fi if [[ -f "$BOX_DIR/marketing/onepager.md" ]]; then check "marketing/onepager.md" "ok"
else check "marketing/onepager.md" "fail"
fi if [[ -f "$BOX_DIR/marketing/comparison.md" ]]; then check "marketing/comparison.md" "ok"
else check "marketing/comparison.md" "fail"
fi if [[ -f "$BOX_DIR/marketing/testimonial-template.md" ]]; then check "marketing/testimonial-template.md" "ok"
else check "marketing/testimonial-template.md" "fail"
fi # ── 8. Конкуренты (блок B) ──
echo ""
echo "── 8. Блок B — анализ конкурентов ──" if [[ -f "$BOX_DIR/competitors/competitors-comparison.md" ]]; then check "competitors/competitors-comparison.md" "ok"
else check "competitors/competitors-comparison.md" "fail"
fi # ── 9. Dogfooding ──
echo ""
echo "── 9. Dogfooding (опционально) ──" if [[ -f "$BOX_DIR/proof/dogfooding-RAAI.md" ]]; then check "proof/dogfooding-RAAI.md" "ok"
else check "proof/dogfooding-RAAI.md" "fail" "(ещё не пройден — ожидается после 21-25.04)"
fi # ── ИТОГ ──
echo ""
echo "──────────────────────────────────────────"
TOTAL=$((PASS + FAIL))
echo " ИТОГО: [✓] $PASS / $TOTAL [✗] $FAIL"
echo "──────────────────────────────────────────"
echo "" if [[ $FAIL -eq 0 ]]; then echo "PASS — коробка $BOX_NAME v$BOX_VERSION установлена корректно." echo "" echo "Следующий шаг: заполните OBLIGATORY поля в config.yaml и напишите триггер 'план дня'." exit 0
else PCT=$((PASS * 100 / TOTAL)) echo "PARTIAL ($PCT%) — $FAIL проблем:" for note in "${NOTES[@]}"; do echo " * $note"; done echo "" echo "Решение: см. docs/anti-fail.md" if [[ $PCT -ge 90 ]]; then exit 0 else exit 1 fi
fi
