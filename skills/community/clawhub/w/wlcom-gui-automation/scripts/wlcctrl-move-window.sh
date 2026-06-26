#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage: wlcctrl-move-window.sh <window_uuid> <x> <y>

Move a wlcctrl window to logical screen coordinates and verify geometry.
Do not multiply x/y by output scale; wlcctrl --windowmove uses logical coordinates.
EOF
}

if [[ ${1:-} == "-h" || ${1:-} == "--help" ]]; then
  usage
  exit 0
fi
if [[ $# -lt 3 ]]; then
  usage
  exit 2
fi

uuid=$1
x=$2
y=$3

echo "$ wlcctrl --getwindowgeometry $uuid"
wlcctrl --getwindowgeometry "$uuid" 2>&1 || true

echo "$ wlcctrl --windowmove $uuid -x $x -y $y"
wlcctrl --windowmove "$uuid" -x "$x" -y "$y" 2>&1
sleep 0.3

echo "$ wlcctrl --getwindowgeometry $uuid"
wlcctrl --getwindowgeometry "$uuid" 2>&1
