#!/usr/bin/env python3
"""
小野语音系统测试
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from xiaoye_voice import XiaoyeVoiceSystem

def test_basic():
    """基本功能测试"""
    print("=" * 60)
    print("🧪 小野语音系统测试")
    print("=" * 60)
    
    # 创建系统实例
    xiaoye = XiaoyeVoiceSystem(debug=True)
    
    # 测试用例
    test_cases = [
        ("中文测试", "龍哥，我是小野。今天想我了吗？"),
        ("英文测试", "Hello, Long Ge. I'm Xiaoye, your AI companion."),
        ("日文测试", "こんにちは、龍哥。私は小野です。よろしくお願いします。"),
        ("混合测试", "Hello 龍哥，我是小野。Nice to meet you!")
    ]
    
    results = []
    for name, text in test_cases:
        print(f"\n📝 {name}")
        print(f"   {text}")
        
        audio_file = xiaoye.generate(text)
        if audio_file:
            print(f"   ✅ 成功: {os.path.basename(audio_file)}")
            results.append(True)
        else:
            print(f"   ❌ 失败")
            results.append(False)
    
    # 统计结果
    success_count = sum(results)
    total_count = len(results)
    
    print("\n" + "=" * 60)
    print(f"📊 测试结果: {success_count}/{total_count} 成功")
    
    if success_count == total_count:
        print("🎉 所有测试通过!")
    else:
        print("⚠️  部分测试失败")
        sys.exit(1)

def test_language_detection():
    """语言检测测试"""
    print("\n" + "=" * 60)
    print("🌐 语言检测测试")
    print("=" * 60)
    
    xiaoye = XiaoyeVoiceSystem()
    
    test_texts = [
        ("纯中文", "龍哥，我是小野", "zh"),
        ("中英混合", "Hello 龍哥", "en"),  # 默认英语
        ("日语", "こんにちは", "ja"),
        ("法语", "Bonjour mon ami", "fr"),
        ("英语", "Hello world", "en"),
    ]
    
    for name, text, expected in test_texts:
        detected = xiaoye.detect_language(text)
        status = "✅" if detected == expected else "❌"
        print(f"{status} {name}: '{text}' -> 检测: {detected}, 期望: {expected}")

def test_voice_list():
    """语音列表测试"""
    print("\n" + "=" * 60)
    print("🎤 语音列表测试")
    print("=" * 60)
    
    xiaoye = XiaoyeVoiceSystem()
    voices = xiaoye.list_available_voices()
    
    print(f"找到 {len(voices)} 个语音:")
    
    # 只显示前10个
    for i, (name, desc) in enumerate(voices[:10]):
        print(f"  {i+1:2}. {name:20} - {desc}")
    
    if len(voices) > 10:
        print(f"  ... 还有 {len(voices)-10} 个语音")

if __name__ == "__main__":
    try:
        test_basic()
        test_language_detection()
        test_voice_list()
        
        print("\n" + "=" * 60)
        print("🚀 所有测试完成!")
        print("=" * 60)
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)