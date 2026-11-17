#!/usr/bin/env bash
# fetch-pr.sh — fetch PR metadata and diff; emit a source blob for merge-pr-context.py
#
# Usage:
#   scripts/fetch-pr.sh <pr-url-or-number> [--repo <owner/repo>]
#
# Arguments:
#   <pr-url-or-number>  GitHub PR URL (https://github.com/owner/repo/pull/N)
#                       or bare number (requires --repo or PR_REPO env var)
#   --repo <owner/repo> Repository slug (not needed when a full URL is given)
#
# Environment:
#   PR_REPO — owner/repo fallback when --repo is omitted and arg is a bare number
#
# Output (stdout): one-line JSON blob:
#   { "source": "fetch-pr", "pr_number": N, "repo": "owner/repo",
#     "url": "...", "title": "...", "body": "...",
#     "head_ref": "...", "base_ref": "...", "head_sha": "...",
#     "state": "OPEN|MERGED|CLOSED",
#     "files_changed": N, "additions": N, "deletions": N,
#     "diff": "<unified diff text>" }
#
# Exit codes:
#   0 — success
#   2 — error (gh not found, PR not found, network or auth failure)

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
    -*)        echo "fetch-pr.sh: unknown option: $1" >&2; exit 2 ;;
    *)         PR="$1"; shift ;;
  esac
done

if [[ -z "$PR" ]]; then
  echo "fetch-pr.sh: PR URL or number is required" >&2
  exit 2
fi

if ! command -v gh >/dev/null 2>&1; then
  echo "fetch-pr.sh: gh CLI not found — install GitHub CLI: https://cli.github.com" >&2
  exit 2
fi

# ---------------------------------------------------------------------------
# Build gh flags
# ---------------------------------------------------------------------------
REPO_ARGS=()
if [[ -n "$REPO" ]]; then
  REPO_ARGS=(--repo "$REPO")
fi

# ---------------------------------------------------------------------------
# Fetch PR metadata
# ---------------------------------------------------------------------------
_STDERR_TMP=$(mktemp)
trap 'rm -f "$_STDERR_TMP"' EXIT
PR_META_OUT=$(gh pr view "$PR" "${REPO_ARGS[@]}" \
  --json number,title,body,headRefName,baseRefName,headRefOid,url,files,additions,deletions,state \
  2>"$_STDERR_TMP") || {
  echo "fetch-pr.sh: gh pr view failed: $(cat "$_STDERR_TMP")" >&2
  exit 2
}

# ---------------------------------------------------------------------------
# Fetch PR diff (non-fatal if it fails — diff may be unavailable for closed PRs)
# ---------------------------------------------------------------------------
PR_DIFF=""
PR_DIFF=$(gh pr diff "$PR" "${REPO_ARGS[@]}" 2>/dev/null) || PR_DIFF=""

# ---------------------------------------------------------------------------
# Build JSON safely via Python (shell values in env, never interpolated)
# ---------------------------------------------------------------------------
PR_JSON=$(PR_META="$PR_META_OUT" PR_DIFF="$PR_DIFF" python3 - <<'PY'
import json, os, sys

raw_meta = os.environ.get("PR_META", "")
raw_diff = os.environ.get("PR_DIFF", "")

try:
    data = json.loads(raw_meta)
except json.JSONDecodeError as e:
    print(f"fetch-pr.sh: could not parse gh pr view output: {e}", file=sys.stderr)
    sys.exit(2)

url = data.get("url", "")
# Extract "owner/repo" from URL: https://github.com/owner/repo/pull/N
repo_slug = ""
if url:
    parts = url.replace("https://github.com/", "").split("/pull/")
    if len(parts) == 2:
        repo_slug = parts[0]

result = {
    "source":        "fetch-pr",
    "pr_number":     data.get("number"),
    "repo":          repo_slug,
    "url":           url,
    "title":         data.get("title", ""),
    "body":          data.get("body") or "",
    "head_ref":      data.get("headRefName", ""),
    "base_ref":      data.get("baseRefName", ""),
    "head_sha":      data.get("headRefOid", ""),
    "state":         data.get("state", ""),
    "files_changed": len(data.get("files") or []),
    "additions":     data.get("additions", 0),
    "deletions":     data.get("deletions", 0),
    "diff":          raw_diff,
}
print(json.dumps(result))
PY
) || exit $?

printf '%s\n' "$PR_JSON"
