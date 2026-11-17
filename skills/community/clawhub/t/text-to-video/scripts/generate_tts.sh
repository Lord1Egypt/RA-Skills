#!/usr/bin/env bash
# generate_tts.sh —— 批量 TTS 生成
# 用法:
#   generate_tts.sh <voice_plan.json> <output_dir>
#
# voice_plan.json 格式:
# {
#   "provider": "say",         # only local macOS say is supported
#   "voice": "longxiaobai",    # 音色
#   "speed": 1.0,
#   "scenes": [
#     { "id": "card-01", "text": "最近在看 AI 硬件..." },
#     { "id": "card-02", "text": "戒指也来了..." },
#     ...
#   ]
# }
#
# 输出:
#   <output_dir>/card-01.mp3, card-02.mp3, ...
#   合并: <output_dir>/full.mp3 (按 scenes 顺序串接)

set -euo pipefail

PLAN_FILE="$1"
OUT_DIR="$2"

if [[ -z "$PLAN_FILE" || -z "$OUT_DIR" ]]; then
  echo "usage: $0 <voice_plan.json> <output_dir>" >&2
  exit 1
fi

if [[ ! -f "$PLAN_FILE" ]]; then
  echo "ERROR: plan file does not exist" >&2
  exit 1
fi

case "$OUT_DIR" in
  /|""|.|..)
    echo "ERROR: choose a dedicated output directory" >&2
    exit 1
    ;;
esac

mkdir -p "$OUT_DIR"

# 解析 JSON（用 jq）
PROVIDER=$(jq -r '.provider' "$PLAN_FILE")
VOICE=$(jq -r '.voice' "$PLAN_FILE")
COUNT=$(jq '.scenes | length' "$PLAN_FILE")

echo "Provider: $PROVIDER"
echo "Voice: $VOICE"
echo "Scenes: $COUNT"
echo "Output: $OUT_DIR"

case "$PROVIDER" in
  say)
    for i in $(seq 0 $((COUNT-1))); do
      SID=$(jq -r ".scenes[$i].id" "$PLAN_FILE")
      TEXT=$(jq -r ".scenes[$i].text" "$PLAN_FILE")
      if [[ ! "$SID" =~ ^[A-Za-z0-9_-]+$ ]]; then
        echo "ERROR: scene id '$SID' must contain only letters, digits, _ or -" >&2
        exit 1
      fi
      AIFF="$OUT_DIR/${SID}.aiff"
      MP3="$OUT_DIR/${SID}.mp3"
      if [[ -e "$AIFF" || -e "$MP3" ]]; then
        echo "ERROR: refusing to overwrite existing scene output: $SID" >&2
        exit 1
      fi
      echo "  say [$SID] $TEXT"
      say -v "$VOICE" -o "$AIFF" "$TEXT"
      ffmpeg -y -loglevel error -i "$AIFF" -codec:a libmp3lame -qscale:a 2 "$MP3"
      rm "$AIFF"
    done
    ;;

  *)
    echo "ERROR: unknown provider '$PROVIDER' (only local 'say' is supported)" >&2
    exit 1
    ;;
esac

# 合并所有 mp3 到 full.mp3（用 ffmpeg concat demuxer）
echo ""
echo "Concatenating scenes..."
LIST_FILE=$(mktemp)
trap 'rm -f "$LIST_FILE"' EXIT
for i in $(seq 0 $((COUNT-1))); do
  SID=$(jq -r ".scenes[$i].id" "$PLAN_FILE")
  if [[ ! "$SID" =~ ^[A-Za-z0-9_-]+$ ]]; then
    echo "ERROR: scene id '$SID' must contain only letters, digits, _ or -" >&2
    exit 1
  fi
  echo "file '$OUT_DIR/${SID}.mp3'" >> "$LIST_FILE"
done
if [[ -e "$OUT_DIR/full.mp3" ]]; then
  echo "ERROR: refusing to overwrite existing full.mp3" >&2
  exit 1
fi
ffmpeg -n -loglevel error -f concat -safe 0 -i "$LIST_FILE" -c copy "$OUT_DIR/full.mp3"

echo ""
echo "Done. Files in $OUT_DIR:"
ls -lh "$OUT_DIR"
