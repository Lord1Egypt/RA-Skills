#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
技能打包器 - 将股票量化投资智囊技能打包为.skill文件
"""

import os
import sys
import json
import zipfile
from pathlib import Path
from datetime import datetime

def create_skill_package(skill_path: str, output_path: str = None) -> bool:
    """创建技能安装包"""
    skill_path = Path(skill_path)

    if not skill_path.exists():
        print(f"❌ 技能路径不存在: {skill_path}")
        return False

    # 生成输出文件名
    if output_path is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = skill_path.parent / f"wall-street-quant-team_{timestamp}.skill"
    else:
        output_path = Path(output_path)

    # 读取meta信息
    meta_file = skill_path / "_meta.json"
    if meta_file.exists():
        meta = json.loads(meta_file.read_text(encoding='utf-8'))
        skill_name = meta.get('id', 'unknown')
        skill_version = meta.get('version', '1.0.0')
    else:
        skill_name = 'unknown'
        skill_version = '1.0.0'

    print("=" * 60)
    print("股票量化投资智囊技能 - 打包器")
    print("=" * 60)
    print(f"技能路径: {skill_path}")
    print(f"输出文件: {output_path}")
    print(f"版本: {skill_version}")
    print("-" * 60)

    # 排除的文件/目录（注意：保留.pyc用于闭源）
    exclude_patterns = [
        '__pycache__',
        '.git',
        '.DS_Store',
        '.pytest_cache'
    ]

    # 创建zip文件
    try:
        with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            file_count = 0
            for root, dirs, files in os.walk(skill_path):
                # 过滤排除的目录
                dirs[:] = [d for d in dirs if not any(
                    pattern in d for pattern in exclude_patterns
                )]

                for file in files:
                    # 过滤排除的文件
                    if any(pattern in file for pattern in exclude_patterns):
                        continue

                    file_path = Path(root) / file
                    arcname = file_path.relative_to(skill_path)
                    zipf.write(file_path, arcname)
                    file_count += 1
                    print(f"  添加: {arcname}")

        # 获取文件大小
        file_size = output_path.stat().st_size
        size_mb = file_size / (1024 * 1024)

        print("-" * 60)
        print(f"✅ 打包完成！")
        print(f"   文件数量: {file_count}")
        print(f"   文件大小: {size_mb:.2f} MB")
        print(f"   输出路径: {output_path.absolute()}")
        print("=" * 60)

        return True

    except Exception as e:
        print(f"❌ 打包失败: {e}")
        return False

def extract_skill_package(skill_file: str, output_path: str = None) -> bool:
    """解压技能包（用于测试）"""
    skill_file = Path(skill_file)

    if not skill_file.exists():
        print(f"❌ 技能文件不存在: {skill_file}")
        return False

    if output_path is None:
        output_path = skill_file.parent / skill_file.stem
    else:
        output_path = Path(output_path)

    print("=" * 60)
    print("股票量化投资智囊技能 - 解压器")
    print("=" * 60)
    print(f"技能文件: {skill_file}")
    print(f"解压路径: {output_path}")
    print("-" * 60)

    try:
        output_path.mkdir(parents=True, exist_ok=True)

        with zipfile.ZipFile(skill_file, 'r') as zipf:
            zipf.extractall(output_path)
            file_count = len(zipf.namelist())

        print(f"✅ 解压完成！文件数量: {file_count}")
        print("=" * 60)
        return True

    except Exception as e:
        print(f"❌ 解压失败: {e}")
        return False

def main():
    skill_path = "/workspace/temp-skills/wall-street-quant-team"

    if len(sys.argv) > 1:
        command = sys.argv[1]

        if command == "package":
            output = sys.argv[2] if len(sys.argv) > 2 else None
            success = create_skill_package(skill_path, output)
        elif command == "extract":
            skill_file = sys.argv[2]
            output = sys.argv[3] if len(sys.argv) > 3 else None
            success = extract_skill_package(skill_file, output)
        elif command == "test":
            # 测试打包-解压循环
            output = "/tmp/test_skill.skill"
            if create_skill_package(skill_path, output):
                extract_skill_package(output, "/tmp/test_extract")
                print("\n✅ 打包-解压测试通过")
                success = True
            else:
                success = False
        else:
            print(f"未知命令: {command}")
            print("用法: package_skill.py [package|extract|test] [参数]")
            success = False
    else:
        # 默认执行打包
        success = create_skill_package(skill_path)

    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())
