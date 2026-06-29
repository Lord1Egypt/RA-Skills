#!/usr/bin/env python3
"""
测试 _truncate_author 函数的行为
"""

# 直接复制函数逻辑进行测试
import re

def _truncate_author(author, max_units=16):
    """
    截断 author 字段以满足微信公众号 API 限制。
    
    微信官方规则（与 title、digest 完全同一套计算逻辑）：
      - 中文字符（汉字、中文标点、Emoji、全角符号）= 1 字
      - 英文/数字/半角标点/空格 = 0.5 字（2 个折算 1 字）
      - 总校验公式：中文字符数 + (英文字符数 ÷ 2) ≤ 16
    """
    if not author:
        return ""
    
    result = []
    used = 0.0
    
    for ch in author:
        code = ord(ch)
        if (
            0x4E00 <= code <= 0x9FFF
            or 0x3400 <= code <= 0x4DBF
            or 0x20000 <= code <= 0x2A6DF
            or 0x2A700 <= code <= 0x2B73F
            or 0x2B740 <= code <= 0x2B81F
            or 0x2B820 <= code <= 0x2CEAF
            or 0xF900 <= code <= 0xFAFF
            or 0xFF00 <= code <= 0xFFEF
            or 0x3000 <= code <= 0x303F
            or 0x1F300 <= code <= 0x1FAFF
        ):
            cost = 1.0
        else:
            cost = 0.5
        
        if used + cost > max_units + 1e-9:
            break
        result.append(ch)
        used += cost
    
    return "".join(result)


# 测试用例
test_cases = [
    ("纯中文", "一二三四五六七八九十") ,  # 10个中文
    ("混合", "晴悦ab"),  # 2中文 + 2英文
    ("纯英文", "Woody"),  # 5个英文
    ("长混合", "晴悦abcde"),  # 2中文 + 5英文 = 2 + 2.5 = 4.5 units
    ("边界测试", "a" * 32),  # 32个英文 = 16 units
    ("超限测试", "一" * 20),  # 20个中文 = 20 units (应该截断到16)
]

print("=" * 60)
print("测试 _truncate_author() 函数")
print("=" * 60)

for name, author in test_cases:
    result = _truncate_author(author)
    print(f"\n【{name}】")
    print(f"  输入: {author}")
    print(f"  输出: {result}")
    print(f"  输入长度: {len(author)} 字符")
    print(f"  输出长度: {len(result)} 字符")
    
    # 计算 units
    units = 0
    for ch in result:
        code = ord(ch)
        if (
            0x4E00 <= code <= 0x9FFF
            or 0x3400 <= code <= 0x4DBF
            or 0x20000 <= code <= 0x2A6DF
            or 0x2A700 <= code <= 0x2B73F
            or 0x2B740 <= code <= 0x2B81F
            or 0x2B820 <= code <= 0x2CEAF
            or 0xF900 <= code <= 0xFAFF
            or 0xFF00 <= code <= 0xFFEF
            or 0x3000 <= code <= 0x303F
            or 0x1F300 <= code <= 0x1FAFF
        ):
            units += 1
        else:
            units += 0.5
    print(f"  消耗 units: {units}")

print("\n" + "=" * 60)
print("问题分析：")
print("=" * 60)
print("当前代码逻辑：")
print("  - 中文 = 1 unit")
print("  - 英文 = 0.5 unit")
print("  - 最大 16 units")
print("\n如果微信实际限制是 16 字节（UTF-8）：")
print("  - 中文 = 3 字节 each")
print("  - 英文 = 1 字节 each")
print("  - 纯中文最多 5 个字符（16÷3=5.33）")
print("\n但用户说纯中文只能 2 个字，这不对...")
print("需要用户提供更多测试数据。")
