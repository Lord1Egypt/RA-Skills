#!/bin/bash
# watch-publish-detached.sh — Fully detached monitor for Publish Skills
# Closes terminal; logs to ~/.wander_logs/; macOS notification when done.

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
WANDER_DIR="${WANDER_HOME:-${WANDER_DIR:-$(dirname "$REPO_ROOT")/wander}}"

if [[ ! -f "$WANDER_DIR/watch-workflow-detached.sh" ]]; then
  echo "Wander not found at $WANDER_DIR"
  echo "Clone: git clone https://github.com/ERerGB/wander.git"
  echo "Or set WANDER_HOME=/path/to/wander (or WANDER_DIR)"
  exit 1
fi

cd "$REPO_ROOT"
export WORKFLOW_REGISTRY_FILE="$REPO_ROOT/.workflows.yml"
exec "$WANDER_DIR/watch-workflow-detached.sh" publish.yml "$@"
