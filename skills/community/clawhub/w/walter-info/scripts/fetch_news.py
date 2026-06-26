#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
跨境电商资讯获取脚本
用法: python fetch_news.py --output OUTPUT_DIR [--config CONFIG_PATH]
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime, timezone, timedelta

# Windows 中文控制台 UTF-8 修复
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

# =============================================================================
# 来源分级表
# =============================================================================
SOURCE_TIER_MAP = {
    "aboutamazon.com": "official", "amazon.com": "official",
    "tiktok.com": "official",
    "reuters": "tier1", "apnews": "tier1", "bloomberg": "tier1", "bbc": "tier1",
    "wsj": "tier2", "financial times": "tier2", "cnbc": "tier2",
    "techcrunch": "tier3", "forbes": "tier3", "fortune": "tier3",
    "marketplace pulse": "tier4", "jungle scout": "tier4",
}

TIER_SCORES = {
    "official": 25, "tier1": 20, "tier2": 12, "tier3": 5, "tier4": 3, "unrated": 0
}


def get_source_tier(source_name: str) -> str:
    name_lower = source_name.lower()
    for key, tier in SOURCE_TIER_MAP.items():
        if key in name_lower:
            return tier
    return "unrated"


def get_core_keywords(text: str) -> set:
    text_lower = text.lower()
    en_core = {
        "amazon", "fba", "temu", "shein", "aliexpress", "mercadolibre",
        "tiktok", "black friday", "cyber monday", "prime day",
        "logistics", "shipping", "freight", "fulfillment",
        "tariff", "duty", "ban", "restriction", "fee", "surcharge",
        "cross-border", "ecommerce", "marketplace", "seller",
    }
    en_words = set(re.findall(r'\b[a-z]{3,}\b', text_lower))
    en_found = en_words & en_core
    zh_core = ["亚马逊", "fba", "temu", "shein", "速卖通", "美客多",
               "tiktok", "抖音", "跨境", "电商", "关税", "物流", "船运", "促销"]
    zh_found = {kw for kw in zh_core if kw.lower() in text_lower}
    return en_found | zh_found





def calculate_impact_score(title: str, description: str, published_at: str, source_name: str) -> tuple:
    text = (title + " " + description).lower()
    score = 0.0

    # 1. 业务相关性权重（0-30）
    amazon_direct = {"fba", "amazon fba", "亚马逊fba", "亚马逊物流",
                    "fba头程", "fba仓储", "fba费用", "fba标签", "亚马逊卖家", "亚马逊店铺"}
    amazon_indirect = {"亚马逊", "amazon.com"}
    tiktok_direct = {"tiktok shop", "tiktokshop"}
    tiktok_indirect = {"tiktok", "抖音电商", "tiktok带货", "tiktok达人"}
    other_platform = {"temu卖家", "temu", "shein", "aliexpress", "速卖通", "美客多", "mercadolibre"}
    general_crossborder = {"跨境电商", "跨境卖家", "跨境物流", "跨境贸易", "ecommerce seller"}

    amazon_hits = sum(1 for kw in amazon_direct if kw in text)
    if amazon_hits == 0:
        amazon_hits = sum(1 for kw in amazon_indirect if kw in text)

    tiktok_hits = sum(1 for kw in tiktok_direct if kw in text)
    if tiktok_hits == 0:
        tiktok_hits = sum(1 for kw in tiktok_indirect if kw in text)

    other_hits = sum(1 for kw in other_platform if kw in text)
    general_hits = sum(1 for kw in general_crossborder if kw in text)

    if amazon_hits > 0:
        score += 30
    elif tiktok_hits > 0:
        score += 18
    elif other_hits > 0:
        score += 12
    elif general_hits > 0:
        score += 5

    # 2. 影响程度（0-30）
    if any(kw in text for kw in ["tariff", "duty", "ban", "restriction", "fee", "surcharge", "penalty", "fine", "margin", "profit drop"]):
        score += 30
    elif any(kw in text for kw in ["expansion", "growth", "investment", "gmv", "revenue", "增长", "营收"]):
        score += 15

    # 3. 品类加成（0-15）
    if any(kw in text for kw in ["fashion", "clothing", "apparel", "dress", "shoe", "美妆", "服装", "时尚", "箱包"]):
        score += 15

    # 4. 时间分数（0-15）
    try:
        pub_time = datetime.fromisoformat(published_at.replace('Z', '+00:00'))
        now = datetime.now(pub_time.tzinfo)
        hours_old = (now - pub_time).total_seconds() / 3600
        if hours_old <= 24:
            score += 15
        elif hours_old <= 48:
            score += 10
        elif hours_old <= 72:
            score += 5
    except Exception:
        score += 5

    # 5. 来源权威性（0-10）
    source_tier = get_source_tier(source_name)
    score += TIER_SCORES.get(source_tier, 0)

    return score, source_tier


