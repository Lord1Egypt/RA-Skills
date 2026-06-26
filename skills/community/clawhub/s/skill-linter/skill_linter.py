#!/usr/bin/env python3
"""
Skill Linter - 检查 SKILL.md 文件的最佳实践
"""

import sys
import re
import yaml
from pathlib import Path
from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Issue:
    severity: str  # critical, warning, info
    category: str
    message: str
    suggestion: str


@dataclass
class AnalysisResult:
    filepath: str
    frontmatter: dict = field(default_factory=dict)
    content: str = ""
    issues: List[Issue] = field(default_factory=list)
    word_count: int = 0

    @property
    def critical_count(self):
        return sum(1 for i in self.issues if i.severity == "critical")

    @property
    def warning_count(self):
        return sum(1 for i in self.issues if i.severity == "warning")

    @property
    def info_count(self):
        return sum(1 for i in self.issues if i.severity == "info")


def parse_skill_md(filepath: str) -> AnalysisResult:
    """解析 SKILL.md 文件"""
    result = AnalysisResult(filepath=filepath)

    try:
        content = Path(filepath).read_text(encoding='utf-8')
    except Exception as e:
        result.issues.append(Issue(
            severity="critical",
            category="file",
            message=f"无法读取文件: {e}",
            suggestion="检查文件路径和权限"
        ))
        return result

    result.content = content
    result.word_count = len(content.split())

    # 解析 frontmatter
    frontmatter_match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
    if frontmatter_match:
        try:
            result.frontmatter = yaml.safe_load(frontmatter_match.group(1)) or {}
        except yaml.YAMLError as e:
            result.issues.append(Issue(
                severity="critical",
                category="frontmatter",
                message=f"YAML 解析错误: {e}",
                suggestion="检查 YAML 语法，确保没有制表符或格式错误"
            ))
    else:
        result.issues.append(Issue(
            severity="critical",
            category="frontmatter",
            message="缺少 YAML frontmatter (--- 分隔符)",
            suggestion="在文件开头添加 ---\n[你的配置]\n---"
        ))

    return result


def analyze_frontmatter(result: AnalysisResult):
    """分析 frontmatter"""
    fm = result.frontmatter

    # 检查 name
    if 'name' not in fm:
        result.issues.append(Issue(
            severity="warning",
            category="frontmatter",
            message="缺少 'name' 字段",
            suggestion="添加 name 字段来明确 Skill 名称，如: name: my-skill"
        ))
    elif not fm.get('name'):
        result.issues.append(Issue(
            severity="warning",
            category="frontmatter",
            message="'name' 字段为空",
            suggestion="提供一个有意义的 Skill 名称"
        ))

    # 检查 description
    if 'description' not in fm:
        result.issues.append(Issue(
            severity="critical",
            category="frontmatter",
            message="缺少 'description' 字段",
            suggestion="description 是必需的，它告诉 Claude 何时使用该 Skill。例如: 'Perform code review when asked to review changes'"
        ))
    else:
        desc = fm.get('description', '')
        if len(desc) < 20:
            result.issues.append(Issue(
                severity="warning",
                category="frontmatter",
                message="description 太短",
                suggestion="description 应该具体说明 Skill 的功能和触发时机，至少 20 个字符"
            ))
        elif len(desc) > 300:
            result.issues.append(Issue(
                severity="info",
                category="frontmatter",
                message="description 较长",
                suggestion="description 会被用于判断相关性，保持简洁明了"
            ))

        # 检查 description 质量
        vague_terms = ['etc', 'etc.', 'something', 'things', 'stuff']
        for term in vague_terms:
            if term in desc.lower():
                result.issues.append(Issue(
                    severity="warning",
                    category="frontmatter",
                    message=f"description 包含模糊词汇 '{term}'",
                    suggestion="使用具体的描述，避免模糊词汇"
                ))

    # 检查 allowed-tools
    if 'allowed-tools' not in fm:
        result.issues.append(Issue(
            severity="info",
            category="frontmatter",
            message="未指定 'allowed-tools'",
            suggestion="如果 Skill 需要特定工具，添加 allowed-tools 字段，如: allowed-tools: Read, Edit, Bash"
        ))

    # 检查 context 和 agent
    if fm.get('context') == 'fork' and 'agent' not in fm:
        result.issues.append(Issue(
            severity="warning",
            category="frontmatter",
            message="context: fork 但未指定 agent",
            suggestion="当使用 context: fork 时，应该指定 agent 类型，如: agent: Explore"
        ))


