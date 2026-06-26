#!/bin/bash
# batch-export.sh — Export one edited reel to multiple platforms at once.
#
# Usage:
#   bash batch-export.sh input.mp4 [output_name] [platforms]
#
# Arguments:
#   input.mp4     — Your final edited reel (should be 1080x1920 already)
#   output_name   — Base name for output files (default: "reel")
#   platforms     — Comma-separated list (default: all)
#                   Options: instagram, tiktok, youtube, facebook, snapchat, pinterest, linkedin, square
#
# Examples:
#   bash batch-export.sh my_reel.mp4
#   bash batch-export.sh my_reel.mp4 cooking_video instagram,tiktok,youtube
#   bash batch-export.sh my_reel.mp4 product_launch all
#
# Output:
#   Creates output directory with platform-optimized versions + quality report

set -e

# ── Arguments ──────────────────────────────────────────────────────────────────
INPUT="${1}"
OUTPUT_NAME="${2:-reel}"
PLATFORMS="${3:-all}"
OUTPUT_DIR="/mnt/user-data/outputs/${OUTPUT_NAME}"

# ── Validate ───────────────────────────────────────────────────────────────────
if [ -z "$INPUT" ]; then
    echo "Usage: bash batch-export.sh input.mp4 [output_name] [platforms]"
    echo "Example: bash batch-export.sh reel_final.mp4 my_reel instagram,tiktok"
    exit 1
fi

if [ ! -f "$INPUT" ]; then
    echo "ERROR: Input file not found: $INPUT"
    exit 1
fi

command -v ffmpeg >/dev/null 2>&1 || { echo "ERROR: ffmpeg not found. Install with: apt-get install ffmpeg"; exit 1; }

mkdir -p "$OUTPUT_DIR"

# ── Colors / UI ────────────────────────────────────────────────────────────────
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

log_start() { echo -e "${BLUE}▶ Exporting: $1...${NC}"; }
log_done()  { echo -e "${GREEN}✓ Done: $1${NC}"; }
log_skip()  { echo -e "${YELLOW}⊘ Skipped: $1${NC}"; }
log_size()  { SIZE=$(du -sh "$1" | cut -f1); echo -e "  Size: ${SIZE}"; }

# ── Helper: should we export this platform? ────────────────────────────────────
should_export() {
    local platform="$1"
    if [ "$PLATFORMS" = "all" ]; then
        return 0
    fi
    if echo "$PLATFORMS" | grep -qw "$platform"; then
        return 0
    fi
    return 1
}

# ── Get video info ─────────────────────────────────────────────────────────────
echo ""
echo "════════════════════════════════════════════════════"
echo " BATCH EXPORT: $(basename $INPUT)"
echo "════════════════════════════════════════════════════"
DURATION=$(ffprobe -v quiet -show_entries format=duration -of csv=p=0 "$INPUT" 2>/dev/null)
DURATION_INT=$(echo "$DURATION" | cut -d. -f1)
echo -e " Duration: ${DURATION}s"
echo -e " Output dir: ${OUTPUT_DIR}"
echo -e " Platforms: ${PLATFORMS}"
echo "════════════════════════════════════════════════════"
echo ""

# ── Base encode flags (shared across platforms) ────────────────────────────────
BASE_VIDEO="-c:v libx264 -pix_fmt yuv420p -movflags +faststart"
BASE_AUDIO="-c:a aac -ar 44100 -ac 2"
SCALE_9x16="-vf scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920"

# ── Instagram Reels ────────────────────────────────────────────────────────────
if should_export "instagram"; then
    OUT="${OUTPUT_DIR}/${OUTPUT_NAME}_instagram.mp4"
    log_start "Instagram Reels (1080x1920, max 90s, CRF 18)"
    TRIM=""
    [ "$DURATION_INT" -gt 90 ] && TRIM="-t 90" && echo -e "  ${YELLOW}⚠ Trimming to 90s (Instagram limit)${NC}"
    ffmpeg -i "$INPUT" \
        $SCALE_9x16 \
        $BASE_VIDEO -preset slow -crf 18 -r 30 \
        $BASE_AUDIO -b:a 128k \
        $TRIM -y "$OUT" 2>/dev/null
    log_done "Instagram Reels → $(basename $OUT)"
    log_size "$OUT"
