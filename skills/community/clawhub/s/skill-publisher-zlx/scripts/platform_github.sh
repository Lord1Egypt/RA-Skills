#!/usr/bin/env bash
set -euo pipefail

# ============================================================
# platform_github.sh — GitHub Releases adapter
# ============================================================

# @platform_name: github
# @platform_label: GitHub Releases
# @auth_method: cli
# @auth_check: gh auth status
# @auth_hint: "请先运行: gh auth login"
# @upload_type: cli_tool
# @upload_command: gh release create
# @requires_bin: gh
# @install_hint: "brew install gh / winget install GitHub.cli"
# @supports_changelog: true
# @supports_version: true

# ----------------------------------------------------------
# platform_github_manifest
# Returns platform manifest as JSON.
# ----------------------------------------------------------
platform_github_manifest() {
  cat <<'EOF'
{
  "name": "github",
  "label": "GitHub Releases",
  "auth_method": "cli",
  "auth_check": "gh auth status",
  "auth_hint": "请先运行: gh auth login",
  "upload_type": "cli_tool",
  "upload_command": "gh release create",
  "requires_bin": "gh",
  "install_hint": "brew install gh / winget install GitHub.cli",
  "supports_changelog": true,
  "supports_version": true
}
EOF
}

# ----------------------------------------------------------
# platform_github_check_auth
# Checks if gh CLI is available and authenticated.
# ----------------------------------------------------------
platform_github_check_auth() {
  # Check binary exists
  if ! command -v gh &>/dev/null; then
    cat <<EOF
{
  "module": "platform_github",
  "function": "check_auth",
  "status": "fail",
  "error": "gh CLI not found",
  "hint": "brew install gh / winget install GitHub.cli"
}
EOF
    return 1
  fi

  # Check auth status
  local status_output
  if status_output=$(gh auth status 2>&1); then
    local user
    user=$(echo "$status_output" | grep -oE 'Logged in to [^ ]+ as [^ ]+' | awk '{print $NF}') || user="authenticated"
    cat <<EOF
{
  "module": "platform_github",
  "function": "check_auth",
  "status": "ok",
  "user": "$user"
}
EOF
  else
    cat <<EOF
{
  "module": "platform_github",
  "function": "check_auth",
  "status": "fail",
  "error": "Not authenticated with GitHub",
  "hint": "请先运行: gh auth login"
}
EOF
    return 1
  fi
}

# ----------------------------------------------------------
# platform_github_publish <tarball_path> <skill_path>
# Creates a GitHub Release with the tarball attached.
# Expects GITHUB_REPO env var or auto-detects from git remote.
# ----------------------------------------------------------
platform_github_publish() {
  local tarball_path="${1:?Usage: platform_github_publish <tarball> <skill-path>}"
  local skill_path="${2:?Usage: platform_github_publish <tarball> <skill-path>}"

  # Validate tarball exists
  if [[ ! -f "$tarball_path" ]]; then
    cat <<EOF
{
  "module": "platform_github",
  "function": "publish",
  "status": "fail",
  "error": "Tarball not found: $tarball_path"
}
EOF
    return 1
  fi

  # Determine repo
  local repo="${GITHUB_REPO:-}"
  if [[ -z "$repo" ]]; then
    # Try to detect from git remote
    repo=$(git -C "$skill_path" remote get-url origin 2>/dev/null | sed 's|.*github.com[:/]||' | sed 's|\.git$||') || true
  fi

  if [[ -z "$repo" ]]; then
    cat <<EOF
{
  "module": "platform_github",
  "function": "publish",
  "status": "fail",
  "error": "Cannot determine GitHub repo. Set GITHUB_REPO env or run from a git repo.",
  "hint": "export GITHUB_REPO=owner/repo"
}
EOF
    return 1
  fi

  # Extract version from tarball name for tag
  local tarball_name
  tarball_name=$(basename "$tarball_path")
  local version_str
  version_str=$(echo "$tarball_name" | grep -oE '[0-9]+\.[0-9]+\.[0-9]+(-[a-zA-Z0-9.]+)?' | head -1) || version_str=""
  # Strip any trailing .tar.gz that might have been captured
  version_str=${version_str%.tar.gz}
  local tag="v${version_str:-latest}"

  # Create release
  local release_output
  if release_output=$(gh release create "$tag" "$tarball_path" \
    --repo "$repo" \
    --title "Release $tag" \
    --generate-notes 2>&1); then
    local release_url
    release_url=$(echo "$release_output" | grep -oE 'https://[^ ]+' | head -1) || release_url=""
    cat <<EOF
{
  "module": "platform_github",
  "function": "publish",
  "status": "ok",
  "tag": "$tag",
  "repo": "$repo",
  "url": "$release_url"
}
EOF
  else
    cat <<EOF
{
  "module": "platform_github",
  "function": "publish",
  "status": "fail",
  "error": "$(echo "$release_output" | head -3 | tr '\n' ' ' | sed 's/"/\\"/g')"
}
EOF
    return 1
  fi
}

# ----------------------------------------------------------
# platform_github_status <skill-name>
# Queries GitHub for published releases.
# ----------------------------------------------------------
platform_github_status() {
  local skill_name="${1:?Usage: platform_github_status <skill-name>}"
  local repo="${GITHUB_REPO:-}"

  if [[ -z "$repo" ]]; then
    cat <<EOF
{
  "module": "platform_github",
  "function": "status",
  "status": "unknown",
  "skill_name": "$skill_name",
  "error": "GITHUB_REPO not set, cannot query releases"
}
EOF
    return 1
  fi

  local releases_output
  if releases_output=$(gh release list --repo "$repo" --limit 5 2>&1); then
    local latest
    latest=$(echo "$releases_output" | head -1 | awk '{print $1, $2}') || latest="none"
    cat <<EOF
{
  "module": "platform_github",
  "function": "status",
  "status": "ok",
  "skill_name": "$skill_name",
  "repo": "$repo",
  "latest_release": "$latest"
}
EOF
  else
    cat <<EOF
{
  "module": "platform_github",
  "function": "status",
  "status": "not_found",
  "skill_name": "$skill_name",
  "error": "No releases found or repo inaccessible"
}
EOF
    return 1
  fi
}

# ----------------------------------------------------------
# platform_github_post_publish <skill-name> <version>
# ----------------------------------------------------------
platform_github_post_publish() {
  local skill_name="${1:-unknown}"
  local version="${2:-unknown}"
  local repo="${GITHUB_REPO:-owner/repo}"

  cat <<EOF
{
  "module": "platform_github",
  "function": "post_publish",
  "status": "ok",
  "message": "Released $skill_name@$version to GitHub",
  "url_hint": "https://github.com/$repo/releases"
}
EOF
}

# ----------------------------------------------------------
# platform_github_help
# ----------------------------------------------------------
platform_github_help() {
  cat <<'EOF'
GitHub Releases — 通过 GitHub Release 发布技能

认证: gh auth login
发布: gh release create <tag> <file> --repo <owner/repo>
查看: gh release list --repo <owner/repo>
设置仓库: export GITHUB_REPO=owner/repo

详见: gh release --help
EOF
}

# ----------------------------------------------------------
# Allow direct execution
# ----------------------------------------------------------
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
  cmd="${1:-manifest}"
  shift || true
  case "$cmd" in
    manifest)   platform_github_manifest ;;
    check_auth) platform_github_check_auth ;;
    publish)    platform_github_publish "$@" ;;
    status)     platform_github_status "$@" ;;
    help)       platform_github_help ;;
    *)          echo "Unknown command: $cmd" >&2; exit 1 ;;
  esac
fi
