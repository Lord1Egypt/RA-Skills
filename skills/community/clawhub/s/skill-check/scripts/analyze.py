#!/usr/bin/env python3
"""
技能结构分析脚本 - 扫描技能目录并输出审查报告

用法:
    analyze.py <skill-directory>

示例:
    analyze.py .qoder/skills/my-skill
    analyze.py .  # 在技能目录内执行
"""

from __future__ import annotations

import os
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class Section:
    """章节结构"""
    title: str
    level: int
    start_line: int
    end_line: int
    line_count: int


@dataclass
class Issue:
    """问题项"""
    priority: str  # P0/P1/P2
    description: str
    suggestion: str


@dataclass
class AnalysisResult:
    """分析结果"""
    skill_name: str
    skill_md_lines: int = 0
    skill_md_sections: list[Section] = field(default_factory=list)
    scripts_count: int = 0
    refs_count: int = 0
    assets_count: int = 0
    frontmatter_valid: bool = True
    frontmatter_issues: list[str] = field(default_factory=list)
    misplaced_assets: list[str] = field(default_factory=list)
    misplaced_refs: list[str] = field(default_factory=list)
    agent_tool_refs: list[str] = field(default_factory=list)  # SKILL.md 中的工具名引用
    agent_path_refs: list[str] = field(default_factory=list)  # SKILL.md 中的路径耦合
    agent_cli_refs: list[str] = field(default_factory=list)  # 脚本中的 CLI 依赖
    vague_refs: list[str] = field(default_factory=list)  # 模糊指代（目录/脚本/工具）
    issues: list[Issue] = field(default_factory=list)


# 资源文件扩展名
ASSET_EXTENSIONS = {
    ".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp",  # 图片
    ".pdf", ".docx", ".xlsx", ".pptx",  # 文档
    ".json", ".yaml", ".yml", ".toml",  # 配置（非代码）
    ".html", ".css",  # 前端资源
    ".template", ".tmpl",  # 模板
}

# 脚本扩展名
SCRIPT_EXTENSIONS = {".py", ".sh", ".js", ".ts"}

# Agent 工具名称（检测绑定）
AGENT_TOOL_NAMES = {
    "qoder",
    "Qoder",
    "QODER",
    "claudecode",
    "ClaudeCode",
    "CLAUDECODE",
    "claude-code",
    "openclaw",
    "OpenClaw",
    "OPENCLAW",
    "cursor",
    "Cursor",
    "CURSOR",
    "windsurf",
    "Windsurf",
    "WINDSURF",
    "cline",
    "Cline",
    "CLINE",
    "aider",
    "Aider",
    "AIDER",
}

# Agent 工具目录名（检测路径耦合）
AGENT_DIR_NAMES = {
    ".qoder",
    ".claude",
    ".cursor",
    ".windsurf",
    ".cline",
    ".aider",
}

# Agent CLI 命令（检测脚本依赖）
AGENT_CLI_COMMANDS = {
    "qoder",
    "claude",
    "cursor",
    "windsurf",
    "cline",
    "aider",
}

# 模糊指代模式（检测执行确定性）
VAGUE_PATTERNS = {
    # 目录路径模糊
    "dir": [
        r"合适的目录",
        r"相关目录",
        r"对应目录",
        r"目标目录(?!\s*\w)",  # 避免匹配"目标目录下"
        r"适当的位置",
        r"合适的位置",
    ],
    # 脚本引用模糊
    "script": [
        r"运行脚本(?!\s*\w+\.py)",  # "运行脚本"后不跟具体脚本名
        r"执行脚本(?!\s*\w+\.py)",
        r"相关脚本",
        r"对应脚本",
        r"使用脚本(?!\s*\w+\.py)",
        r"调用脚本(?!\s*\w+\.py)",
    ],
    # 工具/指令模糊
    "tool": [
        r"使用工具(?!\s*[\w`])",  # "使用工具"后不跟具体工具名
        r"调用工具(?!\s*[\w`])",
        r"相关工具",
        r"适当的工具",
        r"合适的工具",
    ],
    # 程度副词模糊（易让 LLM 跑偏）
    "degree": [
        r"可能(?!\s*会\s*失败)",  # 单独使用的"可能"
        r"也许",
        r"适当",
        r"尽量",
        r"大约",
        r"左右(?!\s*\d)",  # 避免匹配"5个左右"
    ],
}


