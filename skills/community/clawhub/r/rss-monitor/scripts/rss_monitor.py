#!/usr/bin/env python3
"""
RSS Feed Monitor
Monitors RSS feeds and sends notifications for new articles
"""

import argparse
import hashlib
import json
import os
import sys
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse

# Try to import optional dependencies
try:
    import requests
    import feedparser
    HAS_DEPS = True
except ImportError:
    HAS_DEPS = False

# Data directory
DATA_DIR = Path.home() / ".rss_monitor"
FEEDS_FILE = DATA_DIR / "feeds.json"
HISTORY_FILE = DATA_DIR / "history.json"


def ensure_data_dir():
    """Ensure data directory exists"""
    DATA_DIR.mkdir(parents=True, exist_ok=True)


def load_json(filepath, default=None):
    """Load JSON file or return default"""
    if not filepath.exists():
        return default if default is not None else {}
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return default if default is not None else {}


def save_json(filepath, data):
    """Save data to JSON file"""
    ensure_data_dir()
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def get_feed_id(url):
    """Generate unique ID for feed URL"""
    return hashlib.md5(url.encode()).hexdigest()[:8]


def parse_feed(url):
    """Parse RSS/Atom feed and return entries"""
    if not HAS_DEPS:
        print("错误: 缺少依赖")
        print("请安装: pip install requests feedparser")
        return None
    
    try:
        feed = feedparser.parse(url)
        if feed.bozo:
            print(f"警告: 解析 feed 时出现问题: {feed.bozo_exception}")
        
        entries = []
        for entry in feed.entries[:10]:  # Get last 10 entries
            entry_data = {
                "title": entry.get("title", "无标题"),
                "link": entry.get("link", ""),
                "published": entry.get("published", entry.get("updated", "未知时间")),
                "summary": entry.get("summary", entry.get("description", ""))[:200],
                "feed_title": feed.feed.get("title", "未知源")
            }
            entries.append(entry_data)
        
        return {
            "title": feed.feed.get("title", "未知 Feed"),
            "link": feed.feed.get("link", ""),
            "entries": entries
        }
    except Exception as e:
        print(f"解析失败: {e}")
        return None


def send_feishu_notification(title, content, webhook_url=None):
    """Send notification to Feishu via webhook"""
    webhook = webhook_url or os.environ.get('FEISHU_WEBHOOK')
    
    if not webhook:
        print("警告: 未配置 Feishu Webhook，跳过通知")
        return False
    
    if not HAS_DEPS:
        print("错误: 缺少 requests 依赖")
        return False
    
    payload = {
        "msg_type": "post",
        "content": {
            "post": {
                "zh_cn": {
                    "title": title,
                    "content": [[{"tag": "text", "text": content[:3000]}]]
                }
            }
        }
    }
    
    try:
        response = requests.post(webhook, json=payload, timeout=10)
        result = response.json()
        if result.get('code') == 0:
            print("[OK] Feishu 通知已发送")
            return True
        else:
            print(f"[FAIL] Feishu 发送失败: {result}")
            return False
    except Exception as e:
        print(f"[FAIL] 发送异常: {e}")
        return False


def add_feed(url, name=None):
    """Add a feed to watchlist"""
    feeds = load_json(FEEDS_FILE, {})
    feed_id = get_feed_id(url)
    
    if feed_id in feeds:
        print(f"Feed 已在监控列表中")
        return
    
    # Validate feed
    print(f"正在验证 feed: {url}")
    feed_data = parse_feed(url)
    
    if not feed_data:
        print("[FAIL] 无法解析 feed，请检查 URL 是否正确")
        return
    
    feeds[feed_id] = {
        "url": url,
        "name": name or feed_data.get("title", f"Feed-{feed_id}"),
        "feed_title": feed_data.get("title", ""),
        "added_at": datetime.now().isoformat(),
        "last_check": None,
        "last_entry_id": None
    }
    
    save_json(FEEDS_FILE, feeds)
    print(f"[OK] 已添加: {feeds[feed_id]['name']}")
    print(f"  当前共有 {len(feed_data.get('entries', []))} 篇文章")


def remove_feed(name):
    """Remove a feed from watchlist"""
    feeds = load_json(FEEDS_FILE, {})
    
    for feed_id, feed in feeds.items():
        if feed.get('name') == name or feed.get('feed_title') == name:
            del feeds[feed_id]
            save_json(FEEDS_FILE, feeds)
            print(f"[OK] 已移除: {name}")
            return
    
    print(f"[FAIL] 未找到: {name}")


def list_feeds():
    """List all monitored feeds"""
    feeds = load_json(FEEDS_FILE, {})
    
    if not feeds:
        print("监控列表为空")
        return
    
    print(f"\n共 {len(feeds)} 个监控源:\n".encode('utf-8').decode('utf-8'))
    for feed_id, feed in feeds.items():
        name = feed.get('name', 'Unknown')
        url = feed.get('url', '')[:50]
        added = feed.get('added_at', 'Unknown')[:10]
        last_check = feed.get('last_check', '从未')[:16] if feed.get('last_check') else '从未'
        print(f"  - {name}")
        print(f"    URL: {url}...")
        print(f"    添加: {added}, 上次检查: {last_check}\n")


