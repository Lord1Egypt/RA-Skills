#!/usr/bin/env python3
# todo-cleaner.py - 清理已完成的待办事项（Python 版本，完美支持时区）
#
# 用途：删除 status=completed 或 status=cancelled 且超过 24 小时的待办事项
# 用法：./scripts/todo-cleaner.py [--dry-run]

import json
import argparse
import sys
import os
import tempfile
from pathlib import Path
from datetime import datetime, timedelta

# 脚本位于 skills/todo-tracker/scripts/
# memory/todo.json 在 workspace/memory/
# 路径：scripts → todo-tracker → skills → workspace → memory
TODO_FILE = Path(__file__).resolve().parent.parent.parent.parent / "memory" / "todo.json"


def parse_iso8601(dt_str, local_tz):
    """解析 ISO8601 格式，并统一返回带时区的 datetime。"""
    dt = datetime.fromisoformat(dt_str)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=local_tz)
    return dt


def atomic_write_json(path, data):
    """原子写入 JSON，避免中途写坏状态文件。"""
    path = Path(path)
    with tempfile.NamedTemporaryFile(
        'w',
        encoding='utf-8',
        dir=path.parent,
        delete=False,
    ) as tmp:
        json.dump(data, tmp, ensure_ascii=False, indent=2)
        tmp.write('\n')
        tmp.flush()
        os.fsync(tmp.fileno())
        tmp_path = tmp.name
    os.replace(tmp_path, path)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dry-run', action='store_true', help='干跑模式，不实际删除')
    args = parser.parse_args()

    try:
        with open(TODO_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"❌ 错误：{TODO_FILE} 不存在")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"❌ 错误：JSON 格式错误：{e}")
        sys.exit(1)

    if 'items' not in data:
        data['items'] = []

    now = datetime.now().astimezone()
    local_tz = now.tzinfo
    cutoff = now - timedelta(hours=24)

    to_delete = []
    to_keep = []
    parse_errors = []

    for item in data['items']:
        status = item.get('status', 'pending')
        completed_at_str = item.get('completed_at')

        if status in ['completed', 'cancelled'] and completed_at_str:
            try:
                completed_at = parse_iso8601(completed_at_str, local_tz)
                if completed_at < cutoff:
                    to_delete.append(item)
                    continue
            except (ValueError, TypeError) as e:
                parse_errors.append({
                    'id': item.get('id', '<missing-id>'),
                    'completed_at': completed_at_str,
                    'error': str(e),
                })

        to_keep.append(item)

    print(f"\n📊 清理结果：")
    print(f"  总事项数：{len(data['items'])}")
    print(f"  已删除：{len(to_delete)}")
    print(f"  已保留：{len(to_keep)}")

    if parse_errors:
        print(f"  解析异常：{len(parse_errors)}")
        for err in parse_errors:
            print(
                f"  ⚠️  跳过 {err['id']} | completed_at={err['completed_at']} | {err['error']}"
            )

    if len(to_delete) > 0:
        if args.dry_run:
            print("\n⚠️  干跑模式：以下事项将被删除：")
            for item in to_delete:
                print(
                    f"  🗑️  {item.get('id', '<missing-id>')} - "
                    f"{item.get('description', '<missing-description>')}"
                )
                print(f"      完成时间：{item.get('completed_at', '<missing-completed_at>')}")
            print("\n⚠️  干跑模式：未实际删除")
        else:
            print("\n✅ 执行删除...")
            data['items'] = to_keep
            atomic_write_json(TODO_FILE, data)
            print("✅ 已完成清理")
    else:
        print("\n✨ 无需清理")

    sys.exit(0)

if __name__ == '__main__':
    main()