def analyze_sections(content: str) -> list[Section]:
    """分析 SKILL.md 章节结构"""
    lines = content.splitlines()
    
    # 先提取所有标题位置，跳过代码块内的内容
    headings: list[tuple[int, int, str]] = []  # (line_number, level, title)
    in_code_block = False
    
    for i, line in enumerate(lines, 1):
        # 检测代码块边界
        if line.strip().startswith("```"):
            in_code_block = not in_code_block
            continue
        
        # 跳过代码块内的内容
        if in_code_block:
            continue
        
        match = re.match(r'^(#{1,6})\s+(.+)$', line)
        if match:
            level = len(match.group(1))
            title = match.group(2).strip()
            headings.append((i, level, title))
    
    if not headings:
        return []
    
    # 计算每个章节的行数（到下一个同级或更高级标题前）
    total_lines = len(lines)
    sections = []
    
    for idx, (line_num, level, title) in enumerate(headings):
        # 找到下一个同级或更高级标题
        end_line = total_lines
        for next_line, next_level, _ in headings[idx + 1:]:
            if next_level <= level:
                end_line = next_line - 1
                break
        
        line_count = end_line - line_num + 1
        sections.append(Section(
            title=title,
            level=level,
            start_line=line_num,
            end_line=end_line,
            line_count=line_count
        ))
    
    return sections


def check_frontmatter(content: str, skill_name: str) -> tuple[bool, list[str]]:
    """检查 YAML frontmatter"""
    issues = []
    
    # 检查 frontmatter 存在
    if not content.startswith("---"):
        issues.append("缺少 YAML frontmatter")
        return False, issues
    
    # 提取 frontmatter
    fm_match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if not fm_match:
        issues.append("frontmatter 格式错误")
        return False, issues
    
    fm_content = fm_match.group(1)
    
    # 检查 name 字段
    name_match = re.search(r'^name:\s*["\']?([^"\'\n]+)["\']?', fm_content, re.MULTILINE)
    if not name_match:
        issues.append("缺少 name 字段")
    else:
        name_value = name_match.group(1).strip()
        if name_value != skill_name:
            issues.append(f"name('{name_value}') 与目录名('{skill_name}') 不一致")
    
    # 检查 description 字段
    desc_match = re.search(r'^description:', fm_content, re.MULTILINE)
    if not desc_match:
        issues.append("缺少 description 字段")
    
    return len(issues) == 0, issues


def scan_misplaced_files(skill_path: Path) -> tuple[list[str], list[str]]:
    """扫描错位的资源文件和参考文档"""
    misplaced_assets = []
    misplaced_refs = []
    
    refs_dir = skill_path / "references"
    assets_dir = skill_path / "assets"
    
    for file_path in skill_path.iterdir():
        if file_path.is_file() and file_path.name not in ("SKILL.md", "manifest.json"):
            suffix = file_path.suffix.lower()
            
            # 资源文件
            if suffix in ASSET_EXTENSIONS:
                if not assets_dir.exists():
                    misplaced_assets.append(file_path.name)
            # Markdown 参考文档
            elif suffix == ".md":
                if not refs_dir.exists():
                    misplaced_refs.append(file_path.name)
    
    return misplaced_assets, misplaced_refs


