#!/bin/bash
#
# Background removal wrapper script - auto-detects best method
# Usage: ./remove_bg.sh input.jpg output.png [tolerance] [color]
#

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INPUT="$1"
OUTPUT="$2"
TOLERANCE="${3:-20}"
COLOR="${4:-#FFFFFF}"

# Check inputs
if [ -z "$INPUT" ] || [ -z "$OUTPUT" ]; then
    echo "Usage: $0 input.jpg output.png [tolerance] [color]"
    echo "  tolerance: color matching fuzz (0-100, default 20)"
    echo "  color: hex color to remove (default: #FFFFFF)"
    exit 1
fi

if [ ! -f "$INPUT" ]; then
    echo "Error: Input file not found: $INPUT"
    exit 1
fi

# Create output directory if needed
OUT_DIR="$(dirname "$OUTPUT")"
if [ -n "$OUT_DIR" ] && [ ! -d "$OUT_DIR" ]; then
    mkdir -p "$OUT_DIR"
fi

# Method 1: Try rembg first if available (check system and venv)
REMBG_CMD=""
if command -v rembg >/dev/null 2>&1; then
    REMBG_CMD="rembg"
elif [ -f "/home/guoxh/.openclaw/venv-clawd/bin/rembg" ]; then
    REMBG_CMD="/home/guoxh/.openclaw/venv-clawd/bin/rembg"
fi

if [ -n "$REMBG_CMD" ]; then
    echo "🔍 Using AI background removal (rembg)..."
    $REMBG_CMD i "$INPUT" "$OUTPUT"
    echo "✓ Background removed with rembg: $OUTPUT"
    exit 0
fi

# Method 2: Fall back to ImageMagick (solid color backgrounds)
# NOTE: ImageMagick "convert" command may be "magick" on ImageMagick 7+
IM_CONVERT=""
if command -v magick >/dev/null 2>&1; then
    IM_CONVERT="magick"
elif command -v convert >/dev/null 2>&1; then
    IM_CONVERT="convert"
fi

if [ -z "$IM_CONVERT" ]; then
    echo "Error: ImageMagick (convert/magick) not found. Install with:"
    echo "  sudo apt install imagemagick   # Debian/Ubuntu"
    echo "  brew install imagemagick       # macOS"
    exit 1
fi

echo "⚠️  rembg not found, falling back to ImageMagick (solid color only)..."
echo "   Removing color: $COLOR with tolerance: ${TOLERANCE}%"

# Parse hex color to RGB
COLOR_TRIMMED=$(echo "$COLOR" | tr -d '#')
R=$((16#${COLOR_TRIMMED:0:2}))
G=$((16#${COLOR_TRIMMED:2:2}))
B=$((16#${COLOR_TRIMMED:4:2}))

# Determine output format from extension
case "${OUTPUT##*.}" in
    png|PNG)
        # For PNG: make specified color transparent with alpha
        $IM_CONVERT "$INPUT" -fuzz ${TOLERANCE}% \
            -fill "rgba(0,0,0,0)" \
            -draw "matte ${R},${G},${B} floodfill" \
            -alpha extract \
            "$OUTPUT"
        ;;
    *)
        # For other formats: use standard transparency
        $IM_CONVERT "$INPUT" -fuzz ${TOLERANCE}% -transparent "rgb($R,$G,$B)" "$OUTPUT"
        ;;
esac

echo "✓ Background removed with ImageMagick: $OUTPUT"

echo ""
echo "💡 Tip: Install rembg for better AI-powered background removal:"
echo "   source ~/.openclaw/venv-clawd/bin/activate && pip install rembg"
