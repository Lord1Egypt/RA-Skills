#!/usr/bin/env python3
"""
检查技能是否符合 https://agentskills.io/specification
用法: python3 check-spec.py --skill SKILL_NAME [--fix]
"""

import argparse
import json
import re
import sys
from pathlib import Path
from typing import List, Dict, Tuple


def get_skill_path(skill_name: str) -> Path:
    """获取技能目录路径"""
    return Path.home() / ".openclaw/workspace/skills" / skill_name


def check_file_structure(skill_path: Path) -> List[Dict]:
    """检查文件结构"""
    issues = []
    skill_name = skill_path.name
    
    # 检查 SKILL.md 必须在根目录
    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        issues.append({
            "level": "error",
            "type": "missing_skill_md",
            "message": "SKILL.md 不存在（必须在根目录）"
        })
    
    # 检查用户数据是否错误地存放在技能目录内
    user_data_indicators = ['.learnings', 'feedback', 'logs', 'config', 'data', 'user-data']
    for indicator in user_data_indicators:
        if (skill_path / indicator).exists():
            issues.append({
                "level": "error",
                "type": "user_data_in_skill_dir",
                "message": f"发现用户数据目录 '{indicator}' 在技能目录内，应移动到 ~/.openclaw/workspace/.{skill_name}/"
            })
    
    # 检查不建议的文件（警告级别）
    not_recommended_files = ["README.md", "CHANGELOG.md", "VERSION", "version.txt", "requirements.txt"]
    for filename in not_recommended_files:
        if (skill_path / filename).exists():
            issues.append({
                "level": "warning",
                "type": "not_recommended_file",
                "message": f"不建议存在 {filename}，内容应合并到 SKILL.md"
            })
    
    return issues


def check_frontmatter(skill_path: Path, skill_name: str) -> List[Dict]:
    """检查 YAML frontmatter"""
    issues = []
    skill_md = skill_path / "SKILL.md"
    
    if not skill_md.exists():
        return issues
    
    content = skill_md.read_text(encoding="utf-8")
    
    # 检查是否以 --- 开头
    if not content.startswith("---"):
        issues.append({
            "level": "error",
            "type": "frontmatter_start",
            "message": "SKILL.md 必须以 --- 开头"
        })
        return issues
    
    # 提取 frontmatter
    match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
    if not match:
        issues.append({
            "level": "error",
            "type": "frontmatter_end",
            "message": "YAML frontmatter 格式错误，必须以 --- 结束"
        })
        return issues
    
    frontmatter = match.group(1)
    
    # 检查 name 字段
    name_match = re.search(r'^name:\s*(.+)$', frontmatter, re.MULTILINE)
    if not name_match:
        issues.append({
            "level": "error",
            "type": "missing_name",
            "message": "缺少 name 字段"
        })
    else:
        name_value = name_match.group(1).strip()
        if name_value != skill_name:
            issues.append({
                "level": "error",
                "type": "name_mismatch",
                "message": f"name '{name_value}' 与文件夹名 '{skill_name}' 不一致"
            })
    
    # 检查 description 字段
    desc_match = re.search(r'^description:\s*(.+)$', frontmatter, re.MULTILINE)
    if not desc_match:
        issues.append({
            "level": "error",
            "type": "missing_description",
            "message": "缺少 description 字段"
        })
    else:
        desc_value = desc_match.group(1).strip()
        # 去除引号
        if desc_value.startswith('"') and desc_value.endswith('"'):
            desc_value = desc_value[1:-1]
        elif desc_value.startswith("'") and desc_value.endswith("'"):
            desc_value = desc_value[1:-1]
        
        if not desc_value.startswith("当") or "使用" not in desc_value:
            issues.append({
                "level": "warning",
                "type": "description_format",
                "message": "description 建议使用 '当...时使用' 格式"
            })
    
    return issues


