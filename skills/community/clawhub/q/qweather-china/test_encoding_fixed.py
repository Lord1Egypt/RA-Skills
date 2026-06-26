#!/usr/bin/env python3
"""
测试编码修复
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from encoding_utils import safe_print, setup_encoding, remove_all_unsupported_chars

def test_encoding():
    """测试编码处理"""
    info = setup_encoding()
    
    safe_print("=" * 50)
    safe_print("编码处理测试")
    safe_print(f"平台: {info['platform']}, 编码: {info['encoding']}")
    safe_print("=" * 50)
    
    # 测试各种字符
    test_cases = [
        "正常中文文本",
        "ASCII text",
        "混合文本 mixed text",
        "🌤️ 北京天气 🌡️25°C",
        "✅ 测试通过 ❌ 测试失败",
        "📅 2026-03-15 📍 北京",
        "💧 湿度 60% 🌬️ 风力 3级",
        "☀️ 晴天 🌙 夜晚 ☁️ 多云",
        "🌧️ 下雨 ⛈️ 雷雨 🌨️ 下雪",
        "🔍 搜索 💡 提示 📝 笔记",
    ]
    
    for i, text in enumerate(test_cases, 1):
        safe_print(f"\n测试 {i}:")
        safe_print(f"  原始: {text}")
        safe_print(f"  处理: {remove_all_unsupported_chars(text)}")
        safe_print(f"  输出: ", end="")
        safe_print(text)
    
    safe_print("\n" + "=" * 50)
    safe_print("测试完成")
    safe_print("=" * 50)
    
    return True

if __name__ == "__main__":
    try:
        test_encoding()
        safe_print("\n✅ 编码处理测试通过")
    except Exception as e:
        safe_print(f"\n❌ 测试失败: {str(e)}")
        sys.exit(1)