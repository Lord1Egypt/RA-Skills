#!/usr/bin/env python3
"""
Skill Router — Auto-generator / 技能路由器自动生成工具

Scans a skills directory, extracts name + description from each SKILL.md,
auto-categorizes them, and generates a complete skill-router SKILL.md.

扫描指定目录下的所有 skill，提取 frontmatter 中的 name 和 description，
自动分类后生成完整的 skill-router SKILL.md。

Usage / 用法:
    python scripts/generate.py                           # default path / 默认路径
    python scripts/generate.py --skills-dir ~/my-skills  # custom dir / 指定路径
    python scripts/generate.py --output custom.md        # custom output / 自定义输出
"""

import os
import re
import argparse
from pathlib import Path
from collections import defaultdict

# === Config / 配置 ===
DEFAULT_SKILLS_DIR = os.path.expanduser("~/.claude/skills")
DEFAULT_OUTPUT = "SKILL.md"

# === Auto-categorization Rules / 自动分类规则 ===
# Each category has a list of English keywords matched against skill name + description.
# 每个类别有一组英文关键词，与 skill 的 name + description 做匹配。
CATEGORY_RULES = {
    "Architecture / 规划与架构": ["architect", "plan", "design system", "blueprint", "adr", "hexagonal", "ports.adapter"],
    "Code Quality / 代码质量": ["code review", "coding standard", "clean code", "code tour", "onboarding", "codebase", "refactor"],
    "Git & Version Control": ["git", "github", "version control", "commit", "branch", "pull request", "release"],
    "API & Backend / API & 后端": ["api", "rest", "backend", "service", "middleware", "endpoint", "http"],
    "Database / 数据库": ["database", "sql", "migration", "schema", "orm", "query", "ddl"],
    "DevOps & Deploy": ["docker", "kubernetes", "deploy", "ci/cd", "pipeline", "container", "infrastructure"],
    "Testing / 测试": ["test", "e2e", "playwright", "unit test", "benchmark", "qa", "regression"],
    "Frontend / 前端": ["frontend", "react", "vue", "next", "ui", "css", "component", "design", "accessibility", "wcag"],
    "Mobile / 移动端": ["android", "ios", "flutter", "mobile", "swift", "kotlin"],
    "Language-specific / 语言专项": ["golang", "java", "python", "cpp", "c++", "c#", "dotnet", "django", "rust", "typescript", "javascript"],
    "AI / Agent": ["agent", "llm", "ai-first", "autonomous", "prompt", "rag", "retrieval", "eval"],
    "Content / 内容创作": ["writing", "blog", "article", "content", "voice", "brand", "copy", "crosspost", "documentation"],
    "Research / 研究": ["research", "scraper", "crawl", "data extraction", "investigation"],
    "Security / 安全": ["security", "hipaa", "compliance", "phi", "audit", "vulnerability"],
    "System Tools / 系统工具": ["context", "token", "budget", "optimization", "monitoring"],
}


def parse_skill(path: Path) -> dict | None:
    """Extract name and description from SKILL.md frontmatter / 从 SKILL.md 提取 name 和 description"""
    try:
        content = path.read_text(encoding="utf-8")
    except Exception:
        return None

    # Match YAML frontmatter / 匹配 YAML frontmatter
    fm_match = re.match(r"^---\s*\n(.*?)\n---", content, re.DOTALL)
    if not fm_match:
        return None

    fm = fm_match.group(1)
    name = re.search(r"^name:\s*['\"]?(.+?)['\"]?\s*$", fm, re.MULTILINE)
    desc = re.search(r"^description:\s*['\"]?(.+?)['\"]?\s*$", fm, re.MULTILINE)

    if not name:
        return None

    return {
        "name": name.group(1).strip().strip('"').strip("'"),
        "description": desc.group(1).strip().strip('"').strip("'") if desc else "",
        "path": str(path.parent),
    }


def categorize_skill(name: str, description: str) -> str:
    """Auto-categorize by name + description keywords / 根据名称和描述自动分类"""
    text = f"{name} {description}".lower()
    for category, keywords in CATEGORY_RULES.items():
        for kw in keywords:
            if kw in text:
                return category
    return "Other / 其他"


