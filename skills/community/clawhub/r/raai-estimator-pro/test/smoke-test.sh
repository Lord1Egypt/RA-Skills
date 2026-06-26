#!/usr/bin/env bash
# AI-Сметчик PRO — smoke-test
# Проверяет что коробка установлена корректно:
# структура + YAML-валидность + триггеры + ClawHub-совместимость + маркетинг.
# Версия определяется ДИНАМИЧЕСКИ из SKILL.md YAML.
# Время выполнения: ~5-15 секунд. Без внешних вызовов API. set -uo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BOX_DIR="$(cd "$SCRIPT_DIR/.." && pwd)" PASS=0
FAIL=0
NOTES= check { local name="$1" local result="$2" local note="${3:-}" if [[ "$result" == "ok" ]]; then echo " [✓] $name" PASS=$((PASS + 1)) else echo " [✗] $name ${note:+— $note}" FAIL=$((FAIL + 1)) [[ -n "$note" ]] && NOTES+=("$name: $note") fi
} BOX_VERSION="$(grep '^version:' "$BOX_DIR/SKILL.md" 2>/dev/null | head -1 | sed -E 's/version: *//' | tr -d ' ')"
BOX_NAME="$(grep '^name:' "$BOX_DIR/SKILL.md" 2>/dev/null | head -1 | sed -E 's/name: *//' | tr -d ' ')" echo ""
echo "╔══════════════════════════════════════════════════╗"
echo "║ AI-Сметчик PRO — smoke-test ║"
echo "║ Имя: ${BOX_NAME:-?} Версия: ${BOX_VERSION:-?}"
echo "╚══════════════════════════════════════════════════╝"
echo ""
echo "Директория коробки: $BOX_DIR"
echo "" # ── 1. СТРУКТУРА (обязательные файлы) ──────────────────────────────────────
echo "── 1. СТРУКТУРА (обязательные файлы) ──" REQUIRED_FILES=( SKILL.md README.md config.yaml .env.example install.sh test/smoke-test.sh examples/quick-start.md examples/full-library.md docs/onboarding.md docs/anti-fail.md docs/roi.md
)
for f in "${REQUIRED_FILES[@]}"; do if [[ -e "$BOX_DIR/$f" ]]; then check "exists: $f" "ok" else check "exists: $f" "fail" "не найден" fi
done # ── 2. PROOF-КЕЙСЫ ────────────────────────────────────────────────────────
echo ""
echo "── 2. Proof-кейсы (5 обязательных) ──"
for n in 01 02 03 04 05; do case_file=$(find "$BOX_DIR/proof" -maxdepth 1 -name "case-${n}*.md" 2>/dev/null | head -1) if [[ -n "$case_file" ]]; then check "proof case-$n" "ok" else check "proof case-$n" "fail" "не найден" fi
done # ── 3. SKILL.md — ClawHub-совместимость ───────────────────────────────────
echo ""
echo "── 3. SKILL.md — ClawHub-совместимость ──" if [[ "$BOX_NAME" == "estimator-pro" ]] || [[ "$BOX_NAME" == "raai-estimator-pro" ]]; then check "manifest name: $BOX_NAME" "ok"
else check "manifest name" "fail" "ожидается estimator-pro, получен: $BOX_NAME"
fi if [[ -n "$BOX_VERSION" ]]; then check "manifest version: $BOX_VERSION" "ok"
else check "manifest version" "fail" "не найден"
fi # Проверка metadata.openclaw
if grep -q "openclaw:" "$BOX_DIR/SKILL.md" 2>/dev/null; then check "metadata.openclaw block" "ok"
else check "metadata.openclaw block" "fail" "отсутствует в SKILL.md"
fi # Проверка emoji
if grep -q 'emoji:' "$BOX_DIR/SKILL.md" 2>/dev/null; then check "metadata.openclaw.emoji" "ok"
else check "metadata.openclaw.emoji" "fail" "не найден"
fi # security_level L1
if grep -q 'security_level:' "$BOX_DIR/SKILL.md" 2>/dev/null; then check "metadata.openclaw.security_level" "ok"
else check "metadata.openclaw.security_level" "fail" "не найден"
fi # always: false
if grep -q 'always: false' "$BOX_DIR/SKILL.md" 2>/dev/null; then check "metadata.openclaw.always: false" "ok"
else check "metadata.openclaw.always" "fail" "должно быть 'always: false'"
fi # ── 4. ТРИГГЕРЫ (25+) ─────────────────────────────────────────────────────
echo ""
echo "── 4. Триггеры ──" TRIGGER_COUNT=$(grep -c '^\s*- ' "$BOX_DIR/SKILL.md" 2>/dev/null | head -1 || echo 0)
if [[ "$TRIGGER_COUNT" -ge 25 ]]; then check "triggers count >= 25 (найдено: $TRIGGER_COUNT)" "ok"
else check "triggers count >= 25 (найдено: $TRIGGER_COUNT)" "fail" "нужно минимум 25 триггеров"
fi # Проверка ключевых RU-триггеров
RU_TRIGGERS=("смета" "материалы" "тендер" "дефектовка" "ФЕР" "ТЕР" "локальная смета" "аудит сметы")
for t in "${RU_TRIGGERS[@]}"; do if grep -qi "$t" "$BOX_DIR/SKILL.md" 2>/dev/null; then check "trigger RU: $t" "ok" else check "trigger RU: $t" "fail" "не найден в SKILL.md" fi
done # Проверка EN-триггеров (для ClawHub поиска)
EN_TRIGGERS=("construction estimate" "BOQ" "bid analysis" "material costs")
for t in "${EN_TRIGGERS[@]}"; do if grep -qi "$t" "$BOX_DIR/SKILL.md" 2>/dev/null; then check "trigger EN: $t" "ok" else check "trigger EN: $t" "fail" "не найден в SKILL.md" fi
done # ── 5. ТЕГИ ──────────────────────────────────────────────────────────────
echo ""
echo "── 5. Теги ──" REQUIRED_TAGS=("russian" "construction" "estimating" "dogfooded")
for t in "${REQUIRED_TAGS[@]}"; do if grep -q "$t" "$BOX_DIR/SKILL.md" 2>/dev/null; then check "tag: $t" "ok" else check "tag: $t" "fail" "не найден в tags: блоке" fi
done # ── 6. ОПИСАНИЕ (EN + RU + ROI 25x) ──────────────────────────────────────
echo ""
echo "── 6. Описание SKILL.md ──" if grep -qi "ROI 25x\|ROI: 25x\|25x\|25-кратн" "$BOX_DIR/SKILL.md" 2>/dev/null; then check "description: ROI 25x упомянут" "ok"
else check "description: ROI 25x" "fail" "ROI 25x не найден в SKILL.md"
fi if grep -qi "джуниора\|60-70%\|replaces" "$BOX_DIR/SKILL.md" 2>/dev/null; then check "description: заменяет сметчика-джуниора" "ok"
else check "description: заменяет сметчика" "fail" "формулировка замены не найдена"
fi # ── 7. CONFIG.YAML ───────────────────────────────────────────────────────
echo ""
echo "── 7. config.yaml ──" if [[ -f "$BOX_DIR/config.yaml" ]]; then check "config.yaml существует" "ok" # Проверка обязательных секций for section in "region:" "normatives:" "roi_model:" "audit:" "leader:"; do if grep -q "$section" "$BOX_DIR/config.yaml" 2>/dev/null; then check "config section: $section" "ok" else check "config section: $section" "fail" "не найдена в config.yaml" fi done
else check "config.yaml существует" "fail"
fi # ── 8. МАРКЕТИНГ ────────────────────────────────────────────────────────
echo ""
echo "── 8. Маркетинг-упаковка ──" MARKETING_FILES=( "marketing/onepager.md" "marketing/comparison.md" "marketing/testimonial-template.md"
)
for f in "${MARKETING_FILES[@]}"; do if [[ -f "$BOX_DIR/$f" ]]; then check "marketing: $f" "ok" else check "marketing: $f" "fail" "не найден" fi
done # ── 9. КОНКУРЕНТЫ ─────────────────────────────────────────────────────
echo ""
echo "── 9. Ресёрч конкурентов ──" if [[ -f "$BOX_DIR/competitors/competitors-comparison.md" ]]; then check "competitors/competitors-comparison.md" "ok"
else check "competitors/competitors-comparison.md" "fail" "не найден"
fi # ── 10. СКРИПТЫ ИСПОЛНЯЕМЫЕ ──────────────────────────────────────────
echo ""
echo "── 10. Исполняемые скрипты ──" for s in install.sh build.sh test/smoke-test.sh; do if [[ -f "$BOX_DIR/$s" ]]; then check "exists: $s" "ok" else check "exists: $s" "fail" fi
done # ── ИТОГ ─────────────────────────────────────────────────────────────
echo ""
echo "══════════════════════════════════════════════════"
TOTAL=$((PASS + FAIL))
echo " ИТОГО: $PASS/$TOTAL PASS"
if [[ $FAIL -gt 0 ]]; then echo "" echo " Проблемы:" for note in "${NOTES[@]}"; do echo " • $note" done echo "" PCTG=$(( PASS * 100 / TOTAL )) echo " Результат: $PCTG% PASS — нужно исправить перед отгрузкой" echo "══════════════════════════════════════════════════" exit 1
else echo "" echo " ВСЕ ПРОВЕРКИ ПРОЙДЕНЫ — коробка готова к отгрузке" echo "══════════════════════════════════════════════════" exit 0
fi
