#!/usr/bin/env python3
"""
检查是否有新邀请码并通知
每 2 分钟检查一次日志文件
"""

import os
import sys
import time
from datetime import datetime

LOG_FILE = "/tmp/wukong-monitor.log"
STATE_FILE = "/tmp/wukong-notify-state.json"
NOTIFY_FILE = "/tmp/wukong-new-code-notify.txt"

def load_state():
    """加载上次检查的行数"""
    try:
        with open(STATE_FILE, 'r') as f:
            import json
            return json.load(f)
    except:
        return {"last_line": 0, "last_notify": None}

def save_state(state):
    """保存状态"""
    import json
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f, indent=2)

def check_and_notify():
    """检查日志并通知"""
    if not os.path.exists(LOG_FILE):
        return
    
    state = load_state()
    last_line = state.get("last_line", 0)
    
    # 读取新日志
    with open(LOG_FILE, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # 检查新行
    new_lines = lines[last_line:]
    
    for line in new_lines:
        # 检测是否发现新邀请码
        if "发现新邀请码" in line or "版本变化" in line:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # 提取邀请码信息
            notify_msg = []
            notify_msg.append(f"🎉 **悟空邀请码更新通知**")
            notify_msg.append(f"━━━━━━━━━━━━━━━━━━━━")
            notify_msg.append(f"📅 时间：{timestamp}")
            
            # 读取后续几行获取详细信息
            for i, l in enumerate(new_lines):
                if "版本：" in l:
                    notify_msg.append(f"🔢 {l.strip()}")
                if "内容：" in l:
                    notify_msg.append(f"📝 {l.strip()}")
                if "路径：" in l:
                    notify_msg.append(f"💾 图片已保存")
            
            notify_msg.append(f"━━━━━━━━━━━━━━━━━━━━")
            notify_msg.append(f"💡 立即查看日志：tail -f /tmp/wukong-monitor.log")
            
            message = "\n".join(notify_msg)
            
            # 写入通知文件
            with open(NOTIFY_FILE, 'w', encoding='utf-8') as f:
                f.write(message)
            
            # 同时输出到 stdout（可被其他工具捕获）
            print(message)
            
            # 更新状态
            state["last_notify"] = timestamp
            save_state(state)
            
            return True
    
    # 更新行数
    state["last_line"] = len(lines)
    save_state(state)
    return False

if __name__ == "__main__":
    check_and_notify()
