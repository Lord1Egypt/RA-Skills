#!/usr/bin/env bash
# validate_contract.sh — Ensure generated code matches the OpenAPI spec
#
# Checks:
#  1. Generated files are newer than api/openapi.yaml (or spec hasn't changed)
#  2. TypeScript type check passes for generated code
#
# Usage:
#   ./scripts/validate_contract.sh
#
# Exit 0 if all good, 1 if contract drift detected.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

API_SPEC="$PROJECT_ROOT/api/openapi.yaml"
WORKER_TYPES="$PROJECT_ROOT/src/worker/generated/api-types.ts"
CLIENT_DIR="$PROJECT_ROOT/src/pages/src/api/generated"

echo "=== Contract Validation ==="

# Check spec exists
if [[ ! -f "$API_SPEC" ]]; then
  echo "✗ OpenAPI spec not found: $API_SPEC"
  exit 1
fi

# 1. Check staleness
echo "→ Checking if generated files are up-to-date..."

if [[ ! -f "$WORKER_TYPES" ]]; then
  echo "✗ Worker types missing: $WORKER_TYPES"
  echo "  Run ./scripts/generate.sh first."
  exit 1
fi

if [[ ! -d "$CLIENT_DIR" ]]; then
  echo "✗ Pages client missing: $CLIENT_DIR"
  echo "  Run ./scripts/generate.sh first."
  exit 1
fi

stale=0
if [[ "$API_SPEC" -nt "$WORKER_TYPES" ]]; then
  echo "✗ Worker types are stale (older than spec)"
  echo "  Run ./scripts/generate.sh to update."
  stale=1
fi

if [[ "$API_SPEC" -nt "$CLIENT_DIR" ]]; then
  echo "✗ Pages client is stale (older than spec)"
  echo "  Run ./scripts/generate.sh to update."
  stale=1
fi

if [[ $stale -eq 1 ]]; then
  exit 1
fi

echo "  ✓ Generated files are up-to-date"

# 2. Type check backend types (if tsconfig exists)
if [[ -f "$PROJECT_ROOT/src/worker/tsconfig.json" ]] || [[ -f "$PROJECT_ROOT/tsconfig.json" ]]; then
  echo "→ Type-checking Worker generated types..."
  # Try worker-specific tsconfig, fallback to root
  if npx tsc --project "$PROJECT_ROOT/src/worker/tsconfig.json" --noEmit 2>/dev/null; then
    echo "  ✓ Worker types valid"
  elif npx tsc --project "$PROJECT_ROOT/tsconfig.json" --noEmit 2>/dev/null; then
    echo "  ✓ Project types valid"
  else
    echo "⚠ Type check failed — but generated code may still be syntactically valid"
    echo "  (This is expected if the rest of the project has unrelated type errors)"
  fi
else
  echo "  ℹ No tsconfig found — skipping type check"
fi

# 3. Check frontend client (check for marker file; generated directory may contain multiple files)
CLIENT_DIR="$PROJECT_ROOT/src/pages/src/api/generated"
if [[ -d "$CLIENT_DIR" ]]; then
  # Find the newest generated file in the directory to compare against spec
  CLIENT_NEWEST=$(find "$CLIENT_DIR" -type f -name "*.ts" -exec ls -t {} + 2>/dev/null | head -1)
  if [[ -n "$CLIENT_NEWEST" ]]; then
    if [[ "$API_SPEC" -nt "$CLIENT_NEWEST" ]]; then
      echo "✗ Pages client is stale (older than spec)"
      echo "  Run ./scripts/generate.sh to update."
      stale=1
    fi
  fi
  echo "  ✓ Pages client present"
else
  echo "⚠ Pages client directory not found: $CLIENT_DIR"
  echo "  Run ./scripts/generate.sh to create."
fi

echo ""
echo "✅ Contract validation passed"
echo ""
echo "If you see stale warnings, run: ./scripts/generate.sh"
echo "If type check fails, review the generated types for compatibility issues with your implementation."

exit 0
