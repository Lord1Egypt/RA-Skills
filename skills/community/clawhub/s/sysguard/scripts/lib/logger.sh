#!/usr/bin/env bash
#===============================================================================
# Logger Library
#===============================================================================

# === Config ===
LOG_DIR="${DATA_DIR:-/tmp}/sysguard/logs"
mkdir -p "$LOG_DIR"
LOG_FILE="$LOG_DIR/$(date +%Y-%m-%d).log"

# === Log Levels ===
LOG_LEVEL_DEBUG=0
LOG_LEVEL_INFO=1
LOG_LEVEL_WARN=2
LOG_LEVEL_ERROR=3
CURRENT_LEVEL="${LOG_LEVEL:-1}"

# === Color Codes ===
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# === Log Functions ===
log_debug() { [[ $CURRENT_LEVEL -le 0 ]] && _log "DEBUG" "$1"; }
log_info()  { [[ $CURRENT_LEVEL -le 1 ]] && _log "INFO"  "$1"; }
log_warn()  { [[ $CURRENT_LEVEL -le 2 ]] && _log "WARN"  "$1"; }
log_error() { [[ $CURRENT_LEVEL -le 3 ]] && _log "ERROR" "$1"; }

_log() {
    local level="$1"
    local msg="$2"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    echo "[$timestamp] [$level] $msg" >> "$LOG_FILE"
}

# === Emoji Alias ===
emoji_ok()   { echo "✅"; }
emoji_warn() { echo "⚠️"; }
emoji_fail() { echo "❌"; }
emoji_info() { echo "📢"; }
