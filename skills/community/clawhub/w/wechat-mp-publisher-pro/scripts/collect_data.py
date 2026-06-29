#!/usr/bin/env python3
"""
公众号数据采集脚本 — 热点追踪、竞品分析、关键词挖掘

用法:
  python3 collect_data.py --mode trending           # 当前热点趋势
  python3 collect_data.py --mode competitor          # 竞品公众号分析
  python3 collect_data.py --mode keywords            # 关键词数据挖掘
  python3 collect_data.py --mode search --query "关键词" # 搜索指定话题
"""

import argparse
import csv
import json
import re
import sys
import time
from collections import Counter, defaultdict
from datetime import datetime, timedelta
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.parse import quote, urlencode
from urllib.error import HTTPError, URLError


OUTPUT_DIR = Path("workspace/wechat_data")


def fetch_url(url: str, timeout: int = 15) -> str:
    """请求URL并返回响应文本"""
    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 14) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.230 Mobile Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/json,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Referer": "https://weixin.sogou.com/",
    }
    req = Request(url, headers=headers)
    for attempt in range(3):
        try:
            with urlopen(req, timeout=timeout) as resp:
                charset = resp.headers.get_content_charset() or "utf-8"
                return resp.read().decode(charset, errors="replace")
        except HTTPError as e:
            if e.code == 429 or e.code >= 500:
                wait = 2 ** (attempt + 1)
                print(f"  ⏳ 请求被限制，等待 {wait}s 重试...")
                time.sleep(wait)
            else:
                print(f"  ❌ HTTP {e.code}: {e.reason}")
                return ""
        except URLError as e:
            print(f"  ❌ 网络错误: {e.reason}")
            if attempt < 2:
                time.sleep(3)
                continue
            return ""
    return ""


def save_json(data: dict, filename: str):
    """保存JSON"""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    filepath = OUTPUT_DIR / filename
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2, default=str)
    print(f"  ✅ 已保存: {filepath}")
    return str(filepath)


def save_csv(headers: list[str], rows: list[dict], filename: str):
    """保存CSV"""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    filepath = OUTPUT_DIR / filename
    with open(filepath, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)
    print(f"  ✅ 已保存: {filepath}")
    return str(filepath)


def extract_sogou_articles(html: str) -> list[dict]:
    """从搜狗微信搜索结果中提取文章列表"""
    articles = []

    # 匹配文章块
    pattern = re.compile(
        r'<div class="txt-box">.*?'
        r'<h3>.*?<a[^>]*href="([^"]+)"[^>]*>(.*?)</a>.*?</h3>.*?'
        r'<p class="txt-info"[^>]*>(.*?)</p>',
        re.DOTALL
    )

    # 简化版提取 - 按文章卡片切分
    blocks = re.findall(
        r'<div class="news-box[^"]*"[^>]*>.*?</div>\s*</div>\s*</li>',
        html, re.DOTALL
    )

    for block in blocks:
        # 标题
        title_match = re.search(r'<h3>.*?<a[^>]*>(.*?)</a>', block, re.DOTALL)
        if not title_match:
            continue
        title = re.sub(r'<[^>]+>', '', title_match.group(1)).strip()
        title = re.sub(r'\s+', ' ', title)

        # 链接
        link_match = re.search(r'<a[^>]*href="([^"]*weixin[^"]*)"', block)
        link = link_match.group(1) if link_match else ""

        # 摘要
        desc_match = re.search(r'<p class="txt-info"[^>]*>(.*?)</p>', block, re.DOTALL)
        desc = re.sub(r'<[^>]+>', '', desc_match.group(1)).strip() if desc_match else ""
        desc = re.sub(r'\s+', ' ', desc)

        # 公众号名称
        account_match = re.search(r'<a[^>]*class="account"[^>]*>(.*?)</a>', block)
        account = re.sub(r'<[^>]+>', '', account_match.group(1)).strip() if account_match else ""

        articles.append({
            "title": title,
            "link": link,
            "summary": desc[:120],
            "account": account,
            "source": "sogou_wechat"
        })

    return articles


