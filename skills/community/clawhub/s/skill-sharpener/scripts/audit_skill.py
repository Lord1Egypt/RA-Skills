#!/usr/bin/env python3
"""
Skill Quality Auditor - 自动化结构分析脚本

用法：python scripts/audit_skill.py <skill目录路径>

输出：
- SKILL.md 行数统计
- 文件树结构
- Frontmatter 字段检查
- 自动检测的常见反模式
"""

import sys
import os
import re
import io
from pathlib import Path

# Windows 终端 UTF-8 输出支持
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")


def count_lines(filepath: Path) -> int:
    """统计文件行数。"""
    try:
        return len(filepath.read_text(encoding="utf-8").splitlines())
    except Exception as e:
        return -1


def parse_frontmatter(content: str) -> dict:
    """
    从 SKILL.md 内容中提取 YAML frontmatter。
    返回字段字典，解析失败返回空字典。
    """
    if not content.startswith("---"):
        return {}

    end = content.find("---", 3)
    if end == -1:
        return {}

    frontmatter_text = content[3:end].strip()
    result = {}

    for line in frontmatter_text.splitlines():
        if ":" in line:
            key, _, value = line.partition(":")
            result[key.strip()] = value.strip()

    return result


def check_name(name: str) -> list[str]:
    """
    检查 name 字段是否符合规范。
    返回问题列表（空表示通过）。
    """
    issues = []

    if not name:
        issues.append("❌ name 字段为空")
        return issues

    if len(name) > 64:
        issues.append(f"❌ name 超过 64 字符（当前 {len(name)} 字符）")

    if not re.match(r"^[a-z0-9-]+$", name):
        issues.append(f"❌ name 包含非法字符（只允许小写字母、数字、连字符）：`{name}`")

    reserved_words = ["anthropic", "claude"]
    for word in reserved_words:
        if word in name:
            issues.append(f"❌ name 包含保留字 '{word}'")

    vague_names = ["helper", "utils", "tools", "misc", "common", "general"]
    for vague in vague_names:
        if name == vague or name.endswith(f"-{vague}") or name.startswith(f"{vague}-"):
            issues.append(f"⚠️  name 使用了模糊词汇 '{vague}'，建议使用更具体的名称")

    return issues


def check_description(description: str) -> list[str]:
    """
    检查 description 字段的质量问题。
    返回问题列表。
    """
    issues = []

    if not description:
        issues.append("❌ description 字段为空")
        return issues

    if len(description) > 1024:
        issues.append(f"❌ description 超过 1024 字符（当前 {len(description)} 字符）")

    # 检查第一人称/第二人称
    first_person_patterns = ["我可以", "我能", "I can", "I will", "I'll", "帮你", "帮助你"]
    for pattern in first_person_patterns:
        if pattern in description:
            issues.append(f"⚠️  description 包含非第三人称表述 '{pattern}'，应改为客观描述")

    second_person_patterns = ["你可以", "您可以", "You can", "you can use this"]
    for pattern in second_person_patterns:
        if pattern.lower() in description.lower():
            issues.append(f"⚠️  description 包含第二人称表述 '{pattern}'，应改为第三人称")

    # 检查是否包含 WHEN（触发条件）
    when_keywords = ["当", "Use when", "when", "使用时", "触发", "场景", "时使用"]
    has_when = any(kw.lower() in description.lower() for kw in when_keywords)
    if not has_when:
        issues.append("⚠️  description 可能缺少 WHEN（何时触发）的描述，建议加入触发场景")

    # 检查 XML 标签
    if re.search(r"<[^>]+>", description):
        issues.append("❌ description 包含 XML 标签，不允许使用")

    # 长度过短警告
    if len(description) < 20:
        issues.append(f"⚠️  description 过短（{len(description)} 字符），建议更详细地描述功能和触发场景")

    return issues


def check_windows_paths(content: str) -> list[str]:
    """
    检测内容中的 Windows 风格路径（反斜杠）。
    只检查看起来像文件路径的模式，跳过行尾的 bash 换行符 \。
    """
    issues = []
    # 匹配行内代码中包含反斜杠且后面跟着路径字符的模式
    # 排除纯换行续行（行尾单独的 \）
    backslash_patterns = re.findall(r'`[^`]*\\[a-zA-Z0-9_.][^`]*`', content)
    for pattern in backslash_patterns:
        # 进一步过滤：跳过看起来是 bash 转义而非文件路径的
        if re.search(r'\\[a-zA-Z0-9_.]', pattern):
            short = pattern[:80] + "..." if len(pattern) > 80 else pattern
            issues.append(f"⚠️  检测到可能的 Windows 路径（反斜杠）：{short}")
    return issues


def check_time_sensitive(content: str) -> list[str]:
    """
    检测时间敏感信息。
    """
    issues = []
    year_patterns = re.findall(r'\b(20\d\d)\s*年', content)
    month_patterns = re.findall(r'\b(20\d\d[-/]\d{1,2})', content)

    for year in year_patterns:
        issues.append(f"⚠️  检测到年份引用 '{year}年'，注意避免时间敏感信息")
    for date in month_patterns:
        issues.append(f"⚠️  检测到日期引用 '{date}'，注意避免时间敏感信息")

    return issues


