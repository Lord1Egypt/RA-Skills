#!/usr/bin/env python3
"""List Yuque repositories (knowledge bases).

Usage:
    python list_repos.py                          # list current user's repos
    python list_repos.py --user my_login          # list a user's repos
    python list_repos.py --group my-team          # list a group's repos
    python list_repos.py --offset 0 --limit 50
"""

import argparse
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
from _client import api_request, output_json


def main():
    parser = argparse.ArgumentParser(description="List Yuque repositories")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--user", default=None, help="User login (default: current user)")
    group.add_argument("--group", default=None, help="Group login")
    parser.add_argument("--offset", type=int, default=0, help="Offset for pagination")
    parser.add_argument("--limit", type=int, default=100, help="Number of repos to return")
    parser.add_argument("--type", default=None, choices=["Book", "Design", "Sheet", "Resource"],
                        help="Filter by repo type")
    args = parser.parse_args()

    params = {
        "offset": args.offset,
        "limit": args.limit,
        "type": args.type,
    }

    if args.group:
        path = f"/api/v2/groups/{args.group}/repos"
    elif args.user:
        path = f"/api/v2/users/{args.user}/repos"
    else:
        # Get current user login first
        user_info = api_request("GET", "/api/v2/user")
        login = user_info.get("data", {}).get("login")
        if not login:
            print("Error: Could not determine current user login.", file=sys.stderr)
            sys.exit(1)
        path = f"/api/v2/users/{login}/repos"

    result = api_request("GET", path, params=params)
    output_json(result)


if __name__ == "__main__":
    main()
