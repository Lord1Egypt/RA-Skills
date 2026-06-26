#!/bin/bash
# slack-standup v1.0.0
set -e

SLACK_TOKEN="${SLACK_BOT_TOKEN:-}"
CHANNEL_ID="${SLACK_CHANNEL_ID:-}"

log_info() { echo "[INFO] $1"; }
log_error() { echo "[ERROR] $1"; }

check_prereqs() {
    [ -z "$SLACK_TOKEN" ] && log_error "SLACK_BOT_TOKEN not set" && exit 1
    log_info "Prerequisites checked"
}

send_prompt() {
    msg='{"channel":"'"$CHANNEL_ID"'","text":"🎯 *Daily Standup*\nUpdates:\n• Yesterday?\n• Today?\n• Blockers?","as_user":true}'
    curl -s -X POST -H "Authorization: Bearer $SLACK_TOKEN" -H "Content-Type: application/json" -d "$msg" https://slack.com/api/chat.postMessage
    log_info "Prompt sent"
}

case "$1" in
    prompt) check_prereqs; send_prompt ;;
    test) log_info "Test mode..."; check_prereqs; send_prompt ;;
    *) echo "Usage: $0 {prompt|test}" ;;
esac