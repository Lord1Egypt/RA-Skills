#!/usr/bin/env bash
# session-janitor setup — discovers gateways, generates config, installs cron
set -euo pipefail

SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
CONFIG_FILE="$SKILL_DIR/config.json"
OS="$(uname -s)"

echo "=== Session Janitor Setup ==="
echo ""

# --- Discover gateways ---
echo "Scanning for OpenClaw gateway installations..."
gateways=()
gateway_dirs=()

# Check standard locations
for candidate in "$HOME/.openclaw" "$HOME/.openclaw-"*; do
    [[ -d "$candidate" ]] || continue
    [[ -f "$candidate/openclaw.json" ]] || continue

    config_json="$candidate/openclaw.json"
    sessions_dir="$candidate/agents/main/sessions"

    if [[ ! -d "$sessions_dir" ]]; then
        echo "  ⚠ Found $candidate but no sessions dir — skipping"
        continue
    fi

    # Extract name from dir
    dirname=$(basename "$candidate")
    if [[ "$dirname" == ".openclaw" ]]; then
        name="default"
    else
        name="${dirname#.openclaw-}"
    fi

    # Extract port from config
    port=$(python3 -c "
import json
c = json.load(open('$config_json'))
print(c.get('gateway',{}).get('port', c.get('port', 18789)))
" 2>/dev/null || echo "18789")

    # Extract auth token
    token=$(python3 -c "
import json
c = json.load(open('$config_json'))
print(c.get('gateway',{}).get('auth',{}).get('token',''))
" 2>/dev/null || echo "")

    echo "  ✓ Found gateway: $name (${candidate}, port $port)"
    gateways+=("$name")
    gateway_dirs+=("$candidate")
done

if [[ ${#gateways[@]} -eq 0 ]]; then
    echo ""
    echo "❌ No OpenClaw gateway installations found."
    echo "   Expected: ~/.openclaw/openclaw.json or ~/.openclaw-*/openclaw.json"
    exit 1
fi

echo ""
echo "Found ${#gateways[@]} gateway(s): ${gateways[*]}"
echo ""

# --- Check for mem CLI ---
mem_available=false
mem_path=""
if command -v mem &>/dev/null; then
    mem_available=true
    mem_path=$(command -v mem)
    echo "✓ mem CLI found at $mem_path"
elif [[ -x "$HOME/bin/mem" ]]; then
    mem_available=true
    mem_path="$HOME/bin/mem"
    echo "✓ mem CLI found at $mem_path"
elif [[ -x "$HOME/.npm-global/bin/mem" ]]; then
    mem_available=true
    mem_path="$HOME/.npm-global/bin/mem"
    echo "✓ mem CLI found at $mem_path"
else
    echo "ℹ mem CLI not found — LLM extraction will skip structured memory storage"
    echo "  (Memories will still be extracted, just not stored in a searchable DB)"
fi

# --- Check for Python 3 ---
if ! command -v python3 &>/dev/null; then
    echo "❌ python3 is required but not found"
    exit 1
fi
echo "✓ python3 found"

# --- Check OS-specific watcher dependency ---
if [[ "$OS" == "Darwin" ]]; then
    if command -v fswatch &>/dev/null; then
        echo "✓ fswatch found (per-turn watcher)"
    else
        echo "⚠ fswatch not found — per-turn watcher will not work"
        echo "  Install with: brew install fswatch"
        echo "  (cron-based trimming every 15 min will still work without it)"
    fi
else
    if command -v inotifywait &>/dev/null; then
        echo "✓ inotifywait found (per-turn watcher)"
    else
        echo "⚠ inotifywait not found — per-turn watcher will not work"
        echo "  Install with: sudo apt install inotify-tools (or equivalent)"
        echo "  (cron-based trimming every 15 min will still work without it)"
    fi
fi

# --- Generate config ---
echo ""
echo "Generating config.json..."

python3 - "$CONFIG_FILE" "${gateways[@]}" <<'PYEOF'
import json, sys, os, subprocess

config_file = sys.argv[1]
gateway_names = sys.argv[2:]

gateways = []
for name in gateway_names:
    if name == "default":
        config_dir = os.path.expanduser("~/.openclaw")
    else:
        config_dir = os.path.expanduser(f"~/.openclaw-{name}")

    config_json = os.path.join(config_dir, "openclaw.json")
    sessions_dir = os.path.join(config_dir, "agents/main/sessions")

    port = 18789
    token = ""
    try:
        c = json.load(open(config_json))
        port = c.get("gateway", {}).get("port", c.get("port", 18789))
        token = c.get("gateway", {}).get("auth", {}).get("token", "")
    except:
        pass

    gateways.append({
        "name": name,
        "configDir": config_dir,
        "sessionsDir": sessions_dir,
        "port": port,
        "token": token,
    })

# Check for mem
mem_path = ""
for candidate in [
    subprocess.run(["which", "mem"], capture_output=True, text=True).stdout.strip(),
    os.path.expanduser("~/bin/mem"),
    os.path.expanduser("~/.npm-global/bin/mem"),
]:
    if candidate and os.path.isfile(candidate) and os.access(candidate, os.X_OK):
        mem_path = candidate
        break

config = {
    "gateways": gateways,
    "trimMaxKB": 250,
    "keepPairs": 10,
    "keepFullPairs": 2,
    "minArchivePairs": 5,
    "trimFullThresholdPct": 50,
    "archiveRetentionDays": 7,
    "orphanGraceMinutes": 30,
    "staleSubagentHours": 24,
    "staleCronSessionHours": 24,
    "llmExtraction": {
        "enabled": True,
        "maxPerRun": 1,
        "model": "openclaw",
        "maxInputChars": 20000,
        "timeoutSecs": 60,
        "maxMemories": 15,
        "minArchived": 3,
    },
    "memCli": {
        "enabled": bool(mem_path),
        "path": mem_path,
    },
    "stateFile": os.path.expanduser("~/.openclaw/session-janitor-state.json"),
    "watcherDebounceSecs": 3,
    "cronSchedule": "*/15 * * * *",
    "logFile": "/tmp/session-janitor.log",
}

json.dump(config, open(config_file, "w"), indent=2)
print(f"  Written to {config_file}")
PYEOF

echo ""

# --- Install cron ---
JANITOR_SCRIPT="$SKILL_DIR/scripts/janitor.sh"
CRON_SCHEDULE=$(python3 -c "import json; print(json.load(open('$CONFIG_FILE')).get('cronSchedule','*/15 * * * *'))")
LOG_FILE=$(python3 -c "import json; print(json.load(open('$CONFIG_FILE')).get('logFile','/tmp/session-janitor.log'))")

CRON_LINE="$CRON_SCHEDULE $JANITOR_SCRIPT >> $LOG_FILE 2>&1"

# Check if already installed
if crontab -l 2>/dev/null | grep -qF "session-janitor"; then
    echo "Updating existing cron entry..."
    crontab -l 2>/dev/null | grep -v "session-janitor" | { cat; echo "$CRON_LINE  # session-janitor"; } | crontab -
else
    echo "Installing cron entry..."
    (crontab -l 2>/dev/null; echo "$CRON_LINE  # session-janitor") | crontab -
fi

echo "  ✓ Cron installed: $CRON_SCHEDULE"
echo ""

# --- Install watcher service (systemd on Linux, launchd on macOS) ---
if [[ "$OS" == "Darwin" ]]; then
    PLIST_TEMPLATE="$SKILL_DIR/session-janitor-watcher.plist"
    LAUNCH_AGENTS_DIR="$HOME/Library/LaunchAgents"
    PLIST_LABEL="ai.openclaw.session-janitor-watcher"
    PLIST_DEST="$LAUNCH_AGENTS_DIR/${PLIST_LABEL}.plist"

    if [[ -f "$PLIST_TEMPLATE" ]]; then
        mkdir -p "$LAUNCH_AGENTS_DIR"
        sed "s|SKILL_DIR_PLACEHOLDER|$SKILL_DIR|g" "$PLIST_TEMPLATE" > "$PLIST_DEST"
        launchctl unload "$PLIST_DEST" 2>/dev/null || true
        launchctl load "$PLIST_DEST" 2>/dev/null && \
            echo "  ✓ Watcher LaunchAgent installed and started" || \
            echo "  ⚠ LaunchAgent load failed — check: launchctl list | grep session-janitor"
        echo "  Location: $PLIST_DEST"
        echo "  Stop:     launchctl unload \"$PLIST_DEST\""
        echo "  Start:    launchctl load \"$PLIST_DEST\""
    else
        echo "  ⚠ Plist template not found at $PLIST_TEMPLATE — skipping watcher service"
    fi
else
    # Linux — systemd user service
    SERVICE_TEMPLATE="$SKILL_DIR/session-janitor-watcher.service"
    SERVICE_DIR="$HOME/.config/systemd/user"
    SERVICE_DEST="$SERVICE_DIR/session-janitor-watcher.service"

    if [[ -f "$SERVICE_TEMPLATE" ]]; then
        mkdir -p "$SERVICE_DIR"
        sed "s|SKILL_DIR_PLACEHOLDER|$SKILL_DIR|g" "$SERVICE_TEMPLATE" > "$SERVICE_DEST"
        systemctl --user daemon-reload
        systemctl --user enable --now session-janitor-watcher.service 2>/dev/null && \
            echo "  ✓ Watcher service enabled and started" || \
            echo "  ⚠ Watcher service install failed — check: systemctl --user status session-janitor-watcher"
    else
        echo "  ⚠ Service template not found at $SERVICE_TEMPLATE — skipping watcher service"
    fi
fi

echo ""

# --- Verify ---
echo "=== Setup Complete ==="
echo ""
echo "Config:    $CONFIG_FILE"
echo "Script:    $JANITOR_SCRIPT"
echo "Log:       $LOG_FILE"
echo "Schedule:  $CRON_SCHEDULE"
echo ""
echo "Test with: bash $JANITOR_SCRIPT"
echo "Logs:      tail -f $LOG_FILE"
if [[ "$OS" == "Darwin" ]]; then
    echo "Watcher:   tail -f /tmp/session-janitor-watcher.log"
    echo "           launchctl list | grep session-janitor"
else
    echo "Watcher:   tail -f /tmp/session-janitor-watcher.log"
    echo "           systemctl --user status session-janitor-watcher"
fi
