#!/usr/bin/env bash
# run.sh — Video Analyzer 主编排脚本（三阶段）
#
# Stage 1: Input → 并行启动 visual.py（抽帧+视觉观测）和 transcribe.py（音频观测）
# Stage 2: 等待两者完成，产出 observations_visual.json + observations_audio.json
# Stage 3: （可选）调用 analyze.py 合成 metadata.json
#
# 用法:
#   bash run.sh --video <video> --output <dir> [options]
#

set -euo pipefail

# Default timeout: 1 hour (covers frame extraction + LLM analysis for long videos)
# Override via environment: VA_TIMEOUT=3600
: "${VA_TIMEOUT:=3600}"
if [[ -z "${_VA_TIMEOUT_SET:-}" ]]; then
  export _VA_TIMEOUT_SET=1
  exec timeout "$VA_TIMEOUT" "$0" "$@"
fi

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# 默认值
VIDEO=""
OUTPUT=""
INTERVAL=""  # deprecated: auto-calculated per segment
MAX_FRAMES=15
KEEP_FRAMES=false
TRANSCRIBE_MODE="skip"
WHISPER_MODEL="base"
WHISPER_API_KEY=""
WHISPER_API_BASE=""
VISION_LLM_KEY=""
VISION_LLM_BASE=""
VISION_LLM_MODEL=""
AUDIO_LLM_KEY=""
AUDIO_LLM_BASE=""
AUDIO_LLM_MODEL=""
ANALYZE_LLM_KEY=""
ANALYZE_LLM_BASE=""
ANALYZE_LLM_MODEL=""
SYNTHESIZE_METHOD=""

while [[ $# -gt 0 ]]; do
  case $1 in
    --video)              VIDEO="$2"; shift 2 ;;
    --output)             OUTPUT="$2"; shift 2 ;;
    --max-frames)        MAX_FRAMES="$2"; shift 2 ;;
    --interval)
      shift 2 ;;  # deprecated, ignored
    --keep-frames)        KEEP_FRAMES=true; shift ;;
    --transcribe)         TRANSCRIBE_MODE="$2"; shift 2 ;;
    --whisper-model)      WHISPER_MODEL="$2"; shift 2 ;;
    --whisper-api-key)   WHISPER_API_KEY="$2"; shift 2 ;;
    --whisper-api-base)  WHISPER_API_BASE="$2"; shift 2 ;;
    --vision-llm-key)     VISION_LLM_KEY="$2"; shift 2 ;;
    --vision-llm-base)    VISION_LLM_BASE="$2"; shift 2 ;;
    --vision-llm-model)   VISION_LLM_MODEL="$2"; shift 2 ;;
    --audio-llm-key)      AUDIO_LLM_KEY="$2"; shift 2 ;;
    --audio-llm-base)     AUDIO_LLM_BASE="$2"; shift 2 ;;
    --audio-llm-model)    AUDIO_LLM_MODEL="$2"; shift 2 ;;
    --synthesize-method)  SYNTHESIZE_METHOD="$2"; shift 2 ;;
    --analyze-llm-key)    ANALYZE_LLM_KEY="$2"; shift 2 ;;
    --analyze-llm-base)   ANALYZE_LLM_BASE="$2"; shift 2 ;;
    --analyze-llm-model)  ANALYZE_LLM_MODEL="$2"; shift 2 ;;
    *) echo "Unknown option: $1"; exit 1 ;;
  esac
done

if [ -z "$VIDEO" ] || [ -z "$OUTPUT" ]; then
  echo "Usage: run.sh --video <path> --output <dir> [options]"
  echo ""
  echo "Transcription (--transcribe): required, choose one:"
  echo "  local | cloud | agent-direct | audio-llm"
  echo ""
  echo "Visual (--vision-llm-*):"
  echo "  --vision-llm-key KEY           (no key = preprocess-only)"
  echo "  --vision-llm-base URL"
  echo "  --vision-llm-model MODEL       (must support image input)"
  echo "  --max-frames N                 per-segment max frames (default: 15)"
  echo "  --keep-frames"
  echo ""
  echo "Audio LLM (--audio-llm-*):"
  echo "  --audio-llm-key KEY"
  echo "  --audio-llm-base URL"
  echo "  --audio-llm-model MODEL"
  echo ""
  echo "Synthesis:"
  echo "  --synthesize-method api|agent|manual  (omit = observe only)"
  echo "  --analyze-llm-key KEY                 (required for api method)"
  echo "  --analyze-llm-base URL"
  echo "  --analyze-llm-model MODEL"
  echo ""
  echo "Dependency: Vision needs image-capable model; Audio needs audio-capable model or Whisper."
  echo "Confirm with user whether to use external API or Agent's own capabilities."
  exit 1