def mode_trending():
    """采集当前热点趋势"""
    print("🔥 采集微信热点趋势...")
    print("=" * 50)

    # 通过搜狗微信热点
    url = "https://weixin.sogou.com/"
    html = fetch_url(url)
    if not html:
        print("  ❌ 无法获取热点数据")
        return

    # 提取热搜词
    hot_pattern = re.compile(
        r'<li[^>]*>.*?<a[^>]*>(.*?)</a>.*?</li>',
        re.DOTALL
    )
    hot_items = re.findall(r'<li class="[^"]*hot[^"]*"[^>]*>.*?<a[^>]*>(.*?)</a>', html)
    if not hot_items:
        hot_items = re.findall(r'<a[^>]*class="hot[^"]*"[^>]*>(.*?)</a>', html)

    hot_words = []
    for item in hot_items[:20]:
        word = re.sub(r'<[^>]+>', '', item).strip()
        if word and len(word) > 1:
            hot_words.append({"keyword": word, "source": "sogou_hot", "collected_at": datetime.now().isoformat()})

    if hot_words:
        print(f"  获取到 {len(hot_words)} 个热搜词")
        for h in hot_words[:10]:
            print(f"    • {h['keyword']}")
        filename = f"trending_{datetime.now().strftime('%Y%m%d')}.json"
        save_json({"hot_words": hot_words, "collected_at": datetime.now().isoformat()}, filename)
    else:
        # 回退方案：从文章标题提取高频词
        print("  ⚠️ 未直接获取到热搜列表，从文章标题提取高频词")
        articles = extract_sogou_articles(html)
        if articles:
            words = []
            for a in articles:
                words.extend(re.findall(r'[\u4e00-\u9fa5]{2,6}', a["title"]))
            word_counts = Counter(words)
            common = word_counts.most_common(20)
            print(f"  从 {len(articles)} 篇文章提取高频词:")
            for word, count in common[:15]:
                print(f"    • {word} ({count}次)")
            save_json({"extracted_words": [{"word": w, "count": c} for w, c in common]}, f"keywords_{datetime.now().strftime('%Y%m%d')}.json")


def mode_competitor():
    """竞品内容分析"""
    print("📊 竞品公众号内容分析...")
    print("=" * 50)

    print("  输入竞品公众号名称（多个用逗号分隔）:")
    print("  💡 示例: 运营研究社,秋叶PPT,插座学院")

    # 读取用户输入的竞品列表
    competitors_input = input("  >> ").strip()
    if not competitors_input:
        competitors = ["运营研究社", "秋叶PPT", "插座学院"]
        print(f"  使用默认竞品列表: {', '.join(competitors)}")
    else:
        competitors = [c.strip() for c in competitors_input.split(",")]

    all_articles = []
    for competitor in competitors[:5]:
        print(f"\n  🔍 搜索公众号: {competitor}")
        url = f"https://weixin.sogou.com/weixin?type=1&query={quote(competitor)}&ie=utf8"
        html = fetch_url(url)
        if html:
            # 提取最新文章
            articles = extract_sogou_articles(html)
            for a in articles:
                a["competitor"] = competitor
            all_articles.extend(articles)
            print(f"    找到 {len(articles)} 篇文章")
        time.sleep(1)

    if not all_articles:
        print("  ❌ 未获取到竞品数据，将使用通用行业数据")
        # 按行业搜索通用数据
        industries = [
            "公众号运营", "自媒体", "新媒体", "内容创业", "知识付费",
            "副业赚钱", "个人IP", "职场", "AI", "效率工具"
        ]
        for ind in industries[:5]:
            url = f"https://weixin.sogou.com/weixin?type=2&query={quote(ind)}&ie=utf8"
            html = fetch_url(url)
            if html:
                articles = extract_sogou_articles(html)
                for a in articles:
                    a["competitor"] = ind
                all_articles.extend(articles)
            time.sleep(1)
        save_csv(
            ["title", "account", "summary", "competitor", "source"],
            all_articles,
            f"industry_data_{datetime.now().strftime('%Y%m%d')}.csv"
        )
        return

    # 统计分析
    accounts = Counter(a["account"] for a in all_articles if a["account"])
    print(f"\n📈 竞品分析结果:")
    print(f"  共获取 {len(all_articles)} 篇文章")
    print(f"  涉及 {len(accounts)} 个公众号")
    for acc, count in accounts.most_common(10):
        print(f"    • {acc}: {count} 篇")

    # 标题高频词
    titles_text = " ".join(a["title"] for a in all_articles)
    title_words = [w for w in re.findall(r'[\u4e00-\u9fa5]{2,8}', titles_text)
                   if w not in ["我们", "什么", "一个", "可以", "没有", "这个", "那个", "就是",
                                "不是", "他们", "你们", "已经", "自己", "知道", "如果", "因为"]]
    common_words = Counter(title_words).most_common(20)
    if common_words:
        print(f"\n  标题高频词 Top10:")
        for word, count in common_words[:10]:
            print(f"    • {word} ({count}次)")

    save_csv(
        ["title", "account", "summary", "competitor", "source"],
        all_articles,
        f"competitor_{datetime.now().strftime('%Y%m%d')}.csv"
    )

    summary = {
        "total_articles": len(all_articles),
        "competitors_analyzed": len(competitors),
        "accounts_found": len(accounts),
        "top_accounts": dict(accounts.most_common(10)),
        "title_hot_words": dict(common_words[:15]),
        "collected_at": datetime.now().isoformat()
    }
    save_json(summary, f"competitor_summary_{datetime.now().strftime('%Y%m%d')}.json")


