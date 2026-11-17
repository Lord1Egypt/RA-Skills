#!/usr/bin/env bash
# Resolve smart-commit.host-agent.json for the skill copy the host actually loaded.
# Always uses the smart-git/ directory that contains this script, unless
# SMART_GIT_CONFIG points at another file. Does not relocate to another
# tool's copy (including Cursor / Claude Code / Codex).
# stdout: absolute path to config file; stderr: selection notes/errors; exit 0 on success.

set -euo pipefail

CONFIG_NAME="smart-commit.host-agent.json"
SKILL_DIR_NAME="smart-git"

# Explicit override for troubleshooting, CI, or temporary one-off runs.
if [[ -n "${SMART_GIT_CONFIG:-}" ]]; then
  if [[ -f "${SMART_GIT_CONFIG}" ]]; then
    echo "Using SMART_GIT_CONFIG override: ${SMART_GIT_CONFIG}" >&2
    echo "${SMART_GIT_CONFIG}"
    exit 0
  fi

  echo "SMART_GIT_CONFIG points at a file that does not exist: ${SMART_GIT_CONFIG}" >&2
  exit 1
fi

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
loaded_skill_dir="$(cd "${script_dir}/.." && pwd)"

if [[ "$(basename "${loaded_skill_dir}")" != "${SKILL_DIR_NAME}" ]]; then
  cat >&2 <<EOF
This resolve script is not under ${SKILL_DIR_NAME}/scripts/, so colocated config cannot be resolved safely.

Script path: ${BASH_SOURCE[0]}
Call the installed ${SKILL_DIR_NAME}/scripts/resolve-config.sh, or set SMART_GIT_CONFIG to point at a config file explicitly.
EOF
  exit 1
fi

config_path="${loaded_skill_dir}/${CONFIG_NAME}"

if [[ ! -f "${config_path}" ]]; then
  cat >&2 <<EOF
Colocated smart-git config file not found: ${config_path}

Confirm the ${SKILL_DIR_NAME}/ directory loaded this turn is complete, and that ${CONFIG_NAME} sits next to SKILL.md.
This script will not switch to a copy in another directory.
EOF
  exit 1
fi

if [[ ! -r "${config_path}" ]]; then
  echo "smart-git config file is not readable: ${config_path}" >&2
  exit 1
fi

echo "${config_path}"
