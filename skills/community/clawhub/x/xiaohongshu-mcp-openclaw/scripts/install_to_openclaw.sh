#!/usr/bin/env bash
set -euo pipefail

BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SKILL_NAME="$(basename "$BASE_DIR")"
TARGET_ROOT="${1:-$HOME/.openclaw/workspace/skills}"
TARGET_DIR="$TARGET_ROOT/$SKILL_NAME"
SYNC_AGENTS_SKILL="${XHS_SYNC_AGENTS_SKILL:-1}"
AGENTS_ROOT="${XHS_AGENTS_SKILLS_ROOT:-$HOME/.agents/skills}"
AGENTS_DIR="${XHS_AGENTS_SKILL_DIR:-$AGENTS_ROOT/${SKILL_NAME}-1.0.0}"

if [ -z "$SKILL_NAME" ] || [ "$SKILL_NAME" = "/" ]; then
  echo "[ERROR] invalid skill name resolved from: $BASE_DIR"
  exit 1
fi

copy_skill() {
  local dst="$1"
  (
    set -e
    mkdir -p "$(dirname "$dst")"
    rm -rf "$dst"
    cp -R "$BASE_DIR" "$dst"
    rm -rf "$dst/.git" || true
    rm -rf "$dst/dist" || true
    find "$dst" -type d -name "__pycache__" -prune -exec rm -rf {} +
    find "$dst" -name ".DS_Store" -delete
  )
}

mkdir -p "$TARGET_ROOT"
copy_skill "$TARGET_DIR"

echo "[OK] Installed skill to: $TARGET_DIR"

if command -v openclaw >/dev/null 2>&1; then
  echo "[INFO] OpenClaw skill info:"
  openclaw skills info "$SKILL_NAME" || true
fi

if [ "$SYNC_AGENTS_SKILL" = "1" ]; then
  if [ -d "$AGENTS_ROOT" ] && [ ! -w "$AGENTS_ROOT" ]; then
    echo "[WARN] $AGENTS_ROOT is not writable, skip persistent copy sync"
  elif [ -e "$AGENTS_DIR" ] && [ ! -w "$AGENTS_DIR" ]; then
    echo "[WARN] $AGENTS_DIR is not writable, skip persistent copy sync"
  elif mkdir -p "$AGENTS_ROOT" >/dev/null 2>&1; then
    set +e
    copy_skill "$AGENTS_DIR"
    SYNC_RC=$?
    set -e
    if [ "$SYNC_RC" -eq 0 ]; then
      echo "[OK] Synced persistent copy to: $AGENTS_DIR"
    else
      echo "[WARN] failed to sync persistent copy to: $AGENTS_DIR"
      echo "[WARN] fallback: set XHS_SYNC_AGENTS_SKILL=0 or sync manually later"
    fi
  else
    echo "[WARN] failed to create $AGENTS_ROOT, skip persistent copy sync"
  fi
fi
