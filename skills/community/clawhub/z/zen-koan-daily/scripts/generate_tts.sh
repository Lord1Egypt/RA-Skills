#!/bin/bash
# Generate TTS audio for Zen koan lecture
# Uses Edge TTS (free, no API key needed)

set -e

# Check edge-tts is installed
if ! command -v edge-tts &> /dev/null; then
    echo "Error: edge-tts not installed. Run: pipx install edge-tts" >&2
    exit 1
fi

# Parse arguments
TEXT=""
OUTPUT=""
LANG="zh"

while [[ $# -gt 0 ]]; do
    case $1 in
        --text)
            TEXT="$2"
            shift 2
            ;;
        --text-file)
            TEXT=$(cat "$2")
            shift 2
            ;;
        --output)
            OUTPUT="$2"
            shift 2
            ;;
        --lang)
            LANG="$2"
            shift 2
            ;;
        *)
            echo "Unknown option: $1" >&2
            exit 1
            ;;
    esac
done

# Validate
if [ -z "$TEXT" ]; then
    echo "Error: --text or --text-file required" >&2
    exit 1
fi

# Default output path
if [ -z "$OUTPUT" ]; then
    TIMESTAMP=$(date +%Y%m%d-%H%M%S)
    OUTPUT="$HOME/.openclaw/media/outbound/zen-koan/koan-${TIMESTAMP}.mp3"
fi

# Create output directory
mkdir -p "$(dirname "$OUTPUT")"

# Select voice based on language
if [ "$LANG" = "zh" ]; then
    VOICE="zh-CN-XiaoxiaoNeural"  # 晓晓：温暖、平静、适合讲解
elif [ "$LANG" = "en" ]; then
    VOICE="en-US-AriaNeural"      # Aria：平静、叙述风格
else
    echo "Error: Unsupported language: $LANG" >&2
    exit 1
fi

# Generate audio
echo "Generating TTS audio..." >&2
echo "Voice: $VOICE" >&2
echo "Output: $OUTPUT" >&2

edge-tts --voice "$VOICE" --text "$TEXT" --write-media "$OUTPUT"

echo "✅ TTS audio generated: $OUTPUT" >&2
echo "$OUTPUT"
