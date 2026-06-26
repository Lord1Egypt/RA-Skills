#!/usr/bin/env python3
"""
技能结构自动修复脚本 - 自动修复审查发现的常见问题

用法:
    fix.py <skill-directory>

示例:
    fix.py .qoder/skills/my-skill
    fix.py .  # 在技能目录内执行
"""

import sys
from pathlib import Path


def create_missing_directories(skill_path: Path) -> list[str]:
    """创建缺失的标准目录"""
    created = []
    
    for dirname in ["scripts", "references", "assets"]:
        dir_path = skill_path / dirname
        if not dir_path.exists():
            dir_path.mkdir(parents=True)
            created.append(dirname)
    
    return created


def fix_skill(skill_path: Path) -> dict:
    """执行所有修复操作"""
    results = {
        "dirs_created": [],
        "errors": []
    }
    
    # 创建缺失目录
    try:
        results["dirs_created"] = create_missing_directories(skill_path)
    except Exception as e:
        results["errors"].append(f"创建目录失败: {e}")
    
    return results


def print_results(results: dict) -> None:
    """输出修复结果"""
    print()
    print("# 自动修复结果")
    print()
    
    if results["dirs_created"]:
        print("✅ 已创建目录:")
        for name in results["dirs_created"]:
            print(f"   - {name}/")
        print()
    
    if results["errors"]:
        print("❌ 修复失败:")
        for error in results["errors"]:
            print(f"   - {error}")
        print()
    
    if not any([results["dirs_created"], results["errors"]]):
        print("ℹ️ 未发现需要修复的问题")
        print()


def main():
    if len(sys.argv) < 2:
        print("用法: fix.py <skill-directory>")
        print("")
        print("示例:")
        print("  fix.py .qoder/skills/my-skill")
        print("  fix.py .  # 在技能目录内执行")
        sys.exit(1)
    
    skill_path = Path(sys.argv[1]).resolve()
    
    if not skill_path.exists():
        print(f"❌ 错误: 目录不存在: {skill_path}")
        sys.exit(1)
    
    results = fix_skill(skill_path)
    print_results(results)
    
    # 如果有错误，返回非零退出码
    if results["errors"]:
        sys.exit(1)


if __name__ == "__main__":
    main()
