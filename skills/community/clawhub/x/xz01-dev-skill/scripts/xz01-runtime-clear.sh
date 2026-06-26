#!/usr/bin/env bash
set -euo pipefail
RUNTIME="${1:-/www/wwwroot/www.900az.com/runtime}"
if [[ ! -d "$RUNTIME" ]]; then echo "FAIL runtime_dir_not_found $RUNTIME" >&2; exit 2; fi
find "$RUNTIME" -mindepth 1 -maxdepth 1 -exec rm -rf {} +
if find "$RUNTIME" -mindepth 1 -print -quit | grep -q .; then
  echo "FAIL runtime_not_empty_after_clear" >&2
  find "$RUNTIME" -mindepth 1 -maxdepth 2 -print >&2
  exit 1
fi
echo "PASS runtime_empty $RUNTIME"
