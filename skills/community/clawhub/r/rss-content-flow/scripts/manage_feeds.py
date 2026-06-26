#!/usr/bin/env python3
"""
RSS 订阅管理：添加/删除/列出订阅源
用法:
  python3 manage_feeds.py --list
  python3 manage_feeds.py --add 36氪 https://36kr.com/feed
  python3 manage_feeds.py --remove 36氪
"""

import json
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE = os.path.join(SCRIPT_DIR, "config.json")

DEFAULT_FEEDS = {
    "36氪": "https://36kr.com/feed",
    "虎嗅": "https://www.huxiu.com/rss/0.xml",
    "少数派": "https://sspai.com/feed",
    "AI研习社": "https://ai.googleblog.com/feed/",
}

def load_feeds():
    """加载订阅配置"""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_feeds(feeds):
    """保存订阅配置"""
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(feeds, f, ensure_ascii=False, indent=2, sort_keys=True)
    print(f"✅ 已保存 {len(feeds)} 个订阅源")

def list_feeds():
    """列出所有订阅"""
    feeds = load_feeds()
    if not feeds:
        print("📭 暂无订阅源（使用 --add 添加）")
        print("\n默认推荐订阅：")
        for name, url in DEFAULT_FEEDS.items():
            print(f"  {name}: {url}")
        return
    
    print(f"📡 当前订阅（共 {len(feeds)} 个）：\n")
    for name, url in feeds.items():
        print(f"  • {name}")
        print(f"    {url}")
        print()

def add_feed(name, url):
    """添加订阅源"""
    if not name or not url:
        print("❌ 请提供名称和 URL：--add <名称> <URL>")
        sys.exit(1)
    
    feeds = load_feeds()
    
    if name in feeds:
        print(f"⚠️  已存在同名订阅源「{name}」，将覆盖原 URL")
    
    feeds[name] = url
    save_feeds(feeds)
    print(f"✅ 已添加/更新：{name}")
    print(f"   URL: {url}")

def remove_feed(name):
    """删除订阅源"""
    feeds = load_feeds()
    
    if name not in feeds:
        print(f"❌ 未找到订阅源「{name}」")
        available = list(feeds.keys())
        if available:
            print(f"   现有订阅：{', '.join(available)}")
        sys.exit(1)
    
    removed_url = feeds.pop(name)
    save_feeds(feeds)
    print(f"🗑️  已删除：{name}")
    print(f"   原URL: {removed_url}")

def init_default():
    """初始化默认订阅"""
    feeds = load_feeds()
    if not feeds:
        feeds = DEFAULT_FEEDS.copy()
        save_feeds(feeds)
        print("✅ 已初始化默认订阅源（36氪、虎嗅、少数派、AI研习社）")
    else:
        print(f"📡 已有 {len(feeds)} 个订阅源，跳过默认初始化")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="RSS 订阅管理")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--list", action="store_true", help="列出所有订阅")
    group.add_argument("--add", nargs=2, metavar=("名称", "URL"), help="添加订阅源")
    group.add_argument("--remove", metavar="名称", help="删除订阅源")
    group.add_argument("--init", action="store_true", help="初始化默认订阅源")
    args = parser.parse_args()
    
    if args.list:
        list_feeds()
    elif args.add:
        add_feed(args.add[0], args.add[1])
    elif args.remove:
        remove_feed(args.remove)
    elif args.init:
        init_default()
