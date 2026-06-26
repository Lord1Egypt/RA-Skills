#!/usr/bin/env bash
# setup.sh — Install/uninstall the self-heal watchdog
set -euo pipefail

OPENCLAW_HOME="${OPENCLAW_HOME:-$HOME/.openclaw}"
WATCHDOG_DIR="$OPENCLAW_HOME/watchdog"
STATE_FILE="$WATCHDOG_DIR/watchdog-state.json"
CONFIG_FILE="$OPENCLAW_HOME/openclaw.json"
SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
CRON_MARKER="# openclaw-watchdog"
LAUNCHD_PLIST="$HOME/Library/LaunchAgents/com.openclaw.watchdog.plist"

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[0;33m'
NC='\033[0m'

log() { echo -e "${GREEN}[setup]${NC} $*"; }
warn() { echo -e "${YELLOW}[setup]${NC} $*"; }
err() { echo -e "${RED}[setup]${NC} $*"; }

# ── Uninstall ──
if [[ "${1:-}" == "--uninstall" ]]; then
    log "Uninstalling watchdog..."
    # Unload and remove launchd agent
    launchctl unload "$LAUNCHD_PLIST" 2>/dev/null || true
    rm -f "$LAUNCHD_PLIST"
    log "launchd agent removed."
    # Also remove any legacy cron entry
    (crontab -l 2>/dev/null | grep -v "$CRON_MARKER" | crontab -) 2>/dev/null || true
    log "Cron job removed."
    # Optionally remove watchdog dir
    if [[ "${2:-}" == "--clean" ]]; then
        rm -rf "$WATCHDOG_DIR"
        log "Watchdog directory removed."
    else
        warn "Watchdog files kept at $WATCHDOG_DIR (use --uninstall --clean to remove)"
    fi
    log "Uninstall complete ✅"
    exit 0
fi

# ── Install ──
log "Installing self-heal watchdog..."

# 1. Create watchdog directory
mkdir -p "$WATCHDOG_DIR"
log "Directory: $WATCHDOG_DIR"

# 2. Copy scripts
cp "$SKILL_DIR/scripts/watchdog.sh" "$WATCHDOG_DIR/"
cp "$SKILL_DIR/scripts/health-check.sh" "$WATCHDOG_DIR/"
cp "$SKILL_DIR/scripts/model-failover.sh" "$WATCHDOG_DIR/"
chmod +x "$WATCHDOG_DIR"/*.sh
log "Scripts copied and made executable."

# 3. Create initial state file
if [[ ! -f "$STATE_FILE" ]]; then
    # Read current model from config
    CURRENT_MODEL=$(python3 -c "
import json, sys
try:
    with open('$CONFIG_FILE') as f:
        d = json.load(f)
    print(d.get('agents',{}).get('defaults',{}).get('model',{}).get('primary','unknown'))
except:
    print('unknown')
" 2>/dev/null || echo "unknown")

    cat > "$STATE_FILE" << EOF
{
  "current_model": "$CURRENT_MODEL",
  "original_model": "$CURRENT_MODEL",
  "fail_count": 0,
  "last_check": null,
  "last_failover": null,
  "config_backups": 0,
  "failed_models": []
}
EOF
    log "State file created (model: $CURRENT_MODEL)."
else
    log "State file already exists, skipping."
fi

# 4. First config backup
BACKUP_FILE="${CONFIG_FILE}.bak"
cp "$CONFIG_FILE" "$BACKUP_FILE"
log "Config backed up to $BACKUP_FILE."

# 5. Register launchd agent (macOS-native scheduler, every 60s)
mkdir -p "$HOME/Library/LaunchAgents"
if [[ -f "$LAUNCHD_PLIST" ]]; then
    # Unload existing first
    launchctl unload "$LAUNCHD_PLIST" 2>/dev/null || true
fi

cat > "$LAUNCHD_PLIST" << PLISTEOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.openclaw.watchdog</string>
    <key>ProgramArguments</key>
    <array>
        <string>/bin/bash</string>
        <string>$WATCHDOG_DIR/watchdog.sh</string>
    </array>
    <key>StartInterval</key>
    <integer>60</integer>
    <key>StandardOutPath</key>
    <string>$WATCHDOG_DIR/watchdog.log</string>
    <key>StandardErrorPath</key>
    <string>$WATCHDOG_DIR/watchdog.log</string>
    <key>WorkingDirectory</key>
    <string>$WATCHDOG_DIR</string>
    <key>EnvironmentVariables</key>
    <dict>
        <key>PATH</key>
        <string>/usr/local/bin:/opt/homebrew/bin:/usr/bin:/bin:/usr/sbin:/sbin:$HOME/.npm-global/bin</string>
        <key>HOME</key>
        <string>$HOME</string>
        <key>OPENCLAW_HOME</key>
        <string>$OPENCLAW_HOME</string>
    </dict>
</dict>
</plist>
PLISTEOF

# Load the agent
if launchctl load "$LAUNCHD_PLIST" 2>/dev/null; then
    log "launchd agent registered (runs every 60s)."
else
    warn "launchd load returned non-zero (may already be loaded). Try: launchctl load $LAUNCHD_PLIST"
fi

# 6. Initialize log
mkdir -p "$(dirname "$WATCHDOG_DIR/watchdog.log")"
touch "$WATCHDOG_DIR/watchdog.log"

echo ""
log "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
log " ✅ Self-Heal Watchdog installed!"
log ""
log " Files:"
log "   Scripts:  $WATCHDOG_DIR/"
log "   State:    $STATE_FILE"
log "   Log:      $WATCHDOG_DIR/watchdog.log"
log ""
log " Commands:"
log "   Status:   bash $SKILL_DIR/scripts/status.sh"
log "   Run once: bash $WATCHDOG_DIR/watchdog.sh"
log "   Dry-run:  DRY_RUN=1 bash $WATCHDOG_DIR/watchdog.sh"
log "   Uninstall: bash $SKILL_DIR/scripts/setup.sh --uninstall"
log "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
