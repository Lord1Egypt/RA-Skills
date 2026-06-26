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

def save(data):
    with open(SECRETS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    os.chmod(SECRETS_FILE, stat.S_IRUSR | stat.S_IWUSR)

def remove(key):
    data = load()
    if key not in data:
        print(f"[错误] 未找到令牌: {key}")
        return

    name = data[key].get("name", key)
    del data[key]
    save(data)
    print(f"[OK] 已删除 {key} ({name})")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python remove.py <key>")
        print("例:  python remove.py wechat")
        sys.exit(1)

    remove(sys.argv[1])
