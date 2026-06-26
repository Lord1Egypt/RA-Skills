#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
toc.py — 语雀知识库目录(TOC)管理。

语雀TOC接口接受一个 action 对象,常见 action:
    appendNode      新增节点
    prependNode     插入到最前
    editNode        修改节点(标题、可见性等)
    removeNode      删除节点
    moveNode        移动节点

target_type:
    DOC             文档节点(必须配 target_uuid 已有节点 或 doc_ids 新增)
    TITLE           纯目录占位节点
    LINK            外链节点

子命令:
    show       树形展示当前TOC
    add-doc    把已有文档挂进目录
    add-title  添加纯目录占位
    move       移动节点(before/after/inside)
    rename     重命名节点
    remove     删除节点(可选保留底层文档)
    apply      读取一份本地JSON action列表,顺序提交
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

from yuque_client import YuqueClient, YuqueError


def _print(data) -> None:
    json.dump(data, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")


def _build_tree(toc: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """语雀TOC返回的是带 parent_uuid 的扁平列表,转成树。"""
    by_uuid: Dict[str, Dict[str, Any]] = {}
    for n in toc:
        node = {**n, "children": []}
        by_uuid[n["uuid"]] = node
    roots: List[Dict[str, Any]] = []
    for n in toc:
        node = by_uuid[n["uuid"]]
        parent = by_uuid.get(n.get("parent_uuid") or "")
        if parent:
            parent["children"].append(node)
        else:
            roots.append(node)
    return roots


def _format_tree(nodes: List[Dict[str, Any]], depth: int = 0) -> List[str]:
    lines = []
    for n in nodes:
        prefix = "  " * depth + ("📄" if n.get("type") == "DOC" else "📁")
        lines.append(f"{prefix} {n.get('title')}  [uuid={n.get('uuid')} type={n.get('type')}]")
        lines.extend(_format_tree(n.get("children", []), depth + 1))
    return lines


def cmd_show(args, client: YuqueClient):
    toc = client.get_toc(args.namespace)
    if args.flat:
        _print(toc)
        return
    tree = _build_tree(toc)
    if args.json:
        _print(tree)
    else:
        sys.stdout.write("\n".join(_format_tree(tree)) + "\n")


def cmd_add_doc(args, client: YuqueClient):
    body: Dict[str, Any] = {
        "action": "appendNode",
        "action_mode": "child" if args.parent_uuid else "sibling",
        "type": "DOC",
        "doc_ids": [int(args.doc_id)],
    }
    if args.parent_uuid:
        body["target_uuid"] = args.parent_uuid
    if args.title:
        body["title"] = args.title
    _print(client.update_toc(args.namespace, body))


def cmd_add_title(args, client: YuqueClient):
    body: Dict[str, Any] = {
        "action": "appendNode",
        "action_mode": "child" if args.parent_uuid else "sibling",
        "type": "TITLE",
        "title": args.title,
    }
    if args.parent_uuid:
        body["target_uuid"] = args.parent_uuid
    _print(client.update_toc(args.namespace, body))


def cmd_move(args, client: YuqueClient):
    mode_map = {"before": "prevSibling", "after": "nextSibling", "inside": "child"}
    body = {
        "action": "moveNode",
        "node_uuid": args.uuid,
        "target_uuid": args.target,
        "action_mode": mode_map[args.mode],
    }
    _print(client.update_toc(args.namespace, body))


def cmd_rename(args, client: YuqueClient):
    body = {"action": "editNode", "node_uuid": args.uuid, "title": args.title}
    _print(client.update_toc(args.namespace, body))


def cmd_remove(args, client: YuqueClient):
    body = {
        "action": "removeNode",
        "node_uuid": args.uuid,
        "delete_doc": not args.keep_doc,  # 默认连同文档一起删
    }
    _print(client.update_toc(args.namespace, body))


def cmd_apply(args, client: YuqueClient):
    """从一个本地JSON文件读取action列表,顺序提交。失败时停止并报告进度。"""
    actions = json.loads(Path(args.actions_file).read_text(encoding="utf-8"))
    if isinstance(actions, dict):
        actions = [actions]
    results = []
    for i, body in enumerate(actions):
        try:
            results.append({"index": i, "ok": True,
                            "data": client.update_toc(args.namespace, body)})
        except YuqueError as e:
            results.append({"index": i, "ok": False, "error": str(e),
                            "payload": e.payload})
            if args.stop_on_error:
                break
    _print(results)


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="toc.py", description="语雀目录(TOC)管理")
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("show", help="展示TOC")
    s.add_argument("namespace")
    s.add_argument("--json", action="store_true", help="输出JSON树")
    s.add_argument("--flat", action="store_true", help="输出语雀原始扁平结构")
    s.set_defaults(func=cmd_show)

    s = sub.add_parser("add-doc", help="把已有文档挂进TOC")
    s.add_argument("namespace")
    s.add_argument("--doc-id", required=True)
    s.add_argument("--parent-uuid", help="父节点uuid;不填则放根级")
    s.add_argument("--title", help="目录中显示的标题(可与文档标题不同)")
    s.set_defaults(func=cmd_add_doc)

    s = sub.add_parser("add-title", help="添加纯目录占位节点")
    s.add_argument("namespace")
    s.add_argument("--title", required=True)
    s.add_argument("--parent-uuid")
    s.set_defaults(func=cmd_add_title)

    s = sub.add_parser("move", help="移动节点")
    s.add_argument("namespace")
    s.add_argument("--uuid", required=True, help="要移动的节点")
    s.add_argument("--target", required=True, help="目标节点")
    s.add_argument("--mode", choices=["before", "after", "inside"], default="after")
    s.set_defaults(func=cmd_move)

    s = sub.add_parser("rename", help="重命名节点")
    s.add_argument("namespace")
    s.add_argument("--uuid", required=True)
    s.add_argument("--title", required=True)
    s.set_defaults(func=cmd_rename)

    s = sub.add_parser("remove", help="删除节点")
    s.add_argument("namespace")
    s.add_argument("--uuid", required=True)
    s.add_argument("--keep-doc", action="store_true",
                   help="只从目录移除,保留底层文档")
    s.set_defaults(func=cmd_remove)

    s = sub.add_parser("apply", help="批量提交action列表(JSON文件)")
    s.add_argument("namespace")
    s.add_argument("actions_file")
    s.add_argument("--stop-on-error", action="store_true")
    s.set_defaults(func=cmd_apply)

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
