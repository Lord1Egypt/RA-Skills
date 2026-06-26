#!/usr/bin/env bash
# One-shot install under the skill: clone -> $SKILL/.upstream, venv -> $SKILL/.upstream/.venv
# ($SKILL = parent of scripts/).
# - Picks Python 3.10–3.12 when available (warns on 3.13+)
# - Creates .venv if the interpreter supports venv
# - Chooses deps: NVIDIA CUDA (requirements_cuda.txt) vs CPU upstream vs macOS-friendly fallback
#
# Usage:
#   ./scripts/install.sh              # clone if needed, venv, pip deps (no model download)
#   ./scripts/install.sh --with-models
#   REPO_URL=... BRANCH=main ./scripts/install.sh
#   PY=/path/to/python3.12 ./scripts/install.sh

set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
UP="${ROOT}/.upstream"
REPO_URL="${REPO_URL:-https://github.com/jamesphotography/SuperPicky.git}"
BRANCH="${BRANCH:-master}"
WITH_MODELS=0
SKIP_CLONE=0
SKIP_VERIFY="${SKIP_VERIFY:-0}"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --with-models) WITH_MODELS=1; shift ;;
    --no-clone)    SKIP_CLONE=1; shift ;;
    --skip-verify) SKIP_VERIFY=1; shift ;;
    --branch)      BRANCH="$2"; shift 2 ;;
    --repo-url)    REPO_URL="$2"; shift 2 ;;
    -h|--help)
      cat <<'EOF'
Usage: install.sh [options]

  Clones SuperPicky to .upstream/ (unless present), creates .venv when venv works,
  installs deps: CUDA (nvidia-smi) | macOS (base+PyPI torch) | CPU (requirements.txt or fallback).

Options:
  --with-models   Run scripts/download_models.py after pip (large download)
  --no-clone      Do not git clone; .upstream must already exist
  --skip-verify   Skip post-install environment checks (not recommended)
  --branch NAME   Git branch (default: master)
  --repo-url URL  Git remote (default: jamesphotography/SuperPicky)

Environment:
  PY=python3.12   Force a specific interpreter (must support python -m venv)
  REPO_URL / BRANCH  Same as flags above
  SKIP_VERIFY=1   Same as --skip-verify
EOF
      exit 0
      ;;
    *) echo "unknown arg: $1" >&2; exit 1 ;;
  esac
done

log() { printf '%s\n' "$*"; }
err() { printf '%s\n' "$*" >&2; }

python_version_tuple() {
  "$1" -c 'import sys; print(sys.version_info[0], sys.version_info[1])' 2>/dev/null || echo "0 0"
}

venv_works() {
  local py="$1" tmp
  tmp="$(mktemp -d "${TMPDIR:-/tmp}/sp-venv-test.XXXXXX")"
  if "$py" -m venv "$tmp/v" >/dev/null 2>&1; then
    rm -rf "$tmp"
    return 0
  fi
  rm -rf "$tmp"
  return 1
}

pick_python() {
  if [[ -n "${PY:-}" ]]; then
    if command -v "$PY" &>/dev/null && venv_works "$PY"; then
      echo "$PY"
      return 0
    fi
    err "error: PY=$PY is missing or cannot create venv"
    return 1
  fi

  local candidates=(python3.12 python3.11 python3.10 python3)
  local c maj min
  for c in "${candidates[@]}"; do
    command -v "$c" &>/dev/null || continue
    read -r maj min <<<"$(python_version_tuple "$c")"
    [[ "$maj" -eq 3 ]] || continue
    if [[ "$min" -ge 13 ]]; then
      err "note: skipping $c (3.13+ often breaks upstream torch pins; install python3.12)"
      continue
    fi
    if [[ "$min" -lt 10 ]]; then
      continue
    fi
    if venv_works "$c"; then
      echo "$c"
      return 0
    fi
    err "note: $c has no working venv module"
  done

  # Last resort: 3.13+ if nothing else
  for c in python3.13 python3; do
    command -v "$c" &>/dev/null || continue
    read -r maj min <<<"$(python_version_tuple "$c")"
    [[ "$maj" -eq 3 ]] || continue
    if venv_works "$c"; then
      err "warning: using $c — if pip fails, install Python 3.12 and re-run"
      echo "$c"
      return 0
    fi
  done

  err "error: no Python with working 'python -m venv' found. Install Python 3.10–3.12."
  return 1
}

