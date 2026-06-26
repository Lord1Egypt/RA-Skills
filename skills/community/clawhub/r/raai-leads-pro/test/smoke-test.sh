#!/usr/bin/env bash
# AI-Лиды PRO — smoke-test
# Проверяет что коробка установлена корректно: структура, YAML, триггеры, ClawHub-совместимость.
# Версия определяется динамически из SKILL.md.
# Время: ~5-10 секунд. Без внешних API-вызовов. set -uo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BOX_DIR="$(cd "$SCRIPT_DIR/.." && pwd)" PASS=0
FAIL=0
NOTES= check { local name="$1" local result="$2" local note="${3:-}" if [[ "$result" == "ok" ]]; then echo " [✓] $name" PASS=$((PASS + 1)) else echo " [✗] $name ${note:+— $note}" FAIL=$((FAIL + 1)) [[ -n "$note" ]] && NOTES+=("$name: $note") fi
} BOX_VERSION="$(grep '^version:' "$BOX_DIR/SKILL.md" 2>/dev/null | head -1 | sed -E 's/version: *//' | tr -d ' ')"
BOX_NAME="$(grep '^name:' "$BOX_DIR/SKILL.md" 2>/dev/null | head -1 | sed -E 's/name: *//' | tr -d ' ')" echo ""
echo "╔══════════════════════════════════════════════════╗"
echo "║ AI-Лиды PRO — smoke-test ║"
echo "║ Имя: ${BOX_NAME:-?} Версия: ${BOX_VERSION:-?}"
echo "╚══════════════════════════════════════════════════╝"
echo ""
echo "Директория коробки: $BOX_DIR"
echo "" # ── 1. СТРУКТУРА (обязательные файлы) ──────────────────
echo "── 1. СТРУКТУРА (обязательные файлы) ──"
REQUIRED_FILES=( SKILL.md README.md config.yaml .env.example install.sh test/smoke-test.sh examples/quick-start.md examples/full-library.md docs/onboarding.md docs/anti-fail.md docs/roi.md
)
for f in "${REQUIRED_FILES[@]}"; do if [[ -e "$BOX_DIR/$f" ]]; then check "exists: $f" "ok" else check "exists: $f" "fail" "не найден" fi
done # ── 2. PROOF-КЕЙСЫ (5 обязательных) ───────────────────
echo ""
echo "── 2. Proof-кейсы (5 обязательных) ──"
for n in 01 02 03 04 05; do case_file=$(find "$BOX_DIR/proof" -maxdepth 1 -name "case-${n}*.md" 2>/dev/null | head -1) if [[ -n "$case_file" ]]; then check "proof case-$n" "ok" else check "proof case-$n" "fail" fi
done # ── 3. SKILL.md — ClawHub-совместимость ────────────────
echo ""
echo "── 3. SKILL.md — ClawHub-совместимость ──" if [[ "$BOX_NAME" == "leads-pro" ]] || [[ "$BOX_NAME" == "raai-leads-pro" ]]; then check "manifest name: $BOX_NAME" "ok"
else check "manifest name" "fail" "ожидается leads-pro или raai-leads-pro, получено: $BOX_NAME"
fi if [[ -n "$BOX_VERSION" ]] && [[ "$BOX_VERSION" =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then check "version semver: $BOX_VERSION" "ok"
else check "version semver" "fail" "ожидается X.Y.Z, получено: ${BOX_VERSION:-пусто}"
fi if grep -q "^metadata:" "$BOX_DIR/SKILL.md" && grep -q "openclaw:" "$BOX_DIR/SKILL.md"; then check "metadata.openclaw блок" "ok"
else check "metadata.openclaw блок" "fail" "нужен для ClawHub-совместимости"
fi if grep -q "^tags:" "$BOX_DIR/SKILL.md"; then check "tags: блок" "ok"
else check "tags: блок" "fail"
fi if grep -qE "^price: *[0-9]+" "$BOX_DIR/SKILL.md"; then check "price: явная цена" "ok"
else check "price:" "fail" "добавьте price: 20000 в YAML-заголовок"
fi if grep -q "dogfooded_in:" "$BOX_DIR/SKILL.md"; then check "dogfooded_in: поле" "ok"
else check "dogfooded_in:" "fail"
fi # ── 4. SKILL.md — RU и EN триггеры (leads-specific) ──
echo ""
echo "── 4. SKILL.md — ключевые RU триггеры ──"
RU_TRIGGERS=( "лидогенерация" "квалификация лидов" "обогащение лидов" "BANT" "автоворонка" "отчёт лиды" "скоринг"
)
for trg in "${RU_TRIGGERS[@]}"; do if grep -Fq "$trg" "$BOX_DIR/SKILL.md" 2>/dev/null; then check "RU trigger: $trg" "ok" else check "RU trigger: $trg" "fail" fi
done echo ""
echo "── 5. SKILL.md — EN триггеры (ClawHub search) ──"
EN_TRIGGERS=( "lead generation" "lead qualification" "lead enrichment" "lead scoring" "ICP" "outbound"
)
for trg in "${EN_TRIGGERS[@]}"; do # grep -F (без -i) — избегаем Aborted на больших файлах в Windows/Git-bash if grep -Fq "$trg" "$BOX_DIR/SKILL.md" 2>/dev/null; then check "EN trigger: $trg" "ok" else check "EN trigger: $trg" "fail" fi
done # ── 6. CONFIG.YAML ──────────────────────────────────────
echo ""
echo "── 6. config.yaml — базовая валидность ──"
if [[ -f "$BOX_DIR/config.yaml" ]]; then if grep -qE "^company:" "$BOX_DIR/config.yaml"; then check "config: company: block" "ok" else check "config: company: block" "fail" fi if grep -qE "^sales:" "$BOX_DIR/config.yaml"; then check "config: sales: block" "ok" else check "config: sales: block" "fail" fi if grep -qi "OBLIGATORY\|обязат" "$BOX_DIR/config.yaml"; then check "config: маркировка OBLIGATORY полей" "ok" else check "config: маркировка OBLIGATORY полей" "fail" fi
else check "config.yaml" "fail" "не найден"
fi # ── 7. README — Quick Start в первых 30 строках ─────────
echo ""
echo "── 7. README.md — Quick Start в первых 30 строках ──"
HEAD_30=$(head -30 "$BOX_DIR/README.md" 2>/dev/null)
if echo "$HEAD_30" | grep -qi "quick start\|быстрый старт\|установка\|15 минут"; then check "Quick Start в начале README" "ok"
else check "Quick Start в начале README" "fail"
fi # ── 8. МАРКЕТИНГ и КОНКУРЕНТЫ ──────────────────────────
echo ""
echo "── 8. Marketing pack + competitors ──"
if [[ -f "$BOX_DIR/marketing/onepager.md" ]]; then check "marketing/onepager.md" "ok"
else check "marketing/onepager.md" "fail"
fi
if [[ -f "$BOX_DIR/marketing/comparison.md" ]]; then check "marketing/comparison.md" "ok"
else check "marketing/comparison.md" "fail"
fi
if [[ -f "$BOX_DIR/marketing/testimonial-template.md" ]]; then check "marketing/testimonial-template.md" "ok"
else check "marketing/testimonial-template.md" "fail"
fi
if [[ -f "$BOX_DIR/competitors/competitors-comparison.md" ]]; then check "competitors/competitors-comparison.md" "ok"
else check "competitors/competitors-comparison.md" "fail"
fi # ── 9. ENV EXAMPLE ──────────────────────────────────────
echo ""
echo "── 9. .env.example — ключевые блоки ──"
if [[ -f "$BOX_DIR/.env.example" ]]; then if grep -q "ANTHROPIC_API_KEY\|OPENAI_API_KEY" "$BOX_DIR/.env.example"; then check ".env.example: LLM API ключи" "ok" else check ".env.example: LLM API ключи" "fail" fi if grep -q "TELEGRAM_BOT_TOKEN" "$BOX_DIR/.env.example"; then check ".env.example: Telegram" "ok" else check ".env.example: Telegram" "fail" fi if grep -q "GOOGLE_SHEETS" "$BOX_DIR/.env.example"; then check ".env.example: Google Sheets" "ok" else check ".env.example: Google Sheets" "fail" fi if grep -q "AMOCRM\|BITRIX24\|HUBSPOT" "$BOX_DIR/.env.example"; then check ".env.example: CRM интеграция" "ok" else check ".env.example: CRM интеграция" "fail" fi if grep -q "APOLLO_API_KEY\|FINDYMAIL\|TARGETHUNTER" "$BOX_DIR/.env.example"; then check ".env.example: парсеры/обогащение" "ok" else check ".env.example: парсеры/обогащение" "fail" fi
else check ".env.example" "fail" "не найден"
fi # ── ИТОГ ────────────────────────────────────────────────
echo ""
echo "──────────────────────────────────────────"
TOTAL=$((PASS + FAIL))
echo " ИТОГО: [✓] $PASS / $TOTAL [✗] $FAIL"
echo "──────────────────────────────────────────"
echo "" if [[ $FAIL -eq 0 ]]; then echo "PASS — коробка $BOX_NAME v$BOX_VERSION установлена корректно." echo "" echo "Следующий шаг: заполните OBLIGATORY поля в config.yaml и напишите боту триггер 'аватар' или 'где брать лидов'." exit 0
else echo "FAIL — есть $FAIL проблем:" for note in "${NOTES[@]}"; do echo " • $note"; done echo "" echo "Решение: см. docs/anti-fail.md." exit 1
fi
