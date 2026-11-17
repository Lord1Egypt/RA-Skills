#!/usr/bin/env bash
# ============================================================
# speechfy-tts — SSML Emotion Examples
# ============================================================
# Run: bash examples/ssml-emotions.sh
# ============================================================
set -euo pipefail

SCRIPT="scripts/speechfy-tts.py"
SCRIPT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
OUTDIR="/tmp/speechfy-examples"
mkdir -p "$OUTDIR"

echo "=== 1. Cheerful (excited) ==="
python3 "$SCRIPT_DIR/$SCRIPT" \
  '<speak><speechify:style emotion="cheerful">Great news! We received good news today!</speechify:style></speak>' \
  "$OUTDIR/cheerful.ogg"

echo ""
echo "=== 2. Calm (serene) ==="
python3 "$SCRIPT_DIR/$SCRIPT" \
  '<speak><speechify:style emotion="calm">Let us analyze the data step by step. There is no rush.</speechify:style></speak>' \
  "$OUTDIR/calm.ogg"

echo ""
echo "=== 3. Bright (ironic) ==="
python3 "$SCRIPT_DIR/$SCRIPT" \
  '<speak><speechify:style emotion="bright">Of course it worked. As always, right?</speechify:style></speak>' \
  "$OUTDIR/bright.ogg"

echo ""
echo "=== 4. Warm (welcoming) ==="
python3 "$SCRIPT_DIR/$SCRIPT" \
  '<speak><speechify:style emotion="warm">Hi! Great to talk to you. How can I help today?</speechify:style></speak>' \
  "$OUTDIR/warm.ogg"

echo ""
echo "=== 5. Assertive (firm) ==="
python3 "$SCRIPT_DIR/$SCRIPT" \
  '<speak><speechify:style emotion="assertive">This cannot continue. We need to act now.</speechify:style></speak>' \
  "$OUTDIR/assertive.ogg"

echo ""
echo "=== 6. Sad (melancholic) ==="
python3 "$SCRIPT_DIR/$SCRIPT" \
  '<speak><speechify:style emotion="sad">Its a shame things ended this way.</speechify:style></speak>' \
  "$OUTDIR/sad.ogg"

echo ""
echo "=== 7. Surprised (astonished) ==="
python3 "$SCRIPT_DIR/$SCRIPT" \
  '<speak><speechify:style emotion="surprised">Wow! I was not expecting that!</speechify:style></speak>' \
  "$OUTDIR/surprised.ogg"

echo ""
echo "=== 8. Energetic (lively) ==="
python3 "$SCRIPT_DIR/$SCRIPT" \
  '<speak><speechify:style emotion="energetic">Lets go! Today is the day to conquer everything!</speechify:style></speak>' \
  "$OUTDIR/energetic.ogg"

echo ""
echo "=== 9. Direct (no-nonsense) ==="
python3 "$SCRIPT_DIR/$SCRIPT" \
  '<speak><speechify:style emotion="direct">The meeting is at 3 PM. Do not be late.</speechify:style></speak>' \
  "$OUTDIR/direct.ogg"

echo ""
echo "=== 10. Mixed (combined emotions) ==="
python3 "$SCRIPT_DIR/$SCRIPT" \
  '<speak><speechify:style emotion="cheerful">Good news!</speechify:style><break time="300ms"/> But <speechify:style emotion="calm">we need to analyze carefully.</speechify:style></speak>' \
  "$OUTDIR/mixed.ogg"

echo ""
echo "=== Generated files ==="
ls -lh "$OUTDIR/"*.ogg 2>/dev/null

echo ""
echo "✅ SSML emotion examples complete."
