#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys; sys.stdout.reconfigure(encoding='utf-8')
import os, json, stat

SECRETS_FILE = os.path.expanduser("~/.openclaw/workspace/secrets.json")

def load():
    if os.path.exists(SECRETS_FILE):
        with open(SECRETS_FILE, encoding="utf-8") as f:
            return json.load(f)
    return {}

def get(key, field=None):
    data = load()
    if key not in data:
        print(f"[错误] 未找到令牌: {key}")
        return None

    if field:
        val = data[key].get(field)
        if val is None:
            print(f"[错误] {key} 中未找到字段: {field}")
            return None
        print(val)
        return val
    else:
        print(f"\n[{key}] {data[key].get('name', key)}")
        for k, v in data[key].items():
            print(f"  {k}: {v}")
        return data[key]

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python get.py <key> [field]")
        print("例:  python get.py wechat")
        print("例:  python get.py wechat appid")
        sys.exit(1)

    key = sys.argv[1]
    field = sys.argv[2] if len(sys.argv) > 2 else None
    get(key, field)
