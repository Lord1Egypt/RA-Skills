#!/usr/bin/env bash
# fetch-reviews.sh — fetch PR review comments and threads; emit a source blob
#
# Usage:
#   scripts/fetch-reviews.sh <pr-url-or-number> [--repo <owner/repo>]
#
# Arguments:
#   <pr-url-or-number>  GitHub PR URL or bare number
#   --repo <owner/repo> Repository slug (not needed when a full URL is given)
#
# Environment:
#   PR_REPO — owner/repo fallback
#
# Output (stdout): one-line JSON blob:
#   { "source": "fetch-reviews", "repo": "owner/repo", "pr_number": N,
#     "review_count": N, "inline_count": N,
#     "reviews": [ { "id": N, "author": "...", "state": "...",
#                    "body": "...", "submitted_at": "..." }, ... ],
#     "inline_comments": [ { "id": N, "author": "...", "path": "...",
#                             "line": N, "body": "...",
#                             "created_at": "..." }, ... ] }
#
# Exit codes:
#   0 — reviews or inline comments found
#   1 — no reviews and no inline comments (absorbed by lobster-safe-run.sh)
#   2 — error (gh not found, PR not found, auth failure)

set -euo pipefail

# ---------------------------------------------------------------------------
# Argument parsing
# ---------------------------------------------------------------------------
PR=""
REPO="${PR_REPO:-}"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --repo)    REPO="${2:?--repo requires a value}"; shift 2 ;;
    --repo=*)  REPO="${1#--repo=}"; shift ;;
    --help|-h)
      sed -n '2,/^$/p' "$0" | grep '^#' | sed 's/^# \?//'
      exit 0 ;;
    -*)        echo "fetch-reviews.sh: unknown option: $1" >&2; exit 2 ;;
    *)         PR="$1"; shift ;;
  esac
done

if [[ -z "$PR" ]]; then
  echo "fetch-reviews.sh: PR URL or number is required" >&2
  exit 2
fi

if ! command -v gh >/dev/null 2>&1; then
  echo "fetch-reviews.sh: gh CLI not found — install GitHub CLI: https://cli.github.com" >&2
  exit 2
fi

# ---------------------------------------------------------------------------
# Resolve owner/repo and PR number
# ---------------------------------------------------------------------------
REPO_ARGS=()
if [[ -n "$REPO" ]]; then
  REPO_ARGS=(--repo "$REPO")
fi

# Extract repo from full URL if repo not yet set
if [[ -z "$REPO" && "$PR" == https://github.com/* ]]; then
  REPO=$(printf '%s' "$PR" | sed 's|https://github.com/||;s|/pull/.*||')
fi

# Resolve PR number (gh pr view returns it reliably for both URL and number inputs)
_STDERR_TMP=$(mktemp)
PR_META_OUT=$(gh pr view "$PR" "${REPO_ARGS[@]}" --json number,url 2>"$_STDERR_TMP") || {
  echo "fetch-reviews.sh: gh pr view failed: $(cat "$_STDERR_TMP")" >&2
  exit 2
}
PR_NUMBER=$(printf '%s' "$PR_META_OUT" | python3 -c \
  'import json,sys; d=json.load(sys.stdin); print(d.get("number",""))')

if [[ -z "$REPO" ]]; then
  PR_URL=$(printf '%s' "$PR_META_OUT" | python3 -c \
    'import json,sys; print(json.load(sys.stdin).get("url",""))')
  if [[ -n "$PR_URL" ]]; then
    REPO=$(printf '%s' "$PR_URL" | sed 's|https://github.com/||;s|/pull/.*||')
  fi
fi

if [[ -z "$PR_NUMBER" || -z "$REPO" ]]; then
  echo "fetch-reviews.sh: could not resolve PR number or repository" >&2
  exit 2
fi

# ---------------------------------------------------------------------------
# Fetch review-level comments and inline comments
# ---------------------------------------------------------------------------
_API_STDERR_TMP=$(mktemp)
_cleanup() { rm -f "${_STDERR_TMP:-}" "$_API_STDERR_TMP"; }
trap _cleanup EXIT
REVIEWS_OUT=$(gh api "repos/${REPO}/pulls/${PR_NUMBER}/reviews" \
  --paginate 2>"$_API_STDERR_TMP") || {
  echo "fetch-reviews.sh: gh api reviews failed: $(cat "$_API_STDERR_TMP")" >&2
  exit 2
}

INLINE_OUT=$(gh api "repos/${REPO}/pulls/${PR_NUMBER}/comments" \
  --paginate 2>"$_API_STDERR_TMP") || {
  echo "fetch-reviews.sh: gh api inline comments failed: $(cat "$_API_STDERR_TMP")" >&2
  exit 2
}

# ---------------------------------------------------------------------------
# Build JSON; exit 1 if no activity at all
# ---------------------------------------------------------------------------
set +e
RESULT_JSON=$(REVIEWS_RAW="$REVIEWS_OUT" INLINE_RAW="$INLINE_OUT" \
  REPO="$REPO" PR_NUMBER="$PR_NUMBER" python3 - <<'PY'
import json, os, sys

repo      = os.environ.get("REPO", "")
pr_number = int(os.environ.get("PR_NUMBER", "0") or "0")

def parse_paginated(raw):
    """Collect items from one or more JSON arrays (gh --paginate output)."""
    items = []
    for line in raw.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            chunk = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(chunk, list):
            items.extend(chunk)
    return items

reviews_raw = os.environ.get("REVIEWS_RAW", "")
inline_raw  = os.environ.get("INLINE_RAW", "")

raw_reviews = parse_paginated(reviews_raw)
raw_inline  = parse_paginated(inline_raw)

reviews = [
    {
        "id":           r.get("id"),
        "author":       (r.get("user") or {}).get("login", ""),
        "state":        r.get("state", ""),
        "body":         r.get("body") or "",
        "submitted_at": r.get("submitted_at", ""),
    }
    for r in raw_reviews
    # Skip PENDING reviews (draft reviews that haven't been submitted)
    if r.get("state") != "PENDING"
]

inline = [
    {
        "id":         c.get("id"),
        "author":     (c.get("user") or {}).get("login", ""),
        "path":       c.get("path", ""),
        "line":       c.get("line") or c.get("original_line"),
        "body":       c.get("body", ""),
        "created_at": c.get("created_at", ""),
    }
    for c in raw_inline
]

result = {
    "source":          "fetch-reviews",
    "repo":            repo,
    "pr_number":       pr_number,
    "review_count":    len(reviews),
    "inline_count":    len(inline),
    "reviews":         reviews,
    "inline_comments": inline,
}
print(json.dumps(result))

if not reviews and not inline:
    sys.exit(1)
PY
)
PYTHON_RC=$?
set -e

printf '%s\n' "$RESULT_JSON"
exit $PYTHON_RC
