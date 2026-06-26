#!/bin/bash

ACTION=$1
shift

CONFIG_FILE="${HOME}/.openclaw/openclaw.json"
HEARTBEAT_FILE="${OPENCLAW_WORKSPACE:-.}/HEARTBEAT.md"

if [ "$ACTION" == "on" ]; then
    TASK=""
    INTERVAL="3m"

    while [[ "$#" -gt 0 ]]; do
        case $1 in
            --task) TASK="$2"; shift ;;
            --every) INTERVAL="$2"; shift ;;
            *) echo "Unknown parameter: $1"; exit 1 ;;
        esac
        shift
    done

    if [ -z "$TASK" ]; then
        echo "Error: --task required for 'on' mode."
        exit 1
    fi

    echo "🏎️  Activating Sport Mode (Interval: $INTERVAL)..."
    
    # 1. Patch Config
    openclaw config set agents.defaults.heartbeat.every "$INTERVAL"
    
    # 2. Update HEARTBEAT.md
    cat > "$HEARTBEAT_FILE" <<EOF
# 🏎️ Sport Mode Active
Target: High-frequency monitoring ($INTERVAL)

## Task
$TASK

## Auto-Off
If the task is complete, run:
\`skills/sport-mode/scripts/sport-mode.sh off\`
EOF
    
    echo "✅ Heartbeat set to $INTERVAL. Task written to HEARTBEAT.md."

elif [ "$ACTION" == "off" ]; then
    echo "🐢 Deactivating Sport Mode..."
    
    # 1. Patch Config (Default Frequency)
    openclaw config set agents.defaults.heartbeat.every "30m"
    
    # 2. Clear HEARTBEAT.md
    echo "" > "$HEARTBEAT_FILE"
    
    echo "✅ Heartbeat reset to 30m. HEARTBEAT.md cleared."

else
    echo "Usage: $0 [on --task '...'] | [off]"
    exit 1
fi
