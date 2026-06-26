#!/usr/bin/env python3
"""
GitHub PR & Review Collector

Collects PRs, code reviews, issue comments from a target GitHub user.

Usage:
    python3 github_collector.py --username "alexchen" --repos "org/repo1,org/repo2" --output-dir ./knowledge/alex
    python3 github_collector.py --username "alexchen" --org "mycompany" --output-dir ./knowledge/alex
"""

from __future__ import annotations

import json
import argparse
import os
import sys
from pathlib import Path
from datetime import datetime, timezone
from urllib.request import urlopen, Request
from urllib.error import HTTPError
from typing import Optional

GITHUB_API = "https://api.github.com"


def gh_request(path: str, token: Optional[str] = None, params: dict = None) -> dict | list:
    """Make a GitHub API request with retry on rate limit."""
    url = f"{GITHUB_API}{path}"
    if params:
        query = "&".join(f"{k}={v}" for k, v in params.items())
        url = f"{url}?{query}"

    headers = {"Accept": "application/vnd.github.v3+json"}
    if token:
        headers["Authorization"] = f"token {token}"

    req = Request(url, headers=headers)
    max_retries = 3
    for attempt in range(max_retries):
        try:
            with urlopen(req) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except HTTPError as e:
            if e.code == 403:
                # Check if rate limited
                reset_time = e.headers.get("X-RateLimit-Reset")
                remaining = e.headers.get("X-RateLimit-Remaining", "?")
                if remaining == "0" and reset_time:
                    import time as _time
                    wait_seconds = max(int(reset_time) - int(_time.time()), 1)
                    wait_seconds = min(wait_seconds, 300)  # cap at 5 min
                    print(f"   ⏳ Rate limited, waiting {wait_seconds}s (attempt {attempt+1}/{max_retries})...")
                    _time.sleep(wait_seconds)
                    continue
                if not token:
                    print("⚠️  Rate limited. Set GITHUB_TOKEN env var for 5000 req/hr (vs 60 unauthenticated).")
            if e.code == 404:
                return []  # repo not found or private without auth
            raise
    raise Exception(f"GitHub API failed after {max_retries} retries: {path}")


def collect_prs(username: str, repos: list, token: Optional[str], pr_limit: int) -> list:
    """Collect PRs authored by the target user."""
    prs = []
    for repo in repos:
        try:
            page = 1
            while len(prs) < pr_limit:
                data = gh_request(
                    f"/repos/{repo}/pulls",
                    token=token,
                    params={"state": "all", "per_page": 30, "page": page}
                )
                if not data:
                    break
                for pr in data:
                    if pr.get("user", {}).get("login", "").lower() == username.lower():
                        prs.append({
                            "repo": repo,
                            "number": pr["number"],
                            "title": pr["title"],
                            "body": (pr.get("body") or "")[:2000],
                            "state": pr["state"],
                            "created_at": pr["created_at"],
                            "additions": pr.get("additions", 0),
                            "deletions": pr.get("deletions", 0),
                        })
                page += 1
                if len(data) < 30:
                    break
        except Exception as e:
            print(f"⚠️  Error fetching PRs from {repo}: {e}")
    return prs[:pr_limit]


def collect_reviews(username: str, repos: list, token: Optional[str], review_limit: int) -> list:
    """Collect code review comments left by the target user."""
    reviews = []
    for repo in repos:
        try:
            page = 1
            while len(reviews) < review_limit:
                data = gh_request(
                    f"/repos/{repo}/pulls/comments",
                    token=token,
                    params={"per_page": 50, "page": page, "sort": "created", "direction": "desc"}
                )
                if not data:
                    break
                for comment in data:
                    if comment.get("user", {}).get("login", "").lower() == username.lower():
                        reviews.append({
                            "repo": repo,
                            "pr_url": comment.get("pull_request_url", ""),
                            "path": comment.get("path", ""),
                            "body": (comment.get("body") or "")[:1000],
                            "created_at": comment["created_at"],
                        })
                page += 1
                if len(data) < 50:
                    break
        except Exception as e:
            print(f"⚠️  Error fetching reviews from {repo}: {e}")
    return reviews[:review_limit]


