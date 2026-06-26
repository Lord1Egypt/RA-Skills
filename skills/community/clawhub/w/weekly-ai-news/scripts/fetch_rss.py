#!/usr/bin/env python3
"""
RSS 抓取脚本 - 获取 AI 新闻
Usage: python fetch_rss.py [--days N]
"""

import sys
import json
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
import re
import html

# RSS 源配置 - 增加更多AI相关源
RSS_SOURCES = {
    "ruanyifeng": {
        "name": "阮一峰的网络日志",
        "url": "https://www.ruanyifeng.com/blog/atom.xml",
        "type": "atom"
    },
    "36kr_ai": {
        "name": "36氪",
        "url": "https://36kr.com/feed",
        "type": "rss"
    },
    "huxiu": {
        "name": "虎嗅科技",
        "url": "https://www.huxiu.com/rss/0.xml",
        "type": "rss"
    },
    "tmtpost": {
        "name": "钛媒体",
        "url": "https://www.tmtpost.com/rss.xml",
        "type": "rss"
    },
    "ithome": {
        "name": "IT之家",
        "url": "https://www.ithome.com/rss/",
        "type": "rss"
    }
}

# AI 关键词 — 强信号（标题命中任一即认定为AI相关）
AI_KEYWORDS_STRONG = [
    # 明确的AI产品/模型名
    "chatgpt", "gpt-4", "gpt-5", "claude", "gemini", "copilot",
    "文心一言", "通义千问", "讯飞星火", "kimi", "月之暗面", "豆包",
    "midjourney", "stable diffusion", "dall-e", "sora", "suno",
    # 明确的AI公司
    "openai", "anthropic", "deepmind", "mistral",
    "智谱", "商汤", "百川智能", "零一万物", "minimax",
    # 明确的AI概念
    "大模型", "大语言模型", "aigc", "生成式ai", "generative ai",
    "人工智能", "artificial intelligence",
    "智能体", "ai agent",
]

# AI 关键词 — 弱信号（正文需命中2个以上才算）
AI_KEYWORDS_WEAK = [
    "ai", "llm", "机器学习", "深度学习",
    "多模态", "multimodal", "nlp", "computer vision",
    "算力", "gpu", "英伟达", "nvidia", "智算",
    "ai应用", "ai产品", "ai工具", "ai助手", "智能助手",
    "ai绘画", "ai写作", "ai编程", "ai医疗", "ai教育", "ai金融",
    "ai投资", "ai融资", "ai创业",
    "rag", "向量数据库", "embedding",
    "机器人", "自动驾驶", "无人驾驶",
]

# 技术性关键词（命中1个即过滤，要求词本身就足够说明是纯技术内容）
TECH_KEYWORDS = [
    # 论文/学术
    "论文解读", "论文精读", "arxiv", "paper reading",
    # 教程/原理讲解
    "pytorch", "tensorflow", "fine-tuning", "微调教程",
    "从零实现", "手把手", "源码解析", "代码实战",
    # 模型训练细节
    "梯度下降", "损失函数", "反向传播", "backpropagation",
    "模型蒸馏", "量化部署", "rlhf", "dpo",
    # 算法/架构
    "transformer原理", "attention机制", "卷积神经网络",
    "扩散模型原理", "vae原理",
    # 基准评测
    "benchmark", "sota", "leaderboard",
]

# 排除关键词 — 仅在标题中匹配（避免误杀正文提及这些词的AI新闻）
EXCLUDE_TITLE_KEYWORDS = [
    # 汽车（但保留"智能驾驶"、"自动驾驶"相关）
    "新能源汽车", "电动车", "充电桩", "小米汽车", "su7",
    # 房产/传统财经
    "房地产", "楼市", "房价",
    # 娱乐
    "娱乐圈", "明星", "电影票房", "综艺节目",
    # 电商促销
    "双十一", "618", "年货节", "大促",
    # 手机评测（非AI功能）
    "拆解", "跑分", "续航测试", "充电速度",
    # 新闻聚合/早晚报（通常是杂烩，AI内容被稀释）
    "早报", "晚报", "今日要闻",
    # 游戏
    "游戏评测", "游戏攻略", "steam",
]

def clean_html(raw_html):
    """清理 HTML 标签"""
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return html.unescape(cleantext)

