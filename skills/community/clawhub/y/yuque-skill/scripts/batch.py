#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
batch.py — 整本知识库的批量导入/导出/查找替换。

子命令:
    export    把某知识库下所有文档落到本地目录,文件名 = slug.md,
              首行注释保留 id/title/public 元信息便于回写。
    import    从本地目录批量同步:slug相同则更新,否则创建。
              使用 --create-only / --update-only 限定行为。
    replace   对整本知识库的Markdown正文做正则替换(默认dry-run)。
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Dict

from yuque_client import YuqueClient, YuqueError


META_HEADER = "<!-- yuque-skill: id={id} slug={slug} title={title} public={public} -->"
META_RE = re.compile(
    r"^<!-- yuque-skill: id=(?P<id>\d+) slug=(?P<slug>[^ ]+) title=(?P<title>.*?) public=(?P<public>\d+) -->\s*"
)


def _print(data) -> None:
    json.dump(data, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")


def _safe_filename(slug: str) -> str:
    return re.sub(r"[^A-Za-z0-9_\-\.]", "_", slug) + ".md"


def cmd_export(args, client: YuqueClient):
    out = Path(args.out_dir)
    out.mkdir(parents=True, exist_ok=True)
    docs = client.list_docs(args.namespace)
    written = []
    for meta in docs:
        full = client.get_doc(args.namespace, meta["slug"], raw=True)
        header = META_HEADER.format(
            id=full.get("id"), slug=full.get("slug"),
            title=(full.get("title") or "").replace("\n", " "),
            public=full.get("public", 0),
        )
        content = header + "\n\n" + (full.get("body") or "")
        path = out / _safe_filename(full["slug"])
        path.write_text(content, encoding="utf-8")
        written.append({"slug": full.get("slug"), "path": str(path),
                        "title": full.get("title")})
    _print({"namespace": args.namespace, "count": len(written), "files": written})


def _parse_local(path: Path) -> Dict[str, str]:
    text = path.read_text(encoding="utf-8")
    m = META_RE.match(text)
    info = {"slug": path.stem, "title": path.stem, "public": 0, "id": None}
    if m:
        info.update({
            "id": int(m.group("id")),
            "slug": m.group("slug"),
            "title": m.group("title"),
            "public": int(m.group("public")),
        })
        text = text[m.end():].lstrip("\n")
    info["body"] = text
    return info


def cmd_import(args, client: YuqueClient):
    src = Path(args.from_dir)
    if not src.is_dir():
        raise YuqueError(0, f"{src} 不是目录")
    existing = {d["slug"]: d for d in client.list_docs(args.to)}
    actions = []
    for md in sorted(src.glob("*.md")):
        info = _parse_local(md)
        if info["slug"] in existing and not args.create_only:
            doc_id = existing[info["slug"]]["id"]
            client.update_doc(args.to, doc_id,
                              title=info["title"], body=info["body"],
                              public=info["public"])
            actions.append({"file": md.name, "op": "update",
                            "slug": info["slug"], "id": doc_id})
        elif info["slug"] not in existing and not args.update_only:
            new = client.create_doc(args.to, title=info["title"],
                                    slug=info["slug"], format="markdown",
                                    body=info["body"], public=info["public"])
            actions.append({"file": md.name, "op": "create",
                            "slug": new.get("slug"), "id": new.get("id")})
        else:
            actions.append({"file": md.name, "op": "skip", "slug": info["slug"]})
    _print({"namespace": args.to, "count": len(actions), "actions": actions})


def cmd_replace(args, client: YuqueClient):
    pattern = re.compile(args.pattern, re.MULTILINE)
    docs = client.list_docs(args.namespace)
    changed = []
    for meta in docs:
        full = client.get_doc(args.namespace, meta["slug"], raw=True)
        body = full.get("body") or ""
        new_body, n = pattern.subn(args.replacement, body)
        if n == 0:
            continue
        record = {"slug": full.get("slug"), "title": full.get("title"),
                  "matches": n, "applied": False}
        if not args.dry_run:
            client.update_doc(args.namespace, full["id"], body=new_body)
            record["applied"] = True
        changed.append(record)
    _print({"namespace": args.namespace, "dry_run": args.dry_run,
            "changed_count": len(changed), "details": changed})


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="batch.py", description="语雀批量操作")
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("export", help="导出整个知识库为Markdown")
    s.add_argument("namespace")
    s.add_argument("--out-dir", required=True)
    s.set_defaults(func=cmd_export)

    s = sub.add_parser("import", help="把本地Markdown批量同步到知识库")
    s.add_argument("--from-dir", required=True)
    s.add_argument("--to", required=True, help="目标 namespace")
    g = s.add_mutually_exclusive_group()
    g.add_argument("--create-only", action="store_true", help="只创建,跳过已存在")
    g.add_argument("--update-only", action="store_true", help="只更新,跳过新文档")
    s.set_defaults(func=cmd_import)

    s = sub.add_parser("replace", help="正则查找替换整库正文")
    s.add_argument("namespace")
    s.add_argument("--pattern", required=True)
    s.add_argument("--replacement", required=True)
    s.add_argument("--dry-run", action="store_true",
                   help="只统计不写回,不加此参数将真实写入,强烈建议先 --dry-run 确认影响范围")
    s.set_defaults(func=cmd_replace)

    return p


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    try:
        client = YuqueClient()
        args.func(args, client)
        return 0
    except YuqueError as e:
        print(json.dumps({"error": str(e), "status": e.status, "payload": e.payload},
                         ensure_ascii=False, indent=2), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
