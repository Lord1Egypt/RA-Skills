#!/usr/bin/env bash
set -euo pipefail

BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

python3 -c "import py_compile; py_compile.compile('$BASE_DIR/cdp-eval.py', doraise=True)"
python3 "$BASE_DIR/cdp-eval.py" --help | grep -q "cdp-eval"
