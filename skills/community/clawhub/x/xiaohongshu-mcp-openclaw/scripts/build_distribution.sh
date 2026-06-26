#!/usr/bin/env bash
set -euo pipefail

BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SKILL_NAME="$(basename "$BASE_DIR")"
DIST_DIR="${1:-$BASE_DIR/dist}"
STAMP="$(date +%Y%m%d-%H%M%S)"
PKG_NAME="${SKILL_NAME}-${STAMP}"
STAGE_DIR="$(mktemp -d "/tmp/${SKILL_NAME}.XXXXXX")"
OUT_TAR="${DIST_DIR}/${PKG_NAME}.tar.gz"
OUT_ZIP="${DIST_DIR}/${PKG_NAME}.zip"
BUILD_ZIP="${XHS_BUILD_ZIP:-0}"

cleanup() {
  rm -rf "$STAGE_DIR"
}
trap cleanup EXIT INT TERM

mkdir -p "$DIST_DIR"
mkdir -p "$STAGE_DIR/$SKILL_NAME"

echo "[INFO] staging files..."
shopt -s dotglob
for entry in "$BASE_DIR"/*; do
  cp -R "$entry" "$STAGE_DIR/$SKILL_NAME/"
done
shopt -u dotglob
rm -rf "$STAGE_DIR/$SKILL_NAME/.git" || true
rm -rf "$STAGE_DIR/$SKILL_NAME/dist" || true
find "$STAGE_DIR/$SKILL_NAME" -type d -name "__pycache__" -prune -exec rm -rf {} +
find "$STAGE_DIR/$SKILL_NAME" -name ".DS_Store" -delete

if command -v git >/dev/null 2>&1; then
  COMMIT_ID="$(git -C "$BASE_DIR" rev-parse --short HEAD 2>/dev/null || echo unknown)"
else
  COMMIT_ID="unknown"
fi

cat > "$STAGE_DIR/$SKILL_NAME/DISTRIBUTION.md" <<EOF
# Distribution Info

- Skill: $SKILL_NAME
- Package: $PKG_NAME
- Build Time: $(date -u +"%Y-%m-%dT%H:%M:%SZ")
- Source Commit: $COMMIT_ID

## Quick Start

\`\`\`bash
bash scripts/preflight.sh
bash scripts/install_to_openclaw.sh
bash scripts/quickstart.sh
\`\`\`
EOF

echo "[INFO] creating tarball: $OUT_TAR"
LC_ALL=C LANG=C LC_CTYPE=C tar -C "$STAGE_DIR" -czf "$OUT_TAR" "$SKILL_NAME"

if [ "$BUILD_ZIP" = "1" ] && command -v zip >/dev/null 2>&1; then
  echo "[INFO] creating zip: $OUT_ZIP"
  (
    cd "$STAGE_DIR"
    LC_ALL=C LANG=C LC_CTYPE=C zip -rq "$OUT_ZIP" "$SKILL_NAME"
  )
else
  echo "[INFO] skip zip package (set XHS_BUILD_ZIP=1 to enable)"
fi

sha_file="${DIST_DIR}/${PKG_NAME}.sha256"
if command -v shasum >/dev/null 2>&1; then
  {
    LC_ALL=C LANG=C LC_CTYPE=C shasum -a 256 "$OUT_TAR"
    [ -f "$OUT_ZIP" ] && LC_ALL=C LANG=C LC_CTYPE=C shasum -a 256 "$OUT_ZIP"
  } > "$sha_file"
elif command -v sha256sum >/dev/null 2>&1; then
  {
    sha256sum "$OUT_TAR"
    [ -f "$OUT_ZIP" ] && sha256sum "$OUT_ZIP"
  } > "$sha_file"
fi

echo "[DONE] distribution package created"
echo "[INFO] tar: $OUT_TAR"
[ -f "$OUT_ZIP" ] && echo "[INFO] zip: $OUT_ZIP"
[ -f "$sha_file" ] && echo "[INFO] checksum: $sha_file"
