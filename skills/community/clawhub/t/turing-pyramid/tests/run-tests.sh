#!/usr/bin/env bash
# Turing Pyramid Test Runner
# Usage: ./run-tests.sh [unit|integration|all]

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

PASSED=0
FAILED=0
SKIPPED=0

run_test() {
    local test_file="$1"
    local test_name="$(basename "$test_file" .sh)"
    
    # Execute with bash even if executable bit was lost in packaging.
    # Tests are never silently skipped: a present test file must pass or fail.
    
    # Reset needs state + clear lock files and gate state before each test
    [[ -f "$SKILL_DIR/assets/needs-state.template.json" ]] && cp "$SKILL_DIR/assets/needs-state.template.json" "$SKILL_DIR/assets/needs-state.json" 2>/dev/null || true
    rm -f "$SKILL_DIR"/assets/*.lock 2>/dev/null || true
    rm -f "$SKILL_DIR"/assets/pending_actions.json "$SKILL_DIR"/assets/gate.lock 2>/dev/null || true
    
    output_file=$(mktemp)
    if WORKSPACE="$SKILL_DIR" SKIP_GATE=true SKIP_DAEMON_FORCE=true timeout "${TEST_TIMEOUT_SECONDS:-300}" bash "$test_file" >"$output_file" 2>&1; then
        echo -e "${GREEN}PASS${NC} $test_name"
        ((PASSED++)) || true
    else
        status=$?
        echo -e "${RED}FAIL${NC} $test_name (exit $status)"
        sed 's/^/    | /' "$output_file" | tail -80
        ((FAILED++)) || true
    fi
    rm -f "$output_file"
}

run_suite() {
    local suite_dir="$1"
    local suite_name="$(basename "$suite_dir")"
    
    if [[ ! -d "$suite_dir" ]]; then
        echo "Suite not found: $suite_dir"
        return
    fi
    
    echo ""
    echo "=== $suite_name tests ==="
    
    for test_file in "$suite_dir"/test_*.sh; do
        [[ -e "$test_file" ]] || continue
        run_test "$test_file"
    done
}

# Main
echo "🔺 Turing Pyramid Test Suite"
echo "============================"

case "${1:-all}" in
    unit)
        run_suite "$SCRIPT_DIR/unit"
        ;;
    integration)
        run_suite "$SCRIPT_DIR/integration"
        ;;
    regression)
        run_suite "$SCRIPT_DIR/regression"
        ;;
    all)
        run_suite "$SCRIPT_DIR/unit"
        run_suite "$SCRIPT_DIR/integration"
        run_suite "$SCRIPT_DIR/regression"
        run_suite "$SCRIPT_DIR"
        ;;
    *)
        echo "Usage: $0 [unit|integration|all]"
        exit 1
        ;;
esac

echo ""
echo "============================"
echo -e "Results: ${GREEN}$PASSED passed${NC}, ${RED}$FAILED failed${NC}, ${YELLOW}$SKIPPED skipped${NC}"

[[ $FAILED -eq 0 ]]
