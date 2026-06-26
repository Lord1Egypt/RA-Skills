#!/usr/bin/env bash
set -euo pipefail
python -c "import velog_cli, sys; print(velog_cli.__version__)"
python -m velog_cli.cli -h >/dev/null 2>&1 || true
