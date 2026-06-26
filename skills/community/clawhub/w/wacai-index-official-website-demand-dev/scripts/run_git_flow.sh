#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="${1:-}"
BRANCH="${2:-feat/test}"
SUMMARY_FILE="${3:-}"
shift 3 || true

if [[ -z "$PROJECT_DIR" || "$#" -eq 0 ]]; then
  echo "Usage: $0 <project-dir> <branch> <summary-file> <file1> [file2 ...]" >&2
  exit 2
fi

cd "$PROJECT_DIR"

git fetch origin
git checkout "$BRANCH"
git pull --ff-only origin "$BRANCH"

git add "$@"

STAMP="$(date '+%Y%m%d-%H%M%S')"
MSG="chore: 官网需求变更-${STAMP}"

git commit -m "$MSG"
git push origin "$BRANCH"

NOTICE_ARGS=(--project-dir "$PROJECT_DIR" --branch "$BRANCH" --commit-ref HEAD)
if [[ -n "$SUMMARY_FILE" ]]; then
  NOTICE_ARGS+=(--summary-file "$SUMMARY_FILE")
fi
python3 "$SCRIPT_DIR/push_wecom_push_notice.py" "${NOTICE_ARGS[@]}"

echo "PROJECT_DIR=$PROJECT_DIR"
echo "COMMIT_MESSAGE=$MSG"
echo "COMMIT_HASH=$(git rev-parse HEAD)"
