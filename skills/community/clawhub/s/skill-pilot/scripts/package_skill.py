#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SkillPilot 技能打包脚本

Usage:
    python scripts/package_skill.py <skill-directory> [--output <output-dir>]

Process:
1. Validate the skill (auto)
2. Package into .skill file (zip with .skill extension)
3. Output to specified directory or current directory
"""

import os
import sys
import zipfile
import argparse
import shutil
from pathlib import Path
from datetime import datetime

# 导入验证器
from validate import SkillValidator


def package_skill(skill_path: str, output_dir: str = None) -> bool:
    """打包技能"""
    skill_path = Path(skill_path).resolve()
    
    if not skill_path.exists():
        print(f"Error: {skill_path} does not exist")
        return False
    
    if not skill_path.is_dir():
        print(f"Error: {skill_path} is not a directory")
        return False
    
    # 步骤 1: 验证技能
    print("Step 1: Validating skill...")
    print("=" * 60)
    validator = SkillValidator(str(skill_path))
    if not validator.validate():
        print("\n❌ Validation failed. Fix errors before packaging.")
        return False
    
    # 步骤 2: 打包
    print("\nStep 2: Packaging skill...")
    print("=" * 60)
    
    # 确定输出目录
    if output_dir:
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
    else:
        output_path = skill_path.parent / "dist"
        output_path.mkdir(exist_ok=True)
    
    # 创建 .skill 文件 (zip)
    skill_name = skill_path.name if skill_path.name else skill_path.parent.name
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    zip_filename = f"{skill_name}.skill"
    zip_path = output_path / zip_filename
    
    # 排除的文件/目录
    exclude_patterns = {
        "__pycache__",
        "*.pyc",
        "*.pyo",
        ".git",
        ".DS_Store",
        "*.log",
        "dist",
    }
    
    def should_exclude(path: Path) -> bool:
        for pattern in exclude_patterns:
            if pattern in str(path) or path.name == pattern or path.match(pattern):
                return True
        return False
    
    # 打包
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file_path in skill_path.rglob('*'):
            if file_path.is_file() and not should_exclude(file_path):
                # 计算相对路径
                relative_path = file_path.relative_to(skill_path)
                
                # 添加到 zip
                zipf.write(file_path, relative_path)
                print(f"  Added: {relative_path}")
    
    # 输出结果
    print("\n" + "=" * 60)
    print(f"✅ Skill packaged successfully!")
    print(f"   Output: {zip_path}")
    print(f"   Size: {zip_path.stat().st_size / 1024:.1f} KB")
    
    return True


def main():
    parser = argparse.ArgumentParser(description="Package SkillPilot skill")
    parser.add_argument("skill_path", help="Path to skill directory")
    parser.add_argument("--output", "-o", help="Output directory (default: ./dist)")
    
    args = parser.parse_args()
    
    success = package_skill(args.skill_path, args.output)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
