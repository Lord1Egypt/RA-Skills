#!/usr/bin/env python3
"""
deep-research v2 — Agent-Assisted 搜索编排引擎

设计理念：脚本不直接调搜索 API，而是生成工具调用指令让 agent 执行。
整个流程：脚本出指令 → agent 执行工具 → 结果喂回脚本 → 脚本出报告。

用法:
  # Step 1: 生成研究计划 + 搜索指令
  python3 research.py plan "Amazon MSK" --depth standard --out plan.json

  # Step 2: Agent 执行 web_search，把结果存入 JSON
  # (agent 读 plan.json 中的 search_commands，逐一执行 web_search)

  # Step 3: 喂搜索结果，脚本做去重+排序+选出要 fetch 的 URL
  python3 research.py analyze search-results.json --top 8 --out fetch-plan.json

  # Step 4: Agent 执行 web_fetch，结果存入 JSON
  # (agent 读 fetch-plan.json 中的 urls)

  # Step 5: 喂抓取结果，脚本生成报告骨架
  python3 research.py report --topic "Amazon MSK" --search search-results.json \
    --fetch fetch-results.json --depth standard --out report.md

  # 或者一步到位生成所有指令:
  python3 research.py plan "Amazon MSK" --depth deep
  # → 输出 JSON，agent 自行编排执行
"""

import argparse
import hashlib
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse


# ─── Config ───────────────────────────────────────────────────────
RESEARCH_DIR = Path(os.environ.get("RESEARCH_DIR",
    os.path.expanduser("~/.openclaw/workspace/research")))

SEARCH_COUNT = int(os.environ.get("SEARCH_COUNT", "8"))
FETCH_MAX_CHARS = int(os.environ.get("FETCH_MAX_CHARS", "20000"))


# ─── Source Authority ─────────────────────────────────────────────

TIER1_DOMAINS = {
    "docs.aws.amazon.com", "cloud.google.com", "learn.microsoft.com",
    "kubernetes.io", "kafka.apache.org", "postgresql.org", "mysql.com",
    "arxiv.org", "github.com", "rfc-editor.org", "prometheus.io",
    "docs.docker.com", "go.dev", "python.org", "rust-lang.org",
    "developer.mozilla.org", "tc39.es", "w3.org",
}
TIER2_DOMAINS = {
    "stackoverflow.com", "engineering.fb.com", "netflixtechblog.com",
    "aws.amazon.com", "blog.cloudflare.com", "thenewstack.io",
    "infoq.com", "martinfowler.com", "highscalability.com",
    "confluent.io", "cockroachlabs.com", "planetscale.com",
    "elastic.co", "redis.io", "grafana.com",
}


def domain(url: str) -> str:
    try:
        return urlparse(url).netloc.lower().replace("www.", "")
    except Exception:
        return ""


def source_tier(url: str) -> int:
    d = domain(url)
    if d in TIER1_DOMAINS or d.endswith(".gov") or d.endswith(".edu"):
        return 1
    if d in TIER2_DOMAINS:
        return 2
    # 营销页面检测
    if any(kw in url.lower() for kw in ["/pricing", "/vs-", "/compare", "/landing"]):
        return 3  # 可能是营销内容
    return 3


def url_hash(url: str) -> str:
    return hashlib.md5(url.encode()).hexdigest()[:10]


def slug(text: str) -> str:
    s = re.sub(r'[^\w\s-]', '', text.lower().strip())
    return re.sub(r'[\s_]+', '-', s)[:50]


def now_str() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")


def today_str() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%d")


# ─── Plan: 生成研究计划 ──────────────────────────────────────────

def make_plan(topic: str, depth: str = "standard", lang: str = "zh") -> dict:
    """生成研究计划：子问题 + 搜索指令列表."""

    # 子问题模板
    if depth == "quick":
        sub_qs = [topic]
    elif depth == "standard":
        sub_qs = [
            f"{topic} overview architecture key concepts",
            f"{topic} latest features updates 2025 2026",
            f"{topic} best practices common issues pitfalls",
            f"{topic} vs alternatives comparison pros cons",
        ]
    else:  # deep
        sub_qs = [
            f"{topic} architecture internals deep dive",
            f"{topic} new features 2025 2026 changelog",
            f"{topic} performance benchmarks throughput latency",
            f"{topic} known issues limitations bugs",
            f"{topic} vs competitors comparison",
            f"{topic} production experience real world case study",
            f"problems with {topic} why not use criticism",
        ]

    # 如果是中文 topic，额外加中文搜索词
    has_chinese = bool(re.search(r'[\u4e00-\u9fff]', topic))
    cn_queries = []
    if not has_chinese and depth != "quick":
        # 英文 topic 加一个中文搜索
        cn_queries = [f"{topic} 教程 最佳实践 踩坑"]
    elif has_chinese and depth != "quick":
        # 中文 topic 加一个英文搜索
        cn_queries = [f"{topic} tutorial best practices"]

    all_queries = sub_qs + cn_queries

    # 生成 agent 工具调用指令
    search_commands = []
    for i, q in enumerate(all_queries):
        search_commands.append({
            "id": f"s{i+1}",
            "tool": "web_search",
            "params": {"query": q, "count": SEARCH_COUNT},
        })

    config = {
        "quick":    {"max_fetches": 2,  "rounds": 1},
        "standard": {"max_fetches": 8,  "rounds": 1},
        "deep":     {"max_fetches": 15, "rounds": 2},
    }

    return {
        "topic": topic,
        "depth": depth,
        "lang": lang,
        "created": now_str(),
        "sub_questions": sub_qs,
        "search_commands": search_commands,
        "config": config.get(depth, config["standard"]),
        "instructions": (
            "Agent: 执行上面每个 search_commands 中的 web_search 工具调用。\n"
            "收集所有结果后，运行:\n"
            f"  python3 research.py analyze <results.json> --top {config.get(depth, config['standard'])['max_fetches']}\n"
            "然后对输出的 URLs 执行 web_fetch，最后运行:\n"
            "  python3 research.py report --topic '...' --search <search.json> --fetch <fetch.json>"
        ),
    }


