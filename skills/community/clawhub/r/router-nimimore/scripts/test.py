#!/usr/bin/env python3
"""
Test Router NIMIMORE
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
from router import SmartRouter


def test_routing():
    """测试路由功能"""
    router = SmartRouter()
    
    test_cases = [
        ("你好", "bailian/qwen-turbo", "简单问候"),
        ("帮我写个Python函数", "bailian/qwen-max", "代码生成"),
        ("分析一下股票走势", "moonshot/kimi-k2.5", "复杂分析"),
        ("谢谢", "bailian/qwen-turbo", "简单感谢"),
    ]
    
    print("=" * 60)
    print("Router NIMIMORE - Test Results")
    print("=" * 60)
    
    passed = 0
    for query, expected, desc in test_cases:
        result = router.route(query)
        actual = result['selected_model']
        success = actual == expected
        
        status = "✅" if success else "❌"
        print(f"\n{status} {desc}")
        print(f"   Query: {query}")
        print(f"   Expected: {expected}")
        print(f"   Actual: {actual}")
        
        if success:
            passed += 1
    
    print("\n" + "=" * 60)
    print(f"Passed: {passed}/{len(test_cases)}")
    print("=" * 60)
    
    return passed == len(test_cases)


if __name__ == "__main__":
    success = test_routing()
    sys.exit(0 if success else 1)
