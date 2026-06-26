#!/usr/bin/env zsh
set -euo pipefail

if [[ $# -lt 3 ]]; then
  echo "Usage: $0 <topic|service> <name> <expected_type>"
  echo "Example: $0 topic /cmd_vel geometry_msgs/Twist"
  exit 2
fi

kind="$1"
name="$2"
expected="$3"

case "$kind" in
  topic)
    if ! rostopic type "$name" >/dev/null 2>&1; then
      echo "[ERROR] topic not found: $name"
      exit 1
    fi
    actual="$(rostopic type "$name")"
    ;;
  service)
    if ! rosservice type "$name" >/dev/null 2>&1; then
      echo "[ERROR] service not found: $name"
      exit 1
    fi
    actual="$(rosservice type "$name")"
    ;;
  *)
    echo "[ERROR] kind must be topic or service"
    exit 2
    ;;
esac

if [[ "$actual" != "$expected" ]]; then
  echo "[ERROR] type mismatch for $kind $name"
  echo "  expected: $expected"
  echo "  actual:   $actual"
  exit 1
fi

echo "[OK] $kind $name type matches: $actual"
