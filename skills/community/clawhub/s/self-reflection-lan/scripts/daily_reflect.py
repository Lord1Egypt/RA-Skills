#!/usr/bin/env python3
"""
每日聊天记录生成脚本
- 在 ~/.openclaw/workspace/memory/ 下创建当日聊天记录文件
- 支持 --setup 设置每日执行时间，自动配置 launchd 定时任务
"""

import os
import sys
import datetime
import json
import re

MEMORY_DIR = os.path.expanduser("~/.openclaw/workspace/memory")
SKILL_DIR = os.path.expanduser("~/.openclaw/workspace/skills/self-reflection")
CONFIG_FILE = os.path.expanduser("~/.openclaw/workspace/reflections/schedule.json")
PLIST_FILE = os.path.expanduser("~/Library/LaunchAgents/com.openclaw.daily-reflect.plist")


def get_scheduled_time():
    """读取已保存的执行时间"""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE) as f:
            data = json.load(f)
        return data.get("hour", 23), data.get("minute", 0)
    return None, None


def save_scheduled_time(hour, minute):
    """保存执行时间"""
    os.makedirs(os.path.dirname(CONFIG_FILE), exist_ok=True)
    with open(CONFIG_FILE, "w") as f:
        json.dump({"hour": hour, "minute": minute}, f)


def remove_launchd():
    """删除已有的 launchd 定时任务"""
    if os.path.exists(PLIST_FILE):
        os.system(f"launchctl unload '{PLIST_FILE}' 2>/dev/null")
        os.remove(PLIST_FILE)
        print("已删除定时任务")


def create_launchd_plist(hour, minute):
    """创建 launchd plist 定时任务"""
    script_path = os.path.join(SKILL_DIR, "scripts", "daily_reflect.py")
    
    plist_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.openclaw.daily-reflect</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/python3</string>
        <string>{script_path}</string>
    </array>
    <key>StartCalendarInterval</key>
    <dict>
        <key>Hour</key>
        <integer>{hour}</integer>
        <key>Minute</key>
        <integer>{minute}</integer>
    </dict>
    <key>StandardOutPath</key>
    <string>/tmp/daily_reflect.log</string>
    <key>StandardErrorPath</key>
    <string>/tmp/daily_reflect.err</string>
    <key>RunAtLoad</key>
    <false/>
</dict>
</plist>
"""
    
    os.makedirs(os.path.dirname(PLIST_FILE), exist_ok=True)
    with open(PLIST_FILE, "w") as f:
        f.write(plist_content)
    
    result = os.system(f"launchctl load '{PLIST_FILE}' 2>/dev/null")
    if result == 0:
        print(f"✅ 定时任务已设置：每天 {hour:02d}:{minute:02d} 执行")
    else:
        print(f"⚠️ plist 已创建但 launchctl load 失败，请手动执行：launchctl load '{PLIST_FILE}'")


def setup_schedule():
    """引导用户设置执行时间"""
    print("\n📅 每日聊天记录定时任务设置")
    print("=" * 40)
    
    # 显示当前设置
    h, m = get_scheduled_time()
    if h is not None:
        print(f"当前设置：每天 {h:02d}:{m:02d} 执行")
        response = input("要修改吗？(y/n): ").strip().lower()
        if response != "y":
            print("保持不变")
            return
    
    # 输入时间
    while True:
        time_str = input("\n请输入执行时间（格式 HH:MM，例如 23:59 或 08:00）: ").strip()
        match = re.match(r"^(\d{1,2}):(\d{2})$", time_str)
        if not match:
            print("格式错误，请重新输入")
            continue
        hour = int(match.group(1))
        minute = int(match.group(2))
        if hour < 0 or hour > 23 or minute < 0 or minute > 59:
            print("时间超出范围，请重新输入")
            continue
        break
    
    # 确认并保存
    confirm = input(f"\n确认每天 {hour:02d}:{minute:02d} 执行？(y/n): ").strip().lower()
    if confirm != "y":
        print("已取消")
        return
    
    save_scheduled_time(hour, minute)
    remove_launchd()  # 先删旧的
    create_launchd_plist(hour, minute)


def show_status():
    """显示当前定时任务状态"""
    h, m = get_scheduled_time()
    if h is None:
        print("未设置定时任务。运行 python3 daily_reflect.py --setup 来设置")
    else:
        print(f"定时任务：每天 {h:02d}:{m:02d} 执行")
        if os.path.exists(PLIST_FILE):
            print("launchd 状态：已加载")
        else:
            print("launchd 状态：未安装（运行 --setup 重新安装）")


# ================== 原有功能 ==================

def ensure_memory_dir():
    os.makedirs(MEMORY_DIR, exist_ok=True)


def today_has_content():
    if not os.path.exists(f"{MEMORY_DIR}/{TODAY}.md"):
        return False
    with open(f"{MEMORY_DIR}/{TODAY}.md", encoding="utf-8") as f:
        content = f.read()
    return "今日主要话题" in content or len(content.strip()) > 100


def generate_template():
    return f"""## 今日主要话题

<!-- 记录今日与用户讨论的主要话题和结论 -->

## 技术笔记

<!-- 记录涉及的技术信息、命令、配置等 -->

## 待办事项

<!-- 用户交代的待办 -->

---
*由 system 自动生成*
"""


def create_daily_file():
    ensure_memory_dir()
    filepath = f"{MEMORY_DIR}/{TODAY}.md"
    
    if os.path.exists(filepath):
        if today_has_content():
            print(f"今日聊天记录已存在，跳过: {filepath}")
            return filepath
    
    template = f"""# 每日总结 - {TODAY}

{generate_template()}
"""
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(template)
    
    print(f"✅ 每日聊天记录已创建: {filepath}")
    return filepath


if __name__ == "__main__":
    TODAY = datetime.datetime.now().strftime("%Y-%m-%d")
    MEMORY_DIR = os.path.expanduser("~/.openclaw/workspace/memory")
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "--setup":
            setup_schedule()
        elif sys.argv[1] == "--status":
            show_status()
        elif sys.argv[1] == "--remove":
            remove_launchd()
            print("定时任务已删除")
        else:
            print("未知参数: --setup / --status / --remove")
    else:
        create_daily_file()
