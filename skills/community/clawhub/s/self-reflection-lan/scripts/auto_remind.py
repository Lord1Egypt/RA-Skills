#!/usr/bin/env python3
"""
auto_remind.py - 轻量自动触发提醒脚本
实现三个自动触发规则：
1. 命令执行失败提醒
2. 用户否定表述提醒
3. 每日 22:00 同步提醒
"""

import os
import sys
import json
import re
import datetime
import subprocess

REFLECTIONS_DIR = os.path.expanduser("~/.openclaw/workspace/reflections")
MEMORY_DIR = os.path.expanduser("~/.openclaw/workspace/memory")
CONFIG_FILE = os.path.expanduser("~/.openclaw/workspace/reflections/auto_remind_config.json")

# ==================== 配置 ====================

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE) as f:
            return json.load(f)
    return {"negation_keywords": ["不对", "错了", "不是这样", "No", "wrong", "not right", "actually"]}

def save_config(config):
    os.makedirs(os.path.dirname(CONFIG_FILE), exist_ok=True)
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, ensure_ascii=False, indent=2)

# ==================== 规则1：命令失败提醒 ====================

def check_command_failure():
    """检查最近日志中的命令失败，记录到 mistakes.md"""
    log_file = "/tmp/openclaw/openclaw-2026-04-03.log"  # 今天日期
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    log_file = f"/tmp/openclaw/openclaw-{today}.log"
    
    if not os.path.exists(log_file):
        return None
    
    # 查找最近的错误模式
    error_patterns = [
        r"error.*(?:timeout|ETIMEDOUT|ECONNREFUSED|ENOTFOUND)",
        r"Command exited with code [1-9]",
        r"Traceback.*\n.*Error",
        r"Exception.*\n.*",
    ]
    
    try:
        with open(log_file, encoding="utf-8", errors="ignore") as f:
            lines = f.readlines()
        
        recent_errors = []
        for i, line in enumerate(lines[-100:]):  # 只看最后100行
            for pattern in error_patterns:
                if re.search(pattern, line, re.IGNORECASE):
                    # 提取错误描述
                    context = lines[max(0, i-1):min(len(lines), i+3)]
                    error_text = "".join(context).strip()[:200]
                    if error_text not in recent_errors:
                        recent_errors.append(error_text)
                    break
        
        if not recent_errors:
            return None
        
        # 检查是否已记录过
        mistakes_file = os.path.join(REFLECTIONS_DIR, "mistakes.md")
        if os.path.exists(mistakes_file):
            with open(mistakes_file, encoding="utf-8") as f:
                content = f.read()
        else:
            content = ""
        
        new_entries = []
        today_str = datetime.datetime.now().strftime("%Y-%m-%d")
        for err in recent_errors[:3]:  # 最多记录3个
            # 简单去重：检查错误文本是否已在文件中
            short_err = err[:50]
            if short_err not in content and "命令执行失败" not in content:
                new_entries.append(err)
        
        if new_entries:
            return f"[规则1] 检测到最近命令失败，建议记录至 mistakes.md：\n\n" + "\n---\n".join(new_entries[:2])
        
        return None
        
    except Exception as e:
        return None

# ==================== 规则2：用户否定表述提醒 ====================

def check_negation_in_history():
    """检查最近消息中是否有否定表述"""
    # 这个规则需要读取飞书消息历史，但作为轻量提醒
    # 这里只输出提示文本，实际由AI自觉触发
    pass

# ==================== 规则3：每日 22:00 同步提醒 ====================

def check_daily_sync():
    """检查今日是否生成了聊天记录，如有则提醒记录复盘"""
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    memory_file = os.path.join(MEMORY_DIR, f"{today}.md")
    
    if not os.path.exists(memory_file):
        return None
    
    with open(memory_file, encoding="utf-8") as f:
        content = f.read()
    
    # 检查是否有实质内容（超过模板）
    template_markers = ["今日主要话题", "<!-- 记录"]
    has_real_content = any(marker in content for marker in template_markers if content.count(marker) > 1)
    
    if not has_real_content:
        return "今日聊天记录已生成，建议回顾是否有值得记录的：\n- 做得好的经验？\n- 犯过的错误？\n- 学到的新东西？"
    
    return None

# ==================== 主函数 ====================

def run_checks():
    """运行所有检查，返回需要提醒的内容"""
    reminders = []
    
    result1 = check_command_failure()
    if result1:
        reminders.append(("🔴 命令执行失败", result1))
    
    result3 = check_daily_sync()
    if result3:
        reminders.append(("📋 每日复盘提醒", result3))
    
    return reminders

def main():
    if len(sys.argv) > 1:
        if sys.argv[1] == "--check":
            # 仅运行检查，返回结果
            reminders = run_checks()
            if reminders:
                for title, body in reminders:
                    print(f"\n{title}:\n{body}")
            else:
                print("无自动触发提醒")
            return
        
        if sys.argv[1] == "--setup":
            # 初始化配置
            config = load_config()
            print("auto_remind 配置已加载")
            print(f"否定关键词: {config.get('negation_keywords', [])}")
            return
        
        if sys.argv[1] == "--help":
            print("用法:")
            print("  python3 auto_remind.py           # 运行所有检查")
            print("  python3 auto_remind.py --check     # 仅检查，不输出")
            print("  python3 auto_remind.py --setup     # 初始化配置")
            print("  python3 auto_remind.py --help      # 显示帮助")
            return
    
    # 默认：运行所有检查
    reminders = run_checks()
    
    if reminders:
        print(f"\n📬 auto_remind 检测到 {len(reminders)} 个提醒：\n")
        for title, body in reminders:
            print(f"\n{title}:\n{body}\n")
    else:
        print("无自动触发提醒")

if __name__ == "__main__":
    main()
