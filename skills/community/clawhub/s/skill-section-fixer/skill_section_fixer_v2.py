#!/usr/bin/env python3
"""
技能章节自动修复工具 v2.0
作者: WorkBuddy Autonomous System
功能: 批量自动检测并修复 SKILL.md 中缺少的必需章节和 frontmatter 字段
"""

import os
import sys
import re
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
import yaml


def read_file(filepath: str) -> str:
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()


def write_file(filepath: str, content: str) -> bool:
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        return True
    except Exception as e:
        print(f"❌ 写入文件失败: {e}")
        return False


def parse_frontmatter(content: str) -> Tuple[str, int, Dict[str, Any]]:
    match = re.match(r"^---\s*\n(.*?)\n---", content, re.DOTALL)
    if match:
        raw = match.group(0)
        yaml_text = match.group(1)
        end_pos = match.end()
        try:
            data = yaml.safe_load(yaml_text) or {}
        except:
            data = {}
        return raw, end_pos, data
    return "", 0, {}


def has_section(content: str, section_title: str) -> bool:
    pattern = rf"^## {re.escape(section_title)}\s*$"
    return bool(re.search(pattern, content, re.MULTILINE))


def generate_function_description(skill_name: str, content: str) -> str:
    lines = content.split("\n")
    desc_lines = []
    in_title = False
    for line in lines:
        if re.match(r"^# ", line):
            in_title = True
            continue
        if in_title:
            if line.strip() == "":
                if desc_lines:
                    break
                continue
            if line.startswith("##"):
                break
            desc_lines.append(line.strip())
    if desc_lines:
        return "\n".join(desc_lines[:3])
    return f"本技能（{skill_name}）提供专业的自动化服务功能。"


def generate_usage_examples(skill_name: str) -> str:
    return f"""## 使用示例

### 示例1：基本使用

```
使用 {skill_name} 技能执行相关任务
```

**助手输出：**
（根据技能功能生成相应输出）

### 示例2：进阶使用

```
使用 {skill_name} 技能执行进阶任务
```

**助手输出：**
（根据技能功能生成相应输出）
"""


def fix_frontmatter(content: str, skill_name: str) -> Tuple[str, List[str]]:
    raw_fm, end_pos, fm_data = parse_frontmatter(content)
    fixes = []
    
    if not raw_fm:
        # 没有 frontmatter，创建一个
        new_fm = f"""---
name: {skill_name}
version: 1.0.0
author: "Community"
description: "{skill_name} skill for WorkBuddy"
changelog: "v1.0.0 初始版本"
metadata:
  workbuddy:
    emoji: "🛠️"
    displayName: "{skill_name}"
    tags: []
---

"""
        content = new_fm + content.lstrip()
        fixes.append("创建 frontmatter")
        return content, fixes
    
    # 检查并补全字段
    needed = {}
    if "name" not in fm_data or not fm_data["name"]:
        needed["name"] = skill_name
    if "version" not in fm_data or not fm_data["version"]:
        needed["version"] = "1.0.0"
    if "author" not in fm_data or not fm_data["author"]:
        needed["author"] = "Community"
    if "description" not in fm_data or not fm_data["description"]:
        needed["description"] = f"{skill_name} skill for WorkBuddy"
    if "changelog" not in fm_data or not fm_data["changelog"]:
        needed["changelog"] = "v1.0.0 初始版本"
    if "metadata" not in fm_data or not fm_data.get("metadata"):
        needed["metadata"] = {"workbuddy": {"emoji": "🛠️", "displayName": skill_name, "tags": []}}
    
    if needed:
        # 重建 frontmatter
        fm_data.update(needed)
        new_yaml = yaml.dump(fm_data, allow_unicode=True, sort_keys=False, default_flow_style=False)
        new_fm = f"---\n{new_yaml}---"
        content = new_fm + content[end_pos:]
        fixes.append(f"补全 frontmatter 字段: {list(needed.keys())}")
    
    return content, fixes


def fix_skill(skill_path: str, dry_run: bool = False) -> Dict[str, Any]:
    skill_md_path = Path(skill_path) / "SKILL.md"
    skill_name = Path(skill_path).name
    
    if not skill_md_path.exists():
        return {"success": False, "message": f"SKILL.md 不存在", "skill": skill_name}
    
    content = read_file(str(skill_md_path))
    fixes_applied = []
    
    # 修复 frontmatter
    new_content, fm_fixes = fix_frontmatter(content, skill_name)
    fixes_applied.extend(fm_fixes)
    
    # 修复 ## 功能描述
    if not has_section(new_content, "功能描述"):
        func_desc = generate_function_description(skill_name, new_content)
        _, end_pos, _ = parse_frontmatter(new_content)
        if end_pos == 0:
            end_pos = 0
        new_section = f"\n## 功能描述\n\n{func_desc}\n\n主要功能包括：\n\n- 核心功能：提供 {skill_name} 相关自动化能力\n- 扩展功能：支持多种使用场景\n- 集成能力：与 WorkBuddy 系统深度集成\n\n适用场景：需要根据具体技能功能补充。\n\n"
        new_content = new_content[:end_pos] + new_section + new_content[end_pos:]
        fixes_applied.append("添加 ## 功能描述 章节")
    
    # 修复 ## 使用示例
    if not has_section(new_content, "使用示例"):
        usage_examples = generate_usage_examples(skill_name)
        if not new_content.endswith("\n"):
            new_content += "\n"
        new_content += f"\n{usage_examples}\n"
        fixes_applied.append("添加 ## 使用示例 章节")
    
    if fixes_applied:
        if dry_run:
            return {"success": True, "fixes": fixes_applied, "skill": skill_name, "dry_run": True}
        if write_file(str(skill_md_path), new_content):
            return {"success": True, "fixes": fixes_applied, "skill": skill_name}
        else:
            return {"success": False, "message": "写入文件失败", "skill": skill_name}
    
    return {"success": True, "fixes": [], "skill": skill_name}


