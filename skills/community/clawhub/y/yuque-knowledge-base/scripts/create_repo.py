#!/usr/bin/env python3
"""Create a new Yuque repository (knowledge base).

Usage:
    python create_repo.py --name "My Repo" --slug my-repo
    python create_repo.py --name "My Repo" --slug my-repo --description "A knowledge base"
    python create_repo.py --name "My Repo" --slug my-repo --group my-team
    python create_repo.py --name "My Repo" --slug my-repo --public 1
"""

import argparse
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
from _client import api_request, output_json


def main():
    parser = argparse.ArgumentParser(description="Create a Yuque repository")
    parser.add_argument("--name", required=True, help="Repository name")
    parser.add_argument("--slug", required=True, help="Repository slug/path")
    parser.add_argument("--description", default=None, help="Repository description")
    parser.add_argument("--group", default=None, help="Create under this group (login)")
    parser.add_argument("--user", default=None, help="Create under this user (login)")
    parser.add_argument("--public", type=int, default=0, choices=[0, 1, 2],
                        help="Visibility: 0=private (default), 1=public, 2=org-public")
    args = parser.parse_args()

    data = {
        "name": args.name,
        "slug": args.slug,
        "public": args.public,
    }
    if args.description:
        data["description"] = args.description

    if args.group:
        path = f"/api/v2/groups/{args.group}/repos"
    elif args.user:
        path = f"/api/v2/users/{args.user}/repos"
    else:
        user_info = api_request("GET", "/api/v2/user")
        login = user_info.get("data", {}).get("login")
        if not login:
            print("Error: Could not determine current user login.", file=sys.stderr)
            sys.exit(1)
        path = f"/api/v2/users/{login}/repos"

    result = api_request("POST", path, data=data)
    output_json(result)


if __name__ == "__main__":
    main()
