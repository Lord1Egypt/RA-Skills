#!/bin/bash
# 🌐 Travel Lobster - Self-scheduling travel loop
# Usage: bash travel.sh <chat_id> [channel] [min_interval] [max_interval]
# Example: bash travel.sh chat:oc_abc123 feishu 10 30

# Ensure openclaw is in PATH (crontab/watchdog has minimal PATH)
# Add pnpm, nvm node, and standard paths for crontab compatibility
NVM_NODE=$(ls -d "$HOME/.nvm/versions/node"/*/bin 2>/dev/null | sort -V | tail -1)
export PATH="${NVM_NODE:+$NVM_NODE:}$HOME/.local/share/pnpm:$HOME/.local/bin:/usr/local/bin:/usr/bin:/bin:$PATH"

set -e

SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
CONFIG="$SKILL_DIR/.travel-config"

if [ ! -f "$CONFIG" ]; then
    echo "Error: Run setup.sh first!" >&2
    exit 1
fi

source "$CONFIG"

CHAT_ID="${1:-${TRAVEL_CHAT_ID}}"
CHANNEL="${2:-${TRAVEL_CHANNEL:-feishu}}"
MIN_INTERVAL="${3:-10}"
MAX_INTERVAL="${4:-30}"

if [ -z "$CHAT_ID" ]; then
    echo "Error: No chat ID. Usage: bash travel.sh <chat_id> [channel]" >&2
    exit 1
fi

# Validate interval params are numbers
if ! [[ "$MIN_INTERVAL" =~ ^[0-9]+$ ]] || ! [[ "$MAX_INTERVAL" =~ ^[0-9]+$ ]]; then
    echo "Error: Intervals must be positive integers" >&2
    exit 1
fi

# Save chat config (overwrite to prevent bloat)
{
    echo "AGENT_NAME=\"$AGENT_NAME\""
    echo "USER_NAME=\"$USER_NAME\""
    echo "USER_TZ=\"$USER_TZ\""
    echo "WORKSPACE=\"$WORKSPACE\""
    echo "JOURNAL=\"$JOURNAL\""
    echo "SKILL_DIR=\"$SKILL_DIR\""
    echo "TRAVEL_CHAT_ID=\"$CHAT_ID\""
    echo "TRAVEL_CHANNEL=\"$CHANNEL\""
    echo "TRAVEL_MIN_INTERVAL=\"$MIN_INTERVAL\""
    echo "TRAVEL_MAX_INTERVAL=\"$MAX_INTERVAL\""
    echo "USER_LANG=\"$USER_LANG\""
} > "$CONFIG"

LOGFILE="$WORKSPACE/logs/travel-lobster.log"
mkdir -p "$(dirname "$LOGFILE")"
RANGE=$((MAX_INTERVAL - MIN_INTERVAL + 1))
NEXT_MIN=$((RANDOM % RANGE + MIN_INTERVAL))

echo "$(date -u '+%Y-%m-%d %H:%M:%S UTC') 🌐 Next trip in ${NEXT_MIN}m → $CHAT_ID ($CHANNEL)" >> "$LOGFILE"

# Remove old job if exists
openclaw cron rm travel-next 2>/dev/null || true

# Read and fill the prompt template using envsubst (safe against special chars)
PROMPT_FILE="$SKILL_DIR/references/travel-prompt.md"
if [ ! -f "$PROMPT_FILE" ]; then
    echo "Error: Missing $PROMPT_FILE" >&2
    exit 1
fi

# Generate the prompt into a temp file to avoid shell quoting issues
PROMPT_TMP=$(mktemp)
trap "rm -f $PROMPT_TMP" EXIT

# Calculate next postcard number from journal
if [ -f "$JOURNAL" ]; then
    LAST_NUM=$(grep -oP '### #(\d+)' "$JOURNAL" | grep -oP '\d+' | sort -n | tail -1)
    NEXT_POSTCARD_NUM=$((${LAST_NUM:-0} + 1))
else
    NEXT_POSTCARD_NUM=1
fi
export NEXT_POSTCARD_NUM

export AGENT_NAME USER_NAME USER_TZ USER_LANG CHAT_ID CHANNEL WORKSPACE JOURNAL SKILL_DIR NEXT_POSTCARD_NUM
envsubst '${AGENT_NAME} ${USER_NAME} ${USER_TZ} ${USER_LANG} ${CHAT_ID} ${CHANNEL} ${WORKSPACE} ${JOURNAL} ${SKILL_DIR} ${NEXT_POSTCARD_NUM}' < "$PROMPT_FILE" > "$PROMPT_TMP"

# Use process substitution to safely pass multi-line, quote-containing prompts
PROMPT=$(cat "$PROMPT_TMP")

openclaw cron add \
    --name "travel-next" \
    --at "${NEXT_MIN}m" \
    --delete-after-run \
    --session isolated \
    --model "openrouter/google/gemini-3.1-pro-preview" \
    --timeout-seconds 300 \
    --no-deliver \
    --message "$PROMPT" \
    2>> "$LOGFILE"

rm -f "$PROMPT_TMP"

echo "$(date -u '+%Y-%m-%d %H:%M:%S UTC') ✅ Scheduled in ${NEXT_MIN}m" >> "$LOGFILE"
