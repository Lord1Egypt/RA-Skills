#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Remote Dispatch — 远程桌面执行器
将QQ消息中的远程指令转发到 computer-use 执行
支持：截图、搜索、剪贴板、窗口管理
"""
import sys
import io
import subprocess
import json
import os
from pathlib import Path
from datetime import datetime

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 指令映射
COMMANDS = [
    # 截图
    {'keys': ['截个屏', '截屏', '截图', '屏幕截图', 'screenshot', '桌面'], 'cmd': 'screenshot', 'desc': '全屏截图', 'return': 'image'},
    {'keys': ['看看', '看下', '看现在'], 'cmd': 'screenshot', 'desc': '看桌面', 'return': 'image'},

    # 搜索
    {'keys': ['搜索', '搜一下', '帮我搜', '百度搜', 'google搜'], 'cmd': 'search', 'desc': '搜索', 'return': 'image'},
    {'keys': ['查一下', '帮我查'], 'cmd': 'search', 'desc': '查询', 'return': 'image'},

    # 剪贴板
    {'keys': ['剪贴板', 'clipboard', '复制了什么'], 'cmd': 'clipboard_read', 'desc': '读取剪贴板', 'return': 'text'},
    {'keys': ['复制这个', '帮我复制'], 'cmd': 'clipboard_write', 'desc': '写入剪贴板', 'return': 'confirm'},

    # 窗口
    {'keys': ['打开', '启动'], 'cmd': 'open', 'desc': '打开', 'return': 'image'},
    {'keys': ['关闭窗口', '关掉'], 'cmd': 'close_window', 'desc': '关闭窗口', 'return': 'confirm'},
    {'keys': ['聚焦', '切换到'], 'cmd': 'focus_window', 'desc': '聚焦窗口', 'return': 'image'},
]


def parse_command(text):
    """解析用户消息中的远程指令"""
    text = text.strip()

    # 检查是否有 [远程] 标记
    is_remote = '[远程]' in text

    # 匹配指令
    for cmd_def in COMMANDS:
        for keyword in cmd_def['keys']:
            if keyword in text:
                # 提取参数（关键词后面的内容）
                parts = text.split(keyword, 1)
                args = parts[1].strip() if len(parts) > 1 else ''
                return {
                    'cmd': cmd_def['cmd'],
                    'desc': cmd_def['desc'],
                    'return': cmd_def['return'],
                    'keyword': keyword,
                    'args': args,
                }

    return None


def execute_screenshot():
    """执行截图"""
    output = f"/tmp/remote_screenshot_{datetime.now().strftime('%H%M%S')}.png"
    print(json.dumps({
        'action': 'screenshot',
        'command': f'python screenshot --output {output}',
        'output': output,
        'message': '📸 正在截图...',
    }, ensure_ascii=False))


def execute_search(query):
    """执行搜索"""
    print(json.dumps({
        'action': 'search',
        'steps': [
            {'cmd': 'open', 'target': 'https://www.baidu.com'},
            {'cmd': 'type', 'text': query},
            {'cmd': 'key', 'key': 'enter'},
        ],
        'message': f'🔍 正在搜索: {query}',
    }, ensure_ascii=False))


def execute_clipboard_read():
    """读取剪贴板"""
    print(json.dumps({
        'action': 'clipboard_read',
        'command': 'clipboard',
        'message': '📋 正在读取剪贴板...',
    }, ensure_ascii=False))


def execute_open(target):
    """打开文件/URL/应用"""
    print(json.dumps({
        'action': 'open',
        'target': target or '(默认)',
        'message': f'🚀 正在打开: {target or "默认"}',
    }, ensure_ascii=False))


def main():
    if len(sys.argv) < 2:
        print("Remote Dispatch — 远程桌面执行器")
        print()
        print("用法: python dispatch.py <消息文本>")
        print()
        print("示例:")
        print('  python dispatch.py "[远程] 帮我截个屏"')
        print('  python dispatch.py "搜索 端午节放假安排"')
        print('  python dispatch.py "看看我在干嘛"')
        print()
        print("指令列表:")
        for cmd, info in COMMANDS.items():
            print(f"  {cmd} → {info['desc']}")
        sys.exit(1)

    text = ' '.join(sys.argv[1:])
    parsed = parse_command(text)

    if not parsed:
        print(json.dumps({
            'error': True,
            'message': f'未识别到远程指令。可用的指令: {", ".join(COMMANDS.keys())}',
        }, ensure_ascii=False))
        sys.exit(1)

    cmd = parsed['cmd']
    args = parsed['args']

    if cmd == 'screenshot':
        execute_screenshot()
    elif cmd == 'search':
        execute_search(args or text)
    elif cmd == 'clipboard_read':
        execute_clipboard_read()
    elif cmd == 'open':
        execute_open(args)
    elif cmd == 'close_window':
        print(json.dumps({'action': 'close_window', 'message': '🪟 正在关闭窗口...'}))
    elif cmd == 'focus_window':
        print(json.dumps({'action': 'focus_window', 'target': args or '(未指定)',
                         'message': f'🎯 正在聚焦窗口: {args or "(未指定)"}'}))
    else:
        print(json.dumps({
            'error': True,
            'message': f'未实现的指令: {cmd}',
        }, ensure_ascii=False))


if __name__ == '__main__':
    main()
