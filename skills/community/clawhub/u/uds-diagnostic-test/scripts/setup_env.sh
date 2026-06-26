#!/usr/bin/env bash
set -euo pipefail

ENV_FILE="${UDS_ENV_FILE:-$HOME/.uds_env}"
WORK_DIR="${UDS_WORK_DIR:-$HOME/.uds_workspace}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
VENV_DIR="${UDS_VENV_DIR:-$HOME/.venvs/uds_diag}"
PIP_INDEX_URL="${PIP_INDEX_URL:-}"

log() {
  printf '[setup_env] %s\n' "$*"
}

fatal() {
  log "[ERROR] $*"
  exit 1
}

validate_skill_layout() {
  [ -d "$SCRIPT_DIR" ] || fatal "scripts directory not found: $SCRIPT_DIR"
  [ -d "$SKILL_DIR" ] || fatal "skill root not found: $SKILL_DIR"
  [ -f "$SKILL_DIR/SKILL.md" ] || fatal "incomplete skill directory: missing $SKILL_DIR/SKILL.md"
  [ -d "$SKILL_DIR/scripts" ] || fatal "incomplete skill directory: missing $SKILL_DIR/scripts/"

  if [ ! -f "$SKILL_DIR/requirements.txt" ]; then
    log "[WARN] requirements.txt missing under $SKILL_DIR; fallback install will be used"
  fi
}

python_check_cmd() {
  cat <<'EOF'
import importlib.metadata as md
import sys

import can
import can.interfaces.socketcan
import openpyxl

assert sys.version_info >= (3, 8)
assert hasattr(can, 'Bus')
assert tuple(int(part) for part in md.version('python-can').split('.')[:2]) >= (4, 0)
assert 'site-packages/can-0.0.0' not in can.__file__
print(md.version('python-can'))
EOF
}

pick_host_python() {
  if command -v python3 >/dev/null 2>&1; then
    command -v python3
    return 0
  fi
  if command -v python >/dev/null 2>&1; then
    command -v python
    return 0
  fi
  return 1
}

collect_from_root() {
  local root="$1"
  [ -d "$root" ] || return 0

  if command -v timeout >/dev/null 2>&1; then
    timeout 5 find "$root" -maxdepth 3 -name python -path '*/bin/python' 2>/dev/null || true
  else
    find "$root" -maxdepth 3 -name python -path '*/bin/python' 2>/dev/null || true
  fi
}

validate_python() {
  local candidate="$1"
  local check_cmd
  check_cmd="$(python_check_cmd)"
  PYTHONNOUSERSITE=1 "$candidate" -c "$check_cmd" >/dev/null 2>&1
}

diagnose_python_failure() {
  local candidate="$1"

  log "Validation failed for interpreter: $candidate"
  PYTHONNOUSERSITE=1 "$candidate" - <<'PY' || true
import importlib.metadata as md

def print_dist(name):
    try:
        print(f"[setup_env] dist {name}: {md.version(name)}")
    except Exception:
        print(f"[setup_env] dist {name}: <missing>")

print_dist('python-can')
print_dist('openpyxl')
print_dist('can')

try:
    import can
    print(f"[setup_env] module can: {getattr(can, '__file__', '<unknown>')}")
    print(f"[setup_env] module can.__version__: {getattr(can, '__version__', '<missing>')}")
except Exception as exc:
    print(f"[setup_env] import can failed: {exc}")

try:
    import can.interfaces.socketcan  # noqa: F401
    print('[setup_env] socketcan backend: OK')
except Exception as exc:
    print(f"[setup_env] socketcan backend failed: {exc}")
PY

  log "Never run: pip install can"
  log "If pip only offers can-0.0.0 or python-can<=1.5.x, stop retrying: this is a package-source/mirror issue"
  log "Expected: python-can>=4.0 with can.interfaces.socketcan available"
  log "Try once: $candidate -m pip uninstall -y can python-can"
  log "Then:    $candidate -m pip install --no-cache-dir -U python-can openpyxl"
  log "If that still installs can-0.0.0 or python-can 1.5.x, report the package source problem to the user"
}

pick_existing_python() {
  local host_python="$1"
  local candidate
  local roots=(
    "$HOME/.venvs"
    "$HOME/venvs"
    "$HOME/.virtualenvs"
    "$HOME/.local/share/venvs"
    "$HOME/.pyenv/versions"
    "$SKILL_DIR/.venv"
    "$SKILL_DIR/venv"
  )

  while IFS= read -r candidate; do
    [ -n "$candidate" ] || continue
    [ -x "$candidate" ] || continue
    if validate_python "$candidate"; then
      printf '%s\n' "$candidate"
      return 0
    fi
  done < <(
    for root in "${roots[@]}"; do
      collect_from_root "$root"
    done

    if command -v conda >/dev/null 2>&1; then
      conda env list --json 2>/dev/null | "$host_python" -c "import json, sys; [print(p + '/bin/python') for p in json.load(sys.stdin).get('envs', [])]" 2>/dev/null || true
    fi

    if command -v python3 >/dev/null 2>&1; then
      command -v python3
    fi
    if command -v python >/dev/null 2>&1; then
      command -v python
    fi
  )

  return 1
}

