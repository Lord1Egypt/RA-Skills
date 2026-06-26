#!/usr/bin/env python3
"""
心跳检查脚本 - 检查悟空邀请码通知
只在官方更新时间段检查，发现新内容时推送飞书通知
"""

import os
import sys
import json
from datetime import datetime

NOTIFY_FILE = "/tmp/wukong-new-code-notify.txt"
WATCHED_FILE = "/tmp/wukong-watched-state.json"

def is_official_time():
    """检查是否在官方更新时间段（9-12 点、14-18 点）"""
    hour = datetime.now().hour
    return hour in [9, 10, 11, 12, 14, 15, 16, 17, 18]

def load_watched():
    """加载已查看的通知"""
    try:
        with open(WATCHED_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return {"last_notify": "", "last_check": None}

def save_watched(state):
    """保存状态"""
    with open(WATCHED_FILE, 'w', encoding='utf-8') as f:
        json.dump(state, f, indent=2, ensure_ascii=False)

def check_and_notify():
    """检查通知并推送"""
    # 检查是否在官方时间
    if not is_official_time():
        print(f"[{datetime.now().strftime('%H:%M:%S')}] 非官方时间，跳过检查")
        return {"status": "skipped", "reason": "not_official_time"}
    
    # 检查通知文件
    if not os.path.exists(NOTIFY_FILE):
        print(f"[{datetime.now().strftime('%H:%M:%S')}] 通知文件不存在")
        return {"status": "no_notify_file"}
    
    # 读取通知内容
    with open(NOTIFY_FILE, 'r', encoding='utf-8') as f:
        content = f.read().strip()
    
    if not content:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] 通知文件为空")
        return {"status": "empty"}
    
    # 检查是否已查看
    watched = load_watched()
    last_notify = watched.get("last_notify", "")
    
    if content == last_notify:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] 无新通知")
        return {"status": "no_new"}
    
    # 发现新通知！
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] 🎉 发现新邀请码通知！")
    
    # 准备推送消息
    message = {
        "msg_type": "text",
        "content": {
            "text": content + f"\n\n[监控时间] {timestamp}"
        }
    }
    
    # 输出消息（由调用者处理推送）
    print("\n=== 推送消息 ===")
    print(json.dumps(message, ensure_ascii=False, indent=2))
    print("===============\n")
    
    # 更新状态
    watched["last_notify"] = content
    watched["last_check"] = timestamp
    watched["notified_at"] = timestamp
    save_watched(watched)
    
    return {
        "status": "notified",
        "timestamp": timestamp,
        "message": message
    }

if __name__ == "__main__":
    result = check_and_notify()
    sys.exit(0 if result.get("status") in ["notified", "no_new", "skipped"] else 1)
