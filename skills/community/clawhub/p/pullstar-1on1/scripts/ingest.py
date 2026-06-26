"""
ingest.py — GitHub data fetcher for PullStar 1-on-1

Usage:
    python scripts/ingest.py --login jsmith
    python scripts/ingest.py --login jsmith --days 14 --output-dir .pullstar
    python scripts/ingest.py --login jsmith --pr_insights
    python scripts/ingest.py --login jsmith --api-mode rest

GraphQL mode (default when GITHUB_TOKEN is set): fetches all PR, review, and
comment data in 2–4 queries total, dramatically reducing latency and rate-limit
pressure. Falls back to REST automatically when no token is found.

REST mode (--api-mode rest, or automatic fallback): uses PyGithub REST API and
supports unauthenticated access at 60 req/hr.

Phase 2: Adds optional --pr_insights flag for detailed PR discussion context.
         When enabled, each authored PR is enriched with three new fields:
           - reviews_received_detail  (list of compact review objects)
           - comments_detail          (list of compact issue comment objects)
           - discussion_summary_stats (aggregate counts)
         In GraphQL mode these are fetched at no extra API cost.
         In REST mode each PR costs ~3 additional API calls, capped at
         _INSIGHTS_PR_CAP PRs.
         Default mode (no flag) is unchanged.
"""

import argparse
import json
import math
import os
import socket
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import requests
from dotenv import load_dotenv
from github import Github, GithubException, RateLimitExceededException

# Default socket timeout for all network operations (GitHub API calls)
socket.setdefaulttimeout(60)  # 60 seconds per API call max

# Load .env from repo root regardless of where the script is invoked from
load_dotenv(Path(__file__).parent.parent / ".env")

# ---------------------------------------------------------------------------
# Secret resolution and log scrubbing
# ---------------------------------------------------------------------------

_CENTRAL_CREDS_FILE = Path.home() / ".pullstar" / "credentials"
_PROJECT_ENV_FILE   = Path(__file__).parent.parent / ".env"

# Secret values registered here are scrubbed from all log/error output.
_registered_secrets: set[str] = set()


def _register_secret(value: str) -> str:
    """Mark a resolved secret value for log scrubbing. Returns the value unchanged."""
    if value:
        _registered_secrets.add(value)
    return value


def _scrub(text: str) -> str:
    """Replace any registered secret value in text with ***."""
    for secret in _registered_secrets:
        if secret and secret in text:
            text = text.replace(secret, "***")
    return text


def resolve_secret(name: str, cli_value: str | None = None) -> str | None:
    """
    Resolve a secret by name using a layered lookup:
      1. cli_value  — CLI override (highest priority; for debug/testing only)
      2. os.getenv  — environment variable (includes values loaded from .env)
      3. ~/.pullstar/credentials — central credentials file (key=value format)
      4. .env       — project-local .env re-read explicitly as final fallback

    Registers the resolved value for automatic log scrubbing.
    Returns None if not found in any source.
    """
    from dotenv import dotenv_values

    value = (
        (cli_value or "").strip()
        or (os.getenv(name) or "").strip()
        or (dotenv_values(_CENTRAL_CREDS_FILE).get(name) or "").strip()
        or (dotenv_values(_PROJECT_ENV_FILE).get(name) or "").strip()
        or None
    )
    if value:
        _register_secret(value)
    return value


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def fail(msg: str) -> None:
    print(f"Error: {_scrub(msg)}", file=sys.stderr)
    sys.exit(1)


def as_utc(dt: datetime | None) -> datetime | None:
    """Return dt as a timezone-aware UTC datetime, or None."""
    if dt is None:
        return None
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def normalize_review_state(state: str) -> str:
    """Map GitHub review states to the three values in our schema."""
    mapping = {
        "APPROVED": "approved",
        "CHANGES_REQUESTED": "changes_requested",
    }
    return mapping.get(state.upper(), "commented")  # COMMENTED, DISMISSED -> commented


