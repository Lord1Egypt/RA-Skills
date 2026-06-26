#!/usr/bin/env python3
"""
magnet_search.py - Search torrents via Knaben API (primary) + apibay (fallback/secondary)
version: 1.1.0
"""

import sys
import json
import argparse
import subprocess
from pathlib import Path
from typing import Optional

try:
    import urllib.request
    import urllib.parse
except ImportError:
    print("Error: urllib not available")
    sys.exit(1)

# Common Chinese title to English mapping
TITLE_MAP = {
    '唐探1900': 'Detective Chinatown 1900',
    '唐人街探案1900': 'Detective Chinatown 1900',
    '唐人街探案': 'Detective Chinatown',
    '哪吒2': 'Nezha 2 2025',
    '哪吒之魔童闹海': 'Nezha 2 2025',
    '哪吒': 'Ne Zha',
    '流浪地球': 'The Wandering Earth',
    '流浪地球2': 'The Wandering Earth 2',
    '满江红': 'Full River Red',
    '封神': 'Creation of the Gods',
    '长安三万里': 'Chang An',
    '消失的她': 'Lost in the Stars',
    '孤注一掷': 'No More Bets',
    '三体': 'Three Body Problem',
    '美国队长4': 'Captain America Brave New World',
    '勇敢新世界': 'Captain America Brave New World',
}

KNABEN_API = 'https://api.knaben.org/v1'
APIBAY_API = 'https://apibay.org/q.php'


def search_knaben(query: str, size: int = 10, page: int = 0) -> list:
    """Search Knaben API for torrents."""
    payload = json.dumps({
        'search_type': '70%',
        'search_field': 'title',
        'query': query,
        'from': page * size,
        'size': size,
        'orderBy': 'seeders',
        'orderDirection': 'desc'
    }).encode('utf-8')

    req = urllib.request.Request(
        KNABEN_API,
        data=payload,
        headers={
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'User-Agent': 'Mozilla/5.0'
        },
        method='POST'
    )

    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode('utf-8'))
    except Exception as e:
        print(f'[Knaben] 请求失败: {e}')
        return []

    hits = data.get('hits', [])
    results = []
    for h in hits:
        if not h.get('hash'):
            continue
        results.append({
            'name': h.get('title', ''),
            'size_mb': round(h.get('bytes', 0) / 1024 / 1024),
            'seeders': h.get('seeders', 0),
            'hash': h.get('hash', ''),
            'source': 'Knaben',
            'magnet': h.get('magnetUrl') or
                      f"magnet:?xt=urn:btih:{h['hash']}&dn={urllib.parse.quote(h.get('title', ''))}"
        })
    return results


def search_apibay(query: str, size: int = 10) -> list:
    """Search apibay (The Pirate Bay) API for torrents."""
    url = APIBAY_API + '?q=' + urllib.parse.quote(query) + '&cat=0'

    req = urllib.request.Request(
        url,
        headers={'User-Agent': 'Mozilla/5.0'},
        method='GET'
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode('utf-8'))
    except Exception as e:
        print(f'[apibay] 请求失败: {e}')
        return []

    results = []
    for t in data[:size]:
        if t.get('id') == '0':
            continue
        h = t.get('info_hash', '')
        name = t.get('name', '')
        results.append({
            'name': name,
            'size_mb': round(int(t.get('size', 0)) / 1024 / 1024),
            'seeders': int(t.get('seeders', 0)),
            'hash': h,
            'source': 'apibay',
            'magnet': f"magnet:?xt=urn:btih:{h}&dn={urllib.parse.quote(name)}"
        })
    return results


