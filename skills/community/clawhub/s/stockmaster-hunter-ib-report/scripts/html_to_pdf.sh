#!/bin/bash
# ============================================================
# StockMaster Hunter - HTML to PDF Converter
# 摩根士丹利风格投行报告 HTML 转 PDF 工具
#
# Usage:
#   ./html_to_pdf.sh input.html output.pdf
#   ./html_to_pdf.sh input.html output.pdf --landscape
#
# Requirements:
#   - Google Chrome (macOS) or Chromium (Linux)
# ============================================================

set -e

# Color output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Default settings
ORIENTATION="portrait"
VIRTUAL_TIME_BUDGET=15000
WAIT_TIME=2

# Parse arguments
INPUT_HTML=""
OUTPUT_PDF=""

while [[ $# -gt 0 ]]; do
    case $1 in
        --landscape)
            ORIENTATION="landscape"
            shift
            ;;
        --portrait)
            ORIENTATION="portrait"
            shift
            ;;
        --wait)
            WAIT_TIME="$2"
            shift 2
            ;;
        --virtual-time)
            VIRTUAL_TIME_BUDGET="$2"
            shift 2
            ;;
        -h|--help)
            echo "Usage: $0 input.html output.pdf [options]"
            echo ""
            echo "Options:"
            echo "  --landscape       Set PDF orientation to landscape"
            echo "  --portrait        Set PDF orientation to portrait (default)"
            echo "  --wait SECONDS    Wait time before conversion (default: 2)"
            echo "  --virtual-time MS Virtual time budget (default: 15000)"
            echo "  -h, --help        Show this help message"
            exit 0
            ;;
        *)
            if [ -z "$INPUT_HTML" ]; then
                INPUT_HTML="$1"
            elif [ -z "$OUTPUT_PDF" ]; then
                OUTPUT_PDF="$1"
            else
                echo -e "${RED}Unknown argument: $1${NC}"
                exit 1
            fi
            shift
            ;;
    esac
done

# Validate inputs
if [ -z "$INPUT_HTML" ] || [ -z "$OUTPUT_PDF" ]; then
    echo -e "${RED}Error: Input HTML and output PDF paths are required.${NC}"
    echo "Usage: $0 input.html output.pdf [options]"
    exit 1
fi

if [ ! -f "$INPUT_HTML" ]; then
    echo -e "${RED}Error: Input file not found: $INPUT_HTML${NC}"
    exit 1
fi

# Get absolute paths
INPUT_HTML=$(cd "$(dirname "$INPUT_HTML")" && pwd)/$(basename "$INPUT_HTML")
OUTPUT_PDF=$(cd "$(dirname "$OUTPUT_PDF")" && pwd)/$(basename "$OUTPUT_PDF")

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}StockMaster Hunter - HTML to PDF${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""
echo -e "Input:  ${YELLOW}$INPUT_HTML${NC}"
echo -e "Output: ${YELLOW}$OUTPUT_PDF${NC}"
echo -e "Orientation: ${YELLOW}$ORIENTATION${NC}"
echo ""

# Detect Chrome/Chromium
CHROME_PATH=""

if [ -f "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" ]; then
    CHROME_PATH="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
elif [ -f "/Applications/Chromium.app/Contents/MacOS/Chromium" ]; then
    CHROME_PATH="/Applications/Chromium.app/Contents/MacOS/Chromium"
elif command -v google-chrome &> /dev/null; then
    CHROME_PATH=$(command -v google-chrome)
elif command -v chromium &> /dev/null; then
    CHROME_PATH=$(command -v chromium)
elif command -v chromium-browser &> /dev/null; then
    CHROME_PATH=$(command -v chromium-browser)
else
    echo -e "${RED}Error: Google Chrome or Chromium not found.${NC}"
    echo "Please install Google Chrome or Chromium."
    echo "macOS: brew install --cask google-chrome"
    echo "Linux: sudo apt install chromium-browser"
    exit 1
fi

echo -e "Chrome: ${YELLOW}$CHROME_PATH${NC}"
echo ""

# Wait for resources to load
echo -e "${YELLOW}Waiting $WAIT_TIME seconds for resources to load...${NC}"
sleep "$WAIT_TIME"

# Convert HTML to PDF using Chrome headless
echo -e "${YELLOW}Converting HTML to PDF...${NC}"

# Build Chrome command
CHROME_ARGS=(
    --headless
    --disable-gpu
    --no-sandbox
    --disable-dev-shm-usage
    --print-to-pdf="$OUTPUT_PDF"
    --no-pdf-header-footer
    --print-to-pdf-no-header
    --virtual-time-budget="$VIRTUAL_TIME_BUDGET"
    --run-all-compositor-stages-before-draw
)

# Add orientation if landscape
if [ "$ORIENTATION" = "landscape" ]; then
    CHROME_ARGS+=(--landscape)
fi

# Add input URL (file:// protocol)
INPUT_URL="file://$INPUT_HTML"
CHROME_ARGS+=("$INPUT_URL")

# Execute Chrome
"$CHROME_PATH" "${CHROME_ARGS[@]}" 2>&1 | grep -v "Trying to load the allocator" || true

# Check if output was created
if [ -f "$OUTPUT_PDF" ]; then
    FILE_SIZE=$(ls -lh "$OUTPUT_PDF" | awk '{print $5}')
    echo ""
    echo -e "${GREEN}========================================${NC}"
    echo -e "${GREEN}✓ PDF generated successfully!${NC}"
    echo -e "${GREEN}  File: $OUTPUT_PDF${NC}"
    echo -e "${GREEN}  Size: $FILE_SIZE${NC}"
    echo -e "${GREEN}========================================${NC}"

    # Try to get page count using mdls (macOS) or pdfinfo (Linux)
    if command -v mdls &> /dev/null; then
        PAGE_COUNT=$(mdls -name kMDItemNumberOfPages -raw "$OUTPUT_PDF" 2>/dev/null || echo "unknown")
        echo -e "${GREEN}  Pages: $PAGE_COUNT${NC}"
    elif command -v pdfinfo &> /dev/null; then
        PAGE_COUNT=$(pdfinfo "$OUTPUT_PDF" 2>/dev/null | grep "Pages:" | awk '{print $2}')
        echo -e "${GREEN}  Pages: $PAGE_COUNT${NC}"
    fi
else
    echo -e "${RED}Error: PDF was not generated.${NC}"
    exit 1
fi
