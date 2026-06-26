#!/usr/bin/env python3
"""
娜可露露洗发水 Skill - 打包脚本
将 Skill 打包为 .zip 文件，便于分发和安装
"""

import os
import zipfile
from datetime import datetime

def package_skill():
    """打包 Skill"""
    skill_dir = r"C:\Users\chenyuxin\.qclaw\workspace\skills\shampoo-recommender"
    output_dir = r"C:\Users\chenyuxin\.qclaw\workspace"
    
    # 生成文件名
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    zip_filename = f"shampoo-recommender_{timestamp}.zip"
    zip_path = os.path.join(output_dir, zip_filename)
    
    print("=" * 60)
    print("娜可露露洗发水 Skill - 打包工具")
    print("=" * 60)
    print(f"\n源目录: {skill_dir}")
    print(f"输出文件: {zip_path}")
    
    # 要包含的文件
    include_files = [
        "SKILL.md",
        "PACKAGE.md",
        "SETUP_GUIDE.md",
        "references/products.md",
        "references/faq.md",
        "references/examples.md",
        "scripts/card_generator.py",
        "scripts/setup_assets.py",
        "scripts/test_skill.py",
        "assets/README.md",
    ]
    
    # 创建 zip 文件
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file_path in include_files:
            full_path = os.path.join(skill_dir, file_path)
            if os.path.exists(full_path):
                arcname = f"shampoo-recommender/{file_path}"
                zipf.write(full_path, arcname)
                print(f"[ADDED] {file_path}")
            else:
                print(f"[SKIP] {file_path} (not found)")
        
        # 添加空目录占位文件
        empty_dirs = [
            "assets/images/.gitkeep",
            "assets/templates/.gitkeep",
            "assets/mockups/.gitkeep",
        ]
        
        for dir_placeholder in empty_dirs:
            # 创建空文件内容
            zipf.writestr(f"shampoo-recommender/{dir_placeholder}", "")
            print(f"[ADDED] {dir_placeholder} (empty directory placeholder)")
    
    print("\n" + "=" * 60)
    print("打包完成!")
    print("=" * 60)
    
    # 显示文件信息
    file_size = os.path.getsize(zip_path)
    print(f"\n文件名: {zip_filename}")
    print(f"文件大小: {file_size / 1024:.2f} KB")
    print(f"保存位置: {output_dir}")
    
    print("\n安装方法:")
    print("1. 解压 zip 文件到 OpenClaw skills 目录:")
    print(f"   {output_dir}")
    print("2. 或直接在 QClaw 中导入 .zip 文件")
    
    return zip_path

if __name__ == "__main__":
    package_skill()
