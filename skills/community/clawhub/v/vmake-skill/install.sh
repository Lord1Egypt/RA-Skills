#!/usr/bin/env bash

set -euo pipefail

readonly vmake_installer_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly vmake_skill_name="openclaw-vmake-ai"

show_usage() {
  cat <<'USAGE'
Usage:
  ./install.sh codex <package.zip> [project-dir]
  ./install.sh openclaw <package.zip> [workspace-dir]
  ./install.sh <package.zip> [skills-parent-dir]
  ./install.sh openclaw-workspace <workspace-dir>
  ./install.sh openclaw-global
  ./install.sh codex-project <repository-dir>
  ./install.sh codex-user
  ./install.sh path <skills-parent-dir>

ZIP mode installs openclaw-vmake-ai under the current directory by default.
Pass a second argument to choose a different parent directory.

The short codex/openclaw modes install a ZIP into the current project or
workspace by default. Pass the optional directory to target another location.

The installer overwrites packaged skill files but preserves an existing
scripts/.env. It never writes MT_AK or MT_SK; configure them in the host
environment or secret manager.
USAGE
}

require_command() {
  local vmake_command="$1"
  if ! command -v "$vmake_command" >/dev/null 2>&1; then
    echo "error: required command not found: $vmake_command" >&2
    exit 1
  fi
}

validate_package_root() {
  local vmake_root="$1"

  for vmake_required_path in \
    "$vmake_root/SKILL.md" \
    "$vmake_root/skill.json" \
    "$vmake_root/scripts/vmake_ai.py" \
    "$vmake_root/scripts/config.py" \
    "$vmake_root/sdk/core/config.py"; do
    if [[ ! -f "$vmake_required_path" ]]; then
      echo "error: required package file not found: $vmake_required_path" >&2
      exit 1
    fi
  done

  if find "$vmake_root" -type f -name '.env' -print -quit | grep -q .; then
    echo "error: refusing to install a package containing .env" >&2
    exit 1
  fi
}

install_package_root() {
  local vmake_root="$1"
  local vmake_parent="$2"
  local vmake_target="$vmake_parent/$vmake_skill_name"

  validate_package_root "$vmake_root"
  mkdir -p "$vmake_parent"

  if [[ -d "$vmake_target" ]]; then
    local vmake_backup_dir
    vmake_backup_dir="$(mktemp -d /tmp/vmake-skill-install-backup.XXXXXX)"
    rsync -a --exclude='.env' "$vmake_target/" "$vmake_backup_dir/"
    printf 'Existing non-secret files backed up to:\n  %s\n' "$vmake_backup_dir"
  fi

  mkdir -p "$vmake_target"
  rsync -a \
    --exclude='.env' \
    --exclude='install.sh' \
    "$vmake_root/" \
    "$vmake_target/"

  if [[ ! -f "$vmake_target/SKILL.md" ]]; then
    echo "error: installation did not produce SKILL.md" >&2
    exit 1
  fi

  printf 'Installed skill:\n  %s\n' "$vmake_target"
  printf '%s\n' 'Credentials were not installed. Provide MT_AK and MT_SK through the host environment or secret manager.'
  printf '%s\n' 'Start a new agent session; restart the host if the updated skill is not detected.'
}

install_zip() {
  local vmake_archive="$1"
  local vmake_parent="$2"
  local vmake_extract_dir
  local vmake_entry

  require_command unzip

  if [[ ! -f "$vmake_archive" ]]; then
    echo "error: ZIP package not found: $vmake_archive" >&2
    exit 1
  fi

  while IFS= read -r vmake_entry; do
    case "$vmake_entry" in
      /*|../*|*/../*|*/..)
        echo "error: unsafe ZIP entry: $vmake_entry" >&2
        exit 1
        ;;
      .env|*/.env)
        echo "error: refusing to install a ZIP containing .env" >&2
        exit 1
        ;;
    esac
  done < <(unzip -Z1 "$vmake_archive")

  vmake_extract_dir="$(mktemp -d /tmp/vmake-skill-unpack.XXXXXX)"
  cleanup_vmake_extract() {
    case "$vmake_extract_dir" in
      /tmp/vmake-skill-unpack.*)
        rm -rf -- "$vmake_extract_dir"
        ;;
      *)
        echo "warning: refusing to remove unexpected temporary path: $vmake_extract_dir" >&2
        ;;
    esac
  }
  trap cleanup_vmake_extract EXIT INT TERM

  unzip -q "$vmake_archive" -d "$vmake_extract_dir"
  install_package_root "$vmake_extract_dir/$vmake_skill_name" "$vmake_parent"
  cleanup_vmake_extract
  trap - EXIT INT TERM
}

require_command rsync
require_command mktemp

vmake_mode="${1:-}"
case "$vmake_mode" in
  codex)
    if [[ $# -lt 2 || $# -gt 3 ]]; then
      show_usage >&2
      exit 2
    fi
    install_zip "$2" "${3:-$PWD}/.agents/skills"
    ;;
  openclaw)
    if [[ $# -lt 2 || $# -gt 3 ]]; then
      show_usage >&2
      exit 2
    fi
    install_zip "$2" "${3:-$PWD}/skills"
    ;;
  *.zip)
    if [[ $# -gt 2 ]]; then
      show_usage >&2
      exit 2
    fi
    install_zip "$vmake_mode" "${2:-$PWD}"
    ;;
  openclaw-workspace)
    if [[ $# -ne 2 ]]; then
      show_usage >&2
      exit 2
    fi
    install_package_root "$vmake_installer_dir" "$2/skills"
    ;;
  openclaw-global)
    if [[ $# -ne 1 ]]; then
      show_usage >&2
      exit 2
    fi
    install_package_root "$vmake_installer_dir" "${HOME}/.openclaw/skills"
    ;;
  codex-project)
    if [[ $# -ne 2 ]]; then
      show_usage >&2
      exit 2
    fi
    install_package_root "$vmake_installer_dir" "$2/.agents/skills"
    ;;
  codex-user)
    if [[ $# -ne 1 ]]; then
      show_usage >&2
      exit 2
    fi
    install_package_root "$vmake_installer_dir" "${HOME}/.agents/skills"
    ;;
  path)
    if [[ $# -ne 2 ]]; then
      show_usage >&2
      exit 2
    fi
    install_package_root "$vmake_installer_dir" "$2"
    ;;
  -h|--help|help)
    show_usage
    ;;
  *)
    show_usage >&2
    exit 2
    ;;
esac
