#!/usr/bin/env bash
# shellbot-creative-studio — shared configuration
# Source this file at the top of every script.

CREATIVE_STUDIO_VERSION="1.0.0"
DEFAULT_OUTPUT_DIR="./creative-output"
TASK_LOG_FILE=".creative-tasks.jsonl"

_LIB_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(cd "${_LIB_DIR}/../.." && pwd)"
TEMPLATES_DIR="${SKILL_DIR}/assets/templates"

# Ensure structured output directories exist
ensure_output_dirs() {
  local base="${1:-$DEFAULT_OUTPUT_DIR}"
  mkdir -p "${base}"/{assets,scenes,audio,final,manifests}
}

# Resolve output path: use --output if given, else default location
resolve_output() {
  local output="$1"
  local default_dir="$2"
  local default_name="$3"
  if [[ -n "$output" ]]; then
    echo "$output"
  else
    ensure_output_dirs "$default_dir"
    echo "${default_dir}/${default_name}"
  fi
}
