#!/usr/bin/env bash
# AI-База знаний PRO — smoke-test
# Проверяет что коробка установлена корректно:
# структура файлов + YAML-валидность + триггеры + ClawHub-совместимость.
# Версия коробки определяется ДИНАМИЧЕСКИ из SKILL.md (без хардкода).
# Время выполнения: ~3-10 секунд. Без внешних вызовов API. set -uo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BOX_DIR="$(cd "$SCRIPT_DIR/.." && pwd)" PASS=0
FAIL=0
NOTES= check { local name="$1" local result="$2" local note="${3:-}" if [[ "$result" == "ok" ]]; then echo " [OK] $name" PASS=$((PASS + 1)) else echo " [!!] $name ${note:+-- $note}" FAIL=$((FAIL + 1)) [[ -n "$note" ]] && NOTES+=("$name: $note") fi
} BOX_VERSION="$(grep '^version:' "$BOX_DIR/SKILL.md" 2>/dev/null | head -1 | sed -E 's/version: *//' | tr -d ' ')"
BOX_NAME="$(grep '^name:' "$BOX_DIR/SKILL.md" 2>/dev/null | head -1 | sed -E 's/name: *//' | tr -d ' ')" echo ""
echo "======================================================"
echo " AI-База знаний PRO -- smoke-test"
echo " Имя: ${BOX_NAME:-?} Версия: ${BOX_VERSION:-?}"
echo "======================================================"
echo ""
echo "Директория коробки: $BOX_DIR"
echo "" # ── 1. СТРУКТУРА (обязательные файлы) ──────────────────
echo "-- 1. СТРУКТУРА (обязательные файлы) --" REQUIRED_FILES=( SKILL.md README.md config.yaml .env.example install.sh build.sh test/smoke-test.sh examples/quick-start.md examples/full-library.md docs/onboarding.md docs/anti-fail.md docs/roi.md
)
for f in "${REQUIRED_FILES[@]}"; do if [[ -e "$BOX_DIR/$f" ]]; then check "exists: $f" "ok" else check "exists: $f" "fail" "не найден" fi
done # ── 2. Proof-кейсы (5 обязательных) ───────────────────
echo ""
echo "-- 2. Proof-кейсы (5 обязательных) --"
for n in 01 02 03 04 05; do case_file=$(ls "$BOX_DIR/proof/case-${n}"*.md 2>/dev/null | head -1) if [[ -n "$case_file" ]]; then check "proof case-$n: $(basename "$case_file")" "ok" else check "proof case-$n" "fail" "нет файла case-${n}*.md в proof/" fi
done # ── 3. SKILL.md — ClawHub-совместимость ───────────────
echo ""
echo "-- 3. SKILL.md -- ClawHub-совместимость --" if [[ "$BOX_NAME" == "knowledge-base-pro" ]] || [[ "$BOX_NAME" == "raai-knowledge-base" ]]; then check "manifest name: $BOX_NAME" "ok"
else check "manifest name" "fail" "ожидается knowledge-base-pro или raai-knowledge-base, получено: $BOX_NAME"
fi if [[ -n "$BOX_VERSION" ]] && [[ "$BOX_VERSION" =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then check "version semver: $BOX_VERSION" "ok"
else check "version semver" "fail" "ожидается X.Y.Z, получено: ${BOX_VERSION:-пусто}"
fi if grep -q "^metadata:" "$BOX_DIR/SKILL.md" 2>/dev/null && grep -q "openclaw:" "$BOX_DIR/SKILL.md" 2>/dev/null; then check "metadata.openclaw блок" "ok"
else check "metadata.openclaw блок" "fail" "нужен для ClawHub"
fi if grep -q "^tags:" "$BOX_DIR/SKILL.md" 2>/dev/null; then check "tags: блок" "ok"
else check "tags: блок" "fail"
fi if grep -qE "^price: *[0-9]+" "$BOX_DIR/SKILL.md" 2>/dev/null; then check "price: явная цена" "ok"
else check "price: поле" "fail" "нужна явная цена числом"
fi # ── 4. SKILL.md — RU + EN триггеры (25+) ─────────────
echo ""
echo "-- 4. SKILL.md -- ключевые RU триггеры --" RU_TRIGGERS=( "база знаний" "FAQ" "онбординг" "новый сотрудник" "регламент" "найди в базе" "добавь в базу" "аудит базы" "gap анализ" "SOP" "поиск по документам" "часто задаваемые вопросы"
)
for trg in "${RU_TRIGGERS[@]}"; do if grep -Fq "$trg" "$BOX_DIR/SKILL.md" 2>/dev/null; then check "RU trigger: $trg" "ok" else check "RU trigger: $trg" "fail" fi
done echo ""
echo "-- 4b. SKILL.md -- ключевые EN триггеры --" EN_TRIGGERS=( "knowledge base" "onboarding" "FAQ bot" "semantic search" "Q&A"
)
for trg in "${EN_TRIGGERS[@]}"; do if grep -Fq "$trg" "$BOX_DIR/SKILL.md" 2>/dev/null; then check "EN trigger: $trg" "ok" else check "EN trigger: $trg" "fail" fi
done # ── 5. config.yaml — базовая валидность ───────────────
echo ""
echo "-- 5. config.yaml -- базовая валидность --" if [[ -f "$BOX_DIR/config.yaml" ]]; then if grep -qE "^company:" "$BOX_DIR/config.yaml" 2>/dev/null; then check "config: company: block" "ok" else check "config: company: block" "fail" fi if grep -qE "^kb:" "$BOX_DIR/config.yaml" 2>/dev/null; then check "config: kb: block" "ok" else check "config: kb: block" "fail" fi if grep -qi "OBLIGATORY\|обязат\|первом запуске" "$BOX_DIR/config.yaml" 2>/dev/null; then check "config: маркировка обязательных полей" "ok" else check "config: маркировка обязательных полей" "fail" fi
else check "config.yaml" "fail" "не найден"
fi # ── 6. README.md — Quick Start в первых 30 строках ───
echo ""
echo "-- 6. README.md -- Quick Start --" HEAD_30=$(head -30 "$BOX_DIR/README.md" 2>/dev/null || echo "")
if echo "$HEAD_30" | grep -qi "quick start\|быстрый старт\|15 минут\|установка"; then check "Quick Start в начале README" "ok"
else check "Quick Start в начале README" "fail"
fi # ── 7. .env.example — ключевые переменные ─────────────
echo ""
echo "-- 7. .env.example -- ключевые переменные --" if [[ -f "$BOX_DIR/.env.example" ]]; then for env_var in ANTHROPIC_API_KEY OPENAI_API_KEY NOTION_API_KEY TELEGRAM_BOT_TOKEN; do if grep -q "$env_var" "$BOX_DIR/.env.example" 2>/dev/null; then check ".env.example: $env_var" "ok" else check ".env.example: $env_var" "fail" fi done
else check ".env.example" "fail" "не найден"
fi # ── 8. Маркетинг и конкуренты ─────────────────────────
echo ""
echo "-- 8. Marketing pack --" for mkt_file in marketing/onepager.md marketing/comparison.md marketing/testimonial-template.md; do if [[ -f "$BOX_DIR/$mkt_file" ]]; then check "$mkt_file" "ok" else check "$mkt_file" "fail" fi
done if [[ -f "$BOX_DIR/competitors/competitors-comparison.md" ]]; then check "competitors/competitors-comparison.md" "ok"
else check "competitors/competitors-comparison.md" "fail"
fi # ── 9. SKILL.md — дифференциаторы и 3 уровня продукта
echo ""
echo "-- 9. SKILL.md -- ключевые маркетинговые блоки --" if grep -qi "дифференциатор\|differentiator\|Before.*After\|БЫЛО.*СТАЛО" "$BOX_DIR/SKILL.md" 2>/dev/null; then check "Before/After или дифференциаторы в SKILL.md" "ok"
else check "Before/After или дифференциаторы в SKILL.md" "fail"
fi if grep -qi "скилл.*агент.*приложение\|три уровня\|three.*level\|уровн" "$BOX_DIR/SKILL.md" 2>/dev/null; then check "3 уровня продукта в SKILL.md" "ok"
else check "3 уровня продукта в SKILL.md" "fail"
fi if grep -qi "экономи\|ROI\|рублей\|₽" "$BOX_DIR/SKILL.md" 2>/dev/null; then check "ROI/экономия в описании SKILL.md" "ok"
else check "ROI/экономия в описании SKILL.md" "fail"
fi # ── ИТОГ ───────────────────────────────────────────────
echo ""
echo "------------------------------------------------------"
TOTAL=$((PASS + FAIL))
echo " ИТОГО: [OK] $PASS / $TOTAL [!!] $FAIL"
echo "------------------------------------------------------"
echo "" if [[ $FAIL -eq 0 ]]; then echo "PASS -- коробка $BOX_NAME v$BOX_VERSION установлена корректно." echo "" echo "Следующий шаг: заполните OBLIGATORY поля в config.yaml" echo "и напишите боту триггер 'база знаний' или 'онбординг'." exit 0
else echo "FAIL -- есть $FAIL проблем:" for note in "${NOTES[@]}"; do echo " * $note"; done echo "" echo "Решение: см. docs/anti-fail.md." exit 1
fi
