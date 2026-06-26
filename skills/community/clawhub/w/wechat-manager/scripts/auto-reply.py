#!/usr/bin/env python3
"""
WeChat auto-reply rule engine.
"""
import json
import sys
import os
import re
from datetime import datetime, time

RULES_DB = os.path.expanduser("~/.openclaw/data/wechat-autoreply.json")

DEFAULT_RULES = [
    {
        "name": "工作时间",
        "match": {"type": "time_range", "start": "09:00", "end": "18:00"},
        "reply": "我在开会，稍后回复您 🙏",
        "priority": 10
    },
    {
        "name": "休息时间",
        "match": {"type": "time_range", "start": "22:00", "end": "08:00"},
        "reply": "已休息，明天回复 🌙",
        "priority": 10
    },
    {
        "name": "加微信",
        "match": {"type": "keyword", "words": ["加微信", "微信号", "你的微信"]},
        "reply": "这是我的微信，请扫描二维码添加 👇",
        "priority": 5
    },
    {
        "name": "常见问题",
        "match": {"type": "keyword", "words": ["在吗", "在不在", "hello", "hi"]},
        "reply": "在的！有什么可以帮您？😊",
        "priority": 1
    }
]

def load_rules():
    if os.path.exists(RULES_DB):
        with open(RULES_DB, 'r') as f:
            return json.load(f)
    return DEFAULT_RULES

def save_rules(rules):
    os.makedirs(os.path.dirname(RULES_DB), exist_ok=True)
    with open(RULES_DB, 'w') as f:
        json.dump(rules, f, indent=2, ensure_ascii=False)

def list_rules():
    rules = load_rules()
    print(f"📋 自动回复规则 ({len(rules)}条):")
    for r in sorted(rules, key=lambda x: -x.get('priority', 0)):
        print(f"\n  {'🔴' if r.get('enabled', True) else '⚫'} {r['name']} (优先级:{r.get('priority', 0)})")
        print(f"    匹配: {r['match']['type']}")
        print(f"    回复: {r['reply'][:60]}")
        print(f"    目标: {', '.join(r.get('targets', ['所有人']))}")

def add_rule(args):
    """Add a simple keyword rule."""
    if len(args) < 2:
        print("Usage: auto-reply.py add <keyword> <reply_text>")
        return
    
    keyword, reply = args[0], ' '.join(args[1:])
    rules = load_rules()
    
    rules.append({
        "name": f"关键词: {keyword}",
        "match": {"type": "keyword", "words": [keyword]},
        "reply": reply,
        "priority": 5,
        "enabled": True
    })
    
    save_rules(rules)
    print(f"✅ 已添加规则: 当收到 '{keyword}' 时回复 '{reply[:30]}...'")

def remove_rule(name):
    rules = load_rules()
    rules = [r for r in rules if name not in r['name']]
    save_rules(rules)
    print(f"✅ 已删除包含 '{name}' 的规则")

def test_match(msg):
    """Test which rules match a given message."""
    rules = load_rules()
    matched = []
    
    for r in rules:
        if not r.get('enabled', True):
            continue
        match = r['match']
        if match['type'] == 'keyword':
            for word in match['words']:
                if word.lower() in msg.lower():
                    matched.append(r)
                    break
    
    if matched:
        print(f"匹配到 {len(matched)} 条规则:")
        for r in sorted(matched, key=lambda x: -x.get('priority', 0)):
            print(f"  → {r['name']}: {r['reply']}")
    else:
        print("未匹配到任何规则")

def main():
    if len(sys.argv) < 2:
        print("Usage: auto-reply.py <list|add|remove|test> [args]")
        return
    
    cmd = sys.argv[1]
    
    if cmd == 'list':
        list_rules()
    elif cmd == 'add' and len(sys.argv) > 3:
        add_rule(sys.argv[2:])
    elif cmd == 'remove' and len(sys.argv) > 2:
        remove_rule(sys.argv[2])
    elif cmd == 'test' and len(sys.argv) > 2:
        test_match(' '.join(sys.argv[2:]))
    else:
        list_rules()

if __name__ == '__main__':
    main()