def is_similar_news(title1: str, title2: str) -> bool:
    words1 = get_core_keywords(title1)
    words2 = get_core_keywords(title2)
    if not words1 or not words2:
        return False
    common = len(words1 & words2)
    return common >= 2


def _retry_request(url: str, data: bytes = None, headers: dict = None, max_retries: int = 3) -> bytes:
    """带重试的 HTTP 请求"""
    import time
    import urllib.request
    import ssl as _ssl
    ctx = _ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = _ssl.CERT_NONE
    for attempt in range(max_retries):
        try:
            req = urllib.request.Request(url, data=data, headers=headers or {})
            with urllib.request.urlopen(req, timeout=15, context=ctx) as resp:
                return resp.read()
        except Exception:
            if attempt < max_retries - 1:
                time.sleep(1)
            else:
                raise
    return b""


def fetch_news_ennews(config: dict = None) -> list:
    """从 ennews.com 抓取文章，只取最新一天内容，支持翻页

    首页 HTML 只有 10 条，翻页需调 AJAX API：
    POST /Home/NewsFlash/ajaxGetShortNews
    翻页上限由 config["news"]["ennews_max_pages"] 控制，默认 4 页。
    """
    news_cfg = (config or {}).get("news", {})
    max_pages = news_cfg.get("ennews_max_pages", 4)
    import urllib.request
    import urllib.parse
    import ssl

    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    block_pattern = re.compile(r'<div class="z_short_con1">(.*?)</div>\s*</div>', re.DOTALL)
    date_pattern = re.compile(r'<span>(\d{4}-\d{2}-\d{2} \d{2}:\d{2})</span>')
    url_pattern = re.compile(r'href="(https://www\.ennews\.com/news-\d+\.html)"')
    title_pattern = re.compile(r'<h1>(.*?)</h1>', re.DOTALL)
    desc_pattern = re.compile(r'<p[^>]*>(.*?)</p>', re.DOTALL)

    try:
        raw = _retry_request(
            "https://www.ennews.com/news/",
            headers={"User-Agent": "Mozilla/5.0"}
        )
        html_text = raw.decode("utf-8")
    except Exception:
        return []

    all_dates = date_pattern.findall(html_text)
    blocks = block_pattern.findall(html_text)

    # 确定最新一天日期
    latest_date_str = None
    for ds in all_dates:
        try:
            dt = datetime.strptime(ds, "%Y-%m-%d %H:%M")
            if latest_date_str is None or ds[:10] > latest_date_str:
                latest_date_str = ds[:10]
        except Exception:
            continue

    if not latest_date_str:
        return []

    # 从首页获取 last_short_id 用于翻页
    m = re.search(r'id="last_short_id"[^>]+value="(\d+)"', html_text)
    last_short_id = m.group(1) if m else "131661"

    articles = []
    seen_urls = set()
    page = 1
    page_data = html_text
    while True:
        page_blocks = block_pattern.findall(page_data)
        page_dates = date_pattern.findall(page_data)

        if not page_blocks:
            break

        # 判断是否出现更早日期（翻页停止信号）
        # 只要该页所有文章日期都比目标日期老，就停止
        all_older = all(not d.startswith(latest_date_str) for d in page_dates)
        if all_older and page > 1:
            break

        if page > max_pages:
            break

        for i, block in enumerate(page_blocks):
            if i >= len(page_dates):
                continue
            date_str = page_dates[i]
            if not date_str.startswith(latest_date_str):
                continue

            url_match = url_pattern.search(block)
            title_match = title_pattern.search(block)
            desc_match = desc_pattern.search(block)
            if not url_match or not title_match:
                continue

            url = url_match.group(1)
            if url in seen_urls:
                continue
            seen_urls.add(url)

            try:
                pub_dt = datetime.strptime(date_str, "%Y-%m-%d %H:%M")
                pub_dt = pub_dt.replace(tzinfo=timezone.utc)
                published_at = pub_dt.strftime("%Y-%m-%dT%H:%M:%SZ")
            except Exception:
                published_at = ""

            title = re.sub(r'<[^>]+>', '', title_match.group(1))
            desc_html = desc_match.group(1) if desc_match else ""
            desc = re.sub(r'<[^>]+>', '', desc_html).strip()

            articles.append({
                "title": title,
                "description": desc,
                "source": "ennews",
                "url": url,
                "published_at": published_at,
            })

        if len(page_blocks) < 10:
            break

        page += 1
        try:
            post_data = urllib.parse.urlencode({
                "page": page,
                "loadcontinue": "true",
                "cate_id": "",
                "market_id": "",
                "async": "0",
                "social_id": "",
                "ecommerce_id": "",
                "last_short_id": last_short_id,
            }).encode("utf-8")

            raw = _retry_request(
                "https://www.ennews.com/Home/NewsFlash/ajaxGetShortNews",
                data=post_data,
                headers={
                    "User-Agent": "Mozilla/5.0",
                    "Content-Type": "application/x-www-form-urlencoded",
                    "X-Requested-With": "XMLHttpRequest",
                    "Referer": "https://www.ennews.com/news/",
                }
            )
            resp_data = json.loads(raw.decode("utf-8"))

            page_data = resp_data.get("cont", "")
            new_last_id = resp_data.get("last_short_id", "")
            if new_last_id and new_last_id != last_short_id:
                last_short_id = new_last_id
            if not page_data or len(page_data) < 100:
                break
        except Exception:
            break

    return articles


