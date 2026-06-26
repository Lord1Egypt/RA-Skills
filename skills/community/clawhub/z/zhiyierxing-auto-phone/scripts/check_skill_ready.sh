#!/usr/bin/env bash
set -euo pipefail

REPO_DIR="${1:-$PWD/Open-AutoGLM}"
DEVICE_TYPE="${2:-android}"

MISSING=0
MISSING_REPO=0
MISSING_VENV=0
MISSING_ENV=0
MISSING_DEVICE_TOOL=0

echo "[step] checking whether the skill can run your phone task now"

echo "[check] repo"
if [ -d "$REPO_DIR/.git" ]; then
  echo "[ok] code is already deployed: $REPO_DIR"
else
  echo "[missing] code is not deployed yet: $REPO_DIR"
  echo "[next] the repo needs to be cloned or updated first"
  MISSING=1
  MISSING_REPO=1
fi

echo "[check] python virtual environment"
if [ -d "$REPO_DIR/.venv" ]; then
  echo "[ok] repo-local .venv already exists: $REPO_DIR/.venv"
else
  echo "[missing] repo-local .venv is not ready yet: $REPO_DIR/.venv"
  echo "[next] create .venv and install dependencies into it before running the phone task"
  MISSING=1
  MISSING_VENV=1
fi

echo "[check] model environment variables"
for var in MODEL_BASE_URL MODEL_NAME MODEL_API_KEY; do
  if [ -n "${!var:-}" ]; then
    echo "[ok] $var is set"
  else
    echo "[missing] $var is not set"
    MISSING=1
    MISSING_ENV=1
  fi
done

if [ "$MISSING_ENV" -eq 1 ]; then
  echo "[next] configure the missing model env vars before execution"
  echo "[hint] required vars: MODEL_BASE_URL, MODEL_NAME, MODEL_API_KEY"
fi

echo "[check] device connection tool"
case "$DEVICE_TYPE" in
  android)
    if command -v adb >/dev/null 2>&1; then
      echo "[ok] adb is available for Android"
    else
      echo "[missing] adb is not installed or not on PATH"
      echo "[next] install Android platform-tools first"
      MISSING=1
      MISSING_DEVICE_TOOL=1
    fi
    ;;
  harmonyos)
    if command -v hdc >/dev/null 2>&1; then
      echo "[ok] hdc is available for HarmonyOS"
    else
      echo "[missing] hdc is not installed or not on PATH"
      echo "[next] install HarmonyOS SDK tools first"
      MISSING=1
      MISSING_DEVICE_TOOL=1
    fi
    ;;
  iphone)
    echo "[info] iPhone readiness must be confirmed through the repo's iOS setup guide"
    ;;
  *)
    echo "[error] unknown device type: $DEVICE_TYPE"
    exit 1
    ;;
esac

if [ "$MISSING" -eq 0 ]; then
  echo "[ready] everything needed for task execution looks present"
else
  echo "[not-ready] the phone task cannot run yet"
  if [ "$MISSING_REPO" -eq 1 ]; then
    echo "[summary] first blocker: code has not been deployed"
  fi
  if [ "$MISSING_VENV" -eq 1 ]; then
    echo "[summary] python environment is not prepared yet"
  fi
  if [ "$MISSING_ENV" -eq 1 ]; then
    echo "[summary] model configuration is incomplete"
  fi
  if [ "$MISSING_DEVICE_TOOL" -eq 1 ]; then
    echo "[summary] required device tooling is missing on this computer"
  fi
  exit 2
fi
