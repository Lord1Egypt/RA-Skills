#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENV_DIR="${ROOT_DIR}/.venv"
CHECK_DEV=0

for arg in "$@"; do
  case "$arg" in
    --with-dev)
      CHECK_DEV=1
      ;;
    --venv=*)
      VENV_DIR="${arg#*=}"
      ;;
    *)
      echo "Unknown argument: $arg" >&2
      echo "Usage: bash scripts/check_python311.sh [--with-dev] [--venv=/abs/path/.venv]" >&2
      exit 1
      ;;
  esac
done

ok() {
  echo "[OK] $*"
}

warn() {
  echo "[WARN] $*"
}

fail() {
  echo "[FAIL] $*"
}

status=0

echo "Skill root: ${ROOT_DIR}"

if command -v python3.11 >/dev/null 2>&1; then
  py_cmd="$(command -v python3.11)"
  py_ver="$(python3.11 --version 2>&1 || true)"
  ok "python3.11 found: ${py_cmd} (${py_ver})"
else
  fail "python3.11 not found in PATH"
  status=1
fi

if [[ -f "${ROOT_DIR}/.python-version" ]]; then
  pv="$(tr -d '[:space:]' < "${ROOT_DIR}/.python-version")"
  if [[ "$pv" == "3.11" || "$pv" == 3.11.* ]]; then
    ok ".python-version is ${pv}"
  else
    warn ".python-version is ${pv}; expected 3.11"
  fi
else
  warn ".python-version missing"
fi

if [[ -f "${ROOT_DIR}/pyproject.toml" ]]; then
  if rg -n 'requires-python\s*=\s*"\>=3\.11,\<3\.12"' "${ROOT_DIR}/pyproject.toml" >/dev/null 2>&1; then
    ok "pyproject.toml requires-python constraint is set to >=3.11,<3.12"
  else
    warn "pyproject.toml missing strict requires-python >=3.11,<3.12"
  fi
else
  warn "pyproject.toml missing"
fi

if [[ -d "${VENV_DIR}" && -x "${VENV_DIR}/bin/python" ]]; then
  venv_ver="$(${VENV_DIR}/bin/python --version 2>&1 || true)"
  if [[ "$venv_ver" == Python\ 3.11* ]]; then
    ok "venv exists and uses ${venv_ver}"
  else
    fail "venv exists but version is ${venv_ver}; expected Python 3.11.x"
    status=1
  fi

  if [[ -f "${ROOT_DIR}/requirements.txt" ]]; then
    if [[ -s "${ROOT_DIR}/requirements.txt" ]]; then
      if "${VENV_DIR}/bin/pip" check >/dev/null 2>&1; then
        ok "runtime dependencies look consistent (pip check)"
      else
        warn "runtime dependency issues detected; run: ${VENV_DIR}/bin/pip install -r ${ROOT_DIR}/requirements.txt"
      fi
    else
      ok "requirements.txt is empty (no runtime deps)"
    fi
  fi

  if [[ "$CHECK_DEV" -eq 1 ]]; then
    if [[ -f "${ROOT_DIR}/requirements-dev.txt" ]]; then
      if rg -n '^PyYAML' "${ROOT_DIR}/requirements-dev.txt" >/dev/null 2>&1; then
        if "${VENV_DIR}/bin/pip" show PyYAML >/dev/null 2>&1; then
          ok "dev dependency PyYAML is installed"
        else
          warn "PyYAML not installed in venv; run: ${VENV_DIR}/bin/pip install -r ${ROOT_DIR}/requirements-dev.txt"
        fi
      fi
    fi
  fi
else
  warn "venv not found at ${VENV_DIR}"
  warn "create it with: bash scripts/setup_venv.sh$( [[ "$CHECK_DEV" -eq 1 ]] && echo ' --with-dev' || true )"
fi

echo
if [[ "$status" -eq 0 ]]; then
  ok "Environment check passed"
  exit 0
fi

fail "Environment check failed"

echo
if command -v pyenv >/dev/null 2>&1; then
  echo "Suggested fix (pyenv):"
  echo "  pyenv install -s 3.11.11"
  echo "  pyenv local 3.11.11"
  echo "  bash scripts/setup_venv.sh$( [[ "$CHECK_DEV" -eq 1 ]] && echo ' --with-dev' || true )"
  echo "  source .venv/bin/activate"
else
  echo "Suggested fix (homebrew):"
  echo "  brew install python@3.11"
  echo "  echo 'export PATH=\"/opt/homebrew/opt/python@3.11/bin:\$PATH\"' >> ~/.zshrc"
  echo "  source ~/.zshrc"
  echo "  bash scripts/setup_venv.sh$( [[ "$CHECK_DEV" -eq 1 ]] && echo ' --with-dev' || true )"
  echo "  source .venv/bin/activate"
fi

exit 1
