#!/usr/bin/env python3
"""
Skill Validator - 验证 SKILL.md 文件是否符合规范

用法:
    python skill_validator.py /path/to/skill/directory
    python skill_validator.py /path/to/SKILL.md

功能:
    1. 验证 Frontmatter 格式和必填字段
    2. 检查文件大小限制
    3. 验证命名规范
    4. 检查推荐的正文结构
    5. 提供改进建议
"""

import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

try:
    import yaml
except ImportError:
    yaml = None

# ═══════════════════════════════════════════════════════════════════════════
# 常量定义
# ═══════════════════════════════════════════════════════════════════════════

MAX_NAME_LENGTH = 64
MAX_DESCRIPTION_LENGTH = 1024
MAX_SKILL_CONTENT_CHARS = 100_000
MAX_SKILL_FILE_BYTES = 1_048_576

VALID_NAME_RE = re.compile(r'^[a-z0-9][a-z0-9._-]*$')
VALID_PLATFORMS = frozenset({'macos', 'linux', 'windows'})

# 推荐的正文部分
RECOMMENDED_SECTIONS = [
    'When to Use',
    'Prerequisites',
    'Quick Reference',
    'Procedure',
    'Pitfalls',
    'Verification',
]

# ═══════════════════════════════════════════════════════════════════════════
# 颜色输出
# ═══════════════════════════════════════════════════════════════════════════

class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def color(text: str, c: str) -> str:
    return f"{c}{text}{Colors.RESET}"

def error(msg: str) -> str:
    return color(f"✗ {msg}", Colors.RED)

def warning(msg: str) -> str:
    return color(f"⚠ {msg}", Colors.YELLOW)

def success(msg: str) -> str:
    return color(f"✓ {msg}", Colors.GREEN)

def info(msg: str) -> str:
    return color(f"ℹ {msg}", Colors.BLUE)

# ═══════════════════════════════════════════════════════════════════════════
# Frontmatter 解析
# ═══════════════════════════════════════════════════════════════════════════

def parse_frontmatter(content: str) -> Tuple[Dict[str, Any], str, Optional[str]]:
    """解析 YAML frontmatter
    
    Returns:
        (frontmatter_dict, body, error_message)
    """
    if not content.startswith('---'):
        return {}, content, "SKILL.md 必须以 YAML frontmatter (---) 开头"
    
    end_match = re.search(r'\n---\s*\n', content[3:])
    if not end_match:
        return {}, content, "Frontmatter 未正确关闭，缺少结束的 '---'"
    
    yaml_content = content[3:end_match.start() + 3]
    body = content[end_match.end() + 3:]
    
    if yaml is None:
        # 简单的 key:value 解析作为后备
        frontmatter = {}
        for line in yaml_content.strip().split('\n'):
            if ':' not in line:
                continue
            key, _, value = line.partition(':')
            frontmatter[key.strip()] = value.strip()
        return frontmatter, body, None
    
    try:
        parsed = yaml.safe_load(yaml_content)
        if not isinstance(parsed, dict):
            return {}, body, "Frontmatter 必须是 YAML 映射格式"
        return parsed, body, None
    except yaml.YAMLError as e:
        return {}, body, f"YAML 解析错误: {e}"

# ═══════════════════════════════════════════════════════════════════════════
# 验证函数
# ═══════════════════════════════════════════════════════════════════════════

def validate_name(name: str) -> List[str]:
    """验证技能名称"""
    errors = []
    
    if not name:
        errors.append("缺少 'name' 字段")
        return errors
    
    if len(name) > MAX_NAME_LENGTH:
        errors.append(f"名称超过 {MAX_NAME_LENGTH} 字符限制（当前 {len(name)} 字符）")
    
    if not VALID_NAME_RE.match(name):
        errors.append(
            f"名称 '{name}' 不符合规范。"
            "应使用小写字母、数字、连字符、下划线、点号，且必须以字母或数字开头"
        )
    
    return errors