def check_agent_compatibility(skill_md_content: str, scripts_dir: Path | None) -> tuple[list[str], list[str], list[str]]:
    """检查 Agent 兼容性问题
    
    返回: (tool_refs, path_refs, cli_refs)
    - tool_refs: SKILL.md 中的工具名引用
    - path_refs: SKILL.md 中的路径耦合
    - cli_refs: 脚本中的 CLI 依赖
    """
    tool_refs = []
    path_refs = []
    cli_refs = []
    
    # 检查 SKILL.md 中的工具名引用（排除代码块）
    lines = skill_md_content.splitlines()
    in_code_block = False
    
    for line in lines:
        # 检测代码块边界
        if line.strip().startswith("```"):
            in_code_block = not in_code_block
            continue
        
        # 跳过代码块内的内容
        if in_code_block:
            continue
        
        # 检查工具名引用
        for tool_name in AGENT_TOOL_NAMES:
            if tool_name in line:
                # 构造问题描述
                if "description" in line.lower() or "适用于" in line or "仅" in line:
                    tool_refs.append(f"description 限定: {tool_name}")
                elif tool_name in line:
                    tool_refs.append(f"工具名硬编码: {tool_name}")
        
        
        # 检查路径耦合
        for dir_name in AGENT_DIR_NAMES:
            if dir_name in line:
                path_refs.append(f"路径耦合: {dir_name}")
    
    # 去重
    tool_refs = list(set(tool_refs))
    path_refs = list(set(path_refs))
    
    # 检查脚本中的 CLI 依赖
    if scripts_dir and scripts_dir.exists():
        for script in scripts_dir.rglob("*"):
            if script.is_file() and script.suffix in (".py", ".sh", ".js", ".ts"):
                try:
                    script_content = script.read_text(encoding="utf-8")
                    for cli_cmd in AGENT_CLI_COMMANDS:
                        # 检查 CLI 命令调用
                        patterns = [
                            f"subprocess.run([{cli_cmd}]",
                            f"subprocess.call([{cli_cmd}]",
                            f"os.system(\"{cli_cmd}",
                            f"os.system('{cli_cmd}",
                            f"`{cli_cmd} ",  # shell 反引号
                            f"$({cli_cmd} ",  # shell $()
                        ]
                        for pattern in patterns:
                            if pattern in script_content:
                                cli_refs.append(f"{script.name}: {cli_cmd}")
                                break
                except Exception:
                    pass
    
    cli_refs = list(set(cli_refs))
    
    return tool_refs, path_refs, cli_refs


def check_vague_references(skill_md_content: str) -> list[str]:
    """检查提示词模糊问题（执行缺少确定性）
    
    检测：
    - 目录路径模糊：如「合适的目录」「相关目录」
    - 脚本引用模糊：如「运行脚本」但不指明具体脚本
    - 工具指令模糊：如「使用工具」但不明确哪个工具
    - 程度副词模糊：如「可能」「适当」「尽量」等容易让 LLM 跑偏的表述
    
    返回: 模糊指代列表
    """
    vague_refs = []
    lines = skill_md_content.splitlines()
    in_code_block = False
    in_table = False  # 标记是否在表格中
    
    for line_num, line in enumerate(lines, 1):
        stripped = line.strip()
        
        # 检测代码块边界
        if stripped.startswith("```"):
            in_code_block = not in_code_block
            continue
        
        # 跳过代码块内的内容
        if in_code_block:
            continue
        
        # 跳过 frontmatter
        if line_num <= 5 and stripped in ("---", ""):
            continue
        
        # 检测表格（以 | 开头和结尾的行）
        if stripped.startswith("|") and stripped.endswith("|"):
            in_table = True
            # 表格中的模糊词通常是示例说明，跳过
            continue
        else:
            # 非表格行重置标记
            if not stripped.startswith("|"):
                in_table = False
        
        # 跳过表格行
        if in_table:
            continue
        
        # 检查各类模糊模式
        for category, patterns in VAGUE_PATTERNS.items():
            for pattern in patterns:
                if re.search(pattern, line):
                    # 提取上下文（前后各 10 字符）
                    match = re.search(pattern, line)
                    if match:
                        start = max(0, match.start() - 10)
                        end = min(len(line), match.end() + 10)
                        context = line[start:end].strip()
                        vague_refs.append(f"L{line_num}: [{category}] ...{context}...")
                    break  # 同一行同一类别只报告一次
    
    return vague_refs


def analyze_skill(skill_path: Path) -> AnalysisResult:
    """分析技能目录"""
    result = AnalysisResult(skill_name=skill_path.name)
    skill_md_path = skill_path / "SKILL.md"
    
    if not skill_md_path.exists():
        result.issues.append(Issue("P0", "SKILL.md 不存在", "创建 SKILL.md 文件"))
        return result
    
    content = skill_md_path.read_text(encoding="utf-8")
    lines = content.splitlines()
    result.skill_md_lines = len(lines)
    
    # 分析章节结构
    result.skill_md_sections = analyze_sections(content)
    
    # 检查 frontmatter
    result.frontmatter_valid, result.frontmatter_issues = check_frontmatter(
        content, result.skill_name
    )
    
    # 检查目录
    scripts_dir = skill_path / "scripts"
    refs_dir = skill_path / "references"
    assets_dir = skill_path / "assets"
    
    if scripts_dir.exists():
        result.scripts_count = sum(1 for _ in scripts_dir.rglob("*") if _.is_file())
    
    if refs_dir.exists():
        result.refs_count = sum(1 for _ in refs_dir.rglob("*") if _.is_file())
    
    if assets_dir.exists():
        result.assets_count = sum(1 for _ in assets_dir.rglob("*") if _.is_file())
    
    # 扫描错位文件
    result.misplaced_assets, result.misplaced_refs = scan_misplaced_files(skill_path)
    
    # 检查 Agent 兼容性
    result.agent_tool_refs, result.agent_path_refs, result.agent_cli_refs = check_agent_compatibility(
        content, scripts_dir
    )
    
    # 检查提示词模糊（执行确定性）
    result.vague_refs = check_vague_references(content)
    
    # 生成问题清单
    generate_issues(result)
    
    return result


