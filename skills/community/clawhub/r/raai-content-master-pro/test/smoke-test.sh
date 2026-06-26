#!/usr/bin/env bash
# Контент-мастер PRO — smoke-test
# Проверяет корректность установки: структура + YAML + триггеры + ClawHub-совместимость.
# Версия коробки определяется ДИНАМИЧЕСКИ из SKILL.md YAML (без хардкода).
# Время выполнения: ~5-15 секунд. Без внешних вызовов API. set -uo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BOX_DIR="$(cd "$SCRIPT_DIR/.." && pwd)" PASS=0
FAIL=0
NOTES= check { local name="$1" local result="$2" local note="${3:-}" if [[ "$result" == "ok" ]]; then echo " [✓] $name" PASS=$((PASS + 1)) else echo " [✗] $name ${note:+— $note}" FAIL=$((FAIL + 1)) [[ -n "$note" ]] && NOTES+=("$name: $note") fi
} BOX_VERSION="$(grep '^version:' "$BOX_DIR/SKILL.md" 2>/dev/null | head -1 | sed -E 's/version: *//' | tr -d ' ')"
BOX_NAME="$(grep '^name:' "$BOX_DIR/SKILL.md" 2>/dev/null | head -1 | sed -E 's/name: *//' | tr -d ' ')" echo ""
echo "╔══════════════════════════════════════════════════╗"
echo "║ Контент-мастер PRO — smoke-test ║"
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
echo "── 3. SKILL.md — ClawHub-совместимость ──" if [[ "$BOX_NAME" == "content-master-pro" ]] || [[ "$BOX_NAME" == "raai-content-master" ]]; then check "manifest name: $BOX_NAME" "ok"
else check "manifest name" "fail" "ожидается content-master-pro или raai-content-master, получен: ${BOX_NAME:-пусто}"
fi if [[ -n "$BOX_VERSION" ]] && [[ "$BOX_VERSION" =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then check "version semver: $BOX_VERSION" "ok"
else check "version semver" "fail" "ожидается X.Y.Z, получен: ${BOX_VERSION:-пусто}"
fi if (cd "$BOX_DIR" && grep -q "^metadata:" "SKILL.md" && grep -q "openclaw:" "SKILL.md"); then check "metadata.openclaw блок" "ok"
else check "metadata.openclaw блок" "fail" "нужен для ClawHub"
fi if (cd "$BOX_DIR" && grep -q "^tags:" "SKILL.md"); then check "tags: блок" "ok"
else check "tags: блок" "fail"
fi if (cd "$BOX_DIR" && grep -qE "^price: *[0-9]+" "SKILL.md"); then check "price: явная цена" "ok"
else check "price: явная цена" "fail"
fi if (cd "$BOX_DIR" && grep -q "^differentiators:" "SKILL.md"); then check "differentiators: блок" "ok"
else check "differentiators: блок" "fail" "нужен для позиционирования"
fi # ── 4. SKILL.md — ключевые RU и EN триггеры ──
echo ""
echo "── 4. SKILL.md — ключевые RU и EN триггеры ──" RU_TRIGGERS=("контент-план" "стратегия контента" "SEO-ядро" "воронка контента" "анализ конкурентов" "email-цепочка" "tone of voice")
for trg in "${RU_TRIGGERS[@]}"; do if (cd "$BOX_DIR" && grep -Fq "$trg" "SKILL.md" 2>/dev/null); then check "RU trigger: $trg" "ok" else check "RU trigger: $trg" "fail" fi
done EN_TRIGGERS=("content strategy" "content marketing" "email sequence")
for trg in "${EN_TRIGGERS[@]}"; do # grep -i падает на кириллице в Windows bash — используем python для case-insensitive поиска EN TRG_LOWER="$(echo "$trg" | tr '[:upper:]' '[:lower:]')" if (cd "$BOX_DIR" && python -c "
import sys
needle = sys.argv[1].lower
content = open('SKILL.md', encoding='utf-8', errors='replace').read.lower
sys.exit(0 if needle in content else 1)
" "$trg" 2>/dev/null); then check "EN trigger: $trg" "ok" else check "EN trigger: $trg" "fail" fi
done # ── 5. config.yaml — базовая валидность ──
echo ""
echo "── 5. config.yaml — базовая валидность ──" if [[ -f "$BOX_DIR/config.yaml" ]]; then if (cd "$BOX_DIR" && grep -qE "^leader:" "config.yaml"); then check "config: leader: block" "ok" else check "config: leader: block" "fail" fi if (cd "$BOX_DIR" && grep -qE "^business:" "config.yaml"); then check "config: business: block" "ok" else check "config: business: block" "fail" fi if (cd "$BOX_DIR" && grep -qE "^channels:" "config.yaml"); then check "config: channels: block" "ok" else check "config: channels: block" "fail" fi if (cd "$BOX_DIR" && grep -qE "^tone_of_voice:" "config.yaml"); then check "config: tone_of_voice: block" "ok" else check "config: tone_of_voice: block" "fail" fi if (cd "$BOX_DIR" && grep -qE "^roi_model:" "config.yaml"); then check "config: roi_model: block" "ok" else check "config: roi_model: block" "fail" fi
else check "config.yaml" "fail" "не найден"
fi # ── 6. README.md — Quick Start в первых 30 строках ──
echo ""
echo "── 6. README.md — Quick Start в первых 30 строках ──" HEAD_30=$(head -30 "$BOX_DIR/README.md" 2>/dev/null || true)
if echo "$HEAD_30" | LANG=C LC_ALL=C grep -qi "quick start\|15 min"; then check "Quick Start в начале README" "ok"
elif (cd "$BOX_DIR" && head -30 "README.md" | grep -qi "Quick Start\|быстрый старт\|установка\|15 минут"); then check "Quick Start в начале README" "ok"
else check "Quick Start в начале README" "fail"
fi # ── 7. Marketing pack (премиум-бонус) ──
echo ""
echo "── 7. Marketing pack (премиум) ──" if [[ -f "$BOX_DIR/marketing/onepager.md" ]]; then check "marketing/onepager.md" "ok"
else check "marketing/onepager.md" "fail" "нужен для продажи"
fi if [[ -f "$BOX_DIR/marketing/comparison.md" ]]; then check "marketing/comparison.md" "ok"
else check "marketing/comparison.md" "fail"
fi if [[ -f "$BOX_DIR/marketing/testimonial-template.md" ]]; then check "marketing/testimonial-template.md" "ok"
else check "marketing/testimonial-template.md" "fail"
fi # ── 8. Конкуренты и dogfooding ──
echo ""
echo "── 8. Конкуренты и dogfooding ──" if [[ -f "$BOX_DIR/competitors/competitors-comparison.md" ]]; then check "competitors/competitors-comparison.md" "ok"
else check "competitors/competitors-comparison.md" "fail"
fi if [[ -f "$BOX_DIR/proof/dogfooding-RAAI.md" ]]; then check "proof/dogfooding-RAAI.md" "ok"
else check "proof/dogfooding-RAAI.md" "fail" "(опционально — появится после C.2/C.3)"
fi # ── 9. Минимальный размер ключевых файлов ──
echo ""
echo "── 9. Минимальный размер ключевых файлов ──" SKILL_SIZE=$(wc -c < "$BOX_DIR/SKILL.md" 2>/dev/null || echo 0)
if [[ "$SKILL_SIZE" -gt 5000 ]]; then check "SKILL.md размер (>${SKILL_SIZE}b)" "ok"
else check "SKILL.md слишком мал (${SKILL_SIZE}b)" "fail" "ожидается >5000 байт"
fi CONFIG_SIZE=$(wc -c < "$BOX_DIR/config.yaml" 2>/dev/null || echo 0)
if [[ "$CONFIG_SIZE" -gt 2000 ]]; then check "config.yaml размер (>${CONFIG_SIZE}b)" "ok"
else check "config.yaml слишком мал (${CONFIG_SIZE}b)" "fail"
fi # ── ИТОГ ──
echo ""
echo "──────────────────────────────────────────"
TOTAL=$((PASS + FAIL))
echo " ИТОГО: [✓] $PASS / $TOTAL [✗] $FAIL"
echo "──────────────────────────────────────────"
echo "" if [[ $FAIL -eq 0 ]]; then echo "PASS — коробка ${BOX_NAME} v${BOX_VERSION} установлена корректно." echo "" echo "Следующий шаг: заполните business/channels/tone_of_voice в config.yaml" echo "и напишите боту триггер 'контент-план на месяц'." exit 0
else echo "FAIL — есть $FAIL проблем:" for note in "${NOTES[@]}"; do echo " • $note"; done echo "" echo "Решение: см. docs/anti-fail.md." exit 1
fi
