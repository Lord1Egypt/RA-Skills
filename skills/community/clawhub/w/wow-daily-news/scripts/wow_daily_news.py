#!/usr/bin/env python3
"""
魔兽世界每日新闻推送 - 完整内容版
"""

import subprocess
import time
import re
import json
from datetime import datetime
from pathlib import Path

# 配置
IMG_DIR = Path.home() / ".openclaw" / "workspace" / "img"
IMG_DIR.mkdir(parents=True, exist_ok=True)


def run_cmd(cmd: str, timeout: int = 30) -> tuple[bool, str]:
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
        return result.returncode == 0, result.stdout + result.stderr
    except Exception as e:
        return False, str(e)


def close_browser():
    run_cmd('agent-browser close', 10)


def open_page(url: str) -> bool:
    run_cmd('agent-browser close', 10)
    time.sleep(1)
    success, _ = run_cmd(f'agent-browser open "{url}" --timeout 45000', 60)
    return success


def get_snapshot() -> str:
    success, output = run_cmd('agent-browser snapshot -c', 30)
    return output if success else ""


def is_today(date_str: str) -> bool:
    date_str = date_str.strip()
    today = datetime.now()
    
    try:
        parsed = datetime.strptime(date_str[:10], "%Y-%m-%d")
        return parsed.date() == today.date()
    except:
        pass
    
    try:
        parsed = datetime.strptime(date_str, "%B %d, %Y")
        return parsed.date() == today.date()
    except:
        pass
    
    return False


# ============ EXWIND 新闻详情获取 ============

def get_exwind_article_content(url: str) -> str:
    """打开文章详情页，获取完整内容"""
    print(f"    获取详情: {url}")
    
    if not open_page(url):
        return ""
    
    time.sleep(3)
    snapshot = get_snapshot()
    
    if not snapshot:
        return ""
    
    # 解析文章内容 - listitem 包含实际内容
    content_lines = []
    lines = snapshot.split('\n')
    
    for line in lines:
        line = line.strip()
        
        # listitem 包含具体内容
        if 'listitem:' in line:
            text = line.replace('listitem:', '').strip()
            if text and len(text) > 5:
                content_lines.append(text)
        
        # strong 标签可能是分类标题
        elif 'strong:' in line:
            text = line.replace('strong:', '').strip()
            if text and len(text) > 2:
                content_lines.append(f"\n**{text}**")
    
    close_browser()
    return '\n'.join(content_lines)


def fetch_exwind_news() -> list:
    """获取 EXWIND 新闻列表"""
    print("\n🔍 获取 EXWIND 新闻...")
    
    if not open_page("https://exwind.net/"):
        print("  打开页面失败")
        return []
    
    time.sleep(3)
    snapshot = get_snapshot()
    close_browser()
    
    if not snapshot:
        return []
    
    print(f"  快照: {len(snapshot)} 字符")
    
    articles = []
    current = {}
    
    for line in snapshot.split('\n'):
        line = line.strip()
        
        if line in ['- text: 蓝帖', '- text: 热修', '- text: 新闻']:
            if current.get('title') and current.get('url'):
                current['source'] = 'EXWIND'
                articles.append(current)
            current = {'type': line.replace('- text: ', '')}
        
        if '- heading "' in line and '[level=3]' in line and current.get('type'):
            match = re.search(r'heading "([^"]+)"', line)
            if match:
                current['title'] = match.group(1)
        
        if '/url: /post/' in line and current.get('title'):
            match = re.search(r'/url: (/\S+)', line)
            if match:
                current['url'] = f"https://exwind.net{match.group(1)}"
        
        if line.startswith('- paragraph:') and current.get('url') and not current.get('summary'):
            s = line.replace('- paragraph:', '').strip().strip('"')
            current['summary'] = s[:200] + '...' if len(s) > 200 else s
        
        if line.startswith('- text: schedule ') and current.get('url'):
            current['date'] = line.replace('- text: schedule ', '')
    
    if current.get('title') and current.get('url'):
        current['source'] = 'EXWIND'
        articles.append(current)
    
    print(f"  解析: {len(articles)} 条")
    return articles


def enrich_exwind_articles(articles: list, max_count: int = 4) -> list:
    """获取文章完整内容"""
    print("\n📖 获取文章详情...")
    
    enriched = []
    for i, article in enumerate(articles[:max_count]):
        print(f"  [{i+1}/{min(len(articles), max_count)}] {article['title'][:30]}...")
        
        content = get_exwind_article_content(article['url'])
        if content:
            article['content'] = content
        else:
            article['content'] = article.get('summary', '')
        
        enriched.append(article)
        time.sleep(2)
    
    return enriched


def filter_today(items: list) -> list:
    result = []
    for item in items:
        if is_today(item.get('date', '')):
            result.append(item)
        else:
            print(f"  跳过: {item['title'][:25]}... ({item.get('date', '')})")
    return result


def format_markdown(items: list) -> str:
    today = datetime.now().strftime('%Y年%m月%d日')
    
    lines = [f"# 🎮 魔兽世界今日新闻 ({today})", "", f"共 {len(items)} 条资讯", "", "---"]
    
    icons = {'蓝帖': '📘', '热修': '🔧', '新闻': '📰'}
    
    for i, n in enumerate(items):
        icon = icons.get(n.get('type', ''), '📄')
        lines.extend([
            "",
            f"## {icon} {n.get('type', '')}: {n['title']}",
            f"📅 {n.get('date', '')}",
            f"🔗 {n['url']}",
            "",
            n.get('content', n.get('summary', '')),
            "",
            "---"
        ])
    
    return '\n'.join(lines)


def main():
    print(f"[{datetime.now()}] 开始获取魔兽世界新闻...")
    print(f"[限制] 只获取 {datetime.now().strftime('%Y-%m-%d')} 发布的内容")
    
    # 获取 EXWIND 新闻
    exwind = fetch_exwind_news()
    
    # 筛选今日新闻
    all_news = []
    if exwind:
        print("\n筛选今日 EXWIND 新闻...")
        all_news.extend(filter_today(exwind))
    
    # 降级
    if not all_news:
        print("\n⚠️ 无今日新闻，取最近2条...")
        all_news.extend((exwind or [])[:2])
    
    all_news = all_news[:4]
    
    if not all_news:
        print("\n未获取到新闻")
        return
    
    # 获取完整内容
    all_news = enrich_exwind_articles(all_news)
    
    # 格式化
    markdown = format_markdown(all_news)
    print("\n" + markdown[:2000])  # 只打印前2000字符
    
    # 保存本地
    output_file = IMG_DIR / f"wow-news-{datetime.now().strftime('%Y%m%d')}.md"
    output_file.write_text(markdown, encoding='utf-8')
    print(f"\n✅ 已保存: {output_file}")
    
    # 输出 JSON
    today = datetime.now().strftime('%Y年%m月%d日')
    output = {
        "news": all_news,
        "markdown": markdown,
        "local_file": str(output_file),
        "doc_title": f"🎮 魔兽世界今日新闻 ({today})"
    }
    print("\n--- JSON OUTPUT (news count: {}) ---".format(len(all_news)))
    # 只输出 news 摘要
    for n in all_news:
        print(f"  - {n['title']}: {len(n.get('content', ''))} 字符")


if __name__ == '__main__':
    main()