# ─── Analyze: 搜索结果去重+排序 ──────────────────────────────────

def analyze_results(results: list[dict], top_n: int = 8) -> dict:
    """对搜索结果去重、分级、排序，输出要 fetch 的 URL 列表.
    
    输入格式 (agent 收集的搜索结果):
    [
      {"query": "...", "results": [{"title": "...", "url": "...", "snippet": "..."}, ...]},
      ...
    ]
    """
    seen_hashes = set()
    all_items = []

    for group in results:
        query = group.get("query", "")
        for r in group.get("results", []):
            url = r.get("url", "")
            if not url:
                continue
            h = url_hash(url)
            if h in seen_hashes:
                continue
            seen_hashes.add(h)
            tier = source_tier(url)
            all_items.append({
                "title": r.get("title", ""),
                "url": url,
                "snippet": r.get("snippet", "")[:300],
                "domain": domain(url),
                "tier": tier,
                "query": query,
                "hash": h,
            })

    # 排序: tier 优先（小 = 好），然后按出现顺序
    all_items.sort(key=lambda x: x["tier"])

    # 域名多样性：同域名最多取 3 个
    domain_count = {}
    diverse = []
    for item in all_items:
        d = item["domain"]
        domain_count[d] = domain_count.get(d, 0) + 1
        if domain_count[d] <= 3:
            diverse.append(item)

    selected = diverse[:top_n]
    remaining = diverse[top_n:]

    # 生成 fetch 指令
    fetch_commands = []
    for i, item in enumerate(selected):
        fetch_commands.append({
            "id": f"f{i+1}",
            "tool": "web_fetch",
            "params": {"url": item["url"], "maxChars": FETCH_MAX_CHARS},
        })

    tier_emoji = {1: "🟢", 2: "🟡", 3: "🟠", 4: "🔴"}
    summary_lines = []
    for i, item in enumerate(selected, 1):
        t = tier_emoji.get(item["tier"], "🟠")
        summary_lines.append(f"  [{i}] {t} T{item['tier']} {item['domain']} — {item['title'][:60]}")

    return {
        "total_found": len(all_items),
        "unique_urls": len(seen_hashes),
        "selected": len(selected),
        "remaining": len(remaining),
        "fetch_commands": fetch_commands,
        "selected_sources": selected,
        "summary": "\n".join(summary_lines),
        "instructions": (
            f"Agent: 执行上面 {len(fetch_commands)} 个 web_fetch 调用。\n"
            "收集结果后运行 report 命令生成最终报告。"
        ),
    }


# ─── Report: 生成报告 ─────────────────────────────────────────────

