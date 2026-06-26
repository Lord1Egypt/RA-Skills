#!/bin/bash
# QuickBooks CLI helper script
# Usage: ~/skills/qb-cli/run.sh customer list
# Usage: ~/skills/qb-cli/run.sh invoice get 123
# Usage: ~/skills/qb-cli/run.sh auth login --print-url

set -euo pipefail

SKILL_DIR="$(cd "$(dirname "$0")" && pwd)"

# Load .env if it exists
if [ -f "$SKILL_DIR/.env" ]; then
    set -a
    source "$SKILL_DIR/.env"
    set +a
fi

# Use sg docker wrapper if docker socket isn't accessible directly
if docker info >/dev/null 2>&1; then
    exec docker compose -f "$SKILL_DIR/docker-compose.yml" run --rm qb "$@"
else
    exec sg docker -c "docker compose -f \"$SKILL_DIR/docker-compose.yml\" run --rm qb $*"
fi
