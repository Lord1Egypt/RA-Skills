#!/usr/bin/env bash
# kai-report-creator — run automated tests
#
# Usage:
#   ./run_tests.sh           # all tests (unit + Playwright)
#   ./run_tests.sh --fast    # unit tests only (no browser, ~1 s)
#
# First-time setup:
#   pip install -r requirements-test.txt
#   playwright install chromium

set -euo pipefail
cd "$(dirname "$0")"

echo "══════════════════════════════════════════"
echo "  kai-report-creator · automated tests"
echo "══════════════════════════════════════════"

if [ "${1-}" = "--fast" ]; then
  echo "Mode: unit tests only (--fast)"
  python3 -m pytest \
    tests/test_export_config.py \
    tests/test_skill_size.py \
    tests/test_validator_profile_artifacts.py \
    tests/test_reference_split_contract.py \
    tests/test_color_system_docs.py \
    tests/test_html_shell_contract.py \
    tests/test_review_docs.py \
    tests/test_doc_sync.py \
    tests/test_shell_metadata.py \
    tests/test_theme_screenshot_assets.py \
    tests/test_context_isolation.py \
    tests/test_late_context_eval.py \
    tests/test_verify_release.py
else
  echo "Mode: full suite (unit + Playwright)"
  python3 -m pytest tests/ "$@"
fi