def scan_skills(skills_dir: str) -> dict[str, list[dict]]:
    """Scan directory, return skills grouped by category / 扫描目录，返回按类别分组的技能列表"""
    categories = defaultdict(list)
    skills_path = Path(skills_dir)

    if not skills_path.exists():
        print(f"[Error] Directory not found / 目录不存在: {skills_dir}")
        return categories

    for skill_dir in sorted(skills_path.iterdir()):
        if not skill_dir.is_dir():
            continue
        skill_file = skill_dir / "SKILL.md"
        if not skill_file.exists():
            continue

        skill = parse_skill(skill_file)
        if not skill:
            continue

        category = categorize_skill(skill["name"], skill["description"])
        categories[category].append(skill)

    return categories


def generate_index(categories: dict[str, list[dict]]) -> str:
    """Generate skill index table in Markdown / 生成技能索引 Markdown 表格"""
    lines = []

    # Preserve category order / 按自定义顺序排列类别
    category_order = list(CATEGORY_RULES.keys()) + ["Other / 其他"]

    for cat in category_order:
        if cat not in categories:
            continue
        skills = categories[cat]
        lines.append(f"### {cat}")
        lines.append("| Skill / 技能 | Trigger / 触发场景 |")
        lines.append("|--------|----------|")
        for s in sorted(skills, key=lambda x: x["name"]):
            # Use first sentence of description as trigger summary
            # 取 description 的第一句作为触发场景摘要
            desc = s["description"]
            trigger = desc.split(".")[0].strip()
            if len(trigger) > 80:
                trigger = trigger[:77] + "..."
            lines.append(f"| `{s['name']}` | {trigger} |")
        lines.append("")

    return "\n".join(lines)


def generate(skills_dir: str, output_path: str, template_path: str | None = None):
    """Main entry: generate complete skill-router SKILL.md / 主入口：生成完整的 skill-router SKILL.md"""

    # Scan skills / 扫描技能
    categories = scan_skills(skills_dir)
    total = sum(len(v) for v in categories.values())
    print(f"[Scan] Found {total} skills in {skills_dir} / 在 {skills_dir} 中发现 {total} 个技能")

    for cat, skills in categories.items():
        print(f"  {cat}: {len(skills)}")

    # Generate index / 生成索引
    index = generate_index(categories)

    # Read template / 读取模板
    if template_path:
        template = Path(template_path).read_text(encoding="utf-8")
    else:
        template = Path(__file__).parent.parent / "SKILL.md"
        template = template.read_text(encoding="utf-8")

    # Replace index section / 替换索引区域
    start = "<!-- SKILL_INDEX_START -->"
    end = "<!-- SKILL_INDEX_END -->"
    pattern = re.compile(f"{start}.*?{end}", re.DOTALL)
    timestamp = Path(output_path).parent.name
    replacement = f"{start}\n{index}\n<!-- Auto-generated from {timestamp} — {total} skills / 自动生成 — {total} 个技能 -->\n{end}"
    result = pattern.sub(replacement, template)

    # Write output / 写入输出
    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(result, encoding="utf-8")
    print(f"\n[Done] Generated: {out} ({total} skills) / 已生成: {out} ({total} 个技能)")


def main():
    parser = argparse.ArgumentParser(
        description="Generate Skill Router index / 生成 Skill Router 技能索引"
    )
    parser.add_argument(
        "--skills-dir",
        default=DEFAULT_SKILLS_DIR,
        help=f"Skills directory path (default: {DEFAULT_SKILLS_DIR}) / 技能目录路径 (默认: {DEFAULT_SKILLS_DIR})",
    )
    parser.add_argument(
        "--output",
        default=DEFAULT_OUTPUT,
        help=f"Output file path (default: {DEFAULT_OUTPUT}) / 输出文件路径 (默认: {DEFAULT_OUTPUT})",
    )
    parser.add_argument(
        "--template",
        default=None,
        help="Template SKILL.md path (default: repo root SKILL.md) / 模板文件路径",
    )
    args = parser.parse_args()

    generate(args.skills_dir, args.output, args.template)


if __name__ == "__main__":
    main()