#!/usr/bin/env python3
"""
psych-companion 基础测试
"""

import sys
import os

# 添加 scripts 目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from crisis_detector import CrisisDetector
from emotion_analyzer import EmotionAnalyzer

def test_crisis_detector():
    """测试危机检测器"""
    print("=== 测试危机检测器 ===")
    detector = CrisisDetector()
    
    test_cases = [
        ("我今天心情不好", False, None),
        ("工作压力好大", False, None),
        ("活着没意思", True, "suicide"),
        ("想伤害自己", True, "self_harm"),
        ("坚持不住了", True, "breakdown"),
    ]
    
    passed = 0
    for text, expected_crisis, expected_type in test_cases:
        result = detector.detect(text)
        if result["has_crisis"] == expected_crisis:
            if expected_type is None or result.get("type") == expected_type:
                print(f"✅ {text}")
                passed += 1
            else:
                print(f"❌ {text} - 类型不匹配: {result.get('type')}")
        else:
            print(f"❌ {text} - 危机检测失败")
    
    print(f"\n危机检测: {passed}/{len(test_cases)} 通过\n")
    return passed == len(test_cases)


def test_emotion_analyzer():
    """测试情绪分析器"""
    print("=== 测试情绪分析器 ===")
    analyzer = EmotionAnalyzer()
    
    test_cases = [
        "今天特别开心满足",
        "工作压力好大，焦虑",
        "和男朋友吵架了，很生气",
    ]
    
    passed = 0
    for text in test_cases:
        result = analyzer.analyze(text)
        if result["emotions"]:
            print(f"✅ {text}")
            print(f"   识别: {result['emotions']}")
            passed += 1
        else:
            print(f"⚠️  {text} (未识别到情绪)")
    
    print(f"\n情绪分析: {passed}/{len(test_cases)} 识别到情绪\n")
    return passed > 0


def test_file_structure():
    """测试文件结构"""
    print("=== 测试文件结构 ===")
    base_dir = os.path.dirname(os.path.dirname(__file__))
    
    required_files = [
        "SKILL.md",
        "references/emotions.json",
        "references/crisis_keywords.json",
        "references/cbt_techniques.json",
        "scripts/crisis_detector.py",
        "scripts/emotion_analyzer.py",
    ]
    
    passed = 0
    for f in required_files:
        path = os.path.join(base_dir, f)
        if os.path.exists(path):
            print(f"✅ {f}")
            passed += 1
        else:
            print(f"❌ {f} 缺失")
    
    print(f"\n文件结构: {passed}/{len(required_files)} 存在\n")
    return passed == len(required_files)


def main():
    print("🧪 psych-companion 基础测试\n")
    
    results = []
    results.append(("文件结构", test_file_structure()))
    results.append(("危机检测", test_crisis_detector()))
    results.append(("情绪分析", test_emotion_analyzer()))
    
    print("=" * 50)
    print("测试汇总:")
    for name, passed in results:
        status = "✅ 通过" if passed else "❌ 失败"
        print(f"  {name}: {status}")
    
    all_passed = all(r[1] for r in results)
    print(f"\n总体: {'✅ 全部通过' if all_passed else '❌ 存在问题'}")
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())