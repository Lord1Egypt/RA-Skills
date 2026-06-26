#!/usr/bin/env bash
set -euo pipefail

# ============================================================
# platform_clawhub.sh — ClawHub (OpenClaw Registry) adapter
# ============================================================

# @platform_name: clawhub
# @platform_label: ClawHub (OpenClaw Registry)
# @auth_method: cli
# @auth_check: clawhub whoami
# @auth_hint: "请先运行: clawhub login"
# @upload_type: cli_tool
# @upload_command: clawhub publish
# @requires_bin: clawhub
# @install_hint: "npm i -g clawhub"
# @supports_changelog: true
# @supports_version: true

# ----------------------------------------------------------
# platform_clawhub_manifest
# Returns platform manifest as JSON.
# ----------------------------------------------------------
platform_clawhub_manifest() {
  cat <<'EOF'
{
  "name": "clawhub",
  "label": "ClawHub (OpenClaw Registry)",
  "auth_method": "cli",
  "auth_check": "clawhub whoami",
  "auth_hint": "请先运行: clawhub login",
  "upload_type": "cli_tool",
  "upload_command": "clawhub publish",
  "requires_bin": "clawhub",
  "install_hint": "npm i -g clawhub",
  "supports_changelog": true,
  "supports_version": true
}
EOF
}

# ----------------------------------------------------------
# platform_clawhub_check_auth
# Checks if clawhub CLI is available and logged in.
# Returns JSON status.
# ----------------------------------------------------------
platform_clawhub_check_auth() {
  # Check binary exists
  if ! command -v clawhub &>/dev/null; then
    cat <<EOF
{
  "module": "platform_clawhub",
  "function": "check_auth",
  "status": "fail",
  "error": "clawhub CLI not found",
  "hint": "npm i -g clawhub"
}
EOF
    return 1
  fi

  # Check login status
  local whoami_output
  if whoami_output=$(clawhub whoami 2>&1); then
    cat <<EOF
{
  "module": "platform_clawhub",
  "function": "check_auth",
  "status": "ok",
  "user": "$whoami_output"
}
EOF
  else
    cat <<EOF
{
  "module": "platform_clawhub",
  "function": "check_auth",
  "status": "fail",
  "error": "Not logged in to ClawHub",
  "hint": "请先运行: clawhub login"
}
EOF
    return 1
  fi
}

# ----------------------------------------------------------
# platform_clawhub_publish <tarball_path> <skill_path>
# Publishes a skill to ClawHub via CLI.
# ----------------------------------------------------------
platform_clawhub_publish() {
  local tarball_path="${1:?Usage: platform_clawhub_publish <tarball> <skill-path> [--slug <slug>] [--version <ver>] [--changelog <text>] [--yes]}"
  local skill_path="${2:?Usage: platform_clawhub_publish <tarball> <skill-path> [--slug <slug>] [--version <ver>] [--changelog <text>] [--yes]}"
  shift 2

  # Parse extra args
  local slug="" version="" changelog="" yes_flag=""
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --slug)      slug="$2"; shift 2 ;;
      --version)   version="$2"; shift 2 ;;
      --changelog) changelog="$2"; shift 2 ;;
      --yes)       yes_flag="--no-input"; shift ;;
      *)           shift ;;
    esac
  done

  # Validate tarball exists
  if [[ ! -f "$tarball_path" ]]; then
    cat <<EOF
{
  "module": "platform_clawhub",
  "function": "publish",
  "status": "fail",
  "error": "Tarball not found: $tarball_path"
}
EOF
    return 1
  fi

  # Build command
  local cmd=(clawhub publish "$skill_path")
  [[ -n "$slug" ]]      && cmd+=(--slug "$slug")
  [[ -n "$version" ]]   && cmd+=(--version "$version")
  [[ -n "$changelog" ]] && cmd+=(--changelog "$changelog")
  [[ -n "$yes_flag" ]]  && cmd+=("$yes_flag")

  local publish_output
  if publish_output=$("${cmd[@]}" 2>&1); then
    cat <<EOF
{
  "module": "platform_clawhub",
  "function": "publish",
  "status": "ok",
  "output": "$(echo "$publish_output" | head -5 | tr '\n' ' ' | sed 's/"/\\"/g')"
}
EOF
  else
    cat <<EOF
{
  "module": "platform_clawhub",
  "function": "publish",
  "status": "fail",
  "error": "$(echo "$publish_output" | head -5 | tr '\n' ' ' | sed 's/"/\\"/g')"
}
EOF
    return 1
  fi
}

# ----------------------------------------------------------
# platform_clawhub_status <skill-name>
# Queries ClawHub for published version/status.
# ----------------------------------------------------------
platform_clawhub_status() {
  local skill_name="${1:?Usage: platform_clawhub_status <skill-name>}"

  local search_output
  if search_output=$(clawhub search "$skill_name" --json 2>&1); then
    cat <<EOF
{
  "module": "platform_clawhub",
  "function": "status",
  "status": "ok",
  "skill_name": "$skill_name",
  "remote_info": "$(echo "$search_output" | head -10 | tr '\n' ' ' | sed 's/"/\\"/g')"
}
EOF
  else
    cat <<EOF
{
  "module": "platform_clawhub",
  "function": "status",
  "status": "not_found",
  "skill_name": "$skill_name",
  "error": "Skill not found on ClawHub or query failed"
}
EOF
    return 1
  fi
}

# ----------------------------------------------------------
# platform_clawhub_post_publish <skill-name> <version>
# Optional post-publish hook.
# ----------------------------------------------------------
platform_clawhub_post_publish() {
  local skill_name="${1:-unknown}"
  local version="${2:-unknown}"

  cat <<EOF
{
  "module": "platform_clawhub",
  "function": "post_publish",
  "status": "ok",
  "message": "Published $skill_name@$version to ClawHub",
  "url_hint": "https://clawhub.com/skills/$skill_name"
}
EOF
}

# ----------------------------------------------------------
# platform_clawhub_help
# Platform-specific help text.
# ----------------------------------------------------------
platform_clawhub_help() {
  cat <<'EOF'
ClawHub (OpenClaw Registry) — 官方技能注册平台

认证: clawhub login
发布: clawhub publish <skill-path>
搜索: clawhub search <keyword>
状态: clawhub whoami

详见: clawhub --help
EOF
}

# ----------------------------------------------------------
# Allow direct execution
# ----------------------------------------------------------
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
  cmd="${1:-manifest}"
  shift || true
  case "$cmd" in
    manifest)   platform_clawhub_manifest ;;
    check_auth) platform_clawhub_check_auth ;;
    publish)    platform_clawhub_publish "$@" ;;
    status)     platform_clawhub_status "$@" ;;
    help)       platform_clawhub_help ;;
    *)          echo "Unknown command: $cmd" >&2; exit 1 ;;
  esac
fi
