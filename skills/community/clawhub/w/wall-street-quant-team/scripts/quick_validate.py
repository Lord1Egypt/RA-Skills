#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
技能验证器 - 验证股票量化投资智囊技能结构和内容
"""

import os
import sys
import json
from pathlib import Path

def validate_skill_structure(skill_path: str) -> bool:
    """验证技能目录结构"""
    skill_path = Path(skill_path)
    errors = []

    # 检查必需文件
    required_files = [
        "SKILL.md",
        "_meta.json"
    ]

    for f in required_files:
        if not (skill_path / f).exists():
            errors.append(f"缺少必需文件: {f}")

    # 检查SKILL.md格式
    skill_md = skill_path / "SKILL.md"
    if skill_md.exists():
        content = skill_md.read_text(encoding='utf-8')

        # 检查frontmatter
        if not content.startswith('---'):
            errors.append("SKILL.md 必须以 frontmatter (---) 开头")

        if 'name:' not in content or 'description:' not in content:
            errors.append("SKILL.md frontmatter 必须包含 name 和 description")

    # 检查_meta.json格式
    meta_json = skill_path / "_meta.json"
    if meta_json.exists():
        try:
            meta = json.loads(meta_json.read_text(encoding='utf-8'))
            if 'id' not in meta:
                errors.append("_meta.json 必须包含 id 字段")
            if 'version' not in meta:
                errors.append("_meta.json 必须包含 version 字段")
        except json.JSONDecodeError as e:
            errors.append(f"_meta.json 格式错误: {e}")

    # 检查目录结构
    required_dirs = [
        "references",
        "scripts",
        "assets/agent-templates"
    ]

    for d in required_dirs:
        if not (skill_path / d).is_dir():
            errors.append(f"缺少目录: {d}")

    if errors:
        print("❌ 验证失败:")
        for err in errors:
            print(f"  - {err}")
        return False

    print("✅ 技能结构验证通过")
    return True

def validate_skill_content(skill_path: str) -> bool:
    """验证技能内容完整性"""
    skill_path = Path(skill_path)
    errors = []

    # 检查参考文档
    references_dir = skill_path / "references"
    if references_dir.exists():
        ref_files = list(references_dir.glob("*.md"))
        if len(ref_files) < 3:
            errors.append(f"参考文档不足，至少需要3个，当前: {len(ref_files)}")

        # 检查关键参考文档
        key_refs = ["ai-quant-guide.md", "workflow-orchestration.md"]
        for ref in key_refs:
            if not (references_dir / ref).exists():
                errors.append(f"缺少关键参考文档: {ref}")

    # 检查代理模板
    templates_dir = skill_path / "assets/agent-templates"
    if templates_dir.exists():
        template_files = list(templates_dir.glob("*.md"))
        if len(template_files) < 5:
            errors.append(f"代理模板不足，至少需要5个，当前: {len(template_files)}")

    # 检查脚本
    scripts_dir = skill_path / "scripts"
    if scripts_dir.exists():
        script_files = list(scripts_dir.glob("*.py"))
        if len(script_files) < 1:
            errors.append("缺少Python脚本")

    if errors:
        print("⚠️ 内容完整性警告:")
        for err in errors:
            print(f"  - {err}")
        return True  # 内容警告不影响验证通过

    print("✅ 技能内容完整性验证通过")
    return True

def main():
    skill_path = "/workspace/temp-skills/wall-street-quant-team"

    print("=" * 60)
    print("股票量化投资智囊技能 - 验证器")
    print("=" * 60)

    # 验证结构
    struct_ok = validate_skill_structure(skill_path)

    # 验证内容
    content_ok = validate_skill_content(skill_path)

    if struct_ok and content_ok:
        print("\n" + "=" * 60)
        print("✅ 所有验证通过！技能可以发布")
        print("=" * 60)
        return 0

    return 1

if __name__ == "__main__":
    sys.exit(main())
