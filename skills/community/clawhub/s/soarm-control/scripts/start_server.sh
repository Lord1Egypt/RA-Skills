#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LEROBOT_ROOT="${LEROBOT_ROOT:-${HOME}/lerobot}"
CONDA_BIN="${CONDA_BIN:-}"

if [[ -z "${CONDA_BIN}" ]]; then
  for candidate in "${HOME}/miniconda3/bin/conda" "${HOME}/anaconda3/bin/conda"; do
    if [[ -x "${candidate}" ]]; then
      CONDA_BIN="${candidate}"
      break
    fi
  done
fi

export SOARM_API_HOST="${SOARM_API_HOST:-127.0.0.1}"
export SOARM_API_PORT="${SOARM_API_PORT:-8000}"
export SOARM_PORT="${SOARM_PORT:-/dev/ttyACM0}"
export SOARM_ID="${SOARM_ID:-openclaw_soarm}"
export SOARM_SKIP_CALIBRATION="${SOARM_SKIP_CALIBRATION:-1}"
if [[ -d "${LEROBOT_ROOT}" ]]; then
  export PYTHONPATH="${LEROBOT_ROOT}:${PYTHONPATH:-}"
fi

if [[ -z "${CONDA_BIN}" ]]; then
  echo "Error: conda executable not found in ~/miniconda3/bin/conda or ~/anaconda3/bin/conda" >&2
  exit 1
fi

API_SCRIPT="${SCRIPT_DIR}/soarm_api.py"
RUNNING_PIDS="$(pgrep -f "${API_SCRIPT}" || true)"
PORT_PID="$(ss -ltnp "( sport = :${SOARM_API_PORT} )" 2>/dev/null | sed -n 's/.*pid=\([0-9]\+\).*/\1/p' | head -n1)"

if [[ -n "${RUNNING_PIDS}" ]]; then
  echo "SOARM API is already running on port ${SOARM_API_PORT}."
  echo "PIDs: ${RUNNING_PIDS}"
  exit 0
fi

if [[ -n "${PORT_PID}" ]]; then
  echo "Error: port ${SOARM_API_PORT} is already in use by PID ${PORT_PID}, not by ${API_SCRIPT}." >&2
  echo "Stop that process or set a different SOARM_API_PORT before starting the server." >&2
  exit 1
fi

exec "${CONDA_BIN}" run -n lerobot python "${API_SCRIPT}"
