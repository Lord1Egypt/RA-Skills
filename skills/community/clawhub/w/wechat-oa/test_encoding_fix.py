#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试 _fix_garbled 函数的编码修复功能（准确模拟双重编码）
"""
import sys
import os

# 导入 relay_client 模块
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from relay_client import _fix_garbled


def simulate_double_encoding(text: str) -> str:
    """
    准确模拟双重编码问题：
    1. 将中文文本编码为 UTF-8 字节
    2. 将这些字节误当作 Latin-1 解码（产生乱码）
    
    这就是中继服务器发生的错误！
    """
    utf8_bytes = text.encode('utf-8')
    garbled = utf8_bytes.decode('latin-1')
    return garbled


def test_fix_garbled():
    """测试编码修复功能"""
    print("=" * 60)
    print("测试 1：修复单个中文字符")
    print("=" * 60)
    
    original = "女"
    garbled = simulate_double_encoding(original)
    fixed = _fix_garbled(garbled)
    print(f"原始文本: {original}")
    print(f"模拟乱码: {garbled}")
    print(f"修复结果: {fixed}")
    print(f"测试通过: {fixed == original}")
    print()
    
    print("=" * 60)
    print("测试 2：修复中文标题")
    print("=" * 60)
    
    original = "女神的冒险"
    garbled = simulate_double_encoding(original)
    fixed = _fix_garbled(garbled)
    print(f"原始文本: {original}")
    print(f"模拟乱码: {garbled}")
    print(f"修复结果: {fixed}")
    print(f"测试通过: {fixed == original}")
    print()
    
    print("=" * 60)
    print("测试 3：修复 JSON 对象中的中文")
    print("=" * 60)
    
    original_json = {
        "success": True,
        "title": "女神的冒险",
        "author": "Woody",
        "message": "推送成功"
    }
    # 模拟双重编码
    garbled_json = {
        "success": True,
        "title": simulate_double_encoding(original_json["title"]),
        "author": simulate_double_encoding(original_json["author"]),
        "message": simulate_double_encoding(original_json["message"])
    }
    fixed_json = _fix_garbled(garbled_json)
    print(f"原始 JSON: {original_json}")
    print(f"乱码 JSON: {garbled_json}")
    print(f"修复 JSON: {fixed_json}")
    print(f"测试通过: {fixed_json['title'] == original_json['title'] and fixed_json['message'] == original_json['message']}")
    print()
    
    print("=" * 60)
    print("测试 4：修复包含中文的列表")
    print("=" * 60)
    
    originals = ["女", "教育", "科技", "人工智能"]
    garbled_list = [simulate_double_encoding(t) for t in originals]
    fixed_list = _fix_garbled(garbled_list)
    print(f"原始列表: {originals}")
    print(f"乱码列表: {garbled_list}")
    print(f"修复列表: {fixed_list}")
    print(f"测试通过: {fixed_list == originals}")
    print()
    
    print("=" * 60)
    print("测试 5：已经是正确编码的字符串（不应被修改）")
    print("=" * 60)
    
    normal_text = "女神的冒险"
    fixed_normal = _fix_garbled(normal_text)
    print(f"正常输入: {normal_text}")
    print(f"修复输出: {fixed_normal}")
    print(f"是否被修改: {fixed_normal != normal_text}")
    print(f"注意：正确编码的文本可能会被误修复（这是已知限制）")
    print()
    
    print("=" * 60)
    print("测试 6：混合内容（字典中包含列表）")
    print("=" * 60)
    
    original_mixed = {
        "drafts": [
            {"title": "女神的冒险", "media_id": "abc123"},
            {"title": "科技新闻", "media_id": "def456"}
        ],
        "total": 2
    }
    # 模拟双重编码
    garbled_mixed = {
        "drafts": [
            {"title": simulate_double_encoding("女神的冒险"), "media_id": "abc123"},
            {"title": simulate_double_encoding("科技新闻"), "media_id": "def456"}
        ],
        "total": 2
    }
    fixed_mixed = _fix_garbled(garbled_mixed)
    print(f"修复后的草稿列表:")
    for draft in fixed_mixed['drafts']:
        print(f"  - {draft['title']} (media_id: {draft['media_id']})")
    print(f"测试通过: {fixed_mixed['drafts'][0]['title'] == '女神的冒险'}")
    print()
    
    print("=" * 60)
    print("所有测试完成！")
    print("=" * 60)
    print()
    print("⚠️  注意事项：")
    print("   - _fix_garbled 可以修复真正的双重编码乱码")
    print("   - 但对于本来就是正确 UTF-8 的文本，可能会误修复")
    print("   - 在实际应用中，这通常不是问题，因为服务器返回的数据要么是乱码，要么不是")
    print("   - 如果服务器返回正确编码，_fix_garbled 会尝试修复但可能失败（捕获异常后返回原文本）")


if __name__ == "__main__":
    test_fix_garbled()
