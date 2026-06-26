#!/usr/bin/env bash
# Universal PDF Build Script for Pandoc
# Usage: ./build-pdf.sh [OPTIONS] [input.md] [output.pdf]
#
# Options:
#   --landscape      Landscape orientation (default)
#   --portrait       Portrait orientation
#   --monospace      Use monospace font (DejaVu Sans Mono) - ideal for ASCII diagrams
#   --hide-details   Hide <details> blocks (e.g., graph-easy source) from PDF output
#   -h, --help       Show this help message
#
# If no input file provided, looks for single .md file in current directory

set -euo pipefail

# ==============================================================================
# Configuration
# ==============================================================================
# Resolve the actual directory of this script (works with symlinks)
SCRIPT_DIR="$(cd "$(dirname "$(readlink -f "$0" 2>/dev/null || echo "$0")")" && pwd)"
LATEX_PREAMBLE="$SCRIPT_DIR/table-spacing-template.tex"
HIDE_DETAILS_FILTER="$SCRIPT_DIR/hide-details-for-pdf.lua"

# Defaults
ORIENTATION="landscape"
FONT="DejaVu Sans"
USE_HIDE_DETAILS=""

# Color output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

log_info() { echo -e "${GREEN}✓${NC} $1"; }
log_warn() { echo -e "${YELLOW}⚠${NC} $1"; }
log_error() { echo -e "${RED}✗${NC} $1"; }

show_help() {
    echo "Usage: $0 [OPTIONS] [input.md] [output.pdf]"
    echo ""
    echo "Options:"
    echo "  --landscape      Landscape orientation (default)"
    echo "  --portrait       Portrait orientation"
    echo "  --monospace      Use monospace font (DejaVu Sans Mono) - ideal for ASCII diagrams"
    echo "  --hide-details   Hide <details> blocks (e.g., graph-easy source) from PDF output"
    echo "  -h, --help       Show this help message"
    echo ""
    echo "If no input file provided, auto-detects single .md file in current directory."
    echo ""
    echo "Examples:"
    echo "  $0                               # Auto-detect, landscape"
    echo "  $0 --portrait doc.md             # Portrait mode"
    echo "  $0 --monospace diagrams.md       # Monospace font for ASCII art"
    echo "  $0 --hide-details doc.md         # Hide <details> blocks in PDF"
    echo "  $0 doc.md output.pdf             # Explicit input/output"
}

# ==============================================================================
# Parse Arguments
# ==============================================================================
POSITIONAL_ARGS=()

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
        --monospace)
            FONT="DejaVu Sans Mono"
            shift
            ;;
        --hide-details)
            USE_HIDE_DETAILS="yes"
            shift
            ;;
        -h|--help)
            show_help
            exit 0
            ;;
        -*)
            log_error "Unknown option: $1"
            show_help
            exit 1
            ;;
        *)
            POSITIONAL_ARGS+=("$1")
            shift
            ;;
    esac
done

# Restore positional parameters
set -- "${POSITIONAL_ARGS[@]}"

# ==============================================================================
# Input Detection
# ==============================================================================

# If input file provided as argument
if [[ -n "${1:-}" ]]; then
    INPUT_FILE="$1"
