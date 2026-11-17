#!/usr/bin/env bash
# ============================================================
# speechfy-tts — SSML Pitch, Rate & Emphasis Examples
# ============================================================
# Run: bash examples/ssml-pitch-rate.sh
# ============================================================
set -euo pipefail

SCRIPT="scripts/speechfy-tts.py"
SCRIPT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
OUTDIR="/tmp/speechfy-examples"
mkdir -p "$OUTDIR"

echo "=== 1. Pitch +5% (slightly higher) ==="
python3 "$SCRIPT_DIR/$SCRIPT" \
  '<speak><prosody pitch="+5%">This message has a slightly more animated tone.</prosody></speak>' \
  "$OUTDIR/pitch-plus5.ogg"

echo ""
echo "=== 2. Pitch -10% (deeper) ==="
python3 "$SCRIPT_DIR/$SCRIPT" \
  '<speak><prosody pitch="-10%">Now I am speaking in a more serious, deeper voice.</prosody></speak>' \
  "$OUTDIR/pitch-minus10.ogg"

echo ""
echo "=== 3. Rate slow (slow) ==="
python3 "$SCRIPT_DIR/$SCRIPT" \
  '<speak><prosody rate="slow">Pay attention. This is very important. I will speak slowly.</prosody></speak>' \
  "$OUTDIR/rate-slow.ogg"

echo ""
echo "=== 4. Rate fast (fast) ==="
python3 "$SCRIPT_DIR/$SCRIPT" \
  '<speak><prosody rate="fast">Running against time, lets get straight to the point.</prosody></speak>' \
  "$OUTDIR/rate-fast.ogg"

echo ""
echo "=== 5. Combined: high pitch + fast ==="
python3 "$SCRIPT_DIR/$SCRIPT" \
  '<speak><prosody pitch="high" rate="fast">Wow! This is amazing! I can hardly believe it!</prosody></speak>' \
  "$OUTDIR/pitch-high-rate-fast.ogg"

echo ""
echo "=== 6. Combined: low pitch + slow ==="
python3 "$SCRIPT_DIR/$SCRIPT" \
  '<speak><prosody pitch="low" rate="x-slow">The situation... is serious... we need... to think...</prosody></speak>' \
  "$OUTDIR/pitch-low-rate-slow.ogg"

echo ""
echo "=== 7. Word emphasis ==="
python3 "$SCRIPT_DIR/$SCRIPT" \
  '<speak>I <emphasis level="strong">already</emphasis> told you this is <emphasis level="strong">very</emphasis> dangerous.</speak>' \
  "$OUTDIR/emphasis.ogg"

echo ""
echo "=== 8. Strategic pauses ==="
python3 "$SCRIPT_DIR/$SCRIPT" \
  '<speak>First, <break time="500ms"/> lets organize. <break time="300ms"/> Then, <break time="200ms"/> execute.</speak>' \
  "$OUTDIR/pauses.ogg"

echo ""
echo "=== 9. Complete irony recipe ==="
python3 "$SCRIPT_DIR/$SCRIPT" \
  '<speak><speechify:style emotion="bright">Oh, of course, it worked perfectly.</speechify:style><break time="200ms"/> <emphasis level="strong">Of course</emphasis> it did...</speak>' \
  "$OUTDIR/irony-recipe.ogg"

echo ""
echo "=== 10. Everything combined ==="
python3 "$SCRIPT_DIR/$SCRIPT" \
  '<speak><speechify:style emotion="cheerful">Great question!</speechify:style><break time="300ms"/> <prosody rate="slow" pitch="-5%">Let me explain calmly.</prosody> <break time="200ms"/> The <emphasis level="strong">main</emphasis> point is <prosody pitch="+10%">this one here</prosody>.</speak>' \
  "$OUTDIR/everything-combined.ogg"

echo ""
echo "=== Generated files ==="
ls -lh "$OUTDIR/"*.ogg 2>/dev/null

echo ""
echo "✅ SSML pitch/rate/emphasis examples complete."
