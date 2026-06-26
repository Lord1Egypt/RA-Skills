#!/usr/bin/env bash
set -euo pipefail

# ============================================================
# validate.sh — Skill validation module
# ============================================================
# Checks: SKILL.md exists, frontmatter valid, name/description
# non-empty, description ≤ 160 chars, no sensitive keywords,
# file structure norms.
# ============================================================

# Sensitive keywords that must not appear in skill files
SENSITIVE_KEYWORDS=(
  "secret"
  "token"
  "password"
  "api_key"
  "api-key"
  "apikey"
  "private_key"
  "private-key"
  "access_token"
  "access-token"
  "auth_token"
  "auth-token"
  "credential"
)

# ----------------------------------------------------------
# validate_run <skill-path>
# Main entry. Returns JSON to stdout, errors to stderr.
# Exit 0 on success, 1 on failure.
# ----------------------------------------------------------
validate_run() {
  local skill_path="${1:?Usage: validate_run <skill-path>}"
  local errors=()
  local warnings=()

  # --- Check directory exists ---
  if [[ ! -d "$skill_path" ]]; then
    _validate_json "fail" "" "" "Skill directory not found: $skill_path"
    return 1
  fi

  # --- Check SKILL.md exists ---
  local skill_md="$skill_path/SKILL.md"
  if [[ ! -f "$skill_md" ]]; then
    _validate_json "fail" "" "" "SKILL.md not found in $skill_path"
    return 1
  fi

  # --- Parse frontmatter ---
  local frontmatter
  frontmatter=$(_validate_extract_frontmatter "$skill_md") || {
    _validate_json "fail" "" "" "Failed to parse frontmatter in SKILL.md"
    return 1
  }

  # --- Extract name and description ---
  local name description
  name=$(echo "$frontmatter" | grep -E '^name:' | head -1 | sed 's/^name:\s*//' | sed 's/^"\(.*\)"$/\1/' | xargs) || true
  description=$(echo "$frontmatter" | grep -E '^description:' | head -1 | sed 's/^description:\s*//' | sed 's/^"\(.*\)"$/\1/' | xargs) || true

  # --- Validate name ---
  if [[ -z "$name" ]]; then
    errors+=("name is missing or empty in frontmatter")
  fi

  # --- Validate description ---
  if [[ -z "$description" ]]; then
    errors+=("description is missing or empty in frontmatter")
  else
    local desc_len=${#description}
    if (( desc_len > 160 )); then
      errors+=("description exceeds 160 characters (${desc_len} chars)")
    fi
  fi

  # --- Sensitive keyword scan ---
  local found_sensitive=()
  for kw in "${SENSITIVE_KEYWORDS[@]}"; do
    # case-insensitive grep, skip binary files
    if grep -rliI -- "$kw" "$skill_path" 2>/dev/null | head -1 > /dev/null 2>&1; then
      found_sensitive+=("$kw")
    fi
  done
  if (( ${#found_sensitive[@]} > 0 )); then
    warnings+=("Sensitive keywords found in files: ${found_sensitive[*]}")
  fi

  # --- Check scripts/ directory structure ---
  if [[ -d "$skill_path/scripts" ]]; then
    local script_count
    script_count=$(find "$skill_path/scripts" -name "*.sh" -type f 2>/dev/null | wc -l | xargs)
    if (( script_count == 0 )); then
      warnings+=("scripts/ directory exists but contains no .sh files")
    fi
  fi

  # --- Check references/ directory ---
  if [[ -d "$skill_path/references" ]]; then
    local ref_count
    ref_count=$(find "$skill_path/references" -type f 2>/dev/null | wc -l | xargs)
    if (( ref_count == 0 )); then
      warnings+=("references/ directory exists but is empty")
    fi
  fi

  # --- Output result ---
  if (( ${#errors[@]} > 0 )); then
    local err_json
    err_json=$(printf '%s\n' "${errors[@]}" | _validate_json_array)
    _validate_json "fail" "$name" "$description" "$err_json" "${warnings[@]+"${warnings[@]}"}"
    return 1
  fi

  _validate_json "ok" "$name" "$description" "" "${warnings[@]+"${warnings[@]}"}"
  return 0
}

# ----------------------------------------------------------
# validate_extract_frontmatter <file>
# Extracts YAML frontmatter between --- delimiters.
# Outputs to stdout.
# ----------------------------------------------------------
_validate_extract_frontmatter() {
  local file="$1"
  local in_frontmatter=0
  local line_num=0

  while IFS= read -r line; do
    (( line_num++ )) || true
    if (( line_num == 1 )) && [[ "$line" == "---" ]]; then
      in_frontmatter=1
      continue
    fi
    if (( in_frontmatter == 1 )); then
      if [[ "$line" == "---" ]]; then
        return 0
      fi
      echo "$line"
    fi
  done < "$file"

  # If we never closed frontmatter, it's still valid if we found content
  if (( in_frontmatter == 1 )); then
    return 0
  fi
  return 1
}

# ----------------------------------------------------------
# validate_json_array — pipe lines into a JSON array string
# ----------------------------------------------------------
_validate_json_array() {
  local items=()
  while IFS= read -r line; do
    [[ -n "$line" ]] && items+=("$(printf '%s' "$line" | _json_escape)")
  done
  local IFS=','
  echo "[${items[*]+"${items[*]}"}]"
}

# ----------------------------------------------------------
# _json_escape — escape string for JSON
# ----------------------------------------------------------
_json_escape() {
  sed 's/\\/\\\\/g; s/"/\\"/g; s/\t/\\t/g' | tr '\n' ' '
}

# ----------------------------------------------------------
# _validate_json <status> <name> <description> <errors> [warnings...]
# Outputs final JSON result.
# ----------------------------------------------------------
_validate_json() {
  local status="$1"
  local name="$2"
  local description="$3"
  local errors="$4"
  shift 4
  local warnings_arr=("$@")
  local warnings="[]"

  if (( ${#warnings_arr[@]} > 0 )); then
    warnings=$(printf '%s\n' "${warnings_arr[@]}" | _validate_json_array)
  fi

  [[ -z "$errors" ]] && errors="[]"

  cat <<EOF
{
  "module": "validate",
  "status": "$status",
  "name": "$name",
  "description": "$description",
  "errors": $errors,
  "warnings": $warnings
}
EOF
}

# ----------------------------------------------------------
# Allow direct execution
# ----------------------------------------------------------
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
  validate_run "${1:?Usage: validate.sh <skill-path>}"
fi
