#!/usr/bin/env bash
# Local test helper for xiaomi-mimo-tts
# Usage: ./scripts/test_local.sh [--mock]

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/_env.sh"

TEXT="示例：你好，测试语音生成。"
OUTPUT="${1:-$SCRIPT_DIR/../output.mock.ogg}"

MOCK=0
if [ "$1" = "--mock" ] || [ -z "${XIAOMI_API_KEY}" ]; then
  MOCK=1
fi

if [ "$MOCK" -eq 1 ]; then
  echo "运行 mock 模式：不会调用外部 API，生成占位音频"
  # create a short silent ogg as placeholder
  if command -v ffmpeg &> /dev/null; then
    ffmpeg -f lavfi -i anullsrc=r=16000:cl=mono -t 0.5 -q:a 9 -acodec libvorbis "$OUTPUT" -y >/dev/null 2>&1 || true
  else
    # fallback: create empty file
    printf '' > "$OUTPUT"
  fi
  echo "mock output: $OUTPUT"
  exit 0
fi

# Real mode: call entry script
bash "$SCRIPT_DIR/mimo-tts.sh" "$TEXT" "$OUTPUT"

if [ $? -eq 0 ]; then
  echo "生成文件： $OUTPUT"
else
  echo "生成失败" >&2
  exit 2
fi