ensure_venv_support() {
  local host_python="$1"
  if ! "$host_python" -m venv --help >/dev/null 2>&1; then
    log "[ERROR] Python venv support is missing on the target machine"
    log "Debian/Ubuntu: sudo apt install python3-venv"
    log "RHEL/Fedora:   sudo dnf install python3-virtualenv"
    log "Arch:          sudo pacman -S python-virtualenv"
    exit 1
  fi
}

install_failed_msg() {
  local venv_dir="$1"
  log "[ERROR] pip install failed — check network / pip source"
  log "[ERROR] Removing incomplete venv: $venv_dir"
  rm -rf "$venv_dir"
  exit 1
}

create_venv() {
  local host_python="$1"
  ensure_venv_support "$host_python"

  if [ -d "$VENV_DIR" ]; then
    log "Removing broken venv: $VENV_DIR"
    rm -rf "$VENV_DIR"
  fi

  mkdir -p "$(dirname "$VENV_DIR")"
  log "Creating Python environment: $VENV_DIR"
  "$host_python" -m venv "$VENV_DIR" || {
    log "[ERROR] venv creation failed; install python3-venv and retry"
    exit 1
  }
  "$VENV_DIR/bin/python" -m pip uninstall -y can python-can >/dev/null 2>&1 || true

  local pip_flags=""
  [ -n "$PIP_INDEX_URL" ] && pip_flags="-i $PIP_INDEX_URL"

  if [ -f "$SKILL_DIR/requirements.txt" ]; then
    "$VENV_DIR/bin/python" -m pip install $pip_flags -U pip setuptools wheel || install_failed_msg "$VENV_DIR"
    "$VENV_DIR/bin/python" -m pip install $pip_flags --no-cache-dir -r "$SKILL_DIR/requirements.txt" || install_failed_msg "$VENV_DIR"
  else
    "$VENV_DIR/bin/python" -m pip install $pip_flags -U pip setuptools wheel || install_failed_msg "$VENV_DIR"
    "$VENV_DIR/bin/python" -m pip install $pip_flags --no-cache-dir python-can openpyxl || install_failed_msg "$VENV_DIR"
  fi
  printf '%s\n' "$VENV_DIR/bin/python"
}

persist_env() {
  local python_path="$1"
  mkdir -p "$WORK_DIR"
  cat > "$ENV_FILE" <<EOF
UDS_PYTHON="$python_path"
UDS_SKILL_DIR="$SKILL_DIR"
UDS_WORK="$WORK_DIR"
EOF
  [ -n "$PIP_INDEX_URL" ] && echo "PIP_INDEX_URL=\"$PIP_INDEX_URL\"" >> "$ENV_FILE"
  log "Wrote $ENV_FILE"
  log "UDS_PYTHON=$python_path"
  log "UDS_SKILL_DIR=$SKILL_DIR"
  log "UDS_WORK=$WORK_DIR"
  [ -n "$PIP_INDEX_URL" ] && log "PIP_INDEX_URL=$PIP_INDEX_URL"
}

check_env_file_complete() {
  if [ -f "$ENV_FILE" ]; then
    local missing_vars=""
    for v in UDS_PYTHON UDS_SKILL_DIR UDS_WORK; do
      if ! grep -q "^${v}=" "$ENV_FILE" 2>/dev/null; then
        missing_vars="$missing_vars $v"
      fi
    done
    if [ -n "$missing_vars" ]; then
      log "[WARN] $ENV_FILE incomplete (missing:$missing_vars), will regenerate"
    fi
  fi
}

main() {
  local host_python
  local picked_python

  check_env_file_complete

  validate_skill_layout

  host_python="$(pick_host_python)" || {
    log "[ERROR] python3/python not found on the target machine"
    exit 1
  }

  picked_python=""
  if picked_python="$(pick_existing_python "$host_python")"; then
    log "Found reusable interpreter: $picked_python"
  else
    picked_python="$(create_venv "$host_python")"
    log "Created interpreter: $picked_python"
  fi

  validate_python "$picked_python" || {
    diagnose_python_failure "$picked_python"
    exit 1
  }

  persist_env "$picked_python"
  PYTHONNOUSERSITE=1 "$picked_python" -c "import can, importlib.metadata as md; print('Python deps OK, python-can', md.version('python-can'), 'module', can.__file__)"
  log "CAN hardware checks are intentionally separate; run can_init.sh only on the target machine that has the adapter attached"
}

main "$@"