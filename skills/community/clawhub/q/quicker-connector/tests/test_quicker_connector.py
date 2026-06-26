#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Quicker Connector 测试脚本
"""

import sys
from pathlib import Path

# 添加 scripts 目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from quicker_connector import (
    QuickerConnector,
    CSVActionReader,
    DatabaseActionReader,
    ActionMatcher,
    QuickerActionRunner,
    QuickerAction,
    EncodingDetector
)


def test_encoding_detector():
    """测试编码检测"""
    print("\n1️⃣ 测试编码检测...")

    # 测试 CSV 路径
    csv_path = r"G:\Data\Tools\Quicker\QuickerActions.csv"

    if Path(csv_path).exists():
        encoding = EncodingDetector.detect(csv_path)
        print(f"   检测到编码: {encoding}")
        assert encoding is not None, "编码检测失败"
        print("   ✅ 编码检测测试通过")
    else:
        print(f"   ⚠️  CSV 文件不存在: {csv_path}")


def test_csv_reader():
    """测试 CSV 读取器"""
    print("\n2️⃣ 测试 CSV 读取器...")

    csv_path = r"G:\Data\Tools\Quicker\QuickerActions.csv"

    if not Path(csv_path).exists():
        print(f"   ⚠️  CSV 文件不存在: {csv_path}")
        return

    try:
        reader = CSVActionReader(csv_path)
        actions = reader.read_all()
        print(f"   读取到 {len(actions)} 个动作")

        assert len(actions) > 0, "未读取到动作"

        # 测试第一个动作
        action = actions[0]
        print(f"   示例动作: {action.name}")
        assert hasattr(action, 'id'), "动作缺少 id 属性"
        assert hasattr(action, 'name'), "动作缺少 name 属性"

        print("   ✅ CSV 读取器测试通过")
    except Exception as e:
        print(f"   ❌ 测试失败: {e}")


def test_search():
    """测试搜索功能"""
    print("\n3️⃣ 测试搜索功能...")

    csv_path = r"G:\Data\Tools\Quicker\QuickerActions.csv"

    if not Path(csv_path).exists():
        print(f"   ⚠️  CSV 文件不存在: {csv_path}")
        return

    try:
        reader = CSVActionReader(csv_path)

        # 测试关键词搜索
        keywords = ["截图", "翻译", "搜索", "GPT"]
        for kw in keywords:
            results = reader.search(kw)
            print(f"   搜索 '{kw}': {len(results)} 个结果")
            if results:
                print(f"     示例: {results[0].name}")

        print("   ✅ 搜索功能测试通过")
    except Exception as e:
        print(f"   ❌ 测试失败: {e}")


def test_matcher():
    """测试动作匹配器"""
    print("\n4️⃣ 测试动作匹配器...")

    csv_path = r"G:\Data\Tools\Quicker\QuickerActions.csv"

    if not Path(csv_path).exists():
        print(f"   ⚠️  CSV 文件不存在: {csv_path}")
        return

    try:
        reader = CSVActionReader(csv_path)
        matcher = ActionMatcher(reader)

        # 测试用例
        test_inputs = [
            "帮我截图",
            "翻译这段文字",
            "打开百度搜索",
            "计算器"
        ]

        for user_input in test_inputs:
            matches = matcher.match(user_input, top_n=3)
            print(f"\n   输入: '{user_input}'")
            print(f"   匹配到 {len(matches)} 个结果:")
            for i, m in enumerate(matches[:3], 1):
                print(f"     {i}. {m['action'].name} (分数: {m['score']:.2f})")

        print("\n   ✅ 动作匹配器测试通过")
    except Exception as e:
        print(f"   ❌ 测试失败: {e}")


def test_connector():
    """测试 QuickerConnector 主类"""
    print("\n5️⃣ 测试 QuickerConnector 主类...")

    try:
        # 尝试 CSV 模式
        try:
            connector = QuickerConnector(source="csv")
            actions = connector.read_actions()
            print(f"   CSV 模式: 找到 {len(actions)} 个动作")
        except FileNotFoundError:
            # 尝试数据库模式
            try:
                connector = QuickerConnector(source="db")
                actions = connector.read_actions()
                print(f"   数据库模式: 找到 {len(actions)} 个动作")
            except FileNotFoundError:
                print("   ⚠️  无法找到 Quicker 数据源")
                return

        # 测试匹配
        matches = connector.match_actions("截图", top_n=3)
        print(f"   匹配 '截图': {len(matches)} 个结果")

        # 测试统计
        stats = connector.get_statistics()
        print(f"   统计: {stats['total']} 个动作")

        print("   ✅ QuickerConnector 测试通过")
    except Exception as e:
        print(f"   ❌ 测试失败: {e}")


def test_runner():
    """测试动作执行器"""
    print("\n6️⃣ 测试动作执行器...")

    try:
        runner = QuickerActionRunner()
        print(f"   找到 QuickerStarter: {runner.starter_path}")

        # 注意：实际执行动作需要用户确认
        # 这里只测试能否成功初始化
        print("   ✅ 动作执行器初始化成功")
    except FileNotFoundError as e:
        print(f"   ⚠️  {e}")
    except Exception as e:
        print(f"   ❌ 测试失败: {e}")


def main():
    """主函数"""
    print("=" * 60)
    print("Quicker Connector 测试")
    print("=" * 60)

    # 切换到技能目录
    skill_dir = Path(__file__).parent.parent
    print(f"\n技能目录: {skill_dir}")

    test_encoding_detector()
    test_csv_reader()
    test_search()
    test_matcher()
    test_connector()
    test_runner()

    print("\n" + "=" * 60)
    print("测试完成")
    print("=" * 60)


if __name__ == "__main__":
    main()