fi

if [ ! -f "$VIDEO" ]; then
  echo "ERROR: Video not found: $VIDEO"
  exit 1
fi

mkdir -p "$OUTPUT"

# Privacy warning for API modes
if [ -n "$VISION_LLM_KEY" ] || [ -n "$AUDIO_LLM_KEY" ] || [ "$TRANSCRIBE_MODE" = "cloud" ] || [ "$TRANSCRIBE_MODE" = "audio-llm" ] || [ "$SYNTHESIZE_METHOD" = "api" ]; then
  echo "⚠️  PRIVACY: API mode active — video frames and/or audio will be sent to external LLM endpoints."
  echo "   Ensure you trust the endpoint and understand the provider's data retention policy."
  echo "   Use agent-direct or local modes for confidential media."
  echo ""
fi

echo "=== Video Analyzer ==="
echo "Video: $VIDEO"
echo "Output: $OUTPUT"
echo "Max frames/segment: $MAX_FRAMES"
echo "Transcription: $TRANSCRIBE_MODE"
if [ -n "$VISION_LLM_KEY" ]; then
  echo "Vision: vision-llm"
else
  echo "Vision: preprocess-only"
fi
if [ -n "$SYNTHESIZE_METHOD" ]; then
  echo "Synthesis: $SYNTHESIZE_METHOD"
  if [ -n "$ANALYZE_LLM_KEY" ]; then
    echo "Analyze LLM: $ANALYZE_LLM_MODEL"
  fi
else
  echo "Synthesis: observe only (no --synthesize-method)"
fi
echo ""

# ═══════════════════════════════════════════════════════
# Stage 1: 并行启动 visual.py 和 transcribe.py
# ═══════════════════════════════════════════════════════

VISUAL_PID=""
TRANSCRIBE_PID=""
OBS_AUDIO="$OUTPUT/observations_audio.json"

# 启动 visual.py（抽帧 + 视觉观测）
echo "--- Starting visual.py (extract + observe) ---"
VISUAL_ARGS=("--video" "$VIDEO" "--output-dir" "$OUTPUT" "--max-frames" "$MAX_FRAMES")
if [ "$KEEP_FRAMES" = true ]; then
  VISUAL_ARGS+=("--keep-frames")
fi
if [ -n "$VISION_LLM_KEY" ] && [ -n "$VISION_LLM_BASE" ]; then
  VISUAL_ARGS+=("--vision-llm-key" "$VISION_LLM_KEY" "--vision-llm-base" "$VISION_LLM_BASE" "--vision-llm-model" "$VISION_LLM_MODEL")
fi
( python3 "$SCRIPT_DIR/visual.py" "${VISUAL_ARGS[@]}" ) &
VISUAL_PID=$!
echo "visual.py started (pid=$VISUAL_PID)"

# 启动 transcribe.py（音频观测 → observations_audio.json）
if [ -z "$TRANSCRIBE_MODE" ]; then
  echo "NOTE: No --transcribe specified, defaulting to agent-direct (extract audio only)"
  TRANSCRIBE_MODE="agent-direct"
fi
if [ "$TRANSCRIBE_MODE" = "skip" ]; then
  echo "--- Skipping audio transcription (--transcribe skip) ---"
