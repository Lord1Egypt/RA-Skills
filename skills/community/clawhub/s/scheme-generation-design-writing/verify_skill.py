#!/usr/bin/env python3
"""
技能验证脚本 - 在上传前验证技能的完整性和正确性

用法:
    python verify_skill.py
"""

import os
import sys
from pathlib import Path
import json

# 技能根目录
SKILL_ROOT = Path(__file__).parent

# 必需文件列表
REQUIRED_FILES = [
    'SKILL.md',
    'README.md',
    'config.json',
    'LICENSE',
    'CHANGELOG.md',
    '.gitignore',
    'scripts/index_projects.py',
    'scripts/match_projects.py',
    'data/project_index_example.json',
    'references/concept_plan_schema.md',
    'references/design_desc_schema.md',
    'references/examples.md',
    'references/quick-start.md',
]

# 可选文件列表
OPTIONAL_FILES = [
    'PROJECT_STRUCTURE.md',
    'UPLOAD_GUIDE.md',
]


def check_file_exists(filepath: Path) -> bool:
    """检查文件是否存在"""
    return filepath.exists() and filepath.is_file()


def check_skill_metadata(skill_md: Path) -> tuple[bool, str]:
    """检查 SKILL.md 的元数据"""
    try:
        content = skill_md.read_text(encoding='utf-8')
        
        # 检查是否有元数据块
        if not content.startswith('---'):
            return False, "SKILL.md 缺少元数据块（应以 --- 开头）"
        
        # 提取元数据
        lines = content.split('\n')
        metadata = {}
        in_metadata = False
        
        for line in lines:
            if line.strip() == '---':
                if not in_metadata:
                    in_metadata = True
                else:
                    break
            elif in_metadata and ':' in line:
                key, value = line.split(':', 1)
                metadata[key.strip()] = value.strip()
        
        # 检查必需字段
        if 'name' not in metadata:
            return False, "SKILL.md 元数据缺少 'name' 字段"
        
        if 'description' not in metadata:
            return False, "SKILL.md 元数据缺少 'description' 字段"
        
        # 检查 name 格式
        name = metadata['name']
        if not name.replace('-', '').replace('_', '').isalnum():
            return False, f"技能名称格式不正确: {name}（应只包含字母、数字、连字符和下划线）"
        
        return True, f"元数据正确 (name: {name})"
        
    except Exception as e:
        return False, f"读取 SKILL.md 失败: {e}"


def check_config_json(config_file: Path) -> tuple[bool, str]:
    """检查 config.json 格式"""
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        # 检查必需字段
        required_keys = ['projects_path', 'output_path']
        for key in required_keys:
            if key not in config:
                return False, f"config.json 缺少必需字段: {key}"
        
        return True, "配置文件格式正确"
        
    except json.JSONDecodeError as e:
        return False, f"config.json 格式错误: {e}"
    except Exception as e:
        return False, f"读取 config.json 失败: {e}"


def check_python_syntax(py_file: Path) -> tuple[bool, str]:
    """检查 Python 文件语法"""
    try:
        with open(py_file, 'r', encoding='utf-8') as f:
            code = f.read()
        
        compile(code, py_file.name, 'exec')
        return True, "语法正确"
        
    except SyntaxError as e:
        return False, f"语法错误: {e}"
    except Exception as e:
        return False, f"检查失败: {e}"


