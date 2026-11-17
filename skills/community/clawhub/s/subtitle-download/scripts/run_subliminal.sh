#!/bin/bash
# Podman-based Subliminal batch subtitle download for a media library of organized
# movie folders.
# Mounts RW (subliminal must write). Pre-existing subs are tagged .en.srt so they're
# skipped; new downloads get .en.srt too, then we strip .en for exact-stem matching.
#
# Usage: MOVIES=/path/to/Movies bash run_subliminal.sh
#   (defaults MOVIES to /path/to/Movies)
#
# What it does:
#   1. podman volume create subliminal_cache (persists provider responses -> avoids rate-limit bans)
#   2. pull ghcr.io/diaoul/subliminal:latest if missing
#   3. pre-tag every existing *.srt as *.en.srt so subliminal skips already-subtitled movies
#   4. run `subliminal download -l en` with READ-WRITE mount (NOT :ro) and --age 3650d
#   5. strip .en from all *.srt so filenames match video stems exactly
#   6. report final video<->srt stem mismatches (should be 0)
set -u
MOVIES="${MOVIES:-/path/to/Movies}"
LOG="${LOG:-/tmp/subliminal-run.log}"
exec > >(tee -a "$LOG") 2>&1

echo "=== $(date) subliminal pass (podman) ==="

podman volume create subliminal_cache 2>/dev/null || true

if ! podman images --format '{{.Repository}}:{{.Tag}}' | grep -q 'ghcr.io/diaoul/subliminal'; then
  echo '--- pulling image ---'
  podman pull ghcr.io/diaoul/subliminal:latest
fi

# Pre-tag existing subs as .en.srt so subliminal recognizes them and skips re-download
cd "$MOVIES"
find . -maxdepth 2 -type f -name '*.srt' ! -name '*.en.srt' \
  -exec sh -c 'mv "$1" "${1%.srt}.en.srt"' _ {} \;

# RW mount (NOT :ro). --age 3650d = treat all files as in scope.
podman run --rm \
  -v subliminal_cache:/usr/src/cache \
  -v "$MOVIES":/movies \
  ghcr.io/diaoul/subliminal:latest \
  download -l en --age 3650d /movies

echo "=== download pass exit: $? ==="

# Strip .en from every .srt so filenames match video stems exactly
cd "$MOVIES"
n=0
while IFS= read -r -d '' f; do
  mv "$f" "${f%.en.srt}.srt"
  n=$((n+1))
done < <(find . -maxdepth 2 -type f -name '*.en.srt' -print0)
echo "Stripped .en from $n subtitle files."

# Stray .ass/.sub -> .srt via ffmpeg (best effort; keep original if conversion fails)
while IFS= read -r -d '' f; do
  out="${f%.*}.srt"
  fmt=""; case "$f" in *.ass) fmt="-f ass";; esac
  if ffmpeg -y $fmt -i "$f" "$out" >/dev/null 2>&1 && [ -s "$out" ]; then
    rm -f "$f"; echo "Converted $(basename "$f") -> $(basename "$out")"
  else
    echo "WARN: could not convert $(basename "$f") (kept as-is)"
  fi
done < <(find . -maxdepth 2 -type f \( -name '*.ass' -o -name '*.sub' \) -print0)

# Final stem-mismatch report (video stem vs srt stem only)
mm=0
while IFS= read -r -d '' d; do
  v=$(find "$d" -maxdepth 1 -type f \( -name '*.mp4' -o -name '*.mkv' -o -name '*.avi' -o -name '*.mov' -o -name '*.mpg' -o -name '*.rmvb' \) -printf '%f\n' | head -1)
  [ -z "$v" ] && continue
  vstem="${v%.*}"
  while IFS= read -r -d '' s; do
    sstem=$(basename "$s"); sstem="${sstem%.*}"
    [ "$vstem" != "$sstem" ] && { echo "MISMATCH: $d -> '$vstem' vs '$sstem'"; mm=$((mm+1)); }
  done < <(find "$d" -maxdepth 1 -type f -name '*.srt' -print0)
done < <(find . -maxdepth 1 -type d ! -name '.' -print0)
echo "Final stem mismatches: $mm"
echo "=== $(date) done ==="
