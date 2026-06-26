#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
版本验证脚本 v3.0
作者: zcg007
日期: 2026-03-15

验证workbuddy-add-memory技能所有文件都是v3.0版本
"""

import os
import re
from pathlib import Path

def check_file_version(file_path, expected_version="v3.0"):
    """检查单个文件的版本信息"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read(2000)  # 读取前2000个字符
        
        # 检查版本信息
        if expected_version in content:
            return True, f"✅ {os.path.basename(file_path)}: {expected_version}"
        else:
            # 检查是否有其他版本
            version_match = re.search(r'v\d+\.\d+', content)
            if version_match:
                return False, f"❌ {os.path.basename(file_path)}: {version_match.group()} (期望: {expected_version})"
            else:
                return False, f"❌ {os.path.basename(file_path)}: 未找到版本信息"
    except Exception as e:
        return False, f"❌ {os.path.basename(file_path)}: 读取失败 - {e}"

def main():
    print("🔍 WorkBuddy智能记忆管理系统 v3.0 版本验证")
    print("=" * 60)
    
    skill_dir = Path(__file__).parent
    expected_version = "v3.0"
    
    # 需要检查的核心文件
    core_files = [
        "start_work.py",
        "config_loader.py",
        "task_detector.py",
        "memory_retriever.py",
        "conversation_hook.py",
        "work_preparation.py",
        "SKILL.md",
        "INSTALLATION_AND_TEST.md"
    ]
    
    all_passed = True
    results = []
    
    for file_name in core_files:
        file_path = skill_dir / file_name
        if file_path.exists():
            passed, message = check_file_version(file_path, expected_version)
            results.append((passed, message))
            if not passed:
                all_passed = False
        else:
            results.append((False, f"❌ {file_name}: 文件不存在"))
            all_passed = False
    
    # 输出结果
    print("\n📋 版本验证结果:")
    for passed, message in results:
        print(f"  {message}")
    
    print("\n" + "=" * 60)
    if all_passed:
        print(f"🎉 恭喜！所有核心文件都是 {expected_version} 版本！")
        print("✅ 新版本技能安装和版本统一完成！")
    else:
        print("⚠️  发现版本不一致，请检查上述文件")
    
    # 验证技能功能
    print("\n🔧 功能验证:")
    try:
        from start_work import main as start_work_main
        print("✅ start_work.py: 可导入")
    except Exception as e:
        print(f"❌ start_work.py: 导入失败 - {e}")
        all_passed = False
    
    try:
        from memory_retriever import MemoryRetriever
        print("✅ memory_retriever.py: 可导入")
    except Exception as e:
        print(f"❌ memory_retriever.py: 导入失败 - {e}")
        all_passed = False
    
    print("\n" + "=" * 60)
    if all_passed:
        print("🚀 新版本workbuddy-add-memory v3.0技能已完全安装并验证！")
        print("📁 技能位置:", skill_dir)
        print("📅 版本: v3.0 (2026-03-15)")
        print("👤 作者: zcg007")
    else:
        print("⚠️  需要修复版本不一致或导入问题")

if __name__ == "__main__":
    main()