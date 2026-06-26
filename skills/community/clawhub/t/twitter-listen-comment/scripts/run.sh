#!/bin/sh
set -eu
SCRIPT_DIR="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
CONFIG_PATH="${1:-$SKILL_DIR/references/config.json}"
exec python3 "$SCRIPT_DIR/twitter_listen_comment.py" --config "$CONFIG_PATH"
