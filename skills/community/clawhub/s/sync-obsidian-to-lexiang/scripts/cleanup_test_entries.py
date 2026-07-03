#!/usr/bin/env python3
"""
cleanup_test_entries.py - 归拢乐享侧测试遗留目录，便于人工一键删除

背景：乐享 MCP 连接器没有「删除 entry」的工具（只能删 block / 移动 entry）。
因此脚本无法直接删除文件夹/文档；本工具把指定的测试目录集中移动到一个
「_待删除-测试遗留」文件夹下，用户在乐享界面只需删这一个文件夹即可清空全部。

⚠️ 重要：今后做端到端测试，请用 --target-folder-id 指向一个临时目录，
   或更好的做法是用本地临时 vault（见 SKILL.md「测试铁律」），从根上避免污染真实库。

用法：
  # 把指定名字的测试目录归拢到待删除文件夹
  python3 cleanup_test_entries.py \
      --space-id <SPACE_ID> --under <PARENT_FOLDER_ID> \
      --names _filetest _imgtest _tmp_xxx

  # 仅列出某目录下的子项（不移动）
  python3 cleanup_test_entries.py --under <PARENT_FOLDER_ID> --list
"""

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lexiang_api import LexiangConnector, LexiangError

# 常见测试目录名前缀（约定：测试目录一律以下划线开头）
DEFAULT_TEST_PREFIXES = ("_",)
TRASH_FOLDER_NAME = "_待删除-测试遗留"


def main():
    p = argparse.ArgumentParser(description="归拢乐享测试遗留目录")
    p.add_argument("--space-id", help="知识库 space_id（移动到新建待删除夹时需要）")
    p.add_argument("--under", required=True, help="父目录 entry_id（在其下查找/归拢）")
    p.add_argument("--names", nargs="*", default=None,
                   help="要归拢的目录名列表；不指定则按 _ 前缀自动识别")
    p.add_argument("--list", action="store_true", help="仅列出子项，不移动")
    args = p.parse_args()

    api = LexiangConnector()
    children = api.list_children(args.under, limit=100)

    if args.list:
        print(json.dumps(
            [{"name": c.get("name"), "type": c.get("entry_type"), "id": c.get("id")}
             for c in children], ensure_ascii=False, indent=2))
        return

    # 选出待归拢目录
    if args.names:
        targets = [c for c in children if c.get("name") in set(args.names)]
    else:
        targets = [c for c in children
                   if c.get("name", "").startswith(DEFAULT_TEST_PREFIXES)
                   and c.get("name") != TRASH_FOLDER_NAME]

    if not targets:
        print(json.dumps({"status": "noop", "message": "未发现需归拢的测试目录"},
                         ensure_ascii=False))
        return

    if not args.space_id:
        print(json.dumps({"error": "归拢需要 --space-id"}, ensure_ascii=False))
        sys.exit(1)

    # 复用已有的待删除夹（若存在），否则新建
    trash = next((c["id"] for c in children if c.get("name") == TRASH_FOLDER_NAME), None)
    if not trash:
        trash = api.create_folder(args.space_id, TRASH_FOLDER_NAME, args.under)

    moved, failed = [], []
    for c in targets:
        try:
            api.call_tool("entry_move_entry", {"entry_id": c["id"], "parent_id": trash})
            moved.append(c.get("name"))
        except LexiangError as e:
            failed.append({"name": c.get("name"), "error": str(e)[:120]})

    print(json.dumps({
        "status": "done",
        "trash_folder_id": trash,
        "trash_folder_name": TRASH_FOLDER_NAME,
        "moved": moved,
        "failed": failed,
        "note": "请在乐享界面手动删除「%s」文件夹以彻底清理（连接器无删除 entry 工具）"
                % TRASH_FOLDER_NAME,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
