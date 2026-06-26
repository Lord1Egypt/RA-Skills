#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UniSkill V4 - CNC Quote Example

Industrial use case: CNC machining requirement analysis
"""

import sys
sys.path.insert(0, '..')

from socratic_engine_v4 import SocraticEngineV4
from idea_debater_v4 import HighSpeedDebater


def analyze_cnc_requirement(user_input: str) -> dict:
    """
    Analyze CNC machining requirement
    
    Args:
        user_input: User's requirement description
        
    Returns:
        Analysis result with anchor data and recommendations
    """
    engine = SocraticEngineV4()
    score, prompt, anchor = engine.analyze_clarity(user_input)
    
    result = {
        "input": user_input,
        "clarity_score": score,
        "is_clear": score >= 0.7,
        "anchor": {
            "material": anchor.material,
            "dimensions": anchor.dimensions,
            "quantity": anchor.quantity,
            "process": anchor.process,
            "precision": anchor.precision,
        },
        "missing_params": anchor.missing,
        "prompt": None if prompt == "CLEAR" else prompt
    }
    
    # If clear, suggest processing methods
    if result["is_clear"]:
        debater = HighSpeedDebater()
        debate_result = debater.debate(
            f"CNC加工方案选择: {user_input}",
            ["五轴加工", "三轴加工", "车削加工", "铣削加工"]
        )
        result["recommended_process"] = debate_result.recommended
        result["confidence"] = debate_result.confidence
    
    return result


def main():
    print("=" * 50)
    print("UniSkill V4 - CNC Quote Demo")
    print("=" * 50)
    
    # Test cases
    requirements = [
        "加工50个TC4钛合金零件，外径30mm，精加工，公差±0.02",
        "需要车削100件7075铝，粗加工即可",
        "做个零件",  # Incomplete requirement
    ]
    
    for req in requirements:
        print(f"\n{'='*50}")
        print(f"需求: {req}")
        print("-" * 40)
        
        result = analyze_cnc_requirement(req)
        
        print(f"清晰度: {result['clarity_score']:.2f} ({'✅' if result['is_clear'] else '❌'})")
        
        if result["anchor"]:
            print("\n提取参数:")
            for key, value in result["anchor"].items():
                if value:
                    print(f"  - {key}: {value}")
        
        if result["missing_params"]:
            print(f"\n缺失: {', '.join(result['missing_params'])}")
        
        if result["prompt"]:
            print(f"\n💡 提示: {result['prompt']}")
        
        if result.get("recommended_process"):
            print(f"\n🔧 推荐工艺: {result['recommended_process']}")
            print(f"🎯 置信度: {result['confidence']*100:.1f}%")


if __name__ == "__main__":
    main()