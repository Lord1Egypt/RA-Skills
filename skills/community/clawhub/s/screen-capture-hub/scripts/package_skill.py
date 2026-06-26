#!/usr/bin/env python3
"""
技能打包脚本
将技能目录打包为ZIP文件，准备发布到OpenClaw Hub
"""

import os
import sys
import json
import zipfile
import shutil
from pathlib import Path
import argparse
import yaml
from datetime import datetime

def validate_skill(skill_dir):
    """验证技能目录结构"""
    print("验证技能结构...")
    
    required_files = ["SKILL.md"]
    required_dirs = ["scripts"]
    
    skill_path = Path(skill_dir)
    
    # 检查必需文件
    for file_name in required_files:
        file_path = skill_path / file_name
        if not file_path.exists():
            print(f"[失败] 缺少必需文件: {file_name}")
            return False
    
    # 检查必需目录
    for dir_name in required_dirs:
        dir_path = skill_path / dir_name
        if not dir_path.exists():
            print(f"[失败] 缺少必需目录: {dir_name}")
            return False
    
    # 检查SKILL.md格式
    skill_md_path = skill_path / "SKILL.md"
    try:
        with open(skill_md_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # 检查YAML frontmatter
        if not content.startswith('---'):
            print("[失败] SKILL.md 必须以YAML frontmatter开始 (---)")
            return False
            
        # 解析YAML
        parts = content.split('---')
        if len(parts) < 3:
            print("[失败] SKILL.md 格式错误，缺少YAML frontmatter结束标记")
            return False
            
        frontmatter = parts[1].strip()
        metadata = yaml.safe_load(frontmatter)
        
        # 检查必需字段
        if 'name' not in metadata:
            print("[失败] SKILL.md 缺少 'name' 字段")
            return False
            
        if 'description' not in metadata:
            print("[失败] SKILL.md 缺少 'description' 字段")
            return False
            
        skill_name = metadata['name']
        print(f"[成功] 技能名称: {skill_name}")
        print(f"[成功] 技能描述: {metadata['description'][:100]}...")
        
    except yaml.YAMLError as e:
        print(f"[失败] YAML解析错误: {e}")
        return False
    except Exception as e:
        print(f"[失败] 文件读取错误: {e}")
        return False
    
    # 检查package.json (可选但推荐)
    package_json_path = skill_path / "package.json"
    if package_json_path.exists():
        try:
            with open(package_json_path, 'r', encoding='utf-8') as f:
                package_data = json.load(f)
            
            if 'version' not in package_data:
                print("⚠ package.json 缺少 'version' 字段")
            else:
                print(f"[成功] 版本号: {package_data.get('version', '未指定')}")
                
        except json.JSONDecodeError as e:
            print(f"[警告] package.json JSON解析错误: {e}")
    
    print("[成功] 技能验证通过")
    return skill_name

def create_zip_file(skill_dir, output_dir, skill_name):
    """创建ZIP压缩包"""
    print(f"\n创建ZIP压缩包...")
    
    # 创建输出目录
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # 生成ZIP文件名
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    zip_filename = f"{skill_name}-{timestamp}.zip"
    zip_path = output_path / zip_filename
    
    # 创建ZIP文件
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        skill_path = Path(skill_dir)
        
        # 遍历所有文件
        for root, dirs, files in os.walk(skill_dir):
            # 跳过一些目录
            if '__pycache__' in dirs:
                dirs.remove('__pycache__')
            if '.git' in dirs:
                dirs.remove('.git')
            
            for file in files:
                # 跳过一些文件
                if file.endswith('.pyc') or file == '.DS_Store':
                    continue
                    
                file_path = Path(root) / file
                # 计算相对路径
                rel_path = file_path.relative_to(skill_path)
                
                # 添加到ZIP
                zipf.write(file_path, rel_path)
                print(f"  添加: {rel_path}")
    
    print(f"[成功] ZIP文件创建完成: {zip_path}")
    print(f"   大小: {zip_path.stat().st_size / 1024:.1f} KB")
    
    return zip_path

def create_manifest(skill_dir, output_dir, skill_name, zip_path):
    """创建发布清单"""
    print(f"\n创建发布清单...")
    
    manifest_path = Path(output_dir) / f"{skill_name}-manifest.json"
    
    # 收集技能信息
    skill_path = Path(skill_dir)
    
    # 读取SKILL.md元数据
    skill_md_path = skill_path / "SKILL.md"
    with open(skill_md_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    parts = content.split('---')
    frontmatter = parts[1].strip()
    metadata = yaml.safe_load(frontmatter)
    
    # 读取package.json (如果存在)
    package_info = {}
    package_json_path = skill_path / "package.json"
    if package_json_path.exists():
        with open(package_json_path, 'r', encoding='utf-8') as f:
            package_info = json.load(f)
    
    # 统计文件
    script_count = 0
    reference_count = 0
    asset_count = 0
    
    scripts_dir = skill_path / "scripts"
    if scripts_dir.exists():
        script_count = sum(1 for f in scripts_dir.glob('*.py') if f.is_file())
    
    references_dir = skill_path / "references"
    if references_dir.exists():
        reference_count = sum(1 for f in references_dir.glob('*') if f.is_file())
    
    assets_dir = skill_path / "assets"
    if assets_dir.exists():
        asset_count = sum(1 for f in assets_dir.glob('*') if f.is_file())
    
    # 创建清单
    manifest = {
        "skill": {
            "name": metadata['name'],
            "description": metadata['description'],
            "version": package_info.get('version', '1.0.0'),
            "author": package_info.get('author', 'Unknown'),
            "license": package_info.get('license', 'MIT'),
            "created_at": datetime.now().isoformat(),
            "stats": {
                "scripts": script_count,
                "references": reference_count,
                "assets": asset_count,
                "total_files": script_count + reference_count + asset_count + 3  # SKILL.md, README.md, requirements.txt
            }
        },
        "package": {
            "filename": zip_path.name,
            "size_bytes": zip_path.stat().st_size,
            "created_at": datetime.now().isoformat(),
            "sha256": "计算中..."  # 实际应用中需要计算
        },
        "requirements": {
            "python": ">=3.8",
            "dependencies": [
                "pillow>=9.0.0",
                "pyautogui>=0.9.0"
            ],
            "optional_dependencies": [
                "pytesseract>=0.3.0",
                "opencv-python>=4.5.0",
                "numpy>=1.20.0"
            ]
        },
        "compatibility": {
            "platforms": ["windows", "macos", "linux"],
            "codebuddy_version": ">=1.0.0"
        }
    }
    
    # 保存清单
    with open(manifest_path, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
    
    print(f"[成功] 发布清单创建完成: {manifest_path}")
    
    return manifest_path

def main():
    parser = argparse.ArgumentParser(description='技能打包工具')
    parser.add_argument('skill_dir', help='技能目录路径')
    parser.add_argument('-o', '--output', default='./dist', help='输出目录 (默认: ./dist)')
    parser.add_argument('--no-validate', action='store_true', help='跳过验证')
    parser.add_argument('--no-manifest', action='store_true', help='跳过清单创建')
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("Screen Capture Hub 技能打包工具")
    print("=" * 60)
    
    # 验证技能
    if not args.no_validate:
        skill_name = validate_skill(args.skill_dir)
        if not skill_name:
            print("[失败] 技能验证失败，打包中止")
            sys.exit(1)
    else:
        # 从目录名提取技能名
        skill_name = Path(args.skill_dir).name
        print(f"[警告] 跳过验证，使用目录名作为技能名: {skill_name}")
    
    # 创建ZIP文件
    zip_path = create_zip_file(args.skill_dir, args.output, skill_name)
    
    # 创建清单
    if not args.no_manifest:
        manifest_path = create_manifest(args.skill_dir, args.output, skill_name, zip_path)
    
    print("\n" + "=" * 60)
    print("[成功] 打包完成!")
    print("=" * 60)
    
    print(f"\n生成的文件:")
    print(f"  1. ZIP包: {zip_path}")
    if not args.no_manifest:
        print(f"  2. 清单: {manifest_path}")
    
    print(f"\n发布到OpenClaw Hub的步骤:")
    print(f"  1. 登录 OpenClaw Hub: https://hub.openclaw.org/")
    print(f"  2. 进入 '发布技能' 页面")
    print(f"  3. 上传: {zip_path.name}")
    print(f"  4. 填写技能信息")
    print(f"  5. 提交审核")
    
    print(f"\n技能信息:")
    print(f"  名称: {skill_name}")
    print(f"  版本: 1.0.0")
    print(f"  平台: Windows/macOS/Linux")
    print(f"  依赖: Python 3.8+, Pillow, PyAutoGUI")
    
    print(f"\n查看完整文档:")
    print(f"  {Path(args.skill_dir) / 'README.md'}")

if __name__ == "__main__":
    main()