# Otherwise, auto-detect single .md file in current directory
else
    MD_FILES=(*.md)
    if [[ ${#MD_FILES[@]} -eq 0 || ! -f "${MD_FILES[0]}" ]]; then
        log_error "No Markdown files found in current directory"
        show_help
        exit 1
    elif [[ ${#MD_FILES[@]} -gt 1 ]]; then
        log_error "Multiple Markdown files found. Please specify which one:"
        printf '  - %s\n' "${MD_FILES[@]}"
        show_help
        exit 1
    fi
    INPUT_FILE="${MD_FILES[0]}"
fi

# Verify input file exists
if [[ ! -f "$INPUT_FILE" ]]; then
    log_error "Input file not found: $INPUT_FILE"
    exit 1
fi

# If output file provided as argument
if [[ -n "${2:-}" ]]; then
    OUTPUT_FILE="$2"
else
    # Auto-generate output filename from input
    OUTPUT_FILE="${INPUT_FILE%.md}.pdf"
fi

log_info "Input:  $INPUT_FILE"
log_info "Output: $OUTPUT_FILE"
log_info "Orientation: $ORIENTATION"
log_info "Font: $FONT"
if [[ -n "$USE_HIDE_DETAILS" ]]; then
    log_info "Hide details: enabled"
fi

# ==============================================================================
# Pre-flight Checks
# ==============================================================================

# Check if Pandoc is installed
if ! command -v pandoc &> /dev/null; then
    log_error "Pandoc is not installed. Install with: brew install pandoc"
    exit 1
fi

# Check if XeLaTeX is available
if ! command -v xelatex &> /dev/null; then
    log_error "XeLaTeX not found. Install MacTeX: brew install --cask mactex"
    exit 1
fi

# Check if LaTeX preamble exists
if [[ ! -f "$LATEX_PREAMBLE" ]]; then
    log_error "LaTeX preamble not found: $LATEX_PREAMBLE"
    exit 1
fi

# ==============================================================================
# Build PDF
# ==============================================================================
log_info "Generating PDF with table of contents..."

# Check for local or global bibliography
BIBLIOGRAPHY=""
if [[ -f "references.bib" ]]; then
    BIBLIOGRAPHY="--citeproc --bibliography=references.bib"
    log_info "Using bibliography: references.bib"
fi

# Check for CSL style
CSL=""
if [[ -f "chicago-note-bibliography.csl" ]]; then
    CSL="--csl=chicago-note-bibliography.csl"
    log_info "Using citation style: chicago-note-bibliography.csl"
fi

# Build geometry string based on orientation
if [[ "$ORIENTATION" == "landscape" ]]; then
    GEOMETRY="a4paper,landscape"
else
    GEOMETRY="a4paper"
fi

# Build Lua filter option if requested
LUA_FILTER=""
if [[ -n "$USE_HIDE_DETAILS" ]]; then
    if [[ -f "$HIDE_DETAILS_FILTER" ]]; then
        LUA_FILTER="--lua-filter=$HIDE_DETAILS_FILTER"
        log_info "Using Lua filter: hide-details-for-pdf.lua"
    else
        log_warn "Hide details filter not found: $HIDE_DETAILS_FILTER"
    fi
fi

# Build command - use array for optional arguments to avoid SC2086
PANDOC_OPTS=()
[[ -n "$LUA_FILTER" ]] && PANDOC_OPTS+=("$LUA_FILTER")
[[ -n "$BIBLIOGRAPHY" ]] && PANDOC_OPTS+=("$BIBLIOGRAPHY")
[[ -n "$CSL" ]] && PANDOC_OPTS+=("$CSL")

pandoc "$INPUT_FILE" \
  -o "$OUTPUT_FILE" \
  --pdf-engine=xelatex \
  --toc \
  --toc-depth=3 \
  --number-sections \
  -V mainfont="$FONT" \
  -V monofont="DejaVu Sans Mono" \
  -V geometry:"$GEOMETRY" \
  -V geometry:margin=1in \
  -V toc-title="Table of Contents" \
  -H "$LATEX_PREAMBLE" \
  "${PANDOC_OPTS[@]}"

# ==============================================================================
# Post-build Validation
# ==============================================================================

if [[ ! -f "$OUTPUT_FILE" ]]; then
    log_error "PDF generation failed - output file not created"
    exit 1
fi

# Use stat for portable file size (avoids SC2012 ls warning)
if [[ "$OSTYPE" == "darwin"* ]]; then
    FILE_SIZE=$(stat -f%z "$OUTPUT_FILE" | awk '{printf "%.1fK", $1/1024}')
else
    FILE_SIZE=$(stat --printf="%s" "$OUTPUT_FILE" | awk '{printf "%.1fK", $1/1024}')
fi
log_info "PDF generated: $OUTPUT_FILE ($FILE_SIZE)"

# Get page count if pdfinfo available
if command -v pdfinfo &> /dev/null; then
    PAGE_COUNT=$(pdfinfo "$OUTPUT_FILE" 2>/dev/null | grep "^Pages:" | awk '{print $2}')
    if [[ -n "$PAGE_COUNT" ]]; then
        log_info "Page count: $PAGE_COUNT pages"
    fi
fi

echo ""
echo "Build complete!"
echo "   View: open $OUTPUT_FILE"
