#!/usr/bin/env python3
"""
会议纪要生成器 - 技能验证脚本
验证 SKILL.md frontmatter、结构完整性和文件合规性
"""

import json
import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple


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


def print_warning(msg: str):
    print(f"{Colors.YELLOW}⚠{Colors.RESET} {msg}")


def print_info(msg: str):
    print(f"{Colors.BLUE}ℹ{Colors.RESET} {msg}")


def validate_frontmatter(skill_path: Path) -> Tuple[bool, List[str]]:
    """验证 SKILL.md frontmatter"""
    errors = []
    skill_md = skill_path / "SKILL.md"
    
    if not skill_md.exists():
        errors.append("SKILL.md 文件不存在")
        return False, errors
    
    content = skill_md.read_text(encoding='utf-8')
    
    # 检查是否以 --- 开头
    if not content.strip().startswith('---'):
        errors.append("SKILL.md 必须以 YAML frontmatter --- 开头")
    
    # 提取 frontmatter
    if content.startswith('---'):
        end_match = re.search(r'^---$', content[3:], re.MULTILINE)
        if end_match:
            frontmatter = content[3:end_match.start()].strip()
        else:
            errors.append("缺少 closing --- 分隔符")
            return False, errors
    else:
        errors.append("无法解析 frontmatter")
        return False, errors
    
    # 检查必需字段
    required_fields = ['name', 'description']
    for field in required_fields:
        if not re.search(rf'^{field}:', frontmatter, re.MULTILINE):
            errors.append(f"缺少必需字段: {field}")
    
    # 检查 name 格式
    name_match = re.search(r'^name:\s*(.+?)\s*$', frontmatter, re.MULTILINE)
    if name_match:
        name = name_match.group(1).strip()
        if not re.match(r'^[a-z0-9-]+$', name):
            errors.append(f"name 字段格式错误: '{name}' (应使用小写字母、数字和连字符)")
        if len(name) > 64:
            errors.append(f"name 长度超过64字符限制: {len(name)}")
    
    # 检查 description 包含触发短语
    desc_match = re.search(r'^description:\s*(.+?)(?=\n\w|$)', frontmatter, re.DOTALL | re.MULTILINE)
    if desc_match:
        desc = desc_match.group(1).strip()
        if 'Use when' not in desc and '当用户' not in desc:
            errors.append("description 应包含触发短语 (如 'Use when...' 或 '当用户...')")
    
    return len(errors) == 0, errors


def validate_meta_json(skill_path: Path) -> Tuple[bool, List[str]]:
    """验证 _meta.json"""
    errors = []
    meta_file = skill_path / "_meta.json"
    
    if not meta_file.exists():
        errors.append("_meta.json 文件不存在")
        return False, errors
    
    try:
        meta = json.loads(meta_file.read_text(encoding='utf-8'))
    except json.JSONDecodeError as e:
        errors.append(f"_meta.json 格式错误: {e}")
        return False, errors
    
    # 检查必需字段
    required_fields = ['id', 'version']
    for field in required_fields:
        if field not in meta:
            errors.append(f"_meta.json 缺少字段: {field}")
    
    # 检查 version 格式
    if 'version' in meta:
        if not re.match(r'^\d+\.\d+\.\d+$', meta['version']):
            errors.append(f"version 格式错误: '{meta['version']}' (应为 x.y.z 格式)")
    
    return len(errors) == 0, errors


def validate_structure(skill_path: Path) -> Tuple[bool, List[str]]:
    """验证目录结构"""
    errors = []
    
    # 检查必需文件
    required_files = ['SKILL.md', '_meta.json']
    for fname in required_files:
        if not (skill_path / fname).exists():
            errors.append(f"缺少必需文件: {fname}")
    
    # 检查 references 目录
    refs_dir = skill_path / "references"
    if refs_dir.exists():
        if not refs_dir.is_dir():
            errors.append("references 应该是目录")
        else:
            md_files = list(refs_dir.glob("*.md"))
            if not md_files:
                errors.append("references 目录为空，应包含相关文档")
    
    # 检查是否有 scripts 目录（可选但建议）
    scripts_dir = skill_path / "scripts"
    if scripts_dir.exists() and not list(scripts_dir.glob("*.py")):
        print_warning("scripts 目录存在但没有 Python 脚本")
    
    return len(errors) == 0, errors