fi

# ── TikTok ────────────────────────────────────────────────────────────────────
if should_export "tiktok"; then
    OUT="${OUTPUT_DIR}/${OUTPUT_NAME}_tiktok.mp4"
    log_start "TikTok (1080x1920, max 60s, CRF 17)"
    TRIM=""
    [ "$DURATION_INT" -gt 60 ] && TRIM="-t 60" && echo -e "  ${YELLOW}⚠ Trimming to 60s (TikTok short limit)${NC}"
    ffmpeg -i "$INPUT" \
        $SCALE_9x16 \
        $BASE_VIDEO -preset slow -crf 17 -r 30 \
        $BASE_AUDIO -b:a 192k \
        $TRIM -y "$OUT" 2>/dev/null
    log_done "TikTok → $(basename $OUT)"
    log_size "$OUT"
fi

# ── YouTube Shorts ────────────────────────────────────────────────────────────
if should_export "youtube"; then
    OUT="${OUTPUT_DIR}/${OUTPUT_NAME}_youtube_shorts.mp4"
    log_start "YouTube Shorts (1080x1920, max 60s, 60fps, CRF 18)"
    TRIM=""
    [ "$DURATION_INT" -gt 60 ] && TRIM="-t 60" && echo -e "  ${YELLOW}⚠ Trimming to 60s (YouTube Shorts limit)${NC}"
    ffmpeg -i "$INPUT" \
        -vf "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=60" \
        $BASE_VIDEO -preset slow -crf 18 \
        $BASE_AUDIO -b:a 192k \
        $TRIM -y "$OUT" 2>/dev/null
    log_done "YouTube Shorts → $(basename $OUT)"
    log_size "$OUT"
fi

# ── Facebook Reels ────────────────────────────────────────────────────────────
if should_export "facebook"; then
    OUT="${OUTPUT_DIR}/${OUTPUT_NAME}_facebook.mp4"
    log_start "Facebook Reels (1080x1920, max 90s, CRF 16 — highest quality)"
    TRIM=""
    [ "$DURATION_INT" -gt 90 ] && TRIM="-t 90" && echo -e "  ${YELLOW}⚠ Trimming to 90s (Facebook limit)${NC}"
    ffmpeg -i "$INPUT" \
        $SCALE_9x16 \
        $BASE_VIDEO -preset slow -crf 16 -r 30 \
        $BASE_AUDIO -b:a 192k \
        $TRIM -y "$OUT" 2>/dev/null
    log_done "Facebook Reels → $(basename $OUT)"
    log_size "$OUT"
fi

# ── Snapchat Spotlight ────────────────────────────────────────────────────────
if should_export "snapchat"; then
    OUT="${OUTPUT_DIR}/${OUTPUT_NAME}_snapchat.mp4"
    log_start "Snapchat Spotlight (1080x1920, max 60s, CRF 26 — small file)"
    TRIM=""
    [ "$DURATION_INT" -gt 60 ] && TRIM="-t 60" && echo -e "  ${YELLOW}⚠ Trimming to 60s (Snapchat limit)${NC}"
    ffmpeg -i "$INPUT" \
        $SCALE_9x16 \
        $BASE_VIDEO -preset slow -crf 26 -r 30 \
        $BASE_AUDIO -b:a 128k \
        $TRIM -y "$OUT" 2>/dev/null
    # Check file size — Snapchat limit is 32MB
    SIZE_MB=$(du -m "$OUT" | cut -f1)
    if [ "$SIZE_MB" -gt 30 ]; then
        echo -e "  ${RED}⚠ File is ${SIZE_MB}MB — Snapchat limit is 32MB. Re-encoding with CRF 30...${NC}"
        ffmpeg -i "$INPUT" \
            $SCALE_9x16 \
            $BASE_VIDEO -preset slow -crf 30 -r 30 \
            $BASE_AUDIO -b:a 96k \
            $TRIM -y "$OUT" 2>/dev/null
    fi
    log_done "Snapchat Spotlight → $(basename $OUT)"
    log_size "$OUT"
