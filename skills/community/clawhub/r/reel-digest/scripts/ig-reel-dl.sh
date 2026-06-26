#!/bin/bash
# ig-reel-dl.sh — Download Instagram reel
set -e

URL="$1"
OUTDIR="${2:-/tmp/reel-dl}"
mkdir -p "$OUTDIR/frames"

# Step 1: Fetch embed and extract video URL
VIDEO_URL=$(curl -sL -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36' \
    "${URL%/}/embed/" 2>/dev/null | \
    tr -d '\\' | \
    grep -oP 'scontent[^"'\''<>\s]+\.mp4[^"'\''<>\s]+' | \
    head -1)

if [ -z "$VIDEO_URL" ]; then
    echo "ERROR: Could not extract video URL"
    exit 1
fi

VIDEO_URL="https://${VIDEO_URL}"
echo "Video URL found (${#VIDEO_URL} chars)"

# Step 2: Download video immediately
curl -sL -o "$OUTDIR/video.mp4" \
    -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36' \
    -H 'Referer: https://www.instagram.com/' \
    "$VIDEO_URL"

SIZE=$(stat -c%s "$OUTDIR/video.mp4" 2>/dev/null || echo 0)
echo "Downloaded: $SIZE bytes"

if [ "$SIZE" -lt 1000 ]; then
    echo "ERROR: Download too small"
    exit 1
fi

# Step 3: Extract frames (1 per 5 seconds)
ffmpeg -y -i "$OUTDIR/video.mp4" -vf 'fps=1/5,scale=640:-1' -q:v 2 "$OUTDIR/frames/frame_%02d.jpg" 2>/dev/null || true
FRAMES=$(ls "$OUTDIR/frames/"*.jpg 2>/dev/null | wc -l)
echo "Frames: $FRAMES"

# Step 4: Extract audio
ffmpeg -y -i "$OUTDIR/video.mp4" -vn -acodec pcm_s16le -ar 16000 -ac 1 "$OUTDIR/audio.wav" 2>/dev/null || true
if [ -f "$OUTDIR/audio.wav" ]; then
    ASIZE=$(stat -c%s "$OUTDIR/audio.wav" 2>/dev/null || echo 0)
    echo "Audio: $ASIZE bytes"
fi

# Step 5: Get duration
DURATION=$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$OUTDIR/video.mp4" 2>/dev/null || echo 0)
echo "Duration: ${DURATION}s"

# Step 6: Transcribe (optional)
if [ -f "$OUTDIR/audio.wav" ] && [ "$ASIZE" -gt 1000 ]; then
    echo "Transcribing..."
    python3 -c "
from faster_whisper import WhisperModel
import sys
model = WhisperModel('base', device='cpu', compute_type='int8')
segments, _ = model.transcribe('${OUTDIR}/audio.wav')
with open('${OUTDIR}/transcript.txt', 'w') as f:
    for s in segments:
        line = '[%.1fs-%.1fs] %s' % (s.start, s.end, s.text)
        f.write(line + chr(10))
        print(line)
" 2>/dev/null && echo "Transcription done" || echo "Transcription failed"
fi

echo ""
echo "=== DONE ==="
echo "Output: $OUTDIR"
ls -la "$OUTDIR/"
if [ -d "$OUTDIR/frames" ]; then
    echo "Frames: $(ls "$OUTDIR/frames/" | wc -l) files"
fi
