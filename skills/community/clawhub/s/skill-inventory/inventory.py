#!/usr/bin/env python3
"""
Skill Inventory - 技能目录生成器
扫描已安装的技能，生成 skills.md
"""

import os
import re
import sys
from pathlib import Path
from datetime import datetime

# 自动检测工作目录
# 脚本在 ~/xiaoqing/skills/skill-inventory/inventory.py
SCRIPT_DIR = Path(__file__).resolve().parent
SKILLS_DIR = SCRIPT_DIR.parent  # ~/xiaoqing/skills
WORKSPACE_DIR = SKILLS_DIR.parent  # ~/xiaoqing
OUTPUT_FILE = WORKSPACE_DIR / "skills.md"

def get_trigger_words(skill_dir: Path) -> list:
    """从 SKILL.md 中提取触发词"""
    skill_file = skill_dir / "SKILL.md"
    if not skill_file.exists():
        return []
    
    triggers = []
    content = skill_file.read_text(encoding='utf-8')
    
    # 查找触发词列表（简化版：匹配常见的触发词模式）
    lines = content.split('\n')
    for i, line in enumerate(lines):
        # 匹配触发词表格或列表
        if '触发词' in line or 'trigger' in line.lower():
            # 读取接下来的几行
            for j in range(i+1, min(i+10, len(lines))):
                next_line = lines[j].strip()
                if next_line and not next_line.startswith('#'):
                    # 提取引号中的内容
                    matches = re.findall(r'["「]([^"」]+)["」]', next_line)
                    triggers.extend(matches)
                if next_line.startswith('#') or next_line.startswith('---'):
                    break
    
    return triggers[:5]  # 最多5个

def get_skill_info(skill_dir: Path) -> dict:
    """获取技能元信息"""
    skill_file = skill_dir / "SKILL.md"
    
    info = {
        "name": skill_dir.name,
        "description": "(无描述)",
        "triggers": []
    }
    
    if not skill_file.exists():
        return info
    
    content = skill_file.read_text(encoding='utf-8')
    lines = content.split('\n')
    
    # 查找描述（第一段非注释内容）
    for line in lines:
        line = line.strip()
        if line and not line.startswith('---') and not line.startswith('#'):
            # 移除可能的 frontmatter
            if ':' in line and not line.startswith('name:'):
                info["description"] = line[:100]
                break
            elif line.startswith('description:'):
                # 多行描述
                desc_lines = []
                for j in lines[lines.index(line)+1:]:
                    if j.strip().startswith('---'):
                        break
                    desc_lines.append(j.strip())
                info["description"] = ' '.join(desc_lines)[:100]
                break
    
    # 获取触发词
    info["triggers"] = get_trigger_words(skill_dir)
    
    return info

def generate_skills_md(skills: list, workspace: Path) -> str:
    """生成 skills.md 内容"""
    
    # 技能清单表格
    skill_rows = []
    for s in skills:
        location = f"~/{WORKSPACE_DIR.name}/skills/{s['name']}/"
        skill_rows.append(f"| **{s['name']}** | {s['description']} | {location} |")
    
    # 触发词速查
    trigger_rows = []
    for s in skills:
        if s['triggers']:
            triggers = ', '.join(s['triggers'][:3])
            trigger_rows.append(f"| {s['name']} | {triggers} |")
    
    workspace_name = WORKSPACE_DIR.name
    content = f"""# skills.md - 技能目录

> 本文件由 skill-inventory 自动生成。每次安装新技能后运行 `python3 ~/{workspace_name}/skills/skill-inventory/inventory.py` 更新。

---

## 📋 技能清单

| 技能名称 | 功能描述 | 位置 |
|----------|----------|------|
{chr(10).join(skill_rows)}

---

## 🔑 触发词速查

| 技能 | 触发词 |
|------|--------|
{chr(10).join(trigger_rows) if trigger_rows else "| - | - |"}

---

## 📝 更新日志

- **{datetime.now().strftime('%Y-%m-%d')}**: 自动更新，共 {len(skills)} 个技能
"""
    
    return content

def main():
    """主函数"""
    # 如果命令行指定了路径，覆盖默认值
    global SKILLS_DIR, OUTPUT_FILE, WORKSPACE_DIR
    if len(sys.argv) > 1:
        WORKSPACE_DIR = Path(sys.argv[1]).resolve()
        SKILLS_DIR = WORKSPACE_DIR / "skills"
        OUTPUT_FILE = WORKSPACE_DIR / "skills.md"
    
    print(f"🔍 扫描技能目录: {SKILLS_DIR}")
    print(f"📁 工作目录: {WORKSPACE_DIR}")
    
    # 扫描所有技能子目录
    skills = []
    for item in sorted(SKILLS_DIR.iterdir()):
        if item.is_dir() and not item.name.startswith('.'):
            info = get_skill_info(item)
            skills.append(info)
            print(f"  ✅ {info['name']}: {info['description'][:50]}...")
    
    # 生成内容
    content = generate_skills_md(skills, WORKSPACE_DIR)
    
    # 写入文件
    OUTPUT_FILE.write_text(content, encoding='utf-8')
    
    print(f"\n✅ 已生成技能目录: {OUTPUT_FILE}")
    print(f"   共 {len(skills)} 个技能")

if __name__ == "__main__":
    main()
