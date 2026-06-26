#!/usr/bin/env bash
set -euo pipefail

# ============================================================
# publish.sh — Main entry point for skill-publisher
# ============================================================
# Parses CLI arguments and dispatches to modules:
#   validate, package, publish, version, status, platforms
# ============================================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# History file location
HISTORY_DIR="${HOME}/.openclaw/skill-publisher"
HISTORY_FILE="$HISTORY_DIR/history.jsonl"

# ----------------------------------------------------------
# Main dispatcher
# ----------------------------------------------------------
main() {
  local cmd="${1:-help}"
  shift || true

  case "$cmd" in
    validate)  cmd_validate "$@" ;;
    package)   cmd_package "$@" ;;
    publish)   cmd_publish "$@" ;;
    version)   cmd_version "$@" ;;
    status)    cmd_status "$@" ;;
    platforms) cmd_platforms "$@" ;;
    help|--help|-h) cmd_help ;;
    *)
      _pub_err "Unknown command: $cmd"
      cmd_help
      return 1
      ;;
  esac
}

# ============================================================
# validate <skill-path>
# ============================================================
cmd_validate() {
  local skill_path="${1:?Usage: skill-publisher validate <skill-path>}"

  # shellcheck disable=SC1090
  source "$SCRIPT_DIR/validate.sh"
  validate_run "$skill_path"
}

# ============================================================
# package <skill-path> [--output <dir>] [--version <ver>]
# ============================================================
cmd_package() {
  local skill_path="${1:?Usage: skill-publisher package <skill-path> [--output <dir>] [--version <ver>]}"
  shift
  local output_dir="" version_override=""

  while [[ $# -gt 0 ]]; do
    case "$1" in
      --output)  output_dir="$2"; shift 2 ;;
      --version) version_override="$2"; shift 2 ;;
      *)         _pub_err "Unknown option: $1"; return 1 ;;
    esac
  done

  # Validate first
  # shellcheck disable=SC1090
  source "$SCRIPT_DIR/validate.sh"
  local validate_result
  validate_result=$(validate_run "$skill_path") || {
    _pub_err "Validation failed. Aborting package."
    echo "$validate_result"
    return 1
  }

  # Get version
  # shellcheck disable=SC1090
  source "$SCRIPT_DIR/version.sh"
  local version
  if [[ -n "$version_override" ]]; then
    version="$version_override"
  else
    version=$(_version_extract "$skill_path/SKILL.md") || version="0.0.0"
  fi

  # Get skill name
  local name
  name=$(grep -m1 '^name:' "$skill_path/SKILL.md" | sed 's/^name:\s*//' | sed 's/^"\(.*\)"$/\1/' | xargs) || name="unknown-skill"

  # Determine output
  if [[ -z "$output_dir" ]]; then
    output_dir=$(dirname "$skill_path")
  fi
  mkdir -p "$output_dir"

  local tarball_name="${name}-${version}.tar.gz"
  local tarball_path="$output_dir/$tarball_name"

  # Create tarball
  local base_dir
  base_dir=$(basename "$skill_path")
  tar -czf "$tarball_path" -C "$(dirname "$skill_path")" "$base_dir"

  cat <<EOF
{
  "module": "publish",
  "command": "package",
  "status": "ok",
  "name": "$name",
  "version": "$version",
  "tarball": "$tarball_path",
  "size_bytes": $(stat -c%s "$tarball_path" 2>/dev/null || stat -f%z "$tarball_path" 2>/dev/null || echo 0)
}
EOF
}