else
  echo "--- Starting transcribe.py (mode=$TRANSCRIBE_MODE) ---"
  TRANSCRIBE_ARGS=("--video" "$VIDEO" "--output" "$OBS_AUDIO" "--mode" "$TRANSCRIBE_MODE" "--whisper-model" "$WHISPER_MODEL")
  if [ "$TRANSCRIBE_MODE" = "cloud" ]; then
    if [ -z "$WHISPER_API_KEY" ]; then
      echo "WARNING: --whisper-api-key required for cloud, falling back to agent-direct"
      TRANSCRIBE_MODE="agent-direct"
    else
      TRANSCRIBE_ARGS+=("--whisper-api-key" "$WHISPER_API_KEY" "--whisper-api-base" "$WHISPER_API_BASE")
    fi
  fi
  if [ "$TRANSCRIBE_MODE" = "audio-llm" ]; then
    if [ -z "$AUDIO_LLM_KEY" ] || [ -z "$AUDIO_LLM_BASE" ] || [ -z "$AUDIO_LLM_MODEL" ]; then
      echo "WARNING: --audio-llm-key/base/model required, falling back to agent-direct"
      TRANSCRIBE_MODE="agent-direct"
    else
      TRANSCRIBE_ARGS+=("--audio-llm-key" "$AUDIO_LLM_KEY" "--audio-llm-base" "$AUDIO_LLM_BASE" "--audio-llm-model" "$AUDIO_LLM_MODEL")
    fi
  fi
  ( python3 "$SCRIPT_DIR/transcribe.py" "${TRANSCRIBE_ARGS[@]}" ) &
  TRANSCRIBE_PID=$!
  echo "transcribe.py started (pid=$TRANSCRIBE_PID)"
fi

echo ""

# ═══════════════════════════════════════════════════════
# Stage 2: 等待两者完成
# ═══════════════════════════════════════════════════════

echo "--- Waiting for observations to complete ---"

if [ -n "$VISUAL_PID" ]; then
  echo "Waiting for visual.py (pid=$VISUAL_PID)..."
  wait $VISUAL_PID || echo "visual.py exited with non-zero status"
fi

if [ -n "$TRANSCRIBE_PID" ]; then
  echo "Waiting for transcribe.py (pid=$TRANSCRIBE_PID)..."
  wait $TRANSCRIBE_PID || echo "transcribe.py exited with non-zero status"
fi

echo "Both observations completed"
echo ""

OBS_VISUAL="$OUTPUT/observations_visual.json"

echo "Observations:"
echo "  visual -> $OBS_VISUAL"
echo "  audio  -> $OBS_AUDIO"
echo ""

# ═══════════════════════════════════════════════════════
# Stage 3: 合成（可选）
# ═══════════════════════════════════════════════════════

if [ -n "$SYNTHESIZE_METHOD" ]; then
  echo "--- Stage 3: Synthesis (method=$SYNTHESIZE_METHOD) ---"
  SYNTH_ARGS=("--observations-visual" "$OBS_VISUAL" "--observations-audio" "$OBS_AUDIO" "--output" "$OUTPUT/metadata.json" "--method" "$SYNTHESIZE_METHOD")
  if [ -n "$ANALYZE_LLM_KEY" ] && [ -n "$ANALYZE_LLM_BASE" ]; then
    SYNTH_ARGS+=("--api-key" "$ANALYZE_LLM_KEY" "--api-base" "$ANALYZE_LLM_BASE" "--model" "$ANALYZE_LLM_MODEL")
  else
    echo "WARNING: --synthesize-method api requires --analyze-llm-key/base/model. Skipping synthesis."
  fi
  python3 "$SCRIPT_DIR/analyze.py" "${SYNTH_ARGS[@]}"
  echo ""
else
  echo "--- Stage 3: Skipped (no --synthesize-method provided) ---"
  echo "To synthesize, run:"
  echo "  python3 $SCRIPT_DIR/analyze.py --observations-visual $OBS_VISUAL --observations-audio $OBS_AUDIO --output $OUTPUT/metadata.json --method <api|agent|manual>"
  echo ""
fi

echo "=== Done ==="
echo "Observations: $OBS_VISUAL + $OBS_AUDIO"
[ -f "$OUTPUT/metadata.json" ] && echo "Metadata: $OUTPUT/metadata.json"
