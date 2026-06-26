#!/usr/bin/env python3
"""测试分类匹配功能"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from publish_v2_full import get_existing_categories, match_category, load_env

# 获取已有分类
config = load_env()
existing_cats = get_existing_categories(config)

print(f"博客已有 {len(existing_cats)} 个分类:")
for name, id in existing_cats.items():
    print(f"  - {name} (ID:{id})")

# 测试匹配
test_cases = [
    "技术",
    "AI",
    "人工智",
    "创业",
    "团子",
    "默认",
    "不存在的分类"
]

print("\n分类匹配测试:")
for test in test_cases:
    matched = match_category(test, existing_cats)
    status = "✅" if matched != test else "⚠️"
    print(f"  {status} '{test}' → '{matched}'")
