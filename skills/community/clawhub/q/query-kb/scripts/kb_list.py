from __future__ import annotations

import argparse
import json

import catalog
import gitea_api as g


def out(data: dict) -> None:
    print(json.dumps(data, ensure_ascii=False))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--owner", required=True)
    parser.add_argument("--repo", required=True)
    parser.add_argument("--kind", default="all", choices=["all", "documents", "concepts", "resources", "people", "projects", "reviews", "imports"])
    parser.add_argument("--log_question", default="")
    args = parser.parse_args()

    cat = catalog.read(args.owner, args.repo)
    payload = {
        "success": True,
        "owner": args.owner,
        "repo": args.repo,
        "repo_url": f"{g.GITEA_URL}/{args.owner}/{args.repo}",
        "base_url": f"{g.GITEA_URL}/{args.owner}/{args.repo}/src/branch/main/",
    }
    if args.kind == "all":
        payload.update(cat)
    else:
        payload[args.kind] = cat.get(args.kind, [])
    out(payload)


if __name__ == "__main__":
    main()
