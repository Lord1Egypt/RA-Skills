#!/usr/bin/env python3
"""
测试新的 _truncate_author 函数（按 UTF-8 字节数截断）
"""

import sys
sys.path.insert(0, '/Users/woody/WorkBuddy/2026-06-25-15-55-19/wechat-oa')

from wechat_push import _truncate_author

# 测试用例
test_cases = [
    ("纯中文2字", "一二"),
    ("纯中文5字", "一二三四五"),
    ("纯中文10字", "一二三四五六七八九十"),
    ("混合4字", "晴悦ab"),
    ("纯英文", "Woody"),
    ("长英文", "A" * 20),
    ("中文+英文混合", "晴悦abcde"),
]

print("=" * 70)
print("测试新的 _truncate_author() 函数（按 UTF-8 字节数截断）")
print("=" * 70)

for name, author in test_cases:
    result = _truncate_author(author)
    author_bytes = len(author.encode('utf-8'))
    result_bytes = len(result.encode('utf-8'))
    
    print(f"\n【{name}】")
    print(f"  输入: {author}")
    print(f"  输出: {result}")
    print(f"  输入长度: {len(author)} 字符, {author_bytes} 字节")
    print(f"  输出长度: {len(result)} 字符, {result_bytes} 字节")
    print(f"  ✅ 字节数 ≤ 16" if result_bytes <= 16 else f"  ❌ 字节数 > 16")

print("\n" + "=" * 70)
print("说明：")
print("=" * 70)
print("新逻辑：按 UTF-8 字节数截断，最大 16 字节")
print("  - 中文 = 3 字节/字符")
print("  - 英文 = 1 字节/字符")
print("  - 所以纯中文最多 5 个字符（16÷3=5.33）")
print("  - 纯英文最多 16 个字符")
