#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试实时搜索引擎功能
"""

import sys
import os
from pathlib import Path

os.chdir(Path(__file__).parent)
sys.path.insert(0, str(Path(__file__).parent))

from scheduled_publish_security import collect_security_news

print("=" * 60)
print("🔍 测试实时搜索引擎")
print("=" * 60)

# 收集新闻
news_items = collect_security_news()

print(f"\n✅ 共收集到 {len(news_items)} 起事件\n")

# 分类统计
real_time = [n for n in news_items if n.get('real_time')]
preset = [n for n in news_items if not n.get('real_time')]

print(f"📊 数据来源统计:")
print(f"  🔍 实时搜索：{len(real_time)} 起")
print(f"  📋 预设模板：{len(preset)} 起")

print("\n" + "=" * 60)
print("📰 实时搜索结果（前 5 条）")
print("=" * 60)

for i, n in enumerate(real_time[:5], 1):
    print(f"\n{i}. {n['title']}")
    print(f"   来源：{n.get('source', 'N/A')[:60]}...")
    print(f"   摘要：{n['summary'][:100]}...")

print("\n" + "=" * 60)
if len(real_time) > 0:
    print("✅ 实时搜索引擎工作正常！")
else:
    print("⚠️ 实时搜索未返回结果，使用预设数据")
print("=" * 60)
