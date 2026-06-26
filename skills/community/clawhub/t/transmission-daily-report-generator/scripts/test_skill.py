#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试日报报表生成器 skill
"""

import os
import sys

def test_skill_structure():
    """测试 skill 结构是否完整"""
    print("=== 测试 Skill 结构 ===\n")

    skill_dir = "/Users/ahs/.openclaw/workspace/skills/daily-report-generator"

    # 检查必要文件
    required_files = [
        "SKILL.md",
        "scripts/generate_assessment_period_report.py",
        "references/README.md"
    ]

    all_exist = True
    for file_path in required_files:
        full_path = os.path.join(skill_dir, file_path)
        if os.path.exists(full_path):
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} - 不存在")
            all_exist = False

    if all_exist:
        print("\n✅ 所有必要文件都存在")
    else:
        print("\n❌ 部分文件缺失")
        return False

    # 检查 SKILL.md 格式
    print("\n=== 检查 SKILL.md 格式 ===\n")
    skill_md_path = os.path.join(skill_dir, "SKILL.md")
    with open(skill_md_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 检查 frontmatter
    if content.startswith('---'):
        print("✅ 包含 frontmatter")
        frontmatter_end = content.find('---', 3)
        if frontmatter_end > 0:
            frontmatter = content[3:frontmatter_end]
            if 'name:' in frontmatter:
                print("✅ 包含 name 字段")
            if 'description:' in frontmatter:
                print("✅ 包含 description 字段")
            if 'metadata:' in frontmatter:
                print("✅ 包含 metadata 字段")
        else:
            print("❌ frontmatter 格式错误")
            return False
    else:
        print("❌ 缺少 frontmatter")
        return False

    # 检查脚本是否可执行
    print("\n=== 检查脚本 ===\n")
    script_path = os.path.join(skill_dir, "scripts/generate_assessment_period_report.py")
    if os.path.exists(script_path):
        print(f"✅ 脚本存在: {script_path}")
        # 检查脚本语法
        try:
            with open(script_path, 'r', encoding='utf-8') as f:
                script_content = f.read()
            compile(script_content, script_path, 'exec')
            print("✅ 脚本语法正确")
        except SyntaxError as e:
            print(f"❌ 脚本语法错误: {e}")
            return False
    else:
        print(f"❌ 脚本不存在: {script_path}")
        return False

    # 检查新功能
    print("\n=== 检查新功能 ===\n")
    with open(script_path, 'r', encoding='utf-8') as f:
        script_content = f.read()
    
    # 检查全年累计功能
    if '全年累计' in script_content:
        print("✅ 包含全年累计功能")
    else:
        print("❌ 缺少全年累计功能")
        return False
    
    # 检查风险评分过滤功能
    if "风险评分" in script_content and "!= 0" in script_content:
        print("✅ 包含风险评分过滤功能")
    else:
        print("❌ 缺少风险评分过滤功能")
        return False

    print("\n✅ 所有测试通过！")
    return True

if __name__ == '__main__':
    success = test_skill_structure()
    sys.exit(0 if success else 1)
