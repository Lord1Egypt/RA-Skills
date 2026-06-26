#!/usr/bin/env bash
# ============================================================================
# Offline full test runner for quant-paper2spec
#
# Usage:
#   nohup bash scripts/run_full_tests.sh &
#   # or
#   bash scripts/run_full_tests.sh   (foreground)
#
# Results:  test_results/  directory (timestamped)
# ============================================================================

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
TIMESTAMP="$(date +%Y%m%d_%H%M%S)"
RESULTS_DIR="$PROJECT_ROOT/test_results/$TIMESTAMP"

mkdir -p "$RESULTS_DIR"

# -- Log everything --
LOG_FILE="$RESULTS_DIR/full_test.log"
exec > >(tee -a "$LOG_FILE") 2>&1

echo "========================================"
echo " quant-paper2spec — Full Test Suite"
echo " Started: $(date)"
echo " Results: $RESULTS_DIR"
echo "========================================"

cd "$PROJECT_ROOT"

# -- Load API keys --
AEGRA_ENV="/home/whlu/ALAGENT/deepagents-quickstarts/aegra/.env"
if [[ -f "$AEGRA_ENV" ]]; then
    echo "[env] Loading API keys from aegra/.env"
    set -a
    # Only export DEEPSEEK_API_KEY and OPENROUTER_API_KEY
    while IFS='=' read -r key value; do
        case "$key" in
            DEEPSEEK_API_KEY|OPENROUTER_API_KEY)
                export "$key=$value"
                echo "[env] Loaded $key"
                ;;
        esac
    done < <(grep -E '^(DEEPSEEK|OPENROUTER)' "$AEGRA_ENV" | sed 's/#.*//' | grep '=')
    set +a
else
    echo "[env] WARNING: aegra/.env not found, relying on existing env vars"
fi

# -- Activate venv --
if [[ -d ".venv" ]]; then
    source .venv/bin/activate
    echo "[env] Using venv: $(which python)"
else
    echo "[env] WARNING: .venv not found, using system python"
fi

echo ""
echo "========================================"
echo " Phase 1: Unit Tests"
echo "========================================"
echo ""

python -m pytest tests/test_parser.py tests/test_extractor.py tests/test_models.py tests/test_render.py \
    -v --tb=short --no-header \
    --junitxml="$RESULTS_DIR/unit_tests.xml" \
    2>&1 | tee "$RESULTS_DIR/unit_tests.txt"
UNIT_EXIT=${PIPESTATUS[0]}
echo ""
echo "[Phase 1] Unit tests exit code: $UNIT_EXIT"

echo ""
echo "========================================"
echo " Phase 2: Real E2E — Search & PDF"
echo "========================================"
echo ""

python -m pytest tests/test_real_e2e.py \
    -v --tb=long --no-header \
    -k "TestRealSearch or TestRealPDFExtraction" \
    --junitxml="$RESULTS_DIR/real_e2e_search_pdf.xml" \
    2>&1 | tee "$RESULTS_DIR/real_e2e_search_pdf.txt"
SEARCH_EXIT=${PIPESTATUS[0]}
echo ""
echo "[Phase 2] Search & PDF exit code: $SEARCH_EXIT"

echo ""
echo "========================================"
echo " Phase 3: Real E2E — Parser (LLM)"
echo "========================================"
echo ""

python -m pytest tests/test_real_e2e.py \
    -v --tb=long --no-header \
    -k "TestRealParserSingleStrategy or TestRealParserMultiStrategy" \
    --junitxml="$RESULTS_DIR/real_e2e_parser.xml" \
    2>&1 | tee "$RESULTS_DIR/real_e2e_parser.txt"
PARSER_EXIT=${PIPESTATUS[0]}
echo ""
echo "[Phase 3] Parser exit code: $PARSER_EXIT"

echo ""
echo "========================================"
echo " Phase 4: Real E2E — Extractor (LLM)"
echo "========================================"
echo ""

python -m pytest tests/test_real_e2e.py \
    -v --tb=long --no-header \
    -k "TestRealExtractorSingleStrategy or TestRealExtractorMultiStrategy" \
    --junitxml="$RESULTS_DIR/real_e2e_extractor.xml" \
    2>&1 | tee "$RESULTS_DIR/real_e2e_extractor.txt"
EXTRACTOR_EXIT=${PIPESTATUS[0]}
echo ""
echo "[Phase 4] Extractor exit code: $EXTRACTOR_EXIT"

echo ""
echo "========================================"
echo " Phase 5: Real E2E — Render"
echo "========================================"
echo ""

python -m pytest tests/test_real_e2e.py \
    -v --tb=long --no-header \
    -k "TestRealRender" \
    --junitxml="$RESULTS_DIR/real_e2e_render.xml" \
    2>&1 | tee "$RESULTS_DIR/real_e2e_render.txt"
RENDER_EXIT=${PIPESTATUS[0]}
echo ""
echo "[Phase 5] Render exit code: $RENDER_EXIT"

echo ""
echo "========================================"
echo " Phase 6: Real E2E — Full Pipeline"
echo "========================================"
echo ""

python -m pytest tests/test_real_e2e.py \
    -v --tb=long --no-header \
    -k "TestRealFullPipeline" \
    --junitxml="$RESULTS_DIR/real_e2e_full_pipeline.xml" \
    2>&1 | tee "$RESULTS_DIR/real_e2e_full_pipeline.txt"
