#!/usr/bin/env bash
set -euo pipefail

# ============================================================
# platform_skillhub.sh — SkillHub CN (腾讯云镜像) adapter
# ============================================================

# @platform_name: skillhub
# @platform_label: SkillHub CN (腾讯云 ClawHub 镜像)
# @auth_method: none
# @auth_check: echo "mirror"
# @auth_hint: "SkillHub 是 ClawHub 镜像，发布到 ClawHub 后自动同步"
# @upload_type: mirror
# @upload_command: clawhub publish
# @requires_bin: clawhub
# @install_hint: "npm i -g clawhub"
# @supports_changelog: false
# @supports_version: true

SKILLHUB_BASE_URL="${SKILLHUB_BASE_URL:-https://skillhub.cloud.tencent.com}"

# ----------------------------------------------------------
# platform_skillhub_manifest
# Returns platform manifest as JSON.
# ----------------------------------------------------------
platform_skillhub_manifest() {
  cat <<EOF
{
  "name": "skillhub",
  "label": "SkillHub CN (腾讯云 ClawHub 镜像)",
  "auth_method": "none",
  "upload_type": "mirror",
  "mirror_of": "clawhub",
  "base_url": "$SKILLHUB_BASE_URL",
  "description": "SkillHub 是 ClawHub 的国内镜像平台，发布到 ClawHub 后会自动同步。无需单独发布。",
  "requires_bin": "clawhub",
  "install_hint": "npm i -g clawhub",
  "supports_changelog": false,
  "supports_version": true
}
EOF
}

# ----------------------------------------------------------
# platform_skillhub_check_auth
# Since it's a mirror, no auth needed.
# ----------------------------------------------------------
platform_skillhub_check_auth() {
  cat <<EOF
{
  "module": "platform_skillhub",
  "function": "check_auth",
  "status": "ok",
  "note": "SkillHub 是 ClawHub 镜像，无需单独认证。请确保 ClawHub 已登录。"
}
EOF
}

# ----------------------------------------------------------
# platform_skillhub_validate <skill_path>
# Validates that the skill is also published to ClawHub.
# ----------------------------------------------------------
platform_skillhub_validate() {
  local skill_path="${1:?Usage: platform_skillhub_validate <skill-path>}"

  # Check if clawhub CLI is available
  if ! command -v clawhub &>/dev/null; then
    cat <<EOF
{
  "module": "platform_skillhub",
  "function": "validate",
  "status": "fail",
  "error": "clawhub CLI not found",
  "hint": "npm i -g clawhub"
}
EOF
    return 1
  fi

  # Check if logged in to ClawHub
  if ! clawhub whoami &>/dev/null; then
    cat <<EOF
{
  "module": "platform_skillhub",
  "function": "validate",
  "status": "fail",
  "error": "未登录 ClawHub",
  "hint": "请先运行: clawhub login"
}
EOF
    return 1
  fi

  cat <<EOF
{
  "module": "platform_skillhub",
  "function": "validate",
  "status": "ok",
  "note": "ClawHub 已登录，发布后 SkillHub 会自动同步"
}
EOF
}

