#!/usr/bin/env python3
"""Get the table of contents (TOC) of a Yuque repository.

Usage:
    python get_toc.py --repo 12345
    python get_toc.py --repo group_login/book_slug
"""

import argparse
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
from _client import api_request, output_json


def main():
    parser = argparse.ArgumentParser(description="Get Yuque repo table of contents")
    parser.add_argument("--repo", required=True, help="Repository (book) ID or namespace (group/book)")
    args = parser.parse_args()

    result = api_request("GET", f"/api/v2/repos/{args.repo}/toc")
    output_json(result)


if __name__ == "__main__":
    main()
