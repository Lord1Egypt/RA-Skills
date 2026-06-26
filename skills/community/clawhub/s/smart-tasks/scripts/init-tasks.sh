#!/bin/sh
# init-tasks.sh — Initialize the tasks/ directory structure.
# Idempotent: skips existing files/directories.
# Usage: bash skills/smart-tasks/scripts/init-tasks.sh [workspace_root]

set -e

WORKSPACE="${1:-.}"
TASKS_DIR="$WORKSPACE/tasks"

echo "Initializing task system in $TASKS_DIR ..."

# Create directories
for dir in "$TASKS_DIR" "$TASKS_DIR/active" "$TASKS_DIR/done" "$TASKS_DIR/archive"; do
  if [ ! -d "$dir" ]; then
    mkdir -p "$dir"
    echo "  Created: $dir"
  else
    echo "  Exists:  $dir (skipped)"
  fi
done

# Create .meta.json
META_FILE="$TASKS_DIR/.meta.json"
if [ ! -f "$META_FILE" ]; then
  TODAY=$(date +%Y-%m-%d)
  cat > "$META_FILE" << EOF
{
  "nextId": 1,
  "created": "$TODAY",
  "categories": []
}
EOF
  echo "  Created: $META_FILE"
else
  echo "  Exists:  $META_FILE (skipped)"
fi

# Create INDEX.md
INDEX_FILE="$TASKS_DIR/INDEX.md"
if [ ! -f "$INDEX_FILE" ]; then
  TODAY=$(date +%Y-%m-%d)
  cat > "$INDEX_FILE" << EOF
# Tasks Index

> Last updated: $TODAY
> Active: 0 | Overdue: 0 | Due this week: 0

## 🔴 Overdue

_None_

## 🟡 Due This Week

_None_

## 📋 Later

_None_

## 📊 Summary

Task system initialized. Add your first task!
EOF
  echo "  Created: $INDEX_FILE"
else
  echo "  Exists:  $INDEX_FILE (skipped)"
fi

echo "Done. Task system ready."
