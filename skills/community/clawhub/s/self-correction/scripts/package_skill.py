#!/usr/bin/env python3
"""
技能打包脚本 - 将 self-correction 技能打包为 .skill 文件
"""

import os
import sys
import json
import shutil
import zipfile
import importlib.util
from pathlib import Path
from datetime import datetime

def get_skill_info(skill_dir):
    """从_meta.json获取技能信息"""
    meta_path = os.path.join(skill_dir, '_meta.json')
    with open(meta_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def create_package(skill_dir, output_dir=None):
    """创建技能包"""
    if output_dir is None:
        output_dir = os.path.dirname(skill_dir)

    skill_name = os.path.basename(skill_dir)
    skill_info = get_skill_info(skill_dir)

    # 创建输出文件名
    version = skill_info.get('version', '1.0.0')
    package_name = f"{skill_name}-{version}.skill"
    output_path = os.path.join(output_dir, package_name)

    # 收集所有要打包的文件
    files_to_package = []
    for root, dirs, files in os.walk(skill_dir):
        # 跳过__pycache__等目录
        dirs[:] = [d for d in dirs if d not in ['__pycache__', '.git', '.venv']]

        for file in files:
            file_path = os.path.join(root, file)
            rel_path = os.path.relpath(file_path, skill_dir)
            files_to_package.append((file_path, rel_path))

    # 创建ZIP包
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        for file_path, rel_path in files_to_package:
            zf.write(file_path, arcname=rel_path)

    # 生成包信息
    package_info = {
        "name": skill_name,
        "version": version,
        "package_path": output_path,
        "files_count": len(files_to_package),
        "package_size": os.path.getsize(output_path),
        "created_at": datetime.now().isoformat(),
        "description": skill_info.get('description', ''),
        "author": skill_info.get('author', 'Unknown'),
        "id": skill_info.get('id', '')
    }

    # 保存包信息JSON
    info_path = output_path.replace('.skill', '-info.json')
    with open(info_path, 'w', encoding='utf-8') as f:
        json.dump(package_info, f, ensure_ascii=False, indent=2)

    return output_path, package_info

def verify_package(package_path):
    """验证打包的内容"""
    try:
        with zipfile.ZipFile(package_path, 'r') as zf:
            file_list = zf.namelist()

            # 检查必需文件
            required_files = ['SKILL.md', '_meta.json']
            for req_file in required_files:
                if req_file not in file_list:
                    return False, f"包中缺少必需文件: {req_file}"

            # 检查是否有不安全的文件
            forbidden_patterns = ['__pycache__', '.pyc', '.git', '.DS_Store']
            for pattern in forbidden_patterns:
                for file in file_list:
                    if pattern in file:
                        return False, f"包中包含不应打包的文件: {file}"

        return True, "包验证通过"
    except zipfile.BadZipFile:
        return False, "无效的ZIP文件"

def run_packaging(skill_dir, output_dir=None):
    """运行打包流程"""
    print("=" * 50)
    print("开始打包 self-correction 技能")
    print("=" * 50)

    skill_name = os.path.basename(skill_dir)
    print(f"技能目录: {skill_dir}")

    # 运行验证脚本
    print("\n[1/3] 运行验证...")
    validate_script = os.path.join(os.path.dirname(__file__), 'validate_skill.py')
    if os.path.exists(validate_script):
        # 动态导入验证脚本
        spec = importlib.util.spec_from_file_location("validate_skill", validate_script)
        validate_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(validate_module)
        if validate_module.run_validation(skill_dir) != 0:
            print("❌ 验证失败，停止打包")
            return None
    else:
        print("⚠️ 跳过验证（验证脚本不存在）")

    # 创建包
    print("\n[2/3] 创建技能包...")
    try:
        package_path, package_info = create_package(skill_dir, output_dir)
        print(f"✅ 包已创建: {package_path}")
        print(f"   - 版本: {package_info['version']}")
        print(f"   - 文件数: {package_info['files_count']}")
        print(f"   - 大小: {package_info['package_size']} bytes")

        # 验证包
        print("\n[3/3] 验证技能包...")
        valid, message = verify_package(package_path)
        if valid:
            print(f"✅ {message}")
        else:
            print(f"❌ 验证失败: {message}")
            return None

    except Exception as e:
        print(f"❌ 打包失败: {str(e)}")
        return None

    print("=" * 50)
    print("✅ 打包完成！")
    print("=" * 50)

    return package_path

if __name__ == '__main__':
    skill_dir = sys.argv[1] if len(sys.argv) > 1 else '/workspace/temp-skills/self-correction'
    output_dir = sys.argv[2] if len(sys.argv) > 2 else None

    package_path = run_packaging(skill_dir, output_dir)
    if package_path:
        print(f"\n打包文件路径: {package_path}")
        sys.exit(0)
    else:
        sys.exit(1)