def generate_report(topic: str, depth: str, search_data: list[dict],
                    fetch_data: list[dict], lang: str = "zh") -> str:
    """从搜索+抓取结果生成完整报告框架.
    
    search_data: analyze 输出的 selected_sources
    fetch_data: [{"url": "...", "text": "...", "length": N}, ...]
    """
    date = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    tier_emoji = {1: "🟢", 2: "🟡", 3: "🟠", 4: "🔴"}

    # 匹配 fetch 内容到 source
    url_to_text = {}
    for f in fetch_data:
        url = f.get("url", "")
        text = f.get("text", f.get("content", ""))
        if url and text:
            url_to_text[url] = text[:FETCH_MAX_CHARS]

    # Sources 表
    sources_section = ""
    for i, s in enumerate(search_data, 1):
        tier = s.get("tier", 3)
        emoji = tier_emoji.get(tier, "🟠")
        title = s.get("title", "Unknown")[:80]
        url = s.get("url", "")
        sources_section += f"[{i}] {title} — {url} — Tier {tier} {emoji}\n"

    # 页面文本摘要（供 agent 分析用）
    content_section = ""
    for i, s in enumerate(search_data, 1):
        url = s.get("url", "")
        text = url_to_text.get(url, "")
        if text:
            # 取前 2000 字符作为摘要
            preview = text[:2000].replace("\n", " ").strip()
            content_section += f"\n### Source [{i}] — {s.get('domain', '')}\n\n{preview}\n"

    n_sources = len(search_data)
    n_fetched = len([u for u in url_to_text if u])

    report = f"""# {topic}

> 🔬 Deep Research | {date} | {n_sources} sources ({n_fetched} fetched) | Depth: {depth}
> Confidence: {{FILL: 🟢 High / 🟡 Medium / 🔴 Low}}

## Executive Summary

{{FILL: 3-5 句总结核心发现}}

## Key Findings

{{FILL: Agent 基于下面的 Source Content 分析填写}}

## Conflicting Information

{{FILL: 来源之间的矛盾，或写 "无明显矛盾"}}

## Confidence Assessment

| Finding | Confidence | Sources | Notes |
|---------|-----------|---------|-------|
| {{finding}} | {{level}} | {{refs}} | {{notes}} |

## Sources

{sources_section}
## Source Content (for agent analysis)

{content_section}
"""
    return report


# ─── CLI ──────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="deep-research v2 — Agent-Assisted 搜索编排引擎",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
工作流:
  1. plan   → 生成搜索指令 → agent 执行 web_search
  2. analyze → 去重排序 → 生成 fetch 指令 → agent 执行 web_fetch  
  3. report  → 从搜索+抓取结果生成报告骨架 → agent 填充分析
        """)
    sub = parser.add_subparsers(dest="cmd")

    # plan
    p = sub.add_parser("plan", help="生成研究计划和搜索指令")
    p.add_argument("topic")
    p.add_argument("--depth", choices=["quick", "standard", "deep"], default="standard")
    p.add_argument("--lang", default="zh")
    p.add_argument("--out", help="输出到文件")

    # analyze
    a = sub.add_parser("analyze", help="分析搜索结果，输出 fetch 指令")
    a.add_argument("results_file", help="搜索结果 JSON")
    a.add_argument("--top", type=int, default=8, help="选取 top N URLs 去 fetch")
    a.add_argument("--out", help="输出到文件")

    # report
    r = sub.add_parser("report", help="从搜索+抓取结果生成报告")
    r.add_argument("--topic", required=True)
    r.add_argument("--search", required=True, help="analyze 输出的 JSON（含 selected_sources）")
    r.add_argument("--fetch", required=True, help="fetch 结果 JSON")
    r.add_argument("--depth", choices=["quick", "standard", "deep"], default="standard")
    r.add_argument("--lang", default="zh")
    r.add_argument("--out", help="输出到文件")
    r.add_argument("--save", action="store_true", help="同时保存到 research/ 目录")

    args = parser.parse_args()
    if not args.cmd:
        parser.print_help()
        sys.exit(1)

    if args.cmd == "plan":
        result = make_plan(args.topic, args.depth, args.lang)
        output = json.dumps(result, ensure_ascii=False, indent=2)
        if args.out:
            Path(args.out).write_text(output, encoding="utf-8")
            print(f"✅ Plan saved to {args.out}", file=sys.stderr)
        print(output)

    elif args.cmd == "analyze":
        with open(args.results_file, encoding="utf-8") as f:
            data = json.load(f)
        result = analyze_results(data, args.top)
        output = json.dumps(result, ensure_ascii=False, indent=2)
        if args.out:
            Path(args.out).write_text(output, encoding="utf-8")
            print(f"✅ Analysis saved to {args.out}", file=sys.stderr)
        print(output)

    elif args.cmd == "report":
        with open(args.search, encoding="utf-8") as f:
            search_raw = json.load(f)
        with open(args.fetch, encoding="utf-8") as f:
            fetch_data = json.load(f)
        
        # search 可能是 analyze 输出（有 selected_sources）或直接的源列表
        if isinstance(search_raw, dict) and "selected_sources" in search_raw:
            search_data = search_raw["selected_sources"]
        elif isinstance(search_raw, list):
            search_data = search_raw
        else:
            search_data = search_raw.get("results", [])

        report = generate_report(args.topic, args.depth, search_data, fetch_data, args.lang)
        
        if args.out:
            Path(args.out).write_text(report, encoding="utf-8")
            print(f"✅ Report saved to {args.out}", file=sys.stderr)
        if args.save:
            RESEARCH_DIR.mkdir(parents=True, exist_ok=True)
            fp = RESEARCH_DIR / f"{slug(args.topic)}-{today_str()}.md"
            fp.write_text(report, encoding="utf-8")
            print(f"📄 Also saved to {fp}", file=sys.stderr)
        
        print(report)


if __name__ == "__main__":
    main()
