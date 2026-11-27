#!/usr/bin/env bash
# Run a built K10 firmware in esp32sim and save what its screen shows.
# No board needed. Build first (pio run), then:
#
#   bash scripts/k10-sim.sh ../my-k10-project            # 3 emulated seconds, one PNG
#   bash scripts/k10-sim.sh ../my-k10-project 1.5        # custom duration
#   bash scripts/k10-sim.sh ../my-k10-project --script press.txt
#   bash scripts/k10-sim.sh --demo                       # build+run examples/smiley, 3 frames
#
# Options: --out PNG  --script FILE  --env NAME  --console uart0|usb|both|none  --show-console
#
# Script file lines are esp32sim host actions, e.g.
#   1.2 press btnA 200        press A for 200 ms at t=1.2 s
#   3.0 stop
# Environment: ESP32SIM=/path/to/esp32sim, ESP32SIM_ROM=/path/to/esp32s3_rev0_rom.elf
set -euo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
SKILL="$(cd "$HERE/.." && pwd)"
ORIG_PWD="$PWD"
PROJ=""; SECS="3.0"; OUT=""; SCRIPT=""; ENVNAME=""; CONSOLE="uart0"; DEMO=0; SHOW=0

while [ $# -gt 0 ]; do
  case "$1" in
    --demo)    DEMO=1; shift ;;
    --out)     OUT="$2"; shift 2 ;;
    --script)  SCRIPT="$2"; shift 2 ;;
    --env)     ENVNAME="$2"; shift 2 ;;
    --console) CONSOLE="$2"; shift 2 ;;
    --show-console) SHOW=1; shift ;;
    -h|--help) sed -n '2,15p' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
    -*)        printf 'unknown option: %s\n' "$1" >&2; exit 2 ;;
    *)         if [ -z "$PROJ" ]; then PROJ="$1"; else SECS="$1"; fi; shift ;;
  esac
done

# ---- simulator binary ------------------------------------------------------
SIM="${ESP32SIM:-}"
if [ -z "$SIM" ]; then
  for c in "$HOME/.k10-esp32sim/target/release/esp32sim.exe" \
           "$HOME/.k10-esp32sim/target/release/esp32sim" \
           "$SKILL/../esp32sim-main/target/release/esp32sim.exe" \
           "$SKILL/../esp32sim-main/target/release/esp32sim"; do
    [ -x "$c" ] && SIM="$c" && break
  done
fi
[ -n "$SIM" ] && [ -x "$SIM" ] || {
  printf 'esp32sim not found. Build it once with:\n  bash %s/k10-sim-setup.sh\n' "$HERE" >&2; exit 1; }