# ============================================================
# publish <path> --to <platforms> [--yes]
# ============================================================
cmd_publish() {
  local skill_path="${1:?Usage: skill-publisher publish <path> --to <platforms> [--yes]}"
  shift

  local platforms="" auto_yes=false slug_override=""

  while [[ $# -gt 0 ]]; do
    case "$1" in
      --to|--platform) platforms="$2"; shift 2 ;;
      --slug)          slug_override="$2"; shift 2 ;;
      --yes|-y)        auto_yes=true; shift ;;
      *)               _pub_err "Unknown option: $1"; return 1 ;;
    esac
  done

  # Build auto_yes_flag for platform adapters
  local auto_yes_flag=""
  [[ "$auto_yes" == "true" ]] && auto_yes_flag="--yes"

  if [[ -z "$platforms" ]]; then
    _pub_err "Missing --to <platforms>. Use comma-separated names or 'all'."
    return 1
  fi

  # Source all modules
  # shellcheck disable=SC1090
  source "$SCRIPT_DIR/validate.sh"
  # shellcheck disable=SC1090
  source "$SCRIPT_DIR/version.sh"
  # shellcheck disable=SC1090
  source "$SCRIPT_DIR/platform_registry.sh"

  # Step 1: Validate
  _pub_log "Validating skill..."
  local validate_result
  validate_result=$(validate_run "$skill_path") || {
    _pub_err "Validation failed:"
    echo "$validate_result" >&2
    return 1
  }

  # Step 2: Get version
  local version
  version=$(_version_extract "$skill_path/SKILL.md") || version="0.0.0"
  local name
  name=$(grep -m1 '^name:' "$skill_path/SKILL.md" | sed 's/^name:\s*//' | sed 's/^"\(.*\)"$/\1/' | xargs) || name="unknown-skill"
  local slug
  slug="${slug_override:-$name}"

  # Step 3: Package tarball
  _pub_log "Packaging $name@$version..."
  local tmp_dir
  tmp_dir=$(mktemp -d)
  local tarball_path="$tmp_dir/${name}-${version}.tar.gz"
  local base_dir
  base_dir=$(basename "$skill_path")
  tar -czf "$tarball_path" -C "$(dirname "$skill_path")" "$base_dir"

  # Step 4: Resolve platforms
  local platform_list_arr=()
  if [[ "$platforms" == "all" ]]; then
    for f in "$SCRIPT_DIR"/platform_*.sh; do
      [[ -f "$f" ]] || continue
      local pname
      pname=$(grep -m1 '^# @platform_name:' "$f" 2>/dev/null | sed 's/^# @platform_name:\s*//' | xargs) || true
      [[ -n "$pname" ]] && platform_list_arr+=("$pname")
    done
  else
    IFS=',' read -ra platform_list_arr <<< "$platforms"
  fi

  # Step 5: Publish to each platform
  local results=()
  local overall_status="ok"

  for pname in "${platform_list_arr[@]}"; do
    pname=$(echo "$pname" | xargs)  # trim whitespace
    _pub_log "Publishing to $pname..."

    # Load platform adapter
    local adapter_file="$SCRIPT_DIR/platform_${pname}.sh"
    if [[ ! -f "$adapter_file" ]]; then
      results+=("{\"platform\":\"$pname\",\"status\":\"fail\",\"error\":\"Adapter not found\"}")
      overall_status="partial"
      continue
    fi

    # shellcheck disable=SC1090
    source "$adapter_file"

    # Check auth
    local auth_result
    if auth_result=$("platform_${pname}_check_auth" 2>&1); then
      _pub_log "  ✓ Auth OK for $pname"
    else
      _pub_err "  ✗ Auth failed for $pname"
      results+=("{\"platform\":\"$pname\",\"status\":\"fail\",\"error\":\"Authentication failed\"}")
      overall_status="partial"
      continue
    fi

    # Confirm unless --yes
    if [[ "$auto_yes" != "true" ]]; then
      _pub_log "  Ready to publish $name@$version to $pname. Continue? [y/N]"
      local confirm
      read -r confirm
      if [[ ! "$confirm" =~ ^[yY]$ ]]; then
        _pub_log "  Skipped $pname"
        results+=("{\"platform\":\"$pname\",\"status\":\"skipped\"}")
        continue
      fi
    fi

    # Publish
    local pub_result
    if pub_result=$("platform_${pname}_publish" "$tarball_path" "$skill_path" --slug "$slug" --version "$version" $auto_yes_flag 2>&1); then
      _pub_log "  ✓ Published to $pname"
      results+=("{\"platform\":\"$pname\",\"status\":\"ok\",\"detail\":$(echo "$pub_result" | tr '\n' ' ')}")

      # Post-publish hook
      if declare -f "platform_${pname}_post_publish" &>/dev/null; then
        "platform_${pname}_post_publish" "$name" "$version" > /dev/null 2>&1 || true
      fi
    else
      _pub_err "  ✗ Failed to publish to $pname"
      results+=("{\"platform\":\"$pname\",\"status\":\"fail\",\"error\":\"Publish failed\"}")
      overall_status="partial"
    fi
  done

  # Step 6: Record history
  _pub_record_history "$name" "$version" "$overall_status" "${platform_list_arr[*]}"

  # Cleanup
  rm -rf "$tmp_dir"

  # Step 7: Summary
  local results_json
  local IFS=','
  results_json="[${results[*]}]"

  cat <<EOF
{
  "module": "publish",
  "command": "publish",
  "status": "$overall_status",
  "name": "$name",
  "version": "$version",
  "results": $results_json
}
EOF
}