def mode_keywords():
    """关键词数据挖掘"""
    print("🔑 关键词数据挖掘...")
    print("=" * 50)

    seed_keywords = input("  输入种子关键词（多个用逗号分隔）: ").strip()
    if not seed_keywords:
        print("  ❌ 请至少输入一个关键词")
        return

    seeds = [k.strip() for k in seed_keywords.split(",")]
    all_articles = []
    all_keywords = Counter()

    for seed in seeds[:5]:
        print(f"\n  🔍 搜索: {seed}")
        url = f"https://weixin.sogou.com/weixin?type=2&query={quote(seed)}&ie=utf8"
        html = fetch_url(url)
        if html:
            articles = extract_sogou_articles(html)
            all_articles.extend(articles)
            print(f"    找到 {len(articles)} 篇文章")

            # 提取关联词
            words = re.findall(r'[\u4e00-\u9fa5]{2,6}', " ".join(a["title"] for a in articles))
            for w in words:
                if w != seed:
                    all_keywords[w] += 1
        time.sleep(1)

    if not all_articles:
        print("  ❌ 未获取到数据，将生成关联词建议")
        # 生成常见关联词建议
        related = generate_related_keywords(seeds)
        save_json({"seed_keywords": seeds, "related_keywords": related}, f"keyword_suggestions_{datetime.now().strftime('%Y%m%d')}.json")
        return

    # 过滤常见词
    stop_words = {"我们", "什么", "一个", "可以", "没有", "这个", "那个", "就是", "不是",
                  "他们", "你们", "已经", "自己", "知道", "如果", "因为", "所以", "但是",
                  "而且", "或者", "虽然", "然后", "这样", "那样", "这些", "那些"}
    related_words = {w: c for w, c in all_keywords.most_common(30) if w not in stop_words}

    print(f"\n📈 关联词推荐 Top15:")
    for i, (word, count) in enumerate(list(related_words.items())[:15], 1):
        print(f"  {i:2d}. {word} ({count}次)")

    save_csv(
        ["title", "account", "summary", "source"],
        all_articles,
        f"keyword_{seeds[0]}_{datetime.now().strftime('%Y%m%d')}.csv"
    )

    result = {
        "seed_keywords": seeds,
        "related_keywords": dict(list(related_words.items())[:30]),
        "total_articles": len(all_articles),
        "collected_at": datetime.now().isoformat()
    }
    save_json(result, f"keyword_analysis_{datetime.now().strftime('%Y%m%d')}.json")


def generate_related_keywords(seeds: list[str]) -> list[str]:
    """生成常见关联词（回退方案）"""
    word_map = {
        "公众号": ["运营", "涨粉", "变现", "写作", "内容", "排版", "引流", "自媒体", "副业", "流量"],
        "运营": ["公众号", "私域", "增长", "用户", "内容", "数据", "社群", "活动", "转化", "留存"],
        "副业": ["赚钱", "兼职", "项目", "收入", "月入", "副业", "自由职业", "创业", "投资", "被动收入"],
        "AI": ["人工智能", "ChatGPT", "大模型", "AIGC", "AI工具", "效率提升", "自动化", "机器学习", "Prompt"],
        "职场": ["升职", "加薪", "面试", "简历", "沟通", "管理", "效率", "PPT", "Excel", "汇报"],
    }
    related = []
    for seed in seeds:
        if seed in word_map:
            related.extend(word_map[seed])
        else:
            # 随机建议
            related.extend([f"{seed}入门", f"{seed}技巧", f"{seed}案例", f"{seed}趋势", f"{seed}干货"])
    return list(set(related))[:15]


def mode_search():
    """搜索指定话题"""
    print("🔍 搜索指定话题...")
    print("=" * 50)

    query = input("  输入搜索关键词: ").strip()
    if not query:
        return

    url = f"https://weixin.sogou.com/weixin?type=2&query={quote(query)}&ie=utf8"
    html = fetch_url(url)
    if not html:
        print("  ❌ 搜索失败")
        return

    articles = extract_sogou_articles(html)
    if not articles:
        print("  ⚠️ 未找到相关文章")
        return

    print(f"\n  找到 {len(articles)} 篇相关文章:")
    for i, a in enumerate(articles[:15], 1):
        print(f"  {i:2d}. [{a['account']}] {a['title'][:40]}")
        if a['summary']:
            print(f"      {a['summary'][:60]}")

    # 数据分析
    print(f"\n📈 搜索分析:")
    print(f"  相关文章数: {len(articles)}")
    accounts = Counter(a["account"] for a in articles if a["account"])
    print(f"  涉及公众号: {len(accounts)} 个")
    print(f"  最活跃账号: {accounts.most_common(3)}")

    filename = f"search_{query}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    save_csv(["title", "account", "summary", "source"], articles, filename)


def main():
    parser = argparse.ArgumentParser(description="公众号数据采集工具")
    parser.add_argument("--mode", default="trending",
                       choices=["trending", "competitor", "keywords", "search"],
                       help="采集模式")
    parser.add_argument("--query", help="搜索关键词（search模式）")

    args = parser.parse_args()

    print(f"""
╔══════════════════════════════════════╗
║   公众号数据采集系统                     ║
║   模式: {args.mode:<18}  ║
╚══════════════════════════════════════╝
""")

    mode_map = {
        "trending": mode_trending,
        "competitor": mode_competitor,
        "keywords": mode_keywords,
        "search": mode_search,
    }

    mode_map[args.mode]()
    print(f"\n  输出目录: {OUTPUT_DIR}/")


if __name__ == "__main__":
    main()
