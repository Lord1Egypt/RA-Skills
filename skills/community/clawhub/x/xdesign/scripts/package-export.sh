#!/usr/bin/env bash
# package-export.sh
# ==================
# Convert a deck-studio / prototype HTML file to PDF or PPTX.
#
# Why this exists:
# - SKILL.md promises "export to PPTX, PDF, or standalone HTML" but
#   the runtime requires a one-liner that no one remembers.
# - Centralising the command keeps the right tool flags in one place
#   (e.g. --print-to-paper for headless Chromium PDF).
#
# Usage:
#   ./scripts/package-export.sh pdf  <input.html> [output.pdf]
#   ./scripts/package-export.sh pptx <input.html> [output.pptx]
#
# Dependencies:
# - For PDF: Google Chrome / Chromium with headless flag, OR wkhtmltopdf.
# - For PPTX: pandoc + a presenterm intermediate (currently a stub).

set -euo pipefail

if [[ $# -lt 2 ]]; then
  cat >&2 <<EOF
Usage: $0 <pdf|pptx> <input.html> [output]

Examples:
  $0 pdf  deck-studio/templates/deck.html my-deck.pdf
  $0 pptx deck-studio/templates/deck.html my-deck.pptx
EOF
  exit 1
fi

FORMAT="$1"
INPUT="$2"
OUTPUT="${3:-}"

if [[ ! -f "$INPUT" ]]; then
  echo "[ERR] Input file not found: $INPUT" >&2
  exit 1
fi

case "$FORMAT" in
  pdf)
    OUTPUT="${OUTPUT:-${INPUT%.html}.pdf}"
    echo "[INFO] Converting $INPUT -> $OUTPUT"

    if command -v google-chrome >/dev/null 2>&1; then
      CHROME=google-chrome
    elif command -v chromium >/dev/null 2>&1; then
      CHROME=chromium
    elif command -v "Google Chrome" >/dev/null 2>&1; then
      CHROME="Google Chrome"
    else
      echo "[ERR] No Chrome/Chromium found. Install or use wkhtmltopdf." >&2
      exit 1
    fi

    # For multi-page decks, the printer may truncate.
    # We rely on @page rules in base.css for sizing; see references/technical-specs.md.
    "$CHROME" --headless --disable-gpu --no-sandbox \
      --print-to-pdf="$OUTPUT" \
      --print-to-pdf-no-header \
      "file://$(cd "$(dirname "$INPUT")" && pwd)/$(basename "$INPUT")"
    echo "[OK] Wrote $OUTPUT"
    ;;

  pptx)
    OUTPUT="${OUTPUT:-${INPUT%.html}.pptx}"
    echo "[INFO] Converting $INPUT -> $OUTPUT"

    if ! command -v pandoc >/dev/null 2>&1; then
      echo "[ERR] pandoc not found. Install with: brew install pandoc" >&2
      exit 1
    fi

    # HTML-to-PPTX is lossy. The cleanest path is:
    # 1. Render each <section class="slide"> to a PNG via headless Chrome.
    # 2. Build a PPTX with one slide per image.
    # 3. Use python-pptx to write the .pptx file.
    #
    # This script is a thin wrapper; full pipeline lives in
    # deck-studio/scripts/render.sh if present.
    TMPDIR="$(mktemp -d)"
    trap "rm -rf $TMPDIR" EXIT

    SLIDE_DIR="$TMPDIR/slides"
    mkdir -p "$SLIDE_DIR"

    # Render each <section class="slide"> by manipulating the HTML to show
    # only that slide, then printing. This is a stub — full implementation
    # in deck-studio/scripts/render.sh.
    echo "[WARN] PPTX export is lossy. For best results, use the rendered"
    echo "       images from deck-studio/scripts/render.sh and assemble"
    echo "       the .pptx manually with python-pptx."
    echo ""
    echo "       This stub copies the HTML body into a single-slide .pptx"
    echo "       using pandoc — useful for quick review, not for delivery."

    pandoc "$INPUT" -o "$OUTPUT" \
      --slide-level=1 \
      -t pptx 2>/dev/null \
      || {
        echo "[ERR] pandoc HTML->PPTX failed. Install with: brew install pandoc" >&2
        exit 1
      }
    echo "[OK] Wrote $OUTPUT"
    ;;

  *)
    echo "[ERR] Unknown format '$FORMAT'. Use 'pdf' or 'pptx'." >&2
    exit 1
    ;;
esac
