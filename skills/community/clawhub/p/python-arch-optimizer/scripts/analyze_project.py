#!/usr/bin/env python3
"""
Python 项目结构分析脚本
分析项目目录结构，识别架构问题并生成优化建议
"""

import os
import sys
import json
from pathlib import Path
from collections import defaultdict

def analyze_project(project_path: str) -> dict:
    """分析项目结构并返回报告"""
    project = Path(project_path)
    
    if not project.exists():
        return {"error": f"路径不存在：{project_path}"}
    
    report = {
        "project_name": project.name,
        "root": str(project.absolute()),
        "structure": {},
        "issues": [],
        "suggestions": []
    }
    
    # 扫描目录结构
    report["structure"] = scan_directory(project)
    
    # 检查常见问题
    check_python_structure(project, report)
    check_dependencies(project, report)
    check_tests(project, report)
    check_config(project, report)
    
    return report


def scan_directory(path: Path, depth: int = 0, max_depth: int = 5) -> dict:
    """递归扫描目录结构"""
    if depth > max_depth:
        return {"...": "max depth reached"}
    
    result = {"type": "dir", "children": {}}
    
    try:
        items = sorted(path.iterdir(), key=lambda x: (x.is_file(), x.name))
        for item in items:
            if item.name.startswith((".", "__pycache__", ".git", "node_modules")):
                continue
            
            if item.is_dir():
                result["children"][item.name] = scan_directory(item, depth + 1, max_depth)
            else:
                result["children"][item.name] = {
                    "type": "file",
                    "size": item.stat().st_size
                }
    except PermissionError:
        pass
    
    return result


def check_python_structure(project: Path, report: dict):
    """检查 Python 项目结构问题"""
    src_dirs = list(project.glob("src"))
    package_dirs = list(project.glob("*")) 
    
    # 检查是否有 src 布局
    has_src = len(src_dirs) > 0 and src_dirs[0].is_dir()
    
    # 检查 __init__.py
    missing_init = []
    for py_dir in project.rglob("*"):
        if py_dir.is_dir() and any(py_dir.glob("*.py")):
            if not (py_dir / "__init__.py").exists():
                if py_dir.name not in ["tests", "scripts", "docs"]:
                    missing_init.append(str(py_dir.relative_to(project)))
    
    if missing_init:
        report["issues"].append({
            "type": "missing_init",
            "severity": "medium",
            "message": f"缺少 __init__.py 的目录：{len(missing_init)} 个",
            "details": missing_init[:5]  # 只显示前 5 个
        })
        report["suggestions"].append("为包目录添加 __init__.py 文件")
    
    # 检查目录深度
    max_depth = 0
    for item in project.rglob("*"):
        if item.is_dir():
            depth = len(item.relative_to(project).parts)
            max_depth = max(max_depth, depth)
    
    if max_depth > 5:
        report["issues"].append({
            "type": "deep_nesting",
            "severity": "low",
            "message": f"目录嵌套过深：{max_depth} 层"
        })
        report["suggestions"].append("考虑扁平化目录结构，减少嵌套层级")


def check_dependencies(project: Path, report: dict):
    """检查依赖管理"""
    has_pyproject = (project / "pyproject.toml").exists()
    has_requirements = (project / "requirements.txt").exists()
    has_setup = (project / "setup.py").exists() or (project / "setup.cfg").exists()
    
    if not (has_pyproject or has_requirements or has_setup):
        report["issues"].append({
            "type": "no_dependency_file",
            "severity": "high",
            "message": "缺少依赖管理文件"
        })
        report["suggestions"].append("添加 pyproject.toml 或 requirements.txt 管理依赖")
    elif not has_pyproject and has_requirements:
        report["suggestions"].append("考虑迁移到 pyproject.toml (PEP 517/518)")


def check_tests(project: Path, report: dict):
    """检查测试配置"""
    tests_dir = project / "tests"
    test_files = list(project.glob("test_*.py")) + list(project.glob("*_test.py"))
    
    if not tests_dir.exists() and not test_files:
        report["issues"].append({
            "type": "no_tests",
            "severity": "high",
            "message": "没有发现测试目录或测试文件"
        })
        report["suggestions"].append("创建 tests/ 目录并添加单元测试")
    elif tests_dir.exists():
        test_count = len(list(tests_dir.glob("test_*.py")))
        if test_count == 0:
            report["issues"].append({
                "type": "empty_tests",
                "severity": "medium",
                "message": "tests/ 目录存在但没有测试文件"
            })


def check_config(project: Path, report: dict):
    """检查配置文件"""
    config_files = [
        ".pre-commit-config.yaml",
        "pyproject.toml",
        ".black.toml",
        "setup.cfg",
        ".ruff.toml"
    ]
    
    missing_configs = []
    for cfg in config_files:
        if not (project / cfg).exists():
            missing_configs.append(cfg)
    
    if len(missing_configs) > 2:
        report["suggestions"].append(f"考虑添加工程化配置：{', '.join(missing_configs[:3])}")


def print_report(report: dict, format: str = "text"):
    """打印分析报告"""
    if "error" in report:
        print(f"❌ {report['error']}")
        return
    
    print(f"\n📊 项目分析报告：{report['project_name']}")
    print(f"📁 路径：{report['root']}\n")
    
    # 问题汇总
    if report["issues"]:
        print("⚠️  发现的问题:")
        for issue in report["issues"]:
            severity_icon = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(issue["severity"], "⚪")
            print(f"  {severity_icon} [{issue['severity'].upper()}] {issue['message']}")
    else:
        print("✅ 未发现明显问题")
    
    # 建议
    if report["suggestions"]:
        print("\n💡 优化建议:")
        for i, suggestion in enumerate(report["suggestions"], 1):
            print(f"  {i}. {suggestion}")
    
    print()


def main():
    if len(sys.argv) < 2:
        print("用法：python analyze_project.py <项目路径> [--json]")
        sys.exit(1)
    
    project_path = sys.argv[1]
    as_json = "--json" in sys.argv
    
    report = analyze_project(project_path)
    
    if as_json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print_report(report)


if __name__ == "__main__":
    main()
