#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
auto_publish.py - 一键自动发布到小红书
流程：生成内容 → 生成封面图 → 发布
"""

import sys
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import generate_content
import generate_cover
from publish import publish


def main():
    parser = argparse.ArgumentParser(description="一键发布到小红书")
    parser.add_argument("--topic", default="科技", help="话题/主题（如：美食、旅游、穿搭、科技、生活、健身）")
    parser.add_argument("--title", default=None, help="自定义标题（<20字，不填则自动生成）")
    parser.add_argument("--content", default=None, help="自定义正文（不填则自动生成）")
    parser.add_argument("--cover-text", default=None, help="封面图文字（不填则用标题）")
    parser.add_argument("--image", default=None, nargs="*", help="使用已有图片路径（可多张，跳过图片生成）")
    parser.add_argument("--count", type=int, default=3, help="生成图片数量（默认3张）")
    parser.add_argument("--profile-dir", default=None, help="浏览器 profile 目录（不设则用临时目录，登录态不保留）")
    args = parser.parse_args()

    # Step 1: Generate content
    if args.title and args.content:
        title = args.title[:20]
        content = args.content
        print(f"[INFO] 使用自定义内容")
    else:
        print(f"[INFO] 自动生成内容，话题: {args.topic}")
        data = generate_content.generate_content(args.topic)
        title = args.title or data["title"]
        content = args.content or data["content"]

    title = title[:20]
    print(f"[标题] {title}")
    print(f"[正文] {content[:60]}...")

    # Step 2: Generate or use existing images
    if args.image:
        image_paths = [Path(p) for p in args.image]
        for p in image_paths:
            if not p.exists():
                print(f"[ERROR] 图片不存在: {p}")
                sys.exit(1)
        print(f"[INFO] 使用已有图片: {len(image_paths)} 张")
    else:
        cover_text = args.cover_text or title
        print(f"[INFO] 生成 {args.count} 张封面图，文字: {cover_text}")
        try:
            image_paths = [Path(p) for p in generate_cover.generate(text_fallback=cover_text, count=args.count)]
            print(f"[INFO] 封面图生成完成: {len(image_paths)} 张")
        except Exception as e:
            print(f"[ERROR] 封面图生成失败: {e}")
            sys.exit(1)

    # Step 3: Publish
    print("[INFO] 开始发布流程...")
    try:
        publish(content, image_paths, title, profile_dir=args.profile_dir)
        print("\n[SUCCESS] 发布完成！")
    except Exception as e:
        print(f"\n[ERROR] 发布失败: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
