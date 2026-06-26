#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
LOG_DIR="$ROOT/storage/logs"

for name in api web; do
  pid_file="$LOG_DIR/$name.pid"
  if [ -f "$pid_file" ] && kill -0 "$(cat "$pid_file")" 2>/dev/null; then
    echo "$name running: $(cat "$pid_file")"
  else
    echo "$name stopped"
  fi
done

echo "API: http://127.0.0.1:8000/api/health"
echo "Web: http://127.0.0.1:5173"
