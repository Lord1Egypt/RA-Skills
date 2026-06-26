#!/usr/bin/env python3
"""
Sum2Slides 名称更新脚本
将所有"Sum to Slides"改回"Sum2Slides"
"""

import os
import re
from pathlib import Path

def update_file_content(file_path):
    """更新文件内容"""
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 替换规则
        replacements = [
            ("Sum to Slides", "Sum2Slides"),
            ("sum-to-slides", "sum2slides"),
            ("sum_to_slides", "sum2slides"),
            ("SumToSlides", "Sum2Slides"),
        ]
        
        new_content = content
        for old, new in replacements:
            new_content = new_content.replace(old, new)
        
        if new_content != content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            return True
        return False
    except Exception as e:
        print(f"❌ 更新 {file_path} 失败: {e}")
        return False

def main():
    """主函数"""
    
    project_root = Path(__file__).parent.parent
    
    # 需要更新的文件列表
    files_to_update = [
        "SKILL.md",
        "README.md",
        "CHANGELOG.md",
        "TUTORIAL.md",
        "DEMO.md",
        "FAQ.md",
        "CONTRIBUTING.md",
        "RELEASE_NOTES.md",
        "package.json",
        "scripts/demo.py",
        "scripts/quick_setup.py",
        "scripts/release_prepare.py",
    ]
    
    updated_count = 0
    total_count = 0
    
    for file_rel_path in files_to_update:
        file_path = project_root / file_rel_path
        if file_path.exists():
            total_count += 1
            print(f"🔧 更新: {file_rel_path}...", end="")
            if update_file_content(file_path):
                print("✅")
                updated_count += 1
            else:
                print("⏭️ (无需更新)")
        else:
            print(f"⚠️ 文件不存在: {file_rel_path}")
    
    # 重命名源代码目录
    src_dir_old = project_root / "src" / "sum_to_slides"
    src_dir_new = project_root / "src" / "sum2slides"
    
    if src_dir_old.exists() and not src_dir_new.exists():
        print(f"🔧 重命名源代码目录...")
        os.rename(src_dir_old, src_dir_new)
        updated_count += 1
        print(f"✅ 重命名完成: {src_dir_old} -> {src_dir_new}")
    
    print(f"\n📊 更新总结:")
    print(f"   处理的文件数: {total_count}")
    print(f"   实际更新的文件数: {updated_count}")
    print(f"   重命名的目录: {src_dir_new}")
    
    # 创建新的Skill包
    print("\n📦 创建Skill安装包...")
    skill_package = project_root.parent / "sum2slides-1.0.0.skill.zip"
    
    try:
        import subprocess
        subprocess.run([
            'zip', '-r', str(skill_package), 'sum2slides-1.0.0/'
        ], cwd=project_root.parent, check=True)
        print(f"✅ Skill包已创建: {skill_package}")
        print(f"   大小: {skill_package.stat().st_size / 1024:.1f} KB")
    except Exception as e:
        print(f"❌ 创建Skill包失败: {e}")

if __name__ == "__main__":
    main()