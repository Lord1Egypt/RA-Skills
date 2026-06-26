#!/usr/bin/env python3
"""
Extract structured info from WeChat messages.
"""
import json
import sys
import os
import re
from collections import defaultdict

MESSAGE_DB = os.path.expanduser("~/.openclaw/data/wechat-messages.json")

def load_messages():
    if not os.path.exists(MESSAGE_DB):
        return []
    with open(MESSAGE_DB, 'r') as f:
        return json.load(f)

def extract_links():
    """Extract all URLs from messages."""
    msgs = load_messages()
    url_pattern = r'https?://[^\s<>"]+'
    
    links = defaultdict(list)
    for m in msgs:
        urls = re.findall(url_pattern, m.get('content', ''))
        for u in urls:
            links[u].append({
                'chat': m.get('chat_name', '?'),
                'sender': m.get('sender', '?'),
                'time': m.get('time', '')
            })
    
    print(f"🔗 提取链接: {len(links)} 个")
    for url, refs in sorted(links.items(), key=lambda x: -len(x[1]))[:20]:
        print(f"\n  {url[:80]}")
        print(f"  来自 {len(refs)} 个对话")

def extract_todos():
    """Extract todo items from messages."""
    msgs = load_messages()
    todo_patterns = [
        r'(?:明天|今天|下周|记得|别忘了|提醒我)[^，。,.\n]{2,30}',
        r'TODO[：:]\s*(.+)',
        r'待办[：:]\s*(.+)',
    ]
    
    todos = []
    for m in msgs:
        content = m.get('content', '')
        for pattern in todo_patterns:
            matches = re.findall(pattern, content)
            for match in matches:
                todos.append({
                    'text': match.strip(),
                    'chat': m.get('chat_name', '?'),
                    'sender': m.get('sender', '?'),
                    'time': m.get('time', '')
                })
    
    print(f"📝 提取待办: {len(todos)} 条")
    for t in todos[:15]:
        print(f"  ☐ {t['text'][:60]}")
        print(f"    └─ {t['chat']} | {t['sender']}")

def extract_addresses():
    """Extract addresses from messages."""
    msgs = load_messages()
    addr_patterns = [
        r'(?:地址[：:是]?\s*)([\u4e00-\u9fff0-9a-zA-Z路街巷弄号栋幢单元楼室层\-\s]{6,60})',
        r'(?:定位[：:]\s*)([\u4e00-\u9fff\s]{4,40})',
    ]
    
    addrs = []
    for m in msgs:
        content = m.get('content', '')
        for pattern in addr_patterns:
            matches = re.findall(pattern, content)
            for match in matches:
                addrs.append({
                    'addr': match.strip(),
                    'chat': m.get('chat_name', '?'),
                    'sender': m.get('sender', '?'),
                    'time': m.get('time', '')
                })
    
    print(f"📍 提取地址: {len(addrs)} 条")
    for a in addrs[:10]:
        print(f"  📍 {a['addr'][:60]}")
        print(f"    └─ {a['chat']} | {a['sender']}")

def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else 'help'
    
    if cmd == 'links':
        extract_links()
    elif cmd == 'todos':
        extract_todos()
    elif cmd == 'addresses':
        extract_addresses()
    elif cmd == 'all':
        extract_links()
        print("\n" + "="*40 + "\n")
        extract_todos()
        print("\n" + "="*40 + "\n")
        extract_addresses()
    else:
        print("Usage: extract.py <links|todos|addresses|all>")

if __name__ == '__main__':
    main()
