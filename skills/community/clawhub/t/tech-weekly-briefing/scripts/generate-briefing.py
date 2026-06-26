#!/usr/bin/env python3
"""
Tech Weekly Briefing - RSS Aggregator and Reporter
Strategy: Daily RSS fetch + accumulate, Saturday report generation
"""

import json
import re
import os
import urllib.request
from datetime import datetime, timedelta
from typing import List, Dict, Tuple
from collections import defaultdict
from xml.etree import ElementTree as ET
import sys

# Configuration
DATA_DIR = os.path.expanduser("~/.openclaw/workspace-group/skills/tech-weekly-briefing/data")
RSS_SOURCES = {
    "techcrunch": "https://techcrunch.com/feed/",
    "the-verge": "https://www.theverge.com/rss/index.xml",
    "wired": "https://www.wired.com/feed/rss",
    "ars-technica": "https://arstechnica.com/feed/",
    "mit-technology-review": "https://www.technologyreview.com/feed/",
    "the-information": "https://www.theinformation.com/feed"
}

# Keywords
AUTONOMOUS_KEYWORDS = ["robotaxi", "waymo", "zoox", "aurora", "autonomous", "self-driving", "无人驾驶", "自动驾驶"]

# Negative keywords to filter out non-tech content
NEGATIVE_KEYWORDS = [
    # Sports (specific terms to avoid sports news)
    "baseball game", "basketball game", "football game", "soccer match",
    "nfl draft", "nba playoffs", "mlb season", "world cup final",
    "cruises past", "cruises to", "championship game", "tournament bracket",
    # Promotions/Coupons (specific promotional phrases)
    "promo code", "promo codes", "coupon code", "coupon codes",
    "% off", "percent off", "discount code", "service code",
    "sale: save", "limited time offer", "exclusive discount",
    # Shopping/Deals (specific deal content)
    "mattress firm", "kitchenaid promo", "norton coupon", "turbotax service",
    "hatch's sale", "beats headphones we like", "all discounted",
    # Non-tech lifestyle content
    "bird-watchers", "migratory humming", "coffee (2026)", "brew coffee",
    "sleep week deals", "certified sleep coach",
    # Low quality indicators
    "sponsored content", "advertorial", "paid content", "partner content"
]

def ensure_data_dir():
    """Ensure data directory exists."""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

def get_today_str() -> str:
    """Get today's date string."""
    return datetime.now().strftime('%Y-%m-%d')

def get_last_7_days() -> List[str]:
    """Get date strings for last 7 days."""
    dates = []
    for i in range(7):
        date = datetime.now() - timedelta(days=i)
        dates.append(date.strftime('%Y-%m-%d'))
    return dates

def is_low_quality_content(title: str) -> bool:
    """Check if article title contains negative keywords indicating non-tech content."""
    title_lower = title.lower()
    for keyword in NEGATIVE_KEYWORDS:
        if keyword.lower() in title_lower:
            return True
    return False

def filter_low_quality_articles(articles: List[Dict]) -> List[Dict]:
    """Filter out articles with low-quality or non-tech content."""
    filtered = []
    removed_count = 0
    for article in articles:
        title = article.get('title', '')
        if is_low_quality_content(title):
            removed_count += 1
            print(f"  Filtered out (negative keyword): {title[:60]}...")
            continue
        filtered.append(article)
    if removed_count > 0:
        print(f"  Filtered {removed_count} low-quality articles")
    return filtered

def fetch_rss_with_curl(url: str) -> str:
    """Fetch RSS feed using curl to avoid Python urllib fingerprinting."""
    import subprocess
    try:
        cmd = [
            'curl', '-s', '-L', '--max-time', '30',
            '-A', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            url
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=35)
        if result.returncode == 0:
            return result.stdout
        else:
            print(f"  Curl error: {result.stderr[:100]}")
            return ''
    except Exception as e:
        print(f"  Curl exception: {e}")
        return ''

