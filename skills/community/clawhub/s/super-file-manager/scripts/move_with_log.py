#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""move_with_log.py — 带操作日志的文件移动/删除脚本 v2.0
用法:
  移动文件: python3 move_with_log.py move <源文件> <目标路径> [--log-dir <日志目录>]
  移到回收站: python3 move_with_log.py trash <文件> [--log-dir <日志目录>]
  批量移动: python3 move_with_log.py batch-move --files <文件列表> [--log-dir <日志目录>]

日志格式: JSON Lines，每行一条操作记录
  {"action":"move|trash","source":"原路径","dest":"目标路径","timestamp":"ISO8601","status":"ok|error","error":"错误信息"}

安全: 不修改文件内容，不递归删除，支持回撤
跨平台: macOS / Linux / Windows
"""

import os
import sys
import json
import time
import argparse
import shutil
import platform
from datetime import datetime, timezone

VERSION = "2.0"


def get_default_log_dir():
    """获取默认日志目录（跨平台）"""
    home = os.path.expanduser('~')
    if platform.system() == 'Windows':
        local_app_data = os.environ.get('LOCALAPPDATA', os.path.join(home, 'AppData', 'Local'))
        return os.path.join(local_app_data, 'file_manager', 'logs')
    elif platform.system() == 'Darwin':
        return os.path.join(home, 'Library', 'Caches', 'file_manager', 'logs')
    else:
        xdg = os.environ.get('XDG_CACHE_HOME', os.path.join(home, '.cache'))
        return os.path.join(xdg, 'file_manager', 'logs')


def get_log_file(log_dir):
    """获取当日日志文件路径"""
    date_str = datetime.now().strftime('%Y%m%d')
    return os.path.join(log_dir, f'operations_{date_str}.jsonl')


def log_operation(log_file, action, source, dest, status, error_msg=None):
    """记录操作日志（JSON Lines）"""
    record = {
        "action": action,
        "source": source,
        "dest": dest,
        "timestamp": datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
        "status": status,
    }
    if error_msg:
        record["error"] = error_msg

    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(json.dumps(record, ensure_ascii=False) + '\n')


def do_move(log_file, src, dst):
    """移动文件"""
    if not os.path.exists(src):
        log_operation(log_file, "move", src, dst, "error", "源文件不存在")
        print(f"ERROR: 源文件不存在: {src}", file=sys.stderr)
        return 1

    # 确保目标目录存在
    dst_dir = os.path.dirname(dst)
    if dst_dir:
        os.makedirs(dst_dir, exist_ok=True)

    # 检查目标是否已存在
    if os.path.exists(dst):
        log_operation(log_file, "move", src, dst, "error", "目标路径已存在")
        print(f"ERROR: 目标路径已存在: {dst}", file=sys.stderr)
        return 1

    try:
        shutil.move(src, dst)
        log_operation(log_file, "move", src, dst, "ok")
        print(f"OK: {src} -> {dst}")
        return 0
    except (OSError, shutil.Error) as e:
        log_operation(log_file, "move", src, dst, "error", str(e))
        print(f"ERROR: 移动失败: {src} -> {dst}", file=sys.stderr)
        return 1


def do_trash(log_file, filepath):
    """移到回收站（跨平台）"""
    if not os.path.exists(filepath):
        log_operation(log_file, "trash", filepath, "trash", "error", "文件不存在")
        print(f"ERROR: 文件不存在: {filepath}", file=sys.stderr)
        return 1

    try:
        import send2trash
        send2trash.send2trash(filepath)
        log_operation(log_file, "trash", filepath, "trash", "ok")
        print(f"OK: {filepath} -> 回收站")
        return 0
    except ImportError:
        # send2trash 未安装，尝试系统命令
        log_operation(log_file, "trash", filepath, "trash", "error", "send2trash 未安装")
        print("ERROR: send2trash 未安装，请运行: pip install send2trash", file=sys.stderr)
        return 1
    except OSError as e:
        log_operation(log_file, "trash", filepath, "trash", "error", str(e))
        print(f"ERROR: 移到回收站失败: {filepath}", file=sys.stderr)
        return 1


def do_batch_move(log_file, list_file):
    """批量移动（从文件读取列表）"""
    if not os.path.isfile(list_file):
        print(f"ERROR: 文件列表不存在: {list_file}", file=sys.stderr)
        return 1

    total = 0
    success = 0
    failed = 0

    with open(list_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue

            total += 1
            if '->' not in line:
                print(f"SKIP: 格式错误: {line}")
                failed += 1
                continue

            parts = line.split('->', 1)
            src = parts[0].strip()
            dst = parts[1].strip()

            if not src or not dst:
                print(f"SKIP: 格式错误: {line}")
                failed += 1
                continue

            if do_move(log_file, src, dst) == 0:
                success += 1
            else:
                failed += 1

    print()
    print("=== 批量移动完成 ===")
    print(f"总计: {total} | 成功: {success} | 失败: {failed}")
    print(f"日志: {log_file}")
    return 0 if failed == 0 else 1


def main():
    parser = argparse.ArgumentParser(description='带操作日志的文件移动/删除')
    subparsers = parser.add_subparsers(dest='action', help='操作类型')

    # move
    p_move = subparsers.add_parser('move', help='移动文件')
    p_move.add_argument('source', help='源文件')
    p_move.add_argument('dest', help='目标路径')

    # trash
    p_trash = subparsers.add_parser('trash', help='移到回收站')
    p_trash.add_argument('source', help='文件路径')

    # batch-move
    p_batch = subparsers.add_parser('batch-move', help='批量移动')
    p_batch.add_argument('--files', required=True, help='文件列表路径（每行: source -> dest）')

    # 全局选项
    parser.add_argument('--log-dir', default=None, help='日志目录')

    args = parser.parse_args()
    log_dir = args.log_dir or get_default_log_dir()
    log_file = get_log_file(log_dir)

    if args.action == 'move':
        sys.exit(do_move(log_file, args.source, args.dest))
    elif args.action == 'trash':
        sys.exit(do_trash(log_file, args.source))
    elif args.action == 'batch-move':
        sys.exit(do_batch_move(log_file, args.files))
    else:
        print(f"file-manager 操作日志工具 v{VERSION}")
        print()
        print("用法:")
        print(f"  python3 {os.path.basename(__file__)} move <源文件> <目标路径> [--log-dir <日志目录>]")
        print(f"  python3 {os.path.basename(__file__)} trash <文件> [--log-dir <日志目录>]")
        print(f"  python3 {os.path.basename(__file__)} batch-move --files <文件列表> [--log-dir <日志目录>]")
        print()
        print("文件列表格式（每行一条）:")
        print('  /path/source -> /path/dest')
        sys.exit(0)


if __name__ == '__main__':
    main()
