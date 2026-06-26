#!/usr/bin/env python3
"""Delete a Yuque document.

Usage:
    python delete_doc.py --repo 12345 --doc 67890
"""

import argparse
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
from _client import api_request, output_json


def main():
    parser = argparse.ArgumentParser(description="Delete a Yuque document")
    parser.add_argument("--repo", required=True, help="Repository (book) ID or namespace")
    parser.add_argument("--doc", required=True, help="Document ID or slug")
    args = parser.parse_args()

    result = api_request("DELETE", f"/api/v2/repos/{args.repo}/docs/{args.doc}")
    output_json(result)


if __name__ == "__main__":
    main()
