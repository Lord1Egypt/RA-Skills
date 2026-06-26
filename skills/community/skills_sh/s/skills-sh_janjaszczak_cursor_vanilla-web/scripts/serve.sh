#!/usr/bin/env bash
# .cursor/skills/vanilla-web/scripts/serve.sh
set -euo pipefail
PORT="${1:-8000}"
python3 -m http.server "$PORT"
