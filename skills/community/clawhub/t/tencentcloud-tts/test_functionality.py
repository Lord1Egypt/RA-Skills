#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
腾讯云语音合成Skill包基础功能测试脚本
验证skill包的核心功能和配置
"""

import os
import sys
import time
from pathlib import Path

# 添加skill包路径
sys.path.append(str(Path(__file__).parent / "scripts"))


def test_configuration():
    """测试配置是否正确"""
    print("🔧 测试配置检查...")
    
    # 检查必需的环境变量
    required_vars = ["TENCENTCLOUD_SECRET_ID", "TENCENTCLOUD_SECRET_KEY"]
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print("❌ 缺失必需的环境变量: {}".format(', '.join(missing_vars)))
        print("💡 请设置环境变量:")
        for var in missing_vars:
            print("   export {}=\"your-value\"".format(var))
        return False
    else:
        print("✅ 配置检查通过")
        return True


def test_import():
    """测试模块导入"""
    print("📦 测试模块导入...")
    
    try:
        from tencent_tts import TextToSpeech
        print("✅ 模块导入成功")
        return True
    except ImportError as e:
        print("❌ 模块导入失败: {}".format(e))
        return False


def test_class_instantiation():
    """测试类实例化"""
    print("🏗️  测试类实例化...")
    
    try:
        from tencent_tts import TextToSpeech
        
        # 测试环境变量方式
        tts = TextToSpeech()
        print("✅ 环境变量方式实例化成功")
        
        return True
        
    except Exception as e:
        print("❌ 类实例化失败: {}".format(e))
        return False


def test_method_signatures():
    """测试方法签名"""
    print("📝 测试方法签名...")
    
    try:
        from tencent_tts import TextToSpeech
        
        tts = TextToSpeech()
        
        # 检查方法是否存在
        methods = ['synthesize']
        for method in methods:
            if hasattr(tts, method):
                print("✅ 方法存在: {}".format(method))
            else:
                print("❌ 方法不存在: {}".format(method))
                return False
        
        return True
        
    except Exception as e:
        print("❌ 方法签名测试失败: {}".format(e))
        return False


def test_parameter_validation():
    """测试参数验证"""
    print("🔍 测试参数验证...")
    
    try:
        from tencent_tts import TextToSpeech
        
        tts = TextToSpeech()
        
        # 测试空文本验证
        try:
            result = tts.synthesize(text="")
            print("❌ 空文本验证失败: 应该抛出异常")
            return False
        except ValueError:
            print("✅ 空文本验证通过")
        
        # 测试无效语音类型
        try:
            result = tts.synthesize(text="测试", voice_type=999999)
            print("❌ 无效语音类型验证失败: 应该抛出异常")
            return False
        except ValueError:
            print("✅ 无效语音类型验证通过")
        
        # 测试无效音频格式
        try:
            result = tts.synthesize(text="测试", codec="invalid")
            print("❌ 无效音频格式验证失败: 应该抛出异常")
            return False
        except ValueError:
            print("✅ 无效音频格式验证通过")
        
        return True
        
    except Exception as e:
        print("❌ 参数验证测试失败: {}".format(e))
        return False


def test_file_structure():
    """测试文件结构"""
    print("📁 测试文件结构...")
    
    required_files = [
        "SKILL.md",
        "README.md", 
        "scripts/tencent_tts.py",
        "examples/basic_usage.py",
        "requirements.txt"
    ]
    
    base_path = Path(__file__).parent
    
    all_exist = True
    for file_path in required_files:
        full_path = base_path / file_path
        if full_path.exists():
            print("✅ 文件存在: {}".format(file_path))
        else:
            print("❌ 文件缺失: {}".format(file_path))
            all_exist = False
    
    return all_exist


def generate_test_report(results):
    """生成测试报告"""
    print("\n" + "="*50)
    print("📊 测试报告")
    print("="*50)
    
    total_tests = len(results)
    passed_tests = sum(1 for result in results.values() if result)
    
    print("总测试数: {}".format(total_tests))
    print("通过数: {}".format(passed_tests))
    print("失败数: {}".format(total_tests - passed_tests))
    print("通过率: {:.1f}%".format(passed_tests/total_tests*100))
    
    print("\n详细结果:")
    for test_name, result in results.items():
        status = "✅ 通过" if result else "❌ 失败"
        print("  {}: {}".format(status, test_name))
    
    if passed_tests == total_tests:
        print("\n🎉 所有测试通过！skill包功能完整。")
    else:
        print("\n⚠️  有 {} 个测试失败，请检查相关问题。".format(total_tests - passed_tests))


def main():
    """主测试函数"""
    print("🧪 腾讯云语音合成Skill包基础功能测试")
    print("="*50)
    
    # 运行所有测试
    test_results = {}
    
    test_results["文件结构"] = test_file_structure()
    test_results["模块导入"] = test_import()
    test_results["配置检查"] = test_configuration()
    test_results["类实例化"] = test_class_instantiation()
    test_results["方法签名"] = test_method_signatures()
    test_results["参数验证"] = test_parameter_validation()
    
    # 生成测试报告
    generate_test_report(test_results)
    
    # 提供后续步骤建议
    print("\n💡 后续步骤:")
    if all(test_results.values()):
        print("1. 运行示例代码验证实际功能:")
        print("   python examples/basic_usage.py")
        print("2. 集成到您的项目中使用")
    else:
        print("1. 修复失败的测试项")
        print("2. 检查环境变量配置")
        print("3. 重新运行测试脚本")
    
    return all(test_results.values())


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)