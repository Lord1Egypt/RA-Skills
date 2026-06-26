#!/usr/bin/env python3
"""
飞书 Bitable 任务管理工具
用法:
  python3 bitable_tasks.py list
  python3 bitable_tasks.py create "任务名称"
  python3 bitable_tasks.py done "任务关键词"
"""
import os
import sys
import json
import time
import urllib.request
import argparse

APP_ID = os.environ.get("LARK_APP_ID", "")
APP_SECRET = os.environ.get("LARK_APP_SECRET", "")
APP_TOKEN = os.environ.get("LARK_APP_TOKEN", "")
TABLE_ID = os.environ.get("LARK_TABLE_ID", "")

BASE = f"https://open.larksuite.com/open-apis/bitable/v1/apps/{APP_TOKEN}/tables/{TABLE_ID}"

_cache = {'token': None, 'exp': 0}

def get_token():
    if _cache['token'] and time.time() < _cache['exp']:
        return _cache['token']
    
    url = "https://open.larksuite.com/open-apis/auth/v3/tenant_access_token/internal"
    data = json.dumps({"app_id": APP_ID, "app_secret": APP_SECRET}).encode()
    req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
    
    with urllib.request.urlopen(req, timeout=10) as resp:
        result = json.loads(resp.read())
        _cache['token'] = result['tenant_access_token']
        _cache['exp'] = time.time() + result.get('expire', 7200) - 300
        return _cache['token']

def api(method, path, body=None):
    url = f"{BASE}{path}"
    data = json.dumps(body).encode() if body else None
    
    req = urllib.request.Request(
        url,
        data=data,
        method=method,
        headers={
            'Authorization': f'Bearer {get_token()}',
            'Content-Type': 'application/json'
        }
    )
    return json.loads(urllib.request.urlopen(req, timeout=15).read())

def list_records():
    return api("GET", "/records?page_size=100")

def create_record(name, status="待办", priority="中"):
    fields = {"任务名称": name, "状态": status, "优先级": priority}
    return api("POST", "/records", {"fields": fields})

def find_by_keyword(keyword):
    records = list_records()
    items = records.get('data', {}).get('items', [])
    matches = []
    for r in items:
        name = r['fields'].get('任务名称', '')
        if isinstance(name, list):
            name = ''.join(seg.get('text', '') for seg in name)
        if keyword in str(name):
            matches.append(r)
    return matches

def update_status(record_id, status):
    return api("PUT", f"/records/{record_id}", {"fields": {"状态": status}})

def format_task(r):
    f = r['fields']
    name = f.get('任务名称', '')
    if isinstance(name, list):
        name = ''.join(seg.get('text', '') for seg in name)
    status = f.get('状态', '-')
    pri = f.get('优先级', '-')
    return f"• {name} | {status} | {pri}"

def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest='cmd')
    
    sub.add_parser('list')
    c = sub.add_parser('create')
    c.add_argument('name')
    c.add_argument('--status', default='待办')
    c.add_argument('--priority', default='中')
    d = sub.add_parser('done')
    d.add_argument('keyword')
    
    args = parser.parse_args()
    
    if args.cmd == 'list':
        records = list_records()
        items = records.get('data', {}).get('items', [])
        if not items:
            print("暂无任务")
        else:
            for r in items:
                print(format_task(r))
    
    elif args.cmd == 'create':
        result = create_record(args.name, args.status, args.priority)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    
    elif args.cmd == 'done':
        matches = find_by_keyword(args.keyword)
        if not matches:
            print(f"未找到: {args.keyword}")
        elif len(matches) > 1:
            print(f"匹配多个: {len(matches)}")
        else:
            rec_id = matches[0]['record_id']
            result = update_status(rec_id, "已完成")
            print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
