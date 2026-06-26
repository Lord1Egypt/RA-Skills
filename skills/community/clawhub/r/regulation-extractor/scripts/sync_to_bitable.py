# -*- coding: utf-8 -*-
"""
将提取的条文JSON写入飞书多维表格，支持去重和补写。
用法: python sync_to_bitable.py <json_path> [--app_token APP] [--table_id TBL]
"""

import json, sys, argparse, urllib.request
from pathlib import Path


def get_token(app_id, app_secret):
    url = 'https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal'
    body = json.dumps({"app_id": app_id, "app_secret": app_secret}).encode()
    req = urllib.request.Request(url, data=body, headers={'Content-Type': 'application/json'})
    resp = json.loads(urllib.request.urlopen(req).read())
    return resp['tenant_access_token']


def list_records(token, app_token, table_id, page_size=500):
    url = f'https://open.feishu.cn/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/records?page_size={page_size}'
    req = urllib.request.Request(url, headers={'Authorization': f'Bearer {token}'})
    resp = json.loads(urllib.request.urlopen(req).read())
    return resp.get('data', {}).get('items', [])


def create_record(token, app_token, table_id, fields):
    url = f'https://open.feishu.cn/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/records'
    body = json.dumps({"fields": fields}).encode()
    req = urllib.request.Request(url, data=body, headers={
        'Content-Type': 'application/json', 'Authorization': f'Bearer {token}'
    })
    resp = json.loads(urllib.request.urlopen(req).read())
    return resp


def batch_delete(token, app_token, table_id, record_ids):
    url = f'https://open.feishu.cn/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/records/batch_delete'
    body = json.dumps({"records": record_ids}).encode()
    req = urllib.request.Request(url, data=body, headers={
        'Content-Type': 'application/json', 'Authorization': f'Bearer {token}'
    })
    return json.loads(urllib.request.urlopen(req).read())


def main():
    parser = argparse.ArgumentParser(description="条文写入飞书多维表格")
    parser.add_argument("json", help="提取结果JSON路径")
    parser.add_argument("--app_token", required=True, help="飞书多维表格app_token")
    parser.add_argument("--table_id", required=True, help="表格table_id")
    parser.add_argument("--app_id", required=True, help="飞书App ID")
    parser.add_argument("--app_secret", required=True, help="飞书App Secret")
    parser.add_argument("--dry_run", action="store_true", help="仅检查，不写入")
    parser.add_argument("--delete_dupes", action="store_true", help="删除重复记录（保留最早的）")
    args = parser.parse_args()

    with open(args.json, 'r', encoding='utf-8') as f:
        data = json.load(f)
    articles = data.get('articles', {})

    token = get_token(args.app_id, args.app_secret)
    existing = list_records(token, args.app_token, args.table_id)
    
    existing_ids = {}
    for r in existing:
        aid = r.get('fields', {}).get('条文编号', '')
        if aid:
            existing_ids.setdefault(aid, []).append(r['record_id'])

    # 去重
    dupes = {k: v for k, v in existing_ids.items() if len(v) > 1}
    if dupes and args.delete_dupes:
        to_delete = []
        for aid, rids in dupes.items():
            to_delete.extend(rids[1:])
        if to_delete:
            print(f"🗑️ 删除{len(to_delete)}条重复记录...")
            batch_delete(token, args.app_token, args.table_id, to_delete)
        existing = list_records(token, args.app_token, args.table_id)
        existing_ids = {}
        for r in existing:
            aid = r.get('fields', {}).get('条文编号', '')
            if aid:
                existing_ids[aid] = r['record_id']

    # 查缺
    missing = {aid: info for aid, info in articles.items() if aid not in existing_ids}
    print(f"📊 已有: {len(existing_ids)}条  待写: {len(missing)}条")

    if args.dry_run:
        for aid in sorted(missing.keys()):
            print(f"   {aid}: {missing[aid]['text'][:50]}...")
        return

    # 写入
    ok, fail = 0, 0
    for aid, info in sorted(missing.items()):
        fields = {
            "条文编号": info["id"],
            "所属章节": info.get("chapter", ""),
            "页码": str(info.get("page", "")),
            "质量": "✅ 干净" if info.get("quality") == "clean" else "⚠️ OCR错误",
            "条文内容": info["text"],
        }
        try:
            create_record(token, args.app_token, args.table_id, fields)
            ok += 1
            print(f"  ✅ {aid}")
        except Exception as e:
            fail += 1
            print(f"  ❌ {aid}: {e}")

    print(f"\n✅ 写入{ok}条  ❌ 失败{fail}条")


if __name__ == '__main__':
    main()
