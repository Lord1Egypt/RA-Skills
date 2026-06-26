#!/usr/bin/env python3
"""List documents in a Yuque repository.

Usage:
    python list_docs.py --repo 12345
    python list_docs.py --repo 12345 --offset 0 --limit 100
"""

import argparse
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
from _client import api_request, output_json


def main():
    parser = argparse.ArgumentParser(description="List documents in a Yuque repo")
    parser.add_argument("--repo", required=True, help="Repository (book) ID or namespace")
    parser.add_argument("--offset", type=int, default=0, help="Offset for pagination")
    parser.add_argument("--limit", type=int, default=100, help="Number of docs to return")
    args = parser.parse_args()

    params = {
        "offset": args.offset,
        "limit": args.limit,
    }

    result = api_request("GET", f"/api/v2/repos/{args.repo}/docs", params=params)
    output_json(result)


if __name__ == "__main__":
    main()
