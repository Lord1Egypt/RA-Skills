#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
内容抓取脚本 (crawl4ai版)
读取 JSON 文件中的 url，用 crawl4ai 抓取正文 Markdown。

- 不指定 --output: 将 content 回写到原 JSON 文件中
- 指定 --output:    将抓取结果单独保存到指定文件

支持传入单个 JSON 文件或一个包含 JSON 文件的目录。

用法:
  python fetch_site_content.py <文件.json>
  python fetch_site_content.py <文件.json> --output /tmp/result.json
  python fetch_site_content.py <目录路径>
  python fetch_site_content.py <目录路径> --force --top 10
"""

import json
import os
import sys
import asyncio
import time
import argparse
import glob
from datetime import datetime
from tqdm import tqdm


# ========== crawl4ai 抓取 ==========

async def _fetch_with_crawl4ai(url):
    """使用 crawl4ai 异步抓取页面"""
    from crawl4ai import AsyncWebCrawler, CrawlerRunConfig

    config = CrawlerRunConfig(magic=True)

    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(url=url, config=config)

        if result.success:
            return {'url': url, 'content': result.markdown, 'error': None}
        else:
            return {'url': url, 'content': '', 'error': result.error_message}


def fetch_content(url):
    """同步调用 crawl4ai 抓取"""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        result = loop.run_until_complete(_fetch_with_crawl4ai(url))
    finally:
        loop.close()

    # 微信链接额外等待
    if 'weixin.qq.com' in url or 'wechat.com' in url:
        time.sleep(2)

    return result


# ========== 单文件处理 ==========

def process_single_file(filepath, output_path=None):
    """处理单个 JSON 文件：抓取 url 对应的正文内容

    Args:
        filepath: 输入的 JSON 文件路径
        output_path: 输出路径。None 表示回写到原文件的 content 字段
    """
    filepath = os.path.abspath(filepath)

    if not os.path.isfile(filepath):
        print(f"错误: 文件不存在 '{filepath}'")
        return

    # 读取 JSON
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        print(f"错误: 无法读取文件 '{filepath}' ({e})")
        return

    url = data.get('url', '')
    title = data.get('title', '未知标题')

    if not url:
        print(f"错误: 文件中没有 url 字段 '{filepath}'")
        return

    print(f"抓取: {title}")
    print(f"URL: {url}")

    # 抓取内容
    result = fetch_content(url)

    if result.get('error'):
        print(f"抓取失败: {result['error']}")
    else:
        content_len = len(result.get('content', ''))
        print(f"抓取成功: {content_len} 字符")

    if output_path:
        # 有 --output: 单独保存到指定文件
        output_path = os.path.abspath(output_path)
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        output_data = {
            'title': title,
            'description': data.get('description', ''),
            'url': url,
            'fetched_at': datetime.now().isoformat(),
            'content': result.get('content', ''),
            'error': result.get('error'),
        }

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2)

        print(f"已保存到: {output_path}")
    else:
        # 无 --output: 回写到原文件的 content 字段
        data['content'] = result.get('content', '')
        data['error'] = result.get('error')
        data['fetched_at'] = datetime.now().isoformat()

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        print(f"已保存到: {filepath} [content]")


# ========== 目录批量处理 ==========

def process_directory(directory, output_path=None, force=False, top_n=None):
    """处理目录下的所有 JSON 文件"""

    directory = os.path.abspath(directory)

    if not os.path.isdir(directory):
        print(f"错误: 目录不存在 '{directory}'")
        return

    json_files = sorted(glob.glob(os.path.join(directory, '*.json')))
    if not json_files:
        print(f"目录下没有 JSON 文件: {directory}")
        return

    dir_name = os.path.basename(os.path.normpath(directory))
    print(f"目录: {directory} ({len(json_files)} 个文件)")

    # 筛选需要处理的文件
    todo = []
    skip_count = 0
    for fp in json_files:
        try:
            with open(fp, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            print(f"跳过无效文件: {os.path.basename(fp)} ({e})")
            continue

        url = data.get('url', '')
        if not url:
            continue

        # 非强制模式下，跳过已有内容的文件
        if not force and data.get('content'):
            skip_count += 1
            continue

        todo.append((fp, data))

    if skip_count > 0:
        print(f"跳过已有内容: {skip_count} 个 (使用 --force 强制重新抓取)")

    if not todo:
        print("没有需要处理的文件")
        return

    # 截取 top_n
    if top_n and top_n < len(todo):
        todo = todo[:top_n]
        print(f"取前 {top_n} 个")

    # 如果指定了 output 目录，确保存在
    if output_path:
        output_path = os.path.abspath(output_path)
        os.makedirs(output_path, exist_ok=True)

    print(f"待抓取: {len(todo)} 个\n")

    success_count = 0
    fail_count = 0

    for fp, data in tqdm(todo, desc=f"抓取 {dir_name}", unit="条"):
        url = data['url']
        result = fetch_content(url)

        if result.get('error'):
            fail_count += 1
        else:
            success_count += 1

        if output_path:
            # 有 --output: 每个文件单独保存到 output 目录下同名文件
            output_data = {
                'title': data.get('title', ''),
                'description': data.get('description', ''),
                'url': url,
                'fetched_at': datetime.now().isoformat(),
                'content': result.get('content', ''),
                'error': result.get('error'),
            }
            out_fp = os.path.join(output_path, os.path.basename(fp))
            with open(out_fp, 'w', encoding='utf-8') as f:
                json.dump(output_data, f, ensure_ascii=False, indent=2)
        else:
            # 无 --output: 回写到原文件
            data['content'] = result.get('content', '')
            data['error'] = result.get('error')
            data['fetched_at'] = datetime.now().isoformat()

            with open(fp, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

        time.sleep(1)

    print(f"\n完成! 成功: {success_count}, 失败: {fail_count}")
    if output_path:
        print(f"已保存到: {output_path}")
    else:
        print(f"已回写到: {directory} 下各文件的 [content] 字段")


# ========== 入口 ==========

def main():
    parser = argparse.ArgumentParser(
        description='抓取 JSON 文件中 url 的正文内容 (crawl4ai)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例 (单文件):
  python fetch_site_content.py ./site_contents/zhi_hu/如何评价xxx.json
  python fetch_site_content.py ./site_contents/zhi_hu/如何评价xxx.json -o /tmp/result.json

示例 (目录批量):
  python fetch_site_content.py ./site_contents/zhi_hu
  python fetch_site_content.py ./site_contents/zhi_hu --force --top 5
        """
    )
    parser.add_argument('input', nargs='?', help='JSON 文件路径 或 包含 JSON 文件的目录路径')
    parser.add_argument('--output', '-o', default=None, help='输出路径 (单文件时为文件路径, 目录时为目录路径)。不指定则回写到原文件')
    parser.add_argument('--force', '-f', action='store_true', help='[目录模式] 强制重新抓取已有内容的文件')
    parser.add_argument('--top', '-n', type=int, default=None, help='[目录模式] 只处理前 N 个文件')

    args = parser.parse_args()

    if not args.input:
        parser.print_help()
        return

    input_path = args.input

    if os.path.isfile(input_path):
        # 单文件模式
        process_single_file(input_path, output_path=args.output)
    elif os.path.isdir(input_path):
        # 目录批量模式
        process_directory(input_path, output_path=args.output, force=args.force, top_n=args.top)
    else:
        print(f"错误: 路径不存在 '{input_path}'")


if __name__ == '__main__':
    main()