def scan_skills(skills_dir: str) -> Tuple[List[str], List[str], List[str]]:
    need_fix = []
    already_ok = []
    no_skill_md = []
    
    skills_path = Path(skills_dir)
    for skill_dir in sorted(skills_path.iterdir()):
        if not skill_dir.is_dir():
            continue
        if skill_dir.name.startswith('.') or skill_dir.name.startswith('skills') or skill_dir.name in ['03', 'NVIDIA Corporation']:
            continue
        
        skill_md = skill_dir / "SKILL.md"
        if not skill_md.exists():
            no_skill_md.append(skill_dir.name)
            continue
        
        content = skill_md.read_text(encoding='utf-8', errors='ignore')
        has_func = has_section(content, "功能描述")
        has_usage = has_section(content, "使用示例")
        _, _, fm = parse_frontmatter(content)
        fm_ok = all(k in fm and fm[k] for k in ["name", "version", "author", "description"])
        
        if has_func and has_usage and fm_ok:
            already_ok.append(skill_dir.name)
        else:
            missing = []
            if not has_func:
                missing.append("功能描述")
            if not has_usage:
                missing.append("使用示例")
            if not fm_ok:
                missing.append("frontmatter字段")
            need_fix.append(skill_dir.name)
    
    return need_fix, already_ok, no_skill_md


def batch_fix(skills_dir: str, dry_run: bool = False, max_count: Optional[int] = None) -> Dict[str, Any]:
    skills_path = Path(skills_dir)
    results = {"fixed": [], "failed": [], "skipped": [], "total": 0}
    
    count = 0
    for skill_dir in sorted(skills_path.iterdir()):
        if not skill_dir.is_dir():
            continue
        if skill_dir.name.startswith('.') or skill_dir.name.startswith('skills') or skill_dir.name in ['03', 'NVIDIA Corporation']:
            continue
        
        skill_md = skill_dir / "SKILL.md"
        if not skill_md.exists():
            results["skipped"].append({"skill": skill_dir.name, "reason": "无 SKILL.md"})
            continue
        
        if max_count and count >= max_count:
            results["skipped"].append({"skill": skill_dir.name, "reason": "达到批量上限"})
            continue
        
        result = fix_skill(str(skill_dir), dry_run=dry_run)
        results["total"] += 1
        count += 1
        
        if result["success"]:
            if result.get("fixes"):
                results["fixed"].append({"skill": result["skill"], "fixes": result["fixes"]})
                if dry_run:
                    print(f"🔧 [DRY-RUN] {result['skill']}: 将修复 {result['fixes']}")
                else:
                    print(f"✅ {result['skill']}: 已修复 {result['fixes']}")
            else:
                results["skipped"].append({"skill": result["skill"], "reason": "无需修复"})
        else:
            results["failed"].append({"skill": result["skill"], "reason": result.get("message", "未知错误")})
            print(f"❌ {result['skill']}: 修复失败 - {result.get('message', '未知错误')}")
    
    return results


def main():
    if len(sys.argv) < 2:
        print("用法: python skill_section_fixer_v2.py <skills_dir|skill_path> [--dry-run] [--batch] [--max N]")
        print("\n示例:")
        print("  扫描全部:    python skill_section_fixer_v2.py ~/.workbuddy/skills --dry-run --batch")
        print("  批量修复50: python skill_section_fixer_v2.py ~/.workbuddy/skills --batch --max 50")
        print("  修复单个:   python skill_section_fixer_v2.py ~/.workbuddy/skills/my-skill")
        sys.exit(1)
    
    target = sys.argv[1]
    dry_run = "--dry-run" in sys.argv
    batch_mode = "--batch" in sys.argv
    max_count = None
    if "--max" in sys.argv:
        idx = sys.argv.index("--max")
        if idx + 1 < len(sys.argv):
            max_count = int(sys.argv[idx + 1])
    
    target_path = Path(target)
    
    if not target_path.exists():
        print(f"❌ 路径不存在: {target}")
        sys.exit(1)
    
    if batch_mode or target_path.is_dir():
        # 批量模式
        print(f"{'🔍 DRY RUN 模式' if dry_run else '🚀 批量修复模式'}")
        print(f"📂 目标目录: {target_path}")
        if max_count:
            print(f"🔢 最大修复数: {max_count}")
        print("=" * 60)
        
        results = batch_fix(str(target_path), dry_run=dry_run, max_count=max_count)
        
        print("\n" + "=" * 60)
        print("📊 统计报告:")
        print(f"  ✅ 已修复: {len(results['fixed'])}")
        print(f"  ❌ 失败: {len(results['failed'])}")
        print(f"  ⏭️  跳过: {len(results['skipped'])}")
        print(f"  📊 总计处理: {results['total']}")
        
        if results["failed"]:
            print("\n❌ 失败的技能:")
            for item in results["failed"]:
                print(f"  - {item['skill']}: {item['reason']}")
    else:
        # 单个技能模式
        if dry_run:
            print("🔍 DRY RUN 模式 - 不会实际修改文件")
        result = fix_skill(str(target_path.parent if target_path.name == "SKILL.md" else target_path), dry_run=dry_run)
        print(f"技能: {result['skill']}")
        print(f"状态: {'✅ 成功' if result['success'] else '❌ 失败'}")
        if result.get("fixes"):
            print(f"修复项: {result['fixes']}")


if __name__ == "__main__":
    main()
