#!/usr/bin/env bash
set -euo pipefail

DEVICE_TYPE="${1:-android}"
MODEL_MODE="${2:-bigmodel}"
REPO_DIR="${3:-$PWD/Open-AutoGLM}"

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"

printf '[1/6] host check\n'
python3 "$ROOT_DIR/scripts/check_host_env.py" git python3

printf '\n[2/6] repo sync\n'
bash "$ROOT_DIR/scripts/clone_or_update_open_autoglm.sh" "$REPO_DIR"

printf '\n[3/6] device readiness\n'
case "$DEVICE_TYPE" in
  android)
    python3 "$ROOT_DIR/scripts/check_host_env.py" adb
    bash "$ROOT_DIR/scripts/check_android_ready.sh"
    ;;
  harmonyos)
    python3 "$ROOT_DIR/scripts/check_host_env.py" hdc
    echo '[info] run hdc list targets and confirm the phone is authorized'
    ;;
  iphone)
    echo '[info] follow docs/ios_setup/ios_setup.md in the repo'
    ;;
  *)
    echo "[error] unknown device type: $DEVICE_TYPE"
    echo "Use android, harmonyos, or iphone"
    exit 1
    ;;
esac

printf '\n[4/6] python venv + dependencies\n'
cd "$REPO_DIR"
python3 -m venv .venv
# shellcheck disable=SC1091
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
pip install -e .

printf '\n[5/6] model config\n'
case "$MODEL_MODE" in
  bigmodel)
    echo 'Use: source .venv/bin/activate && python main.py --base-url https://open.bigmodel.cn/api/paas/v4 --model "autoglm-phone" --apikey "YOUR_API_KEY" "打开美团搜索附近的火锅店"'
    ;;
  third-party-openai-compatible)
    echo 'Use: source .venv/bin/activate && python main.py --base-url "<OPENAI_COMPATIBLE_BASE_URL>" --model "<MODEL_NAME>" --apikey "<API_KEY_IF_NEEDED>" "打开美团搜索附近的火锅店"'
    ;;
  self-hosted)
    echo 'Start your /v1 endpoint first, then run: source .venv/bin/activate && python main.py --base-url "<SELF_HOSTED_V1_BASE_URL>" --model "<MODEL_NAME>" --apikey "<API_KEY_IF_NEEDED>" "打开美团搜索附近的火锅店"'
    ;;
  *)
    echo "[error] unknown model mode: $MODEL_MODE"
    exit 1
    ;;
esac

printf '\n[6/6] next step\n'
python3 "$ROOT_DIR/scripts/print_next_steps.py" --device "$DEVICE_TYPE" --mode "$MODEL_MODE"
echo '[hint] after env vars are configured, you can run the full workflow with:'
echo "  bash \"$ROOT_DIR/scripts/ensure_and_run_task.sh\" \"$DEVICE_TYPE\" \"$MODEL_MODE\" \"$REPO_DIR\" \"<YOUR_NATURAL_LANGUAGE_TASK>\""

echo '[done] deployment path prepared'
