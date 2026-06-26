#!/bin/bash
# Reboot Alert — runs at boot via cron
# Sends Telegram alert via Bot API using dedicated config file
#
# SETUP: Create config with your credentials (one-time):
#   cat > ~/.rr-reboot-config << 'EOF'
#   BOT_TOKEN=your_bot_token_here
#   CHAT_ID=your_chat_id_here
#   EOF
#   chmod 600 ~/.rr-reboot-config

SKILL_DIR="$(cd "$(dirname "$0")" && pwd)"
CONFIG_FILE="$HOME/.rr-reboot-config"

RESULT=$(bash "$SKILL_DIR/check-reboot.sh" 2>&1)

if echo "$RESULT" | grep -q "REBOOTED"; then
    BOOT_TIME=$(echo "$RESULT" | grep -oP 'at \K.*')
    MESSAGE="🔄 System rebooted at $BOOT_TIME — RR-RebootReport"

    # Load credentials from dedicated config
    BOT_TOKEN=$(grep "^BOT_TOKEN=" "$CONFIG_FILE" 2>/dev/null | cut -d= -f2)
    CHAT_ID=$(grep "^CHAT_ID=" "$CONFIG_FILE" 2>/dev/null | cut -d= -f2)

    [ -z "$BOT_TOKEN" ] || [ -z "$CHAT_ID" ] && exit 1

    # Wait for network
    for i in $(seq 1 10); do
        curl -s --connect-timeout 3 https://api.telegram.org > /dev/null 2>&1 && break
        sleep 3
    done

    # Send alert
    curl -s --connect-timeout 10 --max-time 15 \
        "https://api.telegram.org/bot${BOT_TOKEN}/sendMessage" \
        -d chat_id="$CHAT_ID" \
        -d text="$MESSAGE" > /dev/null 2>&1

    # Reset state
    bash "$SKILL_DIR/check-reboot.sh" --reset 2>/dev/null
fi
