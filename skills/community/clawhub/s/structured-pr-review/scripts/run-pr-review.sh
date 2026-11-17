#!/usr/bin/env bash
# run-pr-review.sh — PR data-gathering orchestrator with optional Lobster path
#
# Detects whether Lobster is available and uses the structured workflow when
# it is; falls back to the direct pipe-through pattern otherwise.
# Lobster workflow failures also fall back to the direct path (with a warning).
# In both cases the output is a pr-context-v0 JSON blob on stdout which the
# agent uses for its structured review analysis.
#
# Usage:
#   scripts/run-pr-review.sh <pr-url-or-number> [options]
#   PR=<url-or-number> scripts/run-pr-review.sh [options]
#
# Options:
#   --repo <owner/repo>  Repository slug (required for bare PR numbers)
#   --no-lobster         Force direct fallback even if Lobster is installed
#   --lobster-mode       Require Lobster; exit 3 if not available
#   --tool-mode          Pass --mode tool to Lobster (JSON envelope output)
#   --dry-run            Pass --dry-run to Lobster (plan only, no API calls)
#   --help, -h           Show this help
#
# Exit codes:
#   0  — success (pr-context-v0 JSON on stdout)
#   1  — partial context (pr data present; some optional blobs absent)
#   2  — script / config error
#   3  — missing dependency (Lobster required but not available)

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# ---------------------------------------------------------------------------
# Argument parsing
# ---------------------------------------------------------------------------
PR="${PR:-}"
REPO="${PR_REPO:-}"
FORCE_DIRECT=false
REQUIRE_LOBSTER=false
TOOL_MODE=false
DRY_RUN=false

while [[ $# -gt 0 ]]; do
  case "$1" in
    --repo)         REPO="${2:?--repo requires a value}"; shift 2 ;;
    --repo=*)       REPO="${1#--repo=}"; shift ;;
    --no-lobster)   FORCE_DIRECT=true; shift ;;
    --lobster-mode) REQUIRE_LOBSTER=true; shift ;;
    --tool-mode)    TOOL_MODE=true; shift ;;
    --dry-run)      DRY_RUN=true; shift ;;
    --help|-h)
      sed -n '2,/^$/p' "$0" | grep '^#' | sed 's/^# \?//'
      exit 0 ;;
    -*)             echo "run-pr-review.sh: unknown option: $1" >&2; exit 2 ;;
    *)              PR="$1"; shift ;;
  esac
done

if [[ -z "$PR" ]]; then
  echo "run-pr-review.sh: PR URL or number is required (positional arg or PR env)" >&2
  exit 2
fi

# ---------------------------------------------------------------------------
# Helpers (used by both the Lobster path and the direct fallback)
# ---------------------------------------------------------------------------

# _component — run a data-fetch sub-script, absorbing exit 1 (no-data signal)
# so that set -e does not abort the group before all components contribute.
# Exit-code contract: exit 1 is absorbed (soft signal — e.g. no reviews yet,
# checks failing/pending); exit ≥2 is propagated unchanged (real error).
_component() {
  local _rc=0
  "$@" || _rc=$?
  return $(( _rc == 1 ? 0 : _rc ))
}

# run_direct — collect PR context via individual fetch scripts without Lobster.
run_direct() {
  local _repo_args=()
  [[ -n "$REPO" ]] && _repo_args=(--repo "$REPO")
  {
    _component "$SCRIPT_DIR/fetch-pr.sh"      "$PR" "${_repo_args[@]}"
    _component "$SCRIPT_DIR/fetch-ci.sh"      "$PR" "${_repo_args[@]}"
    _component "$SCRIPT_DIR/fetch-reviews.sh" "$PR" "${_repo_args[@]}"
  } | "$SCRIPT_DIR/merge-pr-context.py"
}

# ---------------------------------------------------------------------------
# Lobster detection
# ---------------------------------------------------------------------------
_LOBSTER_BIN=""
if ! $FORCE_DIRECT; then
  if command -v lobster >/dev/null 2>&1; then
    _LOBSTER_BIN="lobster"
  elif command -v npx >/dev/null 2>&1 && npx --no-install @clawdbot/lobster version >/dev/null 2>&1; then
    _LOBSTER_BIN="npx --no-install @clawdbot/lobster"
  fi
fi

if $REQUIRE_LOBSTER && [[ -z "$_LOBSTER_BIN" ]]; then
  echo "run-pr-review.sh: Lobster not found and --lobster-mode was requested" >&2
  echo "  Install: npm install -g @clawdbot/lobster" >&2
  exit 3
fi

