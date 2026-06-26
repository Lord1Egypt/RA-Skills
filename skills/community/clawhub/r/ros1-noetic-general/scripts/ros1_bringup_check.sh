#!/usr/bin/env zsh
set -euo pipefail

script_dir="${0:A:h}"
workspace_path="${PWD}"
launch_pattern=""

print_help() {
  cat <<'EOF'
Usage: ros1_bringup_check.sh [--workspace <path>] [--pattern <text>]

Run a basic ROS1 bringup preflight:
  1. detect shell and source files
  2. detect workspace and build command
  3. source ROS and workspace setup files when present
  4. run environment checks
  5. list candidate launch files

Options:
  --workspace <path>  Workspace or subdirectory to inspect, default: current working directory
  --pattern <text>    Filter discovered launch files by substring
  --help              Show this help
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --workspace|--path)
      workspace_path="${2:?missing workspace path}"
      shift 2
      ;;
    --pattern)
      launch_pattern="${2:?missing pattern}"
      shift 2
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

eval "$("$script_dir/ros1_workspace_probe.sh" --path "$workspace_path" --export)"
workspace_root="$WORKSPACE_ROOT"
build_tool="$BUILD_TOOL"
build_command="$BUILD_COMMAND"
workspace_setup="$WORKSPACE_SETUP"

shell_detect_args=(--export)
if [[ -n "$workspace_root" ]]; then
  shell_detect_args=(--workspace "$workspace_root" --export)
fi
eval "$("$script_dir/ros1_shell_detect.sh" "${shell_detect_args[@]}")"

echo "[ros1-bringup-check] shell parent=${PARENT_SHELL:-unknown} default=${DEFAULT_SHELL:-unknown} preferred=$PREFERRED_SHELL"
if [[ -n "$ROS_SETUP" ]]; then
  echo "[ros1-bringup-check] source_ros=source $ROS_SETUP"
  # shellcheck disable=SC1090
  source "$ROS_SETUP"
else
  echo "[WARN] ROS setup file not found under /opt/ros/noetic" >&2
fi

if [[ -n "$workspace_root" ]]; then
  echo "[ros1-bringup-check] workspace_root=$workspace_root"
  echo "[ros1-bringup-check] package_count=$PACKAGE_COUNT"
  echo "[ros1-bringup-check] build_tool=$build_tool"
  echo "[ros1-bringup-check] build_command=$build_command"
else
  echo "[WARN] no catkin workspace detected from ${workspace_path:A}" >&2
fi

if [[ -n "$workspace_setup" && -f "$workspace_setup" ]]; then
  echo "[ros1-bringup-check] source_workspace=source $workspace_setup"
  # shellcheck disable=SC1090
  source "$workspace_setup"
fi

env_check_args=()
if [[ -n "$workspace_root" ]]; then
  env_check_args=(--workspace "$workspace_root")
fi
zsh "$script_dir/ros1_env_check.sh" "${env_check_args[@]}"

if [[ -n "$workspace_root" ]]; then
  echo "[ros1-bringup-check] launch_candidates:"
  zsh "$script_dir/ros1_launch_discover.sh" --path "$workspace_root" ${launch_pattern:+--pattern "$launch_pattern"} || true
  echo "[ros1-bringup-check] next_step=run '$build_command' in $workspace_root, then choose a launch command above"
else
  echo "[ros1-bringup-check] next_step=locate or create a catkin workspace before bringup"
fi
