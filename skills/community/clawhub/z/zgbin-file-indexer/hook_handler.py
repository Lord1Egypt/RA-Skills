#!/usr/bin/env python3
"""
Hook 处理器 - 用于自动记录文件创建/修改/删除事件
配合 Claude hooks 使用，自动将文件事件记录到索引
"""

import json
import sys
import os
from indexer import FileIndexer

def handle_event(event_data: dict):
    """处理 hook 事件"""
    indexer = FileIndexer()

    # 解析事件数据
    try:
        data = json.loads(event_data) if isinstance(event_data, str) else event_data
    except json.JSONDecodeError:
        return

    # 提取文件路径信息
    tool_call = data.get('tool_call', {})
    tool_name = tool_call.get('name', '')

    # 处理 Write 工具
    if tool_name == 'Write':
        params = tool_call.get('arguments', {})
        file_path = params.get('file_path', '')
        if file_path:
            indexer.add_file(file_path)
            print(f"[HookHandler] Added/Updated: {file_path}")

    # 处理 Edit 工具
    elif tool_name == 'Edit':
        params = tool_call.get('arguments', {})
        file_path = params.get('file_path', '')
        if file_path:
            indexer.add_file(file_path)
            print(f"[HookHandler] Modified: {file_path}")

    # 处理 Bash 工具 - 检测 rm 命令
    elif tool_name == 'Bash':
        params = tool_call.get('arguments', {})
        command = params.get('command', '')
        if 'rm ' in command or 'unlink ' in command:
            # 尝试提取被删除的文件路径
            parts = command.split()
            for i, part in enumerate(parts):
                if part in ['rm', 'unlink'] and i + 1 < len(parts):
                    next_part = parts[i + 1]
                    if not next_part.startswith('-'):
                        indexer.mark_deleted(next_part)
                        print(f"[HookHandler] Deleted: {next_part}")


def main():
    """从 stdin 读取事件并处理"""
    for line in sys.stdin:
        line = line.strip()
        if line:
            try:
                handle_event(line)
            except Exception as e:
                print(f"[HookHandler] Error: {e}")


if __name__ == '__main__':
    main()
