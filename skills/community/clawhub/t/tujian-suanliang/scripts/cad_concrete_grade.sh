#!/usr/bin/env bash
# 分标号台账入口：优先 $CAD_PYTHON，其次 PATH 上的 python3，最后本机 runtime 目录。
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_BIN=""
for candidate in "${CAD_PYTHON:-}" "$(command -v python3 || true)" \
  "$HOME"/.cache/codex-runtimes/*/dependencies/python/bin/python3; do
  if [[ -n "${candidate}" && -x "${candidate}" ]]; then
    PYTHON_BIN="${candidate}"
    break
  fi
done
if [[ -z "${PYTHON_BIN}" ]]; then
  echo "Python 3 not found; cannot run 分标号台账." >&2
  exit 1
fi
exec "${PYTHON_BIN}" "${SCRIPT_DIR}/cad_concrete_grade.py" "$@"
