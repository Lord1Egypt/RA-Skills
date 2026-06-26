#!/usr/bin/env python3
"""
Skill 打包脚本
将 skill 目录打包成 .skill 文件（zip 格式）
"""

import os
import sys
import zipfile
from pathlib import Path

def package_skill(skill_dir, output_dir=None):
    """
    打包 skill 目录
    
    Args:
        skill_dir: skill 目录路径
        output_dir: 输出目录（可选）
    """
    skill_path = Path(skill_dir)
    
    if not skill_path.exists():
        print(f"[ERROR] 目录不存在: {skill_dir}")
        return False
    
    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        print(f"[ERROR] 缺少 SKILL.md: {skill_dir}")
        return False
    
    # 输出文件名
    skill_name = skill_path.name
    if output_dir:
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
    else:
        output_path = skill_path.parent
    
    output_file = output_path / f"{skill_name}.skill"
    
    # 打包
    with zipfile.ZipFile(output_file, 'w', zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(skill_path):
            # 排除隐藏文件和 __pycache__
            dirs[:] = [d for d in dirs if not d.startswith('.') and d != '__pycache__']
            
            for file in files:
                if file.startswith('.'):
                    continue
                
                file_path = Path(root) / file
                arcname = file_path.relative_to(skill_path.parent)
                zf.write(file_path, arcname)
    
    print(f"[OK] 打包完成: {output_file}")
    print(f"     大小: {output_file.stat().st_size / 1024:.1f} KB")
    return True

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python package.py <skill目录> [输出目录]")
        sys.exit(1)
    
    skill_dir = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else None
    
    package_skill(skill_dir, output_dir)
