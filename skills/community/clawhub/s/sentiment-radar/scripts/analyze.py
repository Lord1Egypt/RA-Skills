#!/usr/bin/env python3
"""Analyze XHS crawl data and generate sentiment report.
Usage: python3 analyze.py --data ./data --products "产品A,产品B" --output report.md
"""
import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path


def parse_count(s):
    """Parse Chinese number strings like '1.1万' to int."""
    s = str(s).strip()
    if '万' in s:
        return int(float(s.replace('万', '')) * 10000)
    try:
        return int(s)
    except Exception:
        return 0


def load_data(data_dir: Path):
    """Load notes and comments from JSON files."""
    notes, comments = [], []
    for f in sorted(data_dir.glob("*contents*.json")):
        with open(f) as fh:
            notes.extend(json.load(fh))
    for f in sorted(data_dir.glob("*comments*.json")):
        with open(f) as fh:
            comments.extend(json.load(fh))
    return notes, comments


POSITIVE_KW = ['好用', '推荐', '神器', '方便', '喜欢', '太爱了', '效率', '强烈推荐',
               '真香', '好评', '赞', '实用', '惊艳', '解放', '省事', '好棒']
NEGATIVE_KW = ['智商税', '垃圾', '太贵', '不好用', '坑', '退了', '失望', '鸡肋',
               '收费', '割韭菜', '耍流氓', '误触', '不划算', '烂', '吐槽', '差评']
CONCERN_KW = ['隐私', '安全', '收费', '订阅', '会员', '续费', '免费', '额度', '价格', '贵']


def analyze(notes, comments, products_map):
    """Run sentiment analysis and return structured results."""
    results = {}

    # Keyword distribution
    kw_stats = defaultdict(lambda: {"count": 0, "likes": 0, "collects": 0})
    for n in notes:
        kw = n.get("source_keyword", "unknown")
        kw_stats[kw]["count"] += 1
        kw_stats[kw]["likes"] += parse_count(n.get("liked_count", 0))
        kw_stats[kw]["collects"] += parse_count(n.get("collected_count", 0))
    results["keyword_stats"] = dict(kw_stats)

    # Product mentions in comments
    product_mentions = defaultdict(list)
    for c in comments:
        content = c.get("content", "").lower()
        for prod, keywords in products_map.items():
            if any(kw in content for kw in keywords):
                product_mentions[prod].append(c)
    results["product_mentions"] = {k: len(v) for k, v in product_mentions.items()}

    # Sentiment counts
    total = len(comments)
    pos = sum(1 for c in comments if any(kw in c.get("content", "") for kw in POSITIVE_KW))
    neg = sum(1 for c in comments if any(kw in c.get("content", "") for kw in NEGATIVE_KW))
    concern = sum(1 for c in comments if any(kw in c.get("content", "") for kw in CONCERN_KW))
    results["sentiment"] = {
        "total": total, "positive": pos, "negative": neg,
        "concern": concern, "neutral": total - pos - neg
    }

    # Top notes
    sorted_notes = sorted(notes, key=lambda x: -parse_count(x.get("liked_count", 0)))
    results["top_notes"] = [
        {"title": n["title"][:50], "keyword": n.get("source_keyword", ""),
         "likes": n.get("liked_count", 0), "collects": n.get("collected_count", 0),
         "comments": n.get("comment_count", 0)}
        for n in sorted_notes[:15]
    ]

    # Price-related comments sample
    price_comments = [c for c in comments if any(
        kw in c.get("content", "") for kw in ['贵', '收费', '订阅', '会员', '免费', '额度', '价格', '智商税']
    )]
    results["price_comments"] = [
        {"location": c.get("ip_location", "?"),
         "content": c["content"][:100].replace("\n", " ").replace("\r", "")}
        for c in price_comments[:25]
    ]

    # Comparison comments sample
    compare_comments = [c for c in comments if any(
        kw in c.get("content", "").lower() for kw in ['对比', '比较', 'vs', '还是', '哪个好', '选了', '买了', '退了']
    )]
    results["compare_comments"] = [
        {"location": c.get("ip_location", "?"),
         "content": c["content"][:100].replace("\n", " ").replace("\r", "")}
        for c in compare_comments[:25]
    ]

    return results


def generate_report(results, output_path: Path):
    """Generate markdown report from analysis results."""
    lines = ["# 舆情分析报告\n"]

    # Data overview
    s = results["sentiment"]
    lines.append(f"## 数据概览\n")
    lines.append(f"- 评论总数: {s['total']}")
    lines.append(f"- 正面: {s['positive']} ({s['positive']/max(s['total'],1)*100:.1f}%)")
    lines.append(f"- 负面: {s['negative']} ({s['negative']/max(s['total'],1)*100:.1f}%)")
    lines.append(f"- 价格/隐私关切: {s['concern']} ({s['concern']/max(s['total'],1)*100:.1f}%)\n")

    # Keyword stats
    lines.append("## 各关键词热度\n")
    lines.append("| 关键词 | 笔记数 | 总赞 | 总收藏 |")
    lines.append("|---|---|---|---|")
    for kw, st in sorted(results["keyword_stats"].items(), key=lambda x: -x[1]["likes"]):
        lines.append(f"| {kw} | {st['count']} | {st['likes']:,} | {st['collects']:,} |")
    lines.append("")

    # Product mentions
    if results["product_mentions"]:
        lines.append("## 产品提及频次（评论中）\n")
        for prod, cnt in sorted(results["product_mentions"].items(), key=lambda x: -x[1]):
            lines.append(f"- {prod}: {cnt} 条")
        lines.append("")

    # Top notes
    lines.append("## 热门笔记 TOP 15\n")
    for i, n in enumerate(results["top_notes"], 1):
        lines.append(f"{i}. [{n['keyword']}] {n['title']}")
        lines.append(f"   👍{n['likes']} 📁{n['collects']} 💬{n['comments']}")
    lines.append("")

    # Price comments
    if results["price_comments"]:
        lines.append(f"## 定价相关评论（{len(results['price_comments'])}条采样）\n")
        for c in results["price_comments"]:
            lines.append(f"- [{c['location']}] {c['content']}")
        lines.append("")

    # Comparison comments
    if results["compare_comments"]:
        lines.append(f"## 产品对比评论（{len(results['compare_comments'])}条采样）\n")
        for c in results["compare_comments"]:
            lines.append(f"- [{c['location']}] {c['content']}")

    report = "\n".join(lines)
    output_path.write_text(report, encoding="utf-8")
    print(f"Report saved to {output_path}")
    return report


def main():
    parser = argparse.ArgumentParser(description="XHS Sentiment Analyzer")
    parser.add_argument("--data", required=True, help="Data directory with JSON files")
    parser.add_argument("--products", default="", help="Product mapping JSON file or inline JSON")
    parser.add_argument("--output", default="report.md", help="Output report path")
    args = parser.parse_args()

    data_dir = Path(args.data)
    notes, comments = load_data(data_dir)
    print(f"Loaded {len(notes)} notes, {len(comments)} comments")

    # Parse products map
    products_map = {}
    if args.products:
        p = Path(args.products)
        if p.exists():
            products_map = json.loads(p.read_text())
        else:
            try:
                products_map = json.loads(args.products)
            except json.JSONDecodeError:
                print(f"Warning: Could not parse products map, skipping product analysis")

    results = analyze(notes, comments, products_map)

    # Output JSON results to stdout
    print(json.dumps(results, ensure_ascii=False, indent=2))

    # Generate markdown report
    generate_report(results, Path(args.output))


if __name__ == "__main__":
    main()
