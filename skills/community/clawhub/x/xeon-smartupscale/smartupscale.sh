#!/usr/bin/env bash
# Smart video upscale: lanczos pre-scale + N rounds of ETDS 2x super-resolution
#
# Pipeline:
#   - Pick smallest N such that 2^N >= max(target_w/in_w, target_h/in_h)
#   - Round target to multiple of 2^N (preserves AR if user gave only -t HEIGHT)
#   - Lanczos input -> (target_w / 2^N, target_h / 2^N)
#   - Run ETDS x2 N times, doubling each time, landing on target
set -euo pipefail

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

INPUT=""
TARGET="1080p"
OUTPUT=""
KEEP_INTERMEDIATE=0

usage() {
  cat <<EOF
Usage: $(basename "$0") <input_video> [-t <target>] [-o <output>] [--keep]

  -t, --target   Target: 480p|540p|720p|1080p|1440p|2160p|4k|WxH (default: 1080p)
                 With WxH the aspect ratio is taken as-is (may stretch).
                 With a height-only preset the width is auto-computed from the
                 input aspect ratio.
  -o, --output   Output path (default: <input>_smart_<W>x<H>.mp4)
      --keep     Keep intermediate stage files
  -h, --help     Show this help
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    -t|--target) TARGET="$2"; shift 2;;
    -o|--output) OUTPUT="$2"; shift 2;;
    --keep) KEEP_INTERMEDIATE=1; shift;;
    -h|--help) usage; exit 0;;
    -*) echo "Unknown option: $1" >&2; usage; exit 2;;
    *) INPUT="$1"; shift;;
  esac
done

[[ -z "$INPUT" ]] && { echo "Error: input video required" >&2; usage; exit 2; }
[[ ! -f "$INPUT" ]] && { echo "Error: input not found: $INPUT" >&2; exit 1; }

FFMPEG="$DIR/bin/ffmpeg"
FFPROBE="$DIR/bin/ffprobe"
if [[ ! -x "$FFMPEG" || ! -x "$FFPROBE" ]]; then
  if command -v ffmpeg &>/dev/null && command -v ffprobe &>/dev/null; then
    FFMPEG="$(command -v ffmpeg)"
    FFPROBE="$(command -v ffprobe)"
  else
    echo "Error: ffmpeg/ffprobe not found. Run install.sh first." >&2
    exit 1
  fi
fi

if [[ -f "$DIR/.venv/bin/activate" ]]; then
  # shellcheck disable=SC1091
  source "$DIR/.venv/bin/activate"
fi
PYTHON="${PYTHON:-python3}"

# --- Parse target ---
target_h=0
target_w_explicit=0
case "$TARGET" in
  4k|4K|2160p) target_h=2160;;
  1440p|2k|2K) target_h=1440;;
  1080p|fhd|FHD) target_h=1080;;
  720p|hd|HD) target_h=720;;
  540p) target_h=540;;
  480p) target_h=480;;
  *x*) target_w_explicit="${TARGET%x*}"; target_h="${TARGET#*x}";;
  *) echo "Error: unrecognized target '$TARGET'" >&2; exit 2;;
esac

# --- Probe input ---
_dims="$("$FFPROBE" -v error -select_streams v:0 \
  -show_entries stream=width,height -of default=nw=1:nk=1 "$INPUT" | tr '\n' ' ')"
read -r in_w in_h <<<"$_dims"
[[ -z "$in_w" || -z "$in_h" ]] && { echo "Error: probe failed" >&2; exit 1; }

# --- Compute target width preserving AR (unless explicit) ---
if [[ "$target_w_explicit" -gt 0 ]]; then
  target_w="$target_w_explicit"
else
  target_w=$(( (in_w * target_h / in_h + 1) / 2 * 2 ))
fi

