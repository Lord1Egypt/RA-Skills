#!/usr/bin/env bash
# generate.sh — Generate code from API contract (OpenAPI spec)
#
# This script reads api/openapi.yaml and generates:
#  - TypeScript types for backend (Worker/src/generated/)
#  - API client for frontend (pages/src/api/generated/)
#  - Optional HTML documentation (docs/API.html)
#
# Usage:
#   ./scripts/generate.sh
#
# Prerequisites:
#   npm install -g openapi-typescript
#   npm install -g openapi-typescript-codegen
#   npm install -g redoc-cli  # optional, for HTML docs

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

API_SPEC="$PROJECT_ROOT/api/openapi.yaml"
if [[ ! -f "$API_SPEC" ]]; then
  echo "✗ OpenAPI spec not found: $API_SPEC"
  echo "  Create api/openapi.yaml first."
  exit 1
fi

echo "=== SPM Contract Generation ==="
echo "Spec: $API_SPEC"
echo ""

# 1. Generate TypeScript types for backend (Worker)
echo "→ Generating backend types..."
mkdir -p "$PROJECT_ROOT/src/worker/generated"
npx openapi-typescript "$API_SPEC" --output "$PROJECT_ROOT/src/worker/generated/api-types.ts"
echo "  ✓ Worker types: src/worker/generated/api-types.ts"

# 2. Generate frontend API client (fetch-based)
echo "→ Generating frontend API client..."
mkdir -p "$PROJECT_ROOT/src/pages/src/api/generated"
npx openapi-typescript-codegen \
  --input "$API_SPEC" \
  --output "$PROJECT_ROOT/src/pages/src/api/generated" \
  --client fetch
echo "  ✓ Pages client: src/pages/src/api/generated/"

# 3. Optional: generate HTML documentation
if command -v redoc-cli &>/dev/null; then
  echo "→ Generating API documentation (HTML)..."
  redoc-cli bundle "$API_SPEC" --output "$PROJECT_ROOT/docs/API.html"
  echo "  ✓ API docs: docs/API.html"
else
  echo "  ℹ redoc-cli not installed — skipping HTML docs (npm install -g redoc-cli to enable)"
fi

echo ""
echo "✅ Generation complete."
echo ""
echo "Next steps:"
echo "  1. Import generated types in Worker: import type { OpenAPI, Api } from './generated/api-types'"
echo "  2. Use generated client in Pages: import { Api } from '@/api/generated'"
echo "  3. Run ./scripts/validate_contract.sh to ensure code stays in sync"
echo ""
echo "Remember: API changes must be made in api/openapi.yaml first, then re-run this script."
