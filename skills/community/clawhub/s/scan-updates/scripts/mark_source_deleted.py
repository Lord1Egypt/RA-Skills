from __future__ import annotations

import argparse
import json

import catalog
import gitea_api as g
from utils import json_fail, now_str


def out(data: dict) -> None:
    print(json.dumps(data, ensure_ascii=False))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--owner", required=True)
    parser.add_argument("--repo", required=True)
    parser.add_argument("--source_id", required=True)
    parser.add_argument("--source_path", required=True)
    args = parser.parse_args()

    cat = catalog.read(args.owner, args.repo)
    matched = None
    for doc in cat.get("documents", []):
        if doc.get("source_id") == args.source_id and doc.get("source_path") == args.source_path:
            doc["source_deleted"] = True
            doc["source_deleted_at"] = now_str()
            doc["updated_at"] = now_str()
            matched = doc
            break
    if not matched:
        out(json_fail("document_not_found", "catalog 中找不到对应源文件的知识页。"))
        return

    try:
        result = g.get_file(args.owner, args.repo, matched["file"])
        if result and "源文件已从资料源删除" not in result[0]:
            notice = f"> 注意：该资料对应的源文件 `{args.source_path}` 已从资料源删除（{now_str()}）。\n\n"
            g.put_file(args.owner, args.repo, matched["file"], notice + result[0], "paper-kb: mark source deleted", sha=result[1])
        catalog.write(args.owner, args.repo, cat)
        catalog.regen_index(args.owner, args.repo, args.repo, cat)
    except Exception as exc:
        out(json_fail("mark_deleted_failed", str(exc)))
        return

    out({"success": True, "document": matched})


if __name__ == "__main__":
    main()
