#!/bin/bash
# qwen-asr runner — 自动音频预处理 + 离线语音识别
# Usage: .skill qwen-asr --audio <file> [--model small|large] [--threads <n>]
# model default: small (0.6B), threads default: all CPUs

set -euo pipefail

# ====== 参数解析 ======
AUDIO=""
MODEL="small"
THREADS=""
MODEL_DIR=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --audio)
      AUDIO="$2"
      shift 2
      ;;
    --model)
      MODEL="$2"
      shift 2
      ;;
    --threads)
      THREADS="$2"
      shift 2
      ;;
    *)
      echo "Unknown option: $1" >&2
      exit 1
      ;;
  esac
done

if [[ -z "$AUDIO" ]]; then
  echo "Usage: .skill qwen-asr --audio <file> [--model small|large] [--threads <n>]" >&2
  exit 1
fi

if [[ ! -f "$AUDIO" ]]; then
  echo "Error: Audio file not found: $AUDIO" >&2
  exit 1
fi

# ====== 检查 qwen-asr 仓库 & 编译产物 ======
REPO_DIR="$HOME/.openclaw/workspace/qwen-asr"
BIN="$REPO_DIR/qwen_asr"
MODEL_BASE="qwen3-asr-0.6b"

if [[ "$MODEL" == "large" ]]; then
  MODEL_BASE="qwen3-asr-1.7b"
fi

MODEL_DIR="$REPO_DIR/$MODEL_BASE"

if [[ ! -d "$REPO_DIR" ]]; then
  echo "Error: qwen-asr repo not found at $REPO_DIR. Run: git clone https://github.com/antirez/qwen-asr ~/.openclaw/workspace/qwen-asr" >&2
  exit 1
fi

if [[ ! -x "$BIN" ]]; then
  echo "Warning: qwen_asr binary not found. Building with 'make blas'..." >&2
  cd "$REPO_DIR"
  make blas 2>&1 || { echo "Build failed."; exit 1; }
fi

if [[ ! -d "$MODEL_DIR" ]] || [[ ! -f "$MODEL_DIR/config.json" ]]; then
  echo "Model not found at $MODEL_DIR. Starting download (requires internet)..." >&2
  cd "$REPO_DIR"
  # download_model.sh 需 TTY 交互，无法 piping；此处提示用户手动运行
  echo "Please run manually in terminal:"
  echo "  cd ~/.openclaw/workspace/qwen-asr && ./download_model.sh"
  echo "Then select: $MODEL_BASE"
  exit 1
fi

# ====== 音频预处理（FFmpeg） ======
TEMP_WAV=$(mktemp)/input.wav
mkdir -p "$(dirname "$TEMP_WAV")"

if [[ "${AUDIO##*.}" != "wav" ]]; then
  echo "Converting $AUDIO → 16kHz/mono/WAV..." >&2
else
  echo "Validating $AUDIO (16kHz/mono/WAV check)..." >&2
fi

ffmpeg -y -i "$AUDIO" -ar 16000 -ac 1 -f wav -hide_banner -loglevel error "$TEMP_WAV"

# ====== 推理 ======
ARGS=("-d" "$MODEL_DIR" "-i" "$TEMP_WAV")
[[ -n "$THREADS" ]] && ARGS+=("-t" "$THREADS")

echo "Running inference..." >&2
cd "$REPO_DIR"
"$BIN" "${ARGS[@]}"

rm -f "$TEMP_WAV"
