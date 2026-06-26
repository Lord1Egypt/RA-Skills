#!/bin/bash
# Video STT - Extract audio from video and transcribe

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
AUDIO_DIR="$SCRIPT_DIR/audio"
OUTPUT_DIR="$SCRIPT_DIR/output"

# Create directories
mkdir -p "$AUDIO_DIR" "$OUTPUT_DIR"

# Default values
VIDEO_URL=""
OUTPUT_FILE=""
MODEL="base"
FORMAT="txt"
USE_LOCAL=true

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -o|--output)
            OUTPUT_FILE="$2"
            shift 2
            ;;
        -m|--model)
            MODEL="$2"
            shift 2
            ;;
        -f|--format)
            FORMAT="$2"
            shift 2
            ;;
        --api)
            USE_LOCAL=false
            shift
            ;;
        --local)
            USE_LOCAL=true
            shift
            ;;
        -h|--help)
            echo "Usage: $0 [OPTIONS] VIDEO_URL"
            echo ""
            echo "Options:"
            echo "  -o, --output FILE    Output file (default: auto-generated)"
            echo "  -m, --model MODEL    Whisper model: tiny, base, small, medium, large"
            echo "  -f, --format FORMAT  Output format: txt, srt, vtt, json"
            echo "  --local              Use local Whisper (default)"
            echo "  --api                Use cloud API"
            echo "  -h, --help           Show this help"
            exit 0
            ;;
        *)
            VIDEO_URL="$1"
            shift
            ;;
    esac
done

if [ -z "$VIDEO_URL" ]; then
    echo "Error: Video URL required"
    echo "Usage: $0 VIDEO_URL"
    exit 1
fi

echo -e "${GREEN}Video STT - Starting...${NC}"
echo "Video URL: $VIDEO_URL"

# Step 1: Download audio
echo -e "${YELLOW}[1/3] Downloading audio...${NC}"

# Generate unique filename
TIMESTAMP=$(date +%s)
AUDIO_FILE="$AUDIO_DIR/audio_$TIMESTAMP.wav"

yt-dlp -f "bestaudio" -o "$AUDIO_FILE.%(ext)s" --extract-audio --audio-format wav "$VIDEO_URL" -q

# Find the downloaded file
AUDIO_FILE=$(ls -t "$AUDIO_DIR" | head -1)
AUDIO_PATH="$AUDIO_DIR/$AUDIO_FILE"

echo "Audio saved to: $AUDIO_PATH"

# Step 2: Transcribe
echo -e "${YELLOW}[2/3] Transcribing with Whisper ($MODEL)...${NC}"

# Set output filename
if [ -z "$OUTPUT_FILE" ]; then
    OUTPUT_FILE="$OUTPUT_DIR/transcript_$TIMESTAMP.$FORMAT"
fi

# Run transcription based on mode
if [ "$USE_LOCAL" = true ]; then
    # Check if uv environment exists
    if [ ! -d "$SCRIPT_DIR/.venv" ]; then
        echo "Creating Python environment with uv..."
        cd "$SCRIPT_DIR"
        uv venv
        uv pip install whisper
    fi
    
    source "$SCRIPT_DIR/.venv/bin/activate"
    
    # Run transcription
    python3 -c "
import whisper
import json

model = whisper.load_model('$MODEL')
result = model.transcribe('$AUDIO_PATH')

text = result['text']

# Save based on format
if '$FORMAT' == 'json':
    with open('$OUTPUT_FILE', 'w') as f:
        json.dump(result, f, indent=2)
elif '$FORMAT' == 'srt':
    # Generate SRT
    with open('$OUTPUT_FILE', 'w') as f:
        for i, segment in enumerate(result['segments'], 1):
            start = segment['start']
            end = segment['end']
            content = segment['text']
            f.write(f'$i\\n')
            f.write(f'{int(start//3600):02d}:{int((start%3600)//60):02d},{int((start%1)*1000):03d} --> ')
            f.write(f'{int(end//3600):02d}:{int((end%3600)//60):02d},{int((end%1)*1000):03d}\\n')
            f.write(f'{content}\\n\\n')
else:
    with open('$OUTPUT_FILE', 'w') as f:
        f.write(text)

print(f'Transcription saved to: $OUTPUT_FILE')
print(f'Text: {text[:200]}...')
"
else
    echo "Cloud API mode not implemented yet"
    exit 1
fi

# Step 3: Done
echo -e "${GREEN}[3/3] Done!${NC}"
echo "Output: $OUTPUT_FILE"

# Show content
echo -e "${YELLOW}Transcript:${NC}"
cat "$OUTPUT_FILE"
