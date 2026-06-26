#!/usr/bin/env bash
set -euo pipefail

# ============================================================
# version.sh — Version management module
# ============================================================
# Reads/writes metadata.version in SKILL.md frontmatter.
# Supports --bump patch|minor|major and --set <ver>.
# ============================================================

# ----------------------------------------------------------
# version_get <skill-path>
# Returns current version from SKILL.md frontmatter.
# Outputs JSON to stdout.
# ----------------------------------------------------------
version_get() {
  local skill_path="${1:?Usage: version_get <skill-path>}"
  local skill_md="$skill_path/SKILL.md"

  if [[ ! -f "$skill_md" ]]; then
    _version_json "fail" "" "SKILL.md not found"
    return 1
  fi

  local version
  version=$(_version_extract "$skill_md")

  if [[ -z "$version" ]]; then
    _version_json "fail" "" "No version field found in frontmatter"
    return 1
  fi

  _version_json "ok" "$version" ""
}

# ----------------------------------------------------------
# version_bump <skill-path> <patch|minor|major>
# Bumps version and writes back to SKILL.md.
# Outputs JSON with old and new version.
# ----------------------------------------------------------
version_bump() {
  local skill_path="${1:?Usage: version_bump <skill-path> <patch|minor|major>}"
  local bump_type="${2:?Usage: version_bump <skill-path> <patch|minor|major>}"
  local skill_md="$skill_path/SKILL.md"

  if [[ ! -f "$skill_md" ]]; then
    _version_json "fail" "" "SKILL.md not found"
    return 1
  fi

  local old_version
  old_version=$(_version_extract "$skill_md")

  if [[ -z "$old_version" ]]; then
    _version_json "fail" "" "No version field found in frontmatter"
    return 1
  fi

  local new_version
  new_version=$(_version_compute_bump "$old_version" "$bump_type") || {
    _version_json "fail" "" "Invalid bump type or version format: $bump_type on $old_version"
    return 1
  }

  _version_write_back "$skill_md" "$old_version" "$new_version"
  _version_json_with_old "ok" "$old_version" "$new_version" ""
}

# ----------------------------------------------------------
# version_set <skill-path> <version>
# Sets an explicit version string.
# ----------------------------------------------------------
version_set() {
  local skill_path="${1:?Usage: version_set <skill-path> <version>}"
  local new_version="${2:?Usage: version_set <skill-path> <version>}"
  local skill_md="$skill_path/SKILL.md"

  if [[ ! -f "$skill_md" ]]; then
    _version_json "fail" "" "SKILL.md not found"
    return 1
  fi

  # Validate semver-ish format
  if ! echo "$new_version" | grep -qE '^[0-9]+\.[0-9]+\.[0-9]+(-[a-zA-Z0-9.]+)?(\+[a-zA-Z0-9.]+)?$'; then
    _version_json "fail" "" "Invalid version format: $new_version (expected semver like 1.2.3)"
    return 1
  fi

  local old_version
  old_version=$(_version_extract "$skill_md")

  if [[ -z "$old_version" ]]; then
    _version_json "fail" "" "No version field found in frontmatter to replace"
    return 1
  fi

  _version_write_back "$skill_md" "$old_version" "$new_version"
  _version_json_with_old "ok" "$old_version" "$new_version" ""
}

# ============================================================
# Internal helpers
# ============================================================

_version_extract() {
  local file="$1"
  # Extract version from frontmatter YAML
  local in_fm=0 line_num=0 version=""
  while IFS= read -r line; do
    (( line_num++ )) || true
    if (( line_num == 1 )) && [[ "$line" == "---" ]]; then
      in_fm=1; continue
    fi
    if (( in_fm )); then
      [[ "$line" == "---" ]] && break
      if [[ "$line" =~ ^version:\ *(.*) ]]; then
        version="${BASH_REMATCH[1]}"
        version=$(echo "$version" | sed 's/^"\(.*\)"$/\1/' | xargs)
      fi
    fi
  done < "$file"
  echo "$version"
}

_version_compute_bump() {
  local ver="$1"
  local type="$2"

  # Strip pre-release and build metadata for bumping
  local base="$ver"
  local suffix=""
  if [[ "$ver" == *-* ]]; then
    base="${ver%%-*}"
    suffix="-${ver#*-}"
  elif [[ "$ver" == *+* ]]; then
    base="${ver%%+*}"
  fi

  IFS='.' read -r major minor patch <<< "$base"

  case "$type" in
    patch)
      patch=$(( patch + 1 ))
      ;;
    minor)
      minor=$(( minor + 1 ))
      patch=0
      ;;
    major)
      major=$(( major + 1 ))
      minor=0
      patch=0
      ;;
    *)
      return 1
      ;;
  esac

  echo "${major}.${minor}.${patch}"
}

_version_write_back() {
  local file="$1"
  local old_ver="$2"
  local new_ver="$3"

  # Replace version line in-place using sed
  # Handles both quoted and unquoted version values
  if [[ "$OSTYPE" == "darwin"* ]]; then
    sed -i '' "s/^version: *\"*${old_ver}\"*$/version: \"${new_ver}\"/" "$file"
  else
    sed -i "s/^version: *\"*${old_ver}\"*$/version: \"${new_ver}\"/" "$file"
  fi
}

_version_json() {
  local status="$1"
  local version="$2"
  local error="$3"

  if [[ -n "$error" ]]; then
    cat <<EOF
{
  "module": "version",
  "status": "$status",
  "version": "$version",
  "error": "$error"
}
EOF
  else
    cat <<EOF
{
  "module": "version",
  "status": "$status",
  "version": "$version"
}
EOF
  fi
}

_version_json_with_old() {
  local status="$1"
  local old_ver="$2"
  local new_ver="$3"
  local error="$4"

  if [[ -n "$error" ]]; then
    cat <<EOF
{
  "module": "version",
  "status": "$status",
  "old_version": "$old_ver",
  "new_version": "$new_ver",
  "error": "$error"
}
EOF
  else
    cat <<EOF
{
  "module": "version",
  "status": "$status",
  "old_version": "$old_ver",
  "new_version": "$new_ver"
}
EOF
  fi
}

# ----------------------------------------------------------
# Allow direct execution
# ----------------------------------------------------------
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
  cmd="${1:?Usage: version.sh <get|bump|set> <skill-path> [args...]}"
  shift
  case "$cmd" in
    get)  version_get "$@" ;;
    bump) version_bump "$@" ;;
    set)  version_set "$@" ;;
    *)    echo "Unknown command: $cmd" >&2; exit 1 ;;
  esac
fi
