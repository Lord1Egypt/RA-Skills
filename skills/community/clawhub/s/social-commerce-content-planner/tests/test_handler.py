#!/usr/bin/env python3
"""
Social Commerce Content Planner - 测试用例
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from handler import (
    handle, 
    generate_content_topics, 
    generate_content_calendar,
    SEASONAL_TRENDS,
    FESTIVAL_CALENDAR,
    LIVE_SCRIPT_TEMPLATE,
    CONTENT_CHECKLIST
)


def test_handle_topic():
    """测试主题生成功能"""
    result = handle("抖音", "美妆护肤", "topic")
    assert result["success"] == True
    assert result["platform"] == "抖音"
    assert result["category"] == "美妆护肤"
    assert "topics" in result["data"]
    assert result["data"]["topics"]["total"] > 0
    assert len(result["data"]["topics"]["topics"]) > 0
    first_topic = result["data"]["topics"]["topics"][0]
    assert "主题" in first_topic
    assert "内容形式" in first_topic
    print("✓ test_handle_topic 通过")


def test_handle_calendar():
    """测试内容日历生成"""
    result = handle("小红书", "服饰", "calendar", month=6)
    assert result["success"] == True
    assert "calendar" in result["data"]
    assert result["data"]["calendar"]["month"] == 6
    assert len(result["data"]["calendar"]["calendar"]) > 0
    print("✓ test_handle_calendar 通过")


def test_handle_script():
    """测试直播脚本模板"""
    result = handle("抖音", "服饰", "script")
    assert result["success"] == True
    assert "live_script" in result["data"]
    assert "sections" in result["data"]["live_script"]
    assert len(result["data"]["live_script"]["sections"]) > 0
    first_section = result["data"]["live_script"]["sections"][0]
    assert "环节" in first_section
    assert "目的" in first_section
    print("✓ test_handle_script 通过")


def test_handle_checklist():
    """测试内容检查清单"""
    result = handle("快手", "美妆护肤", "checklist")
    assert result["success"] == True
    assert "checklist" in result["data"]
    assert "合规检查" in result["data"]["checklist"]
    assert len(result["data"]["checklist"]["合规检查"]["违禁词"]) > 0
    print("✓ test_handle_checklist 通过")


def test_handle_all():
    """测试完整内容包"""
    result = handle("抖音", "美妆护肤", "all")
    assert result["success"] == True
    expected_keys = ["trend_analysis", "topics", "calendar", "live_script", "checklist"]
    for key in expected_keys:
        assert key in result["data"], f"缺少模块: {key}"
    print("✓ test_handle_all 通过")


def test_generate_content_topics():
    """测试内容主题生成函数"""
    result = generate_content_topics("抖音", "美妆护肤", count=5)
    assert result["platform"] == "抖音"
    assert result["category"] == "美妆护肤"
    assert result["total"] == 5
    assert len(result["topics"]) == 5
    print("✓ test_generate_content_topics 通过")


def test_generate_content_calendar():
    """测试内容日历生成函数"""
    result = generate_content_calendar("小红书", "服饰", month=6)
    assert result["month"] == 6
    assert result["platform"] == "小红书"
    assert result["category"] == "服饰"
    assert len(result["calendar"]) > 0
    has_weekend = any(day["is_weekend"] for day in result["calendar"])
    assert has_weekend
    print("✓ test_generate_content_calendar 通过")


def test_trend_analysis():
    """测试趋势分析数据"""
    assert "美妆护肤" in SEASONAL_TRENDS
    assert "春" in SEASONAL_TRENDS["美妆护肤"]
    assert len(SEASONAL_TRENDS["美妆护肤"]["春"]) > 0
    assert len(FESTIVAL_CALENDAR) > 0
    months = [f["month"] for f in FESTIVAL_CALENDAR]
    assert 1 in months
    assert 11 in months
    print("✓ test_trend_analysis 通过")


def run_all_tests():
    """运行所有测试"""
    print("=" * 60)
    print("Social Commerce Content Planner - 测试套件")
    print("=" * 60)
    print()
    
    tests = [
        test_handle_topic,
        test_handle_calendar,
        test_handle_script,
        test_handle_checklist,
        test_handle_all,
        test_generate_content_topics,
        test_generate_content_calendar,
        test_trend_analysis,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"✗ {test.__name__} 失败: {e}")
            failed += 1
        except Exception as e:
            print(f"✗ {test.__name__} 异常: {e}")
            failed += 1
    
    print()
    print("=" * 60)
    print(f"测试结果: {passed} 通过, {failed} 失败")
    print("=" * 60)
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
