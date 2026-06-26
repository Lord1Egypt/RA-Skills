#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
跨境电商资讯 skill 统一入口

流程：
  Step 1: fetch_news.py → enews + cifnews 抓取 → 权重排序 → Top 10 → 初始 JSON
  Step 2: AI Agent 读取需要摘要的 cifnews 文章 → 生成 LLM 摘要 → 更新 JSON + Markdown
  Step 3: 输出分源文件（enews_*.md / cifnews_*.md）

用法：
  python run.py                    # 完整流程
  python run.py --python-only      # 仅 Step 1，不调用 LLM
"""
import argparse
import json
import os
import subprocess
import sys
import urllib.request
import ssl
import re
from datetime import datetime

# Windows 中文控制台 UTF-8 修复
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_DIR = os.path.dirname(SCRIPT_DIR)
OUTPUT_DIR = os.path.join(SKILL_DIR, "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)


def step1_fetch():
    """Step 1: 运行 fetch_news.py 获取初始数据"""
    print("=" * 50)
    print("Step 1: Python 抓取 enews + cifnews")
    print("=" * 50)
    result = subprocess.run(
        [sys.executable, os.path.join(SCRIPT_DIR, "fetch_news.py")],
        cwd=SCRIPT_DIR
    )
    if result.returncode != 0:
        print(f"fetch_news.py 执行失败 (exit {result.returncode})")
        sys.exit(result.returncode)
    print("Step 1 完成\n")


def step2_prepare_for_llm():
    """Step 2 准备：抓取需要摘要的 cifnews 文章全文，写入中间文件供 AI Agent 参考

    此函数输出一个 JSON 文件，包含需要 LLM 生成摘要的文章信息：
    - 文章标题、URL、正文内容
    AI Agent 读取此文件，生成摘要，再由 update_json_with_llm_summaries() 更新到最终 JSON。
    """
    print("=" * 50)
    print("Step 2: 准备 cifnews 文章全文（供 AI Agent 生成摘要）")
    print("=" * 50)

    date_str = datetime.now().strftime("%Y%m%d")
    json_path = os.path.join(OUTPUT_DIR, f"news_report_{date_str}.json")

    if not os.path.exists(json_path):
        print(f"找不到 JSON 文件: {json_path}")
        return None

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    cifnews_articles = [
        item for item in data["data"]
        if item.get("source") == "cifnews"
    ]

    if not cifnews_articles:
        print("Top 10 中无 cifnews 文章，跳过")
        return None

    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    llm_input = []
    for item in cifnews_articles:
        url = item.get("url", "")
        title = item.get("title", "")
        print(f"  抓取: {title[:40]}...")

        full_text = ""
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=10, context=ctx) as r:
                raw = r.read()
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
                if len(parts) >= 8:
                    break
            full_text = '\n'.join(parts)
        except Exception as e:
            print(f"    抓取失败: {e}")

        llm_input.append({
            "title": title,
            "url": url,
            "full_text": full_text,
            "current_description": item.get("description", ""),
        })
        print(f"    正文字数: {len(full_text)}")

    # 写入中间文件
    llm_input_path = os.path.join(OUTPUT_DIR, f"llm_input_{date_str}.json")
    with open(llm_input_path, "w", encoding="utf-8") as f:
        json.dump({
            "date": date_str,
            "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "articles": llm_input,
        }, f, ensure_ascii=False, indent=2)

    print(f"\nStep 2 准备完成: {len(llm_input)} 篇 cifnews 文章已写入")
    print(f"  中间文件: {llm_input_path}")
    print("\nAI Agent 接下来需要：")
    print("  1. 读取 llm_input_*.json")
    print("  2. 为每篇文章生成 50 字以内中文摘要")
    print("  3. 调用 update_json_with_llm_summaries() 更新 JSON + Markdown\n")
    return llm_input_path


def update_json_with_llm_summaries(llm_summaries: dict):
    """将 AI Agent 生成的摘要更新到 JSON 和 Markdown

    Args:
        llm_summaries: {url: summary_text, ...}
    """
    print("=" * 50)
    print("Step 2: 更新 LLM 摘要到 JSON")
    print("=" * 50)

    date_str = datetime.now().strftime("%Y%m%d")
    json_path = os.path.join(OUTPUT_DIR, f"news_report_{date_str}.json")
    llm_input_path = os.path.join(OUTPUT_DIR, f"llm_input_{date_str}.json")

    if not os.path.exists(json_path):
        print(f"找不到 JSON 文件")
        return

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    updated = 0
    for item in data["data"]:
        url = item.get("url", "")
        if url in llm_summaries and item.get("source") == "cifnews":
            item["description"] = llm_summaries[url]
            item["summary_type"] = "llm"
            updated += 1

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"已更新 {updated} 篇 cifnews 摘要到 JSON")

    # 重建 Markdown
    news_data = data["data"]
    lines = ["# 跨境电商热点资讯\n"]
    lines.append(f"**获取时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    lines.append(f"**数据来源**: ennews / cifnews\n")
    lines.append(f"**当日资讯数量**: {len(news_data)} 条（LLM 摘要）\n\n")

    for i, item in enumerate(news_data, 1):
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

    md_path = os.path.join(OUTPUT_DIR, f"news_report_{date_str}.md")
    with open(md_path, "w", encoding="utf-8") as f:
        f.write("".join(lines))
    print(f"Markdown 已更新: {md_path}")

    # 删除中间文件
    if os.path.exists(llm_input_path):
        os.remove(llm_input_path)
        print(f"已清理中间文件: {llm_input_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="跨境电商资讯 skill")
    parser.add_argument("--python-only", action="store_true",
                        help="仅运行 Step 1（Python 抓取），不调用 LLM")
    parser.add_argument("--update-summaries", metavar="JSON",
                        help="将 LLM 摘要批量更新到 JSON（AI Agent 调用）")
    args = parser.parse_args()

    # AI Agent 批量更新摘要的入口
    if args.update_summaries:
        summaries_path = args.update_summaries
        with open(summaries_path, "r", encoding="utf-8") as f:
            summaries_data = json.load(f)
        # summaries_data 格式: {"date": "...", "summaries": {"url": "summary", ...}}
        llm_summaries = summaries_data.get("summaries", {})
        update_json_with_llm_summaries(llm_summaries)
        sys.exit(0)

    # 正常流程
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Step 1: Python 抓取（必须）
    step1_fetch()

    if not args.python_only:
        # Step 2: 准备 cifnews 全文，写入中间文件
        llm_input_path = step2_prepare_for_llm()
        if llm_input_path:
            print("=" * 50)
            print("请 AI Agent 根据 llm_input_* 文件生成摘要")
            print("完成后调用：")
            print(f"  python run.py --update-summaries {llm_input_path}")
            print("=" * 50)
    else:
        print("=" * 50)
        print("完成（python-only 模式，跳过 LLM 摘要）")
        print("=" * 50)
