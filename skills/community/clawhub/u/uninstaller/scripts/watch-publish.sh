#!/bin/bash
# watch-publish.sh — Monitor Publish Skills workflow via Wander
# Run from openclaw-uninstall repo. Requires Wander cloned (sibling or WANDER_DIR).

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
WANDER_DIR="${WANDER_HOME:-${WANDER_DIR:-$(dirname "$REPO_ROOT")/wander}}"

if [[ ! -f "$WANDER_DIR/watch-workflow-bg.sh" ]]; then
  echo "Wander not found at $WANDER_DIR"
  echo "Clone: git clone https://github.com/ERerGB/wander.git"
  echo "Or set WANDER_HOME=/path/to/wander (or WANDER_DIR)"
  exit 1
fi

cd "$REPO_ROOT"
# Use project workflow config for check_window and notifications
export WORKFLOW_REGISTRY_FILE="$REPO_ROOT/.workflows.yml"
exec "$WANDER_DIR/watch-workflow-bg.sh" publish.yml "$@"