detect_os() {
  uname -s 2>/dev/null || echo Unknown
}

cuda_available() {
  local os
  os="$(detect_os)"
  [[ "$os" == Darwin ]] && return 1
  command -v nvidia-smi &>/dev/null || return 1
  nvidia-smi &>/dev/null || return 1
  return 0
}

pip_install_profile() {
  local profile="$1"
  cd "$UP"
  # shellcheck disable=SC1091
  source .venv/bin/activate
  pip install -U pip setuptools wheel

  case "$profile" in
    cuda)
      log "Installing CUDA stack (cu118 wheels from PyTorch index) + extras..."
      pip install -r requirements_cuda.txt
      pip install pyinstaller lap
      ;;
    cpu_upstream)
      log "Installing CPU stack from upstream requirements.txt..."
      if pip install -r requirements.txt; then
        return 0
      fi
      err "upstream requirements.txt failed (common on macOS arm64). Falling back to base + PyPI torch..."
      pip install -r requirements_base.txt
      pip install pyinstaller lap
      pip install torch torchvision torchaudio
      ;;
    macos_fallback)
      log "Installing macOS-friendly stack (requirements_base + PyPI torch)..."
      pip install -r requirements_base.txt
      pip install pyinstaller lap
      pip install torch torchvision torchaudio
      ;;
  esac
}

# Post-install checks; prints [superpicky-cli verify] lines for agents/CI.
# Exits 1 if any hard check fails.
verify_environment() {
  local profile="$1"
  local py="${UP}/.venv/bin/python"
  local failed=0

  verify_fail() {
    err "[superpicky-cli verify] ERROR: $*"
    failed=1
  }

  verify_warn() {
    err "[superpicky-cli verify] WARNING: $*"
  }

  log ""
  log "Verifying install (skill: ${ROOT})..."

  if [[ ! -x "$py" ]]; then
    verify_fail "venv python missing or not executable: ${py}"
    err "[superpicky-cli verify] HINT: remove ${UP}/.venv and re-run install.sh"
    return 1
  fi

  if ! out="$("$py" -c "import torch; import torchvision; import torchaudio; print(torch.__version__)" 2>&1)"; then
    verify_fail "PyTorch stack import failed: $out"
  else
    log "[superpicky-cli verify] OK: torch ${out}"
  fi

  case "$profile" in
    cuda)
      if ! cuda_out="$("$py" -c "import torch; print('cuda_available=', torch.cuda.is_available()); print('device_count=', torch.cuda.device_count())" 2>&1)"; then
        verify_fail "torch CUDA probe crashed: $cuda_out"
      elif echo "$cuda_out" | grep -q "cuda_available= True"; then
        log "[superpicky-cli verify] OK: PyTorch sees CUDA ($cuda_out)"
      else
        verify_fail "CUDA install profile was used but torch.cuda.is_available() is False. Output: $cuda_out"
        err "[superpicky-cli verify] HINT: check NVIDIA driver, CUDA runtime, and that this venv used requirements_cuda.txt"
      fi
      ;;
    macos_fallback)
      mps_out="$("$py" -c "
