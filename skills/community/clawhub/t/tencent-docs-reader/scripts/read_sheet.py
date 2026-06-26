#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
QQ Doc Reader - Read Tencent Docs spreadsheet content via agent-browser copy-paste.

Usage:
    python read_sheet.py --url "https://docs.qq.com/sheet/XXXX"
    python read_sheet.py --url "https://docs.qq.com/sheet/XXXX" --tab "0328"
    python read_sheet.py --url "https://docs.qq.com/sheet/XXXX" --auto-tab
    python read_sheet.py --url "https://docs.qq.com/sheet/XXXX" --output result.txt
"""

import subprocess
import time
import sys
import argparse
import json
import os
import re
from datetime import datetime, timedelta

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
sys.stderr.reconfigure(encoding='utf-8', errors='replace')

AB = os.path.join(
    os.environ.get('APPDATA', ''),
    'npm',
    'agent-browser.cmd'
)
if not os.path.isfile(AB):
    AB = 'agent-browser'


def run(args, timeout=20):
    r = subprocess.run(args, capture_output=True, timeout=timeout)
    out = r.stdout.decode('utf-8', errors='replace')
    err = r.stderr.decode('utf-8', errors='replace')
    return out + err


def get_all_tabs():
    """获取所有标签页列表"""
    out = run([AB, 'snapshot', '-i', '--json'], timeout=15)
    lines = out.strip().split('\n')
    json_start = -1
    for i, line in enumerate(lines):
        if line.strip().startswith('{'):
            json_start = i
            break
    if json_start < 0:
        return []
    try:
        data = json.loads('\n'.join(lines[json_start:]))
    except json.JSONDecodeError:
        return []

    refs = data.get('data', {}).get('refs', {})
    tabs = []
    for ref_id, info in refs.items():
        name = info.get('name', '')
        role = info.get('role', '')
        if role == 'tab' and name:
            tabs.append({'ref': ref_id, 'name': name})
    return tabs


def parse_tab_date(tab_name):
    """解析标签页名称中的日期，支持多种格式"""
    # 纯数字格式: "0328" (MMDD)
    if re.match(r'^\d{4}$', tab_name):
        month = int(tab_name[:2])
        day = int(tab_name[2:])
        try:
            return datetime(datetime.now().year, month, day)
        except ValueError:
            return None

    # 格式: "03-28" 或 "3-28"
    match = re.match(r'^(\d{1,2})-(\d{1,2})$', tab_name)
    if match:
        month = int(match.group(1))
        day = int(match.group(2))
        try:
            return datetime(datetime.now().year, month, day)
        except ValueError:
            return None

    # 格式: "2026-03-28"
    match = re.match(r'^(\d{4})-(\d{1,2})-(\d{1,2})$', tab_name)
    if match:
        try:
            return datetime(int(match.group(1)), int(match.group(2)), int(match.group(3)))
        except ValueError:
            return None

    return None


def get_friday_of_week(date=None):
    """获取指定日期所在周的周五日期"""
    if date is None:
        date = datetime.now()

    # 周一=0, 周二=1, ..., 周五=4, 周六=5, 周日=6
    weekday = date.weekday()

    # 计算到周五的天数差
    days_to_friday = 4 - weekday

    # 如果是周六或周日，本周五是上周的（需要减去天数）
    # 周六(5): 4-5=-1, 需要减1天
    # 周日(6): 4-6=-2, 需要减2天
    if days_to_friday < 0:
        # 不需要额外减7，直接用负数即可
        pass

    friday = date + timedelta(days=days_to_friday)
    return friday


def find_nearest_tab(tabs, today=None):
    """找到离今天最近的日期标签页"""
    if today is None:
        today = datetime.now()

    dated_tabs = []
    for tab in tabs:
        tab_date = parse_tab_date(tab['name'])
        if tab_date:
            dated_tabs.append({
                'ref': tab['ref'],
                'name': tab['name'],
                'date': tab_date,
                'diff': abs((tab_date - today).days)
            })

    if not dated_tabs:
        return None

    # 按日期差距排序，选最近的
    dated_tabs.sort(key=lambda x: x['diff'])
    return dated_tabs[0]


def find_current_week_tab(tabs, today=None):
    """找到本周的周报标签页（本周五）"""
    if today is None:
        today = datetime.now()

    # 获取本周五的日期
    friday = get_friday_of_week(today)
    friday_str = friday.strftime('%m%d')

    # 查找匹配本周五的标签页
    for tab in tabs:
        if tab['name'] == friday_str:
            return tab

    return None


def find_nearby_tab(tabs, today=None, days_range=2):
    """找到当前日期前后指定天数内的标签页"""
    if today is None:
        today = datetime.now()

    # 计算日期范围
    start_date = today - timedelta(days=days_range)
    end_date = today + timedelta(days=days_range)

    # 查找范围内的标签页
    nearby_tabs = []
    for tab in tabs:
        tab_date = parse_tab_date(tab['name'])
        if tab_date and start_date <= tab_date <= end_date:
            nearby_tabs.append({
                'ref': tab['ref'],
                'name': tab['name'],
                'date': tab_date,
                'diff': abs((tab_date - today).days)
            })

    if not nearby_tabs:
        return None

    # 按日期差距排序，选最近的
    nearby_tabs.sort(key=lambda x: x['diff'])
    return nearby_tabs[0]


def find_tab_ref(tab_name):
    out = run([AB, 'snapshot', '-i', '--json'], timeout=15)
    lines = out.strip().split('\n')
    json_start = -1
    for i, line in enumerate(lines):
        if line.strip().startswith('{'):
            json_start = i
            break
    if json_start < 0:
        return None
    try:
        data = json.loads('\n'.join(lines[json_start:]))
    except json.JSONDecodeError:
            return None
    refs = data.get('data', {}).get('refs', {})
    for ref_id, info in refs.items():
        name = info.get('name', '')
        role = info.get('role', '')
        if name == tab_name and role == 'tab':
            return ref_id
    return None


def find_table_ref():
    out = run([AB, 'snapshot', '-i', '--json'], timeout=15)
    lines = out.strip().split('\n')
    json_start = -1
    for i, line in enumerate(lines):
        if line.strip().startswith('{'):
            json_start = i
            break
    if json_start < 0:
        return None
    try:
        data = json.loads('\n'.join(lines[json_start:]))
    except json.JSONDecodeError:
        return None
    refs = data.get('data', {}).get('refs', {})
    for ref_id, info in refs.items():
        role = info.get('role', '')
        if role in ('combobox', 'textbox'):
            return ref_id
    return None


def read_sheet(url, tab_name=None, auto_tab=False):
    # 1. Open the document
    print(f'Opening: {url}', file=sys.stderr)
    out = run([AB, 'open', url], timeout=30)
    if 'Error' in out and 'open' not in out.lower():
        print(f'Failed to open: {out}', file=sys.stderr)
        return None
    time.sleep(3)

    # 2. Determine which tab to use
    if auto_tab:
        print('Finding current week tab (this Friday)...', file=sys.stderr)
        tabs = get_all_tabs()
        if tabs:
            print(f'Found {len(tabs)} tabs: {[t["name"] for t in tabs]}', file=sys.stderr)
            current_week_tab = find_current_week_tab(tabs)
            if current_week_tab:
                tab_name = current_week_tab['name']
                print(f'Current week tab: {tab_name}', file=sys.stderr)
            else:
                # 如果找不到本周的标签页，尝试找当前日期前后两天内的
                print('Current week tab not found, trying nearby tabs (within 2 days)...', file=sys.stderr)
                nearby = find_nearby_tab(tabs, days_range=2)
                if nearby:
                    tab_name = nearby['name']
                    print(f'Nearby tab: {tab_name} ({nearby["diff"]} days from today)', file=sys.stderr)
                else:
                    # 如果都找不到，返回None让调用者处理
                    print('No suitable tab found within range', file=sys.stderr)
                    return None
        else:
            print('No tabs found', file=sys.stderr)
            return None

    # 3. Switch to specific tab if requested
    if tab_name:
        print(f'Switching to tab: {tab_name}', file=sys.stderr)
        tab_ref = find_tab_ref(tab_name)
        if tab_ref:
            run([AB, 'click', f'@{tab_ref}'], timeout=10)
            time.sleep(3)
        else:
            print(f'Warning: Tab "{tab_name}" not found, using current view', file=sys.stderr)

    # 4. Click table area to focus
    print('Focusing table area...', file=sys.stderr)
    table_ref = find_table_ref()
    if table_ref:
        run([AB, 'click', f'@{table_ref}'], timeout=10)
        time.sleep(1)
    # 5. Select all and copy
    print('Selecting all...', file=sys.stderr)
    run([AB, 'press', 'Control+a'], timeout=10)
    time.sleep(1)
    print('Copying...', file=sys.stderr)
    run([AB, 'press', 'Control+c'], timeout=10)
    time.sleep(2)
    # 6. Open new tab with textarea
    print('Opening paste target...', file=sys.stderr)
    run([AB, 'tab', 'new'], timeout=10)
    time.sleep(1)
    # 7. Create textarea via eval
    js = (
        "document.body.innerHTML="
        "'<textarea id=\"p\" style=\"width:100vw;height:100vh;font-size:14px\"></textarea>';"
        "document.getElementById('p').focus();"
    )
    run([AB, 'eval', js], timeout=10)
    time.sleep(1)
    # 8. Paste
    print('Pasting...', file=sys.stderr)
    run([AB, 'press', 'Control+v'], timeout=10)
    time.sleep(2)
    # 9. Read textarea content
    print('Reading content...', file=sys.stderr)
    out = run([AB, 'eval', "document.getElementById('p').value"], timeout=10)
    text = out.strip()
    try:
        parsed = json.loads(text)
        if isinstance(parsed, str):
            text = parsed
    except (json.JSONDecodeError, ValueError):
        pass
    lines = text.split('\n')
    while lines and not lines[-1].strip():
        lines.pop()
    text = '\n'.join(lines)
    # 10. Close the paste tab, go back
    run([AB, 'tab', 'close'], timeout=10)
    if len(text) > 10:
        print(f'Success! Read {len(text)} chars', file=sys.stderr)
        return text
    else:
        print(f'Warning: Only got {len(text)} chars', file=sys.stderr)
        return text if text else None


def main():
    parser = argparse.ArgumentParser(description='Read Tencent Docs spreadsheet')
    parser.add_argument('--url', required=True, help='Tencent Docs URL')
    parser.add_argument('--tab', default=None, help='Sheet tab name (e.g. "0328")')
    parser.add_argument('--auto-tab', action='store_true', help='Auto-select nearest date tab')
    parser.add_argument('--output', '-o', default=None, help='Output file path')
    args = parser.parse_args()

    content = read_sheet(args.url, tab_name=args.tab, auto_tab=args.auto_tab)
    if content is None:
        print('Failed to read sheet', file=sys.stderr)
        sys.exit(1)
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'Saved to {args.output}', file=sys.stderr)
    else:
        print(content)


if __name__ == '__main__':
    main()
