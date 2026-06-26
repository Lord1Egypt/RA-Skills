#!/usr/bin/env bash
set -euo pipefail

SRC_DIR="$(cd "$(dirname "$0")" && pwd)"
WORKDIR="${1:-$(pwd)}"

mkdir -p "$WORKDIR/tasks" "$WORKDIR/logs" "$WORKDIR/outputs" "$WORKDIR/scripts" "$WORKDIR/task-templates"

copy_if_missing() {
  local src="$1"
  local dst="$2"
  if [[ -e "$dst" ]]; then
    echo "skip existing: ${dst#$WORKDIR/}"
  else
    mkdir -p "$(dirname "$dst")"
    cp "$src" "$dst"
    echo "installed: ${dst#$WORKDIR/}"
  fi
}

for f in "$SRC_DIR/scripts"/*; do
  copy_if_missing "$f" "$WORKDIR/scripts/$(basename "$f")"
done
for f in "$SRC_DIR/task-templates"/*; do
  copy_if_missing "$f" "$WORKDIR/task-templates/$(basename "$f")"
done
copy_if_missing "$SRC_DIR/tasks/README.md" "$WORKDIR/tasks/README.md"

echo "task-ledger toolkit ready in: $WORKDIR"
