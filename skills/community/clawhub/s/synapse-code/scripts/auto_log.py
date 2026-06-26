#!/usr/bin/env python3
"""
auto_log.py — Synapse 自动记录脚本（内置版本）

用法:
    python3 auto_log.py --input /tmp/pipeline_summary.json --project /path/to/project
    cat /tmp/pipeline_summary.json | python3 auto_log.py --project /path/to/project

输入格式 (pipeline summary JSON):
{
  "project": "amber-hunter",
  "tasks": [
    {
      "id": "2a",
      "task_type": "refactor",
      "description": "修 test_status_returns_version 版本号过时",
      "outcome": "success|failure",
      "commit": "acb6cb5",
      "qa_result": "2 passed",
      "timestamp": "2026-04-07T21:45:00+08:00"
    }
  ]
}

输出:
  - .synapse/memory/{task_type}/{timestamp}-{slug}.md
  - 追加一行到 .knowledge/log.md
"""

import sys
import json
import argparse
from pathlib import Path
from datetime import datetime


MEMORY_TEMPLATE = """# Synapse 执行记录

task_type: {task_type}
task_description: {description}
matched_trigger: {task_type}
condition_checked: repo has .synapse/ index
actions_used: []

outcome: {outcome}
{qa_line}
{commit_line}
timestamp: {timestamp}
"""


def slugify(text: str) -> str:
    """把描述转成 URL-safe slug"""
    import re
    text = re.sub(r"[^\w\s]", "", text)
    text = re.sub(r"\s+", "-", text.strip())
    return text[:40]


def write_memory_record(project: Path, task: dict) -> Path:
    """写单个 task 的 memory record"""
    task_type = task.get("task_type", "unknown")
    timestamp = task.get("timestamp", datetime.now().isoformat())

    try:
        dt = datetime.fromisoformat(timestamp)
        ts_filename = dt.strftime("%Y-%m-%dT%H-%M-%S")
    except ValueError:
        ts_filename = timestamp[:19].replace(":", "-")

    slug = slugify(task.get("description", "unnamed"))
    filename = f"{ts_filename}-{slug}.md"

    memory_dir = project / ".synapse" / "memory" / task_type
    memory_dir.mkdir(parents=True, exist_ok=True)

    filepath = memory_dir / filename

    qa_line = f"qa_result: {task['qa_result']}" if task.get("qa_result") else ""
    commit_line = f"commit: {task['commit']}" if task.get("commit") else ""

    content = MEMORY_TEMPLATE.format(
        task_type=task_type,
        description=task.get("description", ""),
        outcome=task.get("outcome", "unknown"),
        qa_line=qa_line,
        commit_line=commit_line,
        timestamp=timestamp,
    )

    filepath.write_text(content.strip() + "\n")
    return filepath


def append_log(knowledge_dir: Path, task: dict):
    """追加一行到 log.md"""
    if not knowledge_dir.exists():
        return

    log_path = knowledge_dir / "log.md"
    timestamp = task.get("timestamp", datetime.now().isoformat())
    try:
        dt = datetime.fromisoformat(timestamp)
        ts = dt.strftime("%Y-%m-%d %H:%M")
    except ValueError:
        ts = timestamp[:16]

    task_type = task.get("task_type", "unknown")
    description = task.get("description", "")

    entry = f"## [{ts}] {task_type} | {description}\n"
    with open(log_path, "a") as f:
        f.write(entry)


def main():
    parser = argparse.ArgumentParser(description="Synapse auto-log")
    parser.add_argument("--input", help="pipeline summary JSON 文件路径")
    parser.add_argument("--project", required=True, help="项目根目录")
    args = parser.parse_args()

    project = Path(args.project).resolve()

    if args.input:
        with open(args.input) as f:
            data = json.load(f)
    else:
        data = json.load(sys.stdin)

    tasks = data.get("tasks", [])
    if not tasks:
        print("No tasks to log")
        return

    written = []
    for task in tasks:
        fp = write_memory_record(project, task)
        written.append(fp)
        print(f"  memory: {fp.relative_to(project)}")

        knowledge_dirs = [
            project / ".knowledge",
            project / ".synapse",  # fallback: write to synapse memory log
        ]
        for kd in knowledge_dirs:
            log_path = kd / "log.md"
            if log_path.exists():
                append_log(kd, task)
                print(f"  log: {kd.name}/log.md")
                break

    print(f"\nDone: {len(written)} record(s) written")


if __name__ == "__main__":
    main()