# ============================================================
# version <skill-path> [--bump patch|minor|major] [--set <ver>]
# ============================================================
cmd_version() {
  local skill_path="${1:?Usage: skill-publisher version <skill-path> [--bump TYPE|--set VER]}"
  shift

  # shellcheck disable=SC1090
  source "$SCRIPT_DIR/version.sh"

  if [[ $# -eq 0 ]]; then
    version_get "$skill_path"
    return
  fi

  case "$1" in
    --bump)
      version_bump "$skill_path" "${2:?Missing bump type: patch|minor|major}"
      ;;
    --set)
      version_set "$skill_path" "${2:?Missing version string}"
      ;;
    *)
      _pub_err "Unknown version option: $1"
      return 1
      ;;
  esac
}

# ============================================================
# status <skill-path>
# ============================================================
cmd_status() {
  local skill_path="${1:?Usage: skill-publisher status <skill-path>}"

  # shellcheck disable=SC1090
  source "$SCRIPT_DIR/status.sh"
  status_run "$skill_path"
}

# ============================================================
# platforms <list|info> [name]
# ============================================================
cmd_platforms() {
  local subcmd="${1:?Usage: skill-publisher platforms <list|info> [name]}"
  shift || true

  # shellcheck disable=SC1090
  source "$SCRIPT_DIR/platform_registry.sh"

  case "$subcmd" in
    list) platform_list ;;
    info) platform_info "${1:?Usage: skill-publisher platforms info <name>}" ;;
    *)    _pub_err "Unknown platforms subcommand: $subcmd"; return 1 ;;
  esac
}

# ============================================================
# History recording
# ============================================================
pub_record_history() {
  _pub_record_history "$@"
}

_pub_record_history() {
  local name="$1" version="$2" status="$3" platforms="$4"
  mkdir -p "$HISTORY_DIR"

  local timestamp
  timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ" 2>/dev/null || date -Iseconds 2>/dev/null || echo "unknown")

  cat >> "$HISTORY_FILE" <<EOF
{"timestamp":"$timestamp","name":"$name","version":"$version","status":"$status","platforms":"$platforms"}
EOF
}

# ============================================================
# Help
# ============================================================
cmd_help() {
  cat <<'USAGE'
skill-publisher — 将 Agent 技能发布到多个平台

用法:
  skill-publisher validate <skill-path>
  skill-publisher package  <skill-path> [--output <dir>] [--version <ver>]
  skill-publisher publish  <path> --to <platforms> [--slug <slug>] [--yes]
  skill-publisher version  <skill-path> [--bump patch|minor|major] [--set <ver>]
  skill-publisher status   <skill-path>
  skill-publisher platforms list
  skill-publisher platforms info <name>

平台:
  clawhub     ClawHub (OpenClaw 官方)
  github      GitHub Releases
  skillhub    SkillHub CN (国内社区)

示例:
  skill-publisher validate ./my-skill
  skill-publisher publish ./my-skill --to clawhub,github
  skill-publisher publish ./my-skill --to all --yes
  skill-publisher version ./my-skill --bump patch

安全:
  发布前自动验证，失败则中止。
  敏感信息不写入日志。
  需用户确认（--yes 跳过）。
USAGE
}

# ============================================================
# Logging helpers (stderr)
# ============================================================
_pub_log() {
  echo "[skill-publisher] $*" >&2
}

_pub_err() {
  echo "[skill-publisher] ERROR: $*" >&2
}

# ----------------------------------------------------------
# Entry point
# ----------------------------------------------------------
main "$@"