def fetch_url(url, timeout=20):
    """获取 URL 内容"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as response:
            return response.read().decode('utf-8', errors='ignore')
    except Exception as e:
        print(f"获取失败 {url}: {e}", file=sys.stderr)
        return None

def parse_date(date_str):
    """解析日期字符串，返回无时区的 datetime"""
    if not date_str:
        return None
    
    formats = [
        "%a, %d %b %Y %H:%M:%S %z",
        "%Y-%m-%dT%H:%M:%S%z",
        "%Y-%m-%dT%H:%M:%SZ",
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%dT%H:%M:%S.%f%z"
    ]
    
    for fmt in formats:
        try:
            dt = datetime.strptime(date_str.strip(), fmt)
            if dt.tzinfo is not None:
                dt = dt.replace(tzinfo=None)
            return dt
        except:
            continue
    
    return None

def parse_rss(xml_content, source_type="rss"):
    """解析 RSS/Atom"""
    entries = []
    try:
        root = ET.fromstring(xml_content)
        
        if source_type == "rss" or root.tag == "rss":
            channel = root.find("channel")
            if channel is None:
                return entries
            for item in channel.findall("item"):
                title = item.findtext("title", "").strip()
                link = item.findtext("link", "").strip()
                desc = item.findtext("description", "").strip()
                pub_date = item.findtext("pubDate", item.findtext("dc:date", ""))
                entries.append({
                    "title": title,
                    "link": link,
                    "description": desc,
                    "published": pub_date
                })
        
        elif source_type == "atom" or root.tag.endswith("feed"):
            ns = {"atom": "http://www.w3.org/2005/Atom"}
            for entry in root.findall("atom:entry", ns) or root.findall("entry"):
                title_elem = entry.find("atom:title", ns) or entry.find("title")
                title = title_elem.text.strip() if title_elem is not None and title_elem.text else ""
                
                link_elem = entry.find("atom:link", ns) or entry.find("link")
                link = link_elem.get("href", "") if link_elem is not None else ""
                
                summary_elem = entry.find("atom:summary", ns) or entry.find("summary") or entry.find("atom:content", ns) or entry.find("content")
                desc = summary_elem.text if summary_elem is not None and summary_elem.text else ""
                
                published_elem = entry.find("atom:published", ns) or entry.find("published") or entry.find("atom:updated", ns) or entry.find("updated")
                pub_date = published_elem.text if published_elem is not None and published_elem.text else ""
                
                entries.append({
                    "title": title,
                    "link": link,
                    "description": desc,
                    "published": pub_date
                })
    except Exception as e:
        print(f"解析错误: {e}", file=sys.stderr)
    
    return entries

def is_ai_related(title, description):
    """检查是否与 AI 相关"""
    title_lower = title.lower()
    text_lower = (title + " " + description).lower()

    # 标题命中排除词 → 直接排除
    for kw in EXCLUDE_TITLE_KEYWORDS:
        if kw.lower() in title_lower:
            return False

    # 标题命中强信号 → 直接通过
    if any(kw.lower() in title_lower for kw in AI_KEYWORDS_STRONG):
        return True

    # 正文命中强信号 → 通过
    if any(kw.lower() in text_lower for kw in AI_KEYWORDS_STRONG):
        return True

    # 弱信号需要正文命中2个以上
    weak_score = sum(1 for kw in AI_KEYWORDS_WEAK if kw.lower() in text_lower)
    return weak_score >= 2

def is_too_technical(title, description):
    """检查是否过于技术性（命中1个即过滤）"""
    text = (title + " " + description).lower()
    return any(kw.lower() in text for kw in TECH_KEYWORDS)

def get_last_monday():
    """获取上周一 00:00 作为截止日期"""
    now = datetime.now()
    # now.weekday(): 0=周一 ... 6=周日
    # 如果今天是周一，上周一是7天前；周二是8天前，以此类推
    days_since_last_monday = now.weekday() + 7
    last_monday = (now - timedelta(days=days_since_last_monday)).replace(
        hour=0, minute=0, second=0, microsecond=0
    )
    return last_monday

def title_similarity(a, b):
    """基于字符集合的简单相似度（Jaccard），用于去重"""
    set_a = set(a)
    set_b = set(b)
    if not set_a or not set_b:
        return 0.0
    return len(set_a & set_b) / len(set_a | set_b)

def deduplicate(news_list, threshold=0.6):
    """按标题相似度去重，保留先出现的（排序靠前的）"""
    result = []
    for news in news_list:
        is_dup = False
        for existing in result:
            if title_similarity(news["title"], existing["title"]) > threshold:
                is_dup = True
                break
        if not is_dup:
            result.append(news)
    return result

def main():
    # 解析参数
    days = None
    if "--days" in sys.argv:
        idx = sys.argv.index("--days")
        if idx + 1 < len(sys.argv):
            days = int(sys.argv[idx + 1])

    # 默认从上周一开始；指定 --days 则从N天前开始
    if days is not None:
        cutoff_date = datetime.now() - timedelta(days=days)
        print(f"日期范围: 过去 {days} 天", file=sys.stderr)
    else:
        cutoff_date = get_last_monday()
        print(f"日期范围: {cutoff_date.strftime('%Y-%m-%d')} 至今", file=sys.stderr)

    all_news = []
    source_stats = {}

    for source_id, source_info in RSS_SOURCES.items():
        print(f"正在获取: {source_info['name']}...", file=sys.stderr)

        xml_content = fetch_url(source_info["url"])
        if not xml_content:
            source_stats[source_info['name']] = "获取失败"
            continue

        entries = parse_rss(xml_content, source_info["type"])
        source_count = 0

        for entry in entries:
            # 清理描述
            entry["description"] = clean_html(entry["description"])[:500]

            # 解析日期
            pub_date = parse_date(entry["published"])
            if pub_date is None:
                continue

            # 检查日期范围
            if pub_date < cutoff_date:
                continue

            # 检查是否为 AI 相关
            if not is_ai_related(entry["title"], entry["description"]):
                continue

            # 检查是否过于技术性
            if is_too_technical(entry["title"], entry["description"]):
                continue

            all_news.append({
                "source": source_info["name"],
                "title": entry["title"],
                "link": entry["link"],
                "description": entry["description"],
                "published": entry["published"],
                "published_date": pub_date.isoformat()
            })
            source_count += 1

        source_stats[source_info['name']] = f"{source_count}条"

    # 按日期排序
    all_news.sort(key=lambda x: x["published_date"], reverse=True)

    # 去重
    before_dedup = len(all_news)
    all_news = deduplicate(all_news)
    if before_dedup > len(all_news):
        print(f"去重: {before_dedup} → {len(all_news)} 条", file=sys.stderr)

    # 输出统计
    print(f"各源统计: {source_stats}", file=sys.stderr)

    # 输出 JSON
    print(json.dumps(all_news, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
