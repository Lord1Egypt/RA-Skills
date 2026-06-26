"""
技能代码分析模块

负责分析 SKILL.md 文件、检查代码质量、生成改进建议
"""

import os
import re
import ast
import yaml
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass, field


@dataclass
class AnalysisIssue:
    """分析问题"""
    severity: str  # critical, warning, info
    category: str  # syntax, structure, content, performance
    message: str
    line: Optional[int] = None
    suggestion: Optional[str] = None


@dataclass
class SkillAnalysisResult:
    """技能分析结果"""
    skill_name: str
    skill_path: str
    exists: bool = False
    has_skill_md: bool = False
    has_package_json: bool = False
    skill_md_valid: bool = False
    issues: List[AnalysisIssue] = field(default_factory=list)
    suggestions: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    score: int = 0  # 0-100


class SkillAnalyzer:
    """技能分析器"""
    
    # SKILL.md 必需字段
    REQUIRED_SKILL_MD_FIELDS = [
        "name",
        "description",
    ]
    
    # package.json 必需字段
    REQUIRED_PACKAGE_FIELDS = [
        "name",
        "version",
    ]
    
    def __init__(self, skills_dir: Optional[str] = None):
        if skills_dir is None:
            # 默认使用 ~/.openclaw/skills
            self.skills_dir = Path.home() / ".openclaw" / "skills"
        else:
            self.skills_dir = Path(skills_dir)
    
    def analyze_skill(self, skill_name: str) -> SkillAnalysisResult:
        """
        分析单个技能
        
        Args:
            skill_name: 技能名称
        
        Returns:
            分析结果
        """
        skill_path = self.skills_dir / skill_name
        result = SkillAnalysisResult(
            skill_name=skill_name,
            skill_path=str(skill_path)
        )
        
        # 检查目录是否存在
        if not skill_path.exists():
            result.issues.append(AnalysisIssue(
                severity="critical",
                category="structure",
                message=f"技能目录不存在: {skill_path}"
            ))
            return result
        
        result.exists = True
        
        # 分析 SKILL.md
        self._analyze_skill_md(result, skill_path)
        
        # 分析 package.json
        self._analyze_package_json(result, skill_path)
        
        # 分析 Python 代码
        self._analyze_python_code(result, skill_path)
        
        # 分析目录结构
        self._analyze_structure(result, skill_path)
        
        # 计算综合评分
        result.score = self._calculate_score(result)
        
        # 生成改进建议
        result.suggestions = self._generate_suggestions(result)
        
        return result
    
    def analyze_all_skills(self) -> List[SkillAnalysisResult]:
        """分析所有技能"""
        results = []
        
        if not self.skills_dir.exists():
            return results
        
        for item in self.skills_dir.iterdir():
            if item.is_dir() and not item.name.startswith("."):
                result = self.analyze_skill(item.name)
                results.append(result)
        
        return results
    
    def _analyze_skill_md(self, result: SkillAnalysisResult, skill_path: Path):
        """分析 SKILL.md 文件"""
        skill_md_path = skill_path / "SKILL.md"
        
        if not skill_md_path.exists():
            result.issues.append(AnalysisIssue(
                severity="critical",
                category="structure",
                message="缺少 SKILL.md 文件",
                suggestion="创建 SKILL.md 文件，包含技能名称、描述、使用方法等信息"
            ))
            return
        
        result.has_skill_md = True
        
        try:
            content = skill_md_path.read_text(encoding="utf-8")
            
            # 检查 YAML frontmatter
            if content.startswith("---"):
                try:
                    # 提取 YAML frontmatter
                    parts = content.split("---", 2)
                    if len(parts) >= 3:
                        yaml_content = parts[1].strip()
                        metadata = yaml.safe_load(yaml_content)
                        
                        if metadata:
                            result.metadata = metadata
                            
                            # 检查必需字段
                            for field in self.REQUIRED_SKILL_MD_FIELDS:
                                if field not in metadata:
                                    result.issues.append(AnalysisIssue(
                                        severity="warning",
                                        category="content",
                                        message=f"SKILL.md 缺少字段: {field}"
                                    ))
                        else:
                            result.issues.append(AnalysisIssue(
                                severity="warning",
                                category="content",
                                message="SKILL.md YAML frontmatter 为空"
                            ))
                    
                    result.skill_md_valid = True
                    
                except yaml.YAMLError as e:
                    result.issues.append(AnalysisIssue(
                        severity="critical",
                        category="syntax",
                        message=f"SKILL.md YAML 解析错误: {e}"
                    ))
            else:
                result.issues.append(AnalysisIssue(
                    severity="warning",
                    category="structure",
                    message="SKILL.md 缺少 YAML frontmatter（建议以 --- 开头）",
                    suggestion="添加 YAML frontmatter 包含元数据信息"
                ))
            
            # 检查内容长度
            content_without_frontmatter = re.sub(r'^---.*?---', '', content, flags=re.DOTALL).strip()
            if len(content_without_frontmatter) < 100:
                result.issues.append(AnalysisIssue(
                    severity="warning",
                    category="content",
                    message="SKILL.md 内容过短",
                    suggestion="添加更详细的使用说明和示例"
                ))
            
            # 检查是否包含示例
            if "```" not in content:
                result.issues.append(AnalysisIssue(
                    severity="info",
                    category="content",
                    message="SKILL.md 缺少代码示例",
                    suggestion="添加使用示例代码块"
                ))
            
        except Exception as e:
            result.issues.append(AnalysisIssue(
                severity="critical",
                category="syntax",
                message=f"无法读取 SKILL.md: {e}"
            ))
    
    def _analyze_package_json(self, result: SkillAnalysisResult, skill_path: Path):
        """分析 package.json 文件"""
        package_path = skill_path / "package.json"
        
        if not package_path.exists():
            result.issues.append(AnalysisIssue(
                severity="warning",
                category="structure",
                message="缺少 package.json 文件",
                suggestion="创建 package.json 文件，包含技能元数据"
            ))
            return
        
        result.has_package_json = True
        
        try:
            import json
            with open(package_path, 'r', encoding='utf-8') as f:
                package = json.load(f)
            
            # 检查必需字段
            for field in self.REQUIRED_PACKAGE_FIELDS:
                if field not in package:
                    result.issues.append(AnalysisIssue(
                        severity="warning",
                        category="content",
                        message=f"package.json 缺少字段: {field}"
                    ))
            
            # 检查版本格式
            if "version" in package:
                version_pattern = r'^\d+\.\d+\.\d+'
                if not re.match(version_pattern, package["version"]):
                    result.issues.append(AnalysisIssue(
                        severity="warning",
                        category="content",
                        message=f"package.json 版本格式不正确: {package['version']}",
                        suggestion="使用语义化版本格式，如 1.0.0"
                    ))
            
        except json.JSONDecodeError as e:
            result.issues.append(AnalysisIssue(
                severity="critical",
                category="syntax",
                message=f"package.json JSON 解析错误: {e}"
            ))
        except Exception as e:
            result.issues.append(AnalysisIssue(
                severity="critical",
                category="syntax",
                message=f"无法读取 package.json: {e}"
            ))
    
    def _analyze_python_code(self, result: SkillAnalysisResult, skill_path: Path):
        """分析 Python 代码文件"""
        python_files = list(skill_path.rglob("*.py"))
        
        if not python_files:
            result.issues.append(AnalysisIssue(
                severity="info",
                category="structure",
                message="未找到 Python 代码文件"
            ))
            return
        
        for py_file in python_files:
            try:
                content = py_file.read_text(encoding="utf-8")
                
                # 语法检查
                try:
                    ast.parse(content)
                except SyntaxError as e:
                    result.issues.append(AnalysisIssue(
                        severity="critical",
                        category="syntax",
                        message=f"Python 语法错误 in {py_file.name}: {e}",
                        line=e.lineno
                    ))
                    continue
                
                # 检查常见代码问题
                self._check_code_quality(result, py_file, content)
                
            except Exception as e:
                result.issues.append(AnalysisIssue(
                    severity="warning",
                    category="syntax",
                    message=f"无法读取 {py_file.name}: {e}"
                ))
    
    def _check_code_quality(self, result: SkillAnalysisResult, file_path: Path, content: str):
        """检查代码质量问题"""
        lines = content.split('\n')
        
        # 检查过长的行
        for i, line in enumerate(lines, 1):
            if len(line) > 120:
                result.issues.append(AnalysisIssue(
                    severity="info",
                    category="style",
                    message=f"{file_path.name} 第 {i} 行过长 ({len(line)} 字符)",
                    line=i,
                    suggestion="建议每行不超过 120 字符"
                ))
        
        # 检查 TODO/FIXME
        todo_pattern = re.compile(r'#\s*(TODO|FIXME|XXX)', re.IGNORECASE)
        for i, line in enumerate(lines, 1):
            if todo_pattern.search(line):
                result.issues.append(AnalysisIssue(
                    severity="info",
                    category="content",
                    message=f"{file_path.name} 第 {i} 行包含 TODO/FIXME",
                    line=i
                ))
        
        # 检查 bare except
        bare_except_pattern = re.compile(r'^\s*except\s*:')
        for i, line in enumerate(lines, 1):
            if bare_except_pattern.search(line):
                result.issues.append(AnalysisIssue(
                    severity="warning",
                    category="style",
                    message=f"{file_path.name} 第 {i} 行使用了 bare except",
                    line=i,
                    suggestion="使用具体的异常类型，如 except ValueError:"
                ))
        
        # 检查 print 语句（生产代码应该使用日志）
        print_pattern = re.compile(r'^\s*print\s*\(')
        for i, line in enumerate(lines, 1):
            if print_pattern.search(line):
                result.issues.append(AnalysisIssue(
                    severity="info",
                    category="style",
                    message=f"{file_path.name} 第 {i} 行使用了 print",
                    line=i,
                    suggestion="考虑使用 logging 模块替代 print"
                ))
    
    def _analyze_structure(self, result: SkillAnalysisResult, skill_path: Path):
        """分析目录结构"""
        # 检查是否有 src 目录或主模块
        has_src = (skill_path / "src").exists()
        has_main_module = (skill_path / f"{result.skill_name.replace('-', '_')}").exists()
        
        if not has_src and not has_main_module:
            result.issues.append(AnalysisIssue(
                severity="info",
                category="structure",
                message="未找到标准的源代码目录结构",
                suggestion="建议创建 src/ 目录或主模块目录"
            ))
        
        # 检查测试目录
        test_dirs = ["tests", "test", "_test"]
        has_tests = any((skill_path / d).exists() for d in test_dirs)
        
        if not has_tests:
            result.issues.append(AnalysisIssue(
                severity="info",
                category="structure",
                message="未找到测试目录",
                suggestion="建议创建 tests/ 目录并添加单元测试"
            ))
        
        # 检查 README
        readme_files = ["README.md", "README.rst", "README.txt"]
        has_readme = any((skill_path / f).exists() for f in readme_files)
        
        if not has_readme:
            result.issues.append(AnalysisIssue(
                severity="info",
                category="structure",
                message="缺少 README 文件",
                suggestion="创建 README.md 文件，包含项目说明和安装指南"
            ))
    
    def _calculate_score(self, result: SkillAnalysisResult) -> int:
        """计算综合评分"""
        score = 100
        
        # 根据问题严重程度扣分
        for issue in result.issues:
            if issue.severity == "critical":
                score -= 20
            elif issue.severity == "warning":
                score -= 10
            elif issue.severity == "info":
                score -= 2
        
        # 基础分调整
        if not result.has_skill_md:
            score -= 30
        if not result.has_package_json:
            score -= 10
        if not result.skill_md_valid:
            score -= 15
        
        return max(0, score)
    
    def _generate_suggestions(self, result: SkillAnalysisResult) -> List[str]:
        """生成改进建议"""
        suggestions = []
        
        # 根据问题生成建议
        critical_count = sum(1 for i in result.issues if i.severity == "critical")
        warning_count = sum(1 for i in result.issues if i.severity == "warning")
        
        if critical_count > 0:
            suggestions.append(f"修复 {critical_count} 个严重问题")
        
        if warning_count > 0:
            suggestions.append(f"处理 {warning_count} 个警告")
        
        if not result.has_skill_md:
            suggestions.append("创建 SKILL.md 文件，包含完整的技能说明")
        
        if result.score < 60:
            suggestions.append("整体代码质量需要改进，建议重构")
        elif result.score < 80:
            suggestions.append("代码质量良好，但仍有改进空间")
        
        if not suggestions:
            suggestions.append("代码质量优秀，继续保持！")
        
        return suggestions
    
    def compare_skills(self, skill_names: List[str]) -> Dict[str, Any]:
        """对比多个技能的质量"""
        results = []
        for name in skill_names:
            result = self.analyze_skill(name)
            results.append(result)
        
        # 按评分排序
        results.sort(key=lambda r: r.score, reverse=True)
        
        return {
            "ranking": [
                {
                    "name": r.skill_name,
                    "score": r.score,
                    "issues": len(r.issues),
                    "critical": sum(1 for i in r.issues if i.severity == "critical")
                }
                for r in results
            ],
            "best": results[0].skill_name if results else None,
            "worst": results[-1].skill_name if results else None,
            "average_score": sum(r.score for r in results) / len(results) if results else 0
        }
