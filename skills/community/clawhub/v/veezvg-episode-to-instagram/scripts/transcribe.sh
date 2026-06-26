#!/bin/bash
# transcribe.sh — Extract audio from video and transcribe via OpenAI Whisper API
# Usage: ./transcribe.sh <video_file> <output_dir>
# Requires: ffmpeg, curl, OPENAI_API_KEY env var

set -euo pipefail

VIDEO_FILE="${1:?Usage: transcribe.sh <video_file> <output_dir>}"
OUTPUT_DIR="${2:?Usage: transcribe.sh <video_file> <output_dir>}"

mkdir -p "$OUTPUT_DIR"

AUDIO_FILE="$OUTPUT_DIR/audio.mp3"
TRANSCRIPT_JSON="$OUTPUT_DIR/transcript.json"
TRANSCRIPT_TXT="$OUTPUT_DIR/transcript.txt"
CHUNKS_DIR="$OUTPUT_DIR/chunks"

echo "==> Extracting audio from video..."
ffmpeg -y -i "$VIDEO_FILE" -vn -acodec libmp3lame -ar 16000 -ac 1 -b:a 64k "$AUDIO_FILE" 2>/dev/null

FILESIZE=$(stat -f%z "$AUDIO_FILE" 2>/dev/null || stat --printf="%s" "$AUDIO_FILE" 2>/dev/null)
MAX_SIZE=$((24 * 1024 * 1024))  # 24MB to stay under 25MB API limit

if [ "$FILESIZE" -gt "$MAX_SIZE" ]; then
    echo "==> Audio file is ${FILESIZE} bytes, splitting into chunks..."
    mkdir -p "$CHUNKS_DIR"
    
    # Get duration in seconds
    DURATION=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$AUDIO_FILE" | cut -d. -f1)
    
    # Calculate chunk duration (~20MB per chunk at 64kbps = ~2500 seconds)
    CHUNK_DURATION=2400
    NUM_CHUNKS=$(( (DURATION + CHUNK_DURATION - 1) / CHUNK_DURATION ))
    
    echo "==> Splitting into $NUM_CHUNKS chunks of ${CHUNK_DURATION}s each..."
    
    ALL_SEGMENTS="[]"
    OFFSET=0
    
    for i in $(seq 0 $((NUM_CHUNKS - 1))); do
        START=$((i * CHUNK_DURATION))
        CHUNK_FILE="$CHUNKS_DIR/chunk_${i}.mp3"
        
        echo "==> Processing chunk $((i + 1))/$NUM_CHUNKS (start: ${START}s)..."
        ffmpeg -y -i "$AUDIO_FILE" -ss "$START" -t "$CHUNK_DURATION" -acodec libmp3lame -ar 16000 -ac 1 -b:a 64k "$CHUNK_FILE" 2>/dev/null
        
        # Transcribe chunk
        RESPONSE=$(curl -s https://api.openai.com/v1/audio/transcriptions \
            -H "Authorization: Bearer $OPENAI_API_KEY" \
            -F file="@$CHUNK_FILE" \
            -F model="whisper-1" \
            -F response_format="verbose_json" \
            -F timestamp_granularities[]="segment")
        
        # Adjust timestamps by adding the chunk start offset
        ADJUSTED=$(echo "$RESPONSE" | python3 -c "
import json, sys
data = json.load(sys.stdin)
segments = data.get('segments', [])
offset = $START
for seg in segments:
    seg['start'] = round(seg.get('start', 0) + offset, 2)
    seg['end'] = round(seg.get('end', 0) + offset, 2)
json.dump(segments, sys.stdout)
")
        
        # Merge segments
        ALL_SEGMENTS=$(echo "$ALL_SEGMENTS" | python3 -c "
import json, sys
existing = json.load(sys.stdin)
new = json.loads('$ADJUSTED')
existing.extend(new)
json.dump(existing, sys.stdout)
")
    done
    
    # Build final transcript JSON
    python3 -c "
import json
segments = json.loads('$(echo "$ALL_SEGMENTS" | sed "s/'/\\\\'/g")')
full_text = ' '.join(seg.get('text', '').strip() for seg in segments)
result = {
    'text': full_text,
    'segments': segments,
    'source': '$VIDEO_FILE',
    'chunk_count': $NUM_CHUNKS
}
with open('$TRANSCRIPT_JSON', 'w') as f:
    json.dump(result, f, indent=2)
with open('$TRANSCRIPT_TXT', 'w') as f:
    f.write(full_text)
print(f'Transcription complete: {len(segments)} segments, {len(full_text)} chars')
"

else
    echo "==> Audio file is ${FILESIZE} bytes, transcribing in one shot..."
    
    RESPONSE=$(curl -s https://api.openai.com/v1/audio/transcriptions \
        -H "Authorization: Bearer $OPENAI_API_KEY" \
        -F file="@$AUDIO_FILE" \
        -F model="whisper-1" \
        -F response_format="verbose_json" \
        -F timestamp_granularities[]="segment")
    
    python3 -c "
import json
response = json.loads('''$(echo "$RESPONSE" | python3 -c "import sys; print(sys.stdin.read().replace(\"'''\", \"\\\\'''\"))")''')
result = {
    'text': response.get('text', ''),
    'segments': response.get('segments', []),
    'source': '$VIDEO_FILE',
    'chunk_count': 1
}
with open('$TRANSCRIPT_JSON', 'w') as f:
    json.dump(result, f, indent=2)
with open('$TRANSCRIPT_TXT', 'w') as f:
    f.write(response.get('text', ''))
segments = response.get('segments', [])
print(f'Transcription complete: {len(segments)} segments, {len(response.get(\"text\", \"\"))} chars')
"
fi

echo "==> Transcript saved to:"
echo "    JSON: $TRANSCRIPT_JSON"
echo "    Text: $TRANSCRIPT_TXT"
