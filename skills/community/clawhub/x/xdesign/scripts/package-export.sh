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
#   ./scripts/package-export.sh social wechat <input.html> [output.html]
#   ./scripts/package-export.sh social xhs    <input.html> [output.png]
#   ./scripts/package-export.sh social x      <input.html> [output.png]
#
# Dependencies:
# - For PDF: Google Chrome / Chromium with headless flag, OR wkhtmltopdf.
# - For PPTX: pandoc + a presenterm intermediate (currently a stub).
# - For social wechat: `juice` (npm i -g juice) — inlines CSS for WeChat paste.
# - For social xhs / x: `playwright` (npm i -D playwright && npx playwright install chromium)
#   — renders 2× PNG for Xiaohongshu / X / tweet cards.

set -euo pipefail

if [[ $# -lt 2 ]]; then
  cat >&2 <<EOF
Usage:
  $0 <pdf|pptx> <input.html> [output]
  $0 social <wechat|xhs|x> <input.html> [output]

Examples:
  $0 pdf  deck-studio/templates/deck.html my-deck.pdf
  $0 pptx deck-studio/templates/deck.html my-deck.pptx
  $0 social wechat deck.html wechat-deck.html
  $0 social xhs    deck.html xhs-deck.png
  $0 social x      deck.html x-deck.png
EOF
  exit 1
fi

FORMAT="$1"
INPUT=""
OUTPUT=""
SUBCMD=""

if [[ "$FORMAT" == "social" ]]; then
  if [[ $# -lt 3 ]]; then
    echo "[ERR] 'social' requires a subcommand: wechat | xhs | x" >&2
    exit 1
  fi
  SUBCMD="$2"
  INPUT="$3"
  OUTPUT="${4:-}"
else
  INPUT="$2"
  OUTPUT="${3:-}"
fi

if [[ ! -f "$INPUT" ]]; then
  echo "[ERR] Input file not found: $INPUT" >&2
  exit 1
fi

case "$FORMAT" in
  social)
    case "$SUBCMD" in
      wechat)
        OUTPUT="${OUTPUT:-${INPUT%.html}-wechat.html}"
        echo "[INFO] Juice-inlining CSS for WeChat: $INPUT -> $OUTPUT"
        if command -v juice >/dev/null 2>&1; then
          juice "$INPUT" "$OUTPUT"
          echo "[OK] Wrote $OUTPUT — paste directly into WeChat editor"
        else
          echo "[WARN] 'juice' not found. Install with: npm i -g juice"
          echo "       Falling back to raw HTML copy (styles may not paste cleanly)."
          cp "$INPUT" "$OUTPUT"
        fi
        ;;

      xhs)
        OUTPUT="${OUTPUT:-${INPUT%.html}-xhs.png}"
        echo "[INFO] Rendering 2× PNG for Xiaohongshu: $INPUT -> $OUTPUT"
        if command -v npx >/dev/null 2>&1 && npx playwright --version >/dev/null 2>&1; then
          python3 - "$INPUT" "$OUTPUT" <<'PYEOF'
import sys, asyncio
from playwright.async_api import async_playwright

async def main():
    input_html, output_png = sys.argv[1], sys.argv[2]
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 1200, "height": 800})
        await page.goto(f"file://{input_html}")
        await page.wait_for_timeout(500)
        # 2× for retina
        await page.screenshot(path=output_png, scale="device", type="png")
        await browser.close()

asyncio.run(main())
PYEOF
          echo "[OK] Wrote $OUTPUT (2× retina, paste into Xiaohongshu)"
        else
          echo "[ERR] Playwright not found. Install with:" >&2
          echo "       npm i -D playwright && npx playwright install chromium" >&2
          exit 1
        fi
        ;;

      x)
        OUTPUT="${OUTPUT:-${INPUT%.html}-x.png}"
        echo "[INFO] Rendering 2× PNG for X/Twitter: $INPUT -> $OUTPUT"
        if command -v npx >/dev/null 2>&1 && npx playwright --version >/dev/null 2>&1; then
          python3 - "$INPUT" "$OUTPUT" <<'PYEOF'
import sys, asyncio
from playwright.async_api import async_playwright

async def main():
    input_html, output_png = sys.argv[1], sys.argv[2]
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 1600, "height": 900})
        await page.goto(f"file://{input_html}")
        await page.wait_for_timeout(500)
        await page.screenshot(path=output_png, scale="device", type="png")
        await browser.close()

asyncio.run(main())
PYEOF
          echo "[OK] Wrote $OUTPUT (2× retina, paste into X/Twitter)"
        else
          echo "[ERR] Playwright not found. Install with:" >&2
          echo "       npm i -D playwright && npx playwright install chromium" >&2
          exit 1
        fi
        ;;

      *)
        echo "[ERR] Unknown social subcommand '$SUBCMD'. Use wechat | xhs | x." >&2
        exit 1
        ;;
    esac
    ;;

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
