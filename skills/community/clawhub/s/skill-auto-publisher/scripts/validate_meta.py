#!/usr/bin/env python3
"""元数据验证脚本 - 检查 SKILL.md 格式是否正确"""

import sys
import json
import re
from pathlib import Path

def validate_skill(skill_path):
    """验证技能元数据"""
    skill_dir = Path(skill_path)
    skill_md = skill_dir / "SKILL.md"
    
    errors = []
    warnings = []
    
    # 1. 检查 SKILL.md 是否存在
    if not skill_md.exists():
        errors.append("❌ SKILL.md 文件不存在")
        return {"valid": False, "errors": errors, "warnings": warnings}
    
    # 2. 读取文件内容
    content = skill_md.read_text(encoding="utf-8")
    
    # 3. 检查 YAML frontmatter
    if not content.startswith("---"):
        errors.append("❌ 缺少 YAML frontmatter（应以 --- 开头）")
        return {"valid": False, "errors": errors, "warnings": warnings}
    
    # 提取 frontmatter
    parts = content.split("---", 2)
    if len(parts) < 3:
        errors.append("❌ YAML frontmatter 格式错误（应以 --- 结尾）")
        return {"valid": False, "errors": errors, "warnings": warnings}
    
    frontmatter = parts[1].strip()
    
    # 4. 解析 YAML（简单解析，不依赖 pyyaml）
    metadata = {}
    for line in frontmatter.split("\n"):
        if ":" in line:
            key, value = line.split(":", 1)
            metadata[key.strip()] = value.strip().strip('"').strip("'")
    
    # 5. 检查 name 字段
    if "name" not in metadata:
        errors.append("❌ 缺少 name 字段")
    else:
        name = metadata["name"]
        if not name:
            errors.append("❌ name 字段为空")
        elif not re.match(r'^[a-z0-9-]+$', name):
            errors.append(f"❌ name 格式错误：{name}（应为小写字母+连字符）")
    
    # 6. 检查 description 字段
    if "description" not in metadata:
        errors.append("❌ 缺少 description 字段")
    else:
        desc = metadata["description"]
        if len(desc) < 20:
            errors.append(f"❌ description 太短：{len(desc)} 字符（建议至少 20 字符）")
        if "触发词" not in desc and "trigger" not in desc.lower():
            warnings.append("⚠️ description 中没有触发词，可能影响技能触发")
    
    # 7. 检查 _meta.json
    meta_file = skill_dir / "_meta.json"
    if meta_file.exists():
        try:
            meta = json.load(open(meta_file))
            if "version" not in meta:
                warnings.append("⚠️ _meta.json 中没有 version 字段")
        except json.JSONDecodeError:
            errors.append("❌ _meta.json 格式错误")
    
    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "warnings": warnings,
        "metadata": metadata
    }

def main():
    if len(sys.argv) < 2:
        print("用法: python3 validate_meta.py <skill-path>")
        sys.exit(1)
    
    skill_path = sys.argv[1]
    result = validate_skill(skill_path)
    
    print(f"🔍 验证技能: {skill_path}")
    print()
    
    if result["errors"]:
        print("❌ 错误:")
        for err in result["errors"]:
            print(f"  {err}")
    
    if result["warnings"]:
        print("⚠️ 警告:")
        for warn in result["warnings"]:
            print(f"  {warn}")
    
    if result["valid"]:
        print("✅ 元数据验证通过")
        sys.exit(0)
    else:
        print()
        print("❌ 验证失败，请修复后重试")
        sys.exit(1)

if __name__ == "__main__":
    main()
