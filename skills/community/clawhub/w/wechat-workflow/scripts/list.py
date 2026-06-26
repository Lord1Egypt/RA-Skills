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

def mask(val):
    s = str(val)
    if len(s) <= 8:
        return s[:2] + "**" + s[-2:]
    return s[:6] + "..." + s[-4:]

def list_all():
    data = load()
    if not data:
        print("暂无任何令牌，请先用 add.py 添加")
        return

    print(f"\n{'='*50}")
    print(f"  令牌管理中心 (共 {len(data)} 个)")
    print(f"{'='*50}\n")

    for key, info in data.items():
        name = info.get("name", key)
        fields = {k: v for k, v in info.items() if k != "name"}
        masked = {k: mask(v) for k, v in fields.items()}
        print(f"[{key}] {name}")
        for k, v in masked.items():
            print(f"    {k}: {v}")
        print()

if __name__ == "__main__":
    list_all()
