#!/usr/bin/env bash
set -euo pipefail

REPO_DIR="${1:-$PWD/Open-AutoGLM}"
TASK="${2:-}"
BASE_URL="${MODEL_BASE_URL:-}"
MODEL_NAME_VALUE="${MODEL_NAME:-}"
API_KEY="${MODEL_API_KEY:-}"

if [ -z "$TASK" ]; then
  echo "[error] missing task string"
  echo "Usage: run_phone_task.sh <repo_dir> <task>"
  exit 1
fi

if [ ! -d "$REPO_DIR/.venv" ]; then
  echo "[error] missing .venv: $REPO_DIR/.venv"
  echo "Create and install the repo-local virtual environment first."
  exit 1
fi

if [ -z "$BASE_URL" ] || [ -z "$MODEL_NAME_VALUE" ] || [ -z "$API_KEY" ]; then
  echo "[error] missing required model environment variables"
  echo "Required: MODEL_BASE_URL, MODEL_NAME, MODEL_API_KEY"
  exit 1
fi

cd "$REPO_DIR"
# shellcheck disable=SC1091
source .venv/bin/activate

if [ ! -f main.py ]; then
  echo "[error] main.py not found in repo dir: $REPO_DIR"
  exit 1
fi

echo "[run] executing phone task from .venv"
python main.py --base-url "$BASE_URL" --model "$MODEL_NAME_VALUE" --apikey "$API_KEY" "$TASK"