def validate_description(description: str) -> List[str]:
    """验证描述"""
    errors = []
    
    if not description:
        errors.append("缺少 'description' 字段")
        return errors
    
    if len(description) > MAX_DESCRIPTION_LENGTH:
        errors.append(
            f"描述超过 {MAX_DESCRIPTION_LENGTH} 字符限制（当前 {len(description)} 字符）"
        )
    
    return errors

def validate_platforms(platforms: Any) -> List[str]:
    """验证平台字段"""
    warnings = []
    
    if platforms is None:
        return []
    
    if not isinstance(platforms, list):
        platforms = [platforms]
    
    for p in platforms:
        p_lower = str(p).lower()
        if p_lower not in VALID_PLATFORMS:
            warnings.append(f"未知平台 '{p}'，有效值: macos, linux, windows")
    
    return warnings

def validate_frontmatter(frontmatter: Dict[str, Any]) -> Tuple[List[str], List[str]]:
    """验证 frontmatter 的所有字段
    
    Returns:
        (errors, warnings)
    """
    errors = []
    warnings = []
    
    # 必填字段
    errors.extend(validate_name(frontmatter.get('name', '')))
    errors.extend(validate_description(frontmatter.get('description', '')))
    
    # 可选字段验证
    warnings.extend(validate_platforms(frontmatter.get('platforms')))
    
    # 推荐字段提示
    if 'version' not in frontmatter:
        warnings.append("建议添加 'version' 字段（如 1.0.0）")
    
    if 'author' not in frontmatter:
        warnings.append("建议添加 'author' 字段")
    
    # 验证 metadata.hermes 结构
    metadata = frontmatter.get('metadata')
    if metadata and isinstance(metadata, dict):
        hermes = metadata.get('hermes')
        if hermes and isinstance(hermes, dict):
            if 'tags' in hermes and not isinstance(hermes['tags'], list):
                warnings.append("'metadata.hermes.tags' 应该是列表格式")
    
    return errors, warnings

def validate_body_structure(body: str) -> List[str]:
    """验证正文结构"""
    suggestions = []
    body_lower = body.lower()
    
    for section in RECOMMENDED_SECTIONS:
        # 检查 ## Section 或 # Section 格式
        pattern = rf'#{{1,2}}\s*{re.escape(section.lower())}'
        if not re.search(pattern, body_lower):
            suggestions.append(f"建议添加 '{section}' 部分")
    
    return suggestions

def validate_content_size(content: str, path: Path) -> List[str]:
    """验证内容大小"""
    errors = []
    
    if len(content) > MAX_SKILL_CONTENT_CHARS:
        errors.append(
            f"SKILL.md 内容超过 {MAX_SKILL_CONTENT_CHARS:,} 字符限制"
            f"（当前 {len(content):,} 字符）"
        )
    
    file_size = path.stat().st_size
    if file_size > MAX_SKILL_FILE_BYTES:
        errors.append(
            f"文件大小超过 {MAX_SKILL_FILE_BYTES:,} 字节限制"
            f"（当前 {file_size:,} 字节）"
        )
    
    return errors

def validate_supporting_files(skill_dir: Path) -> Tuple[List[str], List[str]]:
    """验证支撑文件"""
    errors = []
    info_messages = []
    
    allowed_subdirs = {'references', 'templates', 'scripts', 'assets'}
    
    for item in skill_dir.iterdir():
        if item.name == 'SKILL.md':
            continue
        
        if item.is_file():
            # 根目录下不应有其他文件
            if item.suffix not in {'.md', '.txt'}:
                errors.append(f"根目录下有非预期文件: {item.name}")
        
        elif item.is_dir():
            if item.name not in allowed_subdirs:
                errors.append(
                    f"非预期的子目录: {item.name}。"
                    f"允许的子目录: {', '.join(sorted(allowed_subdirs))}"
                )
            else:
                # 统计支撑文件
                file_count = sum(1 for f in item.rglob('*') if f.is_file())
                if file_count > 0:
                    info_messages.append(f"{item.name}/: {file_count} 个文件")
    
    return errors, info_messages

