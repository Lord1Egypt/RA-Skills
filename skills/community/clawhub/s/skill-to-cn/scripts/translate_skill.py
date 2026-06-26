#!/usr/bin/env python3
"""
技能汉化脚本
将 Claude Code 技能翻译为中文版本
"""

import argparse
import os
import re
import shutil
import sys
from pathlib import Path


def is_binary_file(file_path: Path) -> bool:
    """检测文件是否为二进制文件"""
    # 常见二进制文件扩展名
    binary_extensions = {
        # 图片
        '.png', '.jpg', '.jpeg', '.gif', '.bmp', '.ico', '.webp', '.svg', '.tiff', '.tif',
        # 音频
        '.mp3', '.wav', '.ogg', '.flac', '.aac', '.m4a', '.wma',
        # 视频
        '.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm',
        # 压缩包
        '.zip', '.tar', '.gz', '.rar', '.7z', '.bz2', '.xz',
        # 可执行文件
        '.exe', '.dll', '.so', '.dylib', '.app', '.dmg', '.deb', '.rpm',
        # 数据库
        '.db', '.sqlite', '.sqlite3',
        # 字体
        '.ttf', '.otf', '.woff', '.woff2', '.eot',
        # PDF 和文档
        '.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx',
        # 其他二进制
        '.bin', '.dat', '.iso', '.img', '.class', '.jar', '.war', '.pyc', '.pyo',
    }

    ext = file_path.suffix.lower()
    if ext in binary_extensions:
        return True

    # 通过文件内容检测：尝试读取前 8192 字节，检查是否包含空字节
    try:
        with open(file_path, 'rb') as f:
            chunk = f.read(8192)
            if b'\x00' in chunk:
                return True
    except (IOError, OSError):
        pass

    return False


