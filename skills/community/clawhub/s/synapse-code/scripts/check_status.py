#!/usr/bin/env python3
"""
check_status.py — 检查项目 Synapse + Pipeline 状态

用法:
    python3 check_status.py /path/to/project

检查内容:
1. .knowledge/ 目录存在性和健康度
2. .synapse/ 目录存在性和 memory 记录数
3. .gitnexus/ 目录存在性和新鲜度
4. Pipeline 项目状态
"""

import sys
import argparse
import subprocess
from pathlib import Path
from datetime import datetime


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 日志输出 (IM 友好格式 - 无 ANSI 颜色码)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def log_info(msg):
    """信息消息 - 用于一般提示"""
    print(f"[INFO] {msg}")

def log_success(msg):
    """成功消息 - 用于完成状态"""
    print(f"[✓] {msg}")

def log_warning(msg):
    """警告消息 - 用于注意点"""
    print(f"[⚠] {msg}")

def log_error(msg):
    """错误消息 - 用于失败状态"""
    print(f"[✗] {msg}")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 检查函数
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


def check_knowledge(project: Path) -> dict:
    """Check Wiki Layer status."""
    knowledge_dir = project / ".knowledge"
    result = {"exists": False, "files": [], "log_entries": 0}

    if not knowledge_dir.exists():
        return result

    result["exists"] = True

    # Check required files
    required_files = ["CLAUDE.md", "log.md", "index.md"]
    for f in required_files:
        if (knowledge_dir / f).exists():
            result["files"].append(f)

    # Count log entries
    log_path = knowledge_dir / "log.md"
    if log_path.exists():
        content = log_path.read_text()
        result["log_entries"] = content.count("## [")

    # Check pages directories
    pages_dir = knowledge_dir / "pages"
    if pages_dir.exists():
        result["pages"] = [d.name for d in pages_dir.iterdir() if d.is_dir()]

    return result


def check_synapse(project: Path) -> dict:
    """Check Synapse memory status."""
    synapse_dir = project / ".synapse"
    result = {"exists": False, "memory_count": 0, "task_types": {}}

    if not synapse_dir.exists():
        return result

    result["exists"] = True

    memory_dir = synapse_dir / "memory"
    if memory_dir.exists():
        for task_type_dir in memory_dir.iterdir():
            if task_type_dir.is_dir():
                count = len(list(task_type_dir.glob("*.md")))
                result["memory_count"] += count
                result["task_types"][task_type_dir.name] = count

    return result


def get_gitnexus_bin() -> str:
    """Get path to gitnexus binary (bundled or global)."""
    # Try bundled version first
    bundled = Path(__file__).parent.parent / "node_modules" / ".bin" / "gitnexus"
    if bundled.exists():
        return str(bundled)
    # Fallback to global
    return "gitnexus"


def check_gitnexus(project: Path) -> dict:
    """Check Code Layer status."""
    gitnexus_dir = project / ".gitnexus"
    result = {"exists": False, "fresh": False, "last_analyzed": None}

    if not gitnexus_dir.exists():
        return result

    result["exists"] = True

    # Check freshness via gitnexus status
    gitnexus_bin = get_gitnexus_bin()
    try:
        proc = subprocess.run(
            [gitnexus_bin, "status"],
            cwd=project,
            capture_output=True,
            text=True,
            timeout=10
        )
        output = proc.stdout.lower()
        result["fresh"] = "up-to-date" in output or "current" in output

        # Try to extract last analyzed time
        for line in proc.stdout.split("\n"):
            if "last analyzed" in line.lower() or "indexed" in line.lower():
                result["last_analyzed"] = line.strip()
    except Exception as e:
        result["error"] = str(e)

    return result


def check_pipeline(project: Path, pipeline_workspace: Path) -> dict:
    """Check Pipeline project status."""
    project_name = project.name
    pipeline_project = pipeline_workspace / project_name
    result = {"exists": False, "phase": "unknown", "contracts": []}

    if not pipeline_project.exists():
        return result

    result["exists"] = True

    # Check contract_board.db
    db_path = pipeline_project / "contract_board.db"
    if db_path.exists():
        result["db_exists"] = True

    # Try to get phase from pipeline status
    try:
        proc = subprocess.run(
            ["python3", "pipeline.py", "status", project_name],
            cwd=pipeline_workspace,
            capture_output=True,
            text=True,
            timeout=10
        )
        output = proc.stdout
        for line in output.split("\n"):
            if "current phase" in line.lower():
                result["phase"] = line.split(":")[-1].strip()
            if "contracts" in line.lower() or "[req]" in line.lower() or "[arch]" in line.lower():
                result["contracts"].append(line.strip())
    except Exception as e:
        result["error"] = str(e)

    return result


