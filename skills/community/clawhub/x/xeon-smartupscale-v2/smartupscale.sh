#!/usr/bin/env bash
set -euo pipefail

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

INPUT=""
OUTPUT=""
TARGET="1080p"

usage() {
  cat <<EOF2
Usage: $(basename "$0") <input_video> [-t <target>] [-o <output>]

  -t, --target   Target: 480p|540p|720p|1080p|1440p|2160p|4k|4320p|8k|WxH
                 (default: 1080p)
  -o, --output   Output path (default: <input>_smart_v2_<W>x<H>.mp4)
  -h, --help     Show this help
EOF2
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    -t|--target) TARGET="$2"; shift 2 ;;
    -o|--output) OUTPUT="$2"; shift 2 ;;
    -h|--help)   usage; exit 0 ;;
    -*)          echo "Unknown option: $1" >&2; usage; exit 2 ;;
    *)           INPUT="$1"; shift ;;
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

target_w=0
target_h=0
case "$TARGET" in
  8k|8K|4320p)   target_w=7680; target_h=4320 ;;
  4k|4K|2160p)   target_w=3840; target_h=2160 ;;
  1440p|2k|2K)   target_w=2560; target_h=1440 ;;
  1080p|fhd|FHD) target_w=1920; target_h=1080 ;;
  720p|hd|HD)    target_w=1280; target_h=720  ;;
  540p)          target_w=960;  target_h=540  ;;
  480p)          target_w=854;  target_h=480  ;;
  *x*)           target_w="${TARGET%x*}"; target_h="${TARGET#*x}" ;;
  *)             echo "Error: unrecognized target '$TARGET'" >&2; exit 2 ;;
esac
[[ "$target_w" =~ ^[0-9]+$ && "$target_h" =~ ^[0-9]+$ ]] || {
  echo "Error: invalid target '$TARGET'" >&2; exit 2; }

read -r in_w in_h <<<"$("$FFPROBE" -v error -select_streams v:0 \
  -show_entries stream=width,height -of default=nw=1:nk=1 "$INPUT" | tr '\n' ' ')"
[[ -n "$in_w" && -n "$in_h" ]] || { echo "Error: probe failed" >&2; exit 1; }

# Resolution planner. Hard constraints:
#   1) pre-scale height must not go below H_FLOOR (default 270)
#   2) super-resolution must be the LAST step (no lanczos after SR)
# Decision:
#   r = target_h / in_h
#   if r < SR_THRESHOLD: pure lanczos
#   else: pick n>=1 with pre_h = target_h / 4^n >= H_FLOOR,
#         pre_h closest to in_h. Then 1 lanczos + n consecutive x4.
plan="$("$PYTHON" - "$in_w" "$in_h" "$target_w" "$target_h" <<'PY'
import sys
in_w, in_h, t_w, t_h = (int(x) for x in sys.argv[1:5])
H_FLOOR = 270
SR_THRESHOLD = 2.0

r = t_h / in_h
candidates = []
for n in range(1, 6):
    ph = t_h / (4 ** n)
    pw = t_w / (4 ** n)
    if ph < H_FLOOR:
        break
    candidates.append((n, pw, ph))

if r < SR_THRESHOLD or not candidates:
    print("lanczos", 0, 0, 0, t_w, t_h)
else:
    n, pw, ph = min(candidates, key=lambda c: abs(c[2] - in_h))
    pw = int(round(pw / 2) * 2)
    ph = int(round(ph / 2) * 2)
    fw = pw * (4 ** n)
    fh = ph * (4 ** n)
    print("sr", n, pw, ph, fw, fh)
PY
)"

read -r mode n pre_w pre_h final_w final_h <<<"$plan"

if [[ -z "$OUTPUT" ]]; then
  OUTPUT="${INPUT%.*}_smart_v2_${final_w}x${final_h}.mp4"
fi
OUTPUT="$(realpath -m "$OUTPUT")"

echo "Input:  ${in_w}x${in_h}"
echo "Target: ${target_w}x${target_h} ($TARGET)"
echo "Plan:   mode=${mode} passes=${n} prescale=${pre_w}x${pre_h} final=${final_w}x${final_h}"

if [[ "$mode" == "lanczos" ]]; then
  echo "[stage 0] lanczos ${in_w}x${in_h} -> ${final_w}x${final_h}"
  "$FFMPEG" -y -loglevel warning -stats -i "$INPUT" \
    -vf "scale=${final_w}:${final_h}:flags=lanczos" \
    -c:v libx264 -preset medium -crf 15 -pix_fmt yuv420p \
    -c:a copy -movflags +faststart "$OUTPUT"
  echo "Saved: $OUTPUT"
  exit 0
fi

MODEL_XML="$DIR/model/realesr-general-x4v3_480x270.xml"
[[ -f "$MODEL_XML" ]] || { echo "Error: missing model $MODEL_XML. Run install.sh." >&2; exit 1; }

TMPDIR_X="$(mktemp -d)"
trap 'rm -rf "$TMPDIR_X"' EXIT

# Pass 1: in-memory lanczos to (pre_w, pre_h), then x4.
out1="$TMPDIR_X/pass1.mp4"
echo "[pass 1/$n] lanczos ${in_w}x${in_h} -> ${pre_w}x${pre_h}, then x4 -> $((pre_w * 4))x$((pre_h * 4))"
"$PYTHON" "$DIR/sr_video_ov.py" "$INPUT" -o "$out1" \
  --model "$MODEL_XML" --scale 4 \
  --prescale-width "$pre_w" --prescale-height "$pre_h"
current="$out1"
cur_w=$((pre_w * 4))
cur_h=$((pre_h * 4))

# Passes 2..n: chain x4 without lanczos (model reshapes to input size dynamically).
for ((i = 2; i <= n; i++)); do
  out_i="$TMPDIR_X/pass${i}.mp4"
  echo "[pass $i/$n] x4 ${cur_w}x${cur_h} -> $((cur_w * 4))x$((cur_h * 4))"
  "$PYTHON" "$DIR/sr_video_ov.py" "$current" -o "$out_i" \
    --model "$MODEL_XML" --scale 4
  current="$out_i"
  cur_w=$((cur_w * 4))
  cur_h=$((cur_h * 4))
done

# Final mux: take video from last SR pass, copy audio from the ORIGINAL input.
echo "[final] mux video (${cur_w}x${cur_h}) + original audio -> $OUTPUT"
"$FFMPEG" -y -loglevel warning -i "$current" -i "$INPUT" \
  -map 0:v:0 -map 1:a:0? \
  -c:v copy -c:a copy -shortest -movflags +faststart "$OUTPUT"

echo "Saved: $OUTPUT"
