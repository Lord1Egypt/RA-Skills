#!/bin/bash
# Rex 小红书图片生成器
# Usage: ./render-rex.sh <content.md> [output-dir]

set -e

CONTENT="$1"
OUTDIR="${2:-/tmp/rex-xhs-images}"
AVATAR="/Users/mo/rex-content/rex-avatar-v5.png"

if [ -z "$CONTENT" ]; then
    echo "Usage: $0 <content.md> [output-dir]"
    exit 1
fi

mkdir -p "$OUTDIR"

cd /Users/mo/.openclaw/workspace/skills/xhs-image-gen
source venv/bin/activate

python scripts/render_xhs.py \
    "$CONTENT" \
    -t rex \
    -m auto-split \
    --width 1080 \
    --height 1440 \
    --dpr 2 \
    --avatar "$AVATAR" \
    --output-dir "$OUTDIR"

echo ""
echo "✅ Images saved to: $OUTDIR"
ls "$OUTDIR"