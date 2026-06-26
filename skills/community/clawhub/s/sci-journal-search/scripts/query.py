#!/usr/bin/env python3
"""
SCI 期刊查询工具
数据源：
  1. 新锐 XinRui (https://www.xr-scholar.com) - 默认查询，快速
  2. LetPub (https://www.letpub.com.cn) - 可选，需要浏览器

使用方法:
    python query.py <期刊名> [--year 2026] [--json] [--letpub]
"""

import requests
import re
import html
import json
import argparse
import sys
from urllib.parse import quote
from pathlib import Path

BASE_URL_XR = "https://www.xr-scholar.com"

def load_abbreviations():
    script_dir = Path(__file__).parent
    abbrev_file = script_dir.parent / "data" / "abbreviations.json"
    try:
        with open(abbrev_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            mappings = {}
            for cat, items in data.get('mappings', {}).items():
                mappings.update(items)
            return mappings, data.get('version', 'unknown')
    except:
        return {}, 'unknown'

JOURNAL_ABBREVIATIONS, ABBREV_VERSION = load_abbreviations()

def search_journal_xr(keyword, year=2026):
    url = f"{BASE_URL_XR}/Journals/Search?year={year}&keyword={keyword}"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        matches = re.findall(r'href="(/Journals/[a-zA-Z0-9]+)"', resp.text)
        for match in matches:
            if match not in ['/Journals/Search', '/Journals/UnderReview']:
                return match
    except:
        pass
    return None

def get_journal_detail_xr(journal_path):
    url = f"{BASE_URL_XR}{journal_path}"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        title_match = re.search(r'<h3[^>]*>([^<]+)</h3>', resp.text)
        issn_match = re.search(r'ISSN</dt>\s*<dd[^>]*>([^<]+)</dd>', resp.text)
        eissn_match = re.search(r'EISSN</dt>\s*<dd[^>]*>([^<]+)</dd>', resp.text)
        publisher_match = re.search(r'>Publisher<.*?<dd[^>]*>([^<]+)</dd>', resp.text)
        
        tables = re.findall(r'<tbody>(.*?)</tbody>', resp.text, re.DOTALL)
        research_areas, jcr_categories = [], []
        current_list = research_areas
        
        for table in tables:
            rows = re.findall(r'<tr>(.*?)</tr>', table, re.DOTALL)
            for row in rows:
                cells = re.findall(r'<td[^>]*>(.*?)</td>', row, re.DOTALL)
                if len(cells) >= 3:
                    cells_clean = [html.unescape(re.sub(r'<[^>]+>', '', c).strip()) for c in cells]
                    if '英文名' in cells_clean[0] or 'Name' in cells_clean[0]:
                        continue
                    if any('区' in c or 'T' in c for c in cells_clean):
                        area_info = {
                            'name_en': cells_clean[0],
                            'name_zh': cells_clean[1] if len(cells_clean) > 1 else '',
                            'partition': cells_clean[2] if len(cells_clean) > 2 else '',
                            'is_top': 'Top' in row
                        }
                        current_list.append(area_info)
            if current_list == research_areas and research_areas:
                current_list = jcr_categories
        
        return {
            'title': html.unescape(title_match.group(1).strip()) if title_match else '',
            'issn': issn_match.group(1).strip() if issn_match else '',
            'eissn': eissn_match.group(1).strip() if eissn_match else '',
            'publisher': html.unescape(publisher_match.group(1).strip()) if publisher_match else '',
            'research_areas': research_areas,
            'jcr_categories': jcr_categories
        }
    except:
        return None

def expand_abbreviation(name):
    upper = name.upper().strip()
    if upper in JOURNAL_ABBREVIATIONS:
        return [JOURNAL_ABBREVIATIONS[upper]]
    return []

def format_output_xr(detail):
    lines = [f"📊 {detail['title']}", f"ISSN: {detail['issn']} | EISSN: {detail['eissn']}"]
    if detail['publisher']:
        lines.append(f"出版社：{detail['publisher']}")
    lines.append("\n【新锐分区（中科院分区）】")
    for area in detail['research_areas']:
        top = " 🏆 Top" if area.get('is_top') else ""
        lines.append(f"  • {area['name_en']} ({area['name_zh']}): {area['partition']}{top}")
    if detail['jcr_categories']:
        lines.append("\n【JCR 小类分区】")
        for cat in detail['jcr_categories']:
            lines.append(f"  • {cat['name_en']} ({cat['name_zh']}): {cat['partition']}")
    return '\n'.join(lines)

def main():
    parser = argparse.ArgumentParser(description='SCI 期刊查询工具')
    parser.add_argument('keyword', help='期刊名或 ISSN')
    parser.add_argument('--year', type=int, default=2026)
    parser.add_argument('--json', action='store_true')
    parser.add_argument('--verbose', '-v', action='store_true')
    parser.add_argument('--no-suggest', action='store_true')
    parser.add_argument('--letpub', action='store_true', help='同时查询 LetPub（需要浏览器）')
    args = parser.parse_args()
    
    if args.verbose:
        print(f"搜索：{args.keyword}", file=sys.stderr)
    
    is_issn = bool(re.match(r'^\d{4}-\d{3}[\dX]$', args.keyword, re.IGNORECASE))
    expanded = None
    if not is_issn and not args.no_suggest:
        possible = expand_abbreviation(args.keyword)
        if possible:
            expanded = possible[0]
            if args.verbose:
                print(f"简称扩展：{args.keyword} -> {expanded}", file=sys.stderr)
    
    keyword = expanded if expanded else args.keyword
    xr_path = search_journal_xr(keyword, args.year)
    xr_data = get_journal_detail_xr(xr_path) if xr_path else None
    
    if args.json:
        print(json.dumps({'xr': xr_data}, ensure_ascii=False, indent=2))
        return 0 if xr_data else 1
    
    if not xr_data:
        print(f"❌ 未找到期刊：{args.keyword}")
        return 1
    
    print(format_output_xr(xr_data))
    
    # 如果指定了 --letpub，调用 query-letpub.py 输出 JSON 配置
    if args.letpub:
        letpub_script = Path(__file__).parent / "query-letpub.py"
        if letpub_script.exists():
            import subprocess
            # 使用扩展后的全称查询 LetPub，而不是原始简称
            letpub_keyword = keyword if keyword else args.keyword
            result = subprocess.run(
                [sys.executable, str(letpub_script), letpub_keyword],
                capture_output=True,
                text=True
            )
            # 输出 LetPub 脚本的 JSON 结果，供 Agent 解析
            print("\n" + result.stdout)
            if result.returncode != 0:
                print(f"⚠️ LetPub 脚本执行失败：{result.stderr}", file=sys.stderr)
        else:
            print(f"\n⚠️ 未找到 query-letpub.py 脚本", file=sys.stderr)
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
