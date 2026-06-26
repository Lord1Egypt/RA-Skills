#!/bin/bash
set -e

PORT="$1"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"
FIRMWARE="${SKILL_DIR}/firmware/k10-micropython-v0.9.2.bin"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log_info() { echo -e "${BLUE}[INFO]${NC} $1"; }
log_success() { echo -e "${GREEN}[OK]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1" >&2; }

check_dependencies() {
    if ! command -v esptool >/dev/null 2>&1; then
        log_error "esptool not found"
        log_info "Install with: pip install esptool"
        exit 1
    fi

    if [[ ! -f "$FIRMWARE" ]]; then
        log_error "Firmware not found: $FIRMWARE"
        exit 1
    fi
}

detect_port() {
    if [[ -z "$PORT" ]]; then
        log_info "Auto-detecting K10 port..."
        PORT=$(bash "${SCRIPT_DIR}/find-port.sh" 2>/dev/null || true)
        if [[ -z "$PORT" ]]; then
            log_error "Could not auto-detect K10 port"
            log_error "Please specify with --port or connect K10"
            exit 1
        fi
        log_success "Found K10 on $PORT"
    fi
}

enter_download_mode() {
    echo ""
    log_warn "=== AUTO FLASH MODE ==="
    echo ""
    log_info "Step 1: Holding BOOT button..."
    log_info "Step 2: Resetting K10 to enter download mode..."
    echo ""

    if command -v stty >/dev/null 2>&1; then
        stty -F "$PORT" raw 0 2>/dev/null || true
    fi

    echo -n "\x03" > "$PORT" 2>/dev/null || true
    sleep 0.5

    log_info "Step 3: Waiting for K10 to enter download mode..."
    sleep 2
}

flash_firmware() {
    log_info "Flashing MicroPython firmware..."
    log_info "Firmware: $FIRMWARE"
    log_info "Port: $PORT"
    log_info "This will take 30-60 seconds..."
    echo ""

    if esptool --chip esp32s3 \
               --port "$PORT" \
               --baud 460800 \
               --before default_reset \
               write_flash \
               0x0 "$FIRMWARE"; then
        echo ""
        log_success "Flash successful!"
    else
        echo ""
        log_error "Flash failed"
        log_info "Tips:"
        log_info "  - Make sure K10 is connected"
        log_info "  - Try holding BOOT button, press RST, then release BOOT"
        log_info "  - Try: k10 flash-micropython (manual mode)"
        exit 1
    fi
}

reset_device() {
    echo ""
    log_info "Resetting K10..."
    sleep 1

    if command -v stty >/dev/null 2>&1; then
        stty -F "$PORT" -hupcl 2>/dev/null || true
    fi

    echo -n "\x03" > "$PORT" 2>/dev/null || true
    sleep 2

    log_info "K10 will boot into MicroPython"
    echo ""
    log_success "Done! You can now upload Python code."
    log_info "Use: k10 upload-mp <file.py>"
}

main() {
    check_dependencies
    detect_port
    enter_download_mode
    flash_firmware
    reset_device
}

main