# --- Already at or above target? Just lanczos to target. ---
if (( in_w >= target_w && in_h >= target_h )); then
  # round to even
  (( target_w % 2 != 0 )) && target_w=$(( target_w + 1 ))
  (( target_h % 2 != 0 )) && target_h=$(( target_h + 1 ))
  if [[ -z "$OUTPUT" ]]; then
    OUTPUT="${INPUT%.*}_smart_${target_w}x${target_h}.mp4"
  fi
  OUTPUT="$(realpath -m "$OUTPUT")"
  echo "Input ${in_w}x${in_h} >= target ${target_w}x${target_h}; lanczos only."
  "$FFMPEG" -y -i "$INPUT" \
    -vf "scale=${target_w}:${target_h}:flags=lanczos" \
    -c:v libx264 -preset medium -crf 18 -pix_fmt yuv420p \
    -c:a aac -movflags +faststart "$OUTPUT"
  echo "Saved: $OUTPUT"
  exit 0
fi

# --- Decide number of ETDS x2 passes (n) ---
# n = largest int with input * 2^n <= target  (i.e. floor(log2(target/input)))
# Use the smaller of the two ratios so neither dim overshoots.
n=0
while (( (in_w * (1 << (n + 1))) <= target_w && (in_h * (1 << (n + 1))) <= target_h )); do
  n=$(( n + 1 ))
  (( n >= 4 )) && break    # cap at 16x
done

scale=$(( 1 << n ))      # 2^n  (1 if n=0)
# Need target divisible by 2^(n+1) so every intermediate stage is even (libx264).
align=$(( scale * 2 ))
target_w=$(( (target_w + align - 1) / align * align ))
target_h=$(( (target_h + align - 1) / align * align ))

mid_w=$(( target_w / scale ))
mid_h=$(( target_h / scale ))

echo "Input:        ${in_w}x${in_h}"
echo "Target:       ${target_w}x${target_h}  ($TARGET)"
echo "ETDS passes:  $n  (each x2)"
echo "Pre-scale:    lanczos -> ${mid_w}x${mid_h}"

# --- Output path ---
if [[ -z "$OUTPUT" ]]; then
  OUTPUT="${INPUT%.*}_smart_${target_w}x${target_h}.mp4"
fi
OUTPUT="$(realpath -m "$OUTPUT")"

TMPDIR_X="$(mktemp -d)"
trap 'rm -rf "$TMPDIR_X"' EXIT

# --- Stage 0: lanczos to mid (or skip if input already matches) ---
stage_file="$TMPDIR_X/stage0.mp4"
cur_w="$mid_w"; cur_h="$mid_h"

if (( in_w == mid_w && in_h == mid_h )); then
  echo "[stage 0] input already at ${mid_w}x${mid_h}, skipping lanczos."
  stage_file="$INPUT"
else
  echo "[stage 0] lanczos ${in_w}x${in_h} -> ${mid_w}x${mid_h}"
  "$FFMPEG" -y -loglevel warning -stats -i "$INPUT" \
    -vf "scale=${mid_w}:${mid_h}:flags=lanczos" \
    -c:v libx264 -preset medium -crf 18 -pix_fmt yuv420p \
    -c:a copy "$stage_file"
fi

# --- Stages 1..n: ETDS x2 ---
for ((i=1; i<=n; i++)); do
  next_w=$(( cur_w * 2 ))
  next_h=$(( cur_h * 2 ))
  if (( i == n )); then
    next_file="$OUTPUT"
  else
    next_file="$TMPDIR_X/stage${i}.mp4"
  fi
  echo "[stage $i] ETDS x2  ${cur_w}x${cur_h} -> ${next_w}x${next_h}"
  "$PYTHON" "$DIR/sr_video_ov.py" "$stage_file" -o "$next_file"
  if (( KEEP_INTERMEDIATE == 1 )) && (( i < n )); then
    keep="${OUTPUT%.*}_stage${i}_${next_w}x${next_h}.mp4"
    cp "$next_file" "$keep"
    echo "Stage $i kept: $keep"
  fi
  stage_file="$next_file"
  cur_w="$next_w"; cur_h="$next_h"
done

if (( KEEP_INTERMEDIATE == 1 )) && [[ -f "$TMPDIR_X/stage0.mp4" ]]; then
  keep="${OUTPUT%.*}_stage0_${mid_w}x${mid_h}.mp4"
  cp "$TMPDIR_X/stage0.mp4" "$keep"
  echo "Stage 0 kept: $keep"
fi

echo "Saved: $OUTPUT"
