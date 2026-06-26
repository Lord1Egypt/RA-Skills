#!/usr/bin/env python3
"""
WeChat chat statistics and analysis.
"""
import json
import sys
import os
from datetime import datetime, timedelta
from collections import Counter, defaultdict

MESSAGE_DB = os.path.expanduser("~/.openclaw/data/wechat-messages.json")

def load_messages():
    if not os.path.exists(MESSAGE_DB):
        return []
    with open(MESSAGE_DB, 'r') as f:
        return json.load(f)

def chat_stats(chat_name=None):
    """Generate statistics for a specific or all chats."""
    msgs = load_messages()
    if not msgs:
        print("📭 没有消息数据")
        return
    
    if chat_name:
        msgs = [m for m in msgs if chat_name in m.get('chat_name', '')]
    
    total = len(msgs)
    users = Counter(m['sender'] for m in msgs)
    by_type = Counter(m.get('type', 'text') for m in msgs)
    by_hour = Counter(m.get('hour', 0) for m in msgs)
    by_day = Counter(m.get('day', '') for m in msgs)
    
    print(f"📊 聊天统计" + (f" ({chat_name})" if chat_name else ""))
    print(f"  总消息: {total}条")
    print(f"\n👥 发言排行:")
    for user, count in users.most_common(10):
        bar = '█' * min(int(count / max(1, max(users.values())) * 20), 20)
        print(f"  {user:12} {bar} {count}")
    
    print(f"\n📎 消息类型:")
    for t, count in by_type.most_common():
        print(f"  {t}: {count}条")
    
    # Active hours heat map
    print(f"\n🕐 活跃时段:")
    for h in range(24):
        count = by_hour.get(h, 0)
        bar = '▁▂▃▄▅▆▇█'[min(int(count / max(1, max(by_hour.values())) * 8), 7)]
        print(f"  {h:02d}:00 {bar} {count}")

def word_cloud(chat_name=None, limit=20):
    """Generate word frequency from messages."""
    msgs = load_messages()
    if chat_name:
        msgs = [m for m in msgs if chat_name in m.get('chat_name', '')]
    
    # Simple word frequency for Chinese
    import re
    words = []
    for m in msgs:
        content = m.get('content', '')
        # Extract Chinese words (2+ chars)
        words.extend(re.findall(r'[\u4e00-\u9fff]{2,}', content))
    
    freq = Counter(words).most_common(limit)
    
    print(f"☁️ 高频词" + (f" ({chat_name})" if chat_name else ""))
    for word, count in freq:
        if count < 3:
            break
        print(f"  {word}: {count}次")

def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else 'all'
    arg = sys.argv[2] if len(sys.argv) > 2 else None
    
    if cmd == 'words':
        word_cloud(arg)
    else:
        chat_stats(arg)

if __name__ == '__main__':
    main()
