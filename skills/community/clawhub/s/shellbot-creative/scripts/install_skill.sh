#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
SKILL_NAME="$(basename "$SKILL_DIR")"

if [[ -n "${OPENCLAW_SKILLS_DIR:-}" ]]; then
  DEFAULT_TARGET="$OPENCLAW_SKILLS_DIR"
elif [[ -n "${OPENCLAW_HOME:-}" ]]; then
  DEFAULT_TARGET="$OPENCLAW_HOME/skills"
else
  DEFAULT_TARGET="$HOME/.openclaw/skills"
fi

TARGET_DIR="$DEFAULT_TARGET"
FORCE=false

while [[ $# -gt 0 ]]; do
  case "$1" in
    --target)
      TARGET_DIR="$2"
      shift 2
      ;;
    --force)
      FORCE=true
      shift
      ;;
    *)
      echo "Unknown argument: $1" >&2
      echo "Usage: $0 [--target <skills_dir>] [--force]" >&2
      exit 1
      ;;
  esac
done

DEST="$TARGET_DIR/$SKILL_NAME"
mkdir -p "$TARGET_DIR"

if [[ -e "$DEST" && "$FORCE" != true ]]; then
  echo "Destination already exists: $DEST" >&2
  echo "Re-run with --force to replace it." >&2
  exit 2
fi

if [[ -e "$DEST" && "$FORCE" == true ]]; then
  rm -rf "$DEST"
fi

cp -R "$SKILL_DIR" "$DEST"
rm -rf "$DEST/scripts/__pycache__" "$DEST/dist"

echo "$DEST"