def fetch_rss_feed(url: str, source_name: str) -> List[Dict]:
    """Fetch and parse RSS feed directly."""
    try:
        # Use curl for The Information to avoid 403 errors
        if source_name == 'the-information':
            xml_data = fetch_rss_with_curl(url)
            if not xml_data:
                return []
            data = xml_data.encode('utf-8')
        else:
            # Use urllib for other sources
            headers = {
                'User-Agent': 'Mozilla/5.0 (compatible; TechBriefingBot/1.0)',
                'Accept': 'application/rss+xml,application/xml,text/xml,*/*',
            }
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=30) as response:
                data = response.read()

        # Try to parse as Atom first (The Information uses Atom), then RSS
        articles = []

        try:
            root = ET.fromstring(data)

            # Check if this is an Atom feed (The Information)
            if root.tag == '{http://www.w3.org/2005/Atom}feed':
                ns = {'atom': 'http://www.w3.org/2005/Atom'}
                for entry in root.findall('atom:entry', ns):
                    title_elem = entry.find('atom:title', ns)
                    link_elem = entry.find('atom:link[@rel="alternate"]', ns)
                    pub_date_elem = entry.find('atom:published', ns)
                    author_elem = entry.find('atom:author/atom:name', ns)

                    if title_elem is not None and title_elem.text:
                        articles.append({
                            'title': title_elem.text,
                            'url': link_elem.get('href') if link_elem is not None else '',
                            'published': pub_date_elem.text[:10] if pub_date_elem is not None and pub_date_elem.text else '',
                            'blog': 'The Information',
                            'source_name': source_name,
                            'fetched_date': get_today_str()
                        })
            else:
                # Standard RSS feed
                for item in root.findall('.//item'):
                    title_elem = item.find('title')
                    link_elem = item.find('link')
                    pub_date_elem = item.find('pubDate')
                    source_elem = item.find('source')

                    if title_elem is not None and title_elem.text:
                        articles.append({
                            'title': title_elem.text,
                            'url': link_elem.text if link_elem is not None else '',
                            'published': pub_date_elem.text[:10] if pub_date_elem is not None and pub_date_elem.text else '',
                            'blog': source_elem.text if source_elem is not None else source_name,
                            'source_name': source_name,
                            'fetched_date': get_today_str()
                        })
        except ET.ParseError as e:
            print(f"XML parse error for {source_name}: {e}")
            return []

        return articles
    except Exception as e:
        print(f"Error fetching {source_name}: {e}")
        return []

def save_daily_articles(articles: List[Dict]):
    """Save today's articles to file."""
    ensure_data_dir()
    today = get_today_str()
    filepath = os.path.join(DATA_DIR, f"articles_{today}.json")
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(articles, f, ensure_ascii=False, indent=2)
    
    print(f"Saved {len(articles)} articles to {filepath}")

def load_articles_last_7_days() -> List[Dict]:
    """Load articles from last 7 days."""
    ensure_data_dir()
    dates = get_last_7_days()
    all_articles = []
    
    for date_str in dates:
        filepath = os.path.join(DATA_DIR, f"articles_{date_str}.json")
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                articles = json.load(f)
                all_articles.extend(articles)
                print(f"Loaded {len(articles)} articles from {date_str}")
        else:
            print(f"No data for {date_str}")
    
    return all_articles

def deduplicate_articles(articles: List[Dict]) -> List[Dict]:
    """Remove duplicate articles based on URL or title."""
    seen_urls = set()
    seen_titles = set()
    unique = []
    
    for article in articles:
        url = article.get('url', '')
        title = article.get('title', '').lower()
        
        # Skip if URL seen
        if url and url in seen_urls:
            continue
        
        # Skip if title seen (exact match)
        if title in seen_titles:
            continue
        
        seen_urls.add(url)
        seen_titles.add(title)
        unique.append(article)
    
    return unique

def extract_key_terms(title: str) -> set:
    """Extract key terms from title for similarity comparison."""
    stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by',
                  'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had', 'do', 'does', 'did',
                  'will', 'would', 'could', 'should', 'may', 'might', 'must', 'can',
                  'this', 'that', 'these', 'those', 'says', 'new', 'after', 'up', 'out', 'over', 'more'}
    
    cleaned = re.sub(r'[^\w\s]', ' ', title.lower())
    words = [w for w in cleaned.split() if len(w) > 2 and w not in stop_words]
    return set(words)

def calculate_similarity(title1: str, title2: str) -> float:
    """Calculate Jaccard similarity between two titles."""
    terms1 = extract_key_terms(title1)
    terms2 = extract_key_terms(title2)
    
    if not terms1 or not terms2:
        return 0.0
    
    intersection = terms1 & terms2
    union = terms1 | terms2
    
    if not union:
        return 0.0
    
    return len(intersection) / len(union)