# ----------------------------------------------------------
# platform_skillhub_publish <tarball_path> <skill_path>
# Since SkillHub is a ClawHub mirror, this publishes to ClawHub
# and informs the user about automatic sync.
# ----------------------------------------------------------
platform_skillhub_publish() {
  local tarball_path="${1:?Usage: platform_skillhub_publish <tarball> <skill-path>}"
  local skill_path="${2:?Usage: platform_skillhub_publish <tarball> <skill-path>}"
  shift 2

  # Parse remaining args for slug/version
  local slug="" version="" auto_yes=false
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --slug)    slug="$2"; shift 2 ;;
      --version) version="$2"; shift 2 ;;
      --yes|-y)  auto_yes=true; shift ;;
      *)         shift ;;
    esac
  done

  # Check clawhub CLI
  if ! command -v clawhub &>/dev/null; then
    cat <<EOF
{
  "module": "platform_skillhub",
  "function": "publish",
  "status": "fail",
  "error": "clawhub CLI not found",
  "hint": "npm i -g clawhub"
}
EOF
    return 1
  fi

  # Check ClawHub auth
  if ! clawhub whoami &>/dev/null; then
    cat <<EOF
{
  "module": "platform_skillhub",
  "function": "publish",
  "status": "fail",
  "error": "未登录 ClawHub",
  "hint": "请先运行: clawhub login"
}
EOF
    return 1
  fi

  # Publish to ClawHub (which triggers SkillHub sync)
  _pub_log "  SkillHub 是 ClawHub 镜像，正在发布到 ClawHub..."

  local clawhub_args=("publish" "$skill_path")
  [[ -n "$slug" ]] && clawhub_args+=("--slug" "$slug")
  [[ -n "$version" ]] && clawhub_args+=("--version" "$version")

  local pub_output
  if pub_output=$(clawhub "${clawhub_args[@]}" 2>&1); then
    cat <<EOF
{
  "module": "platform_skillhub",
  "function": "publish",
  "status": "ok",
  "detail": "已通过 ClawHub 发布，SkillHub 将自动同步",
  "clawhub_output": "$(echo "$pub_output" | head -5 | tr '\n' ' ' | sed 's/"/\\"/g')",
  "skillhub_url": "$SKILLHUB_BASE_URL",
  "sync_note": "SkillHub 镜像同步通常需要几分钟到几小时"
}
EOF
  else
    # Check if error is "version already exists" — treat as success for mirror
    if echo "$pub_output" | grep -qi "already exists"; then
      cat <<EOF
{
  "module": "platform_skillhub",
  "function": "publish",
  "status": "ok",
  "detail": "版本已存在于 ClawHub，SkillHub 将自动同步",
  "skillhub_url": "$SKILLHUB_BASE_URL",
  "sync_note": "SkillHub 镜像同步通常需要几分钟到几小时"
}
EOF
    else
      cat <<EOF
{
  "module": "platform_skillhub",
  "function": "publish",
  "status": "fail",
  "error": "ClawHub 发布失败",
  "clawhub_output": "$(echo "$pub_output" | head -5 | tr '\n' ' ' | sed 's/"/\\"/g')"
}
EOF
      return 1
    fi
  fi
}

# ----------------------------------------------------------
# platform_skillhub_status <skill-name>
# ----------------------------------------------------------
platform_skillhub_status() {
  local skill_name="${1:?Usage: platform_skillhub_status <skill-name>}"

  cat <<EOF
{
  "module": "platform_skillhub",
  "function": "status",
  "status": "info",
  "skill_name": "$skill_name",
  "note": "SkillHub 是 ClawHub 镜像，请在 ClawHub 查看发布状态",
  "clawhub_url": "https://clawhub.com/skills/$skill_name",
  "skillhub_url": "$SKILLHUB_BASE_URL"
}
EOF
}

# ----------------------------------------------------------
# platform_skillhub_post_publish <skill-name> <version>
# ----------------------------------------------------------
platform_skillhub_post_publish() {
  local skill_name="${1:-unknown}"
  local version="${2:-unknown}"

  cat <<EOF
{
  "module": "platform_skillhub",
  "function": "post_publish",
  "status": "ok",
  "message": "已通过 ClawHub 发布 $skill_name@$version，SkillHub 将自动同步",
  "clawhub_url": "https://clawhub.com/skills/$skill_name",
  "skillhub_url": "$SKILLHUB_BASE_URL",
  "sync_note": "镜像同步通常需要几分钟到几小时"
}
EOF
}

# ----------------------------------------------------------
# platform_skillhub_help
# ----------------------------------------------------------
platform_skillhub_help() {
  cat <<EOF
SkillHub CN — 腾讯云 ClawHub 国内镜像

SkillHub ($SKILLHUB_BASE_URL) 是 ClawHub 的国内镜像平台，
发布到 ClawHub 后会自动同步到 SkillHub，无需单独发布。

工作流程:
  1. clawhub login          # 登录 ClawHub
  2. clawhub publish <path> # 发布技能
  3. 等待 SkillHub 自动同步  # 通常几分钟到几小时

查看:
  ClawHub:   https://clawhub.com/skills/<name>
  SkillHub:  $SKILLHUB_BASE_URL
EOF
}

# ----------------------------------------------------------
# Allow direct execution
# ----------------------------------------------------------
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
  cmd="${1:-manifest}"
  shift || true
  case "$cmd" in
    manifest)   platform_skillhub_manifest ;;
    check_auth) platform_skillhub_check_auth ;;
    validate)   platform_skillhub_validate "$@" ;;
    publish)    platform_skillhub_publish "$@" ;;
    status)     platform_skillhub_status "$@" ;;
    help)       platform_skillhub_help ;;
    *)          echo "Unknown command: $cmd" >&2; exit 1 ;;
  esac
fi
