#!/usr/bin/env python3
"""
WeChat message management utilities.
Works with the openclaw-weixin plugin data and local message cache.
"""
import json
import sys
import os
from datetime import datetime
from collections import Counter

MESSAGE_DB = os.path.expanduser("~/.openclaw/data/wechat-messages.json")

def load_messages():
    """Load cached WeChat messages."""
    if not os.path.exists(MESSAGE_DB):
        return []
    with open(MESSAGE_DB, 'r') as f:
        return json.load(f)

def unread_summary():
    """Show unread message summary."""
    msgs = load_messages()
    if not msgs:
        print("📭 没有缓存的消息数据")
        print("💡 请确保 openclaw-weixin 插件已启用并配置")
        return
    
    unread = [m for m in msgs if m.get('status') == 'unread']
    by_chat = Counter(m['chat_name'] for m in unread)
    
    print(f"📬 未读消息: {len(unread)}条 | 来自 {len(by_chat)} 个对话")
    print("🔝 未读最多:")
    for chat, count in by_chat.most_common(5):
        print(f"  • {chat}: {count}条")

def list_chats():
    """List recent chats."""
    msgs = load_messages()
    if not msgs:
        print("📭 没有缓存的消息数据")
        return
    
    chats = {}
    for m in msgs:
        name = m.get('chat_name', 'Unknown')
        if name not in chats:
            chats[name] = {'count': 0, 'last_msg': '', 'last_time': ''}
        chats[name]['count'] += 1
        if m.get('time', '') > chats[name]['last_time']:
            chats[name]['last_msg'] = m.get('content', '')[:50]
            chats[name]['last_time'] = m.get('time', '')
    
    # Sort by last message time
    sorted_chats = sorted(chats.items(), key=lambda x: x[1]['last_time'], reverse=True)
    
    print("💬 最近对话:")
    for name, info in sorted_chats[:10]:
        print(f"  • {name} ({info['count']}条) | {info['last_msg']}")

def search_messages(query):
    """Search messages by keyword."""
    msgs = load_messages()
    query_lower = query.lower()
    
    results = [m for m in msgs if query_lower in m.get('content', '').lower()]
    
    print(f"🔍 搜索 '{query}': {len(results)} 条结果")
    for m in results[:10]:
        print(f"  [{m.get('chat_name', '?')}] {m.get('sender', '?')}: {m.get('content', '')[:80]}")

def main():
    if len(sys.argv) < 2:
        print("Usage: msg.py <command> [args]")
        print("Commands: unread, chats, search <query>")
        return
    
    cmd = sys.argv[1]
    
    if cmd == 'unread':
        unread_summary()
    elif cmd == 'chats':
        list_chats()
    elif cmd == 'search' and len(sys.argv) > 2:
        search_messages(' '.join(sys.argv[2:]))
    else:
        print(f"Unknown command: {cmd}")

if __name__ == '__main__':
    main()