fi

# ── Pinterest Idea Pin ────────────────────────────────────────────────────────
if should_export "pinterest"; then
    OUT="${OUTPUT_DIR}/${OUTPUT_NAME}_pinterest.mp4"
    log_start "Pinterest Idea Pin (1080x1920, max 60s, CRF 20)"
    TRIM=""
    [ "$DURATION_INT" -gt 60 ] && TRIM="-t 60" && echo -e "  ${YELLOW}⚠ Trimming to 60s (Pinterest limit)${NC}"
    ffmpeg -i "$INPUT" \
        $SCALE_9x16 \
        $BASE_VIDEO -preset slow -crf 20 -r 30 \
        $BASE_AUDIO -b:a 128k \
        $TRIM -y "$OUT" 2>/dev/null
    log_done "Pinterest Idea Pin → $(basename $OUT)"
    log_size "$OUT"
fi

# ── LinkedIn ──────────────────────────────────────────────────────────────────
if should_export "linkedin"; then
    OUT="${OUTPUT_DIR}/${OUTPUT_NAME}_linkedin.mp4"
    log_start "LinkedIn (1080x1920, max 30s, CRF 20)"
    TRIM=""
    [ "$DURATION_INT" -gt 30 ] && TRIM="-t 30" && echo -e "  ${YELLOW}⚠ Trimming to 30s (LinkedIn organic limit)${NC}"
    ffmpeg -i "$INPUT" \
        $SCALE_9x16 \
        $BASE_VIDEO -preset slow -crf 20 -r 30 \
        $BASE_AUDIO -b:a 128k \
        $TRIM -y "$OUT" 2>/dev/null
    log_done "LinkedIn → $(basename $OUT)"
    log_size "$OUT"
fi

# ── Square 1:1 (Instagram Feed / LinkedIn Feed) ───────────────────────────────
if should_export "square"; then
    OUT="${OUTPUT_DIR}/${OUTPUT_NAME}_square_1080.mp4"
    log_start "Square 1:1 (1080x1080, Instagram/LinkedIn feed)"
    ffmpeg -i "$INPUT" \
        -vf "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,crop=1080:1080:0:420" \
        $BASE_VIDEO -preset slow -crf 18 -r 30 \
        $BASE_AUDIO -b:a 128k \
        -y "$OUT" 2>/dev/null
    log_done "Square 1080x1080 → $(basename $OUT)"
    log_size "$OUT"
fi

# ── Thumbnail extraction ──────────────────────────────────────────────────────
THUMB="${OUTPUT_DIR}/${OUTPUT_NAME}_thumbnail.jpg"
log_start "Thumbnail (best quality frame)"
ffmpeg -ss 3 -i "$INPUT" -vframes 1 -q:v 2 -y "$THUMB" 2>/dev/null
log_done "Thumbnail → $(basename $THUMB)"

# ── Summary report ────────────────────────────────────────────────────────────
echo ""
echo "════════════════════════════════════════════════════"
echo " EXPORT COMPLETE"
echo "════════════════════════════════════════════════════"
echo ""
echo "Files created in: ${OUTPUT_DIR}"
echo ""
ls -lh "${OUTPUT_DIR}" | awk 'NR>1 {printf "  %-45s %s\n", $NF, $5}'
echo ""
TOTAL=$(du -sh "$OUTPUT_DIR" | cut -f1)
echo -e " Total size: ${TOTAL}"
echo ""
echo "════════════════════════════════════════════════════"
echo " UPLOAD CHECKLIST"
echo "════════════════════════════════════════════════════"
echo " □ Instagram Reels: instagram.com → + → Reel"
echo " □ TikTok:          tiktok.com → Upload"
echo " □ YouTube Shorts:  youtube.com → Create → Upload"
echo " □ Facebook Reels:  facebook.com → Reels → Create"
echo " □ Snapchat:        Snapchat → Spotlight"
echo " □ Pinterest:       pinterest.com → Create → Idea Pin"
echo " □ LinkedIn:        linkedin.com → Start a post → Video"
echo "════════════════════════════════════════════════════"
