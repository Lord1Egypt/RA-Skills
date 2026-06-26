#!/usr/bin/env python3
"""
会议纪要生成器 - 技能打包脚本
将技能打包为 .skill 文件用于发布
"""

import json
import os
import shutil
import sys
import tarfile
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional


class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
    BOLD = '\033[1m'


def print_success(msg: str):
    print(f"{Colors.GREEN}✓{Colors.RESET} {msg}")


def print_error(msg: str):
    print(f"{Colors.RED}✗{Colors.RESET} {msg}")


def print_info(msg: str):
    print(f"{Colors.BLUE}ℹ{Colors.RESET} {msg}")


def read_meta(skill_path: Path) -> Optional[Dict]:
    """读取 _meta.json"""
    meta_file = skill_path / "_meta.json"
    if not meta_file.exists():
        return None
    try:
        return json.loads(meta_file.read_text(encoding='utf-8'))
    except json.JSONDecodeError:
        return None


def get_skill_name(skill_path: Path) -> str:
    """获取技能名称"""
    meta = read_meta(skill_path)
    if meta:
        return f"skill-{meta['id']}-{meta['version']}"
    return skill_path.name


def collect_files(skill_path: Path) -> List[Path]:
    """收集要打包的文件"""
    files = []
    
    # 敏感文件模式（排除）
    exclude_patterns = [
        '.DS_Store', 'Thumbs.db', '__pycache__',
        '*.pyc', '*.pyo', '.git', '.gitignore'
    ]
    
    for item in skill_path.rglob("*"):
        if item.is_file():
            # 跳过隐藏文件和缓存
            if any(item.name.startswith(p.replace('*', '')) for p in exclude_patterns):
                continue
            # 跳过 __pycache__
            if '__pycache__' in str(item):
                continue
            files.append(item)
    
    return files


def create_package(skill_path: str, output_dir: Optional[str] = None) -> Optional[str]:
    """创建技能包"""
    skill_path = Path(skill_path).resolve()
    
    if not skill_path.exists():
        print_error(f"技能路径不存在: {skill_path}")
        return None
    
    # 读取元数据
    meta = read_meta(skill_path)
    if not meta:
        print_error("无法读取 _meta.json")
        return None
    
    # 确定输出目录
    if output_dir:
        output_path = Path(output_dir)
    else:
        output_path = skill_path.parent
    
    # 创建输出文件名
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    output_name = f"meeting-notes-generator-v{meta['version']}-{timestamp}.skill"
    output_file = output_path / output_name
    
    # 收集文件
    files = collect_files(skill_path)
    if not files:
        print_error("没有找到要打包的文件")
        return None
    
    print_info(f"收集到 {len(files)} 个文件:")
    for f in files:
        rel_path = f.relative_to(skill_path)
        print(f"  - {rel_path}")
    
    # 创建 tar.gz 包
    try:
        with tarfile.open(output_file, "w:gz") as tar:
            for file_path in files:
                arcname = file_path.relative_to(skill_path)
                tar.add(file_path, arcname=arcname)
        
        print_success(f"打包完成: {output_file}")
        return str(output_file)
    except Exception as e:
        print_error(f"打包失败: {e}")
        return None


def extract_package(package_path: str, output_dir: str) -> Optional[str]:
    """解压技能包（用于验证）"""
    package_path = Path(package_path)
    
    if not package_path.exists():
        print_error(f"包文件不存在: {package_path}")
        return None
    
    # 创建临时目录
    temp_dir = Path(tempfile.mkdtemp(prefix="skill_extract_"))
    extract_path = temp_dir / package_path.stem.replace('.skill', '')
    extract_path.mkdir(exist_ok=True)
    
    try:
        with tarfile.open(package_path, "r:gz") as tar:
            tar.extractall(extract_path)
        
        print_success(f"解压完成: {extract_path}")
        return str(extract_path)
    except Exception as e:
        print_error(f"解压失败: {e}")
        return None


def verify_package(package_path: str) -> bool:
    """验证包内容"""
    print(f"\n{Colors.BOLD}[验证打包内容]{Colors.RESET}\n")
    
    extract_path = extract_package(package_path, tempfile.gettempdir())
    if not extract_path:
        return False
    
    # 检查必需文件
    required_files = ['SKILL.md', '_meta.json']
    extract_path_obj = Path(extract_path)
    
    all_ok = True
    for fname in required_files:
        if (extract_path_obj / fname).exists():
            print_success(f"包含: {fname}")
        else:
            print_error(f"缺失: {fname}")
            all_ok = False
    
    # 列出所有文件
    print_info("\n包内容结构:")
    for item in sorted(extract_path_obj.rglob("*")):
        if item.is_file():
            rel = item.relative_to(extract_path_obj)
            print(f"  {rel}")
    
    return all_ok


def package_skill(skill_path: str, output_dir: Optional[str] = None, verify: bool = True) -> Optional[str]:
    """打包技能"""
    skill_path = Path(skill_path).resolve()
    
    print(f"\n{Colors.BOLD}{'='*60}")
    print(f"会议纪要生成器 - 技能打包")
    print(f"{'='*60}{Colors.RESET}\n")
    
    print_info(f"技能路径: {skill_path}")
    if output_dir:
        print_info(f"输出目录: {output_dir}")
    print()
    
    # 创建包
    package_path = create_package(skill_path, output_dir)
    if not package_path:
        return None
    
    # 验证包
    if verify:
        print()
        if verify_package(package_path):
            print_success("\n打包验证通过！")
        else:
            print_warning("\n打包验证发现问题，但包已生成。")
    
    print(f"\n{Colors.BOLD}{'='*60}")
    print_success(f"打包完成！")
    print(f"{Colors.BOLD}{'='*60}{Colors.RESET}\n")
    print_info(f"包文件位置: {package_path}\n")
    
    return package_path


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法:")
        print("  打包技能: python package_skill.py <skill_path> [output_dir]")
        print("  验证包:   python package_skill.py --verify <package.skill>")
        sys.exit(1)
    
    # 验证模式
    if sys.argv[1] == "--verify":
        if len(sys.argv) < 3:
            print_error("请指定包文件路径")
            sys.exit(1)
        success = verify_package(sys.argv[2])
        sys.exit(0 if success else 1)
    
    skill_path = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else None
    
    result = package_skill(skill_path, output_dir)
    sys.exit(0 if result else 1)
