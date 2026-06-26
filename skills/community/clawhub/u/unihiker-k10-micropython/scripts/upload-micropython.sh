#!/bin/bash
#
# Unihiker K10 Skill - MicroPython Upload
# Uploads Python files to K10 using mpremote
#

set -e

FILE="$1"
PORT="$2"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log_info() { echo -e "${BLUE}[INFO]${NC} $1"; }
log_success() { echo -e "${GREEN}[OK]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1" >&2; }

# Validate inputs
if [[ -z "$FILE" ]]; then
    log_error "No file specified"
    exit 1
fi

if [[ ! -f "$FILE" ]]; then
    log_error "File not found: $FILE"
    exit 1
fi

if [[ -z "$PORT" ]]; then
    log_error "No port specified"
    exit 1
fi

FILENAME=$(basename "$FILE")

log_info "Uploading $FILENAME to K10 on $PORT..."

# Try mpremote first, fall back to ampy
if command -v mpremote >/dev/null 2>&1; then
    log_info "Using mpremote..."
    
    # Connect, upload file, and reset
    if mpremote connect "$PORT" fs cp "$FILE" ":$FILENAME"; then
        log_success "Upload successful"
        
        # Reset to run the new code if it's main.py
        if [[ "$FILENAME" == "main.py" ]]; then
            log_info "Resetting device to run main.py..."
            mpremote connect "$PORT" reset || true
        fi
        
        log_success "Done!"
    else
        log_error "Upload failed with mpremote"
        exit 1
    fi
    
elif command -v ampy >/dev/null 2>&1; then
    log_info "Using ampy..."
    
    if ampy --port "$PORT" put "$FILE"; then
        log_success "Upload successful"
        
        # List files to confirm
        log_info "Files on device:"
        ampy --port "$PORT" ls || true
        
        # Reset board
        log_info "Resetting device..."
        ampy --port "$PORT" reset || true
        
        log_success "Done!"
    else
        log_error "Upload failed with ampy"
        exit 1
    fi
    
else
    log_error "No upload tool found. Please install mpremote:"
    log_error "  pip install mpremote"
    exit 1
fi

log_info "You can also use 'mpremote connect $PORT repl' for interactive debugging"
