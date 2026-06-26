#!/usr/bin/env bash
# Canonical skill entry: cwd = $SKILL/.upstream, python = $SKILL/.upstream/.venv/bin/python
# ($SKILL = parent of scripts/). No manual cd/activate needed.
#
# Usage:
#   ./scripts/run.sh [superpicky_cli.py arguments...]
#   ./scripts/run.sh --birdid [birdid_cli.py arguments...]
#   ./scripts/run.sh --region-query [args...] # ebird country/region code fuzzy lookup
#   ./scripts/run.sh --py SCRIPT [args...]   # absolute path, or relative to .upstream/ (exec uses abs path)
#   ./scripts/run.sh --help

set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
UP="${ROOT}/.upstream"
PY="${UP}/.venv/bin/python"

# Only this script's meta-help; pass -h through to superpicky_cli / birdid_cli.
if [[ "${1:-}" == "--help" ]] && [[ $# -eq 1 ]]; then
  cat <<EOF
SuperPicky skill entry (${ROOT}/scripts/run.sh -> .upstream + .venv).

  Three entries:
    [ARGS...]                    -> superpicky_cli.py (cull / reset / restar / …)
    --birdid [ARGS...]           -> birdid_cli.py (BirdID batch / organize / …)
    --region-query [ARGS...]     -> ebird_region_query.py (eBird code lookup)
  Helper: --py RELPATH [ARGS...] -> any script under repo root (venv, cwd=.upstream)

Examples:
  $(basename "$0") process ~/Photos/Birds
  $(basename "$0") -h
  $(basename "$0") --birdid identify ~/Photos/bird.jpg
  $(basename "$0") --region-query shanghai
  $(basename "$0") --py scripts/download_models.py

Repo: ${UP}
Interpreter: ${PY}

If missing, run: ${ROOT}/scripts/install.sh
EOF
  exit 0
fi

if [[ ! -x "$PY" ]]; then
  echo "error: venv not found at ${UP}/.venv" >&2
  echo "Run: ${ROOT}/scripts/install.sh" >&2
  exit 1
fi

if [[ ! -f "${UP}/superpicky_cli.py" ]]; then
  echo "error: SuperPicky clone missing at ${UP}" >&2
  echo "Run: ${ROOT}/scripts/install.sh" >&2
  exit 1
fi

if [[ "${1:-}" == "--region-query" ]]; then
  shift
  exec "$PY" "${ROOT}/scripts/ebird_region_query.py" "$@"
fi

cd "$UP"

if [[ "${1:-}" == "--py" ]]; then
  shift
  [[ $# -ge 1 ]] || { echo "error: --py needs a script path" >&2; exit 1; }
  script="$1"
  shift
  # Always invoke Python with an absolute script path (relative paths = under repo root $UP).
  if [[ "$script" != /* ]]; then
    script="${UP}/${script#./}"
  fi
  if [[ ! -f "$script" ]]; then
    echo "error: --py file not found: $script" >&2
    exit 1
  fi
  exec "$PY" "$script" "$@"
fi

if [[ "${1:-}" == "--birdid" ]]; then
  shift
  exec "$PY" "${UP}/birdid_cli.py" "$@"
fi

exec "$PY" "${UP}/superpicky_cli.py" "$@"