def week_index(dt: datetime, since_dt: datetime) -> int:
    """Return which 0-based week bucket dt falls into relative to since_dt."""
    return int((dt - since_dt).total_seconds() // (7 * 86400))


def _truncate(text: str, limit: int) -> str:
    """Collapse whitespace and truncate to limit chars for a compact excerpt."""
    return " ".join(text.split())[:limit]


def _parse_ts(s: str | None) -> str | None:
    """Normalize a GitHub GraphQL ISO timestamp (trailing Z) to +00:00 form."""
    return s.replace("Z", "+00:00") if s else None


# ---------------------------------------------------------------------------
# Caps and limits
# ---------------------------------------------------------------------------
#
# Each PR costs 3 core API calls in REST mode: get_pull + get_reviews + get_issue_comments.
# At _INSIGHTS_PR_CAP=20, worst case is 60 additional calls against the 5000/hr limit.
# In GraphQL mode, insights are folded into the Phase 1 query at no extra cost.
#
_INSIGHTS_PR_CAP       = 20   # max authored PRs to enrich with insight detail
_INSIGHTS_MAX_REVIEWS  = 10   # max review objects stored per PR
_INSIGHTS_MAX_COMMENTS = 10   # max issue comment objects stored per PR
_INSIGHTS_EXCERPT_LEN  = 600  # chars per body excerpt (reviews and comments)

# Pagination limits to prevent runaway queries on high-activity users
_MAX_SEARCH_RESULTS    = 20  # max total results to iterate from search API
_MAX_REVIEWED_SEARCH   = 20   # max results for reviewed-by search (tight cap for speed)
_SEARCH_PAGE_SIZE      = 30   # fetch search results in smaller chunks

# ---------------------------------------------------------------------------
# GraphQL transport
# ---------------------------------------------------------------------------

_GRAPHQL_URL = "https://api.github.com/graphql"


class _RateLimitError(Exception):
    pass


class _GraphQLError(Exception):
    def __init__(self, errors: list) -> None:
        self.errors = errors
        super().__init__(str(errors))


def _gql(token: str, query: str, variables: dict) -> dict:
    """POST a GraphQL query to GitHub. Returns the data dict or raises on errors."""
    resp = requests.post(
        _GRAPHQL_URL,
        json={"query": query, "variables": variables},
        headers={"Authorization": f"Bearer {token}"},
        timeout=60,
    )
    if resp.status_code in (401, 403):
        fail("GitHub API authentication failed — check your GITHUB_TOKEN.")
    if not resp.ok:
        fail(f"GitHub API HTTP error {resp.status_code}.")
    result = resp.json()
    if "errors" in result:
        for err in result["errors"]:
            if err.get("type") == "RATE_LIMITED":
                raise _RateLimitError(err.get("message", "GitHub GraphQL rate limit exceeded."))
        raise _GraphQLError(result["errors"])
    return result.get("data", {})


# ---------------------------------------------------------------------------
# GraphQL query strings
# ---------------------------------------------------------------------------

_USER_QUERY = """
query($login: String!) {
  user(login: $login) { name }
}
"""

# Base authored-PR query — fetches all PR fields plus accurate review total count.
_AUTHORED_PRS_QUERY = """
query($query: String!, $first: Int!, $cursor: String) {
  search(query: $query, type: ISSUE, first: $first, after: $cursor) {
    pageInfo { hasNextPage endCursor }
    nodes {
      ... on PullRequest {
        number title url state
        createdAt mergedAt
        additions deletions changedFiles
        commits { totalCount }
        body
        labels(first: 10) { nodes { name } }
        baseRefName
        repository { nameWithOwner }
        reviews { totalCount }
      }
    }
  }
}
"""

# Insights variant — same fields plus review and comment bodies (capped at 10 each).
# Used in place of _AUTHORED_PRS_QUERY when --pr_insights is set; no extra API calls needed.
_AUTHORED_PRS_INSIGHTS_QUERY = """
query($query: String!, $first: Int!, $cursor: String) {
  search(query: $query, type: ISSUE, first: $first, after: $cursor) {
    pageInfo { hasNextPage endCursor }
    nodes {
      ... on PullRequest {
        number title url state
        createdAt mergedAt
        additions deletions changedFiles
        commits { totalCount }
        body
        labels(first: 10) { nodes { name } }
        baseRefName
        repository { nameWithOwner }
        reviews(first: 10) {
          totalCount
          nodes { state body author { login } submittedAt }
        }
        comments(first: 10) {
          nodes { body author { login } createdAt }
        }
      }
    }
  }
}
"""

# Fetches PRs reviewed by login, with their review details for client-side filtering.
_REVIEWS_GIVEN_QUERY = """
query($query: String!, $first: Int!, $cursor: String) {
  search(query: $query, type: ISSUE, first: $first, after: $cursor) {
    pageInfo { hasNextPage endCursor }
    nodes {
      ... on PullRequest {
        number title
        repository { nameWithOwner }
        reviews(first: 50) {
          nodes { state body author { login } submittedAt }
        }
      }
    }
  }
}
"""


# ---------------------------------------------------------------------------
# REST: PR insights collector (--pr_insights flag, REST mode only)
# ---------------------------------------------------------------------------

def fetch_pr_details(pr_data: dict, g: Github) -> dict | None:
    """
    Fetch review and comment detail for one authored PR (REST mode only).

    Returns a dict of three insight fields to merge into the PR record:
      - reviews_received_detail:  list of compact review objects (up to _INSIGHTS_MAX_REVIEWS)
      - comments_detail:          list of compact issue comment objects (up to _INSIGHTS_MAX_COMMENTS)
      - discussion_summary_stats: {review_count, comment_count,
                                   changes_requested_count, approved_count}

    Returns None if the PR object itself cannot be fetched.
    Per-section failures (reviews or comments) are logged and produce empty lists.

    API calls: 1 (get_pull) + 1 (get_reviews) + 1 (get_issue + get_comments) = 3.
    """
    repo_name = pr_data["repository"]
    pr_number = pr_data["number"]

    try:
        repo = g.get_repo(repo_name)
        pr   = repo.get_pull(pr_number)
    except GithubException as exc:
        print(f"  warning: could not fetch PR #{pr_number} ({repo_name}) — {exc}",
              file=sys.stderr)
        return None

    # --- Reviews received ---
    reviews_detail: list[dict] = []
    changes_requested_count = 0
    approved_count          = 0

    try:
        print(f"  fetching review details for PR #{pr_number} ({repo_name})...")
        for review in pr.get_reviews():
            if len(reviews_detail) >= _INSIGHTS_MAX_REVIEWS:
                break
            state = normalize_review_state(review.state or "COMMENTED")
            if state == "changes_requested":
                changes_requested_count += 1
            if state == "approved":
                approved_count += 1
            body      = (review.body or "").strip()
            submitted = as_utc(review.submitted_at)
            reviews_detail.append({
                "reviewer_login": review.user.login if review.user else None,
                "state":          state,
                "submitted_at":   submitted.isoformat() if submitted else None,
                "body_length":    len(body),
                "body_excerpt":   _truncate(body, _INSIGHTS_EXCERPT_LEN) if body else "",
            })
    except GithubException as exc:
        print(f"  warning: reviews fetch failed for PR #{pr_number} — {exc}",
              file=sys.stderr)

    # --- Issue comments (top-level PR conversation, not inline code comments) ---
    comments_detail: list[dict] = []

    try:
        print(f"  fetching comments for PR #{pr_number} ({repo_name})...")
        for comment in repo.get_issue(pr_number).get_comments():
            if len(comments_detail) >= _INSIGHTS_MAX_COMMENTS:
                break
            body    = (comment.body or "").strip()
            created = as_utc(comment.created_at)
            comments_detail.append({
                "author_login": comment.user.login if comment.user else None,
                "created_at":   created.isoformat() if created else None,
                "body_length":  len(body),
                "body_excerpt": _truncate(body, _INSIGHTS_EXCERPT_LEN) if body else "",
                "comment_type": "issue_comment",
            })
    except GithubException as exc:
        print(f"  warning: comments fetch failed for PR #{pr_number} — {exc}",
              file=sys.stderr)

    return {
        "reviews_received_detail":  reviews_detail,
        "comments_detail":          comments_detail,
        "discussion_summary_stats": {
            "review_count":            len(reviews_detail),
            "comment_count":           len(comments_detail),
            "changes_requested_count": changes_requested_count,
            "approved_count":          approved_count,
        },
    }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Fetch GitHub activity for a PullStar 1-on-1 brief."
    )
    parser.add_argument("--login",       required=True, help="GitHub username of the engineer")
    parser.add_argument("--days",        type=int, default=5, help="Lookback window in days (default: 5)")
    parser.add_argument("--output-dir",  default=".pullstar", help="Output directory (default: .pullstar)")
    parser.add_argument(
        "--github-token",
        default=None,
        metavar="TOKEN",
        help="[Override/debug only] GitHub PAT. Prefer GITHUB_TOKEN in .env or "
             "~/.pullstar/credentials. Never logged.",
    )
    parser.add_argument(
        "--pr_insights",
        action="store_true",
        default=False,
        help=(
            "Collect lightweight PR discussion context (reviews, revision cycles, "
            "comment counts) for the most recent authored PRs. "
            f"No extra cost in GraphQL mode. "
            f"Adds ~3 API calls per PR in REST mode, capped at {_INSIGHTS_PR_CAP} PRs."
        ),
    )
    parser.add_argument(
        "--max-results",
        type=int,
        default=_MAX_SEARCH_RESULTS,
        metavar="N",
        help=(
            f"Maximum search results to iterate (default: {_MAX_SEARCH_RESULTS}). "
            "Lower for faster runs on high-activity users."
        ),
    )
    parser.add_argument(
        "--api-mode",
        choices=["graphql", "rest"],
        default="graphql",
        help=(
            "API mode: 'graphql' (default) uses GitHub GraphQL for efficiency and "
            "falls back to REST automatically when no GITHUB_TOKEN is found; "
            "'rest' forces the legacy REST API (supports unauthenticated access)."
        ),
    )
    args = parser.parse_args()

    # -- Credential resolution -----------------------------------------------
    token = resolve_secret("GITHUB_TOKEN", cli_value=args.github_token)

    # Determine effective API mode
    if args.api_mode == "graphql" and not token:
        print(
            "> Warning: GITHUB_TOKEN not found — falling back to REST API "
            "(unauthenticated, 60 req/hr).\n"
            "  Set GITHUB_TOKEN in .env or ~/.pullstar/credentials to use GraphQL.",
            file=sys.stderr,
        )
        use_graphql = False
    elif args.api_mode == "graphql":
        use_graphql = True
    else:
        # --api-mode rest
        if not token:
            print(
                "> Warning: GITHUB_TOKEN not found in any credential source — "
                "using unauthenticated GitHub API access.\n"
                "  Rate limit: 60 req/hr. Set GITHUB_TOKEN in .env or "
                "~/.pullstar/credentials for higher limits.",
                file=sys.stderr,
            )
        use_graphql = False

    org_name = os.getenv("GITHUB_ORG", "").strip()
    login    = args.login.strip()
    days     = args.days

    output_dir = Path(args.output_dir)
    output_dir.mkdir(exist_ok=True)

    since_dt    = datetime.now(timezone.utc) - timedelta(days=days)
    since_iso   = since_dt.strftime("%Y-%m-%d")
    total_weeks = math.ceil(days / 7)

    # Initialize REST client if needed (use_graphql=True means g is unused)
    g: Github | None = None
    if not use_graphql:
        g = Github(token, timeout=60) if token else Github(timeout=60)

    # -- Look up engineer display name (best-effort) -------------------------
    engineer_name: str | None = None
    if use_graphql:
        assert token  # guaranteed: use_graphql=True only when token is set
        try:
            data = _gql(token, _USER_QUERY, {"login": login})
            engineer_name = (data.get("user") or {}).get("name")
        except (_RateLimitError, _GraphQLError):
            pass
    else:
        assert g is not None
        try:
            user = g.get_user(login)
            engineer_name = user.name
        except GithubException:
            pass

    # -- Fetch PRs authored --------------------------------------------------
    print(f"> Fetching pull requests for {login} (last {days} days)...")

    pr_query = f"author:{login} is:pr created:>={since_iso}"
    if org_name:
        pr_query += f" org:{org_name}"

    print(f"  query: {pr_query}")
    print(f"  pagination: max {args.max_results} results, {_SEARCH_PAGE_SIZE} per page")

    prs_authored: list[dict] = []

    if use_graphql:
        assert token
        prs_checked = 0
        cursor: str | None = None
        query_str = _AUTHORED_PRS_INSIGHTS_QUERY if args.pr_insights else _AUTHORED_PRS_QUERY

        try:
            while prs_checked < args.max_results:
                batch  = min(_SEARCH_PAGE_SIZE, args.max_results - prs_checked)
                data   = _gql(token, query_str, {"query": pr_query, "first": batch, "cursor": cursor})
                search = data["search"]

                for node in search["nodes"]:
                    prs_checked += 1
                    if not node or "number" not in node:
                        continue

                    gql_state = node["state"]  # OPEN, CLOSED, MERGED (GraphQL enum)
                    if gql_state == "MERGED":
                        status = "merged"
                    elif gql_state == "CLOSED":
                        status = "closed"
                    else:
                        status = "open"

                    reviews_count = node["reviews"]["totalCount"]
                    pr_entry: dict = {
                        "number":                 node["number"],
                        "title":                  node["title"],
                        "url":                    node["url"],
                        "repository":             node["repository"]["nameWithOwner"],
                        "status":                 status,
                        "created_at":             _parse_ts(node["createdAt"]),
                        "merged_at":              _parse_ts(node.get("mergedAt")),
                        "lines_added":            node["additions"] or 0,
                        "lines_deleted":          node["deletions"] or 0,
                        "files_changed":          node["changedFiles"] or 0,
                        "commit_count":           node["commits"]["totalCount"] or 0,
                        "description_length":     len(node.get("body") or ""),
                        "label_names":            [lbl["name"] for lbl in node["labels"]["nodes"]],
                        "base_branch":            node["baseRefName"],
                        "reviews_received_count": reviews_count,
                    }

                    if args.pr_insights and len(prs_authored) < _INSIGHTS_PR_CAP:
                        reviews_nodes  = (node["reviews"]["nodes"]  or [])[:_INSIGHTS_MAX_REVIEWS]
                        comments_nodes = (node["comments"]["nodes"] or [])[:_INSIGHTS_MAX_COMMENTS]

                        reviews_detail: list[dict] = []
                        changes_requested_count = 0
                        approved_count = 0
                        for r in reviews_nodes:
                            state_norm = normalize_review_state(r.get("state") or "COMMENTED")
                            if state_norm == "changes_requested":
                                changes_requested_count += 1
                            if state_norm == "approved":
                                approved_count += 1
                            body = (r.get("body") or "").strip()
                            reviews_detail.append({
                                "reviewer_login": (r.get("author") or {}).get("login"),
                                "state":          state_norm,
                                "submitted_at":   _parse_ts(r.get("submittedAt")),
                                "body_length":    len(body),
                                "body_excerpt":   _truncate(body, _INSIGHTS_EXCERPT_LEN) if body else "",
                            })

                        comments_detail: list[dict] = []
                        for c in comments_nodes:
                            body = (c.get("body") or "").strip()
                            comments_detail.append({
                                "author_login": (c.get("author") or {}).get("login"),
                                "created_at":   _parse_ts(c.get("createdAt")),
                                "body_length":  len(body),
                                "body_excerpt": _truncate(body, _INSIGHTS_EXCERPT_LEN) if body else "",
                                "comment_type": "issue_comment",
                            })

                        pr_entry.update({
                            "reviews_received_detail":  reviews_detail,
                            "comments_detail":          comments_detail,
                            "discussion_summary_stats": {
                                "review_count":            len(reviews_detail),
                                "comment_count":           len(comments_detail),
                                "changes_requested_count": changes_requested_count,
                                "approved_count":          approved_count,
                            },
                        })
                        pr_entry["reviews_received_count"] = len(reviews_detail)

                    prs_authored.append(pr_entry)
                    if len(prs_authored) > 0 and len(prs_authored) % 10 == 0:
                        print(f"  ... {len(prs_authored)} PRs fetched")

                if not search["pageInfo"]["hasNextPage"] or prs_checked >= args.max_results:
                    if prs_checked >= args.max_results:
                        print(f"  (capped at {args.max_results} search results)")
                    break
                cursor = search["pageInfo"]["endCursor"]

        except _RateLimitError as exc:
            fail(str(exc))
        except _GraphQLError as exc:
            errors_str = str(exc.errors)
            if any(kw in errors_str.lower() for kw in ("not found", "forbidden", "validation")):
                fail(
                    f"GitHub rejected the PR search query.\n"
                    f"  The engineer login '{login}' may not be visible to your token.\n"
                    f"  Fine-grained PATs cannot search across arbitrary users — use a classic PAT instead.\n"
                    f"  Create one at: https://github.com/settings/tokens (select 'repo' scope)\n"
                    f"  Full error: {exc.errors}"
                )
            fail(f"GitHub GraphQL error fetching PRs: {exc.errors}")

    else:  # REST
        assert g is not None
        try:
            max_search_results = args.max_results
            pr_results = g.search_issues(pr_query, sort="created", order="desc")
            total_fetched = 0
            for issue in pr_results:
                total_fetched += 1
                if total_fetched > max_search_results:
                    print(f"  (capped at {max_search_results} search results)")
                    break
                if len(prs_authored) >= 100:
                    print("  (capped at 100 PRs)")
                    break
                if len(prs_authored) > 0 and len(prs_authored) % 10 == 0:
                    print(f"  ... {len(prs_authored)} PRs fetched")
                try:
                    repo = g.get_repo(issue.repository.full_name)
                    pr   = repo.get_pull(issue.number)
                except GithubException as exc:
                    print(f"  warning: skipped PR #{issue.number} — {_scrub(str(exc))}", file=sys.stderr)
                    continue

                if pr.merged:
                    status = "merged"
                elif pr.state == "closed":
                    status = "closed"
                else:
                    status = "open"

                prs_authored.append({
                    "number":               pr.number,
                    "title":                pr.title,
                    "url":                  pr.html_url,
                    "repository":           issue.repository.full_name,
                    "status":               status,
                    "created_at":           pr.created_at.isoformat(),
                    "merged_at":            pr.merged_at.isoformat() if pr.merged_at else None,
                    "lines_added":          pr.additions or 0,
                    "lines_deleted":        pr.deletions or 0,
                    "files_changed":        pr.changed_files or 0,
                    "commit_count":         pr.commits or 0,
                    "description_length":   len(pr.body or ""),
                    "label_names":          [lbl.name for lbl in pr.labels],
                    "base_branch":          pr.base.ref,
                    "reviews_received_count": 0,   # populated below when --pr_insights is set
                })

        except RateLimitExceededException:
            fail("GitHub rate limit hit fetching PRs. Wait a moment and retry, or use --api-mode graphql.")
        except GithubException as exc:
            if exc.status == 422:
                fail(
                    f"GitHub rejected the PR search query (422 Validation Failed).\n"
                    f"  This usually means the engineer login '{login}' is not visible to your token.\n"
                    f"  Fine-grained PATs cannot search across arbitrary users — use a classic PAT instead.\n"
                    f"  Create one at: https://github.com/settings/tokens (select 'repo' scope)\n"
                    f"  Full error: {exc.data.get('errors', exc.data)}"
                )
            fail(f"GitHub API error fetching PRs (status {exc.status}): {exc.data}")

    print(f"> Found {len(prs_authored)} PRs authored")

    # -- Fetch reviews given -------------------------------------------------
    print("> Fetching reviews given...")

    review_query = f"reviewed-by:{login} is:pr updated:>={since_iso}"
    if org_name:
        review_query += f" org:{org_name}"

    print(f"  query: {review_query}")
    print(f"  pagination: max {_MAX_REVIEWED_SEARCH} results")

    reviews_given: list[dict] = []

    if use_graphql:
        assert token
        prs_checked = 0
        cursor = None

        try:
            while prs_checked < args.max_results:
                batch  = min(_SEARCH_PAGE_SIZE, args.max_results - prs_checked)
                data   = _gql(token, _REVIEWS_GIVEN_QUERY, {"query": review_query, "first": batch, "cursor": cursor})
                search = data["search"]

                for node in search["nodes"]:
                    prs_checked += 1
                    if not node or "number" not in node:
                        continue
                    repo_name = node["repository"]["nameWithOwner"]
                    for review in (node["reviews"]["nodes"] or []):
                        if not review.get("author") or review["author"].get("login") != login:
                            continue
                        submitted_ts = _parse_ts(review.get("submittedAt"))
                        if not submitted_ts:
                            continue
                        submitted = datetime.fromisoformat(submitted_ts)
                        if submitted < since_dt:
                            continue
                        reviews_given.append({
                            "repository":   repo_name,
                            "pr_number":    node["number"],
                            "pr_title":     node["title"],
                            "state":        normalize_review_state(review.get("state") or "COMMENTED"),
                            "submitted_at": submitted_ts,
                            "body_length":  len(review.get("body") or ""),
                        })

                if not search["pageInfo"]["hasNextPage"] or prs_checked >= args.max_results:
                    if prs_checked >= args.max_results:
                        print(f"  (capped at {args.max_results} search results)")
                    break
                cursor = search["pageInfo"]["endCursor"]

        except _RateLimitError as exc:
            fail(str(exc))
        except _GraphQLError as exc:
            fail(f"GitHub GraphQL error fetching reviews: {exc.errors}")

    else:  # REST
        assert g is not None
        try:
            reviewed_results = g.search_issues(review_query, sort="updated", order="desc")
            prs_checked = 0
            total_reviewed_fetched = 0
            for issue in reviewed_results:
                total_reviewed_fetched += 1
                if total_reviewed_fetched > _MAX_REVIEWED_SEARCH:
                    print(f"  (capped at {_MAX_REVIEWED_SEARCH} search results)")
                    break
                if prs_checked >= 100 or len(reviews_given) >= 100:
                    break
                prs_checked += 1
                try:
                    repo = g.get_repo(issue.repository.full_name)
                    pr   = repo.get_pull(issue.number)
                    for review in pr.get_reviews():
                        if not review.user or review.user.login != login:
                            continue
                        submitted = as_utc(review.submitted_at)
                        if submitted is None or submitted < since_dt:
                            continue
                        reviews_given.append({
                            "repository":  issue.repository.full_name,
                            "pr_number":   pr.number,
                            "pr_title":    pr.title,
                            "state":       normalize_review_state(review.state or "COMMENTED"),
                            "submitted_at": submitted.isoformat(),
                            "body_length":  len(review.body or ""),
                        })
                except GithubException as exc:
                    print(f"  warning: skipped review PR #{issue.number} — {_scrub(str(exc))}", file=sys.stderr)
                    continue

        except RateLimitExceededException:
            fail("GitHub rate limit hit fetching reviews. Wait a moment and retry, or use --api-mode graphql.")
        except GithubException as exc:
            fail(f"GitHub API error fetching reviews (status {exc.status}): {exc.data}")

    print(f"> Found {len(reviews_given)} reviews given")

    # -- PR insights (REST mode only) ----------------------------------------
    # GraphQL mode already embedded insights into prs_authored during Phase 1.
    # In REST mode, each authored PR (up to _INSIGHTS_PR_CAP) is enriched IN PLACE
    # with reviews_received_detail, comments_detail, and discussion_summary_stats.
    if args.pr_insights and not use_graphql:
        assert g is not None
        to_enrich = prs_authored[:_INSIGHTS_PR_CAP]
        print(f"> Fetching PR insights for {len(to_enrich)} PRs "
              f"(capped at {_INSIGHTS_PR_CAP}, ~3 API calls each)...")
        enriched = 0
        for pr_data in to_enrich:
            details = fetch_pr_details(pr_data, g)
            if details:
                pr_data.update(details)
                # Back-fill reviews_received_count from the fetched review count
                pr_data["reviews_received_count"] = (
                    details["discussion_summary_stats"]["review_count"]
                )
                enriched += 1
        print(f"> PR insights written for {enriched} of {len(to_enrich)} PRs")

    # -- Compute summary stats -----------------------------------------------
    total_lines_added   = sum(p["lines_added"]   for p in prs_authored)
    total_lines_deleted = sum(p["lines_deleted"] for p in prs_authored)
    total_lines = total_lines_added + total_lines_deleted
    n_prs = len(prs_authored)

    # Active week = at least 1 PR created or 1 review submitted in that calendar week
    active_week_set: set[int] = set()
    for pr in prs_authored:
        created = as_utc(datetime.fromisoformat(pr["created_at"]))
        w = week_index(created, since_dt)
        if 0 <= w < total_weeks:
            active_week_set.add(w)
    for review in reviews_given:
        submitted = as_utc(datetime.fromisoformat(review["submitted_at"]))
        w = week_index(submitted, since_dt)
        if 0 <= w < total_weeks:
            active_week_set.add(w)

    summary_stats = {
        "total_prs_authored":    n_prs,
        "prs_merged":            sum(1 for p in prs_authored if p["status"] == "merged"),
        "prs_open":              sum(1 for p in prs_authored if p["status"] == "open"),
        "prs_closed_unmerged":   sum(1 for p in prs_authored if p["status"] == "closed"),
        "total_reviews_given":   len(reviews_given),
        "total_reviews_received": sum(p["reviews_received_count"] for p in prs_authored),
        "total_lines_added":     total_lines_added,
        "total_lines_deleted":   total_lines_deleted,
        "avg_pr_size_lines":     round(total_lines / n_prs, 1) if n_prs else 0.0,
        "active_weeks":          len(active_week_set),
        "total_weeks":           total_weeks,
    }

    # -- Build output --------------------------------------------------------
    # PR insight fields (reviews_received_detail, comments_detail,
    # discussion_summary_stats) are embedded directly in prs_authored entries
    # when --pr_insights is used — no separate top-level key needed.
    profile: dict = {
        "engineer_login":  login,
        "engineer_name":   engineer_name,
        "org":             org_name,
        "lookback_days":   days,
        "ingested_at":     datetime.now(timezone.utc).isoformat(),
        "prs_authored":    prs_authored,
        "reviews_given":   reviews_given,
        "reviews_received": [],
        "summary_stats":   summary_stats,
    }

    output_path = output_dir / f"ingest_{login}.json"
    tmp_path    = output_path.with_suffix(".tmp")
    tmp_path.write_text(json.dumps(profile, indent=2, default=str), encoding="utf-8")
    tmp_path.replace(output_path)   # replace() works on Windows; rename() does not

    enriched_count = sum(1 for p in prs_authored if "discussion_summary_stats" in p)
    insights_note  = f" + insights for {enriched_count} PRs" if args.pr_insights else ""
    print(f"> Written to {output_path}{insights_note}")


if __name__ == "__main__":
    main()
