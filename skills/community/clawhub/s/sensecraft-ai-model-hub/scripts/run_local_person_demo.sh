#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
VENV_DIR="${ROOT}/.venv"
MODEL_PATH="${ROOT}/models/60080-Person-Detection--Swift-YOLO.tflite"

if [ ! -d "$VENV_DIR" ]; then
  echo "error: missing virtualenv at $VENV_DIR" >&2
  echo "run: bash scripts/setup_local_demo_env.sh" >&2
  exit 1
fi

# shellcheck disable=SC1091
source "$VENV_DIR/bin/activate"

if [ ! -f "$MODEL_PATH" ]; then
  echo "Model not found: $MODEL_PATH" >&2
  echo "Downloading model 60080 into $ROOT/models ..." >&2
  python "$ROOT/scripts/sensecraft_models.py" download --model-id 60080 --output-dir "$ROOT/models" --manifest "$ROOT/models/downloaded.json" --summary
fi

exec python "$ROOT/scripts/sensecraft_webcam_person_demo.py" --model "$MODEL_PATH" "$@"