import torch
m = getattr(torch.backends, 'mps', None)
print('MPS', m.is_available() if m is not None else False)
" 2>&1)" || verify_warn "MPS probe raised: $mps_out"
      if [[ "$mps_out" == "MPS True" ]]; then
        log "[superpicky-cli verify] OK: Apple MPS available for torch"
      elif [[ "$mps_out" == "MPS False" ]]; then
        verify_warn "Apple MPS not available; torch will use CPU on this Mac."
      else
        verify_warn "Unexpected MPS probe output: $mps_out"
      fi
      ;;
  esac

  py_import_check() {
    local stmt="$1"
    local err
    if ! err="$("$py" -c "$stmt" 2>&1)"; then
      verify_fail "Python import check failed: $stmt -> $err"
    fi
  }
  py_import_check "import numpy"
  py_import_check "import cv2"
  py_import_check "from PIL import Image"
  py_import_check "import flask"
  py_import_check "import ultralytics"
  if [[ "$failed" -eq 0 ]]; then
    log "[superpicky-cli verify] OK: core third-party imports (numpy, opencv, Pillow, flask, ultralytics)"
  fi

  cd "$UP"
  if ! cli_out="$("$py" "${UP}/superpicky_cli.py" -h 2>&1)"; then
    verify_fail "superpicky_cli.py -h failed (exit non-zero). Output (first 800 chars): ${cli_out:0:800}"
  elif ! echo "$cli_out" | grep -qE "superpicky_cli|process|reset|restar"; then
    verify_fail "superpicky_cli.py -h produced unexpected output (missing expected usage). Output (first 800 chars): ${cli_out:0:800}"
  else
    log "[superpicky-cli verify] OK: superpicky_cli.py -h"
  fi

  if ! bid_out="$("$py" "${UP}/birdid_cli.py" -h 2>&1)"; then
    verify_fail "birdid_cli.py -h failed. Output (first 800 chars): ${bid_out:0:800}"
  else
    log "[superpicky-cli verify] OK: birdid_cli.py -h"
  fi

  if ! "${ROOT}/scripts/run.sh" --help >/dev/null 2>&1; then
    verify_fail "run.sh --help failed (entry wrapper broken?)"
  else
    log "[superpicky-cli verify] OK: ${ROOT}/scripts/run.sh --help"
  fi

  if [[ "$failed" -ne 0 ]]; then
    err ""
    err "[superpicky-cli verify] SUMMARY: environment validation FAILED. Fix errors above, then re-run: ${ROOT}/scripts/install.sh"
    err ""
    return 1
  fi

  log "[superpicky-cli verify] SUMMARY: all checks passed."
  return 0
}

ensure_repo() {
  if [[ "$SKIP_CLONE" -eq 1 ]]; then
    [[ -d "$UP" ]] || { err "error: .upstream missing and --no-clone set"; exit 1; }
    [[ -f "$UP/requirements_base.txt" ]] || { err "error: $UP does not look like SuperPicky"; exit 1; }
    return 0
  fi
  if [[ ! -d "$UP/.git" ]]; then
    log "Cloning SuperPicky -> $UP (branch $BRANCH)"
    git clone --depth 1 --single-branch --branch "$BRANCH" "$REPO_URL" "$UP"
  else
    log "Using existing clone: $UP"
  fi
}

# --- main ---
PY_BIN="$(pick_python)" || exit 1
log "Using Python: $PY_BIN ($($PY_BIN -V 2>&1))"

ensure_repo

if [[ -d "$UP/.venv" ]]; then
  log "Reusing existing $UP/.venv (remove it for a clean install)"
else
  log "Creating venv: $UP/.venv"
  "$PY_BIN" -m venv "$UP/.venv"
fi

OS="$(detect_os)"
PROFILE="cpu_upstream"
if [[ "$OS" == Darwin ]]; then
  PROFILE="macos_fallback"
elif cuda_available; then
  PROFILE="cuda"
  log "NVIDIA GPU driver detected (nvidia-smi OK) — using CUDA requirements."
else
  PROFILE="cpu_upstream"
  log "No usable NVIDIA CUDA path detected — using CPU requirements."
fi

pip_install_profile "$PROFILE"

if [[ "$WITH_MODELS" -eq 1 ]]; then
  log "Downloading models (this may take a long time and a lot of disk)..."
  "${ROOT}/scripts/run.sh" --py "${UP}/scripts/download_models.py"
else
  log "Skipped model download. Run: ${ROOT}/scripts/run.sh --py ${UP}/scripts/download_models.py"
fi

if [[ "$SKIP_VERIFY" -eq 1 ]]; then
  log "[superpicky-cli verify] SKIPPED (--skip-verify or SKIP_VERIFY=1)"
else
  verify_environment "$PROFILE" || exit 1
fi

log ""
log "Done. CLI entry (no cd / no manual activate):"
log "  ${ROOT}/scripts/run.sh --help          # wrapper usage"
log "  ${ROOT}/scripts/run.sh -h              # superpicky_cli.py help"
log "  ${ROOT}/scripts/run.sh process /path/to/photos"
