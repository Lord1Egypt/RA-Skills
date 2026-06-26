#!/usr/bin/env bash
set -euo pipefail

# ============================================================
# platform_registry.sh — Platform registry & capability discovery
# ============================================================
# Scans scripts/platform_*.sh, parses @manifest annotations,
# provides platform_list / platform_info / platform_load functions.
# ============================================================

# ----------------------------------------------------------
# platform_registry_dir — resolve the scripts directory
# ----------------------------------------------------------
_platform_registry_dir() {
  # If sourced, use BASH_SOURCE; if executed, use $0
  local src="${BASH_SOURCE[0]:-$0}"
  local dir="$(cd "$(dirname "$src")" && pwd)"
  echo "$dir"
}

# ----------------------------------------------------------
# platform_list
# Scans for platform_*.sh files and returns JSON array of
# platform names with labels.
# ----------------------------------------------------------
platform_list() {
  local scripts_dir
  scripts_dir=$(_platform_registry_dir)
  local platforms=()

  for f in "$scripts_dir"/platform_*.sh; do
    [[ -f "$f" ]] || continue
    local name label
    name=$(grep -m1 '^# @platform_name:' "$f" 2>/dev/null | sed 's/^# @platform_name:\s*//' | xargs) || true
    label=$(grep -m1 '^# @platform_label:' "$f" 2>/dev/null | sed 's/^# @platform_label:\s*//' | xargs) || true
    [[ -z "$name" ]] && continue
    platforms+=("{\"name\":\"$name\",\"label\":\"$label\"}")
  done

  local IFS=','
  echo "{\"module\":\"platform_registry\",\"platforms\":[${platforms[*]}]}"
}

# ----------------------------------------------------------
# platform_info <name>
# Returns full manifest metadata for a platform.
# ----------------------------------------------------------
platform_info() {
  local target_name="${1:?Usage: platform_info <name>}"
  local scripts_dir
  scripts_dir=$(_platform_registry_dir)
  local file="$scripts_dir/platform_${target_name}.sh"

  if [[ ! -f "$file" ]]; then
    echo "{\"module\":\"platform_registry\",\"status\":\"fail\",\"error\":\"Platform not found: $target_name\"}" >&2
    return 1
  fi

  # Parse all @manifest annotations
  local name label auth_method auth_check auth_hint upload_type upload_command
  local requires_bin install_hint supports_changelog supports_version

  name=$(grep -m1 '^# @platform_name:' "$file" 2>/dev/null | sed 's/^# @platform_name:\s*//' | xargs) || true
  label=$(grep -m1 '^# @platform_label:' "$file" 2>/dev/null | sed 's/^# @platform_label:\s*//' | xargs) || true
  auth_method=$(grep -m1 '^# @auth_method:' "$file" 2>/dev/null | sed 's/^# @auth_method:\s*//' | xargs) || true
  auth_check=$(grep -m1 '^# @auth_check:' "$file" 2>/dev/null | sed 's/^# @auth_check:\s*//' | xargs) || true
  auth_hint=$(grep -m1 '^# @auth_hint:' "$file" 2>/dev/null | sed 's/^# @auth_hint:\s*//' | xargs) || true
  upload_type=$(grep -m1 '^# @upload_type:' "$file" 2>/dev/null | sed 's/^# @upload_type:\s*//' | xargs) || true
  upload_command=$(grep -m1 '^# @upload_command:' "$file" 2>/dev/null | sed 's/^# @upload_command:\s*//' | xargs) || true
  requires_bin=$(grep -m1 '^# @requires_bin:' "$file" 2>/dev/null | sed 's/^# @requires_bin:\s*//' | xargs) || true
  install_hint=$(grep -m1 '^# @install_hint:' "$file" 2>/dev/null | sed 's/^# @install_hint:\s*//' | xargs) || true
  supports_changelog=$(grep -m1 '^# @supports_changelog:' "$file" 2>/dev/null | sed 's/^# @supports_changelog:\s*//' | xargs) || true
  supports_version=$(grep -m1 '^# @supports_version:' "$file" 2>/dev/null | sed 's/^# @supports_version:\s*//' | xargs) || true

  # Escape for JSON
  label=$(_pr_json_escape "$label")
  auth_hint=$(_pr_json_escape "$auth_hint")
  install_hint=$(_pr_json_escape "$install_hint")

  cat <<EOF
{
  "module": "platform_registry",
  "status": "ok",
  "platform": {
    "name": "$name",
    "label": "$label",
    "auth_method": "$auth_method",
    "auth_check": "$auth_check",
    "auth_hint": "$auth_hint",
    "upload_type": "$upload_type",
    "upload_command": "$upload_command",
    "requires_bin": "$requires_bin",
    "install_hint": "$install_hint",
    "supports_changelog": ${supports_changelog:-false},
    "supports_version": ${supports_version:-false}
  }
}
EOF
}

# ----------------------------------------------------------
# platform_load <name>
# Sources the platform adapter script, making its functions
# available in the caller's shell.
# ----------------------------------------------------------
platform_load() {
  local target_name="${1:?Usage: platform_load <name>}"
  local scripts_dir
  scripts_dir=$(_platform_registry_dir)
  local file="$scripts_dir/platform_${target_name}.sh"

  if [[ ! -f "$file" ]]; then
    echo "Platform adapter not found: $target_name" >&2
    return 1
  fi

  # shellcheck disable=SC1090
  source "$file"
}

# ----------------------------------------------------------
# _pr_json_escape <string>
# Minimal JSON string escaping.
# ----------------------------------------------------------
_pr_json_escape() {
  echo -n "$1" | sed 's/\\/\\\\/g; s/"/\\"/g; s/\t/\\t/g' | tr '\n' ' '
}

# ----------------------------------------------------------
# Allow direct execution for testing
# ----------------------------------------------------------
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
  cmd="${1:-list}"
  shift || true
  case "$cmd" in
    list) platform_list ;;
    info) platform_info "$@" ;;
    *)    echo "Unknown command: $cmd" >&2; exit 1 ;;
  esac
fi
