#!/usr/bin/env python3
"""
Skill Review - Agent Skills 审查工具

用于审查 Agent Skills 的规范性、完整性和代码质量。
"""

import argparse
import json
import os
import re
import sys
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple


@dataclass
class Issue:
    """审查发现的问题"""
    level: str  # 'error', 'warn', 'info'
    message: str
    file: Optional[str] = None
    line: Optional[int] = None
    category: str = ""

    def to_dict(self) -> dict:
        result = {
            "level": self.level,
            "message": self.message,
            "category": self.category
        }
        if self.file:
            result["file"] = self.file
        if self.line:
            result["line"] = self.line
        return result


@dataclass
class CategoryResult:
    """单个类别的审查结果"""
    name: str
    score: int
    max_score: int
    issues: List[Issue] = field(default_factory=list)

    @property
    def status(self) -> str:
        if any(i.level == "error" for i in self.issues):
            return "failed"
        elif any(i.level == "warn" for i in self.issues):
            return "warning"
        return "passed"

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "score": self.score,
            "max_score": self.max_score,
            "status": self.status,
            "issues": [i.to_dict() for i in self.issues]
        }


@dataclass
class ReviewResult:
    """完整的审查结果"""
    skill_name: str
    skill_path: str
    overall_score: int
    max_score: int = 100
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    categories: List[CategoryResult] = field(default_factory=list)

    @property
    def status(self) -> str:
        if self.overall_score < 75:
            return "failed"
        elif any(c.status == "warning" for c in self.categories):
            return "warning"
        return "passed"

    def to_dict(self) -> dict:
        return {
            "skill_name": self.skill_name,
            "skill_path": self.skill_path,
            "overall_score": self.overall_score,
            "max_score": self.max_score,
            "status": self.status,
            "timestamp": self.timestamp,
            "categories": {c.name: c.to_dict() for c in self.categories}
        }

    def to_markdown(self) -> str:
        lines = [
            f"# Skill 审查报告: {self.skill_name}",
            "",
            "## 概要",
            f"- 总分: {self.overall_score}/{self.max_score}",
            f"- 状态: {'✅ 通过' if self.status == 'passed' else '⚠️ 警告' if self.status == 'warning' else '❌ 未通过'}",
            f"- 审查时间: {self.timestamp}",
            "",
            "## 详细结果",
            ""
        ]

        for cat in self.categories:
            status_icon = "✅" if cat.status == "passed" else "⚠️" if cat.status == "warning" else "❌"
            lines.extend([
                f"### {cat.name}",
                f"- 状态: {status_icon} {cat.status.upper()}",
                f"- 得分: {cat.score}/{cat.max_score}",
            ])
            
            if cat.issues:
                lines.append("- 问题:")
                for issue in cat.issues:
                    location = ""
                    if issue.file:
                        location = f" ({issue.file}"
                        if issue.line:
                            location += f":{issue.line}"
                        location += ")"
                    lines.append(f"  - [{issue.level.upper()}] {issue.message}{location}")
            else:
                lines.append("- 问题: 无")
            
            lines.append("")

        return "\n".join(lines)