def generate_issues(result: AnalysisResult) -> None:
    """根据分析结果生成问题清单"""
    # P0: 致命问题
    if not result.frontmatter_valid:
        for issue in result.frontmatter_issues:
            result.issues.append(Issue("P0", issue, "修正 frontmatter"))
    
    # P1: 重要问题
    if result.skill_md_lines > 500:
        result.issues.append(Issue(
            "P1",
            f"SKILL.md 过长（{result.skill_md_lines} 行）",
            "拆分到 references/ 目录"
        ))
    
    # 检查过长章节（超过 100 行）
    for sec in result.skill_md_sections:
        if sec.line_count > 100:
            result.issues.append(Issue(
                "P1",
                f"章节「{sec.title}」过长（{sec.line_count} 行）",
                "考虑拆分到 references/ 目录"
            ))
    
    if result.scripts_count == 0:
        result.issues.append(Issue(
            "P1",
            "缺少 scripts/ 目录",
            "将确定性操作脚本化"
        ))
    
    # P2: 建议优化
    if result.refs_count == 0:
        result.issues.append(Issue(
            "P2",
            "缺少 references/ 目录",
            "将参考文档独立存放"
        ))
    
    if result.misplaced_assets:
        result.issues.append(Issue(
            "P2",
            f"资源文件错位: {', '.join(result.misplaced_assets)}",
            "移动到 assets/ 目录"
        ))
    
    if result.misplaced_refs:
        result.issues.append(Issue(
            "P2",
            f"参考文档错位: {', '.join(result.misplaced_refs)}",
            "移动到 references/ 目录"
        ))
    
    # Agent 兼容性问题（P1）
    if result.agent_tool_refs:
        result.issues.append(Issue(
            "P1",
            f"绑定特定 Agent 工具: {', '.join(result.agent_tool_refs[:3])}{'...' if len(result.agent_tool_refs) > 3 else ''}",
            "移除工具名硬编码，使用通用表述"
        ))
    
    if result.agent_path_refs:
        result.issues.append(Issue(
            "P1",
            f"路径耦合特定工具: {', '.join(result.agent_path_refs[:3])}{'...' if len(result.agent_path_refs) > 3 else ''}",
            "使用相对路径或参数化配置"
        ))
    
    if result.agent_cli_refs:
        result.issues.append(Issue(
            "P1",
            f"脚本依赖特定 CLI: {', '.join(result.agent_cli_refs[:3])}{'...' if len(result.agent_cli_refs) > 3 else ''}",
            "使用通用命令或参数化"
        ))
    
    # 提示词模糊问题（P1）
    if result.vague_refs:
        # 按类别统计
        category_counts = {}
        for ref in result.vague_refs:
            # 提取类别标签 [dir]/[script]/[tool]/[degree]
            match = re.search(r'\[(\w+)\]', ref)
            if match:
                cat = match.group(1)
                category_counts[cat] = category_counts.get(cat, 0) + 1
        
        # 构造问题描述
        category_names = {
            "dir": "目录路径模糊",
            "script": "脚本引用模糊",
            "tool": "工具指令模糊",
            "degree": "程度副词模糊",
        }
        issues_desc = []
        for cat, count in category_counts.items():
            name = category_names.get(cat, cat)
            issues_desc.append(f"{name}: {count} 处")
        
        result.issues.append(Issue(
            "P1",
            f"提示词模糊，执行缺少确定性: {'; '.join(issues_desc)}",
            "替换模糊指代为具体路径、脚本名、工具名，删除程度副词"
        ))


