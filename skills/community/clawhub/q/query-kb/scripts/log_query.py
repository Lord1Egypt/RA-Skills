from __future__ import annotations

import argparse
import json

import gitea_api as g
from utils import now_str


def out(data: dict) -> None:
    print(json.dumps(data, ensure_ascii=False))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--owner", required=True)
    parser.add_argument("--repo", required=True)
    parser.add_argument("--open_id", required=True)
    parser.add_argument("--question", required=True)
    parser.add_argument("--scope", default="")
    parser.add_argument("--hits", default="")
    args = parser.parse_args()

    entry = f"- `{now_str()}` **query** | user={args.open_id} scope={args.scope} | {args.question}"
    if args.hits:
        entry += f" | hits={args.hits}"
    entry += "\n"
    existing = g.get_file(args.owner, args.repo, "log.md")
    if existing:
        g.put_file(args.owner, args.repo, "log.md", existing[0] + entry, "paper-kb: log query", sha=existing[1])
    else:
        g.put_file(args.owner, args.repo, "log.md", "# Log\n\n" + entry, "paper-kb: init log")
    out({"success": True})


if __name__ == "__main__":
    main()
