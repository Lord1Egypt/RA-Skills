#!/bin/bash
# Production-Ready PDF Build Script
# Demonstrates error handling, validation, and logging

set -e  # Exit on any error
set -u  # Error on undefined variables
set -o pipefail  # Catch errors in pipes

# ==============================================================================
# Configuration
# ==============================================================================
INPUT_FILE="DOCUMENT.md"
OUTPUT_FILE="DOCUMENT.pdf"
BIBLIOGRAPHY="references.bib"
LATEX_PREAMBLE="table-spacing.tex"
LOG_FILE="build-pdf.log"

# ==============================================================================
# Log Rotation - prevent unbounded growth
# ADR: /docs/adr/2025-12-07-idempotency-backup-traceability.md
# ==============================================================================
LOG_ROTATION_KEEP_COUNT=5
rotate_log() {
    local log_file="$1"
    local keep_count="${2:-$LOG_ROTATION_KEEP_COUNT}"

    if [ -f "$log_file" ]; then
        mv "$log_file" "${log_file}.$(date +%s)"
        # Keep only last N logs
        ls -t "${log_file}."* 2>/dev/null | tail -n +$((keep_count + 1)) | xargs rm -f 2>/dev/null || true
    fi
}

# Rotate log before starting new build
rotate_log "$LOG_FILE" "$LOG_ROTATION_KEEP_COUNT"

# ==============================================================================
# Color Output
# ==============================================================================
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log_info() { echo -e "${GREEN}✓${NC} $1" | tee -a "$LOG_FILE"; }
log_warn() { echo -e "${YELLOW}⚠${NC} $1" | tee -a "$LOG_FILE"; }
log_error() { echo -e "${RED}✗${NC} $1" | tee -a "$LOG_FILE"; }

# ==============================================================================
# Pre-flight Checks
# ==============================================================================
echo "$(date '+%Y-%m-%d %H:%M:%S') - Starting PDF build" > "$LOG_FILE"

# Check if input file exists
if [[ ! -f "$INPUT_FILE" ]]; then
    log_error "Input file not found: $INPUT_FILE"
    exit 1
fi

# Check if Pandoc is installed
if ! command -v pandoc &> /dev/null; then
    log_error "Pandoc is not installed. Install with: brew install pandoc"
    exit 1
fi

# Check Pandoc version
PANDOC_VERSION=$(pandoc --version | head -n1)
log_info "Using $PANDOC_VERSION"

# Check if XeLaTeX is available
if ! command -v xelatex &> /dev/null; then
    log_error "XeLaTeX not found. Install MacTeX: brew install --cask mactex"
    exit 1
fi

# Check optional files
[[ -f "$BIBLIOGRAPHY" ]] && log_info "Bibliography file found" || log_warn "Bibliography file not found (optional)"
[[ -f "$LATEX_PREAMBLE" ]] && log_info "LaTeX preamble found" || log_warn "LaTeX preamble not found (optional)"

# ==============================================================================
# Build PDF
# ==============================================================================
log_info "Generating PDF: $OUTPUT_FILE"

# Backup existing PDF if it exists
if [[ -f "$OUTPUT_FILE" ]]; then
    BACKUP_FILE="${OUTPUT_FILE}.backup-$(date +%Y%m%d-%H%M%S)"
    cp "$OUTPUT_FILE" "$BACKUP_FILE"
    log_info "Backed up existing PDF to: $BACKUP_FILE"
fi

# Build command with optional flags
PANDOC_CMD=(
    pandoc "$INPUT_FILE"
    -o "$OUTPUT_FILE"
    --pdf-engine=xelatex
    --toc
    --toc-depth=3
    --number-sections
    -V mainfont="DejaVu Sans"
    -V geometry:margin=1in
    -V toc-title="Table of Contents"
)

# Add bibliography if available
if [[ -f "$BIBLIOGRAPHY" ]]; then
    PANDOC_CMD+=(--citeproc --bibliography="$BIBLIOGRAPHY")
fi

# Add LaTeX preamble if available
if [[ -f "$LATEX_PREAMBLE" ]]; then
    PANDOC_CMD+=(-H "$LATEX_PREAMBLE")
fi

# Execute Pandoc
if "${PANDOC_CMD[@]}" >> "$LOG_FILE" 2>&1; then
    log_info "PDF generated successfully"
else
    log_error "PDF generation failed. Check $LOG_FILE for details"
    exit 1
fi

# ==============================================================================
# Post-build Validation
# ==============================================================================

# Check if output file exists
if [[ ! -f "$OUTPUT_FILE" ]]; then
    log_error "Output file was not created"
    exit 1
fi

# Get file size
FILE_SIZE=$(ls -lh "$OUTPUT_FILE" | awk '{print $5}')
log_info "PDF size: $FILE_SIZE"

# Get page count (requires pdfinfo)
if command -v pdfinfo &> /dev/null; then
    PAGE_COUNT=$(pdfinfo "$OUTPUT_FILE" 2>/dev/null | grep "^Pages:" | awk '{print $2}')
    if [[ -n "$PAGE_COUNT" ]]; then
        log_info "Page count: $PAGE_COUNT pages"
    fi
else
    log_warn "pdfinfo not available (install with: brew install poppler)"
fi

# ==============================================================================
# Success Summary
# ==============================================================================
echo ""
echo "======================================"
log_info "Build completed successfully"
echo "======================================"
echo "Output:  $OUTPUT_FILE"
echo "Size:    $FILE_SIZE"
[[ -n "${PAGE_COUNT:-}" ]] && echo "Pages:   $PAGE_COUNT"
echo "Log:     $LOG_FILE"
echo "======================================"
echo ""
log_info "To view: open $OUTPUT_FILE"
