#!/usr/bin/env python3
"""
技能验证脚本 - 验证 self-correction 技能的结构和内容
"""

import os
import sys
import json
import re
from pathlib import Path

def validate_frontmatter(skill_md_path):
    """验证SKILL.md的frontmatter格式"""
    with open(skill_md_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 检查frontmatter是否在文件开头
    if not content.startswith('---'):
        return False, "SKILL.md必须以---开头的frontmatter开始"

    # 提取frontmatter
    frontmatter_match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if not frontmatter_match:
        return False, "无法解析frontmatter"

    frontmatter_text = frontmatter_match.group(1)

    # 检查必需的字段
    required_fields = ['name', 'description']
    for field in required_fields:
        if not re.search(f'^{field}:', frontmatter_text, re.MULTILINE):
            return False, f"frontmatter缺少必需字段: {field}"

    # 提取name和description
    name_match = re.search(r'^name:\s*(.+)$', frontmatter_text, re.MULTILINE)
    desc_match = re.search(r'^description:\s*(.+)$', frontmatter_text, re.MULTILINE)

    if name_match:
        name = name_match.group(1).strip()
        # 检查name是否为英文（允许连字符）
        if not re.match(r'^[a-z0-9-]+$', name):
            return False, f"name字段必须为英文（仅允许小写字母、数字和连字符），当前值: {name}"

    return True, "frontmatter验证通过"

def validate_meta_json(meta_path):
    """验证_meta.json格式"""
    with open(meta_path, 'r', encoding='utf-8') as f:
        meta = json.load(f)

    required_fields = ['id', 'version']
    for field in required_fields:
        if field not in meta:
            return False, f"_meta.json缺少必需字段: {field}"

    # 验证版本格式
    version = meta.get('version', '')
    if not re.match(r'^\d+\.\d+\.\d+$', version):
        return False, f"version字段格式不正确，应为x.y.z格式，当前值: {version}"

    return True, "_meta.json验证通过"

def validate_naming(skill_dir):
    """验证目录和文件命名"""
    dir_name = os.path.basename(skill_dir)

    # 检查目录名是否为英文
    if not re.match(r'^[a-z0-9-]+$', dir_name):
        return False, f"目录名必须为英文小写，当前值: {dir_name}"

    # 检查SKILL.md中的name是否与目录名匹配
    skill_md_path = os.path.join(skill_dir, 'SKILL.md')
    with open(skill_md_path, 'r', encoding='utf-8') as f:
        content = f.read()

    name_match = re.search(r'^name:\s*(.+)$', content, re.MULTILINE)
    if name_match:
        frontmatter_name = name_match.group(1).strip()
        if frontmatter_name != dir_name:
            return False, f"SKILL.md中的name({frontmatter_name})与目录名({dir_name})不匹配"

    return True, "命名验证通过"

def validate_description(skill_md_path):
    """验证description包含触发短语"""
    with open(skill_md_path, 'r', encoding='utf-8') as f:
        content = f.read()

    desc_match = re.search(r'^description:\s*(.+)$', content, re.MULTILINE)
    if not desc_match:
        return False, "未找到description字段"

    desc = desc_match.group(1)

    # 检查description是否包含"当用户..."或"Use when"等触发短语
    trigger_patterns = [
        r'当用户',
        r'触发',
        r'Use when',
        r'utilisé quand'
    ]

    has_trigger = any(re.search(pattern, desc, re.IGNORECASE) for pattern in trigger_patterns)
    if not has_trigger:
        return False, "description应包含触发条件描述（如'当用户...'或'Use when...'）"

    return True, "description验证通过"

def validate_structure(skill_dir):
    """验证技能目录结构"""
    required_files = ['SKILL.md', '_meta.json']
    for file in required_files:
        file_path = os.path.join(skill_dir, file)
        if not os.path.exists(file_path):
            return False, f"缺少必需文件: {file}"

    return True, "结构验证通过"

def validate_no_secrets(skill_dir):
    """检查是否有泄露的密钥或敏感信息（仅检查SKILL.md和_meta.json）"""
    # 只检查技能核心文件，不检查scripts目录
    forbidden_patterns = [
        r'password\s*=\s*["\'][^"\']+["\']',
        r'api_key\s*=\s*["\'][^"\']+["\']',
        r'secret_key\s*=\s*["\'][^"\']+["\']',
        r'token\s*=\s*["\'][^"\']+["\']',
        r'-----BEGIN.*PRIVATE KEY-----',
    ]

    # 只检查核心技能文件
    files_to_check = [
        os.path.join(skill_dir, 'SKILL.md'),
        os.path.join(skill_dir, '_meta.json'),
    ]

    for file_path in files_to_check:
        if not os.path.exists(file_path):
            continue
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            for pattern in forbidden_patterns:
                if re.search(pattern, content, re.IGNORECASE):
                    return False, f"发现可能泄露的敏感信息在 {os.path.basename(file_path)}"

    return True, "安全检查通过"

def run_validation(skill_dir):
    """运行所有验证"""
    print("=" * 50)
    print("开始验证 self-correction 技能")
    print("=" * 50)

    validations = [
        ("结构验证", lambda: validate_structure(skill_dir)),
        ("frontmatter验证", lambda: validate_frontmatter(os.path.join(skill_dir, 'SKILL.md'))),
        ("_meta.json验证", lambda: validate_meta_json(os.path.join(skill_dir, '_meta.json'))),
        ("命名验证", lambda: validate_naming(skill_dir)),
        ("description验证", lambda: validate_description(os.path.join(skill_dir, 'SKILL.md'))),
        ("安全检查", lambda: validate_no_secrets(skill_dir)),
    ]

    all_passed = True
    for name, validator in validations:
        passed, message = validator()
        status = "✅ 通过" if passed else "❌ 失败"
        print(f"[{status}] {name}: {message}")
        if not passed:
            all_passed = False

    print("=" * 50)
    if all_passed:
        print("✅ 所有验证通过！")
        return 0
    else:
        print("❌ 存在验证失败项")
        return 1

if __name__ == '__main__':
    skill_dir = sys.argv[1] if len(sys.argv) > 1 else '/workspace/temp-skills/self-correction'
    exit_code = run_validation(skill_dir)
    sys.exit(exit_code)