def _fetch_cifnews_description(article_url: str) -> str:
    """抓取 cifnews 文章正文前两段作为描述（带重试）"""
    try:
        raw = _retry_request(article_url, headers={"User-Agent": "Mozilla/5.0"}, max_retries=3)
        paragraphs = re.findall(rb'<p[^>]*>(.*?)</p>', raw, re.DOTALL | re.I)
        parts = []
        for p in paragraphs:
            text = re.sub(rb'<[^>]+>', b'', p).strip()
            text = text.decode('utf-8', errors='replace')
            if len(text) < 30:
                continue
            if any(kw in text for kw in ['©', '版权所有', '转载', '未经授权']):
                continue
            parts.append(text)
            if len(parts) >= 2:
                break
        return ' '.join(parts)
    except Exception:
        return ""


def fetch_news_cifnews() -> list:
    """从 cifnews.com 解析文章列表，只取今天和昨天的内容

    首页 HTML 是 GBK 编码，但 data-fetch-title 属性里的中文是 UTF-8 字节。
    以日期位置为锚点，在其前面 500 字节内找 data-fetch-title，
    在标题前面 200 字节内找 data-fetch-id。
    """
    import urllib.request
    import ssl
    from datetime import datetime, timezone, timedelta

    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    try:
        req = urllib.request.Request(
            "https://www.cifnews.com/",
            headers={"User-Agent": "Mozilla/5.0"}
        )
        with urllib.request.urlopen(req, timeout=15, context=ctx) as resp:
            raw = resp.read()
    except Exception:
        return []

    today = datetime.now(timezone.utc).date()
    yesterday = today - timedelta(days=1)
    target_dates = [
        today.strftime("%Y-%m-%d").encode("utf-8"),
        yesterday.strftime("%Y-%m-%d").encode("utf-8"),
    ]

    articles = []
    seen_titles = set()
    seen_urls = set()
    search_from = 0

    while True:
        date_pos = -1
        matched_date_bytes = None
        for td_bytes in target_dates:
            pos = raw.find(td_bytes, search_from)
            if pos != -1 and (date_pos == -1 or pos < date_pos):
                date_pos = pos
                matched_date_bytes = td_bytes
        if date_pos == -1:
            break

        matched_date = matched_date_bytes.decode("utf-8")

        # 在日期前面 500 字节内找 data-fetch-title
        window_before = raw[max(0, date_pos - 500):date_pos]
        title = ""
        title_match = re.search(r'data-fetch-title="([^"]+)"', window_before.decode("utf-8", errors="replace"))
        if title_match:
            title_bytes = title_match.group(1).encode("utf-8")
            try:
                title = title_bytes.decode("utf-8")
            except Exception:
                title = title_bytes.decode("gbk", errors="replace")

        # 在标题前面 200 字节内找 data-fetch-id
        fetch_id = None
        if title_match:
            title_start_in_window = window_before.find(title_match.group(0).encode("utf-8"))
            block_window = window_before[max(0, title_start_in_window - 200):title_start_in_window]
            id_match = re.search(r'data-fetch-id="([^\s"<>]+)"', block_window.decode("utf-8", errors="replace"))
            if id_match:
                fetch_id = id_match.group(1)

        if fetch_id:
            if fetch_id.isdigit():
                full_url = f"https://www.cifnews.com/article/{fetch_id}"
            else:
                full_url = f"https://www.cifnews.com/observer/{fetch_id}"
        else:
            search_from = date_pos + 1
            continue

        if full_url in seen_urls:
            search_from = date_pos + 1
            continue
        seen_urls.add(full_url)

        if not title or title in seen_titles:
            search_from = date_pos + 1
            continue
        seen_titles.add(title)

        try:
            date_parts = matched_date.split("-")
            pub_dt = datetime(int(date_parts[0]), int(date_parts[1]), int(date_parts[2]), tzinfo=timezone.utc)
            published_at = pub_dt.strftime("%Y-%m-%dT%H:%M:%SZ")
        except Exception:
            published_at = ""

        description = _fetch_cifnews_description(full_url)

        articles.append({
            "title": title,
            "description": description,
            "source": "cifnews",
            "url": full_url,
            "published_at": published_at,
        })

        search_from = date_pos + 1

    return articles