# ═══════════════════════════════════════════════════════════════════════════
# 主验证函数
# ═══════════════════════════════════════════════════════════════════════════

def validate_skill(path: Path) -> int:
    """验证一个 Skill
    
    Args:
        path: SKILL.md 文件或 Skill 目录的路径
    
    Returns:
        0 表示成功，1 表示有错误
    """
    # 确定 SKILL.md 路径
    if path.is_dir():
        skill_md = path / 'SKILL.md'
        skill_dir = path
    else:
        skill_md = path
        skill_dir = path.parent
    
    if not skill_md.exists():
        print(error(f"找不到 SKILL.md: {skill_md}"))
        return 1
    
    print(f"\n{Colors.BOLD}验证 Skill: {skill_dir.name}{Colors.RESET}")
    print("=" * 60)
    
    all_errors = []
    all_warnings = []
    all_suggestions = []
    all_info = []
    
    # 读取内容
    try:
        content = skill_md.read_text(encoding='utf-8')
    except Exception as e:
        print(error(f"读取文件失败: {e}"))
        return 1
    
    # 验证文件大小
    size_errors = validate_content_size(content, skill_md)
    all_errors.extend(size_errors)
    
    # 解析 frontmatter
    frontmatter, body, parse_error = parse_frontmatter(content)
    if parse_error:
        all_errors.append(parse_error)
    
    # 验证 frontmatter
    fm_errors, fm_warnings = validate_frontmatter(frontmatter)
    all_errors.extend(fm_errors)
    all_warnings.extend(fm_warnings)
    
    # 验证正文结构
    body_suggestions = validate_body_structure(body)
    all_suggestions.extend(body_suggestions)
    
    # 验证支撑文件
    if skill_dir.exists():
        file_errors, file_info = validate_supporting_files(skill_dir)
        all_errors.extend(file_errors)
        all_info.extend(file_info)
    
    # 输出结果
    print()
    
    if all_errors:
        print(f"{Colors.RED}错误 ({len(all_errors)}):{Colors.RESET}")
        for e in all_errors:
            print(f"  {error(e)}")
        print()
    
    if all_warnings:
        print(f"{Colors.YELLOW}警告 ({len(all_warnings)}):{Colors.RESET}")
        for w in all_warnings:
            print(f"  {warning(w)}")
        print()
    
    if all_suggestions:
        print(f"{Colors.BLUE}建议 ({len(all_suggestions)}):{Colors.RESET}")
        for s in all_suggestions:
            print(f"  {info(s)}")
        print()
    
    if all_info:
        print(f"{Colors.GREEN}支撑文件:{Colors.RESET}")
        for i in all_info:
            print(f"  {success(i)}")
        print()
    
    # 总结
    if all_errors:
        print(error(f"验证失败：发现 {len(all_errors)} 个错误"))
        return 1
    elif all_warnings:
        print(warning(f"验证通过（有 {len(all_warnings)} 个警告）"))
        return 0
    else:
        print(success("验证通过 ✓"))
        return 0

# ═══════════════════════════════════════════════════════════════════════════
# 入口
# ═══════════════════════════════════════════════════════════════════════════

def main():
    if len(sys.argv) < 2:
        print("用法: python skill_validator.py <skill_path>")
        print()
        print("  skill_path: SKILL.md 文件或 Skill 目录的路径")
        print()
        print("示例:")
        print("  python skill_validator.py ~/.hermes/skills/my-skill/")
        print("  python skill_validator.py ./SKILL.md")
        sys.exit(1)
    
    path = Path(sys.argv[1]).expanduser().resolve()
    
    if not path.exists():
        print(error(f"路径不存在: {path}"))
        sys.exit(1)
    
    exit_code = validate_skill(path)
    sys.exit(exit_code)

if __name__ == '__main__':
    main()
