#!/usr/bin/env bash
set -euo pipefail
RUN_DIR="${1:-/root/.hermes/workspace/xz01-factory/runs/run-0002}"
BASELINE="$RUN_DIR/guards/php-backend-baseline-before-theme-repair.sha256"
if [[ ! -f "$BASELINE" ]]; then
  echo "FAIL baseline_not_found $BASELINE" >&2
  exit 2
fi
sha256sum -c "$BASELINE"
echo "PASS backend_baseline_ok count=$(grep -c ': OK$' < <(sha256sum -c "$BASELINE" 2>/dev/null || true))"
