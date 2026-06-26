#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Quicker OCR 示例 - 使用 Quicker 动作执行截图 OCR
"""

import sys
sys.path.insert(0, 'scripts')

from quicker_connector import QuickerConnector

def main():
    """主函数"""
    print("=" * 60)
    print("Quicker OCR 示例")
    print("=" * 60)

    # 创建连接器
    connector = QuickerConnector(source="csv")

    # 读取动作列表
    print("\n读取动作列表...")
    actions = connector.read_actions()
    print(f"✓ 共读取 {len(actions)} 个动作")

    # 搜索 OCR 相关动作
    print("\n【搜索 OCR 相关动作】")
    ocr_keywords = ["截图OCR", "截图识别", "文字识别", "截图", "识别"]

    all_results = []
    for keyword in ocr_keywords:
        results = connector.search_actions(keyword)
        for action in results:
            if action not in all_results:
                all_results.append(action)

    print(f"✓ 找到 {len(all_results)} 个可能相关的动作")
    for i, action in enumerate(all_results[:10], 1):
        print(f"  {i}. {action.name}")
        if action.description:
            desc = action.description[:50] + "..." if len(action.description) > 50 else action.description
            print(f"     {desc}")

    # 智能匹配
    print("\n【智能匹配 \"截图识别文字\"】")
    matches = connector.match_actions("截图识别文字", top_n=5)
    for i, m in enumerate(matches, 1):
        print(f"  {i}. {m['action'].name} (匹配度: {m['score']*100:.0f}%)")
        print(f"     关键词: {m['matched_keywords']}")

    # 执行匹配度最高的动作
    if matches and matches[0]['score'] > 0.5:
        action = matches[0]['action']
        print(f"\n【执行动作】: {action.name}")
        print(f"  ID: {action.id}")
        print(f"  URI: {action.uri}")

        confirm = input("\n是否执行该动作? (y/n): ").strip().lower()
        if confirm == 'y':
            result = connector.execute_action(action.id)
            print(f"\n执行结果: {'成功' if result.success else '失败'}")
            if result.output:
                print(f"输出: {result.output}")
            if result.error:
                print(f"错误: {result.error}")
    else:
        print("\n未找到匹配度足够的动作")

    print("\n" + "=" * 60)
    print("示例结束")
    print("=" * 60)


if __name__ == "__main__":
    main()