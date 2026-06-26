#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
微信自动发送消息技能测试
"""

import sys
import os

# 添加技能目录到路径
skill_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, skill_dir)

def test_import():
    """测试模块导入"""
    print("测试模块导入...")
    
    try:
        import pyautogui
        print("  ✓ pyautogui 导入成功")
    except ImportError as e:
        print(f"  ✗ pyautogui 导入失败: {e}")
        return False
    
    try:
        import pygetwindow
        print("  ✓ pygetwindow 导入成功")
    except ImportError as e:
        print(f"  ✗ pygetwindow 导入失败: {e}")
        return False
    
    try:
        import pyperclip
        print("  ✓ pyperclip 导入成功")
    except ImportError as e:
        print(f"  ✗ pyperclip 导入失败: {e}")
        return False
    
    return True

def test_skill_script():
    """测试技能脚本"""
    print("\n测试技能脚本...")
    
    skill_file = os.path.join(skill_dir, "SKILL.md")
    if os.path.exists(skill_file):
        print(f"  ✓ 技能脚本存在: {skill_file}")
        
        # 检查文件内容
        with open(skill_file, 'r', encoding='utf-8') as f:
            content = f.read()
            if "微信自动发送消息" in content:
                print("  ✓ 技能脚本内容正确")
                return True
            else:
                print("  ✗ 技能脚本内容不正确")
                return False
    else:
        print(f"  ✗ 技能脚本不存在: {skill_file}")
        return False

def test_requirements():
    """测试依赖文件"""
    print("\n测试依赖文件...")
    
    req_file = os.path.join(skill_dir, "requirements.txt")
    if os.path.exists(req_file):
        print(f"  ✓ 依赖文件存在: {req_file}")
        
        with open(req_file, 'r', encoding='utf-8') as f:
            content = f.read()
            required_packages = ['pyautogui', 'pygetwindow', 'pyperclip']
            missing = []
            
            for pkg in required_packages:
                if pkg in content:
                    print(f"    ✓ 包含 {pkg}")
                else:
                    print(f"    ✗ 缺少 {pkg}")
                    missing.append(pkg)
            
            if not missing:
                print("  ✓ 所有必需依赖都已列出")
                return True
            else:
                print(f"  ✗ 缺少依赖: {missing}")
                return False
    else:
        print(f"  ✗ 依赖文件不存在: {req_file}")
        return False

def test_documentation():
    """测试文档文件"""
    print("\n测试文档文件...")
    
    docs = [
        ("README.md", "使用说明"),
        ("EXAMPLES.md", "示例文件"),
        ("技能说明.md", "技能说明"),
        ("技能描述.md", "技能描述")
    ]
    
    all_exist = True
    for filename, description in docs:
        filepath = os.path.join(skill_dir, filename)
        if os.path.exists(filepath):
            print(f"  ✓ {description}存在: {filename}")
        else:
            print(f"  ✗ {description}不存在: {filename}")
            all_exist = False
    
    return all_exist

def main():
    print("=" * 60)
    print("微信自动发送消息技能测试")
    print("=" * 60)
    
    tests = [
        ("模块导入", test_import),
        ("技能脚本", test_skill_script),
        ("依赖文件", test_requirements),
        ("文档文件", test_documentation)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n{test_name}:")
        try:
            result = test_func()
            results.append((test_name, result))
            if result:
                print(f"  → 通过")
            else:
                print(f"  → 失败")
        except Exception as e:
            print(f"  → 错误: {e}")
            results.append((test_name, False))
    
    print("\n" + "=" * 60)
    print("测试结果汇总:")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✓ 通过" if result else "✗ 失败"
        print(f"  {test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\n通过率: {passed}/{total} ({passed/total*100:.1f}%)")
    
    if passed == total:
        print("\n🎉 所有测试通过！技能创建成功。")
        print("\n使用说明:")
        print("1. 确保微信已打开并可见")
        print("2. 安装依赖: pip install pyautogui pygetwindow pyperclip")
        print("3. 测试发送: python SKILL.md \"文件传输助手\" \"测试消息\"")
        return 0
    else:
        print("\n⚠️  部分测试失败，请检查技能配置。")
        return 1

if __name__ == "__main__":
    sys.exit(main())