def search(query: str, size: int = 10, page: int = 0, source: str = 'auto') -> list:
    """Search torrents. source: auto | knaben | apibay | both"""
    search_query = TITLE_MAP.get(query, query)
    if search_query != query:
        print(f'[搜索] "{query}" → "{search_query}"')
    else:
        print(f'[搜索] "{search_query}"')

    if source == 'apibay':
        results = search_apibay(search_query, size)
        print(f'[apibay] 找到 {len(results)} 个结果')
        return results

    if source == 'both':
        r1 = search_knaben(search_query, size, page)
        r2 = search_apibay(search_query, size)
        print(f'[Knaben] {len(r1)} 个 | [apibay] {len(r2)} 个')
        # merge, deduplicate by hash
        seen = set()
        merged = []
        for r in r1 + r2:
            h = r['hash'].upper()
            if h not in seen:
                seen.add(h)
                merged.append(r)
        merged.sort(key=lambda r: r['seeders'], reverse=True)
        return merged[:size]

    # auto: try Knaben first, fallback to apibay
    results = search_knaben(search_query, size, page)
    if not results:
        print('[Knaben] 无结果，尝试 apibay...')
        results = search_apibay(search_query, size)
        if results:
            print(f'[apibay] 找到 {len(results)} 个结果')
    return results


def submit_to_115(magnet: str) -> bool:
    """Submit magnet link to 115 offline download."""
    script = Path(__file__).parent / '115_offline.py'
    if not script.exists():
        print(f'[错误] 找不到 115_offline.py: {script}')
        return False
    for py in ['python3.12', 'python3']:
        result = subprocess.run(
            [py, str(script), magnet],
            capture_output=True, text=True
        )
        if result.returncode == 0:
            print(result.stdout.strip())
            return True
        if 'No such file' not in result.stderr and 'not found' not in result.stderr:
            print(result.stdout.strip())
            if result.returncode != 0:
                print(result.stderr.strip())
            return result.returncode == 0
    return False


def print_results(results: list):
    if not results:
        print('[结果] 未找到相关资源')
        return
    print(f'[结果] 找到 {len(results)} 个资源:\n')
    for i, r in enumerate(results, 1):
        size = f"{r['size_mb']}MB" if r['size_mb'] < 1024 else f"{r['size_mb']/1024:.1f}GB"
        src = f"[{r.get('source','?')}]" 
        print(f"  {i}. [{r['seeders']}s] {r['name'][:60]} {src}")
        print(f"     大小: {size} | Hash: {r['hash'][:16]}...")


def best(results: list) -> Optional[dict]:
    """Pick the best result: prefer 1080p, most seeders."""
    if not results:
        return None
    hd = [r for r in results if '1080p' in r['name'] or '1080P' in r['name']]
    pool = hd if hd else results
    return max(pool, key=lambda r: r['seeders'])


def main():
    parser = argparse.ArgumentParser(
        description='magnet_search v1.1.0 - Search & submit to 115',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python3 scripts/magnet_search.py "Movie Name"                    # 搜索（Knaben优先）
  python3 scripts/magnet_search.py "电影名" --submit               # 自动提交最佳结果到115
  python3 scripts/magnet_search.py "Movie Name" --source apibay   # 仅搜apibay
  python3 scripts/magnet_search.py "Movie Name" --source both     # 两个源合并搜索
  python3 scripts/magnet_search.py "Movie Name" --top 5           # 显示前5个结果
  python3 scripts/magnet_search.py "电影名" --submit --index 2    # 提交第2个结果
        """
    )
    parser.add_argument('query', help='搜索关键词（支持中文和英文）')
    parser.add_argument('--submit', action='store_true', help='自动提交最佳结果到115离线下载')
    parser.add_argument('--index', type=int, default=0, help='提交指定序号的结果（从1开始）')
    parser.add_argument('--top', type=int, default=8, help='显示结果数量（默认8）')
    parser.add_argument('--page', type=int, default=0, help='结果页码（默认0）')
    parser.add_argument('--source', choices=['auto', 'knaben', 'apibay', 'both'],
                        default='auto', help='搜索源: auto(默认)|knaben|apibay|both')
    args = parser.parse_args()

    results = search(args.query, size=args.top, page=args.page, source=args.source)
    print_results(results)

    if not results:
        sys.exit(1)

    if args.submit:
        if args.index > 0:
            if args.index > len(results):
                print(f'[错误] 序号 {args.index} 超出范围（共 {len(results)} 个结果）')
                sys.exit(1)
            chosen = results[args.index - 1]
        else:
            chosen = best(results)

        if chosen:
            print(f'\n[提交] {chosen["name"]} [{chosen.get("source","?")}]')
            submit_to_115(chosen['magnet'])


if __name__ == '__main__':
    main()
