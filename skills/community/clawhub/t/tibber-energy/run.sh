#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"

if [[ -f "${ROOT}/.env" ]]; then
  set -a
  # shellcheck disable=SC1091
  source "${ROOT}/.env"
  set +a
fi

if [[ "${1:-}" == "-h" || "${1:-}" == "--help" ]]; then
  exec python3 "${ROOT}/tibber_energy.py" "$@"
fi

exec python3 "${ROOT}/tibber_energy.py" "$@"
