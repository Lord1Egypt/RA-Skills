#!/usr/bin/env bash
set -euo pipefail

# ============================================================
# status.sh — Status check module
# ============================================================
# Displays skill name, version, description, and queries
# each registered platform for publish status.
# ============================================================

# Resolve script directory
_status_script_dir() {
  local src="${BASH_SOURCE[0]:-$0}"
  dirname "$(cd "$(dirname "$src")" && pwd)"
}

# ----------------------------------------------------------
# status_run <skill-path>
# Main entry. Outputs JSON summary to stdout.
# ----------------------------------------------------------
status_run() {
  local skill_path="${1:?Usage: status_run <skill-path>}"
  local script_dir
  script_dir=$(_status_script_dir)

  # Source version module
  # shellcheck disable=SC1090
  source "$script_dir/version.sh"

  # Extract basic info
  local skill_md="$skill_path/SKILL.md"
  if [[ ! -f "$skill_md" ]]; then
    _status_json "fail" "" "" "" "SKILL.md not found in $skill_path"
    return 1
  fi

  local name description version
  name=$(_status_extract_field "$skill_md" "name")
  description=$(_status_extract_field "$skill_md" "description")
  version=$(_version_extract "$skill_md") || true

  # Gather platform statuses
  local platform_results=()

  # Source platform registry
  # shellcheck disable=SC1090
  source "$script_dir/platform_registry.sh"

  # Get list of platforms
  local platform_names
  platform_names=$(_status_get_platform_names)

  for pname in $platform_names; do
    local pstatus
    pstatus=$(_status_query_platform "$pname" "$name") || true
    platform_results+=("$pstatus")
  done

  # Build JSON output
  local platforms_json
  if (( ${#platform_results[@]} > 0 )); then
    local IFS=','
    platforms_json="[${platform_results[*]}]"
  else
    platforms_json="[]"
  fi

  # Escape for JSON
  name=$(_st_json_escape "$name")
  description=$(_st_json_escape "$description")

  cat <<EOF
{
  "module": "status",
  "status": "ok",
  "skill": {
    "name": "$name",
    "version": "$version",
    "description": "$description",
    "path": "$skill_path"
  },
  "platforms": $platforms_json
}
EOF
}

# ============================================================
# Internal helpers
# ============================================================

_status_extract_field() {
  local file="$1"
  local field="$2"
  local in_fm=0 line_num=0 value=""
  while IFS= read -r line; do
    (( line_num++ )) || true
    if (( line_num == 1 )) && [[ "$line" == "---" ]]; then
      in_fm=1; continue
    fi
    if (( in_fm )); then
      [[ "$line" == "---" ]] && break
      if [[ "$line" =~ ^${field}:\ *(.*) ]]; then
        value="${BASH_REMATCH[1]}"
        value=$(echo "$value" | sed 's/^"\(.*\)"$/\1/' | xargs)
      fi
    fi
  done < "$file"
  echo "$value"
}

_status_get_platform_names() {
  local script_dir
  script_dir=$(_status_script_dir)
  for f in "$script_dir"/platform_*.sh; do
    [[ -f "$f" ]] || continue
    grep -m1 '^# @platform_name:' "$f" 2>/dev/null | sed 's/^# @platform_name:\s*//' | xargs || true
  done
}

_status_query_platform() {
  local pname="$1"
  local skill_name="$2"
  local script_dir
  script_dir=$(_status_script_dir)
  local file="$script_dir/platform_${pname}.sh"

  if [[ ! -f "$file" ]]; then
    echo "{\"platform\":\"$pname\",\"status\":\"adapter_not_found\"}"
    return 1
  fi

  # Source the adapter
  # shellcheck disable=SC1090
  source "$file"

  # Check if platform has status function
  if declare -f "platform_${pname}_status" &>/dev/null; then
    local result
    if result=$("platform_${pname}_status" "$skill_name" 2>&1); then
      echo "$result" | tr '\n' ' '
    else
      echo "{\"platform\":\"$pname\",\"status\":\"query_failed\"}"
    fi
  else
    echo "{\"platform\":\"$pname\",\"status\":\"not_supported\"}"
  fi
}

_st_json_escape() {
  echo -n "$1" | sed 's/\\/\\\\/g; s/"/\\"/g; s/\t/\\t/g' | tr '\n' ' '
}

_status_json() {
  local status="$1"
  local name="$2"
  local version="$3"
  local description="$4"
  local error="$5"

  if [[ -n "$error" ]]; then
    cat <<EOF
{
  "module": "status",
  "status": "$status",
  "error": "$error"
}
EOF
  else
    cat <<EOF
{
  "module": "status",
  "status": "$status",
  "name": "$name",
  "version": "$version",
  "description": "$description"
}
EOF
  fi
}

# ----------------------------------------------------------
# Allow direct execution
# ----------------------------------------------------------
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
  status_run "${1:?Usage: status.sh <skill-path>}"
fi
