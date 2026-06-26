#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
DEVICE_TYPE="${1:-android}"
MODEL_MODE="${2:-bigmodel}"
REPO_DIR="${3:-$PWD/Open-AutoGLM}"
TASK="${4:-}"

if [ -z "$TASK" ]; then
  echo "[error] missing task string"
  echo "Usage: ensure_and_run_task.sh <device_type> <model_mode> <repo_dir> <task>"
  exit 1
fi

echo "[phase] readiness check"
if bash "$ROOT_DIR/scripts/check_skill_ready.sh" "$REPO_DIR" "$DEVICE_TYPE"; then
  echo "[ok] readiness check passed"
else
  STATUS=$?
  if [ "$STATUS" -ne 2 ]; then
    echo "[error] readiness check failed unexpectedly"
    exit "$STATUS"
  fi

  echo "[info] some prerequisites are still missing"
  echo "[info] the workflow will auto-fix local installable blockers when possible"
  echo "[info] if model env vars are missing, you still need to configure them before the real task can run"

  echo "[phase] install host tools if needed"
  bash "$ROOT_DIR/scripts/install_host_tools.sh" "$DEVICE_TYPE" || true

  echo "[phase] deployment / repair"
  bash "$ROOT_DIR/scripts/deploy_open_autoglm.sh" "$DEVICE_TYPE" "$MODEL_MODE" "$REPO_DIR"

  echo "[phase] readiness re-check"
  if ! bash "$ROOT_DIR/scripts/check_skill_ready.sh" "$REPO_DIR" "$DEVICE_TYPE"; then
    echo "[blocked] setup is still incomplete after deployment / repair"
    echo "[blocked] please read the missing items above, fix them, then run the workflow again"
    exit 2
  fi
fi

echo "[phase] model verification"
cd "$REPO_DIR"
# shellcheck disable=SC1091
source .venv/bin/activate
python "$ROOT_DIR/scripts/verify_open_autoglm.py" \
  --base-url "${MODEL_BASE_URL:-}" \
  --model "${MODEL_NAME:-}" \
  --apikey "${MODEL_API_KEY:-}" \
  --task "打开美团搜索附近的火锅店"

echo "[phase] real task execution"
bash "$ROOT_DIR/scripts/run_phone_task.sh" "$REPO_DIR" "$TASK"

echo "[done] task workflow finished"
