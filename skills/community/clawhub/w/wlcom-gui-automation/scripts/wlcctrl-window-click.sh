#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage: wlcctrl-window-click.sh <window_uuid> <relative_x> <relative_y> [button]

Click a point relative to a wlcctrl window capture coordinate system.
- Reads window geometry from wlcctrl --getwindowgeometry.
- Reads output scale from wlcctrl --getdisplaygeometry of the first output.
- Converts logical screen coordinates to scaled wlcctrl --mousemove input.
- Verifies location with wlcctrl --getmouselocation, then clicks.

Example:
  wlcctrl-window-click.sh <uuid> 376 593 1
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
rx=$2
ry=$3
button=${4:-1}

need() { command -v "$1" >/dev/null 2>&1 || { echo "missing command: $1" >&2; exit 127; }; }
need wlcctrl
need awk
need sed

geom_out=$(wlcctrl --getwindowgeometry "$uuid" 2>&1)
echo "$ geom: wlcctrl --getwindowgeometry $uuid"
echo "$geom_out"

geom=$(printf '%s\n' "$geom_out" | sed -n 's/.*geometry: (\([0-9]\+\), *\([0-9]\+\)) *\([0-9]\+\) x *\([0-9]\+\).*/\1 \2 \3 \4/p' | tail -1)
if [[ -z $geom ]]; then
  echo "failed to parse window geometry" >&2
  exit 1
fi
read -r wx wy ww wh <<<"$geom"

outputs_out=$(wlcctrl --outputs 2>&1)
output_uuid=$(printf '%s\n' "$outputs_out" | sed -n 's/^output "\([^"]*\)"/\1/p' | head -1)
if [[ -z $output_uuid ]]; then
  echo "failed to find output uuid" >&2
  echo "$outputs_out" >&2
  exit 1
fi

disp_out=$(wlcctrl --getdisplaygeometry "$output_uuid" 2>&1)
echo "$ display: wlcctrl --getdisplaygeometry $output_uuid"
echo "$disp_out"
scale=$(printf '%s\n' "$disp_out" | sed -n 's/.*scale: *\([0-9.]*\).*/\1/p' | tail -1)
if [[ -z $scale ]]; then
  echo "failed to parse output scale" >&2
  exit 1
fi

logical_x=$(awk -v a="$wx" -v b="$rx" 'BEGIN{printf "%d", a+b}')
logical_y=$(awk -v a="$wy" -v b="$ry" 'BEGIN{printf "%d", a+b}')
move_x=$(awk -v v="$logical_x" -v s="$scale" 'BEGIN{printf "%d", v*s + 0.5}')
move_y=$(awk -v v="$logical_y" -v s="$scale" 'BEGIN{printf "%d", v*s + 0.5}')

echo "# window=($wx,$wy) ${ww}x${wh}, relative=($rx,$ry), logical=($logical_x,$logical_y), scale=$scale, mousemove=($move_x,$move_y)"
echo "$ wlcctrl --mousemove ${move_x},${move_y}"
wlcctrl --mousemove "${move_x},${move_y}" 2>&1

echo "$ wlcctrl --getmouselocation"
wlcctrl --getmouselocation 2>&1

echo "$ wlcctrl --mousebutton $button"
wlcctrl --mousebutton "$button" 2>&1
