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

def add(key, name, **fields):
    data = load()
    if key not in data:
        data[key] = {"name": name}
    else:
        data[key]["name"] = name
    for k, v in fields.items():
        data[key][k] = v
    save(data)
    print(f"[OK] {key} ({name}) 已保存，共 {len(fields)} 个字段")
    printFields(data[key])

def printFields(obj, indent=2):
    for k, v in obj.items():
        print("  " * indent + f"{k}: {v}")

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("用法: python add.py <key> <name> <field=value>...")
        print("例:  python add.py wechat '微信公众号' appid=wxd9f577d56948e564 appsecret=xxx")
        sys.exit(1)

    key = sys.argv[1]
    name = sys.argv[2]
    fields = {}
    for arg in sys.argv[3:]:
        if "=" in arg:
            k, v = arg.split("=", 1)
            fields[k.strip()] = v.strip()

    if not fields:
        print("[错误] 至少需要一个 field=value 参数")
        sys.exit(1)

    add(key, name, **fields)
