#!/usr/bin/env python3
"""环境检查脚本 - 对应SKILL.md中的Pre-flight Check"""

import sys
import importlib
from pathlib import Path
import os

def check_python_version():
    """检查Python版本"""
    required = (3, 10)
    current = sys.version_info[:2]
    if current >= required:
        print(f"✅ Python {current[0]}.{current[1]}")
        return True
    else:
        print(f"❌ Python {current[0]}.{current[1]} (需要 3.10+)")
        return False

def check_dependencies():
    """检查依赖包"""
    required = [
        'akshare', 'pandas', 'google.generativeai', 
        'pytz', 'tabulate', 'requests', 'markdown'
    ]
    all_ok = True
    for package in required:
        try:
            if '.' in package:
                module = package.split('.')[0]
            else:
                module = package
            importlib.import_module(module)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package}")
            all_ok = False
    return all_ok

def check_env_vars():
    """检查环境变量"""
    env_file = Path(__file__).parent.parent / '.env'
    if env_file.exists():
        print(f"✅ 找到.env文件: {env_file}")
    else:
        print(f"⚠️ 未找到.env文件，将使用环境变量或默认值")
    
    # 检查关键环境变量
    gemini_key = os.getenv('GEMINI_API_KEY')
    if gemini_key:
        print(f"✅ GEMINI_API_KEY 已设置")
    else:
        print(f"⚠️ GEMINI_API_KEY 未设置 (AI分析需要)")
    
    return True

def check_directories():
    """检查目录权限"""
    base_dir = Path(__file__).parent.parent
    dirs_to_check = [
        base_dir / 'data',
        base_dir.parent.parent / 'content' / 'posts'  # Hugo目录
    ]
    
    for dir_path in dirs_to_check:
        try:
            dir_path.mkdir(parents=True, exist_ok=True)
            test_file = dir_path / '.write_test'
            test_file.touch()
            test_file.unlink()
            print(f"✅ 可写入: {dir_path.relative_to(base_dir.parent)}")
        except Exception as e:
            print(f"❌ 无法写入: {dir_path} - {e}")
            return False
    
    return True

def main():
    """主检查函数"""
    print("\n🔍 Stock Review Skill - 环境检查\n")
    
    checks = [
        ("Python版本", check_python_version),
        ("依赖包", check_dependencies),
        ("环境变量", check_env_vars),
        ("目录权限", check_directories),
    ]
    
    results = []
    for name, func in checks:
        print(f"\n--- {name} ---")
        result = func()
        results.append(result)
    
    print("\n" + "="*40)
    if all(results):
        print("✅ 所有检查通过！可以运行Stock Review Skill")
        return 0
    else:
        print("❌ 部分检查未通过，请根据提示修复")
        return 1

if __name__ == '__main__':
    sys.exit(main())