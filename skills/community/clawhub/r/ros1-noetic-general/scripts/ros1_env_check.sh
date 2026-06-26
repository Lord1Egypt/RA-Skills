#!/usr/bin/env zsh
set -euo pipefail

script_dir="${0:A:h}"
workspace=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --workspace)
      workspace="${2:?missing workspace}"
      shift 2
      ;;
    --help|-h)
      echo "Usage: ros1_env_check.sh [--workspace <path>]"
      exit 0
      ;;
    *)
      echo "[ERROR] unknown argument: $1" >&2
      exit 2
      ;;
  esac
done

if [[ -n "$workspace" ]]; then
  eval "$("$script_dir/ros1_shell_detect.sh" --workspace "$workspace" --export)"
else
  eval "$("$script_dir/ros1_shell_detect.sh" --export)"
fi

echo "[ros1-env-check] start"
echo "[INFO] detected shells: parent=${PARENT_SHELL:-unknown} default=${DEFAULT_SHELL:-unknown} preferred=$PREFERRED_SHELL"
if [[ -n "$ROS_SETUP" ]]; then
  echo "[INFO] suggested ROS source command: source $ROS_SETUP"
fi
if [[ -n "${WORKSPACE_SETUP:-}" ]]; then
  echo "[INFO] detected workspace setup file: $WORKSPACE_SETUP"
fi

if ! command -v roscore >/dev/null 2>&1; then
  echo "[ERROR] roscore not found in PATH."
  if [[ -n "$ROS_SETUP" ]]; then
    echo "[ERROR] Source ROS first: source $ROS_SETUP"
  fi
  exit 1
fi

echo "[OK] roscore found: $(command -v roscore)"

if ! command -v rostopic >/dev/null 2>&1; then
  echo "[ERROR] rostopic not found in PATH"
  exit 1
fi

echo "[OK] rostopic found: $(command -v rostopic)"

if ! rosnode list >/dev/null 2>&1; then
  echo "[WARN] Cannot query rosnode list (roscore may be down)"
else
  echo "[OK] ROS master reachable"
fi

echo "[INFO] sample topics (cmd/odom/bridge):"
rostopic list 2>/dev/null | grep -E 'cmd_vel|odom|Odometry|rosbridge' || true

echo "[ros1-env-check] done"