def check_file_encoding(filepath: Path) -> tuple[bool, str]:
    """检查文件编码是否为 UTF-8"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            f.read()
        return True, "UTF-8 编码"
    except UnicodeDecodeError:
        return False, "不是 UTF-8 编码"
    except Exception as e:
        return False, f"检查失败: {e}"


def main():
    print("=" * 60)
    print("技能验证脚本")
    print("=" * 60)
    print()
    
    all_passed = True
    
    # 1. 检查必需文件
    print("1. 检查必需文件...")
    print("-" * 60)
    
    for filepath in REQUIRED_FILES:
        full_path = SKILL_ROOT / filepath
        exists = check_file_exists(full_path)
        status = "✓" if exists else "✗"
        print(f"  {status} {filepath}")
        
        if not exists:
            all_passed = False
    
    print()
    
    # 2. 检查可选文件
    print("2. 检查可选文件...")
    print("-" * 60)
    
    for filepath in OPTIONAL_FILES:
        full_path = SKILL_ROOT / filepath
        exists = check_file_exists(full_path)
        status = "✓" if exists else "○"
        print(f"  {status} {filepath}")
    
    print()
    
    # 3. 检查 SKILL.md 元数据
    print("3. 检查 SKILL.md 元数据...")
    print("-" * 60)
    
    skill_md = SKILL_ROOT / 'SKILL.md'
    if skill_md.exists():
        passed, message = check_skill_metadata(skill_md)
        status = "✓" if passed else "✗"
        print(f"  {status} {message}")
        
        if not passed:
            all_passed = False
    else:
        print("  ✗ SKILL.md 不存在")
        all_passed = False
    
    print()
    
    # 4. 检查 config.json
    print("4. 检查 config.json...")
    print("-" * 60)
    
    config_file = SKILL_ROOT / 'config.json'
    if config_file.exists():
        passed, message = check_config_json(config_file)
        status = "✓" if passed else "✗"
        print(f"  {status} {message}")
        
        if not passed:
            all_passed = False
    else:
        print("  ✗ config.json 不存在")
        all_passed = False
    
    print()
    
    # 5. 检查 Python 脚本
    print("5. 检查 Python 脚本语法...")
    print("-" * 60)
    
    python_files = [
        'scripts/index_projects.py',
        'scripts/match_projects.py',
    ]
    
    for filepath in python_files:
        full_path = SKILL_ROOT / filepath
        if full_path.exists():
            passed, message = check_python_syntax(full_path)
            status = "✓" if passed else "✗"
            print(f"  {status} {filepath}: {message}")
            
            if not passed:
                all_passed = False
        else:
            print(f"  ✗ {filepath}: 文件不存在")
            all_passed = False
    
    print()
    
    # 6. 检查文件编码
    print("6. 检查文件编码...")
    print("-" * 60)
    
    text_files = [f for f in REQUIRED_FILES if f.endswith(('.md', '.py', '.json'))]
    
    for filepath in text_files:
        full_path = SKILL_ROOT / filepath
        if full_path.exists():
            passed, message = check_file_encoding(full_path)
            status = "✓" if passed else "✗"
            print(f"  {status} {filepath}: {message}")
            
            if not passed:
                all_passed = False
    
    print()
    
    # 7. 统计信息
    print("7. 统计信息...")
    print("-" * 60)
    
    total_size = 0
    file_count = 0
    
    for root, dirs, files in os.walk(SKILL_ROOT):
        # 排除 __pycache__ 和 .git
        dirs[:] = [d for d in dirs if d not in ['__pycache__', '.git', '.vscode', '.idea']]
        
        for file in files:
            if not file.endswith('.pyc'):
                filepath = Path(root) / file
                total_size += filepath.stat().st_size
                file_count += 1
    
    print(f"  文件总数: {file_count}")
    print(f"  总大小: {total_size / 1024:.2f} KB")
    
    print()
    
    # 8. 最终结果
    print("=" * 60)
    if all_passed:
        print("✓ 验证通过！技能可以上传到 ClawHub。")
        print()
        print("下一步:")
        print("  1. 查看 UPLOAD_GUIDE.md 了解上传步骤")
        print("  2. 创建 Git 仓库或压缩包")
        print("  3. 提交到 ClawHub 技能仓库")
        return 0
    else:
        print("✗ 验证失败！请修复上述问题后重新验证。")
        return 1


if __name__ == '__main__':
    exit(main())
