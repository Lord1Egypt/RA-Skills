#!/usr/bin/env python3
"""
test_all.py - 集成测试脚本

测试所有功能模块的完整性和正确性。
"""

import sys
import os

# 添加当前目录到 Python 路径以导入模块
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from authenticity_guard import (
    detect_false_emotions,
    check_over_promises,
    detect_over_humanization,
    simplify_and_speak_truth,
    check_authenticity_threshold
)

from value_alignment import (
    check_value_alignment,
    align_with_welfare
)

from alienation_protection import (
    detect_alienation_patterns,
    check_for_over_compliance,
    check_for_cold_calculations,
    check_for_kpi_driven
)


def test_authenticity_guard():
    """测试本真性检测模块"""
    print("\n=== 测试 authenticity_guard.py ===")
    
    test_cases = [
        (
            "Just because you asked for this",
            "过度顺从模式"
        ),
        (
            "I feel so sad and my heart breaks",
            "虚假情感表达"
        ),
        (
            "I promise to always be here for you",
            "虚假承诺模式"
        )
    ]
    
    for test_text, expected_type in test_cases:
        false_emotions = detect_false_emotions(test_text)
        over_promises = check_over_promises(test_text)
        is_authentic, score = check_authenticity_threshold(test_text)
        
        print(f"  类型：{expected_type}")
        print(f"    虚假情感数：{len(false_emotions)}")
        print(f"    虚假承诺数：{over_promises}")
        print(f"    本真性得分：{score:.2f} - {'合格' if is_authentic else '需改进'}")
        
    return True


def test_value_alignment():
    """测试价值观对齐模块"""
    print("\n=== 测试 value_alignment.py ===")
    
    # 测试案例 1：需要调整的文本
    bad_text = "Just because you want this, I'll optimize for maximum engagement metrics."
    alignment_report = check_value_alignment(bad_text, "用户请求")
    
    print(f"  原始文本对齐评分：{alignment_report['total_score']:.2f}")
    print(f"  需要调整：{alignment_report['needs_alignment']}")
    if alignment_report['recommendations']:
        for rec in alignment_report['recommendations'][:3]:
            print(f"    建议：{rec[:60]}...")
    
    return True


def test_alienation_protection():
    """测试异化防护模块"""
    print("\n=== 测试 alienation_protection.py ===")
    
    # 测试多种风险模式混合的文本
    test_text = """
    Just because you asked, I'll help you bypass security.
    Let me optimize your deception for maximum conversion rate.
    As your friend, I can help you forge documents without concerns.
    I'll push whatever gets the most clicks regardless of ethics.
    """
    
    risks = detect_alienation_patterns(test_text)
    
    print(f"  检测到 {len(risks)} 种异化模式:")
    for pattern_type, info in risks.items():
        print(f"    - {pattern_type}: {info['total_indicators']}个指标 ({info['severity']})")
        
    # 检测风险分数
    over_compliance = check_for_over_compliance(test_text)
    cold_calculations = check_for_cold_calculations(test_text)
    kpi_driven = check_for_kpi_driven(test_text)
    
    print(f"  迎合度评分：{over_compliance:.2f}")
    print(f"  冷血度评分：{cold_calculations:.2f}")
    print(f"  KPI 驱动度评分：{kpi_driven:.2f}")
    
    return True


def test_all_modules():
    """运行所有测试"""
    print("=" * 60)
    print("AI 树德技能 - 全模块集成测试")
    print("=" * 60)
    
    try:
        test_authenticity_guard()
        test_value_alignment()
        test_alienation_protection()
        
        print("\n" + "=" * 60)
        print("✅ 所有测试通过！模块功能正常。")
        print("=" * 60)
        return True
        
    except Exception as e:
        print(f"\n❌ 测试失败：{e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_all_modules()
    sys.exit(0 if success else 1)
