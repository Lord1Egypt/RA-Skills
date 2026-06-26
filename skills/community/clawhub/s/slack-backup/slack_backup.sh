#!/bin/bash
# slack_backup.sh — Download files from a Slack channel and save to backup directory.
#
# Basic usage (download latest file):
#   ./slack_backup.sh
#
# Smart-matching usage (agent sets env vars based on user intent):
#   LIMIT=2 ./slack_backup.sh                           # latest 2 files
#   NAME_PREFIX=report ./slack_backup.sh                # files starting with "report"
#   MINUTES=5 FILE_TYPE=pdf ./slack_backup.sh           # PDFs from the last 5 minutes
#   LIMIT=3 MINUTES=10 ./slack_backup.sh                # up to 3 files from the last 10 minutes

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DOWNLOADER="$SCRIPT_DIR/../shared/slack_downloader.py"
BACKUP_DIR="${BACKUP_DIR:-$HOME/.openclaw/doc/backup}"

mkdir -p "$BACKUP_DIR"

source "$SCRIPT_DIR/../shared/slack_args.sh"

python3 "$DOWNLOADER" "${SLACK_ARGS[@]}" "$BACKUP_DIR"
