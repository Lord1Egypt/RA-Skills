#!/usr/bin/env bash
# Discover the colocated resolve-config.sh for the skill copy the host actually loaded.
# Always uses the smart-git/ directory that contains this script.
# Does not relocate to another tool's copy (including Cursor / Claude Code / Codex).
# stdout: absolute path to resolve-config.sh; stderr: selection notes/errors; exit 0 on success.

set -euo pipefail

SKILL_DIR_NAME="smart-git"
SCRIPT_NAME="resolve-config.sh"

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
loaded_skill_dir="$(cd "${script_dir}/.." && pwd)"

if [[ "$(basename "${loaded_skill_dir}")" != "${SKILL_DIR_NAME}" ]]; then
  cat >&2 <<EOF
This discover script is not under ${SKILL_DIR_NAME}/scripts/, so colocated config cannot be resolved safely.

Script path: ${BASH_SOURCE[0]}
Call the installed ${SKILL_DIR_NAME}/scripts/discover-resolve-script.sh, or set SMART_GIT_CONFIG to point at a config file explicitly.
EOF
  exit 1
fi

resolve_script="${loaded_skill_dir}/scripts/${SCRIPT_NAME}"

if [[ ! -f "${resolve_script}" ]]; then
  cat >&2 <<EOF
Colocated resolve script not found: ${resolve_script}

Confirm the ${SKILL_DIR_NAME}/ directory loaded this turn is complete and contains scripts/${SCRIPT_NAME}.
EOF
  exit 1
fi

if [[ ! -r "${resolve_script}" ]]; then
  echo "Resolve script is not readable: ${resolve_script}" >&2
  exit 1
fi

echo "Using the colocated resolve script from the skill copy loaded this turn: ${resolve_script}" >&2
echo "${resolve_script}"
