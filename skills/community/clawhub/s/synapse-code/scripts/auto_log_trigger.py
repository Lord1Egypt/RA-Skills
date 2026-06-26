#!/usr/bin/env python3
"""
auto_log_trigger.py — 触发 Synapse auto-log（配置化版本）

用法:
    python3 auto_log_trigger.py /path/to/project
    python3 auto_log_trigger.py --project /path/to/project
    cat /tmp/pipeline_summary.json | python3 auto_log_trigger.py --project /path/to/project

功能:
1. 检查 /tmp/pipeline_summary.json 是否存在
2. 调用内置 auto_log.py 写入 memory 和 log.md
3. 实验评估（测试覆盖率、回归测试等）
"""

import sys
import json
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


def log_json(data: dict, prefix: str = ""):
    """结构化日志输出 (JSON 格式)"""
    timestamp = datetime.now().isoformat()
    log_entry = {
        "timestamp": timestamp,
        **data
    }
    if prefix:
        log_entry["prefix"] = prefix
    print(json.dumps(log_entry, ensure_ascii=False))


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 实验评估逻辑（只读、不阻塞主流程）
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def load_config() -> dict:
    """Load configuration from config.json or use defaults."""
    config_file = Path(__file__).parent / "config.json"
    default_config = {
        "paths": {
            "pipeline_summary": "/tmp/pipeline_summary.json"
        },
        "synapse": {
            "knowledge_dir": ".knowledge",
            "memory_dir": ".synapse/memory"
        },
        "evaluation": {
            "test_coverage_threshold": 80,
            "require_regression_pass": True
        }
    }

    if config_file.exists():
        try:
            with open(config_file) as f:
                config = json.load(f)
                # Merge with defaults
                for key in default_config:
                    if key not in config:
                        config[key] = default_config[key]
                return config
        except (json.JSONDecodeError, IOError) as e:
            print(f"Warning: Could not load config.json, using defaults: {e}")

    return default_config


def evaluate_experiment(summary_path: Path, config: dict) -> dict:
    """
    评估实验结果（只读、不阻塞主流程）

    Args:
        summary_path: pipeline_summary.json 路径
        config: 配置字典

    Returns:
        dict: 评估结果 {passed, score, reasons, suggestions}
    """
    try:
        with open(summary_path) as f:
            summary = json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        return {
            "passed": False,
            "score": 0,
            "reasons": [f"无法读取 Pipeline 摘要：{e}"],
            "suggestions": ["请确认 Pipeline 已成功运行"]
        }

    reasons = []
    suggestions = []

    # 获取配置阈值
    coverage_threshold = config.get("evaluation", {}).get("test_coverage_threshold", 80)
    require_regression = config.get("evaluation", {}).get("require_regression_pass", True)

    # 安全提取测试覆盖率（兼容多种 JSON 结构）
    coverage = 0
    if "qa" in summary:
        coverage = summary["qa"].get("test_coverage", 0)
    elif "test_coverage" in summary:
        coverage = summary["test_coverage"]

    # 安全提取回归测试结果
    regression_passed = False
    if "qa" in summary:
        regression_result = summary["qa"].get("regression_tests", "")
        regression_passed = "passed" in str(regression_result).lower() or regression_result is True
    elif "regression_passed" in summary:
        regression_passed = summary["regression_passed"]

    # 评估逻辑
    score = coverage  # 简化：分数 = 覆盖率

    # 检查覆盖率
    if coverage >= coverage_threshold:
        reasons.append(f"✓ 测试覆盖率 {coverage}% ≥ {coverage_threshold}%")
    else:
        reasons.append(f"○ 测试覆盖率 {coverage}% < {coverage_threshold}%")
        suggestions.append(f"建议提升测试覆盖率至 {coverage_threshold}% 以上")

    # 检查回归测试
    if require_regression:
        if regression_passed:
            reasons.append("✓ 回归测试通过")
        else:
            reasons.append("○ 回归测试未通过或未执行")
            suggestions.append("建议修复失败的回归测试")

    # 判断是否"通过"（仅供参考，不阻塞流程）
    passed = coverage >= coverage_threshold and (not require_regression or regression_passed)

    return {
        "passed": passed,
        "score": score,
        "reasons": reasons,
        "suggestions": suggestions
    }