# ---------------------------------------------------------------------------
# Lobster path
# ---------------------------------------------------------------------------
if [[ -n "$_LOBSTER_BIN" ]]; then
  WORKFLOW="${SCRIPT_DIR}/pr-review-workflow.lobster"
  if [[ ! -f "$WORKFLOW" ]]; then
    echo "run-pr-review.sh: workflow file not found: $WORKFLOW" >&2
    echo "  Falling back to direct execution." >&2
    _LOBSTER_BIN=""  # fall through to direct path below
  fi
fi

if [[ -n "$_LOBSTER_BIN" ]]; then
  # Build JSON safely via Python — shell values in env, never interpolated
  ARGS_JSON=$(PR="$PR" REPO="$REPO" python3 - <<'PY'
import json, os
print(json.dumps({
    "pr":   os.environ["PR"],
    "repo": os.environ["REPO"],
}))
PY
)

  SKILL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

  LOBSTER_CMD=($_LOBSTER_BIN run)
  $TOOL_MODE && LOBSTER_CMD+=(--mode tool)
  $DRY_RUN   && LOBSTER_CMD+=(--dry-run)
  LOBSTER_CMD+=(--file "$WORKFLOW" --args-json "$ARGS_JSON")

  # Dry-run: just print the plan and pass through Lobster's exit code.
  if $DRY_RUN; then
    cd "$SKILL_DIR"
    exec "${LOBSTER_CMD[@]}"
  fi

  cd "$SKILL_DIR"

  # Capture Lobster stdout to a temp file to avoid hitting OS env-size limits
  # when forwarding large PR diffs through environment variables.
  _LOBSTER_TMPFILE=$(mktemp)
  _CONTEXT_TMPFILE=$(mktemp)
  trap 'rm -f "$_LOBSTER_TMPFILE" "$_CONTEXT_TMPFILE"' EXIT

  LOBSTER_RC=0
  "${LOBSTER_CMD[@]}" > "$_LOBSTER_TMPFILE" || LOBSTER_RC=$?

  if [[ $LOBSTER_RC -ne 0 ]]; then
    echo "run-pr-review.sh: Lobster workflow failed (exit $LOBSTER_RC); falling back to direct path" >&2
    # Surface whatever Lobster produced to stderr for inspection
    [[ -s "$_LOBSTER_TMPFILE" ]] && cat "$_LOBSTER_TMPFILE" >&2
    run_direct
    exit $?
  fi

  # Extract the context JSON from Lobster output. Lobster may emit either:
  #   - a compact JSON object per line
  #   - a pretty-printed JSON object
  #   - a JSON array containing step outputs / final context objects
  # Read the Lobster output from the temp file (not an env var) to handle large diffs.
  python3 - "$_LOBSTER_TMPFILE" <<'PY' > "$_CONTEXT_TMPFILE"
import json, sys


def find_context(obj):
    if isinstance(obj, dict):
        if obj.get("schema") == "pr-context-v0":
            return obj
        for value in obj.values():
            found = find_context(value)
            if found is not None:
                return found
    elif isinstance(obj, list):
        # Prefer the last context object because workflow runners may include
        # intermediate envelopes before the final merged context.
        for value in reversed(obj):
            found = find_context(value)
            if found is not None:
                return found
    return None


with open(sys.argv[1]) as fh:
    raw = fh.read()

try:
    parsed = json.loads(raw)
except json.JSONDecodeError:
    parsed = None

context = find_context(parsed) if parsed is not None else None

if context is None:
    for line in raw.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            context = find_context(json.loads(line))
        except json.JSONDecodeError:
            continue
        if context is not None:
            break

if context is not None:
    print(json.dumps(context))
PY

  if [[ ! -s "$_CONTEXT_TMPFILE" ]]; then
    # No pr-context-v0 found — surface raw output and fall back to direct path
    echo "run-pr-review.sh: no pr-context-v0 found in Lobster output; falling back to direct path" >&2
    [[ -s "$_LOBSTER_TMPFILE" ]] && cat "$_LOBSTER_TMPFILE" >&2
    run_direct
    exit $?
  fi

  cat "$_CONTEXT_TMPFILE"

  # Detect partial output (ci or reviews sections empty/none).
  # Read from the temp file rather than an env var to handle large contexts.
  PARTIAL=$(python3 - "$_CONTEXT_TMPFILE" <<'PY'
import json, sys
with open(sys.argv[1]) as fh:
    try:
        d = json.load(fh)
    except json.JSONDecodeError:
        sys.exit(0)
present = set(d.get("blobs_present", []))
if "fetch-ci" not in present or "fetch-reviews" not in present:
    print("partial")
PY
)
  [[ "$PARTIAL" == "partial" ]] && exit 1 || exit 0
fi

# ---------------------------------------------------------------------------
# Direct fallback path (no Lobster)
# ---------------------------------------------------------------------------
run_direct