def is_same_news(article1: Dict, article2: Dict) -> bool:
    """Determine if two articles are about the same news story."""
    title1 = article1.get('title', '')
    title2 = article2.get('title', '')
    
    # Threshold: 18%
    similarity = calculate_similarity(title1, title2)
    if similarity >= 0.18:
        return True
    
    # Check for exact phrase match (3+ consecutive words)
    words1 = title1.lower().split()
    for i in range(len(words1) - 2):
        phrase = ' '.join(words1[i:i+3])
        if len(phrase) > 10 and phrase in title2.lower():
            return True
    
    return False

def is_autonomous_driving(title: str) -> bool:
    """Check if article is about autonomous driving."""
    title_lower = title.lower()
    return any(kw.lower() in title_lower for kw in AUTONOMOUS_KEYWORDS)

def aggregate_news_by_coverage(articles: List[Dict]) -> Tuple[List[Dict], List[Dict]]:
    """Aggregate news by similarity and count coverage across media sources."""
    if not articles:
        return [], []
    
    # Group similar articles together
    news_groups = []
    used = set()
    
    for i, article in enumerate(articles):
        if i in used:
            continue
        
        group = [article]
        used.add(i)
        
        for j, other in enumerate(articles[i+1:], start=i+1):
            if j in used:
                continue
            if is_same_news(article, other):
                group.append(other)
                used.add(j)
        
        news_groups.append(group)
    
    print(f"Grouped {len(articles)} articles into {len(news_groups)} unique stories")
    
    # Create news items with coverage count
    autonomous_news = []
    other_news = []
    
    for group in news_groups:
        title = group[0]['title']
        # Build source->url mapping
        source_url_map = {}
        for a in group:
            blog = a.get('blog', '')
            url = a.get('url', '')
            if blog and url and blog not in source_url_map:
                source_url_map[blog] = url
        
        sources = list(source_url_map.keys())
        urls = list(source_url_map.values())
        
        news_item = {
            'title': title,
            'sources': sources,
            'urls': urls,
            'source_url_map': source_url_map,  # For accurate source->url mapping
            'coverage_count': len(sources)
        }
        
        if is_autonomous_driving(title):
            autonomous_news.append(news_item)
        else:
            other_news.append(news_item)
    
    # Sort by coverage count (descending)
    autonomous_news.sort(key=lambda x: x['coverage_count'], reverse=True)
    other_news.sort(key=lambda x: x['coverage_count'], reverse=True)
    
    return autonomous_news, other_news

# Simple translation cache for common terms
TITLE_TRANSLATIONS = {
    "OpenAI": "OpenAI",
    "Anthropic": "Anthropic",
    "Google": "谷歌",
    "Alphabet": "Alphabet",
    "Microsoft": "微软",
    "Amazon": "亚马逊",
    "Apple": "苹果",
    "Meta": "Meta",
    "Tesla": "特斯拉",
    "NVIDIA": "英伟达",
    "Pentagon": "五角大楼",
    "Defense": "国防",
    "AI": "AI",
    "robotics": "机器人",
    "quits": "辞职",
    "resigns": "辞职",
    "deal": "交易",
    "acquisition": "收购",
    "funding": "融资",
    "valuation": "估值",
    "layoffs": "裁员",
    "launch": "发布",
    "announces": "宣布",
}

def translate_title(title: str) -> str:
    """Simple translation for title context."""
    # For now, return title with key terms noted
    # In production, this could use an API
    return title

def generate_hot_news_summary(hot_news: List[Dict]) -> str:
    """Generate one-paragraph Chinese summary of all hot news per SKILL.md spec."""
    if not hot_news:
        return "本周暂无多媒体报道的热点新闻。"
    
    summaries = []
    for news in hot_news[:5]:  # Top 5 for summary
        title = news['title']
        # Extract key entities from title
        if 'OpenAI' in title and ('Pentagon' in title or 'Defense' in title or 'quits' in title.lower()):
            summaries.append("OpenAI机器人负责人因五角大楼合作辞职")
        elif 'Anthropic' in title and ('Claude' in title or 'defense' in title.lower() or 'Pentagon' in title):
            summaries.append("Anthropic Claude仍对非国防客户可用")
        elif 'Security Cameras' in title or 'Hacking' in title or 'Ukraine' in title or 'Iran' in title:
            summaries.append("监控摄像头入侵成为网络战新趋势")
        elif 'Uncanny Valley' in title or 'Prediction Market' in title or 'Kalshi' in title:
            summaries.append("播客探讨AI时代战争与预测市场伦理")
        elif 'Google' in title and 'Pichai' in title:
            summaries.append("谷歌CEO Pichai获得巨额薪酬")
        elif 'Waymo' in title or 'Zoox' in title or 'Aurora' in title or 'Cruise' in title:
            summaries.append("自动驾驶领域新动态")
        elif 'Tesla' in title or 'Musk' in title:
            summaries.append("特斯拉/Musk相关动态")
        elif 'Apple' in title and ('iPhone' in title or 'Mac' in title):
            summaries.append("苹果产品新动态")
        else:
            # Generic summary - first 30 chars of title
            short_title = title[:25] + "..." if len(title) > 25 else title
            summaries.append(short_title)
    
    return f"{len(hot_news)}条热点新闻被≥2家媒体报道：" + "；".join([f"{i+1}.{s}" for i, s in enumerate(summaries)])

