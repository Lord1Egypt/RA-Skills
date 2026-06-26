#!/usr/bin/env bash
# build.sh — собирает AI-Сметчик PRO в отгрузочный ZIP из исходника.
# ЭТО ЕДИНСТВЕННЫЙ СПОСОБ СОБРАТЬ ZIP. Ручное редактирование ZIP запрещено.
# БЕЗ python3 — упаковка через zip / 7z / powershell (Windows).
#
# Использование:
# ./build.sh # собрать на основе version из SKILL.md
# ./build.sh 3.5.1 # собрать с конкретной версией (override)
#
# Выход: ../zips-v<VER>/estimator-pro-v<VER>.zip set -euo pipefail SRC_DIR="$(cd "$(dirname "$0")" && pwd)"
SLUG="estimator-pro" # Версия из SKILL.md или переопределённая аргументом
if [[ -n "${1:-}" ]]; then VER="$1"
else VER="$(grep '^version:' "$SRC_DIR/SKILL.md" | head -1 | sed -E 's/version: *//' | tr -d ' ')"
fi
[[ -z "$VER" ]] && { echo "ERROR: version not detected"; exit 1; } OUT_DIR="$(cd "$SRC_DIR/.." && pwd)/zips-v${VER}"
ZIP_NAME="${SLUG}-v${VER}.zip"
STAGE_DIR="$(mktemp -d)/${SLUG}-v${VER}" echo "==> Building $ZIP_NAME (ver=$VER)"
echo " Source : $SRC_DIR"
echo " Output : $OUT_DIR/$ZIP_NAME" mkdir -p "$OUT_DIR"
mkdir -p "$STAGE_DIR" # Состав отгрузочного ZIP (строго по эталону PREMIUM_BOX_STANDARD)
FILES=( SKILL.md README.md config.yaml .env.example install.sh test/smoke-test.sh examples/quick-start.md examples/full-library.md docs/onboarding.md docs/anti-fail.md docs/roi.md proof/case-01-slow-estimate-chaos.md proof/case-02-contractor-overpricing-found.md proof/case-03-volume-dispute-resolved.md proof/case-04-documents-scattered.md proof/case-05-budget-not-defended.md
) # Опциональные (включаются если существуют — только одиночные файлы, папки идут через dir-цикл ниже)
OPTIONAL=( docs/competitors-comparison.md
) for f in "${FILES[@]}"; do if [[ ! -f "$SRC_DIR/$f" ]]; then echo "ERROR: missing required file: $f" exit 1 fi mkdir -p "$STAGE_DIR/$(dirname "$f")" cp "$SRC_DIR/$f" "$STAGE_DIR/$f"
done for f in "${OPTIONAL[@]}"; do if [[ -f "$SRC_DIR/$f" ]]; then mkdir -p "$STAGE_DIR/$(dirname "$f")" cp "$SRC_DIR/$f" "$STAGE_DIR/$f" echo " +optional: $f" fi
done # Marketing pack и competitors — включаются целиком если есть
for sub in marketing competitors; do if [[ -d "$SRC_DIR/$sub" ]]; then cp -R "$SRC_DIR/$sub" "$STAGE_DIR/$sub" echo " +dir: $sub/" fi
done # Упаковка — кросс-платформенная (zip / 7z / powershell, БЕЗ python3)
cd "$(dirname "$STAGE_DIR")"
if command -v zip >/dev/null 2>&1; then zip -qr "$OUT_DIR/$ZIP_NAME" "$(basename "$STAGE_DIR")" echo " packed via: zip"
elif command -v 7z >/dev/null 2>&1; then 7z a -tzip "$OUT_DIR/$ZIP_NAME" "$(basename "$STAGE_DIR")" >/dev/null echo " packed via: 7z"
elif command -v powershell.exe >/dev/null 2>&1 || command -v powershell >/dev/null 2>&1; then PSH="$(command -v powershell.exe 2>/dev/null || command -v powershell)" WIN_SRC="$(cygpath -w "$STAGE_DIR" 2>/dev/null || echo "$STAGE_DIR")" WIN_OUT="$(cygpath -w "$OUT_DIR/$ZIP_NAME" 2>/dev/null || echo "$OUT_DIR/$ZIP_NAME")" "$PSH" -NoProfile -Command "Compress-Archive -Path '${WIN_SRC}' -DestinationPath '${WIN_OUT}' -Force" echo " packed via: powershell Compress-Archive"
else echo "ERROR: no zip/7z/powershell available for archiving" exit 1
fi
rm -rf "$(dirname "$STAGE_DIR")" echo ""
echo "==> DONE"
echo " $OUT_DIR/$ZIP_NAME"
ls -la "$OUT_DIR/$ZIP_NAME" 2>/dev/null || echo " (ls unavailable on this platform)"
echo "" # Список файлов в ZIP
if command -v unzip >/dev/null 2>&1; then echo "Contents:" unzip -l "$OUT_DIR/$ZIP_NAME" | tail -35
elif command -v 7z >/dev/null 2>&1; then echo "Contents:" 7z l "$OUT_DIR/$ZIP_NAME" | tail -35
fi # Smoke-test на свежераспакованном ZIP (пропускается если SMOKE_TEST=0)
if [[ "${SMOKE_TEST:-1}" != "0" ]]; then echo "" echo "==> Running smoke-test on fresh ZIP..." TEST_DIR="$(mktemp -d)" if command -v unzip >/dev/null 2>&1; then unzip -q "$OUT_DIR/$ZIP_NAME" -d "$TEST_DIR" elif command -v 7z >/dev/null 2>&1; then 7z x "$OUT_DIR/$ZIP_NAME" -o"$TEST_DIR" -y >/dev/null elif command -v powershell.exe >/dev/null 2>&1 || command -v powershell >/dev/null 2>&1; then PSH2="$(command -v powershell.exe 2>/dev/null || command -v powershell)" WIN_ZIP="$(cygpath -w "$OUT_DIR/$ZIP_NAME" 2>/dev/null || echo "$OUT_DIR/$ZIP_NAME")" WIN_DEST="$(cygpath -w "$TEST_DIR" 2>/dev/null || echo "$TEST_DIR")" "$PSH2" -NoProfile -Command "Expand-Archive -Path '${WIN_ZIP}' -DestinationPath '${WIN_DEST}' -Force" fi cd "$TEST_DIR/${SLUG}-v${VER}" if [[ -f test/smoke-test.sh ]]; then bash test/smoke-test.sh || { echo "SMOKE-TEST FAILED"; rm -rf "$TEST_DIR"; exit 1; } else echo " (smoke-test.sh not found — skipped)" fi rm -rf "$TEST_DIR"
fi
