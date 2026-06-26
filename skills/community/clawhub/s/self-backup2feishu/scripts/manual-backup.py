#!/usr/bin/env python3
"""
手动/事件触发备份脚本
用于在特定事件发生时备份 AI 助手状态

用法：
    python3 manual-backup.py "备份原因"

示例：
    python3 manual-backup.py "掌握新技能：weather"
    python3 manual-backup.py "完成自动化任务：邮件监控"
    python3 manual-backup.py "添加重要联系人"
"""

import subprocess
import sys
import os
from datetime import datetime

# ============== 配置区域 ==============

CONFIG = {
    # 状态文件路径
    "files": {
        "memory": "MEMORY.md",
        "identity": "IDENTITY.md",
        "soul": "SOUL.md",
        "user": "USER.md",
    },
    
    # 工作目录
    "workspace": "/root/.openclaw/workspace",
    
    # 日志文件
    "log_file": "/root/.openclaw/logs/manual-backup.log",
}

# ======================================


def log(msg):
    """记录日志"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {msg}")
    try:
        os.makedirs(os.path.dirname(CONFIG["log_file"]), exist_ok=True)
        with open(CONFIG["log_file"], "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] {msg}\n")
    except:
        pass


def read_file(filename):
    """读取文件内容"""
    path = os.path.join(CONFIG["workspace"], filename)
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except:
        return ""


def backup(trigger_reason):
    """执行手动备份"""
    log(f"开始手动备份，触发原因：{trigger_reason}")
    
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # 读取核心文件
    memory = read_file(CONFIG["files"]["memory"])
    identity = read_file(CONFIG["files"]["identity"])
    
    # 生成备份摘要
    summary = f"""
# 备份摘要

- 时间：{now}
- 原因：{trigger_reason}
- 记忆长度：{len(memory)} 字符
- 身份：{identity.split('\\n')[0] if identity else '未知'}
"""
    
    # 标记待同步
    pending_file = os.path.join(CONFIG["workspace"], ".pending-feishu-backup")
    try:
        with open(pending_file, "w", encoding="utf-8") as f:
            f.write(f"{datetime.now().isoformat()}\n")
            f.write(f"触发原因：{trigger_reason}\n")
            f.write("NOTE: 更新飞书备份时，先读取现有内容，在原有基础上更新，不要直接覆盖\n")
        log("✓ 已标记待同步到飞书")
    except Exception as e:
        log(f"✗ 标记失败: {e}")
        return False
    
    log("✓ 手动备份成功")
    print(summary)
    return True


def main():
    if len(sys.argv) < 2:
        print("用法: python3 manual-backup.py \"备份原因\"")
        print("示例: python3 manual-backup.py \"掌握新技能\"")
        return False
    
    trigger = sys.argv[1]
    success = backup(trigger)
    return success


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
