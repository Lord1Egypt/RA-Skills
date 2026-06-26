#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
docs.py — 语雀文档与知识库的CRUD命令行入口。

所有子命令的输出统一为JSON,便于后续pipeline处理。

子命令:
    list-repos   列出某个用户/团队下的全部知识库
    list-docs    列出某知识库下全部文档(自动分页)
    get          读取一篇文档的Markdown正文
    create       新建文档
    update       更新文档(标题/正文/可见性等)
    delete       删除文档
    copy         跨知识库复制一篇文档
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from yuque_client import YuqueClient, YuqueError


def _print(data) -> None:
    json.dump(data, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")


def cmd_list_repos(args, client: YuqueClient):
    if args.group:
        repos = client.list_group_repos(args.group)
    else:
        login = args.user or client.whoami().get("login")
        if not login:
            raise YuqueError(0, "无法确定用户login,请用 --user 显式指定")
        repos = client.list_user_repos(login)
    _print([
        {"id": r.get("id"), "namespace": r.get("namespace"),
         "name": r.get("name"), "slug": r.get("slug"),
         "type": r.get("type"), "items_count": r.get("items_count")}
        for r in repos
    ])


def cmd_list_docs(args, client: YuqueClient):
    docs = client.list_docs(args.namespace)
    _print([
        {"id": d.get("id"), "slug": d.get("slug"), "title": d.get("title"),
         "public": d.get("public"), "updated_at": d.get("updated_at"),
         "word_count": d.get("word_count")}
        for d in docs
    ])


def cmd_get(args, client: YuqueClient):
    data = client.get_doc(args.namespace, args.slug, raw=True)
    if args.body_only:
        sys.stdout.write(data.get("body", "") + "\n")
    else:
        _print({
            "id": data.get("id"), "slug": data.get("slug"),
            "title": data.get("title"), "public": data.get("public"),
            "format": data.get("format"), "body": data.get("body"),
        })


def _read_body(path: str | None) -> str | None:
    if path is None:
        return None
    if path == "-":
        return sys.stdin.read()
    return Path(path).read_text(encoding="utf-8")


def cmd_create(args, client: YuqueClient):
    body_md = _read_body(args.body_file)
    payload = {"title": args.title, "format": "markdown", "body": body_md or ""}
    if args.slug:
        payload["slug"] = args.slug
    if args.public is not None:
        payload["public"] = args.public
    data = client.create_doc(args.namespace, **payload)
    web_base = client.base_url.replace("/api/v2", "").rstrip("/")
    _print({
        "id": data.get("id"), "slug": data.get("slug"),
        "title": data.get("title"),
        "url": f"{web_base}/{args.namespace}/{data.get('slug')}",
    })


def cmd_update(args, client: YuqueClient):
    # 先把slug换成doc_id(语雀update必须用整数id)
    target = args.slug_or_id
    if not target.isdigit():
        info = client.get_doc(args.namespace, target, raw=False)
        target_id = info.get("id")
        if not target_id:
            raise YuqueError(404, f"未找到文档 {target}")
    else:
        target_id = int(target)

    payload = {}
    if args.title is not None:
        payload["title"] = args.title
    if args.slug is not None:
        payload["slug"] = args.slug
    if args.body_file is not None:
        payload["body"] = _read_body(args.body_file)
    if args.public is not None:
        payload["public"] = args.public

    if not payload:
        raise YuqueError(0, "未提供任何要更新的字段")

    data = client.update_doc(args.namespace, target_id, **payload)
    web_base = client.base_url.replace("/api/v2", "").rstrip("/")
    _print({"id": data.get("id"), "slug": data.get("slug"),
            "title": data.get("title"),
            "url": f"{web_base}/{args.namespace}/{data.get('slug')}"})


def cmd_delete(args, client: YuqueClient):
    target = args.slug_or_id
    if not target.isdigit():
        info = client.get_doc(args.namespace, target, raw=False)
        target_id = info.get("id")
    else:
        target_id = int(target)
    data = client.delete_doc(args.namespace, target_id)
    _print({"deleted_id": target_id, "title": data.get("title")})


def cmd_copy(args, client: YuqueClient):
    src = client.get_doc(args.src_namespace, args.slug, raw=True)
    if not src:
        raise YuqueError(404, "源文档不存在")
    new_doc = client.create_doc(
        args.to,
        title=src.get("title"),
        slug=src.get("slug"),
        format="markdown",
        body=src.get("body", ""),
        public=src.get("public", 0),
    )
    _print({"src": f"{args.src_namespace}/{args.slug}",
            "dst": f"{args.to}/{new_doc.get('slug')}",
            "id": new_doc.get("id")})


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="docs.py", description="语雀文档CRUD")
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("list-repos", help="列出知识库")
    g = s.add_mutually_exclusive_group()
    g.add_argument("--user", help="用户login,缺省取当前token的用户")
    g.add_argument("--group", help="团队login")
    s.set_defaults(func=cmd_list_repos)

    s = sub.add_parser("list-docs", help="列出某知识库下全部文档")
    s.add_argument("namespace")
    s.set_defaults(func=cmd_list_docs)

    s = sub.add_parser("get", help="读取单篇文档")
    s.add_argument("namespace")
    s.add_argument("slug")
    s.add_argument("--body-only", action="store_true", help="只输出Markdown正文")
    s.set_defaults(func=cmd_get)

    s = sub.add_parser("create", help="新建文档")
    s.add_argument("namespace")
    s.add_argument("--title", required=True)
    s.add_argument("--slug")
    s.add_argument("--body-file", help="正文文件路径,'-'表示从stdin读")
    s.add_argument("--public", type=int, choices=[0, 1, 2],
                   help="0私密 1公开 2登录可见")
    s.set_defaults(func=cmd_create)

    s = sub.add_parser("update", help="更新文档")
    s.add_argument("namespace")
    s.add_argument("slug_or_id", help="文档slug或数字id")
    s.add_argument("--title")
    s.add_argument("--slug")
    s.add_argument("--body-file")
    s.add_argument("--public", type=int, choices=[0, 1, 2])
    s.set_defaults(func=cmd_update)

    s = sub.add_parser("delete", help="删除文档")
    s.add_argument("namespace")
    s.add_argument("slug_or_id")
    s.set_defaults(func=cmd_delete)

    s = sub.add_parser("copy", help="跨知识库复制文档")
    s.add_argument("src_namespace")
    s.add_argument("slug")
    s.add_argument("--to", required=True, help="目标 namespace")
    s.set_defaults(func=cmd_copy)

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