def check_naming(skill_name: str) -> List[Dict]:
    """检查命名规范"""
    issues = []
    
    # 检查长度
    if len(skill_name) > 64:
        issues.append({
            "level": "error",
            "type": "name_too_long",
            "message": f"技能名长度 {len(skill_name)} 超过 64 字符限制"
        })
    
    # 检查字符
    if not re.match(r'^[a-z0-9-]+$', skill_name):
        issues.append({
            "level": "error",
            "type": "invalid_chars",
            "message": "技能名只能包含小写字母、数字和连字符"
        })
    
    return issues


def check_scripts(skill_path: Path) -> List[Dict]:
    """检查脚本规范"""
    issues = []
    scripts_dir = skill_path / "scripts"
    
    if not scripts_dir.exists():
        return issues
    
    for script in scripts_dir.iterdir():
        if not script.is_file():
            continue
        
        # 检查 shebang
        with open(script, "r", encoding="utf-8", errors="ignore") as f:
            first_line = f.readline()
        
        if not first_line.startswith("#!/"):
            issues.append({
                "level": "warning",
                "type": "missing_shebang",
                "message": f"{script.name} 缺少 shebang"
            })
        
        # 检查执行权限
        if not script.stat().st_mode & 0o111:
            issues.append({
                "level": "warning",
                "type": "not_executable",
                "message": f"{script.name} 没有执行权限"
            })
    
    return issues


def check_content(skill_path: Path) -> List[Dict]:
    """检查内容规范"""
    issues = []
    skill_md = skill_path / "SKILL.md"
    
    if not skill_md.exists():
        return issues
    
    content = skill_md.read_text(encoding="utf-8")
    
    # 检查 Quick Start
    if "## 快速开始" not in content and "## Quick Start" not in content:
        issues.append({
            "level": "warning",
            "type": "missing_quickstart",
            "message": "缺少 Quick Start 章节"
        })
    
    return issues


def check_skill(skill_name: str) -> Tuple[bool, List[Dict]]:
    """完整检查技能"""
    skill_path = get_skill_path(skill_name)
    
    if not skill_path.exists():
        return False, [{"level": "error", "type": "not_found", "message": f"技能不存在: {skill_name}"}]
    
    all_issues = []
    
    all_issues.extend(check_naming(skill_name))
    all_issues.extend(check_file_structure(skill_path))
    all_issues.extend(check_frontmatter(skill_path, skill_name))
    all_issues.extend(check_content(skill_path))
    all_issues.extend(check_scripts(skill_path))
    
    has_error = any(i["level"] == "error" for i in all_issues)
    
    return not has_error, all_issues


def print_report(skill_name: str, passed: bool, issues: List[Dict]):
    """打印检查报告"""
    print(f"\n{'='*60}")
    status = "✅ 通过" if passed else "❌ 未通过"
    print(f"{status} | {skill_name}")
    print(f"{'='*60}")
    
    if not issues:
        print("  所有检查项均符合规范")
        return
    
    errors = [i for i in issues if i["level"] == "error"]
    warnings = [i for i in issues if i["level"] == "warning"]
    
    if errors:
        print(f"\n🔴 错误 ({len(errors)}):")
        for i, issue in enumerate(errors, 1):
            print(f"  {i}. {issue['message']}")
    
    if warnings:
        print(f"\n🟡 警告 ({len(warnings)}):")
        for i, issue in enumerate(warnings, 1):
            print(f"  {i}. {issue['message']}")


def main():
    parser = argparse.ArgumentParser(description="检查技能是否符合 AgentSkills 规范")
    parser.add_argument("--skill", "-s", required=True, help="技能名称")
    parser.add_argument("--json", action="store_true", help="JSON 格式输出")
    parser.add_argument("--strict", action="store_true", help="将警告也视为错误")
    
    args = parser.parse_args()
    
    passed, issues = check_skill(args.skill)
    
    if args.strict:
        passed = passed and not any(i["level"] == "warning" for i in issues)
    
    if args.json:
        result = {
            "skill": args.skill,
            "passed": passed,
            "strict_mode": args.strict,
            "issues": issues
        }
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print_report(args.skill, passed, issues)
    
    sys.exit(0 if passed else 1)


if __name__ == "__main__":
    main()