def parse_args():
    parser = argparse.ArgumentParser(
        description="将 Claude Code 技能汉化为中文版本",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s pdf-editor
  %(prog)s /path/to/skill --output /custom/output
  %(prog)s my-skill --no-translate
        """
    )
    parser.add_argument(
        "skill",
        help="源技能名称或完整路径"
    )
    parser.add_argument(
        "--output", "-o",
        help="输出目录路径（默认：~/.claude/skills/<技能名>-cn/）"
    )
    parser.add_argument(
        "--no-translate",
        action="store_true",
        help="仅复制结构，不执行翻译（用于手动翻译）"
    )
    return parser.parse_args()


def get_skill_paths(skill_name: str, output_override: str = None) -> tuple:
    """获取源技能路径和目标路径"""
    skills_dir = Path.home() / ".claude" / "skills"

    # 判断是完整路径还是技能名
    if "/" in skill_name or skill_name.startswith("~"):
        source_path = Path(skill_name).expanduser().resolve()
    else:
        source_path = skills_dir / skill_name

    # 验证源路径存在
    if not source_path.exists():
        print(f"❌ 错误：技能目录不存在: {source_path}")
        sys.exit(1)

    # 确定目标路径
    if output_override:
        target_path = Path(output_override).expanduser().resolve()
    else:
        skill_dir_name = source_path.name
        if skill_dir_name.endswith("-cn"):
            print(f"❌ 错误：源技能已是中文版本: {skill_dir_name}")
            sys.exit(1)
        target_path = source_path.parent / f"{skill_dir_name}-cn"

    return source_path, target_path


def translate_yaml_metadata(content: str) -> str:
    """翻译 SKILL.md 的 YAML 前置元数据"""
    # 匹配 YAML 前置元数据
    yaml_pattern = r'^---\s*\n(.*?)\n---\s*\n'
    match = re.match(yaml_pattern, content, re.DOTALL)

    if not match:
        return content

    yaml_content = match.group(1)

    # 解析 YAML 字段
    lines = yaml_content.split('\n')
    translated_lines = []

    for line in lines:
        if line.startswith('name:'):
            # 添加 -cn 后缀
            name = line.split(':', 1)[1].strip()
            if not name.endswith('-cn'):
                name = f"{name}-cn"
            translated_lines.append(f"name: {name}")
        elif line.startswith('description:'):
            # 标记需要翻译
            desc = line.split(':', 1)[1].strip()
            translated_lines.append(f"description: [待翻译] {desc}")
        else:
            translated_lines.append(line)

    # 重建内容
    translated_yaml = '---\n' + '\n'.join(translated_lines) + '\n---\n'
    return translated_yaml + content[match.end():]


def translate_python_comments(content: str) -> str:
    """翻译 Python 文件中的注释和文档字符串"""
    lines = content.split('\n')
    translated_lines = []

    in_docstring = False
    docstring_char = None

    for line in lines:
        # 检测文档字符串开始/结束
        stripped = line.strip()

        if not in_docstring:
            # 跳过 shebang 行
            if stripped.startswith('#!'):
                translated_lines.append(line)
            # 检查是否开始文档字符串
            elif stripped.startswith('"""') or stripped.startswith("'''"):
                docstring_char = stripped[:3]
                if stripped.count(docstring_char) >= 2:
                    # 单行文档字符串
                    translated_lines.append(f"# [待翻译] {line}")
                else:
                    in_docstring = True
                    translated_lines.append(f"# [待翻译] {line}")
            elif stripped.startswith('#'):
                # 普通注释
                translated_lines.append(f"# [待翻译] {line}")
            else:
                translated_lines.append(line)
        else:
            translated_lines.append(f"# [待翻译] {line}")
            if docstring_char in stripped:
                in_docstring = False

    return '\n'.join(translated_lines)


# 定义各语言的注释规则
COMMENT_RULES = {
    # 单行注释符号 -> 是否支持多行注释
    'hash': {  # # 风格：Python, Shell, Ruby, YAML, TOML, etc.
        'single': '#',
        'multi_start': None,
        'multi_end': None,
    },
    'double_slash': {  # // 风格：JavaScript, TypeScript, Java, C, C++, Go, Rust, etc.
        'single': '//',
        'multi_start': '/*',
        'multi_end': '*/',
    },
    'html': {  # HTML, XML
        'single': None,
        'multi_start': '<!--',
        'multi_end': '-->',
    },
    'css': {  # CSS, SCSS, LESS
        'single': None,
        'multi_start': '/*',
        'multi_end': '*/',
    },
}

# 文件扩展名到注释规则的映射
EXT_TO_RULE = {
    # Hash 风格
    '.py': 'hash',
    '.sh': 'hash',
    '.bash': 'hash',
    '.zsh': 'hash',
    '.rb': 'hash',
    '.yaml': 'hash',
    '.yml': 'hash',
    '.toml': 'hash',
    '.r': 'hash',
    '.R': 'hash',
    '.perl': 'hash',
    '.pl': 'hash',
    '.pm': 'hash',
    # Double slash 风格
    '.js': 'double_slash',
    '.jsx': 'double_slash',
    '.ts': 'double_slash',
    '.tsx': 'double_slash',
    '.java': 'double_slash',
    '.c': 'double_slash',
    '.cpp': 'double_slash',
    '.cc': 'double_slash',
    '.cxx': 'double_slash',
    '.h': 'double_slash',
    '.hpp': 'double_slash',
    '.go': 'double_slash',
    '.rs': 'double_slash',
    '.swift': 'double_slash',
    '.kt': 'double_slash',
    '.kts': 'double_slash',
    '.scala': 'double_slash',
    '.cs': 'double_slash',
    '.php': 'double_slash',  # PHP 也支持 //
    # HTML 风格
    '.html': 'html',
    '.htm': 'html',
    '.xml': 'html',
    '.vue': 'html',  # Vue 文件中 HTML 部分用 HTML 注释
    '.svelte': 'html',
    # CSS 风格
    '.css': 'css',
    '.scss': 'css',
    '.less': 'css',
}


def translate_generic_code_comments(content: str, rule_name: str) -> str:
    """翻译通用代码文件中的注释"""
    rule = COMMENT_RULES.get(rule_name)
    if not rule:
        return content

    lines = content.split('\n')
    translated_lines = []
    in_multi_comment = False

    single_char = rule.get('single')
    multi_start = rule.get('multi_start')
    multi_end = rule.get('multi_end')

    for line in lines:
        stripped = line.strip()

        if in_multi_comment:
            # 在多行注释中
            translated_lines.append(f"{single_char or '//'} [待翻译] {line}")
            if multi_end and multi_end in stripped:
                in_multi_comment = False
        elif stripped.startswith('#!'):
            # 跳过 shebang 行
            translated_lines.append(line)
        elif multi_start and stripped.startswith(multi_start):
            # 多行注释开始
            if multi_end in stripped and stripped.find(multi_end) > stripped.find(multi_start):
                # 单行内的多行注释
                translated_lines.append(f"{single_char or '//'} [待翻译] {line}")
            else:
                in_multi_comment = True
                translated_lines.append(f"{single_char or '//'} [待翻译] {line}")
        elif single_char and stripped.startswith(single_char):
            # 单行注释
            translated_lines.append(f"{single_char} [待翻译] {line}")
        else:
            translated_lines.append(line)

    return '\n'.join(translated_lines)


def translate_code_file(source_file: Path, target_file: Path, translate: bool = True):
    """处理任意代码文件，翻译注释和输出内容"""
    # 检测是否为二进制文件
    if is_binary_file(source_file):
        shutil.copy2(source_file, target_file)
        print(f"  📦 已复制（二进制）: scripts/{source_file.name}")
        return

    content = source_file.read_text(encoding='utf-8')

    if translate:
        ext = source_file.suffix.lower()
        rule_name = EXT_TO_RULE.get(ext)

        if ext == '.py':
            # Python 有特殊的文档字符串处理
            content = translate_python_comments(content)
        elif rule_name:
            # 使用通用注释翻译
            content = translate_generic_code_comments(content, rule_name)
        else:
            # 未知类型，原样复制
            pass

    target_file.write_text(content, encoding='utf-8')
    # 保留原始文件权限（如可执行权限）
    shutil.copymode(source_file, target_file)
    print(f"  📝 {'已翻译' if translate else '已复制'}: scripts/{source_file.name}")


def translate_markdown(content: str) -> str:
    """翻译 Markdown 文件内容（标记待翻译）"""
    lines = content.split('\n')
    translated_lines = []
    in_code_block = False
    in_yaml_front_matter = False
    yaml_count = 0

    for i, line in enumerate(lines):
        stripped = line.strip()

        # 检测 YAML 前置元数据（已由 translate_yaml_metadata 处理，跳过）
        if stripped == '---':
            yaml_count += 1
            if yaml_count == 1:
                in_yaml_front_matter = True
            elif yaml_count == 2:
                in_yaml_front_matter = False
            translated_lines.append(line)
            continue

        if in_yaml_front_matter:
            translated_lines.append(line)
            continue

        # 检测代码块
        if stripped.startswith('```'):
            in_code_block = not in_code_block
            translated_lines.append(line)
        elif in_code_block:
            # 代码块内容不翻译
            translated_lines.append(line)
        elif not stripped:
            # 空行保留
            translated_lines.append(line)
        elif stripped.startswith('- ✅') or stripped.startswith('- **') or stripped.startswith('| '):
            # 列表项、表格行：标记待翻译
            translated_lines.append(f"[待翻译] {line}")
        elif stripped.startswith('#'):
            # Markdown 标题
            translated_lines.append(f"[待翻译] {line}")
        elif stripped.startswith('- ') or stripped.startswith('* ') or re.match(r'^\d+\.', stripped):
            # 无序/有序列表
            translated_lines.append(f"[待翻译] {line}")
        elif stripped.startswith('![') or stripped.startswith('['):
            # 链接或图片引用，保留
            translated_lines.append(line)
        else:
            # 普通描述性文本
            translated_lines.append(f"[待翻译] {line}")

    return '\n'.join(translated_lines)


def process_readme_file(source_file: Path, target_file: Path, translate: bool = True):
    """处理 README.md 文件，翻译为 README-cn.md"""
    content = source_file.read_text(encoding='utf-8')

    if translate:
        content = translate_markdown(content)

    target_file.write_text(content, encoding='utf-8')
    print(f"  📝 {'已翻译' if translate else '已复制'}: README.md → README-cn.md")


def process_skill_md(source_file: Path, target_file: Path, translate: bool = True):
    """处理 SKILL.md 文件"""
    content = source_file.read_text(encoding='utf-8')

    if translate:
        content = translate_yaml_metadata(content)
        content = translate_markdown(content)

    target_file.write_text(content, encoding='utf-8')
    print(f"  📝 {'已翻译' if translate else '已复制'}: SKILL.md")


def process_reference_file(source_file: Path, target_file: Path, translate: bool = True):
    """处理参考文档"""
    # 检测是否为二进制文件
    if is_binary_file(source_file):
        shutil.copy2(source_file, target_file)
        print(f"  📦 已复制（二进制）: references/{source_file.name}")
        return

    content = source_file.read_text(encoding='utf-8')

    if translate and source_file.suffix == '.md':
        content = translate_markdown(content)

    target_file.write_text(content, encoding='utf-8')
    print(f"  📝 {'已翻译' if translate else '已复制'}: references/{source_file.name}")


def copy_asset(source_file: Path, target_file: Path):
    """复制资产文件"""
    shutil.copy2(source_file, target_file)
    file_type = "二进制" if is_binary_file(source_file) else "文件"
    print(f"  📦 已复制（{file_type}）: assets/{source_file.name}")


def translate_skill(source_path: Path, target_path: Path, translate: bool = True):
    """执行技能汉化"""
    print(f"\n{'='*50}")
    print(f"🔧 技能汉化工具")
    print(f"{'='*50}")
    print(f"📂 源路径: {source_path}")
    print(f"📂 目标路径: {target_path}")
    print(f"🌐 翻译模式: {'开启' if translate else '关闭（仅复制）'}")
    print(f"{'='*50}\n")

    # 创建目标目录
    if target_path.exists():
        print(f"⚠️  目标目录已存在，将被覆盖")
        shutil.rmtree(target_path)

    target_path.mkdir(parents=True)

    # 处理 SKILL.md
    skill_md = source_path / "SKILL.md"
    if skill_md.exists():
        process_skill_md(skill_md, target_path / "SKILL.md", translate)
    else:
        print(f"⚠️  未找到 SKILL.md")

    # 处理 scripts/
    scripts_dir = source_path / "scripts"
    if scripts_dir.exists():
        target_scripts = target_path / "scripts"
        target_scripts.mkdir()
        print(f"\n📁 处理 scripts/")
        for script_file in scripts_dir.iterdir():
            if script_file.is_file():
                # 处理所有代码文件，翻译注释和输出内容
                translate_code_file(script_file, target_scripts / script_file.name, translate)

    # 处理 references/
    refs_dir = source_path / "references"
    if refs_dir.exists():
        target_refs = target_path / "references"
        target_refs.mkdir()
        print(f"\n📁 处理 references/")
        for ref_file in refs_dir.iterdir():
            if ref_file.is_file():
                process_reference_file(ref_file, target_refs / ref_file.name, translate)

    # 处理 assets/
    assets_dir = source_path / "assets"
    if assets_dir.exists():
        target_assets = target_path / "assets"
        target_assets.mkdir()
        print(f"\n📁 处理 assets/")
        for asset_file in assets_dir.iterdir():
            if asset_file.is_file():
                copy_asset(asset_file, target_assets / asset_file.name)
            elif asset_file.is_dir():
                shutil.copytree(asset_file, target_assets / asset_file.name)
                print(f"  📦 已复制目录: assets/{asset_file.name}")

    # 处理 README.md（翻译为 README-cn.md）
    readme_md = source_path / "README.md"
    readme_cn = target_path / "README-cn.md"
    if readme_md.exists() and not readme_cn.exists():
        process_readme_file(readme_md, readme_cn, translate)
    else:
        # 处理根目录中的其他文件（SKILL.md、README.md 以外的文件，如 LICENSE.txt 等）
        known_dirs = {'scripts', 'references', 'assets'}
        root_files = [
            f for f in source_path.iterdir()
            if f.is_file() and f.name not in ('SKILL.md', 'README.md')
        ]
        if root_files:
            print(f"\n📁 处理根目录其他文件")
            for root_file in root_files:
                shutil.copy2(root_file, target_path / root_file.name)
                print(f"  📦 已复制: {root_file.name}")

    print(f"\n{'='*50}")
    print(f"✅ 汉化完成！")
    print(f"{'='*50}")
    print(f"\n后续步骤:")
    print(f"1. 检查目标目录: {target_path}")
    if translate:
        print(f"2. 编辑 SKILL.md 完成标记为 [待翻译] 的内容")
        print(f"3. 检查并完善翻译质量")
    print()


def main():
    args = parse_args()
    source_path, target_path = get_skill_paths(args.skill, args.output)
    translate_skill(source_path, target_path, translate=not args.no_translate)


if __name__ == "__main__":
    main()
