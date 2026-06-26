#!/usr/bin/env python3
"""Update the table of contents (TOC) of a Yuque repository.

Actions:
  appendNode  - Insert at end (sibling or child of target)
  prependNode - Insert at beginning (child of target only)
  editNode    - Edit an existing node
  removeNode  - Remove a node (sibling: current only, child: with children)

Usage:
    # Append a doc to the root TOC
    python update_toc.py --repo 12345 --action appendNode --action-mode child --doc-ids 111,222

    # Append a doc as sibling of a target node
    python update_toc.py --repo 12345 --action appendNode --action-mode sibling --target-uuid xxx --doc-ids 111

    # Add a title group
    python update_toc.py --repo 12345 --action appendNode --action-mode child --type TITLE --title "Section Name"

    # Remove a node
    python update_toc.py --repo 12345 --action removeNode --action-mode sibling --node-uuid xxx

    # Edit a node
    python update_toc.py --repo 12345 --action editNode --node-uuid xxx --title "New Name"
"""

import argparse
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
from _client import api_request, output_json


def main():
    parser = argparse.ArgumentParser(description="Update Yuque repo TOC")
    parser.add_argument("--repo", required=True, help="Repository (book) ID or namespace")
    parser.add_argument("--action", required=True,
                        choices=["appendNode", "prependNode", "editNode", "removeNode"],
                        help="TOC operation")
    parser.add_argument("--action-mode", required=True, choices=["sibling", "child"],
                        help="Operation mode: sibling or child")
    parser.add_argument("--target-uuid", default=None, help="Target node UUID (default: root)")
    parser.add_argument("--node-uuid", default=None, help="Node UUID (for edit/remove/move)")
    parser.add_argument("--doc-ids", default=None, help="Comma-separated doc IDs (for appendNode/prependNode)")
    parser.add_argument("--type", default="DOC", choices=["DOC", "LINK", "TITLE"],
                        help="Node type (default: DOC)")
    parser.add_argument("--title", default=None, help="Node title (for TITLE/LINK type or editNode)")
    parser.add_argument("--url", default=None, help="Node URL (for LINK type)")
    parser.add_argument("--visible", type=int, default=None, choices=[0, 1],
                        help="Visibility: 0=hidden, 1=visible")
    args = parser.parse_args()

    data = {
        "action": args.action,
        "action_mode": args.action_mode,
    }
    if args.target_uuid:
        data["target_uuid"] = args.target_uuid
    if args.node_uuid:
        data["node_uuid"] = args.node_uuid
    if args.doc_ids:
        data["doc_ids"] = [int(x.strip()) for x in args.doc_ids.split(",")]
    if args.type != "DOC":
        data["type"] = args.type
    if args.title:
        data["title"] = args.title
    if args.url:
        data["url"] = args.url
    if args.visible is not None:
        data["visible"] = args.visible

    result = api_request("PUT", f"/api/v2/repos/{args.repo}/toc", data=data)
    output_json(result)


if __name__ == "__main__":
    main()