PIPELINE_EXIT=${PIPESTATUS[0]}
echo ""
echo "[Phase 6] Full Pipeline exit code: $PIPELINE_EXIT"

echo ""
echo "========================================"
echo " Phase 7: Library Quality + Regeneration"
echo "========================================"
echo ""

python -m pytest tests/test_real_e2e.py \
    -v --tb=long --no-header \
    -k "TestLibraryQuality or TestLibraryRegeneration" \
    --junitxml="$RESULTS_DIR/real_e2e_library.xml" \
    2>&1 | tee "$RESULTS_DIR/real_e2e_library.txt"
LIBRARY_EXIT=${PIPESTATUS[0]}
echo ""
echo "[Phase 7] Library exit code: $LIBRARY_EXIT"

echo ""
echo "========================================"
echo " Phase 8: Quality Metrics + Cross-Paper"
echo "========================================"
echo ""

python -m pytest tests/test_real_e2e.py \
    -v --tb=long --no-header \
    -k "TestQualityMetrics or TestCrossPaperConsistency" \
    --junitxml="$RESULTS_DIR/real_e2e_quality.xml" \
    2>&1 | tee "$RESULTS_DIR/real_e2e_quality.txt"
QUALITY_EXIT=${PIPESTATUS[0]}
echo ""
echo "[Phase 8] Quality Metrics exit code: $QUALITY_EXIT"

echo ""
echo "========================================"
echo " Phase 9: Coverage Report"
echo "========================================"
echo ""

python -m pytest tests/test_parser.py tests/test_extractor.py tests/test_models.py tests/test_render.py \
    --cov=paper2spec --cov-report=term-missing --cov-report=html:"$RESULTS_DIR/htmlcov" \
    --no-header -q \
    2>&1 | tee "$RESULTS_DIR/coverage.txt"

# ==============================================================================
# SUMMARY
# ==============================================================================

echo ""
echo "========================================"
echo " FINAL SUMMARY"
echo "========================================"
echo ""
echo " Completed: $(date)"
echo " Results:   $RESULTS_DIR/"
echo ""
echo " Phase 1 — Unit Tests:           $([ $UNIT_EXIT -eq 0 ] && echo 'PASSED ✓' || echo 'FAILED ✗')"
echo " Phase 2 — Search & PDF:         $([ $SEARCH_EXIT -eq 0 ] && echo 'PASSED ✓' || echo 'FAILED ✗')"
echo " Phase 3 — Parser (LLM):         $([ $PARSER_EXIT -eq 0 ] && echo 'PASSED ✓' || echo 'FAILED ✗')"
echo " Phase 4 — Extractor (LLM):      $([ $EXTRACTOR_EXIT -eq 0 ] && echo 'PASSED ✓' || echo 'FAILED ✗')"
echo " Phase 5 — Render:               $([ $RENDER_EXIT -eq 0 ] && echo 'PASSED ✓' || echo 'FAILED ✗')"
echo " Phase 6 — Full Pipeline:        $([ $PIPELINE_EXIT -eq 0 ] && echo 'PASSED ✓' || echo 'FAILED ✗')"
echo " Phase 7 — Library:              $([ $LIBRARY_EXIT -eq 0 ] && echo 'PASSED ✓' || echo 'FAILED ✗')"
echo " Phase 8 — Quality & CrossPaper: $([ $QUALITY_EXIT -eq 0 ] && echo 'PASSED ✓' || echo 'FAILED ✗')"
echo ""

# Calculate overall
TOTAL_FAILURES=$((UNIT_EXIT + SEARCH_EXIT + PARSER_EXIT + EXTRACTOR_EXIT + RENDER_EXIT + PIPELINE_EXIT + LIBRARY_EXIT + QUALITY_EXIT))
if [[ $TOTAL_FAILURES -eq 0 ]]; then
    echo " ★ ALL PHASES PASSED — Ready for release"
else
    echo " ✗ $TOTAL_FAILURES phase(s) had failures — review logs above"
fi
echo ""
echo " Detailed results:  $RESULTS_DIR/"
echo " Coverage report:   $RESULTS_DIR/htmlcov/index.html"
echo " JUnit XML:         $RESULTS_DIR/*.xml"
echo "========================================"

# Write machine-readable summary
cat > "$RESULTS_DIR/summary.json" <<EOF
{
  "timestamp": "$TIMESTAMP",
  "phases": {
    "unit_tests": {"exit_code": $UNIT_EXIT},
    "search_pdf": {"exit_code": $SEARCH_EXIT},
    "parser":     {"exit_code": $PARSER_EXIT},
    "extractor":  {"exit_code": $EXTRACTOR_EXIT},
    "render":     {"exit_code": $RENDER_EXIT},
    "pipeline":   {"exit_code": $PIPELINE_EXIT},
    "library":    {"exit_code": $LIBRARY_EXIT},
    "quality":    {"exit_code": $QUALITY_EXIT}
  },
  "total_failures": $TOTAL_FAILURES,
  "all_passed": $([ $TOTAL_FAILURES -eq 0 ] && echo 'true' || echo 'false')
}
EOF

exit $TOTAL_FAILURES
