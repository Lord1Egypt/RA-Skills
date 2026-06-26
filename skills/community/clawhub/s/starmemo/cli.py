#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
starmemo CLI - OpenClaw 命令行接口
用于保存、搜索、配置记忆
"""
import os
import sys
import json
import argparse
from datetime import datetime

# 添加技能目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from starmemo import StarMemoSkill, SkillConfig, LLM_PRESET

def cmd_save(args):
    """保存记忆"""
    skill = StarMemoSkill()
    content = args.content
    if not content:
        # 从 stdin 读取
        content = sys.stdin.read().strip()
    if not content:
        print("❌ 错误：未提供内容")
        return 1
    
    from starmemo import MessageCleaner
    content = MessageCleaner.clean(content)
    if content.startswith("记忆配置"):
        print("❌ 跳过配置指令")
        return 0
    
    core = skill.llm.optimize(content)
    skill.storage.save(content, core)
    print(f"✅ 已保存记忆")
    print(f"原文: {content[:100]}...")
    print(f"优化: {core}")
    return 0

def cmd_search(args):
    """搜索记忆"""
    skill = StarMemoSkill()
    keyword = args.keyword
    if not keyword:
        print("❌ 错误：未提供关键词")
        return 1
    
    result = skill.storage.search(keyword)
    if result:
        print(f"🔍 找到记忆:")
        print(result)
    else:
        print(f"❌ 未找到相关记忆: {keyword}")
    return 0

def cmd_config(args):
    """查看/设置配置"""
    config = SkillConfig()
    
    if args.show or not any([args.llm, args.key, args.ai is not None, args.web is not None, args.persist is not None]):
        # 显示配置
        print("=== starmemo 配置 ===")
        print(f"模型: {config.model_name}")
        print(f"端点: {config.base_url}")
        print(f"API Key: {config.api_key[:15]}..." if config.api_key else "未设置")
        print(f"AI优化: {'开启' if config.enable_ai else '关闭'}")
        print(f"持久化: {'开启' if config.persist_key else '关闭'}")
        print(f"联网搜索: {'开启' if config.allow_web_fetch else '关闭'}")
        return 0
    
    # 更新配置
    if args.llm and args.llm in LLM_PRESET:
        config.base_url = LLM_PRESET[args.llm]["url"]
        config.model_name = LLM_PRESET[args.llm]["model"]
        print(f"✅ 模型已切换: {args.llm}")
    
    if args.key:
        config.api_key = args.key
        print(f"✅ API Key 已设置")
    
    if args.ai is not None:
        config.enable_ai = args.ai.lower() == "true"
        print(f"✅ AI优化: {config.enable_ai}")
    
    if args.web is not None:
        config.allow_web_fetch = args.web.lower() == "true"
        print(f"✅ 联网搜索: {config.allow_web_fetch}")
    
    if args.persist is not None:
        config.persist_key = args.persist.lower() == "true"
        print(f"✅ 持久化: {config.persist_key}")
    
    config.save_config()
    print("✅ 配置已保存")
    return 0

def cmd_list(args):
    """列出记忆文件"""
    skill = StarMemoSkill()
    daily_dir = skill.storage.daily
    recent_dir = skill.storage.recent
    
    print("=== 记忆文件列表 ===")
    print("\n📅 热层 (当天):")
    if os.path.exists(daily_dir):
        for f in os.listdir(daily_dir):
            if f.endswith(".md"):
                path = os.path.join(daily_dir, f)
                size = os.path.getsize(path)
                print(f"  {f} ({size} bytes)")
    
    print("\n📦 温层 (近期):")
    if os.path.exists(recent_dir):
        for f in os.listdir(recent_dir):
            if f.endswith(".md"):
                path = os.path.join(recent_dir, f)
                size = os.path.getsize(path)
                print(f"  {f} ({size} bytes)")
    
    return 0

def cmd_show(args):
    """显示今日记忆"""
    skill = StarMemoSkill()
    today_file = skill.storage.today_file()
    if os.path.exists(today_file):
        with open(today_file, "r", encoding="utf-8") as f:
            content = f.read()
        print(f"=== 今日记忆 ({os.path.basename(today_file)}) ===")
        print(content)
    else:
        print("❌ 今日暂无记忆")
    return 0

def main():
    parser = argparse.ArgumentParser(description="starmemo CLI - 智能记忆管理")
    subparsers = parser.add_subparsers(dest="command", help="命令")
    
    # save 命令
    save_parser = subparsers.add_parser("save", help="保存记忆")
    save_parser.add_argument("content", nargs="?", help="要保存的内容")
    save_parser.set_defaults(func=cmd_save)
    
    # search 命令
    search_parser = subparsers.add_parser("search", help="搜索记忆")
    search_parser.add_argument("keyword", help="搜索关键词")
    search_parser.set_defaults(func=cmd_search)
    
    # config 命令
    config_parser = subparsers.add_parser("config", help="查看/设置配置")
    config_parser.add_argument("--show", action="store_true", help="显示当前配置")
    config_parser.add_argument("--llm", help="设置模型 (huoshan/tongyi/wenxin/deepseek/zhipu/xinghuo/hunyuan)")
    config_parser.add_argument("--key", help="设置 API Key")
    config_parser.add_argument("--ai", help="开启/关闭 AI 优化 (true/false)")
    config_parser.add_argument("--web", help="开启/关闭联网搜索 (true/false)")
    config_parser.add_argument("--persist", help="开启/关闭持久化 (true/false)")
    config_parser.set_defaults(func=cmd_config)
    
    # list 命令
    list_parser = subparsers.add_parser("list", help="列出记忆文件")
    list_parser.set_defaults(func=cmd_list)
    
    # show 命令
    show_parser = subparsers.add_parser("show", help="显示今日记忆")
    show_parser.set_defaults(func=cmd_show)
    
    args = parser.parse_args()
    
    if args.command is None:
        parser.print_help()
        return 0
    
    return args.func(args)

if __name__ == "__main__":
    sys.exit(main())