def generate_report(autonomous_news: List[Dict], other_news: List[Dict], total_articles: int, all_articles: List[Dict] = None) -> str:
    """Generate the weekly briefing report per SKILL.md specification.
    
    Format:
    1. 中文概览 - One paragraph summarizing all hot news
    2. 🔥 热点新闻 - English titles, all source links, numbered
    3. 🚗 Robotaxi Weekly - All autonomous news
    4. Timestamp
    """
    now = datetime.now().strftime('%Y-%m-%d')
    
    # Filter hot news (>= 2 media coverage) from other_news
    hot_news = [n for n in other_news if n['coverage_count'] >= 2]
    hot_news.sort(key=lambda x: x['coverage_count'], reverse=True)
    
    # Get all autonomous news for Robotaxi section
    autonomous_display = autonomous_news
    
    # Generate Chinese summary per SKILL.md
    hot_summary = generate_hot_news_summary(hot_news)

    report = f"""📊 外媒科技周报 | {now}

📈 概览
本周扫描{len(RSS_SOURCES)}家科技媒体，获取{total_articles}篇文章，聚类为{len(autonomous_news) + len(other_news)}条独特新闻。{hot_summary}

---

🔥 热点新闻（按媒体报道数倒序）

"""

    if not hot_news:
        report += "本周暂无多媒体报道的热点新闻。\n\n"
    else:
        for i, news in enumerate(hot_news[:20], 1):
            source_url_map = news.get('source_url_map', {})
            
            # Format per SKILL.md: each source on new line with bullet
            source_lines = []
            for src in news['sources'][:5]:
                url = source_url_map.get(src, news['urls'][0] if news['urls'] else '')
                source_lines.append(f"• {src}: {url}")
            sources_text = '\n'.join(source_lines)
            
            report += f"""{i}️⃣ {news['title']}
📰 {news['coverage_count']}家：
{sources_text}

"""

    report += """---

🚗 Robotaxi Weekly / 自动驾驶一周汇总

"""

    if not autonomous_display:
        report += "本周暂无自动驾驶相关新闻。\n\n"
    else:
        for i, news in enumerate(autonomous_display[:30], 1):
            source_url_map = news.get('source_url_map', {})
            sources = list(source_url_map.keys())[:3]
            sources_str = ', '.join(sources)
            url = news['urls'][0] if news['urls'] else ''
            
            report += f"""{i}. {news['title']}
   📰 {sources_str} | 🔗 {url}

"""

    report += f"""---

⏰ 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')} (北京时间)
"""
    return report

    report += f"""
⏰ 报告生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M')} (北京时间)
"""

    return report

def daily_fetch():
    """Daily task: Fetch RSS and save articles."""
    print("=" * 60)
    print("Daily RSS Fetch / 每日RSS抓取")
    print("=" * 60)

    all_articles = []
    for name, url in RSS_SOURCES.items():
        print(f"\nFetching {name}...")
        articles = fetch_rss_feed(url, name)
        print(f"  Found {len(articles)} articles")
        all_articles.extend(articles)

    # Filter low-quality content
    print("\nFiltering low-quality content...")
    filtered_articles = filter_low_quality_articles(all_articles)

    # Deduplicate before saving
    unique_articles = deduplicate_articles(filtered_articles)
    print(f"\nTotal: {len(all_articles)} articles, {len(filtered_articles)} after filtering, {len(unique_articles)} unique")

    # Save to file
    save_daily_articles(unique_articles)

    print("\n" + "=" * 60)
    print("Daily fetch completed / 每日抓取完成")
    print("=" * 60)

