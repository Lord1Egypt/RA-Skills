#!/bin/bash
# Bootstrap yumnb local environment
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
VENV_DIR="$ROOT_DIR/.venv"
PYTHON_BIN="${PYTHON_BIN:-python3}"

cd "$ROOT_DIR"

echo "[yumnb] root: $ROOT_DIR"

if [[ ! -d "$VENV_DIR" ]]; then
  echo "[yumnb] creating virtualenv at $VENV_DIR"
  "$PYTHON_BIN" -m venv "$VENV_DIR"
fi

source "$VENV_DIR/bin/activate"
python -m pip install -U pip
python -m pip install -r "$ROOT_DIR/requirements.txt"

echo
cat <<'EOF'
[yumnb] bootstrap complete.

Next steps:
  1) cp config.example.yaml config.yaml
  2) edit config.yaml
  3) run one of:
     python -m yumnb ingest "<URL>"
     python -m yumnb auto "<URL>"

If you want agent-driven mode, set:
  ai.provider: none
EOF
