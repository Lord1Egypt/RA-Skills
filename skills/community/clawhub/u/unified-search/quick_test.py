#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Baidu Search 快速测试脚本
运行这个脚本可以验证技能是否正常工作
"""

import sys
import subprocess
import os
import io

# 修复 Windows 控制台编码问题
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 技能目录
SKILL_DIR = os.path.dirname(os.path.abspath(__file__))
SCRIPT_PATH = os.path.join(SKILL_DIR, "scripts", "baidu_search.py")

def print_header(text):
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60)

def test_python_search():
    """测试 Python 脚本搜索"""
    print_header("测试1: Python 脚本搜索")
    
    if not os.path.exists(SCRIPT_PATH):
        print(f"[ERROR] 脚本不存在: {SCRIPT_PATH}")
        return False
    
    print(f"[OK] 脚本存在: {SCRIPT_PATH}")
    
    # 测试搜索
    test_query = "Python 教程"
    print(f"\n[SEARCH] 正在搜索: {test_query}")
    
    try:
        # 使用UTF-8编码运行
        env = os.environ.copy()
        env['PYTHONIOENCODING'] = 'utf-8'
        
        result = subprocess.run(
            [sys.executable, SCRIPT_PATH, test_query, "--format"],
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace',
            env=env
        )
        
        print(f"\n[STDOUT] 标准输出:")
        print(result.stdout)
        
        if result.stderr:
            print(f"\n[STDERR] 标准错误:")
            print(result.stderr)
        
        print("\n[OK] Python 脚本搜索测试完成")
        return True
        
    except Exception as e:
        print(f"\n[ERROR] 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def check_dependencies():
    """检查依赖是否安装"""
    print_header("测试2: 检查依赖")
    
    dependencies = ['requests', 'bs4']
    
    for dep in dependencies:
        try:
            __import__(dep)
            print(f"[OK] {dep} 已安装")
        except ImportError:
            print(f"[ERROR] {dep} 未安装")
            return False
    
    return True

def show_usage():
    """显示使用说明"""
    print_header("使用说明")
    
    print("""
Baidu Search 技能已就绪！

两种使用方式：

1) Playwright 浏览器搜索（推荐）
   - 最稳定、最可靠
   - 可以处理验证码
   - 使用 browser 工具

2) Python 脚本搜索（快速）
   - 一行命令搞定
   - 适合简单搜索
   - 可能遇到验证码

快速开始：

# Python 脚本搜索
cd skills/baidu-search
python scripts/baidu_search.py "你的搜索词"
python scripts/baidu_search.py "你的搜索词" --format

# 浏览器搜索（推荐）
查看 SKILL.md 获取详细说明

提示：遇到验证码时，请使用浏览器搜索方式！
""")

def main():
    print("\nBaidu Search 快速测试")
    print("="*60)
    
    # 检查依赖
    deps_ok = check_dependencies()
    
    # 测试 Python 搜索
    search_ok = test_python_search()
    
    # 显示结果
    print_header("测试结果")
    
    if deps_ok and search_ok:
        print("[OK] 所有测试通过！")
    else:
        print("[WARN] 部分测试失败，请查看上面的输出")
    
    # 显示使用说明
    show_usage()

if __name__ == "__main__":
    main()
