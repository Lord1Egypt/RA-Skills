#!/usr/bin/env bash
set -euo pipefail

# Standalone installer for YouOS — no OpenClaw / clawhub required.
#
# Creates a local virtualenv, installs YouOS into it, and runs the doctor so
# you can see what's left to configure. Re-runnable (idempotent).
#
# Usage:
#   ./scripts/install.sh                 # base install
#   ./scripts/install.sh reranker        # base + the `reranker` extra
#   ./scripts/install.sh reranker,dev     # multiple extras (comma-separated)
#
# After it finishes, activate the venv and run the setup wizard:
#   source .venv/bin/activate
#   youos setup

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

VENV_DIR="${YOUOS_VENV:-$ROOT_DIR/.venv}"
EXTRAS="${1:-}"

# --- 1. Locate a Python >= 3.11 -------------------------------------------
PYTHON=""
for candidate in python3.13 python3.12 python3.11 python3; do
  if command -v "$candidate" >/dev/null 2>&1; then
    if "$candidate" -c 'import sys; sys.exit(0 if sys.version_info >= (3, 11) else 1)' 2>/dev/null; then
      PYTHON="$candidate"
      break
    fi
  fi
done

if [[ -z "$PYTHON" ]]; then
  echo "Error: YouOS needs Python >= 3.11, but none was found on PATH." >&2
  echo "Install it (e.g. \`brew install python@3.12\`) and re-run." >&2
  exit 1
fi

echo "==> Using $("$PYTHON" --version) ($(command -v "$PYTHON"))"

# --- 2. Create / reuse the virtualenv -------------------------------------
if [[ ! -d "$VENV_DIR" ]]; then
  echo "==> Creating virtualenv at $VENV_DIR"
  "$PYTHON" -m venv "$VENV_DIR"
else
  echo "==> Reusing existing virtualenv at $VENV_DIR"
fi

VENV_PY="$VENV_DIR/bin/python"

# --- 3. Install YouOS ------------------------------------------------------
TARGET="."
if [[ -n "$EXTRAS" ]]; then
  TARGET=".[${EXTRAS}]"
fi

echo "==> Upgrading pip"
"$VENV_PY" -m pip install --quiet --upgrade pip

echo "==> Installing YouOS ($TARGET)"
"$VENV_PY" -m pip install -e "$TARGET"

# --- 3b. Local model engine (MLX) on Apple Silicon -------------------------
# MLX powers on-device generation/fine-tuning but is Apple-Silicon-only, so
# it's a separate extra. Install it automatically on arm64 macOS (best-effort:
# a failure here shouldn't abort the whole install — YouOS still runs with a
# cloud/Ollama fallback).
if [[ "$(uname -s)" == "Darwin" && "$(uname -m)" == "arm64" ]]; then
  echo "==> Installing the local model engine (MLX, Apple Silicon)"
  if ! "$VENV_PY" -m pip install -e ".[mlx]"; then
    echo "  WARN: MLX install failed — local model unavailable until you run:"
    echo "        $VENV_PY -m pip install -e \".[mlx]\""
  fi
else
  echo "==> Skipping MLX (not Apple Silicon) — local model needs a cloud/Ollama fallback."
fi

# --- 4. Health check (informational; never fails the install) -------------
echo
echo "==> Running \`youos doctor\` (initial setup is expected to show TODOs)"
set +e
"$VENV_DIR/bin/youos" doctor
DOCTOR_RC=$?
set -e

echo
echo "YouOS installed into $VENV_DIR"
if [[ $DOCTOR_RC -ne 0 ]]; then
  echo "Doctor reported items to address — that's normal on a fresh install."
fi
cat <<EOF

Next steps:
  source "$VENV_DIR/bin/activate"
  youos setup        # guided first-run: accounts, ingestion, style analysis

Gmail/Docs ingestion needs a Google backend (set \`ingestion.google_backend\`
in youos_config.yaml). Today the working backend is \`gog\`; \`gws\` (Google's
Workspace CLI) and \`native\` (Google API) are being wired up.
EOF
