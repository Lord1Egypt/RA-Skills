#!/usr/bin/env python3
"""Update an existing Yuque document.

Usage:
    python update_doc.py --repo 12345 --doc 67890 --title "New Title"
    python update_doc.py --repo 12345 --doc 67890 --body-file /tmp/content.md
    python update_doc.py --repo 12345 --doc 67890 --title "New" --body "new content"
    echo "new body" | python update_doc.py --repo 12345 --doc 67890
"""

import argparse
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
from _client import api_request, output_json


def main():
    parser = argparse.ArgumentParser(description="Update a Yuque document")
    parser.add_argument("--repo", required=True, help="Repository (book) ID or namespace")
    parser.add_argument("--doc", required=True, help="Document ID or slug")
    parser.add_argument("--title", default=None, help="New document title")
    parser.add_argument("--body", default=None, help="New body content (markdown)")
    parser.add_argument("--body-file", default=None, help="Read body from file")
    parser.add_argument("--slug", default=None, help="New document slug/path")
    parser.add_argument("--format", default="markdown", choices=["markdown", "html", "lake"],
                        help="Content format (default: markdown)")
    parser.add_argument("--public", type=int, default=None, choices=[0, 1, 2],
                        help="Visibility: 0=private, 1=public, 2=org-public")
    args = parser.parse_args()

    # Resolve body: --body > --body-file > stdin
    body = args.body
    if body is None and args.body_file:
        with open(args.body_file, "r", encoding="utf-8") as f:
            body = f.read()
    if body is None and not sys.stdin.isatty():
        body = sys.stdin.read()

    data = {"format": args.format}
    if args.title:
        data["title"] = args.title
    if body is not None:
        data["body"] = body
    if args.slug:
        data["slug"] = args.slug
    if args.public is not None:
        data["public"] = args.public

    if len(data) <= 1:
        print("Error: Nothing to update. Provide --title, --body, --body-file, or pipe via stdin.",
              file=sys.stderr)
        sys.exit(1)

    result = api_request("PUT", f"/api/v2/repos/{args.repo}/docs/{args.doc}", data=data)
    output_json(result)


if __name__ == "__main__":
    main()