# ---- mask ROM ELF ---------------------------------------------------------
ROM="${ESP32SIM_ROM:-}"
if [ -z "$ROM" ]; then
  for c in "$HOME/.platformio/packages/tool-esp-rom-elfs/esp32s3_rev0_rom.elf" \
           "$HOME"/.espressif/tools/esp-rom-elfs/*/esp32s3_rev0_rom.elf; do
    [ -f "$c" ] && ROM="$c" && break
  done
fi
[ -n "$ROM" ] && [ -f "$ROM" ] || {
  printf 'esp32s3_rev0_rom.elf not found. It ships with the K10 PlatformIO packages;\npoint at it with ESP32SIM_ROM=/path/to/esp32s3_rev0_rom.elf\n' >&2; exit 1; }
# The ROM lives outside the project tree, so it keeps an absolute path; a Windows
# esp32sim.exe cannot read an MSYS path like /c/Users/...
case "$SIM" in *.exe) command -v cygpath >/dev/null && ROM="$(cygpath -w "$ROM")" ;; esac

# ---- demo mode ------------------------------------------------------------
if [ "$DEMO" = 1 ]; then
  PROJ="$SKILL/examples/smiley"
  printf '==> building examples/smiley (pio run)\n'
  # cd instead of `pio run -d`: a native Windows pio cannot open an MSYS path like /c/Users/...
  ( cd "$PROJ" && pio run >/dev/null ) || { printf 'build failed\n' >&2; exit 1; }
  mkdir -p "$PROJ/sim"
  bash "$HERE/k10-sim.sh" "$PROJ" 3.00 --out sim/01-smile.png
  bash "$HERE/k10-sim.sh" "$PROJ" 3.26 --out sim/02-blink.png
  printf '1.2 press btnA 200\n' > "$PROJ/sim/actions.txt"
  bash "$HERE/k10-sim.sh" "$PROJ" 3.00 --out sim/03-laugh.png --script "$PROJ/sim/actions.txt"
  printf '==> frames in %s/sim\n' "$PROJ"
  exit 0
fi

[ -n "$PROJ" ] || { printf 'usage: bash k10-sim.sh <project-dir> [seconds]\n' >&2; exit 2; }

# Run from inside the project and pass relative paths: that works with both the
# native Windows binary and POSIX builds.
cd "$PROJ"

# ---- locate the build -----------------------------------------------------
if [ -n "$ENVNAME" ]; then
  BUILD=".pio/build/$ENVNAME"
else
  BUILD=""
  for d in .pio/build/*/; do
    [ -f "${d}firmware.bin" ] && BUILD="${d%/}" && break
  done
fi
[ -n "$BUILD" ] && [ -f "$BUILD/firmware.bin" ] || {
  printf 'no firmware.bin under %s/.pio/build - run `pio run` first\n' "$PWD" >&2; exit 1; }
for f in bootloader.bin partitions.bin; do
  [ -f "$BUILD/$f" ] || { printf 'missing %s in %s\n' "$f" "$BUILD" >&2; exit 1; }
done

mkdir -p sim
[ -n "$OUT" ] || OUT="sim/sim-${SECS}s.png"
EXTRA=()
if [ -n "$SCRIPT" ]; then
  # Resolve against the caller's directory, then keep a copy inside the project so the
  # emulator only ever sees a path relative to the firmware it is booting.
  sd="$(dirname "$SCRIPT")"; sb="$(basename "$SCRIPT")"
  script_abs="$(cd "$ORIG_PWD" && cd "$sd" && pwd)/$sb"
  [ -f "$script_abs" ] || { printf 'script not found: %s\n' "$SCRIPT" >&2; exit 1; }
  [ "$script_abs" = "$PWD/sim/actions.txt" ] || cp "$script_abs" sim/actions.txt
  EXTRA=(--script sim/actions.txt)
fi

# ---- run ------------------------------------------------------------------
# K10 = ESP32-S3, 16 MB flash, 8 MB PSRAM. The report line is printed at exit.
if [ "$SHOW" = 1 ]; then
  "$SIM" --board unihiker-k10 --boot rom --rom "$ROM" \
    --bootloader "$BUILD/bootloader.bin" --ptable "$BUILD/partitions.bin" \
    --app "$BUILD/firmware.bin" --flash-mb 16 --psram-mb 8 \
    --console "$CONSOLE" --no-dump --max-seconds "$SECS" ${EXTRA[@]+"${EXTRA[@]}"} \
    --tft-png "$OUT" 2>&1
else
  # Default: only the verdict, not the boot log and the "device not found" chatter.
  "$SIM" --board unihiker-k10 --boot rom --rom "$ROM" \
    --bootloader "$BUILD/bootloader.bin" --ptable "$BUILD/partitions.bin" \
    --app "$BUILD/firmware.bin" --flash-mb 16 --psram-mb 8 \
    --console "$CONSOLE" --no-dump --max-seconds "$SECS" ${EXTRA[@]+"${EXTRA[@]}"} \
    --tft-png "$OUT" 2>&1 | grep -E 'k10 tft|\[emu\] stop|panic|assert|Guru Meditation|Backtrace' || true
fi
printf '  -> %s\n' "$PWD/$OUT"
