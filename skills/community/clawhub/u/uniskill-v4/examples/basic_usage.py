#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UniSkill V4 - Basic Usage Example

Demonstrates:
1. Socratic Engine for requirement analysis
2. Quick debate for decision making
"""

import sys
sys.path.insert(0, '..')

from socratic_engine_v4 import check_clarity, SocraticEngineV4
from idea_debater_v4 import quick_debate, validate_need


def main():
    print("=" * 50)
    print("UniSkill V4 - Basic Usage Demo")
    print("=" * 50)
    
    # ===== Example 1: Check Requirement Clarity =====
    print("\n📋 Example 1: Requirement Clarity Check")
    print("-" * 40)
    
    test_cases = [
        "帮我加工10个TC4零件",
        "需要车削50件7075铝，精度要求±0.02",
        "做个零件"
    ]
    
    for case in test_cases:
        is_clear, prompt = check_clarity(case)
        status = "✅ CLEAR" if is_clear else "❌ NEEDS MORE INFO"
        print(f"\n输入: {case}")
        print(f"状态: {status}")
        if not is_clear:
            print(f"提示: {prompt}")
    
    # ===== Example 2: Multi-Model Debate =====
    print("\n\n" + "=" * 50)
    print("📋 Example 2: Multi-Model Debate")
    print("-" * 40)
    
    problem = "开源框架还是开源应用？"
    solutions = [
        "开源框架，闭源应用",
        "全部开源",
        "全部闭源"
    ]
    
    print(f"\n问题: {problem}")
    print(f"候选方案: {solutions}")
    
    result = quick_debate(problem, solutions)
    
    print(f"\n🏆 推荐方案: {result.recommended}")
    print(f"📊 综合评分: {result.score:.2f}/5.0")
    print(f"🎯 置信度: {result.confidence * 100:.1f}%")
    print(f"\n各方案评分:")
    for name, score in result.details.items():
        print(f"  - {name}: {score:.2f}")
    
    # ===== Example 3: Detailed Anchor Analysis =====
    print("\n\n" + "=" * 50)
    print("📋 Example 3: Detailed Anchor Analysis")
    print("-" * 40)
    
    engine = SocraticEngineV4()
    user_input = "需要加工100个6061铝件，精加工，公差±0.05"
    
    score, prompt, anchor = engine.analyze_clarity(user_input)
    
    print(f"\n输入: {user_input}")
    print(f"清晰度得分: {score:.2f}")
    print(f"\n锚点提取结果:")
    print(f"  - 材料: {anchor.material or '未识别'}")
    print(f"  - 尺寸: {anchor.dimensions or '未识别'}")
    print(f"  - 数量: {anchor.quantity or '未识别'}")
    print(f"  - 工艺: {anchor.process or '未识别'}")
    print(f"  - 精度: {anchor.precision or '未识别'}")
    
    if anchor.missing:
        print(f"\n缺失参数: {', '.join(anchor.missing)}")
    
    print("\n" + "=" * 50)
    print("✅ Demo Complete!")
    print("=" * 50)


if __name__ == "__main__":
    main()