#!/usr/bin/env bash
# X Bookmarks Digest — Orchestrator
# Usage: digest_runner.sh [--count N] [--force] [--all] [--dry-run]
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
BASE_DIR="$(dirname "$SCRIPT_DIR")"
PYTHON="python3"

COUNT=50
FORCE=""
ALL=""
DRY_RUN=""

while [[ $# -gt 0 ]]; do
    case "$1" in
        --count) COUNT="$2"; shift 2 ;;
        --force) FORCE="--force"; shift ;;
        --all)   ALL="--all"; shift ;;
        --dry-run) DRY_RUN="--dry-run"; shift ;;
        *) echo "Unknown option: $1" >&2; exit 1 ;;
    esac
done

# Step 1: Check xurl auth
echo "--- Checking xurl authentication..." >&2
if ! xurl whoami >/dev/null 2>&1; then
    echo "ERROR: xurl auth failed. Run: xurl auth apps add <app> --client-id <id> --client-secret <secret>" >&2
    exit 1
fi
echo "--- Auth OK" >&2

# Step 2: Fetch bookmarks
echo "--- Fetching bookmarks (count=$COUNT)..." >&2
BOOKMARKS=$($PYTHON "$SCRIPT_DIR/fetch_bookmarks.py" --count "$COUNT" $FORCE $ALL $DRY_RUN 2>&1)
FETCH_EXIT=$?

if [[ $FETCH_EXIT -ne 0 ]]; then
    echo "ERROR: Fetch failed:" >&2
    echo "$BOOKMARKS" >&2
    exit $FETCH_EXIT
fi

# Check if empty
if [[ "$BOOKMARKS" == "[]" ]] || [[ -z "$BOOKMARKS" ]]; then
    echo "No new bookmarks since last check." >&2
    exit 0
fi

# Step 3: Analyse
echo "--- Analysing bookmarks..." >&2
ANALYSIS=$(echo "$BOOKMARKS" | $PYTHON "$SCRIPT_DIR/analyse_bookmarks.py")

# Step 4: Output
echo "$ANALYSIS"

# Summary to stderr
TOTAL=$(echo "$ANALYSIS" | $PYTHON -c "import sys,json; d=json.load(sys.stdin); print(d['summary']['total'])")
HIGH=$(echo "$ANALYSIS" | $PYTHON -c "import sys,json; d=json.load(sys.stdin); print(d['summary']['high'])")
MEDIUM=$(echo "$ANALYSIS" | $PYTHON -c "import sys,json; d=json.load(sys.stdin); print(d['summary']['medium'])")
echo "--- Done: $TOTAL bookmarks analysed ($HIGH high-value, $MEDIUM medium)" >&2
