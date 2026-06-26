#!/usr/bin/env bash
# Phase 5h: Visual Baseline Generation
#
# Generates PPTX from all test fixtures for visual review.
# Requires libreoffice for PPTX→image conversion (not installed on this system).
#
# Usage:
#   ./generate-baselines.sh                     # generate PPTX only
#   ./generate-baselines.sh --convert           # PPTX → PNG (requires libreoffice)
#   ./generate-baselines.sh --open              # open baselines dir
#
# Prerequisites:
#   - node + npm dependencies installed
#   - For --convert: libreoffice (soffice) on PATH

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"
BASELINES_DIR="$SCRIPT_DIR"
FIXTURES_DIR="$PROJECT_DIR/tests/fixtures"
RENDER_SCRIPT="$PROJECT_DIR/scripts/render.js"

# Ensure output dir exists
mkdir -p "$BASELINES_DIR"

echo "=== Visual Baseline Generation ==="
echo "Output: $BASELINES_DIR"
echo ""

# Collect all content-*.json fixtures
FIXTURES=()
while IFS= read -r f; do
  FIXTURES+=("$f")
done < <(ls "$FIXTURES_DIR"/content-*.json 2>/dev/null || true)

if [ ${#FIXTURES[@]} -eq 0 ]; then
  echo "No content-*.json fixtures found at $FIXTURES_DIR"
  exit 1
fi

echo "Found ${#FIXTURES[@]} fixtures:"
for f in "${FIXTURES[@]}"; do
  base=$(basename "$f" .json)
  echo "  - $base"
done
echo ""

GENERATED=0
for f in "${FIXTURES[@]}"; do
  base=$(basename "$f" .json)
  output="$BASELINES_DIR/${base}.pptx"
  echo "Rendering $base..."
  node "$RENDER_SCRIPT" \
    --file "$f" \
    --skip-confirm \
    --output "$output" \
    2>/dev/null && echo "  ✓ $output" || echo "  ✗ FAILED: $base"
  GENERATED=$((GENERATED + 1))
done

echo ""
echo "=== Generated $GENERATED PPTX files ==="
echo ""

if [ "${1:-}" = "--convert" ]; then
  if ! command -v soffice &>/dev/null; then
    echo "ERROR: libreoffice (soffice) not found on PATH."
    echo "Install it first, then re-run with --convert"
    echo ""
    echo "  # Ubuntu/Debian:"
    echo "  sudo apt install libreoffice"
    echo ""
    echo "  # macOS:"
    echo "  brew install --cask libreoffice"
    exit 1
  fi

  echo "Converting PPTX → PNG (requires libreoffice)..."
  for pptx in "$BASELINES_DIR"/*.pptx; do
    base=$(basename "$pptx" .pptx)
    echo "  Converting $base..."
    soffice --headless --convert-to png --outdir "$BASELINES_DIR" "$pptx" 2>/dev/null
  done
  echo "Done."
fi

echo ""
echo "Next steps:"
echo "  1. Review .pptx files in $BASELINES_DIR"
echo "  2. If visual changes are expected, update baselines"
echo "  3. See docs/ for regression testing documentation"
