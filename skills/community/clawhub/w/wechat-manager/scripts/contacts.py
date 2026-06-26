#!/usr/bin/env python3
"""
WeChat contact management utilities.
"""
import json
import sys
import os
from collections import defaultdict

CONTACTS_DB = os.path.expanduser("~/.openclaw/data/wechat-contacts.json")
TAGS_DB = os.path.expanduser("~/.openclaw/data/wechat-tags.json")

def load_contacts():
    if not os.path.exists(CONTACTS_DB):
        return []
    with open(CONTACTS_DB, 'r') as f:
        return json.load(f)

def load_tags():
    if not os.path.exists(TAGS_DB):
        return {}
    with open(TAGS_DB, 'r') as f:
        return json.load(f)

def search(name):
    """Search for a contact by name, remark, or WeChat ID."""
    contacts = load_contacts()
    name_lower = name.lower()
    
    results = [c for c in contacts if 
               name_lower in (c.get('name', '') + c.get('remark', '') + c.get('wxid', '')).lower()]
    
    if not results:
        print(f"🔍 未找到 '{name}' 相关联系人")
        return
    
    print(f"🔍 找到 {len(results)} 个联系人:")
    for c in results[:5]:
        wxid = c.get('wxid', 'N/A')
        remark = c.get('remark', '')
        display = f"{c.get('name', '?')}"
        if remark:
            display += f" (备注: {remark})"
        print(f"\n👤 {display}")
        print(f"   📱 微信号: {wxid}")
        if c.get('tags'):
            print(f"   🏷️ 标签: {', '.join(c['tags'])}")

def by_tag(tag):
    """List contacts by tag."""
    contacts = load_contacts()
    matched = [c for c in contacts if tag in c.get('tags', [])]
    
    print(f"🏷️ 标签 '{tag}': {len(matched)} 个联系人")
    for c in matched:
        print(f"  • {c.get('name', '?')} {'(备注: ' + c['remark'] + ')' if c.get('remark') else ''}")

def stats():
    """Contact statistics."""
    contacts = load_contacts()
    tags = load_tags()
    
    print(f"📊 联系人统计:")
    print(f"  总计: {len(contacts)} 个联系人")
    
    tag_counts = defaultdict(int)
    for c in contacts:
        for t in c.get('tags', []):
            tag_counts[t] += 1
    
    if tag_counts:
        print("  标签分布:")
        for t, count in sorted(tag_counts.items(), key=lambda x: -x[1])[:10]:
            print(f"    {t}: {count}人")

def main():
    if len(sys.argv) < 2:
        print("Usage: contacts.py <cmd> [args]")
        print("Commands: search <name>, tag <tag>, stats")
        return
    
    cmd = sys.argv[1]
    if cmd == 'search' and len(sys.argv) > 2:
        search(' '.join(sys.argv[2:]))
    elif cmd == 'tag' and len(sys.argv) > 2:
        by_tag(sys.argv[2])
    elif cmd == 'stats':
        stats()
    else:
        print(f"Unknown: {cmd}")

if __name__ == '__main__':
    main()
