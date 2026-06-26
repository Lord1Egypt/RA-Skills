#!/usr/bin/env python3
"""Search documents or repos on Yuque.

Usage:
    python search.py "keyword"
    python search.py "keyword" --type repo
    python search.py "keyword" --scope group_login/book_slug
    python search.py "keyword" --creator user_login
    python search.py "keyword" --page 2
"""

import argparse
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
from _client import api_request, output_json


def main():
    parser = argparse.ArgumentParser(description="Search Yuque documents or repos")
    parser.add_argument("query", help="Search keyword")
    parser.add_argument("--type", default="doc", choices=["doc", "repo"],
                        help="Search type: doc (default) or repo")
    parser.add_argument("--scope", default=None,
                        help="Search scope (e.g. group_login/book_slug)")
    parser.add_argument("--creator", default=None,
                        help="Filter by creator login")
    parser.add_argument("--page", type=int, default=1, help="Page number")
    args = parser.parse_args()

    params = {
        "q": args.query,
        "type": args.type,
        "scope": args.scope,
        "creator": args.creator,
        "page": args.page,
    }

    result = api_request("GET", "/api/v2/search", params=params)
    output_json(result)


if __name__ == "__main__":
    main()
