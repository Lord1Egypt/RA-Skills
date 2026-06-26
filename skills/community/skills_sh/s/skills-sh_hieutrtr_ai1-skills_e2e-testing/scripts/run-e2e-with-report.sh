#!/usr/bin/env bash
# run-e2e-with-report.sh — Run Playwright E2E tests and generate an HTML report.
#
# Usage:
#   ./run-e2e-with-report.sh [--output-dir <dir>] [--project <name>] [--headed]
#
# Options:
#   --output-dir <dir>    Directory to write reports (default: ./e2e-results)
#   --project <name>      Playwright project to run (default: all)
#   --headed              Run in headed mode for debugging

set -euo pipefail

# ─── Defaults ───────────────────────────────────────────────────────────────────
OUTPUT_DIR="./e2e-results"
PROJECT=""
HEADED=""

# ─── Parse arguments ────────────────────────────────────────────────────────────
while [[ $# -gt 0 ]]; do
    case "$1" in
        --output-dir)
            OUTPUT_DIR="$2"
            shift 2
            ;;
        --project)
            PROJECT="--project $2"
            shift 2
            ;;
        --headed)
            HEADED="--headed"
            shift
            ;;
        -h|--help)
            echo "Usage: $0 [--output-dir <dir>] [--project <name>] [--headed]"
            exit 0
            ;;
        *)
            echo "Unknown option: $1" >&2
            exit 1
            ;;
    esac
done

# ─── Setup ───────────────────────────────────────────────────────────────────────
mkdir -p "$OUTPUT_DIR"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
RESULTS_FILE="$OUTPUT_DIR/e2e-summary-${TIMESTAMP}.txt"
REPORT_DIR="$OUTPUT_DIR/html-report-${TIMESTAMP}"

echo "=== E2E Test Run ==="
echo "Output directory: ${OUTPUT_DIR}"
echo "Report directory: ${REPORT_DIR}"
echo ""

# ─── Verify Playwright is installed ──────────────────────────────────────────────
if ! npx playwright --version >/dev/null 2>&1; then
    echo "ERROR: Playwright is not installed. Run: npm install @playwright/test" >&2
    exit 1
fi

# ─── Run Playwright tests ───────────────────────────────────────────────────────
EXIT_CODE=0
npx playwright test \
    ${PROJECT} \
    ${HEADED} \
    --reporter=html \
    --output="$OUTPUT_DIR/test-results" \
    2>&1 | tee "$RESULTS_FILE" || EXIT_CODE=$?

# ─── Move HTML report to output directory ────────────────────────────────────────
if [[ -d "playwright-report" ]]; then
    mv playwright-report "$REPORT_DIR"
    echo "HTML report: ${REPORT_DIR}/index.html"
fi

# ─── Write summary ──────────────────────────────────────────────────────────────
echo "" >> "$RESULTS_FILE"
echo "Timestamp: $(date -Iseconds)" >> "$RESULTS_FILE"
echo "Report: ${REPORT_DIR}/index.html" >> "$RESULTS_FILE"

if [[ $EXIT_CODE -eq 0 ]]; then
    echo ""
    echo "PASS: All E2E tests passed."
    echo "Status: PASS" >> "$RESULTS_FILE"
else
    echo ""
    echo "FAIL: Some E2E tests failed. Review report at: ${REPORT_DIR}/index.html"
    echo "Status: FAIL" >> "$RESULTS_FILE"
fi

# ─── Open report (local only) ───────────────────────────────────────────────────
if [[ -z "${CI:-}" && $EXIT_CODE -ne 0 && -d "$REPORT_DIR" ]]; then
    echo "Opening report in browser..."
    npx playwright show-report "$REPORT_DIR" || true
fi

exit $EXIT_CODE