def print_status(project_name: str, knowledge: dict, synapse: dict, gitnexus: dict, pipeline: dict):
    """Print formatted status report."""
    print()
    print(f"{'=' * 60}")
    print(f"  Synapse + Pipeline 状态报告")
    print(f"{'=' * 60}")
    print(f"  项目：{project_name}")
    print(f"{'=' * 60}")
    print()

    # Wiki Layer
    print(f"Wiki Layer (.knowledge/)")
    print(f"  ├─ 状态：", end="")
    if knowledge["exists"]:
        print(f"✓ 已初始化")
        print(f"  ├─ 文件：{', '.join(knowledge['files']) if knowledge['files'] else 'None'}")
        print(f"  ├─ 日志条目：{knowledge['log_entries']}")
        if knowledge.get("pages"):
            print(f"  └─ 页面：{', '.join(knowledge['pages'])}")
        else:
            print(f"  └─ 页面：暂无")
    else:
        print(f"✗ 未初始化")
        print(f"  → 运行：/synapse-code init")
    print()

    # Synapse Memory
    print(f"Synapse Memory (.synapse/memory/)")
    print(f"  ├─ 状态：", end="")
    if synapse["exists"]:
        print(f"✓ 已初始化")
        print(f"  ├─ 总记录数：{synapse['memory_count']}")
        for task_type, count in sorted(synapse["task_types"].items()):
            print(f"  │  ├─ {task_type}: {count}")
        print(f"  └─ 使用 --task-type 查询特定类型记录")
    else:
        print(f"✗ 未初始化")
        print(f"  → 运行 Pipeline 后自动创建")
    print()

    # Code Layer
    print(f"Code Layer (.gitnexus/)")
    print(f"  ├─ 状态：", end="")
    if gitnexus["exists"]:
        print(f"✓ 已初始化")
        print(f"  ├─ 新鲜度：", end="")
        if gitnexus.get('fresh'):
            print(f"是 (up-to-date)")
        else:
            print(f"否 (需要更新)")
            print(f"  │  → 运行：gitnexus analyze --force")
        if gitnexus.get("last_analyzed"):
            print(f"  ├─ {gitnexus['last_analyzed']}")
        if gitnexus.get("error"):
            print(f"  └─ 错误：{gitnexus['error']}")
    else:
        print(f"✗ 未初始化")
        print(f"  → 运行：gitnexus analyze --force")
    print()

    # Pipeline
    print(f"Pipeline 状态")
    print(f"  ├─ 项目：", end="")
    if pipeline["exists"]:
        print(f"✓ 已创建")
        print(f"  ├─ 当前阶段：{pipeline['phase']}")
        if pipeline.get("contracts"):
            print(f"  ├─ 合约:")
            for c in pipeline["contracts"][:5]:
                print(f"  │  {c}")
        if pipeline.get("db_exists"):
            print(f"  └─ 数据库：✓")
    else:
        print(f"✗ 未创建")
        print(f"  → 运行 Pipeline 自动创建")
    print()

    print(f"{'=' * 60}")


def print_recommendations(project: Path, knowledge: dict, gitnexus: dict, pipeline: dict):
    """Print recommendations based on status."""
    recommendations = []

    if not knowledge["exists"]:
        recommendations.append(("", "初始化 Wiki 层", f"python3 ~/.claude/skills/synapse-core/scripts/scaffold.py {project}"))
    if not gitnexus["exists"] or not gitnexus.get("fresh"):
        recommendations.append(("", "更新代码图谱", f"cd {project} && gitnexus analyze --force"))
    if not pipeline["exists"]:
        pipeline_workspace = Path.home() / "pipeline-workspace"
        recommendations.append(("", "创建 Pipeline 项目", f"cd {pipeline_workspace} && python3 pipeline.py new {project.name}"))

    if recommendations:
        print(f"\n💡 建议操作:")
        for i, (_, desc, cmd) in enumerate(recommendations, 1):
            print(f"  {i}. {desc}")
            print(f"     → {cmd}")
        print()


def main():
    parser = argparse.ArgumentParser(
        description="检查项目 Synapse + Pipeline 状态",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python3 check_status.py ~/my-project
  python3 check_status.py /path/to/project --verbose
        """
    )
    parser.add_argument("project", help="项目根目录路径")
    parser.add_argument("--verbose", "-v", action="store_true", help="详细输出")
    args = parser.parse_args()

    project = Path(args.project).resolve()

    if not project.exists():
        log_error(f"项目目录不存在：{project}")
        sys.exit(1)

    pipeline_workspace = Path.home() / "pipeline-workspace"

    log_info(f"检查项目：{project}")
    print()

    # Run all checks
    knowledge = check_knowledge(project)
    synapse = check_synapse(project)
    gitnexus = check_gitnexus(project)
    pipeline = check_pipeline(project, pipeline_workspace)

    # Print status report
    print_status(project.name, knowledge, synapse, gitnexus, pipeline)

    # Print recommendations
    print_recommendations(project, knowledge, gitnexus, pipeline)


if __name__ == "__main__":
    main()