class SkillReviewer:
    """Skill 审查器"""

    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.skill_path: Optional[Path] = None
        self.skill_name: Optional[str] = None
        self.frontmatter: Dict = {}

    def review(self, skill_path: str) -> ReviewResult:
        """执行完整的 skill 审查"""
        self.skill_path = Path(skill_path).resolve()
        
        if not self.skill_path.exists():
            raise FileNotFoundError(f"Skill 路径不存在: {skill_path}")

        # 首先解析 SKILL.md 获取基本信息
        self._parse_skill_md()
        self.skill_name = self.frontmatter.get("name", self.skill_path.name)

        categories = []
        total_score = 0

        # 审查各个类别
        cat_result = self._review_skill_md()
        categories.append(cat_result)
        total_score += cat_result.score

        cat_result = self._review_directory_structure()
        categories.append(cat_result)
        total_score += cat_result.score

        cat_result = self._review_scripts()
        categories.append(cat_result)
        total_score += cat_result.score

        cat_result = self._review_file_references()
        categories.append(cat_result)
        total_score += cat_result.score

        return ReviewResult(
            skill_name=self.skill_name,
            skill_path=str(self.skill_path),
            overall_score=total_score,
            categories=categories
        )

    def _parse_skill_md(self) -> None:
        """解析 SKILL.md 文件"""
        skill_md_path = self.skill_path / "SKILL.md"
        
        if not skill_md_path.exists():
            self.frontmatter = {}
            return

        content = skill_md_path.read_text(encoding="utf-8")
        
        # 解析 YAML frontmatter
        if content.startswith("---"):
            parts = content.split("---", 2)
            if len(parts) >= 3:
                try:
                    import yaml
                    self.frontmatter = yaml.safe_load(parts[1]) or {}
                except ImportError:
                    # 简单解析
                    self._simple_parse_frontmatter(parts[1])

    def _simple_parse_frontmatter(self, yaml_content: str) -> None:
        """简单解析 YAML frontmatter（无 yaml 库时）"""
        self.frontmatter = {}
        current_key = None
        
        for line in yaml_content.strip().split("\n"):
            line = line.rstrip()
            if not line or line.startswith("#"):
                continue
            
            # 检查是否是键值对
            if ":" in line and not line.startswith(" "):
                key, value = line.split(":", 1)
                key = key.strip()
                value = value.strip()
                
                if value:
                    self.frontmatter[key] = value
                else:
                    self.frontmatter[key] = {}
                    current_key = key
            elif line.startswith("  ") and current_key:
                # 嵌套键值对
                sub_line = line.strip()
                if ":" in sub_line:
                    sub_key, sub_value = sub_line.split(":", 1)
                    if isinstance(self.frontmatter[current_key], dict):
                        self.frontmatter[current_key][sub_key.strip()] = sub_value.strip()

    def _review_skill_md(self) -> CategoryResult:
        """审查 SKILL.md 格式"""
        issues = []
        score = 25
        max_score = 25

        skill_md_path = self.skill_path / "SKILL.md"
        
        # 检查文件是否存在
        if not skill_md_path.exists():
            issues.append(Issue(
                level="error",
                message="SKILL.md 文件不存在",
                category="SKILL.md 格式"
            ))
            return CategoryResult("SKILL.md 格式", 0, max_score, issues)

        content = skill_md_path.read_text(encoding="utf-8")

        # 检查 frontmatter
        if not content.startswith("---"):
            issues.append(Issue(
                level="error",
                message="缺少 YAML frontmatter",
                file="SKILL.md",
                category="SKILL.md 格式"
            ))
            score -= 10
        else:
            # 检查必需的 name 字段
            if "name:" not in content:
                issues.append(Issue(
                    level="error",
                    message="缺少必需的 'name' 字段",
                    file="SKILL.md",
                    category="SKILL.md 格式"
                ))
                score -= 5
            else:
                name = self.frontmatter.get("name", "")
                # 验证 name 格式
                if not self._validate_name(name):
                    issues.append(Issue(
                        level="error",
                        message=f"'name' 字段格式无效: '{name}'",
                        file="SKILL.md",
                        category="SKILL.md 格式"
                    ))
                    score -= 3

            # 检查必需的 description 字段
            if "description:" not in content:
                issues.append(Issue(
                    level="error",
                    message="缺少必需的 'description' 字段",
                    file="SKILL.md",
                    category="SKILL.md 格式"
                ))
                score -= 5
            else:
                desc = self.frontmatter.get("description", "")
                if len(desc) > 1024:
                    issues.append(Issue(
                        level="warn",
                        message=f"'description' 过长 ({len(desc)} 字符, 建议不超过 1024)",
                        file="SKILL.md",
                        category="SKILL.md 格式"
                    ))
                    score -= 2
                elif len(desc) < 10:
                    issues.append(Issue(
                        level="warn",
                        message=f"'description' 过短 ({len(desc)} 字符, 建议至少 10)",
                        file="SKILL.md",
                        category="SKILL.md 格式"
                    ))
                    score -= 1

        return CategoryResult("SKILL.md 格式", max(0, score), max_score, issues)

    def _validate_name(self, name: str) -> bool:
        """验证 name 字段格式"""
        if not name:
            return False
        # 1-64 字符
        if len(name) < 1 or len(name) > 64:
            return False
        # 只能包含小写字母、数字和连字符
        if not re.match(r'^[a-z0-9-]+$', name):
            return False
        # 不能以连字符开头或结尾
        if name.startswith('-') or name.endswith('-'):
            return False
        # 不能有连续连字符
        if '--' in name:
            return False
        return True

    def _is_likely_code_example(self, text: str) -> bool:
        """判断文本是否可能是代码示例"""
        # 如果是多行，可能是代码
        if '\n' in text:
            return True
        # 如果包含常见的代码关键字
        code_keywords = [
            'def ', 'class ', 'import ', 'from ', 'return ',
            'function', 'const ', 'let ', 'var ',
            'if ', 'for ', 'while ', 'echo ', 'print',
            '{', '}', '=>', '===', '!==', '&&', '||'
        ]
        if any(kw in text for kw in code_keywords):
            return True
        # 如果包含 json 结构
        if text.strip().startswith('{') and text.strip().endswith('}'):
            return True
        # 如果包含 bash 命令行
        if text.strip().startswith('# ') or text.strip().startswith('bash '):
            return True
        return False

    def _review_directory_structure(self) -> CategoryResult:
        """审查目录结构"""
        issues = []
        score = 20
        max_score = 20

        # 检查目录名与 name 字段是否匹配
        name = self.frontmatter.get("name", "")
        dir_name = self.skill_path.name
        
        if name and name != dir_name:
            issues.append(Issue(
                level="error",
                message=f"目录名 '{dir_name}' 与 name 字段 '{name}' 不匹配",
                category="目录结构"
            ))
            score -= 5

        # 检查建议的目录结构
        scripts_dir = self.skill_path / "scripts"
        references_dir = self.skill_path / "references"
        assets_dir = self.skill_path / "assets"

        # 检查是否有深层嵌套
        for root, dirs, files in os.walk(self.skill_path):
            rel_path = Path(root).relative_to(self.skill_path)
            depth = len(rel_path.parts) - 1
            
            if depth > 2:
                issues.append(Issue(
                    level="warn",
                    message=f"目录嵌套过深 ({depth} 层): {rel_path}",
                    category="目录结构"
                ))
                score -= 1
                break

        # 检查是否有不必要的文件
        unnecessary_patterns = ['.DS_Store', 'Thumbs.db', '*.tmp', '*.log']
        for pattern in unnecessary_patterns:
            matches = list(self.skill_path.rglob(pattern))
            if matches:
                issues.append(Issue(
                    level="info",
                    message=f"发现临时/系统文件: {pattern}",
                    category="目录结构"
                ))

        return CategoryResult("目录结构", max(0, score), max_score, issues)

    def _review_scripts(self) -> CategoryResult:
        """审查脚本代码"""
        issues = []
        score = 35
        max_score = 35

        scripts_dir = self.skill_path / "scripts"
        
        if not scripts_dir.exists():
            # 没有 scripts 目录，不扣分
            return CategoryResult("脚本代码", max_score, max_score, issues)

        script_files = list(scripts_dir.glob("*"))
        
        if not script_files:
            return CategoryResult("脚本代码", max_score, max_score, issues)

        for script_file in script_files:
            if script_file.is_dir():
                continue

            content = script_file.read_text(encoding="utf-8", errors="ignore")
            rel_path = f"scripts/{script_file.name}"

            # 检查 shebang
            if script_file.suffix in ['.sh', '.py']:
                if not content.startswith('#!'):
                    issues.append(Issue(
                        level="warn",
                        message="脚本缺少 shebang",
                        file=rel_path,
                        category="脚本代码"
                    ))
                    score -= 1

            # 检查硬编码的敏感信息
            sensitive_patterns = [
                (r'password\s*=\s*["\'][^"\']+["\']', "可能的硬编码密码"),
                (r'api[_-]?key\s*=\s*["\'][^"\']+["\']', "可能的硬编码 API Key"),
                (r'secret\s*=\s*["\'][^"\']+["\']', "可能的硬编码密钥"),
                (r'token\s*=\s*["\'][^"\']+["\']', "可能的硬编码 Token"),
            ]

            for pattern, msg in sensitive_patterns:
                if re.search(pattern, content, re.IGNORECASE):
                    issues.append(Issue(
                        level="error",
                        message=f"发现 {msg}",
                        file=rel_path,
                        category="脚本代码"
                    ))
                    score -= 5

            # 检查错误处理（bash 脚本）
            if script_file.suffix == '.sh':
                if 'set -e' not in content and 'set -o errexit' not in content:
                    issues.append(Issue(
                        level="warn",
                        message="建议添加 'set -e' 进行错误处理",
                        file=rel_path,
                        category="脚本代码"
                    ))
                    score -= 1

            # 检查注释
            comment_patterns = ['#', '//', '/*', '"""', "'''"]
            has_comment = any(p in content for p in comment_patterns)
            if not has_comment:
                issues.append(Issue(
                    level="info",
                    message="建议添加注释说明脚本功能",
                    file=rel_path,
                    category="脚本代码"
                ))

        return CategoryResult("脚本代码", max(0, score), max_score, issues)

    def _review_file_references(self) -> CategoryResult:
        """审查文件引用"""
        issues = []
        score = 20
        max_score = 20

        skill_md_path = self.skill_path / "SKILL.md"
        
        if not skill_md_path.exists():
            return CategoryResult("文件引用", 0, max_score, issues)

        content = skill_md_path.read_text(encoding="utf-8")

        # 移除代码块内容，避免误解析
        # 匹配 ```...``` 和 `...` 代码块
        content_without_code_blocks = re.sub(
            r'```[\s\S]*?```|`[^`\n]+`',
            '',
            content
        )

        # 查找 Markdown 链接引用（排除代码块中的）
        md_link_pattern = r'\[([^\]]+)\]\(([^)]+)\)'
        md_links = re.findall(md_link_pattern, content_without_code_blocks)

        # 查找直接的路径引用（排除代码块中的）
        # 注意：这些模式捕获完整路径
        path_patterns = [
            (r'`(scripts/[^`]+)`', 'scripts/'),
            (r'`(references/[^`]+)`', 'references/'),
            (r'`(assets/[^`]+)`', 'assets/'),
        ]

        referenced_paths = set()

        for text, link in md_links:
            if not link.startswith(('http://', 'https://', '#', 'mailto:')):
                # 过滤掉明显的代码示例
                if not self._is_likely_code_example(link):
                    referenced_paths.add(link)

        for pattern, prefix in path_patterns:
            matches = re.findall(pattern, content_without_code_blocks)
            for match in matches:
                if isinstance(match, str) and not self._is_likely_code_example(match):
                    # 确保路径包含前缀
                    if not match.startswith(prefix):
                        match = prefix + match
                    referenced_paths.add(match)

        # 验证引用的文件是否存在
        for ref_path in referenced_paths:
            # 清理路径
            ref_path = ref_path.strip()
            
            # 跳过 URL 和锚点
            if ref_path.startswith(('http://', 'https://', '#', 'mailto:')):
                continue

            full_path = self.skill_path / ref_path
            
            if not full_path.exists():
                issues.append(Issue(
                    level="error",
                    message=f"引用的文件不存在: {ref_path}",
                    file="SKILL.md",
                    category="文件引用"
                ))
                score -= 5

        # 检查文件大小
        large_files = []
        for file_path in self.skill_path.rglob("*"):
            if file_path.is_file():
                size = file_path.stat().st_size
                if size > 1024 * 1024:  # 大于 1MB
                    large_files.append((file_path.relative_to(self.skill_path), size))

        for rel_path, size in large_files:
            issues.append(Issue(
                level="warn",
                message=f"文件过大: {rel_path} ({size / 1024 / 1024:.1f}MB)",
                category="文件引用"
            ))
            score -= 1

        return CategoryResult("文件引用", max(0, score), max_score, issues)


def main():
    parser = argparse.ArgumentParser(description="审查 Agent Skills")
    parser.add_argument("skill_path", help="要审查的 skill 目录路径")
    parser.add_argument("-v", "--verbose", action="store_true", help="详细输出")
    parser.add_argument("-j", "--json", action="store_true", help="输出 JSON 格式")

    args = parser.parse_args()

    reviewer = SkillReviewer(verbose=args.verbose)
    
    try:
        result = reviewer.review(args.skill_path)
        
        if args.json:
            print(json.dumps(result.to_dict(), indent=2, ensure_ascii=False))
        else:
            print(result.to_markdown())

        # 根据状态返回退出码
        if result.status == "failed":
            sys.exit(1)
        elif result.status == "warning":
            sys.exit(2)
        else:
            sys.exit(0)

    except FileNotFoundError as e:
        print(f"错误: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"审查失败: {e}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
