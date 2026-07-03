"""
Web 安全审计引擎 —— 扫描源码目录，识别漏洞
"""
from __future__ import annotations
import os
import sys
from typing import List, Dict, Tuple
from pathlib import Path

# 将当前包目录加入 path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from rules import (
    AuditRule, Finding, get_rules, ALL_RULES,
    PHP_RULES, JAVA_RULES, PYTHON_RULES, GO_RULES, COMMON_RULES
)


def detect_language(file_path: str) -> str | None:
    """根据文件后缀判断语言"""
    ext = Path(file_path).suffix.lower()
    mapping = {
        ".php": "php", ".phtml": "php", ".php3": "php", ".php4": "php",
        ".php5": "php", ".inc": "php",
        ".java": "java", ".jsp": "java", ".jspx": "java",
        ".py": "python", ".pyw": "python",
        ".go": "go",
        ".js": "javascript", ".ts": "typescript",
        ".html": "html", ".htm": "html", ".jinja2": "python", ".j2": "python",
    }
    return mapping.get(ext, None)


def collect_files(root_dir: str) -> List[str]:
    """递归收集目录下所有源码文件"""
    target_exts = {
        ".php", ".phtml", ".php3", ".php4", ".php5", ".inc",
        ".java", ".jsp", ".jspx",
        ".py", ".pyw",
        ".go",
        ".js", ".ts", ".jsx", ".tsx",
        ".html", ".htm", ".jinja2", ".j2",
        ".yml", ".yaml", ".xml", ".json", ".properties",
        ".rb", ".pl", ".sh",
    }
    files = []
    for dirpath, dirnames, filenames in os.walk(root_dir):
        # 跳过常见排除目录
        dirnames[:] = [d for d in dirnames if d not in {
            "node_modules", "vendor", ".git", "__pycache__", ".venv",
            "venv", ".idea", ".vscode", "dist", "build", "target",
            ".mvn", ".gradle", "egg-info", ".egg", ".tox",
        }]
        for f in filenames:
            ext = Path(f).suffix.lower()
            if ext in target_exts:
                files.append(os.path.join(dirpath, f))
    return files


def scan_file(file_path: str, rules: List[AuditRule]) -> List[Finding]:
    """对单个文件应用规则扫描"""
    findings: List[Finding] = []
    try:
        with open(file_path, "r", encoding="utf-8", errors="replace") as fh:
            lines = fh.readlines()
    except Exception:
        return findings

    file_ext = Path(file_path).suffix.lower()
    for rule in rules:
        if file_ext not in rule.file_extensions:
            continue
        for pattern in rule.patterns:
            for idx, line in enumerate(lines, start=1):
                if pattern.search(line):
                    findings.append(Finding(
                        rule=rule,
                        file_path=file_path,
                        line_number=idx,
                        line_content=line.strip()[:200],
                        matched_pattern=pattern.pattern[:120],
                    ))
    return findings


def audit_directory(root_dir: str, language: str | None = None) -> Dict[str, List[Finding]]:
    """
    审计指定目录，返回按文件分组的漏洞发现。
    language: None 表示自动检测，或指定 php/java/python/go
    """
    files = collect_files(root_dir)
    results: Dict[str, List[Finding]] = {}

    for file_path in files:
        lang = language or detect_language(file_path)
        rules = get_rules(lang) if lang else COMMON_RULES
        file_findings = scan_file(file_path, rules)
        if file_findings:
            results[file_path] = file_findings

    return results


def findings_by_severity(findings: List[Finding]) -> Dict[str, List[Finding]]:
    """按严重程度分组"""
    groups: Dict[str, List[Finding]] = {"Critical": [], "High": [], "Medium": [], "Low": []}
    for f in findings:
        groups.setdefault(f.rule.severity, []).append(f)
    return groups


def findings_summary(all_results: Dict[str, List[Finding]]) -> Dict:
    """生成统计摘要"""
    total_files = len(all_results)
    total_findings = 0
    severity_counts = {"Critical": 0, "High": 0, "Medium": 0, "Low": 0}
    category_counts: Dict[str, int] = {}

    for findings in all_results.values():
        total_findings += len(findings)
        for f in findings:
            severity_counts[f.rule.severity] = severity_counts.get(f.rule.severity, 0) + 1
            category_counts[f.rule.category] = category_counts.get(f.rule.category, 0) + 1

    return {
        "total_files_scanned": total_files,
        "total_findings": total_findings,
        "severity_counts": severity_counts,
        "category_counts": category_counts,
    }
