#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE="$(cd "$SCRIPT_DIR/../../.." && pwd)"
VENV="$WORKSPACE/.venv-whisper-gpu"
PY="$VENV/bin/python"
SCRIPT="$SCRIPT_DIR/whisper_gpu_transcribe.py"

if [[ ! -x "$PY" ]]; then
  echo "GPU Whisper venv missing: $PY" >&2
  exit 2
fi

CUBLAS_LIB="$VENV/lib/python3.12/site-packages/nvidia/cublas/lib"
CUDNN_LIB="$VENV/lib/python3.12/site-packages/nvidia/cudnn/lib"
export LD_LIBRARY_PATH="$CUBLAS_LIB:$CUDNN_LIB:${LD_LIBRARY_PATH:-}"

exec "$PY" "$SCRIPT" "$@"