def build_file_tree(skill_dir: Path, indent: str = "") -> str:
    """
    生成技能目录的文件树字符串。
    """
    lines = []
    try:
        items = sorted(skill_dir.iterdir(), key=lambda p: (p.is_file(), p.name))
        for i, item in enumerate(items):
            is_last = i == len(items) - 1
            connector = "└── " if is_last else "├── "
            lines.append(f"{indent}{connector}{item.name}")
            if item.is_dir():
                sub_indent = indent + ("    " if is_last else "│   ")
                lines.append(build_file_tree(item, sub_indent))
    except PermissionError:
        lines.append(f"{indent}[权限不足，无法读取]")

    return "\n".join(filter(None, lines))


def analyze_skill(skill_dir: str) -> None:
    """
    主分析函数：对给定 skill 目录进行结构分析并打印报告。
    """
    skill_path = Path(skill_dir)

    if not skill_path.exists():
        print(f"❌ 路径不存在：{skill_dir}")
        sys.exit(1)

    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        print(f"❌ 未找到 SKILL.md：{skill_md}")
        sys.exit(1)

    print("=" * 60)
    print(f"📁 Skill 目录：{skill_path.resolve()}")
    print("=" * 60)

    # 文件树
    print("\n📂 文件结构：")
    print(f"{skill_path.name}/")
    print(build_file_tree(skill_path))

    # 读取 SKILL.md
    content = skill_md.read_text(encoding="utf-8")
    line_count = len(content.splitlines())

    print(f"\n📏 SKILL.md 行数：{line_count}", end="")
    if line_count <= 300:
        print(" ✅ (良好)")
    elif line_count <= 500:
        print(" 🟡 (接近上限，建议考虑拆分)")
    elif line_count <= 700:
        print(" 🟠 (超出建议值，应拆分到 reference 文件)")
    else:
        print(" 🔴 (严重超出，必须拆分)")

    # Frontmatter 解析
    print("\n📋 Frontmatter 检查：")
    frontmatter = parse_frontmatter(content)

    if not frontmatter:
        print("  ❌ 未找到有效的 YAML frontmatter（文件应以 --- 开头）")
    else:
        name = frontmatter.get("name", "")
        description = frontmatter.get("description", "")

        print(f"  name: {repr(name)}")
        name_issues = check_name(name)
        for issue in name_issues:
            print(f"    {issue}")
        if not name_issues:
            print("    ✅ name 格式合规")

        desc_preview = description[:80] + "..." if len(description) > 80 else description
        print(f"  description ({len(description)} 字符): {repr(desc_preview)}")
        desc_issues = check_description(description)
        for issue in desc_issues:
            print(f"    {issue}")
        if not desc_issues:
            print("    ✅ description 基本合规")

    # 反模式检测
    print("\n🔍 反模式检测：")

    path_issues = check_windows_paths(content)
    time_issues = check_time_sensitive(content)
    all_issues = path_issues + time_issues

    # 检查引用嵌套（简单检测：reference 文件中是否引用其他 .md 文件）
    ref_dir = skill_path / "references"
    if ref_dir.exists():
        for ref_file in ref_dir.glob("*.md"):
            ref_content = ref_file.read_text(encoding="utf-8", errors="ignore")
            nested_refs = re.findall(r'\[.*?\]\(((?!http)[^)]+\.md)\)', ref_content)
            for ref in nested_refs:
                all_issues.append(
                    f"⚠️  {ref_file.name} 中存在嵌套引用 '{ref}'，建议保持引用一级深"
                )

    if all_issues:
        for issue in all_issues:
            print(f"  {issue}")
    else:
        print("  ✅ 未发现明显反模式")

    # reference 文件统计
    print("\n📚 关联文件统计：")
    for md_file in skill_path.rglob("*.md"):
        if md_file.name != "SKILL.md":
            lines = count_lines(md_file)
            rel_path = str(md_file.relative_to(skill_path)).replace("\\", "/")
            note = ""
            if lines > 300:
                note = " ⚠️  建议在文件顶部添加目录"
            print(f"  {rel_path}：{lines} 行{note}")

    for py_file in skill_path.rglob("*.py"):
        lines = count_lines(py_file)
        rel_path = str(py_file.relative_to(skill_path)).replace("\\", "/")
        print(f"  {rel_path}：{lines} 行")

    print("\n" + "=" * 60)
    print("✅ 自动分析完成。请结合 references/checklist.md 进行完整评估。")
    print("=" * 60)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法：python scripts/audit_skill.py <skill目录路径>")
        print("示例：python scripts/audit_skill.py ~/.cursor/skills/my-skill/")
        sys.exit(1)

    analyze_skill(sys.argv[1])
