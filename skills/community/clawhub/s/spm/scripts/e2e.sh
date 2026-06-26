#!/usr/bin/env bash
# e2e.sh — End-to-End pipeline verification for SPM-managed projects
#
# This is a TEMPLATE. Customize for your project's actual pipeline.
# Current skeleton: build → test → deploy → verify
#
# Usage:
#   ./scripts/e2e.sh [--skip-deploy] [--skip-frontend]
#
# Prerequisites (adjust for your stack):
#  - Your CLI tools (wrangler / docker / kubectl / etc.)
#  - Required service tokens in environment variables
#  - Services already deployed to staging
#
# Exit 0 if all passed, non-zero if any step fails.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# Default params (customize for your project)
SKIP_DEPLOY=0
SKIP_FRONTEND=0
STAGE="${E2E_STAGE:-staging}"

# Parse args
while [[ $# -gt 0 ]]; do
  case "$1" in
    --skip-deploy)
      SKIP_DEPLOY=1
      shift
      ;;
    --skip-frontend)
      SKIP_FRONTEND=1
      shift
      ;;
    *)
      echo "Unknown arg: $1" >&2
      exit 1
      ;;
  esac
done

echo "=== SPM End-to-End Verification ==="
echo "Stage: $STAGE"
echo ""

# ──────────────────────────────────────────────
# STEP: Customize the steps below for YOUR project
# Replace each block with your actual pipeline steps
# ──────────────────────────────────────────────

# 0. Environment checks
echo "→ Checking prerequisites..."
FAILED_PREREQS=0
for cmd in curl; do
  if ! command -v "$cmd" &>/dev/null; then
    echo "✗ $cmd not found in PATH"
    FAILED_PREREQS=1
  fi
done
if [[ $FAILED_PREREQS -eq 1 ]]; then
  echo "⚠ Install missing prerequisites and retry."
  exit 1
fi
echo "  ✓ Prerequisites OK"

# ─── Replace below with your actual pipeline steps ───

# 1. Health check
echo "→ Checking health endpoint..."
HEALTH_URL="${HEALTH_CHECK_URL:-https://your-service.staging.example.com/api/health}"
if curl -sf "$HEALTH_URL" > /dev/null; then
  echo "  ✓ Health endpoint OK"
else
  echo "  ⚠ Health endpoint not reachable (set HEALTH_CHECK_URL or customize this step)"
  echo "  Continuing..."
fi

# 2. API smoke test — customize for your endpoints
echo "→ Running API smoke test..."

# Example: verify a core endpoint returns 200
# Replace with your actual API endpoint
API_URL="${API_BASE_URL:-https://your-service.staging.example.com/api}"
SMOKE_TEST_OK=1

# Customize: test your critical endpoints
# curl -sf "$API_URL/projects" > /dev/null && echo "  ✓ GET /projects" || { echo "  ✗ GET /projects failed"; SMOKE_TEST_OK=0; }
echo "  ℹ Customize API smoke tests in scripts/e2e.sh (search for 'SMOKE_TEST')"

if [[ $SMOKE_TEST_OK -eq 0 ]]; then
  echo "✗ API smoke tests failed"
  exit 1
fi

# 3. Database verification — customize for your database
echo "→ Verifying database connectivity..."
# Example: wrangler d1 execute your-db --command "SELECT COUNT(*) FROM your_table;"
echo "  ℹ Customize database verification in scripts/e2e.sh (search for 'DATABASE_VERIFY')"

# 4. Deploy frontend (optional)
if [[ $SKIP_DEPLOY -eq 0 ]]; then
  echo "→ Deploying frontend to $STAGE..."
  # Example: wrangler pages deploy ./dist --project-name your-project --branch="$STAGE"
  echo "  ℹ Customize deployment in scripts/e2e.sh (search for 'DEPLOY_STEP')"
else
  echo "⏭ Skipping deploy (--skip-deploy)"
fi

# 5. Frontend smoke test
if [[ $SKIP_FRONTEND -eq 0 ]]; then
  echo "→ Running frontend smoke test..."
  FRONTEND_URL="${FRONTEND_URL:-https://your-project.pages.dev}"
  HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" "$FRONTEND_URL" 2>/dev/null || echo "000")
  if [[ "$HTTP_CODE" == "200" ]]; then
    echo "  ✓ Frontend returned HTTP 200"
  else
    echo "  ⚠ Frontend returned HTTP $HTTP_CODE (set FRONTEND_URL or customize this step)"
  fi
else
  echo "⏭ Skipping frontend smoke test (--skip-frontend)"
fi

# ──────────────────────────────────────────────

# Summary
echo ""
echo "✅ E2E Pipeline PASSED"
echo ""
echo "⚠ Remember: this is a template. Customize the steps above"
echo "   (grep for 'Customize' or 'SMOKE_TEST' / 'DATABASE_VERIFY' / 'DEPLOY_STEP')"
echo "   to match your actual project pipeline."
echo ""

exit 0
