#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
search.py — 语雀搜索。

* docs            走语雀官方 /search 接口,支持全文检索文档/知识库
* find-by-title   不走API,先 list-docs 拿全集再本地子串匹配,适合知道
                  关键字但官方搜索因索引滞后查不到的场景。
"""
from __future__ import annotations

import argparse
import json
import sys

from yuque_client import YuqueClient, YuqueError


def _print(data) -> None:
    json.dump(data, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")


def cmd_docs(args, client: YuqueClient):
    params = {"type": args.type}
    if args.scope:
        params["scope"] = args.scope
    if args.namespace:
        params["repo"] = args.namespace
    results = client.search(args.keyword, **params)
    _print([
        {"id": r.get("id"), "title": r.get("title"),
         "url": r.get("url"), "summary": r.get("summary"),
         "type": r.get("type"), "namespace": r.get("repo", {}).get("namespace")
         if isinstance(r.get("repo"), dict) else None}
        for r in results
    ])


def cmd_find_by_title(args, client: YuqueClient):
    docs = client.list_docs(args.namespace)
    needle = args.substring.lower()
    hits = [
        {"id": d.get("id"), "slug": d.get("slug"), "title": d.get("title")}
        for d in docs if needle in (d.get("title") or "").lower()
    ]
    _print(hits)


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="search.py", description="语雀搜索")
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("docs", help="官方全文搜索")
    s.add_argument("keyword")
    s.add_argument("--type", default="doc", choices=["doc", "book", "group", "user"])
    s.add_argument("--scope", choices=["user", "group", "repo"])
    s.add_argument("--namespace", help="搜索局限于某个知识库")
    s.set_defaults(func=cmd_docs)

    s = sub.add_parser("find-by-title", help="本地标题子串匹配")
    s.add_argument("namespace")
    s.add_argument("substring")
    s.set_defaults(func=cmd_find_by_title)

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
