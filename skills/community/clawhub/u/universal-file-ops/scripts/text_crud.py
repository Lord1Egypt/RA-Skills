#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
text_crud.py — 文本类文件增删查改（txt / py / html / md 等）

标准化 IO 接口：
  输入（两种模式）：
    A) CLI 参数模式：--action --file [--content] [--line]
    B) JSON 模式    ：echo '{"action":...}' | python text_crud.py
  输出（统一 JSON 到 stdout）：
    {"success":true,"action":"...","file":"...","result":{...},"error":null,"rollback_id":"..."}

幂等性：read 幂等；create 在 overwrite=false 时幂等（已存在则报错）；
          update/delete 在文件未变动时重复执行结果一致。
"""

import argparse
import json
import os
import sys
import shutil
from pathlib import Path
from typing import Any, Dict, Optional

# 复用同目录工具函数
sys.path.insert(0, os.path.dirname(__file__))
from utils import (
    read_input,
    success_output,
    error_output,
    backup_file,
    log_operation,
    ensure_data_dirs,
    is_safe_path,
    file_content_eq,
    atomic_write,
    print_output,
)

SUPPORTED_EXT = {".txt", ".py", ".html", ".md", ".csv", ".json", ".yaml", ".yml", ".xml", ".css", ".js", ".ts"}

# ─────────────────────────────────────────────────────────────────────────────
# 核心逻辑
# ─────────────────────────────────────────────────────────────────────────────

def do_read(file_path: str, encoding: str = "utf-8") -> Dict[str, Any]:
    """读取文本文件内容"""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"文件不存在: {file_path}")
    with open(file_path, "r", encoding=encoding, errors="replace") as f:
        content = f.read()
    stat = os.stat(file_path)
    return {
        "content": content,
        "encoding": encoding,
        "size": stat.st_size,
        "lines": content.count("\n") + 1 if content else 0,
    }


def do_create(
    file_path: str,
    content: str,
    encoding: str = "utf-8",
    overwrite: bool = False,
    backup: bool = True,
) -> Dict[str, Any]:
    """创建文本文件；overwrite=false 且文件存在则报错"""
    rollback_id = None
    if os.path.exists(file_path):
        if not overwrite:
            raise FileExistsError(f"文件已存在（overwrite=false）: {file_path}")
        if backup:
            rollback_id = backup_file(file_path, operation="create_overwrite")
    os.makedirs(os.path.dirname(os.path.abspath(file_path)), exist_ok=True)
    atomic_write(file_path, content, encoding)
    return {
        "content": content,
        "encoding": encoding,
        "size": len(content.encode(encoding)),
        "overwritten": os.path.exists(file_path) and overwrite,
        "backup_file": rollback_id,
    }


def do_update(
    file_path: str,
    content: str,
    encoding: str = "utf-8",
    mode: str = "replace",   # replace | append | insert
    line: Optional[int] = None,
    backup: bool = True,
) -> Dict[str, Any]:
    """更新文本文件（整文件替换 / 追加 / 插入到指定行）"""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"文件不存在: {file_path}")
    rollback_id = backup_file(file_path, operation="update") if backup else None

    if mode == "replace":
        atomic_write(file_path, content, encoding)
    elif mode == "append":
        atomic_write(file_path, content, encoding, mode="a")
    elif mode == "insert":
        if line is None:
            raise ValueError("mode=insert 时必须指定 --line")
        with open(file_path, "r", encoding=encoding) as f:
            lines = f.readlines()
        lines.insert(line, content if content.endswith("\n") else content + "\n")
        atomic_write(file_path, lines, encoding)
    else:
        raise ValueError(f"不支持的 mode: {mode}")
    return {
        "mode": mode,
        "line": line,
        "size": os.path.getsize(file_path),
        "backup_file": rollback_id,
    }


def do_delete(file_path: str, backup: bool = True) -> Dict[str, Any]:
    """删除文本文件（可选先备份）"""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"文件不存在: {file_path}")
    rollback_id = backup_file(file_path, operation="delete") if backup else None
    os.remove(file_path)
    return {
        "deleted": True,
        "backup_file": rollback_id,
    }


# ─────────────────────────────────────────────────────────────────────────────
# 主流程
# ─────────────────────────────────────────────────────────────────────────────

def run(action: str, file_path: str, **kwargs) -> str:
    """执行动作并返回标准化 JSON 字符串"""
    if not is_safe_path(file_path):
        return error_output(f"路径不合法（可能含遍历）: {file_path}", file_path)

    encoding = kwargs.get("encoding", "utf-8")
    backup  = kwargs.get("backup", True)

    try:
        if action == "read":
            result = do_read(file_path, encoding)
        elif action == "create":
            content = kwargs.get("content", "")
            overwrite = kwargs.get("overwrite", False)
            result = do_create(file_path, content, encoding, overwrite, backup)
        elif action == "update":
            content = kwargs.get("content", "")
            mode = kwargs.get("mode", "replace")
            line = kwargs.get("line", None)
            result = do_update(file_path, content, encoding, mode, line, backup)
        elif action == "delete":
            result = do_delete(file_path, backup)
        else:
            return error_output(f"不支持的 action: {action}", file_path)

        rollback_id = result.get("backup_file", None)
        log_operation(action, file_path, True, rollback_id)
        return success_output(action, file_path, result, rollback_id)

    except Exception as e:
        log_operation(action, file_path, False, detail=str(e))
        return error_output(str(e), file_path)


# ─────────────────────────────────────────────────────────────────────────────
# CLI / JSON 双模入口
# ─────────────────────────────────────────────────────────────────────────────

def parse_args():
    p = argparse.ArgumentParser(
        description="文本类文件增删查改（txt/py/html/md 等）"
    )
    p.add_argument("--action",   choices=["read", "create", "update", "delete"],
                    help="操作类型")
    p.add_argument("--file",      help="目标文件路径")
    p.add_argument("--content",   default="",        help="写入内容（create/update）")
    p.add_argument("--encoding",  default="utf-8",  help="文件编码（默认 utf-8）")
    p.add_argument("--mode",      default="replace",   choices=["replace", "append", "insert"],
                    help="update 模式")
    p.add_argument("--line",      type=int, default=None, help="insert 模式下的行号")
    p.add_argument("--overwrite", action="store_true", help="create 时允许覆盖")
    p.add_argument("--no-backup", action="store_true", help="跳过备份（危险！）")
    p.add_argument("--input",     help="JSON 输入文件（替代 stdin）")
    return p.parse_args()


def main():
    args = parse_args()

    # 尝试从 --input 或 stdin 读取 JSON
    input_data = {}
    if args.input:
        with open(args.input, "r", encoding="utf-8") as f:
            input_data = json.load(f)
    else:
        stdin_data = read_input()
        if stdin_data:
            input_data = stdin_data

    # JSON 模式：参数来自 JSON
    if input_data:
        action   = input_data.get("action")
        file_path = input_data.get("file")
        kwargs    = {k: v for k, v in input_data.items() if k not in ("action", "file")}
    else:
        # CLI 模式：参数来自 argparse
        if not args.action or not args.file:
            print_output(
                error_output("--action 和 --file 为必填参数（或使用 JSON 输入）", None),
                is_error=True,
            )
            sys.exit(1)
        action   = args.action
        file_path = args.file
        kwargs    = {
            "content":   args.content,
            "encoding":  args.encoding,
            "mode":      args.mode,
            "line":      args.line,
            "overwrite": args.overwrite,
            "backup":    not args.no_backup,
        }

    result_json = run(action, file_path, **kwargs)
    print_output(result_json, is_error=("\"success\": false" in result_json.lower()))
    sys.exit(0 if '"success": true' in result_json.lower() else 1)


if __name__ == "__main__":
    main()
