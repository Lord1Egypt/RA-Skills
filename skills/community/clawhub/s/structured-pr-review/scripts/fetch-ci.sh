#!/usr/bin/env bash
# fetch-ci.sh — fetch CI / check-run status for a PR; emit a source blob
#
# Usage:
#   scripts/fetch-ci.sh <pr-url-or-number> [--repo <owner/repo>] [--sha <sha>]
#
# Arguments:
#   <pr-url-or-number>  GitHub PR URL or bare number
#   --repo <owner/repo> Repository slug (not needed when a full URL is given)
#   --sha <sha>         Commit SHA to query (skips PR metadata lookup)
#
# Environment:
#   PR_REPO — owner/repo fallback
#   PR_SHA  — commit SHA fallback (skips PR metadata lookup when set)
#
# Output (stdout): one-line JSON blob:
#   { "source": "fetch-ci", "sha": "...", "repo": "owner/repo",
#     "overall": "pass|fail|pending|none",
#     "total": N, "passed": N, "failed": N, "pending": N,
#     "runs": [ { "name": "...", "status": "...", "conclusion": "...",
#                 "details_url": "..." }, ... ] }
#
# Exit codes:
#   0 — all checks pass, or no checks exist (overall: "none")
#   1 — one or more checks failing or pending — absorbed by lobster-safe-run.sh
#   2 — error (gh not found, PR not found, auth failure)

set -euo pipefail

# ---------------------------------------------------------------------------
# Argument parsing
# ---------------------------------------------------------------------------
PR=""
REPO="${PR_REPO:-}"
SHA="${PR_SHA:-}"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --repo)    REPO="${2:?--repo requires a value}"; shift 2 ;;
    --repo=*)  REPO="${1#--repo=}"; shift ;;
    --sha)     SHA="${2:?--sha requires a value}"; shift 2 ;;
    --sha=*)   SHA="${1#--sha=}"; shift ;;
    --help|-h)
      sed -n '2,/^$/p' "$0" | grep '^#' | sed 's/^# \?//'
      exit 0 ;;
    -*)        echo "fetch-ci.sh: unknown option: $1" >&2; exit 2 ;;
    *)         PR="$1"; shift ;;
  esac
done

if [[ -z "$PR" && -z "$SHA" ]]; then
  echo "fetch-ci.sh: PR URL/number or --sha is required" >&2
  exit 2
fi

if ! command -v gh >/dev/null 2>&1; then
  echo "fetch-ci.sh: gh CLI not found — install GitHub CLI: https://cli.github.com" >&2
  exit 2
fi

# ---------------------------------------------------------------------------
# Resolve owner/repo and commit SHA
# ---------------------------------------------------------------------------
REPO_ARGS=()
if [[ -n "$REPO" ]]; then
  REPO_ARGS=(--repo "$REPO")
fi

# Extract repo from full URL if repo not yet set
if [[ -z "$REPO" && "$PR" == https://github.com/* ]]; then
  REPO=$(printf '%s' "$PR" | sed 's|https://github.com/||;s|/pull/.*||')
fi

if [[ -z "$SHA" ]]; then
  _STDERR_TMP=$(mktemp)
  SHA_OUT=$(gh pr view "$PR" "${REPO_ARGS[@]}" --json headRefOid 2>"$_STDERR_TMP") || {
    echo "fetch-ci.sh: gh pr view failed: $(cat "$_STDERR_TMP")" >&2
    exit 2
  }
  SHA=$(printf '%s' "$SHA_OUT" | python3 -c \
    'import json,sys; print(json.load(sys.stdin).get("headRefOid",""))')
fi

if [[ -z "$SHA" || -z "$REPO" ]]; then
  echo "fetch-ci.sh: could not resolve repo or commit SHA" >&2
  exit 2
fi

# ---------------------------------------------------------------------------
# Fetch check runs via GitHub API
# ---------------------------------------------------------------------------
_API_STDERR_TMP=$(mktemp)
_cleanup() { rm -f "${_STDERR_TMP:-}" "$_API_STDERR_TMP"; }
trap _cleanup EXIT
CHECK_OUT=$(gh api "repos/${REPO}/commits/${SHA}/check-runs" \
  --paginate --jq '.check_runs' 2>"$_API_STDERR_TMP") || {
  echo "fetch-ci.sh: gh api check-runs failed: $(cat "$_API_STDERR_TMP")" >&2
  exit 2
}

# ---------------------------------------------------------------------------
# Build JSON + determine overall status
# ---------------------------------------------------------------------------
# Disable errexit around the command substitution: python3 exits 1 for
# failing/pending checks (a soft signal, not an error).  With set -e active,
# bash would abort on that non-zero exit before PYTHON_RC=$? runs — mirroring
# the pattern used in fetch-reviews.sh.
set +e
RESULT_JSON=$(SHA="$SHA" REPO="$REPO" CHECK_RAW="$CHECK_OUT" python3 - <<'PY'
import json, os, sys

sha  = os.environ.get("SHA", "")
repo = os.environ.get("REPO", "")
raw  = os.environ.get("CHECK_RAW", "")

# gh api --paginate emits one JSON array per page; collect all
runs = []
for line in raw.splitlines():
    line = line.strip()
    if not line:
        continue
    try:
        chunk = json.loads(line)
    except json.JSONDecodeError:
        continue
    if isinstance(chunk, list):
        runs.extend(chunk)

simplified = []
for r in runs:
    simplified.append({
        "name":        r.get("name", ""),
        "status":      r.get("status", ""),
        "conclusion":  r.get("conclusion") or "",
        "details_url": r.get("details_url") or "",
    })

if not simplified:
    overall = "none"
    passed = failed = pending_count = 0
else:
    failed = sum(
        1 for r in simplified
        if r["conclusion"] in ("failure", "timed_out", "cancelled", "action_required")
    )
    pending_count = sum(
        1 for r in simplified
        if r["status"] in ("in_progress", "queued", "waiting")
    )
    passed = len(simplified) - failed - pending_count
    if failed > 0:
        overall = "fail"
    elif pending_count > 0:
        overall = "pending"
    else:
        overall = "pass"

result = {
    "source":  "fetch-ci",
    "sha":     sha,
    "repo":    repo,
    "overall": overall,
    "total":   len(simplified),
    "passed":  passed,
    "failed":  failed,
    "pending": pending_count,
    "runs":    simplified,
}
print(json.dumps(result))

# Signal degraded via exit 1 if overall is not pass or none
if overall in ("fail", "pending"):
    sys.exit(1)
PY
)
PYTHON_RC=$?
set -e

printf '%s\n' "$RESULT_JSON"
exit $PYTHON_RC
