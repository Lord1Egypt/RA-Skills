#!/usr/bin/env bash
set -euo pipefail
RUN_DIR="${1:-/root/.hermes/workspace/xz01-factory/runs/run-0002}"
LIVE="${2:-/www/wwwroot/www.900az.com/public/themes/default}"
GEN="$RUN_DIR/generated/public/themes/default"
if [[ ! -d "$LIVE" ]]; then echo "FAIL live_theme_not_found $LIVE" >&2; exit 2; fi
if [[ ! -d "$GEN" ]]; then echo "FAIL generated_theme_not_found $GEN" >&2; exit 2; fi
DIFF_OUT="$(mktemp)"
if diff -qr "$LIVE" "$GEN" >"$DIFF_OUT"; then
  echo "PASS theme_diff_ok live=$LIVE generated=$GEN"
  rm -f "$DIFF_OUT"
else
  echo "FAIL theme_diff_mismatch" >&2
  cat "$DIFF_OUT" >&2
  rm -f "$DIFF_OUT"
  exit 1
fi
