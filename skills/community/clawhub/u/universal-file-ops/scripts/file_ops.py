#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
file_ops.py — 通用文件操作：拷贝、移动、重命名、删除

标准化 IO 接口（同 text_crud.py）：
  输入：CLI 参数 或 stdin JSON
  输出：stdout JSON

幂等性：
  - copy：目标存在且内容相同 → 跳过（幂等）
  - move：源不存在 → 报错
  - rename：同 move（rename 是 move 的特例）
  - delete：文件不存在 → 返回 success=true（幂等）
"""

import argparse
import json
import os
import shutil
import sys
from typing import Any, Dict, Optional

sys.path.insert(0, os.path.dirname(__file__))
from utils import (
    read_input,
    success_output,
    error_output,
    backup_file,
    log_operation,
    is_safe_path,
    file_content_eq,
    print_output,
)

# ── 核心逻辑 ───────────────────────────────────────────────────────────

def do_copy(src: str, dst: str, overwrite: bool = False,
            backup: bool = True) -> Dict[str, Any]:
    """拷贝文件或目录"""
    if not os.path.exists(src):
        raise FileNotFoundError(f"源不存在: {src}")
    if os.path.exists(dst):
        if not overwrite:
            if os.path.isfile(src) and file_content_eq(src, dst):
                return {"skipped": True, "reason": "内容相同（幂等）", "src": src, "dst": dst}
            raise FileExistsError(f"目标已存在（overwrite=false）: {dst}")
        if backup:
            backup_file(dst, operation="copy_overwrite")
    dst_dir = os.path.dirname(os.path.abspath(dst))
    if dst_dir:
        os.makedirs(dst_dir, exist_ok=True)
    if os.path.isdir(src):
        shutil.copytree(src, dst, dirs_exist_ok=overwrite)
    else:
        shutil.copy2(src, dst)
    return {"src": src, "dst": dst, "overwritten": os.path.exists(dst) and overwrite}


def do_move(src: str, dst: str, overwrite: bool = False,
            backup: bool = True) -> Dict[str, Any]:
    """移动（重命名）文件或目录"""
    if not os.path.exists(src):
        raise FileNotFoundError(f"源不存在: {src}")
    if os.path.exists(dst):
        if not overwrite:
            raise FileExistsError(f"目标已存在（overwrite=false）: {dst}")
        if backup:
            backup_file(dst, operation="move_overwrite")
    dst_dir = os.path.dirname(os.path.abspath(dst))
    if dst_dir:
        os.makedirs(dst_dir, exist_ok=True)
    os.replace(src, dst)   # atomic on same filesystem
    return {"src": src, "dst": dst, "overwritten": overwrite}


def do_rename(file_path: str, new_name: str, overwrite: bool = False,
              backup: bool = True) -> Dict[str, Any]:
    """重命名（封装 move）"""
    dir_name  = os.path.dirname(os.path.abspath(file_path))
    dst       = os.path.join(dir_name, new_name) if dir_name else new_name
    return do_move(file_path, dst, overwrite, backup)


def do_delete(file_path: str, backup: bool = True) -> Dict[str, Any]:
    """删除文件或目录（不存在则幂等返回 success）"""
    if not os.path.exists(file_path):
        return {"deleted": False, "skipped": True, "reason": "文件不存在（幂等）", "file": file_path}
    rollback_id = backup_file(file_path, operation="delete") if backup else None
    if os.path.isdir(file_path):
        shutil.rmtree(file_path)
    else:
        os.remove(file_path)
    return {"deleted": True, "file": file_path, "backup_file": rollback_id}


# ── 主分发 ───────────────────────────────────────────────────────────

def run(action: str, **kwargs) -> str:
    backup = kwargs.get("backup", True)
    try:
        if action == "copy":
            src  = kwargs.get("src")
            dst  = kwargs.get("dst")
            if not src or not dst:
                return error_output("copy 需要 src 和 dst 参数", None)
            if not is_safe_path(src) or not is_safe_path(dst):
                return error_output(f"路径不合法: {src} → {dst}", None)
            result = do_copy(src, dst, kwargs.get("overwrite", False), backup)

        elif action == "move":
            src = kwargs.get("src")
            dst = kwargs.get("dst")
            if not src or not dst:
                return error_output("move 需要 src 和 dst 参数", None)
            if not is_safe_path(src) or not is_safe_path(dst):
                return error_output(f"路径不合法: {src} → {dst}", None)
            result = do_move(src, dst, kwargs.get("overwrite", False), backup)

        elif action == "rename":
            file_path = kwargs.get("file")
            new_name  = kwargs.get("new_name")
            if not file_path or not new_name:
                return error_output("rename 需要 file 和 new_name 参数", None)
            if not is_safe_path(file_path):
                return error_output(f"路径不合法: {file_path}", None)
            result = do_rename(file_path, new_name, kwargs.get("overwrite", False), backup)

        elif action == "delete":
            file_path = kwargs.get("file")
            if not file_path:
                return error_output("delete 需要 file 参数", None)
            if not is_safe_path(file_path):
                return error_output(f"路径不合法: {file_path}", None)
            result = do_delete(file_path, backup)

        else:
            return error_output(f"不支持的 action: {action}", None)

        log_operation(action, kwargs.get("file") or kwargs.get("src") or "", True)
        rollback_id = result.get("backup_file", None)
        return success_output(action, kwargs.get("file") or kwargs.get("src") or "", result, rollback_id)

    except Exception as e:
        log_operation(action, kwargs.get("file") or kwargs.get("src") or "", False, detail=str(e))
        return error_output(str(e), kwargs.get("file") or kwargs.get("src") or None)


# ── CLI / JSON 入口 ───────────────────────────────────────────────────

def parse_args():
    p = argparse.ArgumentParser(description="通用文件操作：拷贝、移动、重命名、删除")
    p.add_argument("--action",    choices=["copy", "move", "rename", "delete"], help="操作类型")
    p.add_argument("--src",       help="源路径（copy/move）")
    p.add_argument("--dst",       help="目标路径（copy/move）")
    p.add_argument("--file",      help="目标文件（rename/delete）")
    p.add_argument("--new-name",   help="新文件名（rename）")
    p.add_argument("--overwrite", action="store_true", help="允许覆盖目标")
    p.add_argument("--no-backup", action="store_true", help="跳过备份（危险！）")
    p.add_argument("--input",     help="JSON 输入文件")
    return p.parse_args()


def main():
    args = parse_args()
    input_data = {}
    if args.input:
        with open(args.input, "r", encoding="utf-8") as f:
            input_data = json.load(f)
    else:
        stdin_data = read_input()
        if stdin_data:
            input_data = stdin_data

    if input_data:
        action = input_data.get("action")
        kwargs  = {k: v for k, v in input_data.items() if k != "action"}
    else:
        if not args.action:
            print_output(error_output("--action 为必填参数（或使用 JSON 输入）", None), is_error=True)
            sys.exit(1)
        action = args.action
        kwargs = {
            "src":       args.src,
            "dst":       args.dst,
            "file":      args.file,
            "new_name":  args.new_name,
            "overwrite": args.overwrite,
            "backup":    not args.no_backup,
        }

    result_json = run(action, **kwargs)
    print_output(result_json, is_error=('"success": false' in result_json.lower()))
    sys.exit(0 if '"success": true' in result_json.lower() else 1)


if __name__ == "__main__":
    main()
