#!/usr/bin/env python3
"""
监控通知文件，当有新邀请码时立即通知
"""

import os
import sys
import time
from datetime import datetime

NOTIFY_FILE = "/tmp/wukong-new-code-notify.txt"
WATCHED_FILE = "/tmp/wukong-watched-state.json"

def load_watched():
    """加载已查看的通知"""
    try:
        with open(WATCHED_FILE, 'r') as f:
            import json
            return json.load(f)
    except:
        return {"last_notify": None}

def save_watched(state):
    """保存状态"""
    import json
    with open(WATCHED_FILE, 'w') as f:
        json.dump(state, f, indent=2)

def watch_notify():
    """监控通知文件"""
    if not os.path.exists(NOTIFY_FILE):
        return False
    
    # 读取通知内容
    with open(NOTIFY_FILE, 'r', encoding='utf-8') as f:
        content = f.read()
    
    watched = load_watched()
    last_notify = watched.get("last_notify", "")
    
    # 如果和上次一样，不重复通知
    if content == last_notify:
        return False
    
    # 输出通知（会被调用者捕获）
    print(content)
    print(f"\n[监控时间] {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 标记为已查看
    watched["last_notify"] = content
    watched["last_check"] = datetime.now().isoformat()
    save_watched(watched)
    
    return True

if __name__ == "__main__":
    watch_notify()
