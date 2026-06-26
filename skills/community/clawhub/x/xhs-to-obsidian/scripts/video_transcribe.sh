#!/bin/bash
# Download and transcribe video from Xiaohongshu post
# Usage: bash video_transcribe.sh <video_url> <post_id> <output_dir>

VIDEO_URL="$1"
POST_ID="$2"
OUTPUT_DIR="$3"

TMP_DIR="/tmp/xhs"
mkdir -p "$TMP_DIR"

VIDEO_PATH="$TMP_DIR/${POST_ID}.mp4"
WAV_PATH="$TMP_DIR/${POST_ID}.wav"
TRANSCRIPT_PATH="$TMP_DIR/${POST_ID}.txt"

echo "Downloading video..."
curl -L -o "$VIDEO_PATH" \
  -H "Referer: https://www.xiaohongshu.com/" \
  -H "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36" \
  "$VIDEO_URL"

if [ $? -ne 0 ]; then
    echo "ERROR: Download failed"
    exit 1
fi

echo "Extracting audio..."
ffmpeg -y -i "$VIDEO_PATH" -vn -acodec pcm_s16le -ar 16000 -ac 1 "$WAV_PATH" 2>/dev/null

if [ $? -ne 0 ]; then
    echo "ERROR: Audio extraction failed"
    exit 1
fi

echo "Transcribing with whisper..."
if python3 -c "import mlx_whisper" 2>/dev/null; then
    python3 -c "
import mlx_whisper
result = mlx_whisper.transcribe('$WAV_PATH', path_or_hf_repo='mlx-community/whisper-large-v3-turbo', language='zh', verbose=False)
with open('$TRANSCRIPT_PATH', 'w') as f:
    f.write(result['text'])
"
elif command -v whisper &>/dev/null; then
    whisper "$WAV_PATH" --model medium --language Chinese --output_file "$TMP_DIR/${POST_ID}" 2>/dev/null
    cp "$TMP_DIR/${POST_ID}.txt" "$TRANSCRIPT_PATH" 2>/dev/null
else
    echo "WARNING: No whisper installation found. Install with: pip install mlx-whisper"
    echo "Skipping transcription."
fi

# Cleanup
rm -f "$VIDEO_PATH" "$WAV_PATH"

if [ -f "$TRANSCRIPT_PATH" ]; then
    cat "$TRANSCRIPT_PATH"
else
    echo ""
fi