def validate_naming(skill_path: Path) -> Tuple[bool, List[str]]:
    """验证文件和目录命名（英文、无空格）"""
    errors = []
    
    # 检查根目录文件
    for item in skill_path.iterdir():
        if item.name.startswith('.') or item.name.startswith('_'):
            continue
        
        # 检查是否包含非ASCII字符
        if not item.name.isascii():
            errors.append(f"文件名包含非ASCII字符: {item.name}")
        
        # 检查是否包含空格
        if ' ' in item.name:
            errors.append(f"文件名包含空格: {item.name}")
    
    # 检查 references 目录下的文件
    refs_dir = skill_path / "references"
    if refs_dir.exists():
        for item in refs_dir.rglob("*"):
            if item.is_file():
                if not item.name.isascii():
                    errors.append(f"文件路径包含非ASCII字符: {item}")
                if ' ' in str(item):
                    errors.append(f"文件路径包含空格: {item}")
    
    return len(errors) == 0, errors


def validate_security(skill_path: Path) -> Tuple[bool, List[str]]:
    """安全检查 - 排除敏感文件"""
    errors = []
    warnings = []
    
    # 敏感文件模式
    sensitive_patterns = [
        r'\.env$', r'\.pem$', r'\.key$', r'\.secret$',
        r'credentials', r'password', r'api_key', r'token'
    ]
    
    for item in skill_path.rglob("*"):
        if item.is_file():
            name_lower = item.name.lower()
            for pattern in sensitive_patterns:
                if re.search(pattern, name_lower, re.IGNORECASE):
                    errors.append(f"发现敏感文件: {item}")
    
    # 检查 symlinks
    for item in skill_path.rglob("*"):
        if item.is_symlink():
            errors.append(f"发现符号链接: {item}")
    
    return len(errors) == 0, errors


def run_validation(skill_path: str) -> bool:
    """运行所有验证"""
    skill_path = Path(skill_path).resolve()
    
    print(f"\n{Colors.BOLD}{'='*60}")
    print(f"会议纪要生成器 - 技能验证")
    print(f"{'='*60}{Colors.RESET}\n")
    print_info(f"技能路径: {skill_path}\n")
    
    all_passed = True
    
    # 1. Frontmatter 验证
    print(f"{Colors.BOLD}[1/5] 验证 Frontmatter...{Colors.RESET}")
    passed, errors = validate_frontmatter(skill_path)
    if passed:
        print_success("Frontmatter 验证通过")
    else:
        all_passed = False
        for err in errors:
            print_error(err)
    print()
    
    # 2. _meta.json 验证
    print(f"{Colors.BOLD}[2/5] 验证 _meta.json...{Colors.RESET}")
    passed, errors = validate_meta_json(skill_path)
    if passed:
        print_success("_meta.json 验证通过")
    else:
        all_passed = False
        for err in errors:
            print_error(err)
    print()
    
    # 3. 目录结构验证
    print(f"{Colors.BOLD}[3/5] 验证目录结构...{Colors.RESET}")
    passed, errors = validate_structure(skill_path)
    if passed:
        print_success("目录结构验证通过")
    else:
        all_passed = False
        for err in errors:
            print_error(err)
    print()
    
    # 4. 文件命名验证
    print(f"{Colors.BOLD}[4/5] 验证文件命名...{Colors.RESET}")
    passed, errors = validate_naming(skill_path)
    if passed:
        print_success("文件命名验证通过")
    else:
        all_passed = False
        for err in errors:
            print_error(err)
    print()
    
    # 5. 安全检查
    print(f"{Colors.BOLD}[5/5] 安全检查...{Colors.RESET}")
    passed, errors = validate_security(skill_path)
    if passed:
        print_success("安全检查通过")
    else:
        all_passed = False
        for err in errors:
            print_error(err)
    print()
    
    # 总结
    print(f"{Colors.BOLD}{'='*60}")
    if all_passed:
        print_success("所有验证通过！技能已准备好打包。")
        print(f"{'='*60}{Colors.RESET}\n")
        return True
    else:
        print_error("部分验证未通过，请修复上述问题后重试。")
        print(f"{'='*60}{Colors.RESET}\n")
        return False


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python quick_validate.py <skill_path>")
        sys.exit(1)
    
    skill_path = sys.argv[1]
    success = run_validation(skill_path)
    sys.exit(0 if success else 1)
