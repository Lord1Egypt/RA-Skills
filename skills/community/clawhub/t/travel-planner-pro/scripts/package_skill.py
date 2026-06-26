#!/usr/bin/env python3
"""打包技能为 .skill 文件"""
import os
import sys
import zipfile
import json
from pathlib import Path

def package_skill(skill_dir: str, output_path: str = None):
    skill_path = Path(skill_dir)
    skill_name = skill_path.name
    
    if output_path is None:
        output_path = f"{skill_name}.skill"
    
    # 读取 meta
    meta_path = skill_path / "_meta.json"
    if not meta_path.exists():
        print(f"Error: _meta.json not found in {skill_dir}")
        sys.exit(1)
    
    with open(meta_path) as f:
        meta = json.load(f)
    
    print(f"Packaging skill: {skill_name}")
    print(f"  ID: {meta['id']}")
    print(f"  Version: {meta['version']}")
    
    # 创建 zip 包
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(skill_path):
            for file in files:
                file_path = Path(root) / file
                arcname = file_path.relative_to(skill_path)
                zf.write(file_path, arcname)
                print(f"  + {arcname}")
    
    print(f"\nCreated: {output_path}")
    print(f"Size: {os.path.getsize(output_path)} bytes")
    return output_path

if __name__ == "__main__":
    skill_dir = sys.argv[1] if len(sys.argv) > 1 else "."
    package_skill(skill_dir)
