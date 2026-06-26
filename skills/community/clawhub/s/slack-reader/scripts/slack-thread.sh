#!/bin/bash
# Slack Thread/Channel/Reply Reader
# Fetches conversation history from a Slack link or channel ID.
#
# Usage:
#   ./slack-thread.sh https://...slack.com/archives/CHANNEL                          # channel history
#   ./slack-thread.sh https://...slack.com/archives/CHANNEL/pTS                      # full thread
#   ./slack-thread.sh https://...slack.com/archives/CHANNEL/pTS?thread_ts=...        # single reply
#   ./slack-thread.sh <channel-id> [--with-threads] [--limit N] [--desc]
#
# Output: [ISO-time|ts] username: message text (one per line, ascending order)

set -euo pipefail

CONFIG_FILE="$HOME/.openclaw/openclaw.json"

exec python3 "$(dirname "$0")/slack-thread.py" "$@"
