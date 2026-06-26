#!/usr/bin/env python3
"""
围棋分享棋谱下载器 - 从分享链接自动下载SGF棋谱
"""

import sys
import argparse
import os

# 添加脚本目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sources import get_fetcher_for_url, get_fetcher_by_name, list_fetchers

def print_banner():
    print("=" * 60)
    print("🎯 围棋分享棋谱下载器")
    print("=" * 60)

def print_result(result):
    """打印下载结果"""
    print()
    if result.success:
        print(f"✅ 下载成功！")
        print()
        print(f"🌐 来源: {result.source}")
        print(f"🔗 URL: {result.url}")
        print()
        print("📋 对局信息:")
        meta = result.metadata
        if 'black_name' in meta:
            rank = f" {meta.get('black_rank', '')}" if meta.get('black_rank') else ""
            print(f"  黑棋: {meta['black_name']}{rank}")
        if 'white_name' in meta:
            rank = f" {meta.get('white_rank', '')}" if meta.get('white_rank') else ""
            print(f"  白棋: {meta['white_name']}{rank}")
        if 'rules' in meta:
            print(f"  规则: {meta['rules']}")
        if 'komi' in meta:
            print(f"  贴目: {meta['komi']}")
        if 'handicap' in meta and meta['handicap'] > 0:
            print(f"  让子: {meta['handicap']}")
        if 'moves_count' in meta:
            print(f"  手数: {meta['moves_count']}")
        if 'result' in meta:
            print(f"  结果: {meta['result']}")
        if 'date' in meta and meta['date']:
            print(f"  日期: {meta['date']}")
        print()
        print(f"💾 文件保存: {result.output_path}")
        
        # 性能统计
        if result.timing:
            print()
            print("⏱️ 性能统计:")
            total = 0
            for key, val in result.timing.items():
                print(f"  {key:20s}: {val:.3f}s")
                total += val
            print(f"  {'总计':20s}: {total:.3f}s")
    else:
        print(f"❌ 下载失败: {result.error}")
    
    print()
    print("=" * 60)

def list_sources():
    """列出所有支持的来源"""
    print()
    print("支持的棋谱来源:")
    print()
    for name, display_name, examples in list_fetchers():
        print(f"  [{name}]")
        print(f"    名称: {display_name}")
        if examples:
            print(f"    示例: {examples[0]}")
        print()

def main():
    parser = argparse.ArgumentParser(
        description='围棋分享棋谱下载器 - 支持OGS、野狐围棋等平台',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python3 main.py "https://online-go.com/game/{GAME_ID}"
  python3 main.py "https://h5.foxwq.com/yehunewshare/?chessid={CHESS_ID}"
  python3 main.py "{URL}" -o /path/to/output.sgf
  python3 main.py --list-sources
        """
    )
    parser.add_argument('url', nargs='?', help='棋谱分享链接')
    parser.add_argument('-o', '--output', help='输出文件路径（可选）')
    parser.add_argument('-s', '--source', help='强制指定来源（可选）')
    parser.add_argument('-l', '--list-sources', action='store_true', help='列出支持的来源')
    parser.add_argument('--silent', action='store_true', help='静默模式，只输出文件路径')
    
    args = parser.parse_args()
    
    if args.list_sources:
        print_banner()
        list_sources()
        return
    
    if not args.url:
        parser.print_help()
        sys.exit(1)
    
    if not args.silent:
        print_banner()
        print()
    
    # 自动识别或强制指定来源
    if args.source:
        fetcher = get_fetcher_by_name(args.source)
        if not fetcher:
            print(f"❌ 未知的来源: {args.source}")
            print("使用 --list-sources 查看支持的来源")
            sys.exit(1)
    else:
        fetcher = get_fetcher_for_url(args.url)
        if not fetcher:
            print(f"❌ 不支持该URL: {args.url}")
            print("使用 --list-sources 查看支持的来源")
            sys.exit(1)
    
    if not args.silent:
        print(f"🌐 识别到来源: {fetcher.display_name}")
    
    # 执行下载
    result = fetcher.fetch(args.url, args.output)
    
    if args.silent:
        if result.success:
            print(result.output_path)
        else:
            print(f"ERROR: {result.error}", file=sys.stderr)
            sys.exit(1)
    else:
        print_result(result)
        
        if not result.success:
            sys.exit(1)

if __name__ == '__main__':
    main()