def analyze_content(result: AnalysisResult):
    """分析内容部分"""
    content = result.content

    # 提取 frontmatter 后的内容
    frontmatter_match = re.match(r'^---\s*\n.*?\n---\s*\n', content, re.DOTALL)
    if frontmatter_match:
        body = content[frontmatter_match.end():]
    else:
        body = content

    # 检查是否有标题
    if not re.search(r'^#+\s+', body, re.MULTILINE):
        result.issues.append(Issue(
            severity="warning",
            category="content",
            message="内容缺少标题/标题",
            suggestion="添加一个清晰的标题来说明 Skill 的目的"
        ))

    # 检查是否有步骤/流程
    has_steps = bool(re.search(r'(^|\n)\d+\.', body)) or \
                bool(re.search(r'(^|\n)[\*\-\+]\s', body)) or \
                bool(re.search(r'(?i)(step|process|workflow|procedure)', body))

    if not has_steps:
        result.issues.append(Issue(
            severity="warning",
            category="content",
            message="内容缺少明确的步骤或流程",
            suggestion="添加编号步骤或项目符号列表来指导 Claude 执行"
        ))

    # 检查是否有输出格式说明
    has_output_format = bool(re.search(r'(?i)(output format|output|format|structure|template)', body))
    if not has_output_format:
        result.issues.append(Issue(
            severity="info",
            category="content",
            message="未明确指定输出格式",
            suggestion="添加 '## Output Format' 部分来定义期望的输出结构"
        ))

    # 检查是否有示例
    has_examples = bool(re.search(r'```', body)) or \
                   bool(re.search(r'(?i)(example|for example|e\.g\.)', body))
    if not has_examples:
        result.issues.append(Issue(
            severity="info",
            category="content",
            message="内容缺少示例",
            suggestion="添加代码块或具体示例来帮助 Claude 理解期望的输出"
        ))

    # 检查长度
    word_count = len(body.split())
    if word_count < 50:
        result.issues.append(Issue(
            severity="warning",
            category="content",
            message=f"内容较短 ({word_count} 词)",
            suggestion="考虑添加更多细节和指导，使 Skill 更实用"
        ))
    elif word_count > 1500:
        result.issues.append(Issue(
            severity="info",
            category="content",
            message=f"内容较长 ({word_count} 词)",
            suggestion="长内容没问题，但确保结构清晰，便于 Claude 遵循"
        ))

    # 检查模糊词汇
    vague_patterns = [
        (r'\betc\.?\b', "使用 'etc' 可能过于模糊"),
        (r'\bsomething\b', "使用 'something' 不够具体"),
        (r'\bthings?\b', "使用 'things' 不够具体"),
        (r'\bstuff\b', "使用 'stuff' 不够专业"),
    ]
    for pattern, msg in vague_patterns:
        if re.search(pattern, body, re.IGNORECASE):
            result.issues.append(Issue(
                severity="info",
                category="content",
                message=msg,
                suggestion="使用具体的术语替代模糊词汇"
            ))


def calculate_score(result: AnalysisResult) -> int:
    """计算总分"""
    score = 10
    score -= result.critical_count * 3
    score -= result.warning_count * 1
    score -= result.info_count * 0.5
    return max(0, int(score))


def print_report(result: AnalysisResult):
    """打印分析报告"""
    print(f"\n{'='*60}")
    print(f"# Skill Analysis Report")
    print(f"{'='*60}")
    print(f"\n## 文件: {result.filepath}")

    # Frontmatter 部分
    print(f"\n## Frontmatter 分析")
    print(f"\n| 字段 | 值 |")
    print(f"|------|-----|")
    for key, value in result.frontmatter.items():
        display_value = str(value)[:50] + "..." if len(str(value)) > 50 else str(value)
        print(f"| {key} | {display_value} |")

    # 问题列表
    print(f"\n## 发现的问题")

    critical_issues = [i for i in result.issues if i.severity == "critical"]
    warning_issues = [i for i in result.issues if i.severity == "warning"]
    info_issues = [i for i in result.issues if i.severity == "info"]

    if critical_issues:
        print(f"\n### 🔴 严重问题 (必须修复)")
        for i, issue in enumerate(critical_issues, 1):
            print(f"{i}. **{issue.message}**")
            print(f"   → 建议: {issue.suggestion}")

    if warning_issues:
        print(f"\n### 🟡 警告 (建议修复)")
        for i, issue in enumerate(warning_issues, 1):
            print(f"{i}. **{issue.message}**")
            print(f"   → 建议: {issue.suggestion}")

    if info_issues:
        print(f"\n### 🟢 建议 (可选)")
        for i, issue in enumerate(info_issues, 1):
            print(f"{i}. **{issue.message}**")
            print(f"   → 建议: {issue.suggestion}")

    if not result.issues:
        print("\n✅ 没有发现任何问题！")

    # 评分
    score = calculate_score(result)
    print(f"\n## 总体评估")
    print(f"\n**评分:** {score}/10")

    if score >= 9:
        verdict = "✅ 优秀 - 可以直接使用"
    elif score >= 7:
        verdict = "🟡 良好 - 建议进行小幅改进"
    elif score >= 5:
        verdict = "⚠️ 需要改进 - 使用前请修复警告"
    else:
        verdict = "❌ 严重问题 - 必须修复后才能使用"

    print(f"**结论:** {verdict}")
    print(f"\n**统计:** {result.critical_count} 严重 | {result.warning_count} 警告 | {result.info_count} 建议")
    print(f"**字数:** {result.word_count} 词")


def main():
    if len(sys.argv) < 2:
        print("用法: python3 skill_linter.py <SKILL.md 路径>")
        print("示例: python3 skill_linter.py ~/.claude/skills/my-skill/SKILL.md")
        sys.exit(1)

    filepath = sys.argv[1]

    if not Path(filepath).exists():
        print(f"错误: 文件不存在: {filepath}")
        sys.exit(1)

    # 解析和分析
    result = parse_skill_md(filepath)

    if result.frontmatter:  # 只有成功解析才继续
        analyze_frontmatter(result)
        analyze_content(result)

    # 打印报告
    print_report(result)

    # 返回退出码
    sys.exit(0 if result.critical_count == 0 else 1)


if __name__ == "__main__":
    main()
