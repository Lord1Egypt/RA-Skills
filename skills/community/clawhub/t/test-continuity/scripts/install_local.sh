#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 1 || $# -gt 2 ]]; then
  echo "Usage: bash scripts/install_local.sh /path/to/openclaw-workspace/skills [link|copy]"
  exit 1
fi

TARGET_SKILLS_DIR="$1"
MODE="${2:-link}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PACKAGE_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"
TARGET_PATH="${TARGET_SKILLS_DIR%/}/personal-hooks"
PACKAGE_REAL="$(cd "$PACKAGE_DIR" && pwd -P)"

mkdir -p "$TARGET_SKILLS_DIR"
TARGET_SKILLS_REAL="$(cd "$TARGET_SKILLS_DIR" && pwd -P)"

if [[ "$TARGET_SKILLS_REAL" == "$PACKAGE_REAL" || "$TARGET_SKILLS_REAL" == "$PACKAGE_REAL/"* ]]; then
  echo "Refusing to install into the package source tree: $TARGET_SKILLS_REAL"
  exit 1
fi

case "$MODE" in
  link)
    if [[ -e "$TARGET_PATH" && ! -L "$TARGET_PATH" ]]; then
      echo "Refusing to replace existing non-symlink target: $TARGET_PATH"
      exit 1
    fi
    rm -f "$TARGET_PATH"
    ln -s "$PACKAGE_DIR" "$TARGET_PATH"
    ;;
  copy)
    if [[ -e "$TARGET_PATH" ]]; then
      echo "Refusing to overwrite existing target: $TARGET_PATH"
      exit 1
    fi
    cp -R "$PACKAGE_DIR" "$TARGET_PATH"
    ;;
  *)
    echo "Unknown mode: $MODE"
    echo "Use: link | copy"
    exit 1
    ;;
esac

cat <<EOF
Installed personal-hooks to:
  $TARGET_PATH

Suggested next steps:
  python3 $TARGET_PATH/scripts/personal_hooks.py init
  python3 $TARGET_PATH/scripts/personal_hooks.py capability-state-show

Suggested settings starting point:
  $TARGET_PATH/examples/settings.sample.json

If you want a custom writable settings path, set:
  PERSONAL_HOOKS_SETTINGS_PATH=/path/to/settings.json

This helper does not modify channel delivery, credentials, or live state.
EOF
