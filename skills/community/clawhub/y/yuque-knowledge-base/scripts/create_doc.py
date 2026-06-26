#!/usr/bin/env python3
"""Create a new document in a Yuque repository.

Usage:
    python create_doc.py --repo 12345 --title "My Doc" --body "# Hello"
    python create_doc.py --repo 12345 --title "My Doc" --body-file /tmp/content.md
    echo "# Hello" | python create_doc.py --repo 12345 --title "My Doc"
    python create_doc.py --repo 12345 --title "My Doc" --body "content" --public 1
    python create_doc.py --repo 12345 --title "My Doc" --body "content" --slug my-doc
"""

import argparse
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
from _client import api_request, output_json


def main():
    parser = argparse.ArgumentParser(description="Create a Yuque document")
    parser.add_argument("--repo", required=True, help="Repository (book) ID or namespace")
    parser.add_argument("--title", default="Untitled", help="Document title")
    parser.add_argument("--body", default=None, help="Document body content (markdown)")
    parser.add_argument("--body-file", default=None, help="Read body from file")
    parser.add_argument("--slug", default=None, help="Document slug/path")
    parser.add_argument("--format", default="markdown", choices=["markdown", "html", "lake"],
                        help="Content format (default: markdown)")
    parser.add_argument("--public", type=int, default=None, choices=[0, 1, 2],
                        help="Visibility: 0=private, 1=public, 2=org-public")
    args = parser.parse_args()

    # Resolve body content: --body > --body-file > stdin
    body = args.body
    if body is None and args.body_file:
        with open(args.body_file, "r", encoding="utf-8") as f:
            body = f.read()
    if body is None and not sys.stdin.isatty():
        body = sys.stdin.read()
    if body is None:
        print("Error: No body content provided. Use --body, --body-file, or pipe via stdin.", file=sys.stderr)
        sys.exit(1)

    data = {
        "title": args.title,
        "body": body,
        "format": args.format,
    }
    if args.slug:
        data["slug"] = args.slug
    if args.public is not None:
        data["public"] = args.public

    result = api_request("POST", f"/api/v2/repos/{args.repo}/docs", data=data)
    output_json(result)


if __name__ == "__main__":
    main()
