#!/usr/bin/env bash
# Lossless GIF optimization for VHS recordings.
#
# VHS writes full, undeduplicated frames, so a short terminal demo routinely
# lands at 10-20 MB even though almost nothing changes between frames. This
# runs `gifsicle -O3` (lossless inter-frame transparency optimization — no
# --lossy, no colour quantization), which is typically a 20-30x reduction
# with ZERO pixel changes. That's the difference between a GIF you can put on
# a web page and one you can't.
#
# Best-effort: if gifsicle isn't installed, the GIF is left untouched and you
# get an install hint rather than a hard failure — so this is safe to wire
# into a capture pipeline that may run on machines without gifsicle.
#
# Usage:
#   optimize_gif.sh path/to/demo.gif [more.gif ...]
#
# Exit status is 0 even when gifsicle is missing (best-effort by design).

set -euo pipefail

if ! command -v gifsicle >/dev/null 2>&1; then
  echo "· gifsicle not found — GIF(s) left unoptimized (install: brew install gifsicle)" >&2
  exit 0
fi

if [ "$#" -eq 0 ]; then
  echo "usage: optimize_gif.sh <file.gif> [file.gif ...]" >&2
  exit 2
fi

# Portable byte-size of a file (macOS stat vs GNU stat).
filesize() {
  if stat -f%z "$1" >/dev/null 2>&1; then stat -f%z "$1"; else stat -c%s "$1"; fi
}

human() { awk -v n="$1" 'BEGIN { printf (n < 1048576 ? "%.0f KB" : "%.1f MB"), (n < 1048576 ? n/1024 : n/1048576) }'; }

for gif in "$@"; do
  if [ ! -f "$gif" ]; then
    echo "· skip (not found): $gif" >&2
    continue
  fi
  before=$(filesize "$gif")
  # --batch optimizes in place. -O3 is the most aggressive *lossless* level.
  gifsicle -O3 --batch "$gif"
  after=$(filesize "$gif")
  echo "· $(basename "$gif"): $(human "$before") → $(human "$after") (lossless -O3)"
done