def collect_issues(username: str, repos: list, token: Optional[str], limit: int = 50) -> list:
    """Collect issue comments from the target user."""
    comments = []
    for repo in repos:
        try:
            page = 1
            while len(comments) < limit:
                data = gh_request(
                    f"/repos/{repo}/issues/comments",
                    token=token,
                    params={"per_page": 50, "page": page, "sort": "created", "direction": "desc"}
                )
                if not data:
                    break
                for comment in data:
                    if comment.get("user", {}).get("login", "").lower() == username.lower():
                        comments.append({
                            "repo": repo,
                            "issue_url": comment.get("issue_url", ""),
                            "body": (comment.get("body") or "")[:1000],
                            "created_at": comment["created_at"],
                        })
                page += 1
                if len(data) < 50:
                    break
        except Exception as e:
            print(f"⚠️  Error fetching issue comments from {repo}: {e}")
    return comments[:limit]


def main():
    parser = argparse.ArgumentParser(description="GitHub PR & review collector")
    parser.add_argument("--username", required=True, help="GitHub username")
    parser.add_argument("--repos", help="Comma-separated repo list (org/repo)")
    parser.add_argument("--org", help="GitHub org — collect from all repos")
    parser.add_argument("--output-dir", default="./knowledge", help="Output directory")
    parser.add_argument("--pr-limit", type=int, default=50, help="Max PRs")
    parser.add_argument("--review-limit", type=int, default=100, help="Max review comments")
    parser.add_argument("--token", help="GitHub token (or set GITHUB_TOKEN env var)")

    args = parser.parse_args()
    token = args.token or os.environ.get("GITHUB_TOKEN")

    # Determine repos
    repos = []
    if args.repos:
        repos = [r.strip() for r in args.repos.split(",")]
    elif args.org:
        try:
            org_repos = gh_request(f"/orgs/{args.org}/repos", token=token, params={"per_page": 100})
            repos = [r["full_name"] for r in org_repos]
        except Exception as e:
            print(f"❌ Failed to list org repos: {e}")
            sys.exit(1)
    else:
        parser.error("Either --repos or --org is required")

    print(f"Collecting data for @{args.username} from {len(repos)} repos...")

    # Collect
    prs = collect_prs(args.username, repos, token, args.pr_limit)
    reviews = collect_reviews(args.username, repos, token, args.review_limit)
    issues = collect_issues(args.username, repos, token)

    # Write output
    out_path = Path(args.output_dir)
    out_path.mkdir(parents=True, exist_ok=True)

    # PRs
    with open(out_path / "prs.txt", "w", encoding="utf-8") as f:
        f.write(f"# GitHub PRs by @{args.username}\n")
        f.write(f"# Total: {len(prs)} PRs\n\n")
        for pr in prs:
            f.write(f"## [{pr['repo']}] PR #{pr['number']}: {pr['title']} ({pr['state']})\n")
            f.write(f"Date: {pr['created_at'][:10]} | +{pr['additions']} -{pr['deletions']}\n")
            if pr['body']:
                f.write(f"{pr['body']}\n")
            f.write("\n---\n\n")

    # Reviews
    with open(out_path / "reviews.txt", "w", encoding="utf-8") as f:
        f.write(f"# GitHub Code Reviews by @{args.username}\n")
        f.write(f"# Total: {len(reviews)} comments\n\n")
        for r in reviews:
            f.write(f"[{r['created_at'][:10]}] {r['repo']} — {r['path']}\n")
            f.write(f"{r['body']}\n\n---\n\n")

    # Issues
    with open(out_path / "issues.txt", "w", encoding="utf-8") as f:
        f.write(f"# GitHub Issue Comments by @{args.username}\n")
        f.write(f"# Total: {len(issues)} comments\n\n")
        for c in issues:
            f.write(f"[{c['created_at'][:10]}] {c['repo']}\n")
            f.write(f"{c['body']}\n\n---\n\n")

    # Summary
    summary = {
        "username": args.username,
        "repos_scanned": len(repos),
        "prs_collected": len(prs),
        "reviews_collected": len(reviews),
        "issues_collected": len(issues),
        "collected_at": datetime.now(timezone.utc).isoformat(),
    }
    with open(out_path / "collection_summary.json", "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    print(f"\n✅ Collection complete:")
    print(f"   PRs: {len(prs)}")
    print(f"   Review comments: {len(reviews)}")
    print(f"   Issue comments: {len(issues)}")
    print(f"   Output: {out_path}/")


if __name__ == "__main__":
    main()
