#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Quicker Connector 测试脚本
"""

import sys
sys.path.insert(0, 'scripts')

from quicker_connector import QuickerConnector, is_initialized

print("=" * 60)
print("Quicker Connector 测试")
print("=" * 60)

print(f"\n初始化状态: {is_initialized()}")

# 创建连接器（会从配置文件读取 CSV 路径）
connector = QuickerConnector(source="csv")

print(f"数据源类型: {connector.source}")

# 读取动作
print("\n读取动作列表...")
try:
    actions = connector.read_actions()
    print(f"✓ 成功读取 {len(actions)} 个动作")

    # 分析动作
    print("\n【动作分析】")
    print(f"  总动作数: {len(actions)}")

    # 搜索 OCR 相关动作
    print("\n【搜索 OCR 相关动作】")
    ocr_results = connector.search_actions("OCR")
    print(f"  找到 {len(ocr_results)} 个 OCR 相关动作")
    for action in ocr_results[:5]:
        print(f"    - {action.name}")

    # 搜索截图相关动作
    print("\n【搜索截图相关动作】")
    screenshot_results = connector.search_actions("截图")
    print(f"  找到 {len(screenshot_results)} 个截图相关动作")
    for action in screenshot_results[:5]:
        print(f"    - {action.name}")

    # 智能匹配
    print("\n【智能匹配 \"截图识别文字\"】")
    matches = connector.match_actions("截图识别文字", top_n=5)
    for i, m in enumerate(matches, 1):
        print(f"  {i}. {m['action'].name} (匹配度: {m['score']*100:.0f}%)")
        print(f"     关键词: {m['matched_keywords']}")

    print("\n" + "=" * 60)
    print("测试完成 ✓")
    print("=" * 60)

except Exception as e:
    print(f"\n✗ 测试失败: {e}")
    import traceback
    traceback.print_exc()