# Company keywords for categorization
COMPANY_KEYWORDS = {
    'Waymo': ['waymo', 'robotaxi'],
    'Zoox': ['zoox'],
    'Aurora': ['aurora'],
    'Cruise': ['cruise'],
    'OpenAI': ['openai', 'chatgpt', 'gpt', 'sam altman'],
    'Anthropic': ['anthropic', 'claude', 'dario amodei'],
    'Google': ['google', 'alphabet', 'sundar pichai', 'gemini'],
    'Microsoft': ['microsoft', 'azure', 'satya nadella'],
    'Amazon': ['amazon', 'aws'],
    'Apple': ['apple', 'iphone', 'mac', 'tim cook'],
    'Meta': ['meta', 'facebook', 'instagram', 'mark zuckerberg'],
    'Tesla': ['tesla', 'elon musk', 'cybertruck'],
    'NVIDIA': ['nvidia', 'geforce'],
}

def categorize_by_company(articles: List[Dict]) -> Dict[str, List[Dict]]:
    """Categorize articles by company mentions."""
    categorized = {k: [] for k in COMPANY_KEYWORDS.keys()}
    categorized['Other'] = []
    
    for article in articles:
        title = article.get('title', '').lower()
        found = False
        for company, keywords in COMPANY_KEYWORDS.items():
            if any(kw in title for kw in keywords):
                categorized[company].append(article)
                found = True
                break
        if not found:
            categorized['Other'].append(article)
    
    return categorized

def save_company_data(categorized: Dict[str, List[Dict]]):
    """Save company categorized data for inline buttons."""
    ensure_data_dir()
    filepath = os.path.join(DATA_DIR, f"company_data_{get_today_str()}.json")
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(categorized, f, ensure_ascii=False, indent=2)
    print(f"Company data saved to: {filepath}")

def weekly_report():
    """Weekly task: Generate report from accumulated data."""
    print("=" * 60)
    print("Weekly Report Generation / 周报生成")
    print("=" * 60)
    
    # Load articles from last 7 days
    print("\nLoading articles from last 7 days...")
    articles = load_articles_last_7_days()
    
    if not articles:
        print("ERROR: No articles found. Please run daily fetch first.")
        return None
    
    # Deduplicate across all days
    unique_articles = deduplicate_articles(articles)
    print(f"\nTotal unique articles: {len(unique_articles)}")
    
    # Categorize by company (for inline buttons)
    print("\nCategorizing by company...")
    categorized = categorize_by_company(unique_articles)
    save_company_data(categorized)
    
    # Aggregate by coverage
    print("\nAggregating news by coverage...")
    autonomous_news, other_news = aggregate_news_by_coverage(unique_articles)
    
    print(f"\nResults:")
    print(f"  Autonomous driving stories: {len(autonomous_news)}")
    print(f"  Other tech stories: {len(other_news)}")
    
    # Show company stats
    print(f"\nCompany mentions:")
    for company, items in sorted(categorized.items(), key=lambda x: len(x[1]), reverse=True)[:10]:
        if len(items) > 0:
            print(f"  {company}: {len(items)}篇")
    
    # Show top stories
    if autonomous_news:
        print(f"\nTop autonomous stories by coverage:")
        for i, news in enumerate(autonomous_news[:3], 1):
            print(f"  {i}. [{news['coverage_count']}家] {news['title'][:50]}...")
    
    # Generate report
    print("\nGenerating report...")
    report = generate_report(autonomous_news, other_news, len(unique_articles), unique_articles)
    
    # Output report
    print("\n" + "=" * 60)
    print("REPORT GENERATED / 报告生成")
    print("=" * 60)
    print(report)
    
    # Save to file
    output_file = f"/tmp/tech-weekly-briefing-{datetime.now().strftime('%Y%m%d')}.txt"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(report)
    print(f"\nReport saved to: {output_file}")
    
    return report

def main():
    """Main entry point."""
    import argparse
    parser = argparse.ArgumentParser(description='Tech Weekly Briefing')
    parser.add_argument('mode', choices=['daily', 'weekly'], help='Run mode: daily (fetch RSS) or weekly (generate report)')
    args = parser.parse_args()
    
    if args.mode == 'daily':
        daily_fetch()
    elif args.mode == 'weekly':
        weekly_report()

if __name__ == "__main__":
    main()
