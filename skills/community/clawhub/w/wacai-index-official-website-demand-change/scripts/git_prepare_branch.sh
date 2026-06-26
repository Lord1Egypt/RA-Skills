#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="${1:-}"
TARGET_BRANCH="${2:-feat/test}"

if [[ -z "$PROJECT_DIR" ]]; then
  echo "Usage: $0 <project-dir> [branch]" >&2
  exit 2
fi

cd "$PROJECT_DIR"

if [[ -n "$(git status --porcelain)" ]]; then
  echo "Working tree is dirty. Commit, stash, or clean these files first:" >&2
  git status --short >&2
  exit 2
fi

echo "[1/3] fetch origin"
git fetch origin

echo "[2/3] checkout $TARGET_BRANCH"
git checkout "$TARGET_BRANCH"

echo "[3/3] pull --ff-only origin/$TARGET_BRANCH"
git pull --ff-only origin "$TARGET_BRANCH"

CURRENT_BRANCH="$(git branch --show-current)"
if [[ "$CURRENT_BRANCH" != "$TARGET_BRANCH" ]]; then
  echo "Expected branch $TARGET_BRANCH but got $CURRENT_BRANCH" >&2
  exit 3
fi

echo "PROJECT_DIR=$PROJECT_DIR"
echo "CURRENT_BRANCH=$CURRENT_BRANCH"
git status --short --branch