def print_report(result: AnalysisResult) -> None:
    """输出审查报告"""
    print()
    print(f"# 技能审查报告：{result.skill_name}")
    print()
    
    # 结构概览
    print("## 结构概览")
    print()
    print("| 目录/文件 | 状态 | 说明 |")
    print("|-----------|------|------|")
    
    # SKILL.md
    if result.skill_md_lines == 0:
        print("| SKILL.md | ❌ | 不存在 |")
    elif result.skill_md_lines > 500:
        print(f"| SKILL.md | ⚠️ | {result.skill_md_lines} 行（超过 500 行） |")
    elif result.skill_md_lines > 300:
        print(f"| SKILL.md | ⚠️ | {result.skill_md_lines} 行（接近上限） |")
    else:
        print(f"| SKILL.md | ✅ | {result.skill_md_lines} 行 |")
    
    # scripts/
    if result.scripts_count == 0:
        print("| scripts/ | ❌ | 不存在 |")
    else:
        print(f"| scripts/ | ✅ | {result.scripts_count} 个文件 |")
    
    # references/
    if result.refs_count == 0:
        print("| references/ | ❌ | 不存在 |")
    else:
        print(f"| references/ | ✅ | {result.refs_count} 个文件 |")
    
    # assets/
    if result.assets_count == 0:
        print("| assets/ | ➖ | 不存在（如无资源文件可忽略） |")
    else:
        print(f"| assets/ | ✅ | {result.assets_count} 个文件 |")
    
    print()
    
    # 章节结构
    if result.skill_md_sections:
        print("## 章节结构")
        print()
        print("| 章节 | 行数 | 状态 |")
        print("|------|------|------|")
        for sec in result.skill_md_sections:
            status = "⚠️" if sec.line_count > 100 else "✅"
            print(f"| {sec.title} | {sec.line_count} | {status} |")
        print()
    
    # 详细检查
    print("## 详细检查")
    print()
    print("| 检查项 | 状态 | 说明 |")
    print("|--------|------|------|")
    
    fm_status = "✅" if result.frontmatter_valid else "❌"
    fm_note = "规范" if result.frontmatter_valid else "; ".join(result.frontmatter_issues)
    print(f"| frontmatter | {fm_status} | {fm_note} |")
    
    if result.misplaced_assets:
        print(f"| 资源位置 | ⚠️ | {', '.join(result.misplaced_assets)} 应移至 assets/ |")
    elif result.assets_count > 0:
        print("| 资源位置 | ✅ | 资源文件已归位 |")
    
    if result.misplaced_refs:
        print(f"| 参考文档 | ⚠️ | {', '.join(result.misplaced_refs)} 应移至 references/ |")
    elif result.refs_count > 0:
        print("| 参考文档 | ✅ | 参考文档已归位 |")
    
    # Agent 兼容性检查
    has_agent_issues = result.agent_tool_refs or result.agent_path_refs or result.agent_cli_refs
    if has_agent_issues:
        issues = []
        if result.agent_tool_refs:
            issues.append(f"工具绑定: {len(result.agent_tool_refs)} 处")
        if result.agent_path_refs:
            issues.append(f"路径耦合: {len(result.agent_path_refs)} 处")
        if result.agent_cli_refs:
            issues.append(f"CLI依赖: {len(result.agent_cli_refs)} 处")
        print(f"| Agent 兼容性 | ⚠️ | {'; '.join(issues)} |")
    else:
        print("| Agent 兼容性 | ✅ | 无特定工具绑定 |")
    
    # 执行确定性检查
    if result.vague_refs:
        print(f"| 执行确定性 | ⚠️ | {len(result.vague_refs)} 处模糊指代 |")
    else:
        print("| 执行确定性 | ✅ | 路径/脚本/工具引用明确 |")
    
    print()
    
    # 问题清单
    print("## 问题清单")
    print()
    
    if not result.issues:
        print("✅ 未发现结构性问题")
    else:
        print("| 优先级 | 问题 | 建议 |")
        print("|--------|------|------|")
        for issue in result.issues:
            print(f"| {issue.priority} | {issue.description} | {issue.suggestion} |")
    
    print()
    print("---")
    print("💡 提示: 详细优化模式请参考 references/structure-patterns.md")


def main():
    if len(sys.argv) < 2:
        print("用法: analyze.py <skill-directory>")
        print("")
        print("示例:")
        print("  analyze.py .qoder/skills/my-skill")
        print("  analyze.py .  # 在技能目录内执行")
        sys.exit(1)
    
    skill_path = Path(sys.argv[1]).resolve()
    
    if not skill_path.exists():
        print(f"❌ 错误: 目录不存在: {skill_path}")
        sys.exit(1)
    
    result = analyze_skill(skill_path)
    print_report(result)


if __name__ == "__main__":
    main()
