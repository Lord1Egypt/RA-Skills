
#!/usr/bin/env python3
"""
读取微信公众号文章
用法: python read.py "微信文章URL" [--mode MODE] [--screenshot PATH]
模式: simple|playwright|auto (默认auto)
"""

import sys
import os
import argparse

# 添加脚本路径
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)

from wechat_articles import read_article, print_article_content


def main():
    parser = argparse.ArgumentParser(description="读取微信公众号文章")
    parser.add_argument("url", help="微信文章URL")
    parser.add_argument("--mode", "-m", default="auto", 
                        choices=["simple", "playwright", "auto"],
                        help="读取模式 (默认: auto)")
    parser.add_argument("--screenshot", "-s", help="Playwright模式下截图保存路径")
    parser.add_argument("--max-paragraphs", "-n", type=int, default=50,
                        help="显示的最大段落数 (默认: 50)")
    
    args = parser.parse_args()
    
    print(f"正在读取文章...")
    print(f"URL: {args.url[:80]}...")
    print(f"模式: {args.mode}")
    if args.screenshot:
        print(f"截图: {args.screenshot}")
    print()
    
    try:
        content = read_article(args.url, mode=args.mode, screenshot_path=args.screenshot)
        print_article_content(content, max_paragraphs=args.max_paragraphs)
    except Exception as e:
        print(f"错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
