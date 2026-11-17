#!/usr/bin/env sh
set -eu

SOURCE_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
TARGET_DIR=${1:-${SUNO_CN_SKILL_DIR:-}}
if [ -z "$TARGET_DIR" ]; then
  echo 'Usage: ./install.sh "/absolute/agent/skill/directory"' >&2
  echo "Determine the official Skill directory for the current Agent before installing." >&2
  exit 2
fi
mkdir -p "$TARGET_DIR"
cp -R "$SOURCE_DIR"/. "$TARGET_DIR"/
chmod 755 "$TARGET_DIR/scripts/suno-client.mjs"
echo "suno-cn-music installed. Reload skills or restart the current Agent."