def check_feed(feed_id, feed, notify=True):
    """Check a single feed for updates"""
    url = feed.get('url')
    name = feed.get('name', 'Unknown')
    
    print(f"检查: {name}")
    
    feed_data = parse_feed(url)
    if not feed_data or not feed_data.get('entries'):
        print(f"  [FAIL] 无法获取内容")
        return []
    
    entries = feed_data['entries']
    last_entry_id = feed.get('last_entry_id')
    
    # Find new entries
    new_entries = []
    for entry in entries:
        entry_id = hashlib.md5(entry.get('link', '').encode()).hexdigest()[:12]
        
        if last_entry_id and entry_id == last_entry_id:
            break
        
        new_entries.append(entry)
    
    if new_entries:
        print(f"  [NEW] 发现 {len(new_entries)} 篇新文章")
        
        # Send notification
        if notify and len(new_entries) > 0:
            titles = [f"• {e.get('title', '无标题')}" for e in new_entries[:5]]
            notification_title = f"📰 {name} 有新文章"
            notification_content = f"发现 {len(new_entries)} 篇新文章:\n\n" + "\n".join(titles)
            
            if len(new_entries) > 5:
                notification_content += f"\n\n...还有 {len(new_entries) - 5} 篇"
            
            send_feishu_notification(notification_title, notification_content)
        
        # Save to history
        history = load_json(HISTORY_FILE, [])
        for entry in new_entries:
            entry['detected_at'] = datetime.now().isoformat()
            entry['feed_name'] = name
            history.append(entry)
        save_json(HISTORY_FILE, history[-500:])  # Keep last 500
        
        # Update last entry
        first_entry_id = hashlib.md5(entries[0].get('link', '').encode()).hexdigest()[:12]
        feed['last_entry_id'] = first_entry_id
    else:
        print(f"  [OK] 无更新")
    
    feed['last_check'] = datetime.now().isoformat()
    return new_entries


def check_all():
    """Check all feeds for updates"""
    feeds = load_json(FEEDS_FILE, {})
    
    if not feeds:
        print("监控列表为空，请先添加 feed")
        print("示例: scripts/rss_monitor.py add https://example.com/feed.xml")
        return
    
    print(f"开始检查 {len(feeds)} 个 feed...\n")
    
    total_new = 0
    for feed_id, feed in feeds.items():
        new_entries = check_feed(feed_id, feed)
        total_new += len(new_entries)
    
    # Save updated feeds
    save_json(FEEDS_FILE, feeds)
    
    print(f"\n检查完成，共发现 {total_new} 篇新文章")


def check_specific(name):
    """Check a specific feed"""
    feeds = load_json(FEEDS_FILE, {})
    
    for feed_id, feed in feeds.items():
        if feed.get('name') == name:
            check_feed(feed_id, feed)
            save_json(FEEDS_FILE, feeds)
            return
    
    print(f"未找到: {name}")


def show_history(limit=10):
    """Show recently detected articles"""
    history = load_json(HISTORY_FILE, [])
    
    if not history:
        print("暂无历史记录")
        return
    
    print(f"\n最近 {min(limit, len(history))} 条新文章:\n")
    for item in history[-limit:]:
        title = item.get('title', 'Unknown')[:40]
        feed = item.get('feed_name', 'Unknown')
        time = item.get('detected_at', 'Unknown')[:16]
        print(f"  [{time}] [{feed}] {title}...")


def main():
    parser = argparse.ArgumentParser(
        description='RSS Feed Monitor',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s add https://example.com/feed.xml --name "我的博客"
  %(prog)s list                    # Show all feeds
  %(prog)s check-all               # Check all feeds
  %(prog)s check "我的博客"         # Check specific feed
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # add command
    add_parser = subparsers.add_parser('add', help='Add RSS feed')
    add_parser.add_argument('url', help='Feed URL')
    add_parser.add_argument('--name', help='Friendly name for the feed')
    
    # remove command
    remove_parser = subparsers.add_parser('remove', help='Remove feed')
    remove_parser.add_argument('name', help='Feed name')
    
    # list command
    subparsers.add_parser('list', help='List all feeds')
    
    # check-all command
    subparsers.add_parser('check-all', help='Check all feeds')
    
    # check command
    check_parser = subparsers.add_parser('check', help='Check specific feed')
    check_parser.add_argument('name', help='Feed name')
    
    # history command
    history_parser = subparsers.add_parser('history', help='Show history')
    history_parser.add_argument('--limit', type=int, default=10)
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    # Execute command
    if args.command == 'add':
        add_feed(args.url, args.name)
    elif args.command == 'remove':
        remove_feed(args.name)
    elif args.command == 'list':
        list_feeds()
    elif args.command == 'check-all':
        check_all()
    elif args.command == 'check':
        check_specific(args.name)
    elif args.command == 'history':
        show_history(args.limit)


if __name__ == '__main__':
    main()