def update_program_log(project: Path, evaluation: dict):
    """
    更新 program.md 的实验日志（如果存在）

    Args:
        project: 项目根目录
        evaluation: 评估结果
    """
    program_path = project / "program.md"
    if not program_path.exists():
        return

    try:
        content = program_path.read_text()

        # 检查是否已有实验日志表格
        if "| 日期 |" not in content:
            # 没有找到表格，不修改
            return

        # 追加新记录
        today = datetime.now().strftime("%Y-%m-%d")
        score = evaluation.get("score", 0)
        status = "✅" if evaluation.get("passed") else "⚠️"

        # 简单追加（实际使用可能需要更复杂的表格解析）
        new_line = f"| {today} | 自动记录 | {status} | {score}% | 见 log.md 详情 |\n"

        # 找到表格最后位置
        lines = content.split("\n")
        for i, line in enumerate(lines):
            if line.startswith("|-"):
                # 在分隔线后插入
                lines.insert(i + 1, new_line.strip())
                break

        program_path.write_text("\n".join(lines))

    except Exception as e:
        log_warning(f"更新 program.md 失败：{e}")


def check_pipeline_summary(config: dict) -> tuple[bool, Path]:
    """Check if pipeline_summary.json exists."""
    summary_path = Path(config.get("paths", {}).get("pipeline_summary", "/tmp/pipeline_summary.json"))
    return summary_path.exists() and summary_path.stat().st_size > 0, summary_path


def run_auto_log(project: Path, summary_path: Path) -> bool:
    """Run built-in auto_log.py with the pipeline summary."""
    # Use built-in auto_log.py from the same directory
    auto_log_script = Path(__file__).parent / "auto_log.py"

    if not auto_log_script.exists():
        print(f"Error: auto_log.py not found at {auto_log_script}")
        print("This is a critical file — please reinstall synapse-code skill.")
        return False

    try:
        result = subprocess.run(
            ["python3", str(auto_log_script), "--input", str(summary_path), "--project", str(project)],
            capture_output=True,
            text=True,
            check=True
        )
        print(f"[Auto-Log] {result.stdout.strip()}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"[Auto-Log Error] {e.stderr}")
        return False
    except Exception as e:
        print(f"[Auto-Log Error] Unexpected error: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description="触发 Synapse auto-log（配置化版本）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python3 auto_log_trigger.py /path/to/project
  python3 auto_log_trigger.py --project /path/to/project
  cat /tmp/pipeline_summary.json | python3 auto_log_trigger.py --project /path/to/project
        """
    )
    parser.add_argument("project", nargs="?", help="项目根目录路径")
    parser.add_argument("--project", dest="project_flag", help="项目根目录路径（带 flag）")
    args = parser.parse_args()

    project_path = args.project_flag or args.project
    if not project_path:
        parser.print_help()
        sys.exit(1)

    project = Path(project_path).resolve()

    # Load configuration
    config = load_config()

    if not project.exists():
        log_error(f"项目目录不存在：{project}")
        sys.exit(1)

    print(f"\n{'=' * 60}")
    print(f"  Synapse Auto-Log")
    print(f"{'=' * 60}")
    print(f"  项目：{project}")
    print(f"{'=' * 60}\n")

    # Check pipeline summary
    print(f"[⟳] [1/2] 检查 Pipeline 摘要...")
    has_summary, summary_path = check_pipeline_summary(config)
    if not has_summary:
        log_error("/tmp/pipeline_summary.json 未找到或为空")
        log_info("请确认 Pipeline 已成功运行")
        sys.exit(1)
    log_success(f"Pipeline 摘要：{summary_path}")

    # Run auto-log
    print(f"[⟳] [2/2] 执行知识沉淀...")
    if not run_auto_log(project, summary_path):
        log_error("知识沉淀失败")
        sys.exit(1)
    log_success("知识沉淀完成")

    # 实验评估（可选，不阻塞主流程）
    print()
    log_info("正在评估实验结果...")
    evaluation = evaluate_experiment(summary_path, config)

    if evaluation.get("passed"):
        log_success(f"实验评估通过 (得分：{evaluation.get('score', 0)}%)")
    else:
        log_warning(f"实验评估未通过 (得分：{evaluation.get('score', 0)}%)")

    for reason in evaluation.get("reasons", []):
        print(f"  {reason}")

    if evaluation.get("suggestions"):
        print()
        log_info("改进建议:")
        for suggestion in evaluation.get("suggestions", []):
            print(f"  • {suggestion}")

    # 更新 program.md 实验日志（如果存在）
    update_program_log(project, evaluation)

    print(f"\n{'=' * 60}")
    log_success("Synapse 知识记录完成!")
    print()
    print(f"  查看记录:")
    print(f"  cat {project}/.knowledge/log.md")
    print(f"  cat {project}/.synapse/memory/*/*.md")


if __name__ == "__main__":
    main()
