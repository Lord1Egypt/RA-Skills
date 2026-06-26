#!/usr/bin/env python3
"""Get document detail (including full body content).

Usage:
    python get_doc.py --repo 12345 --doc 67890
    python get_doc.py --doc 67890              # without repo (uses /api/v2/repos/docs/{id})
"""

import argparse
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
from _client import api_request, output_json


def main():
    parser = argparse.ArgumentParser(description="Get Yuque document detail")
    parser.add_argument("--repo", default=None, help="Repository (book) ID or namespace")
    parser.add_argument("--doc", required=True, help="Document ID or slug")
    args = parser.parse_args()

    if args.repo:
        path = f"/api/v2/repos/{args.repo}/docs/{args.doc}"
    else:
        path = f"/api/v2/repos/docs/{args.doc}"

    result = api_request("GET", path)
    output_json(result)


if __name__ == "__main__":
    main()
