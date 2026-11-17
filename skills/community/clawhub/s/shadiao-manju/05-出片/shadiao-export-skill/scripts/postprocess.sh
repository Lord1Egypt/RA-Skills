#!/usr/bin/env bash
# 成片收尾：竖屏 / 压缩 / 响度统一 / 抽封面
# 用法：
#   bash postprocess.sh in.mp4 out.mp4 [--ratio 9:16] [--crf 20] [--cover 3]
set -euo pipefail

IN=""
OUT=""
RATIO="9:16"
CRF="20"
COVER=""
LOUDNORM=1

while [ $# -gt 0 ]; do
  case "$1" in
    --ratio) RATIO="$2"; shift 2 ;;
    --crf) CRF="$2"; shift 2 ;;
    --cover) COVER="$2"; shift 2 ;;
    --no-loudnorm) LOUDNORM=0; shift ;;
    -h|--help)
      echo "用法：bash postprocess.sh in.mp4 out.mp4 [--ratio 9:16] [--crf 20] [--cover 3] [--no-loudnorm]"
      exit 0 ;;
    *)
      if [ -z "$IN" ]; then IN="$1"; elif [ -z "$OUT" ]; then OUT="$1"; else
        echo "多余的参数：$1" >&2; exit 2
      fi
      shift ;;
  esac
done

[ -n "$IN" ] && [ -n "$OUT" ] || { echo "用法：bash postprocess.sh in.mp4 out.mp4 [--ratio 9:16]" >&2; exit 2; }
[ -f "$IN" ] || { echo "找不到输入：$IN" >&2; exit 1; }
command -v ffmpeg >/dev/null || { echo "未安装 ffmpeg：brew install ffmpeg" >&2; exit 1; }

case "$RATIO" in
  9:16) W=1080; H=1920 ;;
  16:9) W=1920; H=1080 ;;
  1:1)  W=1080; H=1080 ;;
  4:5)  W=1080; H=1350 ;;
  *)    echo "不支持的 --ratio：$RATIO（9:16 / 16:9 / 1:1 / 4:5）" >&2; exit 2 ;;
esac

FILTER="scale=${W}:${H}:force_original_aspect_ratio=decrease,pad=${W}:${H}:(ow-iw)/2:(oh-ih)/2:color=black"

AF=""
if [ "$LOUDNORM" = "1" ]; then
  AF="loudnorm=I=-16:TP=-1.5:LRA=11"
fi

mkdir -p "$(dirname "$OUT")"

echo ">> 输入：${IN}"
echo ">> 输出：${OUT} (${W}x${H}, crf=${CRF})"

ARGS=(-y -i "$IN" -vf "$FILTER" -c:v libx264 -preset slow -crf "$CRF" -pix_fmt yuv420p)
if [ -n "$AF" ]; then
  ARGS+=(-af "$AF" -c:a aac -b:a 192k)
else
  ARGS+=(-c:a aac -b:a 192k)
fi
ARGS+=(-movflags +faststart "$OUT")

ffmpeg "${ARGS[@]}"

if [ -n "$COVER" ]; then
  COVER_OUT="$(dirname "$OUT")/cover.jpg"
  echo ">> 封面：${COVER_OUT} (第 ${COVER}s)"
  ffmpeg -y -ss "$COVER" -i "$OUT" -frames:v 1 -q:v 2 "$COVER_OUT" >/dev/null 2>&1
fi

echo ">> 完成"
ffprobe -v error -show_entries format=duration,size -of default=noprint_wrappers=1 "$OUT"
