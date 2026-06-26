#!/usr/bin/env python3
"""Get document version history.

Usage:
    python doc_versions.py --doc 12345                  # list versions
    python doc_versions.py --version 67890              # get version detail with diff
"""

import argparse
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
from _client import api_request, output_json


def main():
    parser = argparse.ArgumentParser(description="Get Yuque document versions")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--doc", default=None, help="Document ID (list all versions)")
    group.add_argument("--version", default=None, help="Version ID (get version detail)")
    args = parser.parse_args()

    if args.doc:
        result = api_request("GET", "/api/v2/doc_versions", params={"doc_id": args.doc})
    else:
        result = api_request("GET", f"/api/v2/doc_versions/{args.version}")

    output_json(result)


if __name__ == "__main__":
    main()
