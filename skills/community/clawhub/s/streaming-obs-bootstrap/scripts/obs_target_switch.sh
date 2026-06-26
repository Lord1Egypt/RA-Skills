#!/usr/bin/env bash
set -euo pipefail

HOST="${1:-localhost}"
PORT="${2:-4455}"
DB="${AGENTIC_OBS_DB:-$HOME/.agentic-obs/db.sqlite}"

sqlite3 "$DB" "update config set value='$HOST', updated_at=datetime('now') where key='obs_host';"
sqlite3 "$DB" "update config set value='$PORT', updated_at=datetime('now') where key='obs_port';"

echo "Updated agentic-obs target to $HOST:$PORT"
mcporter call 'obs.get_obs_status()'
