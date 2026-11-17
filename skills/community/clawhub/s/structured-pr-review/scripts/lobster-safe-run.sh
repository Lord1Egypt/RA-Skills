#!/usr/bin/env bash
# lobster-safe-run.sh — run a command and absorb exit 1 (soft / no-data signal)
#
# Lobster workflow steps abort the pipeline on any non-zero exit code.
# PR data-fetch scripts return exit 1 for "nothing found" (an expected soft
# signal — e.g. fetch-reviews.sh exits 1 when the PR has no reviews yet) and
# exit ≥2 for real errors (missing gh, auth failures, PR not found, etc.).
#
# This wrapper absorbs only exit 1 so Lobster captures the empty JSON blob
# and continues to the merge step; exit ≥2 propagates so genuine errors still
# fail the workflow and are not silently swallowed.
#
# Usage (in pr-review-workflow.lobster step commands):
#   scripts/lobster-safe-run.sh scripts/fetch-reviews.sh "$PR" --repo "$REPO"
#
# Exit codes:
#   0  — wrapped command exited 0 (data found) or 1 (no data — absorbed)
#   2+ — wrapped command exited ≥2; passed through unchanged

set -o pipefail

"$@"
_RC=$?
# Absorb exit 1 (no-data — expected, empty/minimal JSON on stdout).
# Propagate exit ≥2 (real errors) so Lobster aborts the workflow.
[[ $_RC -le 1 ]] && exit 0 || exit $_RC
