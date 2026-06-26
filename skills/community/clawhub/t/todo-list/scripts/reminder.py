#!/usr/bin/env python3
"""
待办事项提醒脚本，用于定时检查即将到期的任务并发送通知

依赖：
- Python 3
- OpenClaw CLI（用于发送提醒消息）
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from todo import check_due_tasks
import json

def send_reminder():
    """发送到期提醒
    
    输出提醒信息到标准输出，供 cron 或其他调度工具使用。
    实际的消息发送由 OpenClaw CLI 的 cron 功能处理。
    """
    due_tasks = check_due_tasks()
    
    if not due_tasks:
        return
    
    message = "⚠️  待办事项提醒\n"
    message += "=" * 30 + "\n"
    
    for task, reason in due_tasks:
        message += f"• [{task['id']}] {task['title']}\n"
        message += f"  {reason}\n"
        if task["description"]:
            message += f"  描述：{task['description']}\n"
        message += "\n"
    
    # 输出提醒信息，供 cron 调用时使用
    print(message)

if __name__ == "__main__":
    send_reminder()