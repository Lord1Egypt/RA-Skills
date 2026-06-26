#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="${1:-}"
TARGET_BRANCH="${2:-feat/test}"
SUMMARY_FILE="${3:-}"
TIMESTAMP="$(date '+%Y%m%d-%H%M%S')"
COMMIT_MSG="chore: 官网需求变更-${TIMESTAMP}"

if [[ -z "$PROJECT_DIR" ]]; then
  echo "Usage: $0 <project-dir> [branch] [summary-file]" >&2
  exit 2
fi

cd "$PROJECT_DIR"

if [[ "$(git branch --show-current)" != "$TARGET_BRANCH" ]]; then
  echo "Not on $TARGET_BRANCH" >&2
  exit 1
fi

if [[ -z "$(git status --porcelain)" ]]; then
  echo "No changes to commit."
  exit 0
fi

git add -A
git commit -m "$COMMIT_MSG"
git push origin "$TARGET_BRANCH"

NOTICE_ARGS=(--project-dir "$PROJECT_DIR" --branch "$TARGET_BRANCH" --commit-ref HEAD)
if [[ -n "$SUMMARY_FILE" ]]; then
  NOTICE_ARGS+=(--summary-file "$SUMMARY_FILE")
fi
python3 "$SCRIPT_DIR/push_wecom_push_notice.py" "${NOTICE_ARGS[@]}"

echo "PROJECT_DIR=$PROJECT_DIR"
echo "COMMIT_MSG=$COMMIT_MSG"
