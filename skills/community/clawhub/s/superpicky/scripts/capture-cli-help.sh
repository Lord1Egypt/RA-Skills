#!/usr/bin/env bash
# Write reference/cli-help-captured.txt using scripts/run.sh (cwd + venv from $SKILL/.upstream).
# Prereq: $SKILL/.upstream/.venv (run scripts/install.sh from $SKILL).

set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
UP="${ROOT}/.upstream"
OUT="${ROOT}/reference/cli-help-captured.txt"
PY="${UP}/.venv/bin/python"
RUN="${ROOT}/scripts/run.sh"

if [[ ! -x "$PY" ]]; then
  echo "error: missing venv at ${UP}/.venv (run ${ROOT}/scripts/install.sh)" >&2
  exit 1
fi

{
  echo "=== Captured $(date -u +%Y-%m-%dT%H:%M:%SZ) ==="
  echo "Python: $("$PY" -V)"
  echo "Invoked via: ${RUN} (cwd fixed to repo root)"
  echo ""
  for cmd in "" process reset restar info burst identify; do
    echo "########## superpicky_cli.py ${cmd:-<no subcommand>} -h ##########"
    if [[ -z "$cmd" ]]; then
      "$RUN" -h 2>&1 || true
    else
      "$RUN" "$cmd" -h 2>&1 || true
    fi
    echo ""
  done
  echo "########## birdid_cli.py -h ##########"
  "$RUN" --birdid -h 2>&1 || true
  echo ""
  for sub in identify organize reset list-countries; do
    echo "########## birdid_cli.py $sub -h ##########"
    "$RUN" --birdid "$sub" -h 2>&1 || true
    echo ""
  done
} > "$OUT"

echo "wrote $OUT ($(wc -l < "$OUT") lines)"
