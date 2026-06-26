#!/usr/bin/env zsh
set -euo pipefail

if [[ $# -lt 1 ]]; then
  echo "Usage: $0 <topic|service|node> [name-pattern]"
  echo "Example: $0 topic cmd_vel"
  exit 2
fi

kind="$1"
pattern="${2:-}"

case "$kind" in
  topic)
    cmd="rostopic list"
    ;;
  service)
    cmd="rosservice list"
    ;;
  node)
    cmd="rosnode list"
    ;;
  *)
    echo "Unsupported kind: $kind (use topic|service|node)"
    exit 2
    ;;
esac

if ! eval "$cmd" >/dev/null 2>&1; then
  echo "ERROR: unable to query ROS graph; ensure ROS env is sourced and roscore is running"
  exit 1
fi

if [[ -n "$pattern" ]]; then
  eval "$cmd" | grep -E "$pattern" || true
else
  eval "$cmd"
fi
