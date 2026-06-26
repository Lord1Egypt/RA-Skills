#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENV_DIR="${ROOT_DIR}/.venv"
WITH_DEV=0

for arg in "$@"; do
  case "$arg" in
    --with-dev)
      WITH_DEV=1
      ;;
    --venv=*)
      VENV_DIR="${arg#*=}"
      ;;
    *)
      echo "Unknown argument: $arg" >&2
      echo "Usage: bash scripts/setup_venv.sh [--with-dev] [--venv=/abs/path/.venv]" >&2
      exit 1
      ;;
  esac
done

if ! command -v python3.11 >/dev/null 2>&1; then
  echo "python3.11 not found in PATH" >&2
  exit 1
fi

python3.11 -m venv "$VENV_DIR"
"$VENV_DIR/bin/python" -m pip install --upgrade pip setuptools wheel

if [[ -f "$ROOT_DIR/requirements.txt" ]]; then
  "$VENV_DIR/bin/pip" install -r "$ROOT_DIR/requirements.txt"
fi

if [[ "$WITH_DEV" -eq 1 && -f "$ROOT_DIR/requirements-dev.txt" ]]; then
  "$VENV_DIR/bin/pip" install -r "$ROOT_DIR/requirements-dev.txt"
fi

echo "Virtual environment is ready: $VENV_DIR"
echo "Activate: source $VENV_DIR/bin/activate"
echo "Python:   $VENV_DIR/bin/python --version"
