#!/usr/bin/env python3
"""
技能章节自动修复工具
版本: 1.0.0
作者: WorkBuddy Autonomous System
功能: 自动检测并添加 SKILL.md 中缺少的 ## 功能描述 和 ## 使用示例 章节
"""

import os
import sys
import re
from pathlib import Path
from typing import Dict, List, Any, Optional


def read_file(filepath: str) -> str:
    """读取文件内容"""
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()


def write_file(filepath: str, content: str) -> bool:
    """写入文件内容"""
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        return True
    except Exception as e:
        print(f"❌ 写入文件失败: {e}")
        return False


def parse_frontmatter(content: str) -> Dict[str, Any]:
    """解析 frontmatter"""
    match = re.match(r"^---\s*\n(.*?)\n---", content, re.DOTALL)
    if match:
        return {"raw": match.group(0), "end_pos": match.end()}
    return {"raw": "", "end_pos": 0}


def has_section(content: str, section_title: str) -> bool:
    """检查是否包含指定章节"""
    pattern = rf"^## {re.escape(section_title)}\s*$"
    return bool(re.search(pattern, content, re.MULTILINE))


def generate_function_description(content: str) -> str:
    """从现有内容生成功能描述"""
    # 尝试从文件开头提取描述
    lines = content.split("\n")
    
    # 查找第一个标题后的描述段落
    in_title = False
    desc_lines = []
    
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
        return "\n".join(desc_lines[:3])  # 取前3行作为描述
    
    # 默认描述
    return "本技能提供专业的自动化服务功能。"


def generate_usage_examples(content: str) -> str:
    """生成使用示例"""
    # 尝试从现有内容中提取示例
    examples = []
    
    # 查找代码块
    code_blocks = re.findall(r"```\n(.*?)\n```", content, re.DOTALL)
    
    if code_blocks:
        for i, block in enumerate(code_blocks[:2]):
            examples.append(f"### 示例{i+1}：使用场景{i+1}\n```\n{block[:200]}\n```\n\n助手输出：\n（根据输入生成相应输出）\n")
    
    if not examples:
        # 默认示例
        examples.append("### 示例1：基本使用\n```\n/your-command\n```\n\n助手输出：\n（根据技能功能生成相应输出）\n")
    
    return "## 使用示例\n\n" + "\n".join(examples)


def fix_skill(skill_path: str) -> Dict[str, Any]:
    """修复技能 SKILL.md"""
    skill_md_path = Path(skill_path) / "SKILL.md"
    
    if not skill_md_path.exists():
        return {"success": False, "message": f"SKILL.md 不存在: {skill_md_path}"}
    
    print(f"📝 修复技能: {Path(skill_path).name}")
    print(f"📂 文件路径: {skill_md_path}")
    print()
    
    # 读取内容
    content = read_file(str(skill_md_path))
    
    fixes_applied = []
    
    # 检查并添加 ## 功能描述
    if not has_section(content, "功能描述"):
        print("🔧 缺少 ## 功能描述 章节，正在添加...")
        
        # 生成功能描述
        func_desc = generate_function_description(content)
        
        # 在 frontmatter 之后添加
        frontmatter = parse_frontmatter(content)
        insert_pos = frontmatter["end_pos"]
        
        new_section = f"\n## 功能描述\n\n{func_desc}\n\n主要功能包括：\n\n- 功能1：待补充\n- 功能2：待补充\n- 功能3：待补充\n\n适用场景：待补充。\n\n"
        
        content = content[:insert_pos] + new_section + content[insert_pos:]
        
        fixes_applied.append("添加 ## 功能描述 章节")
        print("  ✅ 已添加 ## 功能描述 章节")
    else:
        print("  ✅ ## 功能描述 章节已存在，跳过")
    
    # 检查并添加 ## 使用示例
    if not has_section(content, "使用示例"):
        print("🔧 缺少 ## 使用示例 章节，正在添加...")
        
        # 生成使用示例
        usage_examples = generate_usage_examples(content)
        
        # 在文件末尾添加（或在 ## 功能描述 之后）
        # 简单处理：在文件末尾添加
        if not content.endswith("\n"):
            content += "\n"
        
        content += f"\n{usage_examples}\n"
        
        fixes_applied.append("添加 ## 使用示例 章节")
        print("  ✅ 已添加 ## 使用示例 章节")
    else:
        print("  ✅ ## 使用示例 章节已存在，跳过")
    
    # 写入文件
    if fixes_applied:
        if write_file(str(skill_md_path), content):
            print(f"\n✅ 修复完成！应用了 {len(fixes_applied)} 个修复")
            return {"success": True, "fixes": fixes_applied}
        else:
            return {"success": False, "message": "写入文件失败"}
    else:
        print("\n✅ 无需修复，所有必需章节已存在")
        return {"success": True, "fixes": []}


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("用法: python skill_section_fixer.py <skill_path> [--dry-run]")
        print("\n示例:")
        print("  python skill_section_fixer.py ~/.workbuddy/skills/my-skill")
        print("  python skill_section_fixer.py ~/.workbuddy/skills/my-skill --dry-run")
        sys.exit(1)
    
    skill_path = sys.argv[1]
    dry_run = "--dry-run" in sys.argv
    
    if dry_run:
        print("🔍 DRY RUN 模式 - 不会实际修改文件")
        print()
    
    if not Path(skill_path).exists():
        print(f"❌ 错误: 技能路径不存在: {skill_path}")
        sys.exit(1)
    
    if dry_run:
        # 只检查，不修复
        skill_md_path = Path(skill_path) / "SKILL.md"
        if skill_md_path.exists():
            content = read_file(str(skill_md_path))
            print(f"📂 技能: {Path(skill_path).name}")
            print(f"  ## 功能描述: {'✅ 存在' if has_section(content, '功能描述') else '❌ 缺少'}")
            print(f"  ## 使用示例: {'✅ 存在' if has_section(content, '使用示例') else '❌ 缺少'}")
        else:
            print(f"❌ SKILL.md 不存在")
    else:
        # 执行修复
        result = fix_skill(skill_path)
        
        if not result["success"]:
            print(f"\n❌ 修复失败: {result.get('message', '未知错误')}")
            sys.exit(1)


if __name__ == "__main__":
    main()
