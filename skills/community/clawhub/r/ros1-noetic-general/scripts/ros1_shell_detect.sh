#!/usr/bin/env zsh
set -euo pipefail

distro="noetic"
workspace=""
output_format="human"

print_help() {
  cat <<'EOF'
Usage: ros1_shell_detect.sh [--distro <name>] [--workspace <path>] [--export]

Detect the most suitable shell setup file for ROS1 on this machine.

Options:
  --distro <name>      ROS distro name, default: noetic
  --workspace <path>   Optional workspace root for devel/install setup detection
  --export             Print shell-safe key=value lines for eval
  --help               Show this help
EOF
}

shell_basename() {
  local raw="${1:-}"
  raw="${raw##*/}"
  raw="${raw%% *}"
  print -r -- "$raw"
}

choose_setup_file() {
  local prefix="$1"
  local preferred="$2"
  local candidate=""
  local ext=""

  for ext in "$preferred" zsh bash sh; do
    candidate="$prefix/setup.$ext"
    if [[ -f "$candidate" ]]; then
      print -r -- "$candidate"
      return 0
    fi
  done

  return 1
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --distro)
      distro="${2:?missing distro}"
      shift 2
      ;;
    --workspace)
      workspace="${2:?missing workspace}"
      shift 2
      ;;
    --export)
      output_format="export"
      shift
      ;;
    --help|-h)
      print_help
      exit 0
      ;;
    *)
      echo "[ERROR] unknown argument: $1" >&2
      print_help >&2
      exit 2
      ;;
  esac
done

parent_shell="$(shell_basename "$(ps -p "$PPID" -o comm= 2>/dev/null | awk 'NR==1 {print $1}')")"
default_shell="$(shell_basename "${SHELL:-}")"
preferred_shell=""

for candidate in "$parent_shell" "$default_shell" zsh bash; do
  case "$candidate" in
    zsh|bash)
      if command -v "$candidate" >/dev/null 2>&1; then
        preferred_shell="$candidate"
        break
      fi
      ;;
  esac
done

if [[ -z "$preferred_shell" ]]; then
  preferred_shell="sh"
fi

ros_setup="$(choose_setup_file "/opt/ros/$distro" "$preferred_shell" || true)"
workspace_setup=""

if [[ -n "$workspace" ]]; then
  workspace="${workspace:A}"
  for prefix in "$workspace/devel" "$workspace/install"; do
    workspace_setup="$(choose_setup_file "$prefix" "$preferred_shell" || true)"
    if [[ -n "$workspace_setup" ]]; then
      break
    fi
  done
fi

if [[ "$output_format" == "export" ]]; then
  print -r -- "PARENT_SHELL=${(q)parent_shell}"
  print -r -- "DEFAULT_SHELL=${(q)default_shell}"
  print -r -- "PREFERRED_SHELL=${(q)preferred_shell}"
  print -r -- "ROS_SETUP=${(q)ros_setup}"
  print -r -- "WORKSPACE_SETUP=${(q)workspace_setup}"
  exit 0
fi

echo "[ros1-shell-detect] parent_shell=${parent_shell:-unknown}"
echo "[ros1-shell-detect] default_shell=${default_shell:-unknown}"
echo "[ros1-shell-detect] preferred_shell=$preferred_shell"
if [[ -n "$ros_setup" ]]; then
  echo "[ros1-shell-detect] ros_setup=$ros_setup"
else
  echo "[ros1-shell-detect] ros_setup=missing"
fi
if [[ -n "$workspace_setup" ]]; then
  echo "[ros1-shell-detect] workspace_setup=$workspace_setup"
fi
