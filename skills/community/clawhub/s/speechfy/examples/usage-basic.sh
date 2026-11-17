#!/usr/bin/env bash
# ============================================================
# speechfy-tts — Basic Usage Examples
# ============================================================
# Run: bash examples/usage-basic.sh
# ============================================================
set -euo pipefail

SCRIPT="scripts/speechfy-tts.py"
SCRIPT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
OUTDIR="/tmp/speechfy-examples"
mkdir -p "$OUTDIR"

echo "=== 1. Simple text (default output) ==="
python3 "$SCRIPT_DIR/$SCRIPT" "Hello, how are you? Testing the voice."

echo ""
echo "=== 2. Custom output path ==="
python3 "$SCRIPT_DIR/$SCRIPT" \
  "Second test with custom path." \
  "$OUTDIR/test-custom.ogg"

echo ""
echo "=== 3. Long message ==="
python3 "$SCRIPT_DIR/$SCRIPT" \
  "Attention! This is an important reminder. Please check deadlines and make sure everything is in order. Thank you for your attention!" \
  "$OUTDIR/long-message.ogg"

echo ""
echo "=== 4. Force Edge TTS fallback ==="
SPEECHIFY_API_KEY="" python3 "$SCRIPT_DIR/$SCRIPT" \
  "This audio was generated with Edge TTS, the fallback voice." \
  "$OUTDIR/fallback.ogg"

echo ""
echo "=== 5. Alternative voice (Adriana) ==="
SPEECHIFY_VOICE="adriana" python3 "$SCRIPT_DIR/$SCRIPT" \
  "This is Adriana speaking, an alternative voice." \
  "$OUTDIR/adriana.ogg"

echo ""
echo "=== Generated files ==="
ls -lh "$OUTDIR/"*.ogg 2>/dev/null || echo "(no files found)"

echo ""
echo "✅ Examples complete."
