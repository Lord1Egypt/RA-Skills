#!/usr/bin/env python3
"""
Save pre-fetched articles (from WebFetch) to Obsidian/Feishu/IMA.
Supports feishu_url (for filename source) and original_url (for IMA routing).

Usage:
  python save_fetched.py --json articles.json
"""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from web_to_all import save_to_obsidian, save_to_feishu, save_to_ima


def main():
    parser = argparse.ArgumentParser(description="Save pre-fetched articles to Obsidian/Feishu/IMA")
    parser.add_argument("--json", required=True, help="JSON file with articles")
    parser.add_argument("--no-feishu", action="store_true")
    parser.add_argument("--no-ima", action="store_true")
    parser.add_argument("--no-obsidian", action="store_true")
    args = parser.parse_args()

    with open(args.json, "r", encoding="utf-8") as f:
        articles = json.load(f)

    print(f"📋 Processing {len(articles)} articles\n")

    results = []
    for i, article in enumerate(articles, 1):
        title = article["title"]
        feishu_url = article.get("feishu_url", "")
        original_url = article.get("original_url")
        keywords = article.get("keywords")  # v3.5.0: 关键信息

        # 获取内容：优先 source_file，其次 content
        if article.get("source_file"):
            with open(article["source_file"], "r", encoding="utf-8") as f:
                content = f.read()
        else:
            content = article.get("content", "")

        print(f"\n{'='*60}")
        print(f"[{i}/{len(articles)}] {title}")
        print(f"Feishu URL: {feishu_url}")
        print(f"Original URL: {original_url or 'N/A'}")
        print(f"Keywords: {keywords or '(fallback to source)'}")
        print(f"Content: {len(content)} chars")
        print(f"{'='*60}")

        result = {"title": title, "feishu_url": feishu_url}

        # 1. Obsidian — 用 feishu_url（文件名来源 = waytoagi）
        obs_path = None
        if not args.no_obsidian:
            try:
                obs_path = save_to_obsidian(content, title, feishu_url, keywords=keywords)
                result["obsidian"] = obs_path
            except Exception as e:
                print(f"⚠️ Obsidian failed: {e}", file=sys.stderr)
                result["obsidian"] = f"FAILED: {e}"

        # 2. Feishu — v3.6.0: 上传 .md 文件到云盘，复用 Obsidian 文件路径
        if not args.no_feishu:
            if obs_path and not str(obs_path).startswith("FAILED"):
                try:
                    feishu_result = save_to_feishu(obs_path, title)
                    result["feishu"] = feishu_result.get("url", "N/A") if feishu_result else "FAILED"
                except Exception as e:
                    print(f"⚠️ Feishu failed: {e}", file=sys.stderr)
                    result["feishu"] = f"FAILED: {e}"
            else:
                print(f"⚠️ Feishu skipped: Obsidian file not available (required as upload source)", file=sys.stderr)
                result["feishu"] = "SKIPPED (no source file)"

        # 3. IMA — 用 original_url（如果有公众号原文，走 import_urls）
        if not args.no_ima:
            try:
                ima_source_url = original_url or feishu_url
                ima_result = save_to_ima(content, title, source_url=ima_source_url)
                result["ima"] = "OK" if ima_result else "FAILED"
            except Exception as e:
                print(f"⚠️ IMA failed: {e}", file=sys.stderr)
                result["ima"] = f"FAILED: {e}"

        results.append(result)

    # Summary
    print(f"\n\n{'='*60}")
    print("📋 SUMMARY")
    print(f"{'='*60}")
    for r in results:
        print(f"\n📄 {r['title']}")
        print(f"   Obsidian: {r.get('obsidian', 'skipped')}")
        print(f"   Feishu:   {r.get('feishu', 'skipped')}")
        print(f"   IMA:      {r.get('ima', 'skipped')}")


if __name__ == "__main__":
    main()
