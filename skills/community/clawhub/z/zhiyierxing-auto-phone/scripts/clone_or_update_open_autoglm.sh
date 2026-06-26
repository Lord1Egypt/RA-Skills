#!/usr/bin/env bash
set -euo pipefail

REPO_URL="https://github.com/zai-org/Open-AutoGLM.git"
TARGET_DIR="${1:-$PWD/Open-AutoGLM}"

if ! command -v git >/dev/null 2>&1; then
  echo "[error] git not found. Please install git first."
  exit 1
fi

if [ -d "$TARGET_DIR/.git" ]; then
  echo "[info] repo already exists, updating: $TARGET_DIR"
  git -C "$TARGET_DIR" pull --ff-only
else
  echo "[info] cloning repo to: $TARGET_DIR"
  git clone "$REPO_URL" "$TARGET_DIR"
fi

echo "[done] repo ready: $TARGET_DIR"
