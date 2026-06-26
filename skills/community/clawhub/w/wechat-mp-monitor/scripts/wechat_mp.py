#!/usr/bin/env python3
"""
WeChat MP (微信公众号) Article Monitor
Monitors public accounts and sends notifications
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse, parse_qs

# Try to import optional dependencies
try:
    import requests
    from bs4 import BeautifulSoup
    HAS_DEPS = True
except ImportError:
    HAS_DEPS = False

# Data directory
DATA_DIR = Path.home() / ".wechat_mp_monitor"
WATCHLIST_FILE = DATA_DIR / "watchlist.json"
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


def extract_article_info(url):
    """
    Extract article title and content from WeChat MP URL
    Note: WeChat MP requires special handling due to anti-scraping
    """
    if not HAS_DEPS:
        return {
            "title": "无法获取标题 (缺少依赖)",
            "content": "请安装依赖: pip install requests beautifulsoup4",
            "url": url
        }
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.0'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract title
        title = soup.find('h1', class_='rich_media_title')
        title = title.get_text(strip=True) if title else "未知标题"
        
        # Extract content
        content_div = soup.find('div', id='js_content')
        if content_div:
            # Get text content
            content = content_div.get_text(separator='\n', strip=True)
            # Limit length
            content = content[:2000] + "..." if len(content) > 2000 else content
        else:
            content = "无法提取正文内容"
        
        return {
            "title": title,
            "content": content,
            "url": url,
            "fetched_at": datetime.now().isoformat()
        }
    except Exception as e:
        return {
            "title": f"获取失败: {str(e)}",
            "content": "",
            "url": url,
            "error": str(e)
        }


def summarize_article(url):
    """Fetch and summarize a WeChat article"""
    print(f"正在获取文章: {url}")
    info = extract_article_info(url)
    
    print(f"\n标题: {info.get('title', 'N/A')}")
    print(f"链接: {info.get('url', 'N/A')}")
    print(f"\n内容预览:\n{info.get('content', 'N/A')[:500]}...")
    
    return info


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
            print("✓ Feishu 通知已发送")
            return True
        else:
            print(f"✗ Feishu 发送失败: {result}")
            return False
    except Exception as e:
        print(f"✗ 发送异常: {e}")
        return False


def add_watch(account_name, feishu_webhook=None):
    """Add an account to watchlist"""
    watchlist = load_json(WATCHLIST_FILE, [])
    
    # Check if already exists
    for item in watchlist:
        if item.get('name') == account_name:
            print(f"账号 '{account_name}' 已在监控列表中")
            return
    
    watchlist.append({
        "name": account_name,
        "added_at": datetime.now().isoformat(),
        "feishu_webhook": feishu_webhook
    })
    
    save_json(WATCHLIST_FILE, watchlist)
    print(f"✓ 已添加监控: {account_name}")


def remove_watch(account_name):
    """Remove an account from watchlist"""
    watchlist = load_json(WATCHLIST_FILE, [])
    original_len = len(watchlist)
    watchlist = [w for w in watchlist if w.get('name') != account_name]
    
    if len(watchlist) < original_len:
        save_json(WATCHLIST_FILE, watchlist)
        print(f"✓ 已移除监控: {account_name}")
    else:
        print(f"账号 '{account_name}' 不在监控列表中")


def list_watches():
    """List all watched accounts"""
    watchlist = load_json(WATCHLIST_FILE, [])
    
    if not watchlist:
        print("监控列表为空")
        return
    
    print(f"\n共 {len(watchlist)} 个监控账号:\n")
    for item in watchlist:
        name = item.get('name', 'Unknown')
        added = item.get('added_at', 'Unknown')[:10]
        has_webhook = "✓" if item.get('feishu_webhook') else "✗"
        print(f"  • {name} (添加于 {added}, Feishu: {has_webhook})")


def check_all():
    """Check all watched accounts for updates"""
    watchlist = load_json(WATCHLIST_FILE, [])
    history = load_json(HISTORY_FILE, [])
    
    if not watchlist:
        print("监控列表为空，请先添加账号")
        return
    
    print(f"开始检查 {len(watchlist)} 个账号...")
    print("注意: 完整实现需要 RSS 源或搜索 API 支持")
    print("当前为演示版本，请手动提供文章 URL 进行测试\n")
    
    # Demo: just show status
    for item in watchlist:
        name = item.get('name')
        print(f"  • {name}: 待检查 (需要 RSS/API 源)")


def show_history(limit=10):
    """Show recently processed articles"""
    history = load_json(HISTORY_FILE, [])
    
    if not history:
        print("暂无历史记录")
        return
    
    print(f"\n最近 {min(limit, len(history))} 条记录:\n")
    for item in history[-limit:]:
        title = item.get('title', 'Unknown')[:40]
        url = item.get('url', 'N/A')[:50]
        time = item.get('fetched_at', 'Unknown')[:16]
        print(f"  [{time}] {title}...")
        print(f"           {url}...\n")


def main():
    parser = argparse.ArgumentParser(
        description='WeChat MP Article Monitor',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s summary <url>           # Summarize an article
  %(prog)s watch "账号名称"         # Add to watchlist
  %(prog)s list                    # Show watchlist
  %(prog)s check-all               # Check all accounts
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # summary command
    summary_parser = subparsers.add_parser('summary', help='Summarize an article')
    summary_parser.add_argument('url', help='Article URL')
    
    # watch command
    watch_parser = subparsers.add_parser('watch', help='Add account to watchlist')
    watch_parser.add_argument('name', help='Account name')
    watch_parser.add_argument('--feishu-webhook', help='Feishu webhook URL')
    
    # unwatch command
    unwatch_parser = subparsers.add_parser('unwatch', help='Remove from watchlist')
    unwatch_parser.add_argument('name', help='Account name')
    
    # list command
    subparsers.add_parser('list', help='List watched accounts')
    
    # check-all command
    subparsers.add_parser('check-all', help='Check all accounts')
    
    # history command
    history_parser = subparsers.add_parser('history', help='Show history')
    history_parser.add_argument('--limit', type=int, default=10, help='Number of entries')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    # Execute command
    if args.command == 'summary':
        info = summarize_article(args.url)
        # Save to history
        history = load_json(HISTORY_FILE, [])
        history.append(info)
        save_json(HISTORY_FILE, history[-100:])  # Keep last 100
        
    elif args.command == 'watch':
        add_watch(args.name, args.feishu_webhook)
        
    elif args.command == 'unwatch':
        remove_watch(args.name)
        
    elif args.command == 'list':
        list_watches()
        
    elif args.command == 'check-all':
        check_all()
        
    elif args.command == 'history':
        show_history(args.limit)


if __name__ == '__main__':
    main()
