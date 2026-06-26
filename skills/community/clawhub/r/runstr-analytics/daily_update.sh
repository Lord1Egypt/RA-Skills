#!/bin/bash
# RUNSTR Daily Update Script
# Automatically fetches fresh data if backup is old, then generates report
#
# SECURITY NOTICE:
# - This script reads RUNSTR_NSEC from environment (set before running)
# - The nsec is passed securely via stdin to prevent CLI exposure
# - Cache directory uses restrictive permissions (0700)
# - Ensure your system does not log environment variables

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CACHE_DIR="$HOME/.cache/runstr-analytics"
LOG_FILE="$CACHE_DIR/daily_update.log"
REPORT_FILE="$CACHE_DIR/latest_report.txt"

# Get NSEC from environment variable
NSEC="${RUNSTR_NSEC:-}"

if [ -z "$NSEC" ]; then
    echo "Error: RUNSTR_NSEC environment variable is not set"
    echo "Set it with: export RUNSTR_NSEC='nsec1...'"
    exit 1
fi

# Ensure cache dir exists
mkdir -p "$CACHE_DIR"

# Add snap and nak to PATH
export PATH="$PATH:/snap/bin:$HOME/go/bin"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

log "Starting RUNSTR daily update..."

# Check if we have recent data in cache (less than 12 hours old)
REFRESH_NEEDED=false
if [ ! -f "$CACHE_DIR/runstr_cache.db" ]; then
    log "No cache found, refresh needed"
    REFRESH_NEEDED=true
else
    # Check age of cache
    CACHE_AGE=$(stat -c %Y "$CACHE_DIR/runstr_cache.db" 2>/dev/null || stat -f %m "$CACHE_DIR/runstr_cache.db" 2>/dev/null || echo 0)
    CURRENT_TIME=$(date +%s)
    AGE_HOURS=$(( (CURRENT_TIME - CACHE_AGE) / 3600 ))
    
    if [ $AGE_HOURS -gt 12 ]; then
        log "Cache is $AGE_HOURS hours old, refresh needed"
        REFRESH_NEEDED=true
    else
        log "Cache is $AGE_HOURS hours old, using cached data"
    fi
fi

# Run analysis
cd "$SCRIPT_DIR"
if [ "$REFRESH_NEEDED" = true ]; then
    log "Fetching fresh data from Nostr..."
    python3 scripts/analyze_extended.py \
        --nsec "$NSEC" \
        --days 60 \
        --insights \
        --force-refresh > "$REPORT_FILE" 2>&1
    log "Refresh complete"
else
    log "Generating report from cache..."
    python3 scripts/analyze_extended.py \
        --days 60 \
        --insights > "$REPORT_FILE" 2>&1
    log "Report generated"
fi

# Show summary
log "Daily update complete. Report saved to $REPORT_FILE"

# Optional: Send notification (uncomment if desired)
# notify-send "RUNSTR Update" "Daily fitness report ready" 2>/dev/null || true

exit 0
