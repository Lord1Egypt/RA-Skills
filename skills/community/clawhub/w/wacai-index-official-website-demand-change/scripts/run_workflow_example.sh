#!/usr/bin/env bash
set -euo pipefail

SKILL_DIR="/Users/dyshi/.openclaw/workspace/skills/index-official-website-demand-change"
PROJECT_DIR="${1:-}"
TARGET_BRANCH="${2:-feat/test}"

if [[ -z "$PROJECT_DIR" ]]; then
  echo "Usage: $0 <project-dir> [branch]" >&2
  exit 2
fi

echo "Step 1: ensure repo is clean and sync branch"
bash "$SKILL_DIR/scripts/git_prepare_branch.sh" "$PROJECT_DIR" "$TARGET_BRANCH"

echo
echo "Step 2: paste demand content, then Ctrl-D"
python3 "$SKILL_DIR/scripts/save_product_demand.py" --project-dir "$PROJECT_DIR" --stdin

echo
echo "Step 3: run the coding subagent from OpenClaw, using productdemand.md as the source of truth"
echo "Step 4: after code changes finish, run:"
echo "bash $SKILL_DIR/scripts/git_commit_and_push.sh '$PROJECT_DIR' '$TARGET_BRANCH'"
