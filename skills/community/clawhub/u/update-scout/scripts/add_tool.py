#!/usr/bin/env python3
"""
scout - add_tool.py
Adds a tool to the scout watchlist config.

Usage (agent-driven):
  python3 add_tool.py \
    --name "gogcli" \
    --repo "steipete/gogcli" \
    --detect-type command \
    --detect-cmd "gog --version" \
    --version-prefix "v" \
    --notes "Google Workspace CLI"
"""

import json
import os
import re
import shlex
import sys
import argparse

from scout_config import DEFAULT_WATCHLIST_PATH

DEFAULT_CONFIG_PATH = DEFAULT_WATCHLIST_PATH
REPO_PATTERN = re.compile(r'^[\w.\-]+/[\w.\-]+$')


def load_config(path):
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f)
    return []


def save_config(path, watchlist):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(watchlist, f, indent=2)


def main():
    parser = argparse.ArgumentParser(description="Add a tool to the scout watchlist")
    parser.add_argument("--name", required=True, help="Display name")
    parser.add_argument("--repo", required=True, help="GitHub org/repo")
    parser.add_argument("--detect-type", default="command",
                        choices=["command", "npm_global", "pip", "file"],
                        help="Version detection method")
    parser.add_argument("--detect-cmd", help="Command to run (for type=command), space-separated")
    parser.add_argument("--detect-package", help="Package name (for npm_global or pip)")
    parser.add_argument("--detect-file", help="Path to JSON file containing version (for type=file)")
    parser.add_argument("--detect-key", default="version", help="Key in JSON file (for type=file)")
    parser.add_argument("--version-prefix", default="v", help="Version prefix in GitHub tags (e.g. 'v')")
    parser.add_argument("--notes", default="", help="Optional description")
    parser.add_argument("--config", default=DEFAULT_CONFIG_PATH, help="Config file path")
    args = parser.parse_args()

    if not REPO_PATTERN.match(args.repo):
        print(f"⚠️  Invalid repo format: '{args.repo}' — expected 'owner/repo'")
        sys.exit(1)

    watchlist = load_config(args.config)

    if any(t["name"] == args.name for t in watchlist):
        print(f"Tool '{args.name}' already exists in watchlist.")
        sys.exit(1)

    if any(t.get("repo") == args.repo for t in watchlist):
        print(f"⚠️  Repo '{args.repo}' is already watched under a different name.")
        sys.exit(1)

    detect = {"type": args.detect_type}
    if args.detect_type == "command":
        if not args.detect_cmd:
            print("--detect-cmd required for type=command")
            sys.exit(1)
        detect["cmd"] = shlex.split(args.detect_cmd)  # handles paths with spaces
    elif args.detect_type in ("npm_global", "pip"):
        detect["package"] = args.detect_package or args.name
    elif args.detect_type == "file":
        if not args.detect_file:
            print("--detect-file required for type=file")
            sys.exit(1)
        detect["path"] = args.detect_file
        detect["key"] = args.detect_key

    tool = {
        "name": args.name,
        "repo": args.repo,
        "detect": detect,
        "version_prefix": args.version_prefix,
        "notes": args.notes,
    }

    watchlist.append(tool)
    save_config(args.config, watchlist)
    print(f"Added '{args.name}' ({args.repo}) to {args.config}")


if __name__ == "__main__":
    main()
