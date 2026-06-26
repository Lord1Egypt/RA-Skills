#!/usr/bin/env bash
# Environment helper for xiaomi-mimo-tts
# Sets SKILL_HOME to the parent directory of this scripts/ folder unless overridden

# Allow override
: "${SKILL_HOME:=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)}"

# Prefer XIAOMI_API_KEY, fall back to MIMO_API_KEY for compatibility
if [ -z "${XIAOMI_API_KEY}" ] && [ -n "${MIMO_API_KEY}" ]; then
  export XIAOMI_API_KEY="${MIMO_API_KEY}"
fi

export SKILL_HOME

# Default output directory for generated audio files (can be overridden by SKILL_OUT)
: "${SKILL_OUT:=$SKILL_HOME/out}"
mkdir -p "$SKILL_OUT"
export SKILL_OUT

# Reminder for agents/scripts: generated audio files are temporary artifacts.
# Agents/users should remove files in $SKILL_OUT when finished. Example:
#   rm -f "$SKILL_OUT"/*.ogg

# Helper: resolve a script path relative to SKILL_HOME
skill_path() {
  echo "$SKILL_HOME/$1"
}