def fetch_crossborder_news(config: dict = None) -> list:
    """获取跨境电商资讯：ennews + cifnews，计算权重，去重，取 Top N"""
    news_cfg = (config or {}).get("news", {})
    final_top_n = news_cfg.get("final_top_n", 18)

    all_articles = []
    all_articles.extend(fetch_news_ennews(config))
    all_articles.extend(fetch_news_cifnews())

    if not all_articles:
        return [{"error": "未获取到任何文章"}]

    scored = []
    for article in all_articles:
        score, source_tier = calculate_impact_score(
            article["title"], article["description"], article["published_at"], article["source"]
        )
        core_kw = get_core_keywords(article["title"])
        scored.append({
            **article,
            "source_tier": source_tier,
            "impact_score": score,
            "core_keywords": list(core_kw),
        })

    scored.sort(key=lambda x: x["impact_score"], reverse=True)

    selected = []
    for news in scored:
        too_similar = any(is_similar_news(news["title"], kept["title"]) for kept in selected)
        if not too_similar:
            selected.append(news)
        if len(selected) >= final_top_n:
            break

    return selected if selected else [{"error": "处理后无结果"}]


def format_news_report(news_data: list, date_str: str) -> str:
    lines = ["# 跨境电商热点资讯\n"]
    lines.append(f"**获取时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    lines.append(f"**数据来源**: ennews / cifnews\n")
    lines.append(f"**当日资讯数量**: {len(news_data)} 条\n\n")

    if not news_data:
        lines.append("暂无资讯\n")
        return "".join(lines)

    for i, item in enumerate(news_data, 1):
        if "error" in item:
            lines.append(f"### {i}. 错误\n{item.get('error', '')}\n")
            continue
        title = item.get("title", "")
        if not title:
            continue
        lines.append(f"### {i}. {title}\n")
        pub = item.get("published_at", "")
        if pub:
            lines.append(f"**发布时间**: {pub}\n")
        source = item.get("source", "")
        if source:
            lines.append(f"**来源**: {source}\n")
        desc = item.get("description", "")
        if desc:
            lines.append(f"**概要**: {desc}\n")
        url = item.get("url", "")
        if url:
            lines.append(f"**链接**: {url}\n")
        score = item.get("impact_score", 0)
        lines.append(f"**权重分**: {score}\n")
        lines.append("\n")

    return "".join(lines)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="获取跨境电商热点资讯")
    parser.add_argument("--output", default=None, help="输出目录")
    parser.add_argument("--config", default=None, help="配置文件路径")
    args = parser.parse_args()

    script_dir = os.path.dirname(os.path.abspath(__file__))
    if args.output is None:
        args.output = os.path.join(os.path.dirname(script_dir), "output")
    os.makedirs(args.output, exist_ok=True)

    # 加载配置
    if args.config:
        with open(args.config, "r", encoding="utf-8") as f:
            config = json.load(f)
    else:
        config_path = os.path.join(os.path.dirname(script_dir), "config.json")
        config = {"news": {"ennews_max_pages": 4, "final_top_n": 18}}
        if os.path.exists(config_path):
            with open(config_path, "r", encoding="utf-8") as f:
                config = json.load(f)

    date_str = datetime.now().strftime("%Y%m%d")
    news_data = fetch_crossborder_news(config)

    # 保存 JSON
    json_path = os.path.join(args.output, f"news_report_{date_str}.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump({
            "date": date_str,
            "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "type": "news",
            "source": "ennews / cifnews",
            "data": news_data
        }, f, ensure_ascii=False, indent=2)
    print(f"JSON已保存: {json_path}")

    # 保存 Markdown 报告
    md_content = format_news_report(news_data, date_str)
    md_path = os.path.join(args.output, f"news_report_{date_str}.md")
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(md_content)
    print(f"Markdown已保存: {md_path}")

    # 分别保存两个来源的原始数据
    ennews_raw = fetch_news_ennews(config)
    cifnews_raw = fetch_news_cifnews()

    enews_md_lines = [f"# ennews 原始资讯\n",
                      f"**获取时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n",
                      f"**来源**: ennews\n",
                      f"**资讯数量**: {len(ennews_raw)} 条\n\n"]
    for i, a in enumerate(ennews_raw, 1):
        enews_md_lines.append(f"### {i}. {a['title']}\n")
        if a.get('published_at'):
            enews_md_lines.append(f"**发布时间**: {a['published_at'][:10]}\n")
        if a.get('description'):
            desc = a['description']
            if len(desc) > 200:
                desc = desc[:200] + '...'
            enews_md_lines.append(f"**摘要**: {desc}\n")
        enews_md_lines.append(f"**链接**: {a['url']}\n\n")
    enews_path = os.path.join(args.output, f"ennews_{date_str}.md")
    with open(enews_path, "w", encoding="utf-8") as f:
        f.writelines(enews_md_lines)
    print(f"ennews原始数据已保存: {enews_path} ({len(ennews_raw)} 条)")

    cifnews_md_lines = [f"# cifnews 原始资讯\n",
                        f"**获取时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n",
                        f"**来源**: cifnews\n",
                        f"**资讯数量**: {len(cifnews_raw)} 条\n\n"]
    for i, a in enumerate(cifnews_raw, 1):
        cifnews_md_lines.append(f"### {i}. {a['title']}\n")
        if a.get('published_at'):
            cifnews_md_lines.append(f"**发布时间**: {a['published_at'][:10]}\n")
        if a.get('description'):
            desc = a['description']
            if len(desc) > 200:
                desc = desc[:200] + '...'
            cifnews_md_lines.append(f"**摘要**: {desc}\n")
        cifnews_md_lines.append(f"**链接**: {a['url']}\n\n")
    cifnews_path = os.path.join(args.output, f"cifnews_{date_str}.md")
    with open(cifnews_path, "w", encoding="utf-8") as f:
        f.writelines(cifnews_md_lines)
    print(f"cifnews原始数据已保存: {cifnews_path} ({len(cifnews_raw)} 条)")

    print(f"共获取 {len(news_data)} 条资讯")
