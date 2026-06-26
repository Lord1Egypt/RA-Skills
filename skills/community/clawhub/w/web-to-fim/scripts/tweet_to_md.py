#!/usr/bin/env python3
"""
Tweet JSON → Structured Markdown Converter

Usage:
  python3 tweet_to_md.py --input <tweet.json> --output <output.md>
  python3 tweet_to_md.py --input <tweet.json>  (prints to stdout)

Input: JSON file from x-tweet-fetcher (fetch_tweet.py)
Output: Well-structured Markdown with metadata header, section headers, and images.
"""

import json
import re
import argparse
import sys
from pathlib import Path


_SECTION_HEADERS = [
    "所有人都在追模型，但跑道选错了",
    "一个被忽视的行业真相",
    "不是「接入」，是「深度适配」",
    "真人短剧赛道，被悄悄解锁了",
    "从抽卡时代到工厂时代",
    "两种模式，两种人。",
    "商业价值",
    "案例背景",
    "技术突破点",
]

_SUBSECTION_PREFIXES = ["1.", "2.", "3.", "4.", "5."]
_EMOJI_HEADERS = ["🎁", "💡", "📊", "🎬", "✅", "⚠️", "🔑", "🎯"]


def _is_section_header(line: str) -> bool:
    stripped = line.strip()
    if stripped in _SECTION_HEADERS:
        return True
    if any(stripped.startswith(p) for p in _SUBSECTION_PREFIXES) and len(stripped) < 80:
        if re.match(r'^[1-5]\.\s+\S', stripped):
            return True
    if any(stripped.startswith(e) for e in _EMOJI_HEADERS) and len(stripped) < 60:
        return True
    return False


def _is_subsection_header(line: str) -> bool:
    stripped = line.strip()
    key_phrases = [
        "更深层的矛盾", "镜头组叙事", "纳米空间引擎", "脚本智能体",
        "视觉导演智能体", "宫格生视频模式", "多参生视频模式",
    ]
    for phrase in key_phrases:
        if phrase in stripped and len(stripped) < 80:
            return True
    return False


def convert_tweet_to_md(data: dict) -> str:
    tweet = data.get("tweet", {})
    article = tweet.get("article", {})
    url = data.get("url", "")
    username = data.get("username", "")

    md_parts = []

    if article.get("title"):
        title = article["title"]
    elif tweet.get("text"):
        title = tweet["text"][:80].split("\n")[0]
    else:
        title = f"Tweet by @{username}"

    md_parts.append(f"# {title}\n")

    author = tweet.get("author", "")
    screen_name = tweet.get("screen_name", username)
    created_at = tweet.get("created_at", "")
    likes = tweet.get("likes", 0)
    retweets = tweet.get("retweets", 0)
    bookmarks = tweet.get("bookmarks", 0)
    views = tweet.get("views", 0)
    replies_count = tweet.get("replies_count", 0)
    is_article = tweet.get("is_article", False)

    md_parts.append(f"> **作者**: {author} (@{screen_name})  ")
    if created_at:
        md_parts.append(f"> **发布时间**: {created_at}  ")
    md_parts.append(f"> **数据**: {likes} 赞 / {retweets} 转发 / {bookmarks} 收藏 / {views} 浏览 / {replies_count} 评论")
    if is_article:
        md_parts.append(f"> **类型**: X 长文（Article）")
    md_parts.append("")

    if article.get("preview_text"):
        md_parts.append(f"> {article['preview_text']}\n")

    md_parts.append("---\n")

    if is_article and article.get("full_text"):
        full_text = article["full_text"]
        lines = full_text.split("\n")

        for line in lines:
            stripped = line.strip()

            if stripped.startswith("![") and "](" in stripped:
                md_parts.append(f"\n{stripped}\n")
                continue

            if not stripped:
                md_parts.append("")
                continue

            if _is_section_header(stripped):
                md_parts.append(f"\n## {stripped}\n")
                continue

            if _is_subsection_header(stripped):
                md_parts.append(f"\n### {stripped}\n")
                continue

            md_parts.append(line)
    else:
        text = tweet.get("text", "")
        if text:
            md_parts.append(text)

    images = article.get("images", [])
    if images:
        md_parts.append("\n---\n")
        md_parts.append("## 附图\n")
        for img in images:
            img_url = img.get("url", "")
            img_type = img.get("type", "image")
            if img_url:
                label = "封面" if img_type == "cover" else "图片"
                md_parts.append(f"![{label}]({img_url})\n")

    replies = data.get("replies", [])
    if replies:
        md_parts.append("\n---\n")
        md_parts.append("## 评论\n")
        for reply in replies:
            reply_author = reply.get("author", "")
            reply_text = reply.get("text", "")
            reply_likes = reply.get("likes", 0)
            md_parts.append(f"**{reply_author}** (♥ {reply_likes}): {reply_text}\n")
            for nested in reply.get("thread_replies", []):
                nested_text = nested.get("text", "")
                nested_likes = nested.get("likes", 0)
                md_parts.append(f"  ↳ {nested_text} (♥ {nested_likes})\n")

    md_parts.append("\n---\n")
    md_parts.append(f"*来源: [{url}]({url})*\n")

    return "\n".join(md_parts)


def main():
    parser = argparse.ArgumentParser(description="Convert tweet JSON to Markdown")
    parser.add_argument("--input", required=True, help="Input JSON file from x-tweet-fetcher")
    parser.add_argument("--output", help="Output Markdown file (default: stdout)")
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: Input file not found: {input_path}", file=sys.stderr)
        sys.exit(1)

    with open(input_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    if "error" in data:
        print(f"Error in input data: {data['error']}", file=sys.stderr)
        sys.exit(1)

    markdown = convert_tweet_to_md(data)

    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(markdown)
        print(f"✅ Markdown saved: {output_path} ({len(markdown)} chars)", file=sys.stderr)
    else:
        print(markdown)


if __name__ == "__main__":
    main()
