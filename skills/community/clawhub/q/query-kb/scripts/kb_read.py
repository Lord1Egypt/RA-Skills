from __future__ import annotations

import argparse
import json

import gitea_api as g
from utils import json_fail


def out(data: dict) -> None:
    print(json.dumps(data, ensure_ascii=False))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--owner", required=True)
    parser.add_argument("--repo", required=True)
    parser.add_argument("--path", required=True)
    args = parser.parse_args()
    path = args.path.strip().strip("/")
    if not path.endswith(".md") and "." not in path.split("/")[-1]:
        path += ".md"
    result = g.get_file(args.owner, args.repo, path)
    if not result:
        out(json_fail("page_not_found", f"页面不存在：{path}"))
        return
    out({
        "success": True,
        "owner": args.owner,
        "repo": args.repo,
        "path": path,
        "content": result[0],
        "page_url": f"{g.GITEA_URL}/{args.owner}/{args.repo}/src/branch/main/{path}",
    })


if __name__ == "__main__":
    main()
