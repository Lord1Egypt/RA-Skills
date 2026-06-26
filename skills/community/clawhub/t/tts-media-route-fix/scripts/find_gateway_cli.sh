#!/usr/bin/env bash
set -euo pipefail

ROOTS=(
  "/usr/lib/node_modules/openclaw"
  "/opt/openclaw"
)

found=0
for root in "${ROOTS[@]}"; do
  [[ -d "$root" ]] || continue
  while IFS= read -r -d '' f; do
    found=1
    printf '%s\n' "$f"
  done < <(find "$root" -type f -name 'gateway-cli-*.js' -print0 2>/dev/null)
done

if [[ "$found" -eq 0 ]]; then
  echo "No gateway-cli-*.js files found in default roots." >&2
  exit 1
fi
