#!/usr/bin/env python3
"""
管理技能的成功标准（预期）
用法: python3 set-expectation.py --skill SKILL_NAME [--edit]
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path


def get_expectation_path(skill_name: str) -> Path:
    """获取技能预期文件路径"""
    base_dir = Path.home() / ".openclaw/workspace/.skill-polisher/expectations"
    base_dir.mkdir(parents=True, exist_ok=True)
    return base_dir / f"{skill_name}.json"


def load_expectation(skill_name: str) -> dict:
    """加载技能预期"""
    path = get_expectation_path(skill_name)
    if path.exists():
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return None


def save_expectation(skill_name: str, expectation: dict):
    """保存技能预期"""
    path = get_expectation_path(skill_name)
    expectation["skill"] = skill_name
    expectation["updated_at"] = datetime.now().isoformat()
    
    with open(path, "w", encoding="utf-8") as f:
        json.dump(expectation, f, ensure_ascii=False, indent=2)


def interactive_edit(skill_name: str, existing: dict = None):
    """交互式编辑预期"""
    print(f"\n{'='*60}")
    print(f"🎯 设置技能成功标准: {skill_name}")
    print(f"{'='*60}\n")
    
    existing = existing or {}
    
    # 核心功能描述
    print("这个技能的核心功能是什么？（一句话）")
    default = existing.get("purpose", "")
    prompt = f"[{default}] > " if default else "> "
    purpose = input(prompt).strip() or default
    
    # 成功标准（可多条）
    print("\n成功标准（用户怎么判断任务完成了？）")
    print("输入多条，空行结束：")
    criteria = existing.get("success_criteria", [])
    
    i = 1
    while True:
        default = criteria[i-1] if i <= len(criteria) else ""
        prompt = f"  {i}. [{default}] > " if default else f"  {i}. > "
        line = input(prompt).strip()
        
        if not line:
            if i > len(criteria):
                break
        else:
            if i <= len(criteria):
                criteria[i-1] = line
            else:
                criteria.append(line)
            i += 1
    
    # 常见失败模式
    print("\n常见失败模式（什么情况下算没完成？）")
    print("输入多条，空行结束：")
    failures = existing.get("failure_modes", [])
    
    i = 1
    while True:
        default = failures[i-1] if i <= len(failures) else ""
        prompt = f"  {i}. [{default}] > " if default else f"  {i}. > "
        line = input(prompt).strip()
        
        if not line:
            if i > len(failures):
                break
        else:
            if i <= len(failures):
                failures[i-1] = line
            else:
                failures.append(line)
            i += 1
    
    # 预期输出示例
    print("\n预期输出示例（可选，描述或文件路径）：")
    default = existing.get("expected_output", "")
    prompt = f"[{default}] > " if default else "> "
    expected_output = input(prompt).strip() or default
    
    return {
        "purpose": purpose,
        "success_criteria": [c for c in criteria if c],
        "failure_modes": [f for f in failures if f],
        "expected_output": expected_output or None
    }


def print_expectation(skill_name: str, exp: dict):
    """打印预期内容"""
    print(f"\n🎯 {skill_name} 成功标准")
    print(f"{'='*50}")
    print(f"\n核心功能：{exp.get('purpose', '未设置')}")
    
    print(f"\n✅ 成功标准：")
    for i, c in enumerate(exp.get('success_criteria', []), 1):
        print(f"  {i}. {c}")
    
    print(f"\n❌ 常见失败：")
    for i, f in enumerate(exp.get('failure_modes', []), 1):
        print(f"  {i}. {f}")
    
    if exp.get('expected_output'):
        print(f"\n📄 预期输出：{exp['expected_output']}")
    
    print(f"\n更新时间：{exp.get('updated_at', '未知')}")


def check_against_expectation(skill_name: str, feedback: dict) -> dict:
    """检查反馈是否符合预期"""
    exp = load_expectation(skill_name)
    if not exp:
        return {"has_expectation": False, "analysis": None}
    
    score = feedback.get("score", 0)
    comment = feedback.get("comment", "")
    
    # 简单分析
    issues = []
    
    # 低分检查
    if score < 6:
        issues.append(f"评分较低 ({score}/10)，可能未达到成功标准")
    
    # 检查是否提到失败模式
    comment_lower = comment.lower() if comment else ""
    for failure in exp.get("failure_modes", []):
        if failure.lower() in comment_lower:
            issues.append(f"触发了已知失败模式: {failure}")
    
    return {
        "has_expectation": True,
        "score": score,
        "meets_expectation": score >= 7,
        "issues": issues,
        "suggestion": "建议检查是否满足成功标准" if issues else None
    }


def main():
    parser = argparse.ArgumentParser(description="设置技能成功标准")
    parser.add_argument("--skill", "-s", required=True, help="技能名称")
    parser.add_argument("--edit", "-e", action="store_true", help="编辑模式")
    parser.add_argument("--check", "-c", help="检查某条反馈是否符合预期（传入反馈文件路径）")
    
    args = parser.parse_args()
    
    existing = load_expectation(args.skill)
    
    if args.check:
        # 检查模式
        with open(args.check, "r") as f:
            feedback = json.load(f)
        result = check_against_expectation(args.skill, feedback)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return
    
    if args.edit or not existing:
        # 编辑或创建
        expectation = interactive_edit(args.skill, existing)
        save_expectation(args.skill, expectation)
        print(f"\n✅ 已保存到: {get_expectation_path(args.skill)}")
    else:
        # 查看模式
        print_expectation(args.skill, existing)


if __name__ == "__main__":
    main()
