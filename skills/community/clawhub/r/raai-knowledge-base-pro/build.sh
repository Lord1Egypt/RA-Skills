#!/usr/bin/env bash
# build.sh — собирает knowledge-base-pro в отгрузочный ZIP из исходника.
# ЭТО ЕДИНСТВЕННЫЙ СПОСОБ СОБРАТЬ ZIP. Ручное редактирование ZIP запрещено.
#
# Использование:
# ./build.sh # собрать на основе version из SKILL.md
# ./build.sh 3.5.1 # собрать с конкретной версией (override)
#
# Выход: ../zips-v<VER>/knowledge-base-pro-v<VER>.zip
#
# ВАЖНО: Python3/python3 как fallback НЕ используется —
# на Windows python3 = Microsoft Store shim, открывает магазин.
# Порядок: zip → 7z → powershell Compress-Archive. set -euo pipefail SRC_DIR="$(cd "$(dirname "$0")" && pwd)"
SLUG="knowledge-base-pro" # Версия из SKILL.md или переопределённая аргументом
if [[ -n "${1:-}" ]]; then VER="$1"
else VER="$(grep '^version:' "$SRC_DIR/SKILL.md" | head -1 | sed -E 's/version: *//' | tr -d ' ')"
fi
[[ -z "$VER" ]] && { echo "ERROR: version not detected"; exit 1; } OUT_DIR="$(cd "$SRC_DIR/.." && pwd)/zips-v${VER}"
ZIP_NAME="${SLUG}-v${VER}.zip"
STAGE_DIR="$(mktemp -d)/${SLUG}-v${VER}" echo "==> Building $ZIP_NAME (ver=$VER)"
echo " Source : $SRC_DIR"
echo " Output : $OUT_DIR/$ZIP_NAME" mkdir -p "$OUT_DIR"
mkdir -p "$STAGE_DIR" # Состав отгрузочного ZIP (строго по эталону PREMIUM_BOX_STANDARD)
FILES=( SKILL.md README.md config.yaml .env.example install.sh test/smoke-test.sh examples/quick-start.md examples/full-library.md docs/onboarding.md docs/anti-fail.md docs/roi.md
) # Proof-кейсы — искать все case-0N*.md в proof/
for f in "${FILES[@]}"; do if [[ ! -f "$SRC_DIR/$f" ]]; then echo "ERROR: missing required file: $f" exit 1 fi mkdir -p "$STAGE_DIR/$(dirname "$f")" cp "$SRC_DIR/$f" "$STAGE_DIR/$f"
done # Proof-кейсы (динамически — все case-*.md в proof/)
mkdir -p "$STAGE_DIR/proof"
if ls "$SRC_DIR/proof/case-"*.md >/dev/null 2>&1; then for f in "$SRC_DIR/proof/case-"*.md; do cp "$f" "$STAGE_DIR/proof/" done
else echo "WARNING: no proof/case-*.md found"
fi # Опциональные файлы (включаются если существуют)
OPTIONAL=( proof/dogfooding-RAAI.md docs/competitors-comparison.md
) for f in "${OPTIONAL[@]}"; do if [[ -f "$SRC_DIR/$f" ]]; then mkdir -p "$STAGE_DIR/$(dirname "$f")" cp "$SRC_DIR/$f" "$STAGE_DIR/$f" echo " +optional: $f" fi
done # Marketing / competitors / demo — включаются целиком если папка есть
for sub in marketing competitors demo; do if [[ -d "$SRC_DIR/$sub" ]]; then cp -R "$SRC_DIR/$sub" "$STAGE_DIR/$sub" echo " +dir: $sub/" fi
done # Упаковка — кросс-платформенная (zip → 7z → powershell Compress-Archive)
# НЕ используем python3 — на Windows python3 = Microsoft Store shim
cd "$(dirname "$STAGE_DIR")"
if command -v zip >/dev/null 2>&1; then zip -qr "$OUT_DIR/$ZIP_NAME" "$(basename "$STAGE_DIR")"
elif command -v 7z >/dev/null 2>&1; then 7z a -tzip "$OUT_DIR/$ZIP_NAME" "$(basename "$STAGE_DIR")" >/dev/null
elif command -v powershell.exe >/dev/null 2>&1 || command -v powershell >/dev/null 2>&1; then PSH="$(command -v powershell.exe 2>/dev/null || command -v powershell)" WIN_SRC="$(cygpath -w "$(pwd)/$(basename "$STAGE_DIR")" 2>/dev/null || echo "$(pwd)/$(basename "$STAGE_DIR")")" WIN_OUT="$(cygpath -w "$OUT_DIR/$ZIP_NAME" 2>/dev/null || echo "$OUT_DIR/$ZIP_NAME")" "$PSH" -NoProfile -Command "Compress-Archive -Path '${WIN_SRC}' -DestinationPath '${WIN_OUT}' -Force"
else echo "ERROR: no zip/7z/powershell available for archiving. Install one of them." exit 1
fi
rm -rf "$(dirname "$STAGE_DIR")" echo "==> DONE"
echo " $OUT_DIR/$ZIP_NAME"
ls -la "$OUT_DIR/$ZIP_NAME" 2>/dev/null || echo " (ls не доступен, но файл создан)"
echo ""
echo "Contents:"
if command -v unzip >/dev/null 2>&1; then unzip -l "$OUT_DIR/$ZIP_NAME" | tail -35
elif command -v 7z >/dev/null 2>&1; then 7z l "$OUT_DIR/$ZIP_NAME" | tail -35
fi
echo "" # Smoke-test на свежераспакованном ZIP
if [[ "${SMOKE_TEST:-1}" != "0" ]]; then echo "==> Running smoke-test on fresh ZIP..." TEST_DIR="$(mktemp -d)" if command -v unzip >/dev/null 2>&1; then unzip -q "$OUT_DIR/$ZIP_NAME" -d "$TEST_DIR" elif command -v 7z >/dev/null 2>&1; then 7z x "$OUT_DIR/$ZIP_NAME" -o"$TEST_DIR" >/dev/null fi cd "$TEST_DIR/${SLUG}-v${VER}" if [[ -x test/smoke-test.sh ]]; then bash test/smoke-test.sh || { echo "SMOKE-TEST FAILED"; exit 1; } else echo " (smoke-test.sh not found or not executable — skipped)" fi rm -rf "$TEST_DIR"
fi
