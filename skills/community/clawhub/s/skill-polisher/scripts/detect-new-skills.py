#!/usr/bin/env python3
"""
检测新技能并触发设置成功标准
用法: python3 detect-new-skills.py [--auto-setup]
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path


def get_all_skills() -> list:
    """获取所有技能列表"""
    skills_dir = Path.home() / ".openclaw/workspace/skills"
    if not skills_dir.exists():
        return []
    
    skills = []
    for item in skills_dir.iterdir():
        if item.is_dir() and not item.name.startswith("."):
            if (item / "SKILL.md").exists():
                skills.append(item.name)
    
    return sorted(skills)


def get_expectation_path(skill_name: str) -> Path:
    """获取技能预期文件路径"""
    return Path.home() / ".openclaw/workspace/.skill-polisher/expectations" / f"{skill_name}.json"


def has_expectation(skill_name: str) -> bool:
    """检查技能是否已有成功标准"""
    return get_expectation_path(skill_name).exists()


def detect_new_skills() -> list:
    """检测没有成功标准的技能"""
    all_skills = get_all_skills()
    missing = []
    
    for skill in all_skills:
        if not has_expectation(skill):
            missing.append(skill)
    
    return missing


def generate_expectation_template(skill_name: str) -> dict:
    """根据 SKILL.md 生成预期模板"""
    skill_md_path = Path.home() / ".openclaw/workspace/skills" / skill_name / "SKILL.md"
    
    template = {
        "skill": skill_name,
        "purpose": "",
        "success_criteria": [],
        "failure_modes": [],
        "expected_output": "",
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    }
    
    # 尝试从 SKILL.md 提取信息
    if skill_md_path.exists():
        content = skill_md_path.read_text(encoding="utf-8")
        
        # 提取 description 作为 purpose
        if "description:" in content:
            for line in content.split("\n"):
                if "description:" in line and '"' in line:
                    desc = line.split('"')[1] if '"' in line else ""
                    template["purpose"] = desc
                    break
        
        # 提取 Quick Start 作为预期输出参考
        if "## 快速开始" in content or "## Quick Start" in content:
            template["expected_output"] = "参考 SKILL.md 中的 Quick Start 章节"
    
    return template


def interactive_setup(skill_name: str):
    """交互式设置成功标准"""
    print(f"\n{'='*60}")
    print(f"🎯 为新技能设置成功标准: {skill_name}")
    print(f"{'='*60}\n")
    
    template = generate_expectation_template(skill_name)
    
    print(f"检测到新技能: {skill_name}")
    if template["purpose"]:
        print(f"从 SKILL.md 提取的描述: {template['purpose']}")
    
    print("\n请完善成功标准（直接回车使用建议值）：\n")
    
    # 核心功能
    purpose = input(f"核心功能: ").strip() or template["purpose"]
    
    # 成功标准
    print("\n成功标准（输入多条，空行结束）：")
    criteria = []
    i = 1
    while True:
        line = input(f"  {i}. ").strip()
        if not line:
            break
        criteria.append(line)
        i += 1
    
    # 常见失败
    print("\n常见失败模式（输入多条，空行结束）：")
    failures = []
    i = 1
    while True:
        line = input(f"  {i}. ").strip()
        if not line:
            break
        failures.append(line)
        i += 1
    
    expectation = {
        "skill": skill_name,
        "purpose": purpose,
        "success_criteria": criteria,
        "failure_modes": failures,
        "expected_output": template["expected_output"],
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    }
    
    # 保存
    exp_path = get_expectation_path(skill_name)
    exp_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(exp_path, "w", encoding="utf-8") as f:
        json.dump(expectation, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ 成功标准已保存: {exp_path}")
    return expectation


def auto_setup(skill_name: str) -> dict:
    """自动设置（使用模板）"""
    template = generate_expectation_template(skill_name)
    
    # 添加一些默认的成功标准
    template["success_criteria"] = [
        "任务能够正常完成",
        "输出结果符合预期",
        "用户使用流程顺畅"
    ]
    
    template["failure_modes"] = [
        "执行报错或中断",
        "输出结果不完整或错误",
        "用户无法理解如何使用"
    ]
    
    # 保存
    exp_path = get_expectation_path(skill_name)
    exp_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(exp_path, "w", encoding="utf-8") as f:
        json.dump(template, f, ensure_ascii=False, indent=2)
    
    return template


def print_summary(missing: list, auto_mode: bool = False):
    """打印摘要"""
    if not missing:
        print("\n✅ 所有技能都已设置成功标准")
        return
    
    print(f"\n📋 检测到 {len(missing)} 个技能缺少成功标准:")
    for skill in missing:
        print(f"  - {skill}")
    
    if auto_mode:
        print(f"\n🤖 自动模式: 已为这些技能创建默认成功标准")
        print(f"   请运行 `set-expectation.py --skill <name> --edit` 进行完善")
    else:
        print(f"\n💡 建议: 为这些技能设置成功标准，以便追踪和改进")


def main():
    parser = argparse.ArgumentParser(description="检测新技能并设置成功标准")
    parser.add_argument("--auto-setup", action="store_true", help="自动为新技能创建默认成功标准")
    parser.add_argument("--interactive", "-i", action="store_true", help="交互式设置")
    parser.add_argument("--list", "-l", action="store_true", help="仅列出缺少成功标准的技能")
    
    args = parser.parse_args()
    
    missing = detect_new_skills()
    
    if args.list:
        print_summary(missing)
        return
    
    if args.interactive and missing:
        # 交互式设置
        for skill in missing:
            interactive_setup(skill)
            print()
    elif args.auto_setup and missing:
        # 自动设置
        for skill in missing:
            auto_setup(skill)
            print(f"✅ {skill}: 已创建默认成功标准")
    else:
        # 默认：仅报告
        print_summary(missing, auto_mode=args.auto_setup)
        
        if missing and not args.auto_setup:
            print(f"\n运行以下命令进行设置:")
            print(f"  交互式: python3 detect-new-skills.py --interactive")
            print(f"  自动: python3 detect-new-skills.py --auto-setup")


if __name__ == "__main__":
    main()
