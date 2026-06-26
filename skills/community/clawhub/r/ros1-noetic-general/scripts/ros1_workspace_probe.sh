#!/usr/bin/env zsh
set -euo pipefail

script_dir="${0:A:h}"
start_path="${PWD}"
output_format="human"

print_help() {
  cat <<'EOF'
Usage: ros1_workspace_probe.sh [--path <path>] [--export]

Find the nearest ROS1 catkin workspace and suggest a build command.

Options:
  --path <path>   Starting file or directory, default: current working directory
  --export        Print shell-safe key=value lines for eval
  --help          Show this help
EOF
}

has_packages() {
  local root="$1"
  if command -v rg >/dev/null 2>&1; then
    rg --files "$root/src" -g 'package.xml' >/dev/null 2>&1
  else
    find "$root/src" -name package.xml -print -quit >/dev/null 2>&1
  fi
}

is_workspace_root() {
  local root="$1"
  [[ -d "$root/src" ]] || return 1

  if [[ -f "$root/.catkin_workspace" || -d "$root/.catkin_tools" || -f "$root/src/CMakeLists.txt" ]]; then
    return 0
  fi

  has_packages "$root"
}

find_workspace_root() {
  local current="$1"
  while true; do
    if is_workspace_root "$current"; then
      print -r -- "$current"
      return 0
    fi

    if [[ "$current" == "/" ]]; then
      return 1
    fi

    current="${current:h}"
  done
}

count_packages() {
  local root="$1"
  if command -v rg >/dev/null 2>&1; then
    rg --files "$root/src" -g 'package.xml' | wc -l | tr -d ' '
  else
    find "$root/src" -name package.xml | wc -l | tr -d ' '
  fi
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --path)
      start_path="${2:?missing path}"
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

start_path="${start_path:A}"
if [[ -f "$start_path" ]]; then
  start_path="${start_path:h}"
fi

workspace_root="$(find_workspace_root "$start_path" || true)"
build_tool="none"
build_command=""
workspace_setup=""
package_count="0"

if [[ -n "$workspace_root" ]]; then
  if [[ -d "$workspace_root/.catkin_tools" ]]; then
    build_tool="catkin-tools"
    build_command="catkin build"
  elif command -v catkin_make >/dev/null 2>&1; then
    build_tool="catkin_make"
    build_command="catkin_make"
  elif command -v catkin >/dev/null 2>&1; then
    build_tool="catkin-tools"
    build_command="catkin build"
  else
    build_tool="unknown"
    build_command="<install catkin_make or catkin build>"
  fi

  package_count="$(count_packages "$workspace_root")"
  eval "$("$script_dir/ros1_shell_detect.sh" --workspace "$workspace_root" --export)"
  workspace_setup="$WORKSPACE_SETUP"
fi

if [[ "$output_format" == "export" ]]; then
  print -r -- "WORKSPACE_ROOT=${(q)workspace_root}"
  print -r -- "BUILD_TOOL=${(q)build_tool}"
  print -r -- "BUILD_COMMAND=${(q)build_command}"
  print -r -- "WORKSPACE_SETUP=${(q)workspace_setup}"
  print -r -- "PACKAGE_COUNT=${(q)package_count}"
  exit 0
fi

if [[ -z "$workspace_root" ]]; then
  echo "[ros1-workspace-probe] workspace_root=not-found"
  exit 1
fi

echo "[ros1-workspace-probe] workspace_root=$workspace_root"
echo "[ros1-workspace-probe] package_count=$package_count"
echo "[ros1-workspace-probe] build_tool=$build_tool"
echo "[ros1-workspace-probe] build_command=$build_command"
if [[ -n "$workspace_setup" ]]; then
  echo "[ros1-workspace-probe] workspace_setup=$workspace_setup"
fi
