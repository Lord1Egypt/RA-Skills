#!/usr/bin/env python3
"""
scout - verify_release.py
Checks GitHub for bug reports created after a release date.
Helps confirm a release is stable before upgrading.

Usage:
  python3 verify_release.py --repo owner/repo --since YYYY-MM-DD [--json]

Note: GitHub's API `since` parameter filters by *updated* date (not created).
An old issue that received a new comment will appear. Filter results by
`created_at` to focus on genuinely new reports.

Set GITHUB_TOKEN env var for higher API rate limits (your own token, never stored).
"""

import json
import re
import sys
import urllib.error
import urllib.parse
import argparse
from datetime import datetime

from scout_config import github_request


def validate_date(date_str: str) -> bool:
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def fetch_issues(repo: str, since: str, labels: str = "bug") -> list:
    params = urllib.parse.urlencode({
        "state": "open",
        "since": f"{since}T00:00:00Z",
        "per_page": 30,
        "labels": labels,
    })
    url = f"https://api.github.com/repos/{repo}/issues?{params}"
    try:
        return github_request(url)
    except urllib.error.HTTPError as e:
        if e.code == 404:
            raise ValueError(f"Repo not found: {repo}")
        raise


def fetch_all_issues(repo: str, since: str) -> list:
    labeled = fetch_issues(repo, since, labels="bug")
    # Filter labeled results to issues only (not PRs)
    labeled = [i for i in labeled if i.get("pull_request") is None]

    params = urllib.parse.urlencode({
        "state": "open",
        "since": f"{since}T00:00:00Z",
        "per_page": 50,
    })
    url = f"https://api.github.com/repos/{repo}/issues?{params}"
    try:
        all_issues = github_request(url)
    except Exception:
        all_issues = []

    # Use word boundaries to reduce false positives
    keyword_pattern = re.compile(
        r'\b(broken|regression|crash|crashed|crashes|fail|failed|fails|'
        r'bug|error|errors)\b',
        re.IGNORECASE
    )
    keyword_issues = [
        i for i in all_issues
        if keyword_pattern.search(i.get("title", ""))
        and i.get("pull_request") is None
    ]

    seen = {i["number"] for i in labeled}
    combined = labeled + [i for i in keyword_issues if i["number"] not in seen]

    # Filter to only issues *created* after since date (not just updated)
    combined = [i for i in combined if i.get("created_at", "")[:10] >= since]

    return combined


def main():
    parser = argparse.ArgumentParser(
        description="Check for post-release bug reports on GitHub"
    )
    parser.add_argument("--repo", required=True, help="GitHub org/repo (e.g. owner/repo)")
    parser.add_argument("--since", required=True, help="Release date YYYY-MM-DD")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()

    if not validate_date(args.since):
        print(f"⚠️  Invalid date format: '{args.since}' — expected YYYY-MM-DD", file=sys.stderr)
        sys.exit(1)

    try:
        issues = fetch_all_issues(args.repo, args.since)
    except ValueError as e:
        if args.json:
            print(json.dumps({"error": str(e), "repo": args.repo, "since": args.since}))
        else:
            print(f"⚠️  {e}")
        sys.exit(1)
    except Exception as e:
        if args.json:
            print(json.dumps({"error": str(e), "repo": args.repo, "since": args.since}))
        else:
            print(f"⚠️  Could not fetch issues for {args.repo}: {e}")
        sys.exit(1)

    result = {
        "repo": args.repo,
        "since": args.since,
        "issue_count": len(issues),
        "issues": [
            {
                "number": i["number"],
                "title": i["title"],
                "url": i["html_url"],
                "created_at": i["created_at"][:10],
                "labels": [l["name"] for l in i.get("labels", [])],
            }
            for i in issues
        ]
    }

    if args.json:
        print(json.dumps(result, indent=2))
        return

    print(f"Post-release issues for {args.repo} (since {args.since}):\n")
    if not issues:
        print("  ✅ No bug reports or regressions found.")
    else:
        print(f"  ⚠️  {len(issues)} issue(s) created after release:\n")
        for i in result["issues"]:
            labels = f" [{', '.join(i['labels'])}]" if i["labels"] else ""
            print(f"  #{i['number']} ({i['created_at']}){labels}: {i['title']}")
            print(f"    {i['url']}")
    print()


if __name__ == "__main__":
    main()
